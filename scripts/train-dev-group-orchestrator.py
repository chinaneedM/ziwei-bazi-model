#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8"))


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_freeze(receipt: dict[str, Any], expected_group: str, expected_run: str) -> None:
    required = {
        "status": "PASS",
        "freeze_status": "RELATIVE_BASELINE_GROUP_FROZEN",
        "group_id": expected_group,
        "run_id": expected_run,
        "answer_data_available": False,
        "answer_files_read": 0,
        "immutable": True,
        "non_overwrite": True,
    }
    for key, expected in required.items():
        if receipt.get(key) != expected:
            raise SystemExit(f"freeze receipt mismatch: {key}")
    frozen = ROOT / receipt["frozen_prediction_path"]
    if not frozen.exists() or sha256_file(frozen) != receipt["frozen_prediction_sha256"]:
        raise SystemExit("frozen prediction hash mismatch")


def build_request(receipt_path: Path, group_id: str, run_id: str, output: Path) -> dict[str, Any]:
    receipt = load(receipt_path)
    verify_freeze(receipt, group_id, run_id)
    request = {
        "schema": "REVERSE-GRADING-REQUEST-V1",
        "group_id": group_id,
        "run_id": run_id,
        "freeze_receipt_path": receipt_path.relative_to(ROOT).as_posix(),
        "freeze_receipt_sha256": sha256_file(receipt_path),
        "frozen_prediction_path": receipt["frozen_prediction_path"],
        "frozen_prediction_sha256": receipt["frozen_prediction_sha256"],
        "question_count_total": receipt["question_count_total"],
        "case_count": receipt["case_count"],
        "requested_operations": [
            "ANSWER_VECTOR_LITERAL_REPLAY",
            "TOP1_TOP2_SCORING",
            "ERROR_CLASSIFICATION",
            "LEGAL_REGRESSION_INPUT",
        ],
        "answer_data_requested_in_runtime_repository": False,
        "status": "READY_FOR_PRIVATE_VAULT",
    }
    write_json(output, request)
    return request


def verify_response(request_path: Path, response_path: Path, secret: str) -> dict[str, Any]:
    request = load(request_path)
    response = load(response_path)
    if response.get("schema") != "REVERSE-GRADING-RESPONSE-V1":
        raise SystemExit("response schema invalid")
    if response.get("group_id") != request["group_id"] or response.get("run_id") != request["run_id"]:
        raise SystemExit("response identity mismatch")
    if response.get("request_sha256") != sha256_file(request_path):
        raise SystemExit("response request hash mismatch")
    signature = response.pop("signature_hmac_sha256", None)
    expected = hmac.new(secret.encode("utf-8"), canonical_bytes(response), hashlib.sha256).hexdigest()
    if not signature or not hmac.compare_digest(signature, expected):
        raise SystemExit("response signature invalid")
    response["signature_hmac_sha256"] = signature
    if response.get("status") != "PASS":
        raise SystemExit("private vault grading did not pass")
    if response.get("answer_vectors_included") is not False:
        raise SystemExit("response leaked answer vectors")
    return response


def finalize(request_path: Path, response_path: Path, secret: str, output_root: Path) -> dict[str, Any]:
    response = verify_response(request_path, response_path, secret)
    output_root.mkdir(parents=True, exist_ok=True)
    write_json(output_root / "verified-grading-response.json", response)
    report = {
        "schema": "DEV-GROUP-AUTOMATION-FINAL-REPORT-V1",
        "group_id": response["group_id"],
        "run_id": response["run_id"],
        "status": "COMPLETED",
        "freeze_status": "PASS",
        "literal_replay_status": response.get("literal_replay_status"),
        "top1_score": response.get("top1_score"),
        "top2_score": response.get("top2_score"),
        "question_count_total": response.get("question_count_total"),
        "diagnosis_path": response.get("diagnosis_path"),
        "regression_path": response.get("regression_path"),
        "answer_vectors_persisted_in_runtime_repository": False,
        "private_vault_response_sha256": sha256_file(response_path),
    }
    write_json(output_root / "final-report.json", report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    p1 = sub.add_parser("request")
    p1.add_argument("--group-id", required=True)
    p1.add_argument("--run-id", required=True)
    p1.add_argument("--freeze-receipt", required=True, type=Path)
    p1.add_argument("--output", required=True, type=Path)
    p2 = sub.add_parser("finalize")
    p2.add_argument("--request", required=True, type=Path)
    p2.add_argument("--response", required=True, type=Path)
    p2.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args()

    if args.command == "request":
        result = build_request(args.freeze_receipt, args.group_id, args.run_id, args.output)
    else:
        secret = os.environ.get("FORTUNE_GRADING_HMAC_SECRET")
        if not secret:
            raise SystemExit("FORTUNE_GRADING_HMAC_SECRET missing")
        result = finalize(args.request, args.response, secret, args.output_root)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
