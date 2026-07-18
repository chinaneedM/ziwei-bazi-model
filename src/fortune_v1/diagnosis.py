from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, read_json, slug, utc_now

LEARNING_PHASE_MAP = {
    "SOURCE_OR_KNOWLEDGE_GAP": "ABSORB",
    "ATOM_OR_TASK_DECOMPOSITION_ERROR": "DECOMPOSE",
    "MISSING_CAPABILITY_OR_PARENT": "FILL",
    "MECHANISM_OR_RULE_SHAPE_ERROR": "RESHAPE",
    "EXECUTION_OR_COLD_REPLAY_ERROR": "APPLY",
    "GENERALIZATION_OR_TRANSFER_UNKNOWN": "GENERATE",
}


def classify_errors(reveal_path: str | Path, prediction_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    reveal, run = read_json(reveal_path), read_json(prediction_path)
    if reveal["run_id"] != run["run_id"]:
        raise FortuneError("run mismatch", status="DIAGNOSIS_RUN_MISMATCH")
    run_questions = {q["question_id"]: q for q in run["questions"]}
    rows = []
    for scored in reveal["score"]["rows"]:
        if scored["top1_scored_correct"]:
            continue
        question = run_questions[scored["question_id"]]
        categories = []
        learning_defects = []

        if scored["top2_diagnostic_hit"]:
            categories.append("PAIRWISE_OR_FINAL_DECISION_INTERFACE")
            learning_defects.append("MECHANISM_OR_RULE_SHAPE_ERROR")
        else:
            categories.append("COVERAGE_RANKING_OR_SOURCE_GAP")
            learning_defects.extend(["SOURCE_OR_KNOWLEDGE_GAP", "ATOM_OR_TASK_DECOMPOSITION_ERROR"])

        unverified = question.get("most_important_unverified_atom", "")
        if "endpoint" in unverified.lower() or "终点" in unverified:
            categories.append("EXACT_ENDPOINT_UNRESOLVED")
            learning_defects.append("MISSING_CAPABILITY_OR_PARENT")

        fusion_status = question.get("fusion", {}).get("status")
        if fusion_status in {"INVALID", "S03_NOT_PERFORMED"}:
            categories.append("FUSION_INTERFACE_INVALID")
            learning_defects.append("MECHANISM_OR_RULE_SHAPE_ERROR")

        if question.get("complete_knowledge_coverage_status") not in {None, "PASS"}:
            categories.append("COMPLETE_KNOWLEDGE_COVERAGE_INCOMPLETE")
            learning_defects.append("SOURCE_OR_KNOWLEDGE_GAP")
        if question.get("pairwise_row_count", 0) == 0:
            categories.append("PAIRWISE_REPLAY_MISSING")
            learning_defects.append("EXECUTION_OR_COLD_REPLAY_ERROR")

        learning_defects = list(dict.fromkeys(learning_defects))
        next_phases = list(dict.fromkeys(LEARNING_PHASE_MAP[d] for d in learning_defects))
        rows.append({
            "question_id": scored["question_id"],
            "categories": categories,
            "learning_defects": learning_defects,
            "next_learning_phases": next_phases,
            "classification_status": "REASONED_HYPOTHESIS",
            "source_confirmed": [],
            "mechanism_hypotheses": [],
            "missing_parent_families": [],
            "counterexample_requirements": [],
            "open_research_questions": [
                "Replay original SOURCE_EXCERPT parents before changing source direction",
                "Compare the strongest competitor and the correct literal option atom by atom",
                "Test the proposed mechanism against already-mastered questions before promotion",
            ],
        })
    result = {
        "schema": "ERROR-DIAGNOSIS-V2",
        "diagnosis_id": f"DIAG-{slug(run['run_id'])}",
        "run_id": run["run_id"],
        "errors": rows,
        "learning_model": "ABSORB_DECOMPOSE_FILL_RESHAPE_APPLY_GENERATE",
        "single_question_method_change_allowed": True,
        "single_question_base_knowledge_promotion_allowed": False,
        "base_knowledge_candidate_rule": "REQUIRES_TWO_INDEPENDENT_SOURCE_PARENTS_AND_MULTI_UNIT_REPRODUCTION",
        "status": "DIAGNOSED" if rows else "NO_TOP1_ERRORS",
        "created_at": utc_now(),
    }
    atomic_write_json(output_path, result)
    return result


def _base_knowledge_evidence(changes: list[dict[str, Any]]) -> tuple[set[str], set[str]]:
    source_parents: set[str] = set()
    reproduced_units: set[str] = set()
    for change in changes:
        for parent in change.get("source_confirmed_parents", []):
            if isinstance(parent, dict):
                identity = parent.get("parent_sha256") or parent.get("source_excerpt_id") or parent.get("path")
            else:
                identity = str(parent)
            if identity:
                source_parents.add(str(identity))
        for unit_id in change.get("reproduced_unit_ids", []):
            if unit_id:
                reproduced_units.add(str(unit_id))
    return source_parents, reproduced_units


def _contains_answer_direction(changes: list[dict[str, Any]]) -> bool:
    serialized = json.dumps(changes, ensure_ascii=False, sort_keys=True).lower()
    forbidden = (
        "correct_answer",
        "answer_vector",
        "answer_letter",
        "revealed_answer",
        "ground_truth",
        "postreveal_selection",
        "case_specific_direction",
    )
    return any(token in serialized for token in forbidden)


def create_interface_patch_candidate(diagnosis_path: str | Path, defect_ids: list[str], layer: str,
                                     universal_parent_chain: list[dict[str, Any]], changes: list[dict[str, Any]],
                                     output_path: str | Path) -> dict[str, Any]:
    diagnosis = read_json(diagnosis_path)
    if not universal_parent_chain:
        raise FortuneError("universal parent chain required", status="PATCH_PARENT_CHAIN_MISSING")

    normalized_layer = layer.upper()
    available = {
        category
        for row in diagnosis.get("errors", [])
        for category in row.get("categories", [])
    } | {
        defect
        for row in diagnosis.get("errors", [])
        for defect in row.get("learning_defects", [])
    }
    if not set(defect_ids) <= available:
        raise FortuneError("patch cites unclassified defect", status="PATCH_DEFECT_NOT_REPRODUCED")
    if _contains_answer_direction(changes):
        raise FortuneError("patch contains answer or case-direction material", status="PATCH_ANSWER_DIRECTION_CONTAMINATION")

    source_parents, reproduced_units = _base_knowledge_evidence(changes)
    if normalized_layer == "BASE_KNOWLEDGE":
        if len(source_parents) < 2:
            raise FortuneError(
                "base knowledge candidate requires two independent source parents",
                status="BASE_KNOWLEDGE_SOURCE_INDEPENDENCE_MISSING",
            )
        if len(reproduced_units) < 2:
            raise FortuneError(
                "base knowledge candidate requires reproduction in at least two training units",
                status="BASE_KNOWLEDGE_MULTI_UNIT_REPRODUCTION_MISSING",
            )

    result = {
        "schema": "PATCH-CANDIDATE-V2",
        "patch_id": f"PATCH-{slug(diagnosis['run_id'])}-{len(defect_ids)}",
        "layer": normalized_layer,
        "defect_class": defect_ids,
        "universal_parent_chain": universal_parent_chain,
        "changes": changes,
        "generalization_scope": "ALL_CASES_MATCHING_EXPLICIT_CONDITIONS",
        "source_diagnosis_id": diagnosis["diagnosis_id"],
        "learning_model": "ABSORB_DECOMPOSE_FILL_RESHAPE_APPLY_GENERATE",
        "source_confirmed_parent_count": len(source_parents),
        "reproduced_unit_count": len(reproduced_units),
        "answer_direction_material_present": False,
        "leak_scan": {"status": "PENDING", "findings": []},
        "status": "CANDIDATE_UNSCANNED",
        "created_at": utc_now(),
    }
    atomic_write_json(output_path, result)
    return result
