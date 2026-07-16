#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import binascii
import gzip
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


READY_STATES = {"READY_FOR_BASELINE_PREDICTION", "BASELINE_PENDING"}
HOLD_STATES = {
    "GROUP_HOLD",
    "HOLD_SOURCE_REIMPORT_REQUIRED",
    "GROUP_HOLD_SOURCE_REIMPORT_REQUIRED",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(obj: Any) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode(
        "utf-8"
    )


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def materialize(path: Path) -> tuple[Any, bytes]:
    stored = path.read_bytes()
    if path.name.endswith(".json"):
        raw = stored
    elif path.name.endswith(".json.gz.b64"):
        encoded = "".join(stored.decode("ascii").split())
        if len(encoded) % 4:
            raise ValueError(f"invalid Base64 length {len(encoded)}")
        try:
            compressed = base64.b64decode(encoded, validate=True)
        except binascii.Error as exc:
            raise ValueError(f"strict Base64 decode failed: {exc}") from exc
        try:
            raw = gzip.decompress(compressed)
        except Exception as exc:  # noqa: BLE001 - receipt must preserve concrete failure
            raise ValueError(f"gzip integrity check failed: {type(exc).__name__}: {exc}") from exc
    else:
        raise ValueError("unsupported storage format")
    return json.loads(raw.decode("utf-8")), stored


def validate_case(group_id: str, root: Path, row: dict[str, Any]) -> dict[str, Any]:
    path = root.parent.parent / row["path"] if not Path(row["path"]).is_absolute() else Path(row["path"])
    result: dict[str, Any] = {
        "case_id": row.get("case_id"),
        "path": row.get("path"),
        "declared_integrity_status": row.get("integrity_status", "UNDECLARED"),
        "status": "FAIL",
    }
    if not path.is_file():
        result["error"] = "MISSING_CASE_FILE"
        return result

    stored = path.read_bytes()
    result["actual_stored_bytes"] = len(stored)
    result["actual_stored_sha256"] = sha256_bytes(stored)
    result["declared_stored_bytes"] = row.get("stored_bytes")
    result["declared_stored_sha256"] = row.get("stored_sha256")
    result["stored_bytes_match"] = row.get("stored_bytes") == len(stored)
    result["stored_sha256_match"] = row.get("stored_sha256") == result["actual_stored_sha256"]

    try:
        obj, _stored = materialize(path)
        logical = canonical_json_bytes(obj)
        result["materialization"] = "PASS"
        result["actual_logical_json_sha256"] = sha256_bytes(logical)
        result["declared_logical_json_sha256"] = row.get("logical_json_sha256")
        result["logical_sha256_match"] = (
            row.get("logical_json_sha256") == result["actual_logical_json_sha256"]
        )
        isolation = obj.get("answer_isolation", {})
        result["answer_payload_present"] = isolation.get("answer_payload_present")
        result["answer_reference_disclosed"] = isolation.get("answer_reference_disclosed")
        result["question_count"] = obj.get("questions", {}).get("question_count")
        result["case_id_match"] = obj.get("case_id") == row.get("case_id")
        result["group_id_match"] = obj.get("group_id") == group_id
        result["answer_isolation_pass"] = (
            isolation.get("answer_payload_present") is False
            and isolation.get("answer_reference_disclosed") is False
        )
        result["question_count_match"] = (
            obj.get("questions", {}).get("question_count") == row.get("question_count")
        )
    except Exception as exc:  # noqa: BLE001 - exact failure belongs in audit receipt
        result["materialization"] = "FAIL"
        result["error"] = f"{type(exc).__name__}: {exc}"
        result["logical_sha256_match"] = False
        result["answer_isolation_pass"] = False
        result["question_count_match"] = False
        result["case_id_match"] = False
        result["group_id_match"] = False

    checks = [
        result["stored_bytes_match"],
        result["stored_sha256_match"],
        result["materialization"] == "PASS",
        result["logical_sha256_match"],
        result["answer_isolation_pass"],
        result["question_count_match"],
        result["case_id_match"],
        result["group_id_match"],
    ]
    result["status"] = "PASS" if all(checks) else "FAIL"
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("group_root")
    parser.add_argument("--allow-hold", action="store_true")
    parser.add_argument("--require-ready", action="store_true")
    parser.add_argument("--receipt")
    args = parser.parse_args()

    root = Path(args.group_root)
    receipt: dict[str, Any] = {
        "schema": "TRAINING-GROUP-INTEGRITY-RECEIPT-V2",
        "group_root": str(root),
        "answer_repository_accessed": False,
        "status": "FAIL",
        "errors": [],
    }
    try:
        head = read_json(root / "HEAD.json")
        manifest = read_json(root / "manifest.json")
        revision_path = root.parent.parent / head["path"]
        revision = read_json(revision_path)
        group_id = manifest["group_id"]
        receipt.update(
            {
                "group_id": group_id,
                "head_revision": head["revision"],
                "head_path": head["path"],
                "manifest_status": manifest.get("status"),
                "revision_status": revision.get("status"),
                "declared_case_count": manifest.get("case_count"),
                "declared_question_count": manifest.get("question_count_total"),
            }
        )

        if revision.get("revision") != head.get("revision"):
            receipt["errors"].append("HEAD_REVISION_MISMATCH")
        if revision.get("group_id") != group_id:
            receipt["errors"].append("GROUP_ID_MISMATCH")
        if manifest.get("answer_payload_present") is not False:
            receipt["errors"].append("MANIFEST_ANSWER_PAYLOAD_NOT_FALSE")
        if manifest.get("case_count") != len(manifest.get("cases", [])):
            receipt["errors"].append("CASE_COUNT_MISMATCH")
        if sum(row.get("question_count", 0) for row in manifest.get("cases", [])) != manifest.get(
            "question_count_total"
        ):
            receipt["errors"].append("QUESTION_COUNT_TOTAL_MISMATCH")

        case_results = [validate_case(group_id, root, row) for row in manifest.get("cases", [])]
        receipt["cases"] = case_results
        receipt["materialized_case_count"] = sum(
            1 for row in case_results if row.get("materialization") == "PASS"
        )
        receipt["fully_valid_case_count"] = sum(
            1 for row in case_results if row.get("status") == "PASS"
        )
        receipt["failed_case_ids"] = [
            row.get("case_id") for row in case_results if row.get("status") != "PASS"
        ]

        manifest_state = manifest.get("status")
        revision_state = revision.get("status")
        state_is_ready = manifest_state in READY_STATES or revision_state in READY_STATES
        state_is_hold = manifest_state in HOLD_STATES or revision_state in HOLD_STATES
        all_cases_valid = len(case_results) == manifest.get("case_count") and all(
            row.get("status") == "PASS" for row in case_results
        )

        if args.require_ready and not state_is_ready:
            receipt["errors"].append("GROUP_NOT_READY")
        if state_is_ready and not all_cases_valid:
            receipt["errors"].append("FALSE_READY_WITH_INVALID_CASES")
        if state_is_hold:
            if not args.allow_hold:
                receipt["errors"].append("GROUP_IS_HOLD")
            if revision.get("reveal_authorized") is not False:
                receipt["errors"].append("HOLD_REVEAL_AUTHORIZATION_NOT_FALSE")
            if revision.get("baseline_freezes") not in ({}, None):
                receipt["errors"].append("HOLD_BASELINE_FREEZES_NOT_EMPTY")
            if not receipt["failed_case_ids"]:
                receipt["errors"].append("HOLD_WITHOUT_FAILED_CASES")
        if not state_is_ready and not state_is_hold:
            receipt["errors"].append("UNKNOWN_GROUP_STATE")

        if not receipt["errors"]:
            receipt["status"] = (
                "PASS_READY" if state_is_ready else "PASS_HOLD_FAIL_CLOSED"
            )
            return_code = 0
        else:
            return_code = 1
    except Exception as exc:  # noqa: BLE001
        receipt["errors"].append(f"VALIDATOR_EXCEPTION:{type(exc).__name__}:{exc}")
        return_code = 1

    if args.receipt:
        Path(args.receipt).parent.mkdir(parents=True, exist_ok=True)
        Path(args.receipt).write_text(
            json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    else:
        print(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2))
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
