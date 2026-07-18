#!/usr/bin/env python3
"""Validate the DEV-GROUP-002 training regression manifest.

The manifest is answer-visible, same-case SHADOW_REBUILD data. Passing this
validator proves deterministic training-regression structure only. It does not
prove blind accuracy, formal local seals, S03 fusion, or generalization.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path


def score(top1: str, top2: str, answer: str) -> tuple[int, int]:
    return (
        sum(p == a for p, a in zip(top1, answer)),
        sum(a in (p, q) for p, q, a in zip(top1, top2, answer)),
    )


def validate(manifest: dict, patch_spec: dict) -> list[str]:
    errors: list[str] = []

    if manifest.get("score_label") != "TRAINING_REGRESSION_SCORE":
        errors.append("same-case score must be labeled TRAINING_REGRESSION_SCORE")
    if manifest.get("run_class") != "ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD":
        errors.append("run_class must preserve answer-visible shadow status")
    if manifest.get("original_prediction_mutated") is not False:
        errors.append("original prediction must remain immutable")

    declared = manifest["baseline"]["user_declared_r1"]
    if (declared["top1_hits"], declared["top2_coverage"]) != (11, 16):
        errors.append("declared R1 44%/64% baseline changed")

    total_repo_top1 = total_repo_top2 = 0
    total_shadow_top1 = total_shadow_top2 = 0
    generated_pairwise = 0

    cases = manifest.get("cases", {})
    if sorted(cases) != [f"DEV-EXAMPLE-{i:03d}" for i in range(1, 6)]:
        errors.append("manifest must contain exactly DEV-EXAMPLE-001 through 005")

    for case_id, case in sorted(cases.items()):
        for field in ("repository_top1", "repository_top2", "answer", "shadow_top1", "shadow_top2"):
            if len(case.get(field, "")) != 5:
                errors.append(f"{case_id}: {field} must contain five options")

        repo1, repo2 = score(case["repository_top1"], case["repository_top2"], case["answer"])
        shadow1, shadow2 = score(case["shadow_top1"], case["shadow_top2"], case["answer"])
        total_repo_top1 += repo1
        total_repo_top2 += repo2
        total_shadow_top1 += shadow1
        total_shadow_top2 += shadow2

        ranks = case.get("ranks", [])
        if len(ranks) != 5:
            errors.append(f"{case_id}: expected five rank rows")
            continue

        for q_index, rank in enumerate(ranks, start=1):
            if sorted(rank) != list("ABCD"):
                errors.append(f"{case_id} Q{q_index}: rank is not a permutation of ABCD")
                continue
            if case["shadow_top1"][q_index - 1] != rank[0]:
                errors.append(f"{case_id} Q{q_index}: shadow TOP1 not derived from rank")
            if case["shadow_top2"][q_index - 1] != rank[1]:
                errors.append(f"{case_id} Q{q_index}: shadow TOP2 not derived from rank")

            pair_rows = []
            for left, right in itertools.combinations("ABCD", 2):
                winner = left if rank.index(left) < rank.index(right) else right
                pair_rows.append((left, right, winner))
            if len(pair_rows) != 6:
                errors.append(f"{case_id} Q{q_index}: pairwise expansion failed")
            generated_pairwise += len(pair_rows)

    baseline = manifest["baseline"]
    if (total_repo_top1, total_repo_top2) != (
        baseline["current_repo_vectors_recomputed"]["top1_hits"],
        baseline["current_repo_vectors_recomputed"]["top2_coverage"],
    ):
        errors.append("current repository vector score does not recompute")
    if (total_shadow_top1, total_shadow_top2) != (25, 25):
        errors.append("shadow training regression must recompute to 25/25")
    if generated_pairwise != 150:
        errors.append(f"expected 150 mechanically generated pairwise rows, got {generated_pairwise}")

    aggregate = manifest["aggregate"]
    if aggregate["generated_pairwise_rows"] != generated_pairwise:
        errors.append("aggregate pairwise count mismatch")
    if aggregate["formal_valid_question_count"] != 0:
        errors.append("formal validity must remain zero until machine-valid local seals exist")
    if aggregate["formal_dual_track_status"] != "HOLD":
        errors.append("formal dual-track status must remain HOLD")
    if manifest["new_case_admission"] != "BLOCKED_UNTIL_FORMAL_STABILITY":
        errors.append("new case admission must remain blocked")

    general_text = "\n".join(p["general_rule"] for p in patch_spec.get("patches", []))
    forbidden = patch_spec["leakage_scan"]["forbidden_tokens_checked"]
    leaked = [token for token in forbidden if token in general_text]
    if leaked:
        errors.append("case-specific leakage in generic rules: " + ", ".join(leaked))

    if patch_spec.get("base_astrological_knowledge_changed") is not False:
        errors.append("base astrological knowledge change is forbidden")
    if patch_spec.get("case_specific_direction_rule_added") is not False:
        errors.append("case-specific direction rule is forbidden")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    patch_spec = json.loads((root / "generic-patch-spec.json").read_text(encoding="utf-8"))
    errors = validate(manifest, patch_spec)
    result = {
        "schema": "DEV-GROUP-002-TRAINING-REGRESSION-VALIDATION-V1",
        "scope": "DETERMINISTIC_TRAINING_REGRESSION_STRUCTURE_ONLY",
        "status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "errors": errors,
        "generated_pairwise_rows": 150 if not errors else None,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
