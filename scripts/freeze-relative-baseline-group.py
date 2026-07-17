#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

ALLOWED_OPTIONS = {"A", "B", "C", "D"}
FORBIDDEN_KEYS = {
    "answer", "answers", "correct", "correct_option", "correct_answer",
    "literal_answer_vector", "answer_vector",
}
FORBIDDEN_TEXT = ("正确答案：", "正确答案:", "literal_answer_vector", "answer_vector")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def scan(value: Any, path: str = "$") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            if key_text.lower() in FORBIDDEN_KEYS or ("答案" in key_text and key_text != "answer_isolation"):
                findings.append(f"{path}.{key_text}:FORBIDDEN_KEY")
            findings.extend(scan(child, f"{path}.{key_text}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(scan(child, f"{path}[{index}]"))
    elif isinstance(value, str):
        for token in FORBIDDEN_TEXT:
            if token in value:
                findings.append(f"{path}:FORBIDDEN_TEXT:{token}")
    return findings


def validate(obj: dict[str, Any], expected_group: str, expected_cases: int, expected_questions: int) -> list[str]:
    errors: list[str] = []
    if obj.get("schema") != "RELATIVE-BASELINE-GROUP-V1":
        errors.append("SCHEMA_INVALID")
    if obj.get("group_id") != expected_group:
        errors.append("GROUP_ID_MISMATCH")
    if obj.get("dataset_type") != "DEV":
        errors.append("DATASET_TYPE_INVALID")
    if obj.get("answer_payload_used") is not False:
        errors.append("ANSWER_PAYLOAD_ATTESTATION_INVALID")
    if obj.get("answer_visibility") != "PHYSICALLY_INACCESSIBLE":
        errors.append("ANSWER_VISIBILITY_INVALID")
    audit = obj.get("audit", {})
    if audit.get("answer_files_read") != 0:
        errors.append("ANSWER_FILES_READ_NONZERO")
    if audit.get("release_class") != "LOW_VALIDITY_FORCED_CHOICE":
        errors.append("RELEASE_CLASS_INVALID")
    if obj.get("formal_exact_assertion_status") != "NULL_WHERE_EXACT_ENDPOINT_NOT_CLOSED":
        errors.append("FORMAL_EXACT_ASSERTION_STATUS_INVALID")
    run_id = obj.get("run_id")
    if not isinstance(run_id, str) or not re.fullmatch(r"[A-Za-z0-9._-]+", run_id):
        errors.append("RUN_ID_INVALID")
    cases = obj.get("cases")
    if not isinstance(cases, list) or len(cases) != expected_cases:
        errors.append("CASE_COUNT_INVALID")
        cases = []
    seen_cases: set[str] = set()
    total = 0
    for case in cases:
        case_id = case.get("case_id")
        if not isinstance(case_id, str) or case_id in seen_cases:
            errors.append("CASE_ID_INVALID_OR_DUPLICATE")
            continue
        seen_cases.add(case_id)
        questions = case.get("questions")
        if not isinstance(questions, list) or len(questions) != 5:
            errors.append(f"{case_id}:QUESTION_COUNT_INVALID")
            continue
        seen_q: set[str] = set()
        for q in questions:
            total += 1
            qid = q.get("question_id")
            if not isinstance(qid, str) or qid in seen_q:
                errors.append(f"{case_id}:QUESTION_ID_INVALID_OR_DUPLICATE")
                continue
            seen_q.add(qid)
            top1, top2 = q.get("top1"), q.get("top2")
            if top1 not in ALLOWED_OPTIONS or top2 not in ALLOWED_OPTIONS or top1 == top2:
                errors.append(f"{case_id}:{qid}:TOP1_TOP2_INVALID")
            confidence = q.get("confidence")
            if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
                errors.append(f"{case_id}:{qid}:CONFIDENCE_INVALID")
            if q.get("status") != "LOW_VALIDITY_FORCED_CHOICE":
                errors.append(f"{case_id}:{qid}:STATUS_INVALID")
    if total != expected_questions or obj.get("question_count_total") != expected_questions:
        errors.append("QUESTION_TOTAL_INVALID")
    findings = scan(obj)
    if findings:
        errors.extend(f"ANSWER_LEAK:{item}" for item in findings)
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prediction", required=True, type=Path)
    parser.add_argument("--frozen-root", required=True, type=Path)
    parser.add_argument("--expected-group", default="DEV-GROUP-002")
    parser.add_argument("--expected-cases", type=int, default=5)
    parser.add_argument("--expected-questions", type=int, default=25)
    args = parser.parse_args()

    raw = args.prediction.read_bytes()
    obj = json.loads(raw.decode("utf-8"))
    errors = validate(obj, args.expected_group, args.expected_cases, args.expected_questions)
    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    run_id = obj["run_id"]
    target = args.frozen_root / run_id
    if target.exists():
        print(json.dumps({"status": "FAIL", "errors": ["RUN_ID_ALREADY_EXISTS"]}, ensure_ascii=False, indent=2))
        raise SystemExit(3)
    target.mkdir(parents=True)

    frozen = target / "relative-baseline-group.json"
    frozen_bytes = canonical_bytes(obj)
    frozen.write_bytes(frozen_bytes)
    os.chmod(frozen, 0o444)

    receipt = {
        "schema": "RELATIVE-BASELINE-GROUP-FREEZE-RECEIPT-V1",
        "status": "PASS",
        "freeze_status": "RELATIVE_BASELINE_GROUP_FROZEN",
        "group_id": obj["group_id"],
        "run_id": run_id,
        "release_class": "LOW_VALIDITY_FORCED_CHOICE",
        "formal_prediction_run_validity": "NOT_CLAIMED",
        "answer_data_available": False,
        "answer_files_read": 0,
        "question_count_total": obj["question_count_total"],
        "case_count": len(obj["cases"]),
        "source_prediction_path": args.prediction.as_posix(),
        "source_prediction_sha256": sha256_bytes(raw),
        "frozen_prediction_path": frozen.as_posix(),
        "frozen_prediction_sha256": sha256_bytes(frozen_bytes),
        "immutable": True,
        "non_overwrite": True,
        "validator": "scripts/freeze-relative-baseline-group.py",
        "validator_version": 1,
    }
    receipt_path = target / "freeze-receipt.json"
    receipt_bytes = canonical_bytes(receipt)
    receipt_path.write_bytes(receipt_bytes)
    os.chmod(receipt_path, 0o444)
    print(receipt_bytes.decode("utf-8"), end="")


if __name__ == "__main__":
    main()
