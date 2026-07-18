#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

ROUND_DIR = Path("reports/dev-group-002/training-regression-r6")
HISTORY = {
    "R1": "reports/dev-group-002/training-regression-r1/manifest.json",
    "R2": "reports/dev-group-002/training-regression-r2/formal-readiness-matrix.json",
    "R3": "reports/dev-group-002/training-regression-r3/progress.json",
    "R4": "reports/dev-group-002/training-regression-r4/compact-manifest.json",
    "R5": "reports/dev-group-002/training-regression-r5/manifest.json",
}
INPUTS = {
    "r1": HISTORY["R1"],
    "r2_readiness": HISTORY["R2"],
    "r2_source_spec": "reports/dev-group-002/training-regression-r2/source-excerpt-spec.json",
    "r3_progress": HISTORY["R3"],
    "r3_dev001": "reports/dev-group-002/training-regression-r3/DEV-EXAMPLE-001/source-grounded-replay.json",
    "r3_dev002": "reports/dev-group-002/training-regression-r3/DEV-EXAMPLE-002/receipt.json",
    "r4": HISTORY["R4"],
    "r5_manifest": HISTORY["R5"],
    "r5_prediction": "reports/dev-group-002/training-regression-r5/prediction-freeze.json",
    "r5_pairwise": "reports/dev-group-002/training-regression-r5/pairwise-replay.json",
}
GENERATED = (
    "source-parent-coverage.json",
    "option-direction-matrix.json",
    "pairwise-reason-replay.json",
    "question-audit.json",
    "generic-fix.json",
    "manifest.json",
    "summary.md",
    "validation.json",
)


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


def case_defects(r1: dict[str, Any], case_id: str, qindex: int) -> list[str]:
    defects = r1["cases"][case_id]["defects"]
    return list(defects[qindex - 1])


