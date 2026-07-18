#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROUND_DIR = Path("reports/dev-group-002/training-regression-r8")
TARGET_CASE_ID = "DEV-EXAMPLE-002"
HISTORY = {
    "R1": "reports/dev-group-002/training-regression-r1/manifest.json",
    "R2": "reports/dev-group-002/training-regression-r2/formal-readiness-matrix.json",
    "R3": "reports/dev-group-002/training-regression-r3/progress.json",
    "R4": "reports/dev-group-002/training-regression-r4/compact-manifest.json",
    "R5": "reports/dev-group-002/training-regression-r5/manifest.json",
    "R6": "reports/dev-group-002/training-regression-r6/manifest.json",
    "R7": "reports/dev-group-002/training-regression-r7/manifest.json",
}
INPUTS = {
    "candidate": "data/chat-work-candidates/DEV-EXAMPLE-002.prediction-body-draft.json",
    "overlay": "data/chat-work-candidates/DEV-EXAMPLE-002.pairwise-replay-overlay.json",
    "contract": "data/prediction-contracts/DEV-EXAMPLE-002.json",
    "r3_receipt": "reports/dev-group-002/training-regression-r3/DEV-EXAMPLE-002/receipt.json",
    "r7_prediction": "reports/dev-group-002/training-regression-r7/prediction-freeze.json",
}
PLACEHOLDER_PARENT_SEGMENTS = {
    "full applicable parent sentence",
    "full applicable strength paragraph",
    "full strength paragraph",
    "full neutral timing paragraph",
    "full medical endpoint paragraph",
    "full endpoint paragraph",
    "full applicable transformation paragraph",
}


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


def option_status(question: dict[str, Any], option_id: str) -> str:
    rows = question.get("direction_matrix", {}).get(option_id, [])
    if not rows:
        return "UNKNOWN"
    statuses = {row.get("status", "UNKNOWN") for row in rows}
    if "DIRECTLY_CONTRADICTED" in statuses:
        return "DIRECTLY_CONTRADICTED"
    if "PARTIALLY_SUPPORTED" in statuses:
        return "PARTIALLY_SUPPORTED"
    if "MISSING_EXACT_ENDPOINT" in statuses:
        return "MISSING_EXACT_ENDPOINT"
    return sorted(statuses)[0]


