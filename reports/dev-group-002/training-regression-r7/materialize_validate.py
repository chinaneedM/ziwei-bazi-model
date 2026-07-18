#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

ROUND_DIR = Path("reports/dev-group-002/training-regression-r7")
HISTORY = {
    "R1": "reports/dev-group-002/training-regression-r1/manifest.json",
    "R2": "reports/dev-group-002/training-regression-r2/formal-readiness-matrix.json",
    "R3": "reports/dev-group-002/training-regression-r3/progress.json",
    "R4": "reports/dev-group-002/training-regression-r4/compact-manifest.json",
    "R5": "reports/dev-group-002/training-regression-r5/manifest.json",
    "R6": "reports/dev-group-002/training-regression-r6/manifest.json",
}
INPUTS = {
    "r2_source_spec": "reports/dev-group-002/training-regression-r2/source-excerpt-spec.json",
    "r3_dev001": "reports/dev-group-002/training-regression-r3/DEV-EXAMPLE-001/source-grounded-replay.json",
    "r5_prediction": "reports/dev-group-002/training-regression-r5/prediction-freeze.json",
    "r5_review": "reports/dev-group-002/training-regression-r5/postreveal-review.json",
    "r6_manifest": HISTORY["R6"],
}
TARGET_CASE_ID = "DEV-EXAMPLE-001"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_payload(obj: dict[str, Any]) -> bytes:
    clone = dict(obj)
    clone.pop("canonical_sha256", None)
    return (json.dumps(clone, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def canonical_hash(obj: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_payload(obj)).hexdigest()


def with_hash(obj: dict[str, Any]) -> dict[str, Any]:
    clone = dict(obj)
    clone["canonical_sha256"] = canonical_hash(clone)
    return clone


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8") + data).hexdigest()


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def normalized_call_id(call: dict[str, Any]) -> str:
    if call.get("source_atom_id"):
        return call["source_atom_id"]
    return f"{call['library']}@line:{call['source_line']}"


ZIWEI_BINDINGS: dict[str, dict[str, dict[str, Any]]] = {
    "Q1": {
        option: {
            "parent_ids": ["S06-ZZ60-A-560001", "S07-RAT-ABU", "FAMILY_MAGNITUDE_CHAIN", "PARENT_PERSON_ROUTE_REQUIRED"],
            "direction_status": "UNKNOWN_WITH_NEUTRAL_PARENT_SCENE",
            "supported_atoms": [],
            "partial_atoms": [],
            "limited_atoms": ["FAMILY_MAGNITUDE_OR_PARENT_OCCUPATION_ENDPOINT_MISSING"],
            "contradicted_atoms": [],
            "semantic_reason": "The parent-palace physical structure and the failed fire/bell condition do not distinguish wealth magnitude or either parent's exact occupation.",
        }
        for option in "ABCD"
    },
    "Q2": {
        "A": {
            "parent_ids": ["S07-RAT-2VA", "S07-RAT-2VE", "S07-RAT-2VG", "OCCUPATION_MARRIAGE_SURGERY_CHAINS", "MENTAL_HEALTH_AND_DEATH_CHAINS"],
            "direction_status": "LIMITED_BY_RELATION_CHANGE_SCENE",
            "supported_atoms": [],
            "partial_atoms": [],
            "limited_atoms": ["ONE_MARRIAGE_COUNT_NOT_CLOSED"],
            "contradicted_atoms": [],
            "semantic_reason": "Relationship disturbance does not determine that exactly one legal marriage occurred.",
        },
        "B": {
            "parent_ids": ["S07-RAT-2VA", "S07-RAT-2VE", "S07-RAT-2VG", "OCCUPATION_MARRIAGE_SURGERY_CHAINS"],
            "direction_status": "PARTIALLY_SUPPORTED",
            "supported_atoms": [],
            "partial_atoms": ["RELATIONSHIP_CHANGE_OR_MULTIPLE_STAGE_PRECONDITION"],
            "limited_atoms": ["TWO_LEGAL_MARRIAGE_ENDPOINTS_MISSING"],
            "contradicted_atoms": [],
            "semantic_reason": "The spouse-system sources support recurring change or trouble, but not two completed legal marriages.",
        },
        "C": {
            "parent_ids": ["S07-RAT-2VA", "S07-RAT-2VE", "S07-RAT-2VG", "OCCUPATION_MARRIAGE_SURGERY_CHAINS"],
            "direction_status": "UNKNOWN_WITH_RELATION_SCENE",
            "supported_atoms": [],
            "partial_atoms": [],
            "limited_atoms": ["LIFETIME_NEVER_MARRIED_ENDPOINT_MISSING"],
            "contradicted_atoms": [],
            "semantic_reason": "A spouse-palace source does not prove that marriage actually occurred and therefore cannot directly contradict lifetime non-marriage.",
        },
        "D": {
            "parent_ids": ["S07-RAT-2VA", "S07-RAT-2VE", "S07-RAT-2VG", "MENTAL_HEALTH_AND_DEATH_CHAINS"],
            "direction_status": "UNKNOWN_WITH_RELATION_SCENE",
            "supported_atoms": [],
            "partial_atoms": [],
            "limited_atoms": ["HUSBAND_DEATH_ENDPOINT_MISSING"],
            "contradicted_atoms": [],
            "semantic_reason": "Relationship trouble cannot be promoted to the husband's death.",
        },
    },
    "Q3": {
        "A": {
            "parent_ids": ["S07-RAT-832", "S07-RAT-833", "MARRIAGE_YEAR_AND_ACTUAL_OCCUPATION"],
            "direction_status": "LIMITED_BY_WORK_SCENE",
            "supported_atoms": [],
            "partial_atoms": [],
            "limited_atoms": ["NO_WORK_LIFETIME_OR_YOUTH_STATUS_NOT_CLOSED"],
            "contradicted_atoms": [],
            "semantic_reason": "Career-source activity and institutional-work tendencies limit but do not directly contradict a no-work claim.",
        },
        "B": {
            "parent_ids": ["ZZZA-A-0925", "S07-RAT-832", "MARRIAGE_YEAR_AND_ACTUAL_OCCUPATION"],
            "direction_status": "PARTIALLY_SUPPORTED",
            "supported_atoms": [],
            "partial_atoms": ["PERFORMANCE_OR_SINGING_DANCING_TALENT_SCENE"],
            "limited_atoms": ["YOUTH_SELLING_PERFORMANCE_FOR_LIVELIHOOD_ENDPOINT_MISSING"],
            "contradicted_atoms": [],
            "semantic_reason": "Performance talent is a precondition for earning through performance, not proof of the exact livelihood.",
        },
        "C": {
            "parent_ids": ["S07-RAT-833", "MARRIAGE_YEAR_AND_ACTUAL_OCCUPATION"],
            "direction_status": "DIRECTLY_CONTRADICTED_MATERIAL_ATOM",
            "supported_atoms": [],
            "partial_atoms": [],
            "limited_atoms": ["PARENTAL_SUPPORT_AND_BUSINESS_ENDPOINTS_MISSING"],
            "contradicted_atoms": ["SELF_EMPLOYED_BUSINESS_OR_ENTREPRENEURSHIP"],
            "semantic_reason": "The source explicitly states that this career system is not suited to self-run business, directly opposing the entrepreneurship atom.",
        },
        "D": {
            "parent_ids": ["ZZZA-A-0925", "S07-RAT-832", "MARRIAGE_YEAR_AND_ACTUAL_OCCUPATION"],
            "direction_status": "PARTIALLY_SUPPORTED",
            "supported_atoms": [],
            "partial_atoms": ["DANCE_OR_PERFORMANCE_TALENT_SCENE"],
            "limited_atoms": ["DANCER_OCCUPATION_AND_HARDSHIP_CAUSATION_ENDPOINTS_MISSING"],
            "contradicted_atoms": [],
            "semantic_reason": "Dance talent supports a scene candidate but not the exact dancer occupation or hardship cause.",
        },
    },
    "Q4": {
        option: {
            "parent_ids": ["R3-DEV001-TIME-1980", "ZIWEI_NEUTRAL_TIME_BEFORE_OPTIONS", "BAZI_NEUTRAL_TIME_BEFORE_OPTIONS"],
            "direction_status": "UNKNOWN_WITH_NEUTRAL_TIME_PERMISSION",
            "supported_atoms": [],
            "partial_atoms": [],
            "limited_atoms": ["HETEROGENEOUS_EVENT_TYPE_AND_ENDPOINT_MISSING"],
            "contradicted_atoms": [],
            "semantic_reason": "The neutral 1980 time fact permits change or conflict but does not distinguish marriage, traffic accident, robbery injury, or windfall.",
        }
        for option in "ABCD"
    },
    "Q5": {
        "A": {
            "parent_ids": ["R3-DEV001-TIME-1993", "REALITY_CHAIN_LEVELS"],
            "direction_status": "UNKNOWN_WITH_NEUTRAL_TIME_PERMISSION",
            "supported_atoms": [],
            "partial_atoms": [],
            "limited_atoms": ["BENEFACTOR_AND_GAIN_ENDPOINTS_MISSING"],
            "contradicted_atoms": [],
            "semantic_reason": "The 1993 time fact does not identify a benefactor, receipt action, or gain endpoint.",
        },
        "B": {
            "parent_ids": ["R3-DEV001-TIME-1993", "S07-RAT-2VA", "S07-RAT-2VE", "S07-RAT-2VG", "MENTAL_HEALTH_AND_DEATH_CHAINS"],
            "direction_status": "PARTIALLY_SUPPORTED",
            "supported_atoms": [],
            "partial_atoms": ["SPOUSE_OR_RELATIONSHIP_ACTOR_SCENE"],
            "limited_atoms": ["HUSBAND_ILLNESS_AND_DEATH_ENDPOINTS_MISSING"],
            "contradicted_atoms": [],
            "semantic_reason": "Spouse-system disturbance and a relationship/loss year partially identify the spouse scene, but do not prove illness or death.",
        },
        "C": {
            "parent_ids": ["R3-DEV001-TIME-1993", "OCCUPATION_MARRIAGE_SURGERY_CHAINS"],
            "direction_status": "UNKNOWN_WITH_NEUTRAL_TIME_PERMISSION",
            "supported_atoms": [],
            "partial_atoms": [],
            "limited_atoms": ["TRAFFIC_ACCIDENT_HOSPITALIZATION_AND_SURGERY_ENDPOINTS_MISSING"],
            "contradicted_atoms": [],
            "semantic_reason": "General health or loss activation does not identify traffic injury, hospitalization, or surgery.",
        },
        "D": {
            "parent_ids": ["R3-DEV001-TIME-1993", "S06-ZZ60-A-560001", "PARENT_PERSON_ROUTE_REQUIRED", "MENTAL_HEALTH_AND_DEATH_CHAINS"],
            "direction_status": "UNKNOWN_WITH_PARENT_SCENE",
            "supported_atoms": [],
            "partial_atoms": [],
            "limited_atoms": ["FATHER_ACTOR_ILLNESS_AND_DEATH_ENDPOINTS_MISSING"],
            "contradicted_atoms": [],
            "semantic_reason": "A parent-palace structure cannot identify the father as actor or prove illness and death in 1993.",
        },
    },
}

STRENGTH = {
    "DIRECTLY_CONTRADICTED_MATERIAL_ATOM": -1,
    "UNKNOWN_WITH_NEUTRAL_PARENT_SCENE": 0,
    "UNKNOWN_WITH_RELATION_SCENE": 0,
    "UNKNOWN_WITH_NEUTRAL_TIME_PERMISSION": 0,
    "UNKNOWN_WITH_PARENT_SCENE": 0,
    "LIMITED_BY_RELATION_CHANGE_SCENE": 0,
    "LIMITED_BY_WORK_SCENE": 0,
    "PARTIALLY_SUPPORTED": 1,
}


def build_objects(repo_root: Path) -> dict[str, Any]:
    r2_source_spec = read_json(repo_root / INPUTS["r2_source_spec"])
    dev001 = read_json(repo_root / INPUTS["r3_dev001"])
    r5_prediction = read_json(repo_root / INPUTS["r5_prediction"])
    r5_review = read_json(repo_root / INPUTS["r5_review"])
    r6_manifest = read_json(repo_root / INPUTS["r6_manifest"])

    if r6_manifest.get("status") != "FROZEN_AUDIT_HOLD":
        raise ValueError("R6 provenance audit is not frozen")

    excerpt_index = {entry["excerpt_id"]: entry for entry in r2_source_spec["entries"]}
    source_calls = {normalized_call_id(call): call for call in dev001["source_calls"]}
    expected_source_ids = {
        "S06-ZZ60-A-550001", "S06-ZZ60-A-560001", "S06-ZZ60-A-590001", "S06-ZZ60-A-570001",
        "S07-RAT-2VA", "S07-RAT-2VE", "S07-RAT-2VG", "S07-RAT-832", "S07-RAT-833", "ZZZA-A-0925", "S07-RAT-ABU",
        "S16@line:1079", "S16@line:1171", "S16@line:1316",
    }
    if set(source_calls) != expected_source_ids:
        raise ValueError("DEV-EXAMPLE-001 R3 source-call identity changed")

    source_registry_rows: list[dict[str, Any]] = []
    for call_id, call in sorted(source_calls.items()):
        text = call["required_text"]
        source_registry_rows.append(
            {
                "call_id": call_id,
                "library": call["library"],
                "purpose": call["purpose"],
                "required_text": text,
                "required_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "capability_ceiling": call.get("capability_ceiling", "SOURCE_STATED_SCOPE_ONLY"),
                "applicability": call.get("applicability", "CALLED_IN_R3"),
                "parent_artifact": INPUTS["r3_dev001"],
                "parent_artifact_git_blob_sha": git_blob_sha(repo_root / INPUTS["r3_dev001"]),
            }
        )

    for synthetic_id, year in (("R3-DEV001-TIME-1980", 1980), ("R3-DEV001-TIME-1993", 1993)):
        fact = next(row for row in dev001["neutral_time_facts"] if row["year"] == year)
        source_registry_rows.append(
            {
                "call_id": synthetic_id,
                "library": "S10_S15_NEUTRAL_TIME_OBJECT",
                "purpose": f"Option-neutral time fact for {year}",
                "required_text": json.dumps(fact, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
                "required_text_sha256": hashlib.sha256(json.dumps(fact, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest(),
                "capability_ceiling": "TEMPORAL_STAGE_CANDIDATE_ONLY",
                "applicability": "CALLED_IN_R3",
                "parent_artifact": INPUTS["r3_dev001"],
                "parent_artifact_git_blob_sha": git_blob_sha(repo_root / INPUTS["r3_dev001"]),
            }
        )

    generic_parent_ids = {
        parent_id
        for question in ZIWEI_BINDINGS.values()
        for spec in question.values()
        for parent_id in spec["parent_ids"]
        if parent_id not in source_calls and not parent_id.startswith("R3-DEV001-TIME-")
    }
    for parent_id in sorted(generic_parent_ids):
        entry = excerpt_index.get(parent_id)
        if entry is None:
            raise ValueError(f"missing generic parent excerpt: {parent_id}")
        source_registry_rows.append(
            {
                "call_id": parent_id,
                "library": entry["library_id"],
                "purpose": entry["purpose"],
                "required_text": None,
                "required_text_sha256": entry["excerpt_sha256"],
                "capability_ceiling": "GENERIC_REALITY_OR_ADJUDICATION_PARENT_ONLY",
                "applicability": "FULL_PARENT_SEGMENT_MATERIALIZED_IN_R2",
                "parent_artifact": INPUTS["r2_source_spec"],
                "canonical_path": entry["canonical_path"],
                "line_start": entry["line_start"],
                "line_end": entry["line_end"],
            }
        )

    source_registry = with_hash(
        {
            "schema": "DEV-GROUP-002-R7-DEV001-SOURCE-REGISTRY-V1",
            "group_id": "DEV-GROUP-002",
            "case_id": TARGET_CASE_ID,
            "round_id": "R7",
            "rows": source_registry_rows,
            "row_count": len(source_registry_rows),
            "source_body_rule": "R3 source-call bodies and R2 full parent-segment identities are preserved; no new astrological source sentence is introduced.",
        }
    )

    track_rows: list[dict[str, Any]] = []
    composite_rows: list[dict[str, Any]] = []
    for question_id in [f"Q{i}" for i in range(1, 6)]:
        for option_id in "ABCD":
            spec = ZIWEI_BINDINGS[question_id][option_id]
            track_rows.append(
                {
                    "case_id": TARGET_CASE_ID,
                    "question_id": question_id,
                    "track_id": "ZIWEI",
                    "option_id": option_id,
                    "native_parent_ids": [parent for parent in spec["parent_ids"] if parent.startswith("S06-") or parent.startswith("S07-") or parent.startswith("ZZZA-") or parent.startswith("R3-DEV001-TIME-")],
                    "shared_reality_parent_ids": [parent for parent in spec["parent_ids"] if not (parent.startswith("S06-") or parent.startswith("S07-") or parent.startswith("ZZZA-") or parent.startswith("R3-DEV001-TIME-"))],
                    "direction_status": spec["direction_status"],
                    "supported_atom_ids": spec["supported_atoms"],
                    "partial_atom_ids": spec["partial_atoms"],
                    "limited_atom_ids": spec["limited_atoms"],
                    "contradicted_atom_ids": spec["contradicted_atoms"],
                    "unknown_atom_ids": [] if spec["direction_status"] in {"PARTIALLY_SUPPORTED", "DIRECTLY_CONTRADICTED_MATERIAL_ATOM"} else ["EXACT_OPTION_OCCURRENCE_NOT_PROVEN"],
                    "exact_endpoint_status": "MISSING_EXACT_ENDPOINT",
                    "semantic_reason": spec["semantic_reason"],
                    "program_state": "EXECUTED",
                    "effective": spec["direction_status"] in {"PARTIALLY_SUPPORTED", "DIRECTLY_CONTRADICTED_MATERIAL_ATOM"},
                    "formal_exact_assertion": None,
                }
            )
            track_rows.append(
                {
                    "case_id": TARGET_CASE_ID,
                    "question_id": question_id,
                    "track_id": "BAZI",
                    "option_id": option_id,
                    "native_parent_ids": [],
                    "shared_reality_parent_ids": ["VERIFIED_ABSTENTION_HIGH_RISK_TASKS", "BAZI_ROLE_TO_REALITY_CHAIN"],
                    "direction_status": "NATIVE_PARENT_MISSING",
                    "supported_atom_ids": [],
                    "partial_atom_ids": [],
                    "limited_atom_ids": ["S11_TO_S15_CASE_STRUCTURE_PARENT_NOT_PRESERVED_IN_R3"],
                    "contradicted_atom_ids": [],
                    "unknown_atom_ids": ["BAZI_OPTION_DIRECTION_UNKNOWN"],
                    "exact_endpoint_status": "MISSING_EXACT_ENDPOINT",
                    "semantic_reason": "R3 preserved only S16 capability boundaries for this case, not independent S11-S15 option parents.",
                    "program_state": "CALLED",
                    "effective": False,
                    "formal_exact_assertion": None,
                }
            )
            composite_rows.append(
                {
                    "case_id": TARGET_CASE_ID,
                    "question_id": question_id,
                    "option_id": option_id,
                    "ziwei_direction_status": spec["direction_status"],
                    "bazi_direction_status": "NATIVE_PARENT_MISSING",
                    "composite_direction_status": spec["direction_status"],
                    "s03_fusion_status": "NOT_PERFORMED_NO_MACHINE_VALID_BAZI_SEAL",
                    "strength_class": STRENGTH[spec["direction_status"]],
                    "exact_endpoint_status": "MISSING_EXACT_ENDPOINT",
                    "formal_exact_assertion": None,
                }
            )

    parent_bindings = with_hash(
        {
            "schema": "DEV-GROUP-002-R7-DEV001-TRACK-OPTION-PARENT-BINDINGS-V1",
            "group_id": "DEV-GROUP-002",
            "case_id": TARGET_CASE_ID,
            "round_id": "R7",
            "parent_source_registry_sha256": source_registry["canonical_sha256"],
            "track_row_count": len(track_rows),
            "composite_row_count": len(composite_rows),
            "track_rows": track_rows,
            "composite_rows": composite_rows,
            "summary": {
                "ziwei_option_rows_with_native_parent_binding": 20,
                "bazi_option_rows_with_native_parent_binding": 0,
                "directionally_effective_ziwei_option_rows": sum(1 for row in track_rows if row["track_id"] == "ZIWEI" and row["effective"]),
                "questions_with_directionally_distinctive_options": 3,
                "machine_valid_local_seals": 0,
                "s03_fusions": 0,
            },
        }
    )

    r5_case = next(case for case in r5_prediction["cases"] if case["case_id"] == TARGET_CASE_ID)
    previous_ranks = list(r5_case["ranks"])
    new_ranks: list[str] = []
    pairwise_rows: list[dict[str, Any]] = []
    evidence_reconstructed = 0
    low_information = 0
    winner_changes = 0

    for qindex, previous_rank in enumerate(previous_ranks, 1):
        question_id = f"Q{qindex}"
        strengths = {option: STRENGTH[ZIWEI_BINDINGS[question_id][option]["direction_status"]] for option in "ABCD"}
        ordered = sorted("ABCD", key=lambda option: (-strengths[option], previous_rank.index(option)))
        new_rank = "".join(ordered)
        new_ranks.append(new_rank)
        for left, right in itertools.combinations("ABCD", 2):
            if strengths[left] > strengths[right]:
                winner, loser = left, right
                decision_rule = "DISTINCTIVE_DIRECTION_STATUS"
                reason_status = "RECONSTRUCTED_FROM_OPTION_SPECIFIC_PARENT_BINDINGS"
                evidence_reconstructed += 1
            elif strengths[right] > strengths[left]:
                winner, loser = right, left
                decision_rule = "DISTINCTIVE_DIRECTION_STATUS"
                reason_status = "RECONSTRUCTED_FROM_OPTION_SPECIFIC_PARENT_BINDINGS"
                evidence_reconstructed += 1
            else:
                winner = left if previous_rank.index(left) < previous_rank.index(right) else right
                loser = right if winner == left else left
                decision_rule = "LOW_INFORMATION_FORCED_DECISION_PRESERVE_R5_RELATIVE_ORDER"
                reason_status = "TIED_DIRECTION_STATUS"
                low_information += 1
            previous_winner = left if previous_rank.index(left) < previous_rank.index(right) else right
            if winner != previous_winner:
                winner_changes += 1
            pairwise_rows.append(
                {
                    "case_id": TARGET_CASE_ID,
                    "question_id": question_id,
                    "left": left,
                    "right": right,
                    "left_direction_status": ZIWEI_BINDINGS[question_id][left]["direction_status"],
                    "right_direction_status": ZIWEI_BINDINGS[question_id][right]["direction_status"],
                    "winner": winner,
                    "loser": loser,
                    "previous_r5_winner": previous_winner,
                    "winner_changed": winner != previous_winner,
                    "decision_rule": decision_rule,
                    "reason_status": reason_status,
                    "formal_endpoint_status": "BOTH_MISSING_EXACT_ENDPOINT",
                }
            )

    if new_ranks != ["ACBD", "BACD", "DBAC", "CBAD", "BDCA"]:
        raise ValueError(f"unexpected R7 DEV001 ranks: {new_ranks}")

    adjudication = with_hash(
        {
            "schema": "DEV-GROUP-002-R7-DEV001-PAIRWISE-ADJUDICATION-V1",
            "group_id": "DEV-GROUP-002",
            "case_id": TARGET_CASE_ID,
            "round_id": "R7",
            "parent_bindings_sha256": parent_bindings["canonical_sha256"],
            "previous_r5_ranks": previous_ranks,
            "r7_ranks": new_ranks,
            "row_count": len(pairwise_rows),
            "rows": pairwise_rows,
            "summary": {
                "evidence_reconstructed_pairwise_rows": evidence_reconstructed,
                "low_information_forced_pairwise_rows": low_information,
                "winner_changes_from_r5": winner_changes,
                "rank_changes": [{"question_id": "Q3", "from": "DBCA", "to": "DBAC", "reason": "The entrepreneurship atom is directly contradicted, so an unknown no-work option must rank above it."}],
                "top1_changes": 0,
                "top2_changes": 0,
            },
        }
    )

    updated_cases = []
    for case in r5_prediction["cases"]:
        clone = dict(case)
        if case["case_id"] == TARGET_CASE_ID:
            clone["ranks"] = new_ranks
            clone["top1_vector"] = "".join(rank[0] for rank in new_ranks)
            clone["top2_vector"] = "".join(rank[1] for rank in new_ranks)
            clone["prediction_origin"] = "R7_DEV001_OPTION_PARENT_REBUILD"
        updated_cases.append(clone)

    prediction = with_hash(
        {
            "schema": "DEV-GROUP-002-R7-PREDICTION-FREEZE-V1",
            "group_id": "DEV-GROUP-002",
            "round_id": "R7",
            "run_class": "ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD",
            "case_ids": r5_prediction["case_ids"],
            "cases": updated_cases,
            "question_count": 25,
            "changed_case_ids": [TARGET_CASE_ID],
            "changed_question_ids": [f"{TARGET_CASE_ID}:Q3"],
            "top1_or_top2_changed": False,
            "formal_exact_assertion_permission": "NULL_ONLY",
            "machine_valid_local_seals": 0,
            "s03_fusions": 0,
            "new_case_admission": "BLOCKED",
            "contains_answers": False,
            "base_astrological_knowledge_changed": False,
        }
    )

    answer_vectors = r5_review["answer_vectors"]
    total1 = total2 = 0
    case_scores: list[dict[str, Any]] = []
    for case in prediction["cases"]:
        answer = answer_vectors[case["case_id"]]
        top1 = case["top1_vector"]
        top2 = case["top2_vector"]
        h1 = sum(a == b for a, b in zip(top1, answer))
        h2 = sum(c in (a, b) for a, b, c in zip(top1, top2, answer))
        total1 += h1
        total2 += h2
        case_scores.append({"case_id": case["case_id"], "top1_hits": h1, "top2_coverage": h2})

    review = with_hash(
        {
            "schema": "DEV-GROUP-002-R7-POSTREVEAL-REVIEW-V1",
            "group_id": "DEV-GROUP-002",
            "round_id": "R7",
            "parent_prediction_sha256": prediction["canonical_sha256"],
            "answer_vectors": answer_vectors,
            "case_scores": case_scores,
            "totals": {"top1_hits": total1, "top2_coverage": total2, "question_count": 25, "score_label": "TRAINING_REGRESSION_SCORE"},
            "accuracy_claim": "NO_NEW_BLIND_RESULT",
            "diagnosis": "One lower-rank pair changed from a direct counterevidence correction; TOP1 and TOP2 are unchanged.",
        }
    )

    generic_fix = with_hash(
        {
            "schema": "DEV-GROUP-002-R7-GENERIC-FIX-V1",
            "group_id": "DEV-GROUP-002",
            "round_id": "R7",
            "fix_id": "TR-R7-DIRECT-COUNTEREVIDENCE-BEATS-UNKNOWN",
            "defect_class": "DIRECT_COUNTEREVIDENCE_OPTION_RANKED_ABOVE_UNKNOWN_OPTION",
            "general_rules": [
                "A materially contradicted option cannot defeat an otherwise unknown option merely because the older frozen order placed it higher.",
                "A source scene or capability may remain partial direction while its exact occupation, marriage count, death, surgery, or amount endpoint remains missing.",
                "A spouse or parent scene cannot be promoted to death without a person-specific death chain.",
                "A neutral time fact cannot distinguish heterogeneous event types.",
                "Track-local option parents may repair a pairwise reason without creating a machine-valid local seal or S03 fusion.",
            ],
            "case_specific_direction_rule_added": False,
            "base_astrological_knowledge_changed": False,
            "s00_s19_modified": False,
            "impact_scope": "PAIRWISE_ADJUDICATION_AND_RUNTIME_PROVENANCE_ONLY",
        }
    )

    history_rows = {
        round_id: {"path": path, "git_blob_sha": git_blob_sha(repo_root / path), "preserved": True}
        for round_id, path in HISTORY.items()
    }
    manifest = with_hash(
        {
            "schema": "DEV-GROUP-002-R7-FROZEN-MANIFEST-V1",
            "group_id": "DEV-GROUP-002",
            "round_id": "R7",
            "status": "FROZEN_PARTIAL_SOURCE_REBUILD",
            "run_class": "ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD",
            "historical_rounds": history_rows,
            "artifacts": {
                "source_registry": {"path": str(ROUND_DIR / "source-registry.json"), "canonical_sha256": source_registry["canonical_sha256"], "row_count": source_registry["row_count"]},
                "parent_bindings": {"path": str(ROUND_DIR / "track-option-parent-bindings.json"), "canonical_sha256": parent_bindings["canonical_sha256"], "track_row_count": 40, "composite_row_count": 20},
                "adjudication": {"path": str(ROUND_DIR / "pairwise-adjudication.json"), "canonical_sha256": adjudication["canonical_sha256"], "row_count": 30},
                "prediction": {"path": str(ROUND_DIR / "prediction-freeze.json"), "canonical_sha256": prediction["canonical_sha256"]},
                "review": {"path": str(ROUND_DIR / "postreveal-review.json"), "canonical_sha256": review["canonical_sha256"]},
                "generic_fix": {"path": str(ROUND_DIR / "generic-fix.json"), "canonical_sha256": generic_fix["canonical_sha256"]},
            },
            "statistics": {
                "question_count": 25,
                "fully_processed_case_count": 1,
                "fully_processed_question_count": 5,
                "ziwei_option_rows_with_native_parent_binding": 20,
                "bazi_option_rows_with_native_parent_binding": 0,
                "evidence_reconstructed_pairwise_rows": evidence_reconstructed,
                "low_information_forced_pairwise_rows_in_processed_case": low_information,
                "pairwise_winner_changes": winner_changes,
                "top1_hits": total1,
                "top2_coverage": total2,
                "formal_valid_questions": 0,
                "machine_valid_local_seals": 0,
                "s03_fusions": 0,
            },
            "remaining_cases": ["DEV-EXAMPLE-002", "DEV-EXAMPLE-003", "DEV-EXAMPLE-004", "DEV-EXAMPLE-005"],
            "next_required_round": "R8_REBUILD_DEV_EXAMPLE_002_SOURCE_CALL_BODIES_OR_FAIL_CLOSED",
            "new_case_admission": "BLOCKED",
            "base_astrological_knowledge_changed": False,
            "case_specific_direction_rule_added": False,
            "s00_s19_modified": False,
        }
    )

    return {
        "source-registry.json": source_registry,
        "track-option-parent-bindings.json": parent_bindings,
        "pairwise-adjudication.json": adjudication,
        "prediction-freeze.json": prediction,
        "postreveal-review.json": review,
        "generic-fix.json": generic_fix,
        "manifest.json": manifest,
    }


def materialize(repo_root: Path) -> None:
    output_dir = repo_root / ROUND_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    objects = build_objects(repo_root)
    for filename, obj in objects.items():
        write_json(output_dir / filename, obj)
    stats = objects["manifest.json"]["statistics"]
    summary = f"""# DEV-GROUP-002 R7：DEV-EXAMPLE-001逐选项来源父链重建

R7完整保留R1—R6，仅对仓库中具有真实来源调用正文的DEV-EXAMPLE-001进行逐轨、逐选项重建。20条紫微选项行已绑定本轨来源父对象；八字仍缺S11—S15独立父对象，因此不能密封或融合。

本轮从来源方向重建了{stats['evidence_reconstructed_pairwise_rows']}组成对理由，另有{stats['low_information_forced_pairwise_rows_in_processed_case']}组因方向同距继续低信息强制决胜。Q3中创业选项受到“均不宜自行经商”的直接反证，不能再排在无直接反证的“不用工作”选项之前，因此全排序由`DBCA`修正为`DBAC`。该变化只涉及第三、第四位，TOP1和TOP2不变。

全组`TRAINING_REGRESSION_SCORE`仍为TOP1 {stats['top1_hits']}/25、TOP2 {stats['top2_coverage']}/25。正式有效题、本地机器密封和S03融合仍全部为0；S00—S19和基础命理知识未修改。

其余四案没有保存可重放的来源调用正文，下一轮必须先恢复DEV-EXAMPLE-002的真实调用体；若不能恢复，应失败关闭而不是按计数或旧排序猜测方向。
"""
    (output_dir / "summary.md").write_text(summary, encoding="utf-8")


def validate(repo_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    output_dir = repo_root / ROUND_DIR
    required = [
        "source-registry.json", "track-option-parent-bindings.json", "pairwise-adjudication.json",
        "prediction-freeze.json", "postreveal-review.json", "generic-fix.json", "manifest.json", "summary.md",
    ]
    for filename in required:
        if not (output_dir / filename).exists():
            errors.append(f"missing artifact: {filename}")
    if errors:
        return {"status": "FAIL", "error_count": len(errors), "errors": errors}

    source_registry = read_json(output_dir / "source-registry.json")
    bindings = read_json(output_dir / "track-option-parent-bindings.json")
    adjudication = read_json(output_dir / "pairwise-adjudication.json")
    prediction = read_json(output_dir / "prediction-freeze.json")
    review = read_json(output_dir / "postreveal-review.json")
    generic_fix = read_json(output_dir / "generic-fix.json")
    manifest = read_json(output_dir / "manifest.json")

    objects = {
        "source_registry": source_registry,
        "bindings": bindings,
        "adjudication": adjudication,
        "prediction": prediction,
        "review": review,
        "generic_fix": generic_fix,
        "manifest": manifest,
    }
    for name, obj in objects.items():
        if canonical_hash(obj) != obj.get("canonical_sha256"):
            errors.append(f"{name}: canonical hash mismatch")

    registry_ids = {row["call_id"] for row in source_registry.get("rows", [])}
    track_rows = bindings.get("track_rows", [])
    composite_rows = bindings.get("composite_rows", [])
    if len(track_rows) != 40 or len(composite_rows) != 20:
        errors.append("binding row counts")
    if len({(row["question_id"], row["track_id"], row["option_id"]) for row in track_rows}) != 40:
        errors.append("track binding uniqueness")
    for row in track_rows:
        for parent_id in row["native_parent_ids"] + row["shared_reality_parent_ids"]:
            if parent_id not in registry_ids:
                errors.append(f"unregistered parent: {parent_id}")
        if row["track_id"] == "BAZI" and row["native_parent_ids"]:
            errors.append("invented Bazi native parent")
        if row["formal_exact_assertion"] is not None:
            errors.append("formal assertion released")
    effective_ziwei = [row for row in track_rows if row["track_id"] == "ZIWEI" and row["effective"]]
    if len(effective_ziwei) != 4:
        errors.append("unexpected effective Ziwei option count")

    r7_case = next(case for case in prediction["cases"] if case["case_id"] == TARGET_CASE_ID)
    if r7_case["ranks"] != ["ACBD", "BACD", "DBAC", "CBAD", "BDCA"]:
        errors.append("DEV001 R7 ranks")
    if r7_case["top1_vector"] != "ABDCB" or r7_case["top2_vector"] != "CABBD":
        errors.append("DEV001 top vectors changed")
    if prediction.get("top1_or_top2_changed") is not False:
        errors.append("top1/top2 change declaration")
    if prediction.get("contains_answers") is not False:
        errors.append("prediction contains-answer declaration")

    pair_rows = adjudication.get("rows", [])
    if len(pair_rows) != 30 or adjudication.get("row_count") != 30:
        errors.append("adjudication row count")
    if sum(row["reason_status"] == "RECONSTRUCTED_FROM_OPTION_SPECIFIC_PARENT_BINDINGS" for row in pair_rows) != 11:
        errors.append("evidence reconstructed pair count")
    if sum(row["reason_status"] == "TIED_DIRECTION_STATUS" for row in pair_rows) != 19:
        errors.append("low-information pair count")
    changed = [row for row in pair_rows if row["winner_changed"]]
    if len(changed) != 1 or (changed[0]["question_id"], {changed[0]["left"], changed[0]["right"]}, changed[0]["winner"]) != ("Q3", {"A", "C"}, "A"):
        errors.append("unexpected pairwise winner change")

    if review.get("totals", {}).get("top1_hits") != 14 or review.get("totals", {}).get("top2_coverage") != 16:
        errors.append("group score changed")
    if review.get("accuracy_claim") != "NO_NEW_BLIND_RESULT":
        errors.append("accuracy claim")

    general_rule_text = "\n".join(generic_fix.get("general_rules", []))
    forbidden_tokens = [
        "DEV-EXAMPLE-001", "DEV-EXAMPLE-002", "DEV-EXAMPLE-003", "DEV-EXAMPLE-004", "DEV-EXAMPLE-005",
        "BDBAB", "DBDDB", "BBDCA", "CDBAB", "DADAB",
    ]
    if any(token in general_rule_text for token in forbidden_tokens):
        errors.append("case-specific token in general rules")
    if generic_fix.get("base_astrological_knowledge_changed") is not False or generic_fix.get("s00_s19_modified") is not False:
        errors.append("unauthorized knowledge change")

    for round_id, row in manifest.get("historical_rounds", {}).items():
        expected_path = HISTORY.get(round_id)
        if row.get("path") != expected_path:
            errors.append(f"{round_id}: historical path")
            continue
        if git_blob_sha(repo_root / expected_path) != row.get("git_blob_sha"):
            errors.append(f"{round_id}: historical artifact changed")
        if row.get("preserved") is not True:
            errors.append(f"{round_id}: preserve flag")

    artifact_map = {
        "source_registry": source_registry,
        "parent_bindings": bindings,
        "adjudication": adjudication,
        "prediction": prediction,
        "review": review,
        "generic_fix": generic_fix,
    }
    for key, obj in artifact_map.items():
        if manifest.get("artifacts", {}).get(key, {}).get("canonical_sha256") != obj.get("canonical_sha256"):
            errors.append(f"manifest artifact hash: {key}")

    stats = manifest.get("statistics", {})
    expected_stats = {
        "fully_processed_case_count": 1,
        "fully_processed_question_count": 5,
        "ziwei_option_rows_with_native_parent_binding": 20,
        "bazi_option_rows_with_native_parent_binding": 0,
        "evidence_reconstructed_pairwise_rows": 11,
        "low_information_forced_pairwise_rows_in_processed_case": 19,
        "pairwise_winner_changes": 1,
        "top1_hits": 14,
        "top2_coverage": 16,
        "formal_valid_questions": 0,
        "machine_valid_local_seals": 0,
        "s03_fusions": 0,
    }
    for key, value in expected_stats.items():
        if stats.get(key) != value:
            errors.append(f"manifest statistic: {key}")
    if manifest.get("status") != "FROZEN_PARTIAL_SOURCE_REBUILD":
        errors.append("R7 status")
    if manifest.get("new_case_admission") != "BLOCKED":
        errors.append("new-case gate")
    if manifest.get("base_astrological_knowledge_changed") is not False or manifest.get("s00_s19_modified") is not False:
        errors.append("manifest knowledge change")

    return {
        "schema": "DEV-GROUP-002-R7-VALIDATION-V1",
        "status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "errors": errors,
        "historical_rounds_preserved": ["R1", "R2", "R3", "R4", "R5", "R6"],
        "fully_processed_case_count": 1,
        "fully_processed_question_count": 5,
        "track_option_binding_rows": len(track_rows),
        "composite_option_rows": len(composite_rows),
        "pairwise_rows": len(pair_rows),
        "evidence_reconstructed_pairwise_rows": 11,
        "low_information_forced_pairwise_rows": 19,
        "pairwise_winner_changes": 1,
        "top1_hits": 14,
        "top2_coverage": 16,
        "formal_valid_questions": 0,
        "machine_valid_local_seals": 0,
        "s03_fusions": 0,
        "base_astrological_knowledge_changed": False,
        "s00_s19_modified": False,
        "new_case_admission": "BLOCKED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    if not args.write and not args.validate:
        parser.error("select --write and/or --validate")
    if args.write:
        materialize(repo_root)
    if args.validate:
        result = validate(repo_root)
        output_dir = repo_root / ROUND_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        write_json(output_dir / "validation.json", result)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 0 if result["status"] == "PASS" else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
