from __future__ import annotations

from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, read_json, slug, utc_now


def classify_errors(reveal_path: str | Path, prediction_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    reveal, run = read_json(reveal_path), read_json(prediction_path)
    if reveal["run_id"] != run["run_id"]: raise FortuneError("run mismatch", status="DIAGNOSIS_RUN_MISMATCH")
    run_questions = {q["question_id"]: q for q in run["questions"]}
    rows = []
    for scored in reveal["score"]["rows"]:
        if scored["top1_scored_correct"]: continue
        question = run_questions[scored["question_id"]]
        categories = []
        if scored["top2_diagnostic_hit"]: categories.append("PAIRWISE_OR_FINAL_DECISION_INTERFACE")
        else: categories.append("COVERAGE_RANKING_OR_SOURCE_GAP")
        if "endpoint" in question.get("most_important_unverified_atom", "").lower() or "终点" in question.get("most_important_unverified_atom", ""):
            categories.append("EXACT_ENDPOINT_UNRESOLVED")
        if question.get("fusion", {}).get("status") in {"INVALID", "S03_NOT_PERFORMED"}: categories.append("FUSION_INTERFACE_INVALID")
        rows.append({"question_id": scored["question_id"], "categories": categories,
                     "classification_status": "REASONED_HYPOTHESIS", "source_confirmed": [],
                     "open_research_questions": ["Requires original SOURCE_EXCERPT replay before source-direction conclusion"]})
    result = {"schema": "ERROR-DIAGNOSIS-V1", "diagnosis_id": f"DIAG-{slug(run['run_id'])}", "run_id": run["run_id"],
              "errors": rows, "single_case_base_knowledge_change_allowed": False,
              "status": "DIAGNOSED" if rows else "NO_TOP1_ERRORS", "created_at": utc_now()}
    atomic_write_json(output_path, result); return result


def create_interface_patch_candidate(diagnosis_path: str | Path, defect_ids: list[str], layer: str,
                                     universal_parent_chain: list[dict[str, Any]], changes: list[dict[str, Any]],
                                     output_path: str | Path) -> dict[str, Any]:
    diagnosis = read_json(diagnosis_path)
    if not universal_parent_chain: raise FortuneError("universal parent chain required", status="PATCH_PARENT_CHAIN_MISSING")
    if layer == "BASE_KNOWLEDGE": raise FortuneError("automatic base knowledge changes are forbidden", status="AUTO_BASE_KNOWLEDGE_CHANGE_FORBIDDEN")
    available = {category for row in diagnosis["errors"] for category in row["categories"]}
    if not set(defect_ids) <= available: raise FortuneError("patch cites unclassified defect", status="PATCH_DEFECT_NOT_REPRODUCED")
    result = {"schema": "PATCH-CANDIDATE-V1", "patch_id": f"PATCH-{slug(diagnosis['run_id'])}-{len(defect_ids)}",
              "layer": layer, "defect_class": ",".join(defect_ids), "universal_parent_chain": universal_parent_chain,
              "changes": changes, "source_diagnosis_id": diagnosis["diagnosis_id"],
              "leak_scan": {"status": "PENDING", "findings": []}, "status": "CANDIDATE_UNSCANNED", "created_at": utc_now()}
    atomic_write_json(output_path, result); return result

