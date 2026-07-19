#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from fortune_v1.bootstrap_request import (
    build_preauthorized_request,
    create_group_clean_start_from_bootstrap_request,
)
from fortune_v1.end_to_end import validate_staged_clean_start
from fortune_v1.staged_access import harden_clean_start
from fortune_v1.util import atomic_write_json, read_json, sha256_file

SIGNAL_SCHEMA = "GROUP-RUNTIME-START-SIGNAL-V1"
RECEIPT_SCHEMA = "GROUP-RUNTIME-START-SIGNAL-RECEIPT-V1"
ALLOWED_FIELDS = {"schema", "status", "group", "session", "mode"}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def object_hash(value: dict[str, Any]) -> str:
    body = dict(value)
    body.pop("object_hash", None)
    return hashlib.sha256(canonical_bytes(body)).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def execute(signal_path: Path, pointer_path: Path) -> dict[str, Any]:
    require(signal_path.is_file(), f"signal missing: {signal_path}")
    require(signal_path.parent.as_posix() == "runtime/group-start-signals", "signal directory invalid")
    require(signal_path.suffix == ".json", "signal extension invalid")

    signal = read_json(signal_path)
    require(set(signal) == ALLOWED_FIELDS, f"signal fields invalid: {sorted(signal)}")
    require(signal.get("schema") == SIGNAL_SCHEMA, "signal schema invalid")
    require(signal.get("status") == "REQUESTED", "signal status invalid")
    require(signal.get("group") == "DEV-GROUP-002", "signal group invalid")
    require(signal.get("mode") in {"CHAT_ONLY", "WORK"}, "signal mode invalid")
    session_id = signal.get("session")
    require(isinstance(session_id, str) and bool(session_id), "signal session invalid")

    group_run_id = signal_path.stem
    require(group_run_id.startswith("GROUP-RUN-"), "group run identifier invalid")
    pointer = read_json(pointer_path)
    require(pointer.get("group_id") == signal.get("group"), "signal does not match active group")
    require(pointer.get("status") == "ACTIVE", "active group pointer status invalid")
    require(pointer.get("answer_payload_present") is False, "active group pointer payload boundary invalid")
    require(pointer.get("runtime_answer_scan") == "PASS", "active group pointer scan invalid")

    request_path = Path("runtime/clean-start-requests") / f"{group_run_id}.json"
    clean_path = Path("data/group-clean-starts") / group_run_id / "clean-start.json"
    receipt_path = Path("reports/clean-start-preauthorization") / f"{group_run_id}.json"
    for path in (request_path, clean_path, receipt_path):
        require(not path.exists(), f"immutable output already exists: {path}")

    request_result = build_preauthorized_request(
        pointer_path,
        request_path,
        group_run_id,
        session_id,
        str(signal["mode"]),
    )
    clean_result = harden_clean_start(
        create_group_clean_start_from_bootstrap_request(request_path, pointer_path)
    )
    require(clean_path.is_file(), "clean-start file was not materialized")
    validation = validate_staged_clean_start(clean_path)
    require(validation.get("status") == "PASS", f"clean-start validation failed: {validation}")

    clean = read_json(clean_path)
    require(clean.get("status") == "READY_FOR_PREBLIND_MODELING", "clean-start status invalid")
    require(clean.get("group_run_id") == group_run_id, "clean-start identifier mismatch")
    require(clean.get("answer_data_available") is False, "clean-start payload boundary invalid")
    cases = clean.get("cases", [])
    require(len(cases) == 5, "clean-start case count invalid")
    require(
        [row.get("case_id") for row in cases] == [f"DEV-EXAMPLE-{index:03d}" for index in range(1, 6)],
        "clean-start case order invalid",
    )

    request = read_json(request_path)
    require(request.get("schema") == "GROUP-CLEAN-START-REQUEST-V2", "generated request schema invalid")
    require(request.get("request_origin") == "PREAUTHORIZED_ENGINEERING_BOOTSTRAP", "generated request origin invalid")
    for key in (
        "prediction_context_started",
        "prediction_context_repository_search_used",
        "prediction_context_commit_history_used",
        "prediction_context_old_run_objects_visible",
    ):
        require(request.get(key) is False, f"generated request flag invalid: {key}")
    expected_entrypoint = clean_path.as_posix()
    require(request.get("future_prediction_entrypoint") == expected_entrypoint, "future entrypoint invalid")
    require(
        request.get("future_prediction_first_repository_action") == "FETCH_EXACT_CLEAN_START_PATH_ONLY",
        "future first action invalid",
    )

    receipt = {
        "schema": RECEIPT_SCHEMA,
        "status": "PASS",
        "group": signal["group"],
        "group_run_id": group_run_id,
        "session_id": session_id,
        "mode": signal["mode"],
        "signal_path": signal_path.as_posix(),
        "signal_sha256": sha256_file(signal_path),
        "request_path": request_path.as_posix(),
        "request_sha256": sha256_file(request_path),
        "clean_start_path": clean_path.as_posix(),
        "clean_start_sha256": sha256_file(clean_path),
        "case_count": 5,
        "question_count_total": 25,
        "runtime_validation_status": validation["status"],
        "prediction_context_started": False,
        "future_prediction_first_repository_action": "FETCH_EXACT_CLEAN_START_PATH_ONLY",
        "formal_prediction_status": "NOT_STARTED_REQUIRES_FRESH_PREDICTION_CONTEXT",
        "score_eligibility": "NONE_BEFORE_PREDICTION_FREEZE_AND_CAUSAL_USE_RECEIPT",
        "request_result_status": request_result["status"],
        "clean_result_status": clean_result["status"],
    }
    receipt["object_hash"] = object_hash(receipt)
    atomic_write_json(receipt_path, receipt)
    return {**receipt, "receipt_path": receipt_path.as_posix()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--signal", required=True)
    parser.add_argument("--current-group-manifest", default="CURRENT_GROUP_MANIFEST")
    args = parser.parse_args()
    result = execute(Path(args.signal), Path(args.current_group_manifest))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