def build_objects(repo_root: Path) -> dict[str, Any]:
    data = {name: read_json(repo_root / path) for name, path in INPUTS.items()}
    r1 = data["r1"]
    readiness = data["r2_readiness"]
    source_spec = data["r2_source_spec"]
    r3_progress = data["r3_progress"]
    dev001 = data["r3_dev001"]
    dev002 = data["r3_dev002"]
    r4 = data["r4"]
    r5_manifest = data["r5_manifest"]
    r5_prediction = data["r5_prediction"]
    r5_pairwise = data["r5_pairwise"]

    expected_case_ids = [f"DEV-EXAMPLE-{i:03d}" for i in range(1, 6)]
    if r5_prediction.get("case_ids") != expected_case_ids:
        raise ValueError("R5 fixed-case set changed")
    if r5_manifest.get("status") != "FROZEN":
        raise ValueError("R5 is not frozen")

    excerpt_index = {entry["excerpt_id"]: entry for entry in source_spec["entries"]}
    readiness_index = {(row["case_id"], row["question_id"]): row for row in readiness["rows"]}
    progress_index = {row["case_id"]: row for row in r3_progress["cases"]}
    dev001_results = {row["question_id"]: row for row in dev001["question_track_results"]}
    dev001_source_atoms = [
        call.get("source_atom_id") or f"{call.get('library')}@line:{call.get('source_line')}"
        for call in dev001["source_calls"]
    ]

    source_parent_rows: list[dict[str, Any]] = []
    option_rows: list[dict[str, Any]] = []
    pairwise_rows: list[dict[str, Any]] = []
    question_rows: list[dict[str, Any]] = []
    rank_index: dict[tuple[str, str], str] = {}

    for case in r5_prediction["cases"]:
        case_id = case["case_id"]
        for qindex, rank in enumerate(case["ranks"], 1):
            question_id = f"Q{qindex}"
            key = (case_id, question_id)
            rank_index[key] = rank
            ready = readiness_index[key]
            required_excerpt_ids = list(ready["required_excerpt_ids"])
            excerpt_refs = []
            missing_excerpt_ids = []
            for excerpt_id in required_excerpt_ids:
                entry = excerpt_index.get(excerpt_id)
                if entry is None:
                    missing_excerpt_ids.append(excerpt_id)
                else:
                    excerpt_refs.append(
                        {
                            "excerpt_id": excerpt_id,
                            "library_id": entry["library_id"],
                            "canonical_path": entry["canonical_path"],
                            "line_start": entry["line_start"],
                            "line_end": entry["line_end"],
                            "excerpt_sha256": entry["excerpt_sha256"],
                            "parent_scope": "GENERIC_REALITY_OR_ADJUDICATION_PARENT",
                        }
                    )

            case_progress = progress_index[case_id]
            case_artifact_refs: list[dict[str, Any]] = [
                {
                    "path": INPUTS["r3_progress"],
                    "scope": "CASE_LEVEL_COUNT_SUMMARY",
                    "source_call_count": case_progress["source_call_count"],
                    "physical_selector_count": case_progress["physical_selector_count"],
                }
            ]
            question_context: dict[str, Any] = {
                "ziwei_status": "NOT_MATERIALIZED_PER_QUESTION",
                "bazi_status": "NOT_MATERIALIZED_PER_QUESTION",
                "reason": "No question-level source object is preserved for this case in R3.",
            }
            if case_id == "DEV-EXAMPLE-001":
                result = dev001_results[question_id]
                question_context = {
                    "ziwei_status": result["ziwei_status"],
                    "bazi_status": result["bazi_status"],
                    "reason": result["reason"],
                    "formal_exact_assertion": result["formal_exact_assertion"],
                    "local_seal_status": result["local_seal_status"],
                }
                case_artifact_refs.append(
                    {
                        "path": INPUTS["r3_dev001"],
                        "scope": "QUESTION_LEVEL_RESULT_AND_CASE_LEVEL_SOURCE_CALL_BODIES",
                        "available_source_atom_ids": dev001_source_atoms,
                        "option_to_source_binding_present": False,
                    }
                )
                parent_coverage_status = "QUESTION_RESULT_AND_SOURCE_BODIES_AVAILABLE_OPTION_BINDING_MISSING"
            elif case_id == "DEV-EXAMPLE-002":
                case_artifact_refs.append(
                    {
                        "path": INPUTS["r3_dev002"],
                        "scope": "CASE_LEVEL_RECEIPT_ONLY",
                        "source_call_count": dev002["source_call_count"],
                        "physical_selector_count": dev002["physical_selector_count"],
                        "source_call_bodies_present": False,
                    }
                )
                parent_coverage_status = "CASE_RECEIPT_ONLY_OPTION_PARENT_BODY_MISSING"
            else:
                parent_coverage_status = "GROUP_PROGRESS_ONLY_OPTION_PARENT_BODY_MISSING"

            source_parent_rows.append(
                {
                    "case_id": case_id,
                    "question_id": question_id,
                    "task_class": ready["task_class"],
                    "required_excerpt_ids": required_excerpt_ids,
                    "resolved_generic_excerpt_refs": excerpt_refs,
                    "missing_required_excerpt_ids": missing_excerpt_ids,
                    "case_artifact_refs": case_artifact_refs,
                    "question_context": question_context,
                    "option_specific_source_parent_ids": [],
                    "option_specific_source_parent_status": "MISSING",
                    "parent_coverage_status": parent_coverage_status,
                    "formal_exact_assertion_permission": ready["formal_exact_assertion_permission"],
                    "s03_fusion_permission": ready["s03_fusion_permission"],
                }
            )

            defects = case_defects(r1, case_id, qindex)
            for option_id in "ABCD":
                position = rank.index(option_id) + 1
                option_rows.append(
                    {
                        "case_id": case_id,
                        "question_id": question_id,
                        "option_id": option_id,
                        "frozen_rank_position": position,
                        "task_class": ready["task_class"],
                        "upstream_defect_classes": defects,
                        "direct_support_parent_ids": [],
                        "partial_support_parent_ids": [],
                        "limitation_parent_ids": [ref["excerpt_id"] for ref in excerpt_refs],
                        "direct_counterevidence_parent_ids": [],
                        "alternative_explanation_parent_ids": [],
                        "exact_endpoint_parent_ids": [],
                        "supported_atom_ids": [],
                        "partial_atom_ids": [],
                        "limited_atom_ids": ["REALITY_OR_ENDPOINT_CHAIN_NOT_CLOSED"],
                        "contradicted_atom_ids": [],
                        "unknown_atom_ids": ["OPTION_SPECIFIC_SOURCE_DIRECTION_NOT_MATERIALIZED"],
                        "exact_endpoint_status": "MISSING_EXACT_ENDPOINT",
                        "direction_status": "UNKNOWN_AT_OPTION_LEVEL",
                        "parent_coverage_status": parent_coverage_status,
                        "selection_influence_status": "FROZEN_R4_ORDER_ONLY_NOT_RECOMPUTED_FROM_DIRECTION_MATRIX",
                        "formal_exact_assertion": None,
                        "machine_local_seal_permission": "NO",
                    }
                )

            question_rows.append(
                {
                    "case_id": case_id,
                    "question_id": question_id,
                    "task_class": ready["task_class"],
                    "frozen_rank": rank,
                    "strongest_competitor": rank[1],
                    "question_level_source_context": question_context,
                    "option_direction_rows_expected": 4,
                    "option_direction_rows_with_direct_support": 0,
                    "option_direction_rows_with_direct_counterevidence": 0,
                    "option_direction_rows_unknown": 4,
                    "pairwise_rows_expected": 6,
                    "evidence_reconstructed_pairwise_rows": 0,
                    "low_information_forced_pairwise_rows": 6,
                    "formal_exact_assertion": None,
                    "local_seal_status": "NOT_SEALED_OPTION_PARENT_BINDING_MISSING",
                    "audit_conclusion": "R4 order is preserved, but current repository artifacts do not prove the option-level evidence directions required to derive it.",
                }
            )

    for row in r5_pairwise["rows"]:
        key = (row["case_id"], row["question_id"])
        rank = rank_index[key]
        left = row["left"]
        right = row["right"]
        expected_winner = left if rank.index(left) < rank.index(right) else right
        if row["winner"] != expected_winner:
            raise ValueError(f"R5 pairwise mismatch at {key}: {left}/{right}")
        pairwise_rows.append(
            {
                "case_id": row["case_id"],
                "question_id": row["question_id"],
                "left": left,
                "right": right,
                "winner": row["winner"],
                "loser": row["loser"],
                "left_direction_status": "UNKNOWN_AT_OPTION_LEVEL",
                "right_direction_status": "UNKNOWN_AT_OPTION_LEVEL",
                "left_endpoint_status": "MISSING_EXACT_ENDPOINT",
                "right_endpoint_status": "MISSING_EXACT_ENDPOINT",
                "direct_support_comparison": "NOT_RECONSTRUCTABLE",
                "direct_counterevidence_comparison": "NOT_RECONSTRUCTABLE",
                "composite_coverage_comparison": "NOT_RECONSTRUCTABLE",
                "endpoint_distance_comparison": "TIED_MISSING",
                "time_stage_comparison": "NOT_RECONSTRUCTABLE",
                "alternative_explanation_comparison": "NOT_RECONSTRUCTABLE",
                "mechanism_coherence_comparison": "NOT_RECONSTRUCTABLE",
                "decision_rule": "LOW_INFORMATION_FORCED_DECISION_PRESERVE_FROZEN_R4_ORDER",
                "decision_parent": INPUTS["r5_prediction"],
                "evidence_reason_status": "NOT_PROVEN_FROM_OPTION_SPECIFIC_PARENT_OBJECTS",
                "astrological_contribution_added": False,
            }
        )

    source_parent_coverage = with_hash(
        {
            "schema": "DEV-GROUP-002-R6-SOURCE-PARENT-COVERAGE-V1",
            "group_id": "DEV-GROUP-002",
            "round_id": "R6",
            "question_count": 25,
            "rows": source_parent_rows,
            "summary": {
                "question_rows": 25,
                "question_rows_with_option_specific_parent_binding": 0,
                "dev001_question_rows_with_question_level_context": 5,
                "dev002_question_rows_with_case_receipt_only": 5,
                "dev003_to_005_question_rows_with_group_progress_only": 15,
            },
            "scope_limit": "Generic S17/S18 parents and case-level source summaries cannot substitute for per-option native-track parent bindings.",
        }
    )

    direction_matrix = with_hash(
        {
            "schema": "DEV-GROUP-002-R6-OPTION-DIRECTION-MATRIX-V1",
            "group_id": "DEV-GROUP-002",
            "round_id": "R6",
            "parent_source_coverage_sha256": source_parent_coverage["canonical_sha256"],
            "question_count": 25,
            "option_row_count": len(option_rows),
            "rows": option_rows,
            "summary": {
                "directly_supported_option_rows": 0,
                "partially_supported_option_rows": 0,
                "directly_contradicted_option_rows": 0,
                "unknown_option_rows": 100,
                "missing_exact_endpoint_option_rows": 100,
            },
            "interpretation": "Unknown means the repository lacks option-specific parent binding; it is not counterevidence and does not erase question-level directional context.",
        }
    )

    pairwise_replay = with_hash(
        {
            "schema": "DEV-GROUP-002-R6-PAIRWISE-REASON-REPLAY-V1",
            "group_id": "DEV-GROUP-002",
            "round_id": "R6",
            "parent_direction_matrix_sha256": direction_matrix["canonical_sha256"],
            "parent_r5_pairwise_sha256": r5_pairwise["canonical_sha256"],
            "row_count": len(pairwise_rows),
            "rows": pairwise_rows,
            "summary": {
                "evidence_reconstructed_rows": 0,
                "low_information_forced_rows": 150,
                "winner_changes_from_r5": 0,
            },
            "formal_limit": "These rows preserve the frozen R4/R5 total order but do not claim that the order has been re-derived from complete evidence parents.",
        }
    )

    question_audit = with_hash(
        {
            "schema": "DEV-GROUP-002-R6-QUESTION-AUDIT-V1",
            "group_id": "DEV-GROUP-002",
            "round_id": "R6",
            "rows": question_rows,
            "summary": {
                "question_count": 25,
                "questions_with_complete_option_direction_matrix": 0,
                "questions_with_evidence_reconstructed_pairwise_reasons": 0,
                "questions_requiring_option_parent_rebuild": 25,
                "formal_valid_questions": 0,
                "machine_valid_local_seals": 0,
                "s03_fusions": 0,
            },
        }
    )

    generic_fix = with_hash(
        {
            "schema": "DEV-GROUP-002-R6-GENERIC-FIX-V1",
            "group_id": "DEV-GROUP-002",
            "round_id": "R6",
            "fix_id": "TR-R6-OPTION-PARENT-DIRECTION-RECONSTRUCTABILITY-GATE",
            "defect_class": "FROZEN_TOTAL_ORDER_WITHOUT_OPTION_SPECIFIC_EVIDENCE_PARENT_BINDING",
            "reproduction": {
                "observed": [
                    "R3 preserves question-level source bodies only for DEV-EXAMPLE-001 and does not bind them to individual option atoms.",
                    "DEV-EXAMPLE-002 preserves a case receipt with counts but not source-call bodies.",
                    "DEV-EXAMPLE-003 through DEV-EXAMPLE-005 preserve only group progress counts.",
                    "R4 stores total orders without direction matrices or parent-linked pairwise reasons.",
                    "R5 materializes pairwise row bodies but explicitly cannot reconstruct the evidence directions behind them.",
                ],
                "affected_scope": "25 questions, 100 options, 150 pairwise rows",
            },
            "general_rules": [
                "A frozen option rank is not proof of an option direction matrix.",
                "Case-level source counts and question-level narrative summaries cannot substitute for per-option native-track source parents.",
                "Unknown option direction is neither support nor counterevidence and must not be converted into either.",
                "When pairwise evidence parents cannot be reconstructed, preserve the historical winner only as a low-information forced decision and state that the evidence reason is unproven.",
                "No selection change, confidence increase, formal seal, fusion, or knowledge patch is allowed from an unproven pairwise reason.",
                "The next evidence-bearing round must rebuild per-question, per-track, per-option source calls before changing any R4/R5 choice.",
            ],
            "base_astrological_knowledge_changed": False,
            "case_specific_direction_rule_added": False,
            "s00_s19_modified": False,
            "impact_scope": "TRAINING_RUNTIME_PROVENANCE_AND_RELEASE_GATE_ONLY",
        }
    )

    history_rows: dict[str, dict[str, Any]] = {}
    for round_id, relative_path in HISTORY.items():
        path = repo_root / relative_path
        history_rows[round_id] = {
            "path": relative_path,
            "git_blob_sha": git_blob_sha(path),
            "preserved": True,
        }

    manifest = with_hash(
        {
            "schema": "DEV-GROUP-002-R6-FROZEN-MANIFEST-V1",
            "group_id": "DEV-GROUP-002",
            "round_id": "R6",
            "status": "FROZEN_AUDIT_HOLD",
            "run_class": "ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD_PROVENANCE_AUDIT",
            "historical_rounds": history_rows,
            "artifacts": {
                "source_parent_coverage": {"path": str(ROUND_DIR / "source-parent-coverage.json"), "canonical_sha256": source_parent_coverage["canonical_sha256"], "row_count": 25},
                "option_direction_matrix": {"path": str(ROUND_DIR / "option-direction-matrix.json"), "canonical_sha256": direction_matrix["canonical_sha256"], "row_count": 100},
                "pairwise_reason_replay": {"path": str(ROUND_DIR / "pairwise-reason-replay.json"), "canonical_sha256": pairwise_replay["canonical_sha256"], "row_count": 150},
                "question_audit": {"path": str(ROUND_DIR / "question-audit.json"), "canonical_sha256": question_audit["canonical_sha256"], "row_count": 25},
                "generic_fix": {"path": str(ROUND_DIR / "generic-fix.json"), "canonical_sha256": generic_fix["canonical_sha256"]},
            },
            "statistics": {
                "original_blind_baseline": {"top1_hits": 11, "top2_coverage": 16, "status": "PRESERVED_NOT_OVERWRITTEN"},
                "r4_r5_r6_training_score": {"top1_hits": 14, "top2_coverage": 16, "status": "TRAINING_REGRESSION_SCORE_NO_SELECTION_CHANGE"},
                "question_count": 25,
                "option_direction_row_count": 100,
                "pairwise_reason_row_count": 150,
                "option_specific_parent_bound_questions": 0,
                "evidence_reconstructed_pairwise_rows": 0,
                "formal_valid_questions": 0,
                "machine_valid_local_seals": 0,
                "s03_fusions": 0,
            },
            "training_conclusion": "R6 proves that the current repository cannot reconstruct the option-level evidence reasons behind the R4/R5 total orders. It freezes this provenance gap without inventing support, counterevidence, or knowledge rules.",
            "next_required_round": "R7_PER_QUESTION_PER_TRACK_PER_OPTION_SOURCE_PARENT_REBUILD",
            "new_case_admission": "BLOCKED",
            "selection_change_permission": "NO_UNTIL_OPTION_PARENT_REBUILD",
            "base_astrological_knowledge_changed": False,
            "case_specific_direction_rule_added": False,
            "s00_s19_modified": False,
        }
    )

    return {
        "source-parent-coverage.json": source_parent_coverage,
        "option-direction-matrix.json": direction_matrix,
        "pairwise-reason-replay.json": pairwise_replay,
        "question-audit.json": question_audit,
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
    summary = f"""# DEV-GROUP-002 R6：方向矩阵与来源父链可重建性审计

R6继续只使用固定五案，完整保留R1—R5，不修改S00—S19，不改变R4/R5任何首选、次选或全排序。

本轮物化了25条题级来源父链覆盖行、100条选项方向矩阵行、150条成对裁决理由行和25条题级审计行。审计结果显示：当前仓库中没有任何题目具备逐轨、逐选项的来源父对象绑定，因此100条选项方向均必须保持`UNKNOWN_AT_OPTION_LEVEL`；这不是反证，也不能被改写成支持。

R3仅为DEV-EXAMPLE-001保存了题级结果和案例级来源调用正文，但仍未绑定到各选项原子；DEV-EXAMPLE-002只有案例汇总回执；DEV-EXAMPLE-003至005只有组级统计。故R4/R5的150组成对赢家只能继续标记为低信息强制保留，不能声称已经从证据方向矩阵重新推出。

统计保持TOP1 {stats['r4_r5_r6_training_score']['top1_hits']}/25、TOP2 {stats['r4_r5_r6_training_score']['top2_coverage']}/25。正式有效题、本地机器密封和S03融合仍全部为0；新案例准入继续关闭。

R6修复的是运行时来源父链与发布门：冻结排序不等于方向矩阵，来源数量不等于父对象，未知不等于反证。下一轮必须逐题、逐轨、逐选项重建真实来源调用，未完成前不得调整排序或提高置信度。
"""
    (output_dir / "summary.md").write_text(summary, encoding="utf-8")


def validate(repo_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    output_dir = repo_root / ROUND_DIR
    for filename in GENERATED[:-1]:
        if not (output_dir / filename).exists():
            errors.append(f"missing generated artifact: {filename}")
    if errors:
        return {"status": "FAIL", "errors": errors, "error_count": len(errors)}

    source_coverage = read_json(output_dir / "source-parent-coverage.json")
    direction = read_json(output_dir / "option-direction-matrix.json")
    pairwise = read_json(output_dir / "pairwise-reason-replay.json")
    question_audit = read_json(output_dir / "question-audit.json")
    generic_fix = read_json(output_dir / "generic-fix.json")
    manifest = read_json(output_dir / "manifest.json")
    r5_prediction = read_json(repo_root / INPUTS["r5_prediction"])
    r5_pairwise = read_json(repo_root / INPUTS["r5_pairwise"])

    objects = {
        "source_coverage": source_coverage,
        "direction": direction,
        "pairwise": pairwise,
        "question_audit": question_audit,
        "generic_fix": generic_fix,
        "manifest": manifest,
    }
    for name, obj in objects.items():
        if canonical_hash(obj) != obj.get("canonical_sha256"):
            errors.append(f"{name}: canonical hash mismatch")

    coverage_rows = source_coverage.get("rows", [])
    if len(coverage_rows) != 25:
        errors.append("source-parent coverage row count")
    coverage_keys = {(row["case_id"], row["question_id"]) for row in coverage_rows}
    if len(coverage_keys) != 25:
        errors.append("source-parent coverage uniqueness")
    if any(row.get("option_specific_source_parent_status") != "MISSING" for row in coverage_rows):
        errors.append("R6 invented option-specific parent binding")
    if any(row.get("missing_required_excerpt_ids") for row in coverage_rows):
        errors.append("required generic excerpt unresolved")

    direction_rows = direction.get("rows", [])
    if direction.get("option_row_count") != 100 or len(direction_rows) != 100:
        errors.append("option-direction row count")
    grouped_options: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in direction_rows:
        key = (row["case_id"], row["question_id"])
        grouped_options.setdefault(key, []).append(row)
        if row.get("direction_status") != "UNKNOWN_AT_OPTION_LEVEL":
            errors.append(f"invented option direction: {key} {row['option_id']}")
        if row.get("direct_support_parent_ids") or row.get("direct_counterevidence_parent_ids"):
            errors.append(f"invented directional parent: {key} {row['option_id']}")
        if row.get("exact_endpoint_status") != "MISSING_EXACT_ENDPOINT":
            errors.append(f"endpoint incorrectly closed: {key} {row['option_id']}")
        if row.get("formal_exact_assertion") is not None:
            errors.append(f"formal exact assertion released: {key} {row['option_id']}")
        if row.get("selection_influence_status") != "FROZEN_R4_ORDER_ONLY_NOT_RECOMPUTED_FROM_DIRECTION_MATRIX":
            errors.append(f"selection influence mislabeled: {key} {row['option_id']}")
    if len(grouped_options) != 25:
        errors.append("option-direction question coverage")
    for key, rows in grouped_options.items():
        if {row["option_id"] for row in rows} != set("ABCD") or len(rows) != 4:
            errors.append(f"option coverage: {key}")
        positions = sorted(row["frozen_rank_position"] for row in rows)
        if positions != [1, 2, 3, 4]:
            errors.append(f"rank position coverage: {key}")

    expected_pair_keys = {
        (row["case_id"], row["question_id"], row["left"], row["right"], row["winner"], row["loser"])
        for row in r5_pairwise["rows"]
    }
    actual_pair_keys = {
        (row["case_id"], row["question_id"], row["left"], row["right"], row["winner"], row["loser"])
        for row in pairwise.get("rows", [])
    }
    if pairwise.get("row_count") != 150 or len(pairwise.get("rows", [])) != 150:
        errors.append("pairwise reason row count")
    if actual_pair_keys != expected_pair_keys:
        errors.append("R6 pairwise winners differ from R5")
    for row in pairwise.get("rows", []):
        if row.get("decision_rule") != "LOW_INFORMATION_FORCED_DECISION_PRESERVE_FROZEN_R4_ORDER":
            errors.append("pairwise reason falsely reconstructed")
        if row.get("evidence_reason_status") != "NOT_PROVEN_FROM_OPTION_SPECIFIC_PARENT_OBJECTS":
            errors.append("pairwise evidence status")
        if row.get("astrological_contribution_added") is not False:
            errors.append("unauthorized pairwise astrological contribution")

    audit_rows = question_audit.get("rows", [])
    if len(audit_rows) != 25:
        errors.append("question audit row count")
    if any(row.get("evidence_reconstructed_pairwise_rows") != 0 for row in audit_rows):
        errors.append("question audit falsely claims evidence reconstruction")
    if any(row.get("local_seal_status") != "NOT_SEALED_OPTION_PARENT_BINDING_MISSING" for row in audit_rows):
        errors.append("question audit falsely seals")

    general_rule_text = "\n".join(generic_fix.get("general_rules", []))
    forbidden_tokens = [
        "DEV-EXAMPLE-001", "DEV-EXAMPLE-002", "DEV-EXAMPLE-003", "DEV-EXAMPLE-004", "DEV-EXAMPLE-005",
        "BDBAB", "DBDDB", "BBDCA", "CDBAB", "DADAB",
    ]
    if any(token in general_rule_text for token in forbidden_tokens):
        errors.append("case-specific token leaked into general rules")
    if generic_fix.get("base_astrological_knowledge_changed") is not False or generic_fix.get("s00_s19_modified") is not False:
        errors.append("unauthorized knowledge change")

    for round_id, row in manifest.get("historical_rounds", {}).items():
        expected_path = HISTORY.get(round_id)
        if row.get("path") != expected_path:
            errors.append(f"{round_id}: historical path")
            continue
        path = repo_root / expected_path
        if git_blob_sha(path) != row.get("git_blob_sha"):
            errors.append(f"{round_id}: historical artifact changed")
        if row.get("preserved") is not True:
            errors.append(f"{round_id}: preserve flag")

    artifact_map = {
        "source_parent_coverage": source_coverage,
        "option_direction_matrix": direction,
        "pairwise_reason_replay": pairwise,
        "question_audit": question_audit,
        "generic_fix": generic_fix,
    }
    for key, obj in artifact_map.items():
        if manifest.get("artifacts", {}).get(key, {}).get("canonical_sha256") != obj.get("canonical_sha256"):
            errors.append(f"manifest artifact hash: {key}")

    stats = manifest.get("statistics", {})
    score = stats.get("r4_r5_r6_training_score", {})
    if (score.get("top1_hits"), score.get("top2_coverage")) != (14, 16):
        errors.append("R6 score changed")
    if stats.get("option_direction_row_count") != 100 or stats.get("pairwise_reason_row_count") != 150:
        errors.append("manifest row counts")
    if stats.get("option_specific_parent_bound_questions") != 0 or stats.get("evidence_reconstructed_pairwise_rows") != 0:
        errors.append("manifest falsely claims evidence reconstruction")
    for field in ("formal_valid_questions", "machine_valid_local_seals", "s03_fusions"):
        if stats.get(field) != 0:
            errors.append(f"{field} must remain zero")
    if manifest.get("status") != "FROZEN_AUDIT_HOLD":
        errors.append("R6 status")
    if manifest.get("selection_change_permission") != "NO_UNTIL_OPTION_PARENT_REBUILD":
        errors.append("selection change gate")
    if manifest.get("new_case_admission") != "BLOCKED":
        errors.append("new-case gate")
    if manifest.get("base_astrological_knowledge_changed") is not False or manifest.get("s00_s19_modified") is not False:
        errors.append("manifest unauthorized knowledge change")

    prediction_ranks = {
        (case["case_id"], f"Q{index}"): rank
        for case in r5_prediction["cases"]
        for index, rank in enumerate(case["ranks"], 1)
    }
    for key, rows in grouped_options.items():
        rank = prediction_ranks[key]
        reconstructed = "".join(row["option_id"] for row in sorted(rows, key=lambda item: item["frozen_rank_position"]))
        if reconstructed != rank:
            errors.append(f"option matrix rank replay: {key}")

    return {
        "schema": "DEV-GROUP-002-R6-VALIDATION-V1",
        "status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "errors": errors,
        "historical_rounds_preserved": ["R1", "R2", "R3", "R4", "R5"],
        "question_count": 25,
        "source_parent_coverage_rows": len(coverage_rows),
        "option_direction_rows": len(direction_rows),
        "pairwise_reason_rows": len(pairwise.get("rows", [])),
        "question_audit_rows": len(audit_rows),
        "option_specific_parent_bound_questions": 0,
        "evidence_reconstructed_pairwise_rows": 0,
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