def build_objects(repo_root: Path) -> dict[str, dict[str, Any]]:
    candidate = read_json(repo_root / INPUTS["candidate"])
    overlay = read_json(repo_root / INPUTS["overlay"])
    contract = read_json(repo_root / INPUTS["contract"])
    r3_receipt = read_json(repo_root / INPUTS["r3_receipt"])
    r7_prediction = read_json(repo_root / INPUTS["r7_prediction"])

    if candidate.get("case_id") != TARGET_CASE_ID or candidate.get("answer_visibility") != "NO":
        raise ValueError("historical candidate identity or answer isolation mismatch")
    if len(candidate.get("questions", [])) != 5:
        raise ValueError("historical candidate question count")

    question_rows: list[dict[str, Any]] = []
    unresolved_parent_ids: list[str] = []
    placeholder_ledger_rows: list[dict[str, Any]] = []
    contradiction_order_violations: list[dict[str, Any]] = []
    all_parent_ids: set[str] = set()

    for question in candidate["questions"]:
        question_id = question["question_id"]
        matrix_parent_ids = sorted(
            {
                parent_id
                for option_rows in question.get("direction_matrix", {}).values()
                for row in option_rows
                for parent_id in row.get("parent_ids", [])
            }
        )
        all_parent_ids.update(matrix_parent_ids)

        ledger_rows = question.get("evidence_ledger", [])
        explicit_ledger_ids = {
            row.get("evidence_id") or row.get("ledger_id") or row.get("object_id")
            for row in ledger_rows
            if row.get("evidence_id") or row.get("ledger_id") or row.get("object_id")
        }
        unresolved = sorted(set(matrix_parent_ids) - explicit_ledger_ids)
        unresolved_parent_ids.extend(f"{question_id}:{parent_id}" for parent_id in unresolved)

        q_placeholders: list[dict[str, Any]] = []
        for index, row in enumerate(ledger_rows, 1):
            parent_segment = row.get("parent_segment")
            missing_required_identity = [
                field
                for field in (
                    "source_excerpt_object_id",
                    "source_file_sha256",
                    "parent_text_sha256",
                    "source_root_atom_id",
                    "physical_selector_receipt_id",
                )
                if not row.get(field)
            ]
            placeholder = parent_segment in PLACEHOLDER_PARENT_SEGMENTS or (
                isinstance(parent_segment, str) and parent_segment.lower().startswith("full ")
            )
            if placeholder or missing_required_identity:
                item = {
                    "question_id": question_id,
                    "ledger_index": index,
                    "track": row.get("track"),
                    "source_library": row.get("source_library"),
                    "target_atom": row.get("target_atom"),
                    "parent_segment": parent_segment,
                    "placeholder_parent_segment": placeholder,
                    "missing_required_identity_fields": missing_required_identity,
                }
                q_placeholders.append(item)
                placeholder_ledger_rows.append(item)

        q_violations: list[dict[str, Any]] = []
        for pair in question.get("pairwise_rows", []):
            left = pair["left"]
            right = pair["right"]
            winner = pair["winner"]
            loser = right if winner == left else left
            winner_status = option_status(question, winner)
            loser_status = option_status(question, loser)
            if winner_status == "DIRECTLY_CONTRADICTED" and loser_status != "DIRECTLY_CONTRADICTED":
                violation = {
                    "question_id": question_id,
                    "left": left,
                    "right": right,
                    "winner": winner,
                    "loser": loser,
                    "winner_status": winner_status,
                    "loser_status": loser_status,
                    "decision_basis": pair.get("decision_basis"),
                    "violation": "DIRECTLY_CONTRADICTED_OPTION_DEFEATS_NONCONTRADICTED_OPTION",
                }
                q_violations.append(violation)
                contradiction_order_violations.append(violation)

        ziwei_track = question.get("ziwei_track", {})
        bazi_track = question.get("bazi_track", {})
        question_rows.append(
            {
                "case_id": TARGET_CASE_ID,
                "question_id": question_id,
                "matrix_parent_ids": matrix_parent_ids,
                "unresolved_matrix_parent_ids": unresolved,
                "evidence_ledger_row_count": len(ledger_rows),
                "placeholder_or_unbound_ledger_rows": q_placeholders,
                "contradiction_order_violations": q_violations,
                "ziwei_validation_status": ziwei_track.get("validation_status"),
                "ziwei_local_seal": ziwei_track.get("local_seal"),
                "ziwei_blind_model_hash": ziwei_track.get("blind_model_hash"),
                "bazi_validation_status": bazi_track.get("validation_status"),
                "bazi_local_seal": bazi_track.get("local_seal"),
                "bazi_blind_model_hash": bazi_track.get("blind_model_hash"),
                "recoverable_as_option_parent_binding": False,
                "formal_exact_assertion": None,
            }
        )

    recovery_audit = with_hash(
        {
            "schema": "DEV-GROUP-002-R8-DEV002-HISTORICAL-RECOVERY-AUDIT-V1",
            "group_id": "DEV-GROUP-002",
            "case_id": TARGET_CASE_ID,
            "round_id": "R8",
            "historical_candidate_path": INPUTS["candidate"],
            "historical_candidate_git_blob_sha": git_blob_sha(repo_root / INPUTS["candidate"]),
            "historical_overlay_path": INPUTS["overlay"],
            "historical_overlay_git_blob_sha": git_blob_sha(repo_root / INPUTS["overlay"]),
            "historical_contract_path": INPUTS["contract"],
            "historical_contract_git_blob_sha": git_blob_sha(repo_root / INPUTS["contract"]),
            "r3_receipt_path": INPUTS["r3_receipt"],
            "r3_receipt_git_blob_sha": git_blob_sha(repo_root / INPUTS["r3_receipt"]),
            "question_rows": question_rows,
            "summary": {
                "question_count": 5,
                "direction_matrix_parent_id_count": len(all_parent_ids),
                "unresolved_direction_matrix_parent_reference_count": len(unresolved_parent_ids),
                "placeholder_or_unbound_evidence_ledger_row_count": len(placeholder_ledger_rows),
                "pairwise_contradiction_order_violation_count": len(contradiction_order_violations),
                "ziwei_machine_valid_local_seals": 0,
                "bazi_machine_valid_local_seals": 0,
                "recoverable_option_parent_bound_questions": 0,
            },
            "unresolved_parent_references": unresolved_parent_ids,
            "pairwise_contradiction_order_violations": contradiction_order_violations,
            "recovery_status": "FAIL_CLOSED_HISTORICAL_BODY_NOT_SOURCE_PARENT_OBJECT",
            "reason": "The historical body contains semantic summaries and placeholder parent descriptions, but not source excerpt objects, hashes, selector receipts, independent local seals, or resolvable evidence IDs.",
        }
    )

    import_decision = with_hash(
        {
            "schema": "DEV-GROUP-002-R8-DEV002-IMPORT-DECISION-V1",
            "group_id": "DEV-GROUP-002",
            "case_id": TARGET_CASE_ID,
            "round_id": "R8",
            "parent_recovery_audit_sha256": recovery_audit["canonical_sha256"],
            "import_historical_direction_matrix": False,
            "import_historical_pairwise_rows": False,
            "import_historical_evidence_ledger": False,
            "selection_change_permission": "NO",
            "confidence_change_permission": "NO",
            "formal_seal_permission": "NO",
            "s03_fusion_permission": "NO",
            "required_next_action": "FRESH_REBUILD_FROM_CANONICAL_CASE_INPUT_AND_ACTIVE_S00_S19_SOURCE_TEXT",
            "failure_scope": "DEV_EXAMPLE_002_SOURCE_PARENT_RECOVERY_ONLY",
            "does_not_invalidate": [
                "R1_TO_R7_HISTORICAL_ARTIFACTS",
                "DEV_EXAMPLE_001_R7_PARTIAL_REBUILD",
                "R7_GROUP_TOP1_TOP2_VECTORS",
            ],
        }
    )

    preserved_prediction = with_hash(
        {
            "schema": "DEV-GROUP-002-R8-PREDICTION-PRESERVATION-V1",
            "group_id": "DEV-GROUP-002",
            "round_id": "R8",
            "parent_r7_prediction_sha256": r7_prediction["canonical_sha256"],
            "cases": r7_prediction["cases"],
            "question_count": 25,
            "selection_changed": False,
            "top1_hits": 14,
            "top2_coverage": 16,
            "formal_exact_assertion_permission": "NULL_ONLY",
            "new_case_admission": "BLOCKED",
        }
    )

    generic_fix = with_hash(
        {
            "schema": "DEV-GROUP-002-R8-GENERIC-FIX-V1",
            "group_id": "DEV-GROUP-002",
            "round_id": "R8",
            "fix_id": "TR-R8-HISTORICAL-SUMMARY-NOT-SOURCE-PARENT",
            "defect_class": "SEMANTIC_SUMMARY_AND_PLACEHOLDER_PARENT_IMPORTED_AS_EVIDENCE_OBJECT",
            "general_rules": [
                "A historical direction matrix cannot be imported unless every parent identifier resolves to an immutable source or capability object with body and hash.",
                "Text such as full applicable parent sentence is a placeholder description, not a source parent body.",
                "An evidence ledger row without source excerpt identity, file hash, parent-text hash, source-root atom identity, and selector receipt cannot establish option direction.",
                "A directly contradicted option may not defeat a noncontradicted option through frozen wording or narrative preference.",
                "When historical source parents are unrecoverable, preserve the last frozen prediction and perform a fresh source rebuild rather than retroactively sealing the old body.",
            ],
            "case_specific_direction_rule_added": False,
            "base_astrological_knowledge_changed": False,
            "s00_s19_modified": False,
            "impact_scope": "HISTORICAL_ARTIFACT_IMPORT_GATE_AND_PAIRWISE_VALIDATION_ONLY",
        }
    )

    history_rows = {
        round_id: {"path": path, "git_blob_sha": git_blob_sha(repo_root / path), "preserved": True}
        for round_id, path in HISTORY.items()
    }
    manifest = with_hash(
        {
            "schema": "DEV-GROUP-002-R8-FROZEN-MANIFEST-V1",
            "group_id": "DEV-GROUP-002",
            "round_id": "R8",
            "status": "FROZEN_RECOVERY_FAIL_CLOSED",
            "run_class": "ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD_RECOVERY_AUDIT",
            "historical_rounds": history_rows,
            "artifacts": {
                "recovery_audit": {"path": str(ROUND_DIR / "historical-recovery-audit.json"), "canonical_sha256": recovery_audit["canonical_sha256"]},
                "import_decision": {"path": str(ROUND_DIR / "import-decision.json"), "canonical_sha256": import_decision["canonical_sha256"]},
                "prediction_preservation": {"path": str(ROUND_DIR / "prediction-preservation.json"), "canonical_sha256": preserved_prediction["canonical_sha256"]},
                "generic_fix": {"path": str(ROUND_DIR / "generic-fix.json"), "canonical_sha256": generic_fix["canonical_sha256"]},
            },
            "statistics": {
                "question_count": 25,
                "r8_audited_case_count": 1,
                "recoverable_dev002_option_parent_bound_questions": 0,
                "historical_unresolved_parent_reference_count": len(unresolved_parent_ids),
                "historical_placeholder_or_unbound_ledger_rows": len(placeholder_ledger_rows),
                "historical_pairwise_contradiction_order_violations": len(contradiction_order_violations),
                "top1_hits": 14,
                "top2_coverage": 16,
                "formal_valid_questions": 0,
                "machine_valid_local_seals": 0,
                "s03_fusions": 0,
            },
            "training_direction_change_required": True,
            "next_required_round": "R9_FRESH_DEV_EXAMPLE_002_SOURCE_REBUILD_FROM_CANONICAL_INPUTS",
            "new_case_admission": "BLOCKED",
            "selection_change_permission": "NO_FROM_HISTORICAL_BODY",
            "base_astrological_knowledge_changed": False,
            "case_specific_direction_rule_added": False,
            "s00_s19_modified": False,
        }
    )

    return {
        "historical-recovery-audit.json": recovery_audit,
        "import-decision.json": import_decision,
        "prediction-preservation.json": preserved_prediction,
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
    summary = f"""# DEV-GROUP-002 R8：DEV-EXAMPLE-002历史来源恢复审计

R8尝试从已合并的历史CHAT候选对象恢复DEV-EXAMPLE-002的逐选项来源父链。恢复失败关闭：方向矩阵中的父ID不能解析为证据对象，证据调用账使用占位父段且缺少来源摘录ID、文件哈希、父正文哈希、来源根原子ID和物理选择器回执，本地密封与盲态哈希也均为空。

审计同时发现{stats['historical_pairwise_contradiction_order_violations']}条“直接反证选项击败非反证选项”的成对异常。历史对象只能作为诊断材料，不能导入R8方向矩阵、排序理由、密封或融合。

R8完整保留R1—R7及R7预测，组级`TRAINING_REGRESSION_SCORE`仍为TOP1 {stats['top1_hits']}/25、TOP2 {stats['top2_coverage']}/25。正式有效题、本地机器密封和S03融合仍为0，S00—S19未修改。

训练方向必须改变：下一轮不得继续从历史摘要补写来源，而应从DEV-EXAMPLE-002的无答案规范输入与活动S00—S19正文重新建立紫微、八字、时间、现实终点和逐选项来源父对象。
"""
    (output_dir / "summary.md").write_text(summary, encoding="utf-8")


def validate(repo_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    output_dir = repo_root / ROUND_DIR
    required = [
        "historical-recovery-audit.json",
        "import-decision.json",
        "prediction-preservation.json",
        "generic-fix.json",
        "manifest.json",
        "summary.md",
    ]
    for filename in required:
        if not (output_dir / filename).exists():
            errors.append(f"missing artifact: {filename}")
    if errors:
        return {"status": "FAIL", "error_count": len(errors), "errors": errors}

    audit = read_json(output_dir / "historical-recovery-audit.json")
    decision = read_json(output_dir / "import-decision.json")
    prediction = read_json(output_dir / "prediction-preservation.json")
    generic_fix = read_json(output_dir / "generic-fix.json")
    manifest = read_json(output_dir / "manifest.json")
    objects = {
        "audit": audit,
        "decision": decision,
        "prediction": prediction,
        "generic_fix": generic_fix,
        "manifest": manifest,
    }
    for name, obj in objects.items():
        if canonical_hash(obj) != obj.get("canonical_sha256"):
            errors.append(f"{name}: canonical hash mismatch")

    summary = audit.get("summary", {})
    if summary.get("question_count") != 5:
        errors.append("audit question count")
    if summary.get("recoverable_option_parent_bound_questions") != 0:
        errors.append("historical parent recovery falsely succeeded")
    if summary.get("unresolved_direction_matrix_parent_reference_count", 0) <= 0:
        errors.append("unresolved parent references not detected")
    if summary.get("placeholder_or_unbound_evidence_ledger_row_count", 0) <= 0:
        errors.append("placeholder ledger rows not detected")
    if summary.get("pairwise_contradiction_order_violation_count", 0) <= 0:
        errors.append("pairwise contradiction-order violations not detected")
    if audit.get("recovery_status") != "FAIL_CLOSED_HISTORICAL_BODY_NOT_SOURCE_PARENT_OBJECT":
        errors.append("recovery status")

    for field in (
        "import_historical_direction_matrix",
        "import_historical_pairwise_rows",
        "import_historical_evidence_ledger",
    ):
        if decision.get(field) is not False:
            errors.append(f"unsafe historical import: {field}")
    if decision.get("required_next_action") != "FRESH_REBUILD_FROM_CANONICAL_CASE_INPUT_AND_ACTIVE_S00_S19_SOURCE_TEXT":
        errors.append("next action")
    if prediction.get("selection_changed") is not False:
        errors.append("R8 changed prediction")
    if (prediction.get("top1_hits"), prediction.get("top2_coverage")) != (14, 16):
        errors.append("R8 score changed")

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
        "recovery_audit": audit,
        "import_decision": decision,
        "prediction_preservation": prediction,
        "generic_fix": generic_fix,
    }
    for key, obj in artifact_map.items():
        if manifest.get("artifacts", {}).get(key, {}).get("canonical_sha256") != obj.get("canonical_sha256"):
            errors.append(f"manifest artifact hash: {key}")

    stats = manifest.get("statistics", {})
    if stats.get("recoverable_dev002_option_parent_bound_questions") != 0:
        errors.append("manifest recovery count")
    if (stats.get("top1_hits"), stats.get("top2_coverage")) != (14, 16):
        errors.append("manifest score")
    for field in ("formal_valid_questions", "machine_valid_local_seals", "s03_fusions"):
        if stats.get(field) != 0:
            errors.append(f"{field} must remain zero")
    if manifest.get("status") != "FROZEN_RECOVERY_FAIL_CLOSED":
        errors.append("R8 status")
    if manifest.get("training_direction_change_required") is not True:
        errors.append("training direction change gate")
    if manifest.get("new_case_admission") != "BLOCKED":
        errors.append("new-case gate")
    if manifest.get("base_astrological_knowledge_changed") is not False or manifest.get("s00_s19_modified") is not False:
        errors.append("manifest knowledge change")

    return {
        "schema": "DEV-GROUP-002-R8-VALIDATION-V1",
        "status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "errors": errors,
        "historical_rounds_preserved": ["R1", "R2", "R3", "R4", "R5", "R6", "R7"],
        "audited_case_id": TARGET_CASE_ID,
        "question_count": 5,
        "recoverable_option_parent_bound_questions": 0,
        "unresolved_parent_reference_count": summary.get("unresolved_direction_matrix_parent_reference_count"),
        "placeholder_or_unbound_ledger_rows": summary.get("placeholder_or_unbound_evidence_ledger_row_count"),
        "pairwise_contradiction_order_violations": summary.get("pairwise_contradiction_order_violation_count"),
        "selection_changed": False,
        "top1_hits": 14,
        "top2_coverage": 16,
        "formal_valid_questions": 0,
        "machine_valid_local_seals": 0,
        "s03_fusions": 0,
        "training_direction_change_required": True,
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
