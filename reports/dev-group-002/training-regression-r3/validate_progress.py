#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path


def main() -> int:
    path = Path(__file__).with_name("progress.json")
    obj = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    expected_cases = [f"DEV-EXAMPLE-{i:03d}" for i in range(1, 6)]
    rows = obj.get("cases", [])
    if obj.get("case_count") != 5 or obj.get("question_count") != 25:
        errors.append("group cardinality mismatch")
    if [row.get("case_id") for row in rows] != expected_cases:
        errors.append("case order or identity mismatch")
    if sum(row.get("physical_selector_count", 0) for row in rows) != 32:
        errors.append("physical selector total mismatch")
    if sum(row.get("source_call_count", 0) for row in rows) != 64:
        errors.append("source call total mismatch")
    if any(row.get("source_confirmed_exact_top1_count") != 0 for row in rows):
        errors.append("unsupported source-confirmed exact result")
    if any(row.get("machine_valid_local_seals") != 0 for row in rows):
        errors.append("false machine-valid local seal claim")
    totals = obj.get("totals", {})
    for field in ("source_confirmed_exact_top1_count", "machine_valid_local_seals", "s03_fusions", "formal_valid_questions"):
        if totals.get(field) != 0:
            errors.append(f"{field} must remain zero")
    r1 = obj.get("r1_training_regression_score", {})
    if (r1.get("top1"), r1.get("top2"), r1.get("status")) != (
        "25/25", "25/25", "ANSWER_VISIBLE_ALIGNMENT_NOT_SOURCE_GROUNDED"
    ):
        errors.append("R1 training score boundary changed")
    baseline = obj.get("original_blind_baseline", {})
    if (baseline.get("top1"), baseline.get("top2"), baseline.get("status")) != (
        "11/25", "16/25", "PRESERVED_NOT_OVERWRITTEN"
    ):
        errors.append("original blind baseline changed")
    if obj.get("new_case_admission") != "BLOCKED":
        errors.append("new case admission must remain blocked")
    result = {
        "schema": "DEV-GROUP-002-R3-PROGRESS-VALIDATION-V1",
        "status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "errors": errors,
        "case_count": len(rows),
        "question_count": 25,
        "physical_selector_count": 32,
        "source_call_count": 64,
        "source_confirmed_exact_top1_count": 0,
        "machine_valid_local_seals": 0,
        "s03_fusions": 0,
        "formal_valid_questions": 0,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
