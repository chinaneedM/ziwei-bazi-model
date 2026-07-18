#!/usr/bin/env python3
from __future__ import annotations
import itertools, json
from pathlib import Path


def score(top1: str, top2: str, answer: str) -> tuple[int, int]:
    return sum(a == b for a, b in zip(top1, answer)), sum(c in (a, b) for a, b, c in zip(top1, top2, answer))


def main() -> int:
    obj = json.loads(Path(__file__).with_name("compact-manifest.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    expected = [f"DEV-EXAMPLE-{i:03d}" for i in range(1, 6)]
    if [c.get("case_id") for c in obj.get("cases", [])] != expected:
        errors.append("case order mismatch")
    total1 = total2 = pairs = 0
    for case in obj.get("cases", []):
        ranks = case.get("ranks", [])
        if len(ranks) != 5:
            errors.append(case["case_id"] + ": rank count")
            continue
        top1 = "".join(r[0] for r in ranks)
        top2 = "".join(r[1] for r in ranks)
        if top1 != case.get("top1_vector") or top2 != case.get("top2_vector"):
            errors.append(case["case_id"] + ": vector derivation")
        for rank in ranks:
            if sorted(rank) != list("ABCD"):
                errors.append(case["case_id"] + ": invalid rank")
            for left, right in itertools.combinations("ABCD", 2):
                _winner = left if rank.index(left) < rank.index(right) else right
                pairs += 1
        h1, h2 = score(top1, top2, case["answer_vector"])
        if (h1, h2) != (case["top1_hits"], case["top2_coverage"]):
            errors.append(case["case_id"] + ": score mismatch")
        total1 += h1
        total2 += h2
    if (pairs, total1, total2) != (150, 14, 16):
        errors.append("aggregate recomputation mismatch")
    totals = obj.get("totals", {})
    if totals.get("score_label") != "TRAINING_REGRESSION_SCORE":
        errors.append("score label")
    if (totals.get("top1_hits"), totals.get("top2_coverage"), totals.get("pairwise_row_count")) != (14, 16, 150):
        errors.append("declared totals")
    if obj.get("run_class") != "ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD":
        errors.append("run class")
    if obj.get("local_seal_status") != "DIAGNOSTIC_RELATIVE_ORDER_NOT_MACHINE_SEALED":
        errors.append("seal boundary")
    for field in ("formal_valid_questions", "machine_valid_local_seals", "s03_fusions"):
        if totals.get(field) != 0:
            errors.append(field + " must remain zero")
    base = obj["comparison"]["original_blind_baseline"]
    if (base["top1_hits"], base["top2_coverage"], base["status"]) != (11, 16, "PRESERVED_NOT_OVERWRITTEN"):
        errors.append("original baseline changed")
    if obj.get("new_case_admission") != "BLOCKED":
        errors.append("new-case gate")
    result = {
        "schema": "DEV-GROUP-002-R4-VALIDATION-V1",
        "status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "errors": errors,
        "question_count": 25,
        "pairwise_row_count": pairs,
        "top1_hits": total1,
        "top2_coverage": total2,
        "score_label": "TRAINING_REGRESSION_SCORE",
        "formal_valid_questions": 0,
        "machine_valid_local_seals": 0,
        "s03_fusions": 0,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
