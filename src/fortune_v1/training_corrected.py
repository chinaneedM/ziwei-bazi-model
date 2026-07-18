from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, canonical_bytes, read_json, sha256_bytes, slug, utc_now

SCHEMA = "LEARNING-CYCLE-V2.1"
EVIDENCE_SCHEMA = "QUESTION-TRAINING-EVIDENCE-V2.1"
EVALUATION_SCHEMA = "QUESTION-TRAINING-EVALUATION-V2.1"
REASONING_CORRECTION_SCHEMA = "REASONING-CORRECTION-OBJECT-V2.1"
FIRST_BLIND_ROLE = "FIRST_BLIND_PREDICTION"
POST_REVEAL_ROLE = "POST_REVEAL_TRAINING_REPLAY"


def _require(condition: bool, message: str, status: str) -> None:
    if not condition:
        raise FortuneError(message, status=status)


def _rate(hits: int, total: int) -> float | None:
    return hits / total if total else None


def _with_hash(value: dict[str, Any]) -> dict[str, Any]:
    result = dict(value)
    result["object_hash"] = sha256_bytes(canonical_bytes({k: v for k, v in result.items() if k != "object_hash"}))
    return result


def _hash_matches(value: dict[str, Any]) -> bool:
    expected = value.get("object_hash")
    if not isinstance(expected, str) or len(expected) != 64:
        return False
    actual = sha256_bytes(canonical_bytes({k: v for k, v in value.items() if k != "object_hash"}))
    return expected == actual


def default_thresholds() -> dict[str, Any]:
    return {
        "min_post_reveal_stability_replays": 5,
        "min_distinct_first_blind_questions_for_rate_gate": 5,
        "rolling_top1_target": 0.80,
        "rolling_top2_target": 0.90,
        "prior_method_retention_target": 0.80,
    }


def create_cycle(
    cycle_id: str,
    group_id: str,
    units: list[dict[str, Any]],
    output_path: str | Path,
    *,
    thresholds: dict[str, Any] | None = None,
    bindings: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _require(bool(units), "cycle requires units", "TRAINING_UNIT_PLAN_EMPTY")
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(units):
        unit_id = slug(str(raw.get("unit_id") or f"UNIT-{index + 1:03d}"))
        _require(unit_id not in seen, f"duplicate unit: {unit_id}", "TRAINING_UNIT_DUPLICATE")
        seen.add(unit_id)
        question_ids = [str(v) for v in raw.get("question_ids", [])]
        _require(len(question_ids) == 1, f"{unit_id} must bind one question", "QUESTION_UNIT_SCOPE_INVALID")
        normalized.append({
            "unit_id": unit_id,
            "case_ids": [str(v) for v in raw.get("case_ids", [])],
            "question_ids": question_ids,
            "status": "PENDING",
            "completion_evaluation_id": None,
        })

    merged = default_thresholds()
    if thresholds:
        merged.update(thresholds)
    _require(int(merged["min_post_reveal_stability_replays"]) >= 1, "stability replay threshold invalid", "TRAINING_THRESHOLD_INVALID")
    _require(int(merged["min_distinct_first_blind_questions_for_rate_gate"]) >= 2, "distinct blind question threshold invalid", "TRAINING_THRESHOLD_INVALID")

    result = _with_hash({
        "schema": SCHEMA,
        "cycle_id": slug(cycle_id),
        "group_id": slug(group_id),
        "dataset_role": "REVEALED_TRAINING_SET",
        "unit_mode": "QUESTION",
        "training_principle": "WRONG_ANSWER_DRIVES_REASONING_CORRECTION_NOT_ANSWER_MEMORIZATION",
        "accuracy_policy": {
            "eligible_observation": FIRST_BLIND_ROLE,
            "one_observation_per_distinct_question": True,
            "post_reveal_replays_count_as_accuracy": False,
            "same_question_repetition_count_as_accuracy": False,
            "distinct_question_key": "UNIT_ID_OR_EXPLICIT_QUESTION_KEY",
            "rate_gate_scope": "ROLLING_DISTINCT_QUESTIONS_AND_FINAL_GROUP",
        },
        "units": normalized,
        "current_unit_index": 0,
        "completed_training_units": [],
        "blind_accuracy_ledger": [],
        "thresholds": merged,
        "bindings": bindings or {},
        "status": "LEARNING_ACTIVE",
        "generalization_status": "NOT_TESTED_ON_FROZEN_UNSEEN_CASES",
        "created_at": utc_now(),
    })
    atomic_write_json(output_path, result)
    return result


def _clean_prediction_row(row: dict[str, Any], *, expected_role: str) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if row.get("evaluation_role") != expected_role:
        reasons.append("EVALUATION_ROLE_MISMATCH")
    if row.get("answer_visible_during_prediction") is not False:
        reasons.append("ANSWER_VISIBILITY_NOT_DENIED")
    if row.get("prediction_input_answer_free") is not True:
        reasons.append("ANSWER_FREE_INPUT_NOT_PROVEN")
    if row.get("case_specific_rule_detected") is True:
        reasons.append("CASE_SPECIFIC_RULE_DETECTED")
    if row.get("source_provenance_status") != "PASS":
        reasons.append("SOURCE_PROVENANCE_NOT_PASS")
    if row.get("pairwise_replay_status") != "PASS":
        reasons.append("PAIRWISE_REPLAY_NOT_PASS")
    if expected_role == FIRST_BLIND_ROLE and row.get("frozen_before_reveal") is not True:
        reasons.append("FIRST_BLIND_FREEZE_NOT_PROVEN")
    return not reasons, reasons


def _distinct_question_key(row: dict[str, Any]) -> str:
    explicit = row.get("distinct_question_key")
    if explicit:
        return str(explicit)
    unit_id = row.get("unit_id")
    if unit_id:
        return str(unit_id)
    case_id = row.get("case_id")
    question_id = row.get("question_id")
    if case_id and question_id:
        return f"{case_id}::{question_id}"
    return str(question_id)


def _rolling_blind_metrics(cycle: dict[str, Any], current_first_blind: dict[str, Any]) -> dict[str, Any]:
    rows = [dict(v) for v in cycle.get("blind_accuracy_ledger", [])]
    question_key = _distinct_question_key(current_first_blind)
    rows = [v for v in rows if _distinct_question_key(v) != question_key]
    rows.append({
        "distinct_question_key": question_key,
        "question_id": current_first_blind.get("question_id"),
        "case_id": current_first_blind.get("case_id"),
        "unit_id": current_first_blind.get("unit_id"),
        "top1_correct": bool(current_first_blind.get("top1_correct")),
        "top2_hit": bool(current_first_blind.get("top2_hit")),
        "prediction_freeze_hash": current_first_blind.get("prediction_freeze_hash"),
    })
    distinct = len({_distinct_question_key(v) for v in rows})
    top1_hits = sum(bool(v.get("top1_correct")) for v in rows)
    top2_hits = sum(bool(v.get("top2_hit")) for v in rows)
    minimum = int(cycle["thresholds"]["min_distinct_first_blind_questions_for_rate_gate"])
    gate_evaluable = distinct >= minimum
    top1_rate = _rate(top1_hits, distinct)
    top2_rate = _rate(top2_hits, distinct)
    gate_pass = bool(
        gate_evaluable
        and top1_rate is not None
        and top2_rate is not None
        and top1_rate >= float(cycle["thresholds"]["rolling_top1_target"])
        and top2_rate >= float(cycle["thresholds"]["rolling_top2_target"])
    )
    return {
        "eligible_role": FIRST_BLIND_ROLE,
        "distinct_question_key": "UNIT_ID_OR_EXPLICIT_QUESTION_KEY",
        "distinct_question_count": distinct,
        "top1_hits": top1_hits,
        "top1_rate": top1_rate,
        "top2_hits": top2_hits,
        "top2_rate": top2_rate,
        "minimum_distinct_questions": minimum,
        "rate_gate_evaluable": gate_evaluable,
        "rate_gate_pass": gate_pass,
        "status": "PASS" if gate_pass else ("BELOW_TARGET" if gate_evaluable else "NOT_YET_EVALUABLE"),
        "ledger": rows,
    }


def _validate_pairwise_rows(reasoning: dict[str, Any], reasons: list[str]) -> None:
    option_rows = reasoning.get("option_semantics")
    if not isinstance(option_rows, list) or len(option_rows) < 2:
        reasons.append("OPTION_SEMANTICS_INCOMPLETE")
        return
    option_ids = [str(v.get("option_id")) for v in option_rows if isinstance(v, dict) and v.get("option_id")]
    if len(option_ids) != len(option_rows) or len(set(option_ids)) != len(option_ids):
        reasons.append("OPTION_ID_SET_INVALID")
        return
    pairwise_rows = reasoning.get("pairwise_rows")
    expected_count = len(option_ids) * (len(option_ids) - 1) // 2
    if not isinstance(pairwise_rows, list) or len(pairwise_rows) != expected_count:
        reasons.append("PAIRWISE_ROW_COUNT_INCOMPLETE")
        return
    seen: set[tuple[str, str]] = set()
    for row in pairwise_rows:
        if not isinstance(row, dict):
            reasons.append("PAIRWISE_ROW_INVALID")
            continue
        left, right = str(row.get("left", "")), str(row.get("right", ""))
        pair = tuple(sorted((left, right)))
        if left not in option_ids or right not in option_ids or left == right or pair in seen:
            reasons.append("PAIRWISE_PAIR_SET_INVALID")
            continue
        seen.add(pair)
        direction = row.get("direction")
        if direction not in {"LEFT_AHEAD", "RIGHT_AHEAD", "TRUE_TIE"}:
            reasons.append("PAIRWISE_DIRECTION_INVALID")
        if not row.get("decisive_rule") or not row.get("reason"):
            reasons.append("PAIRWISE_DECISION_PAYLOAD_INCOMPLETE")
        if not isinstance(row.get("left_vector"), dict) or not isinstance(row.get("right_vector"), dict):
            reasons.append("PAIRWISE_VECTOR_MISSING")
    if len(seen) != expected_count:
        reasons.append("PAIRWISE_PAIR_SET_INCOMPLETE")


def _validate_reasoning_correction(reasoning: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if reasoning.get("schema") != REASONING_CORRECTION_SCHEMA:
        reasons.append("REASONING_CORRECTION_SCHEMA_INVALID")
        return reasons
    if not _hash_matches(reasoning):
        reasons.append("REASONING_CORRECTION_HASH_INVALID")
    required_nonempty_lists = {
        "error_mechanisms": "ERROR_MECHANISM_LEDGER_INCOMPLETE",
        "source_parent_chains": "SOURCE_PARENT_CHAINS_INCOMPLETE",
        "corrected_reasoning_order": "CORRECTED_REASONING_ORDER_INCOMPLETE",
        "capability_ceiling_and_no_overreach": "CAPABILITY_CEILING_RULES_INCOMPLETE",
        "applicability_conditions": "APPLICABILITY_CONDITIONS_INCOMPLETE",
        "counterexamples_and_failure_boundaries": "COUNTEREXAMPLE_BOUNDARIES_INCOMPLETE",
    }
    for field, reason in required_nonempty_lists.items():
        value = reasoning.get(field)
        if not isinstance(value, list) or not value:
            reasons.append(reason)
    for parent in reasoning.get("source_parent_chains", []):
        if not isinstance(parent, dict):
            reasons.append("SOURCE_PARENT_CHAIN_INVALID")
            continue
        required = {
            "library_id",
            "active_file_sha256",
            "excerpt_sha256",
            "line_ranges",
            "knowledge_point",
            "applicability_conditions",
            "capability_ceiling",
            "downstream_effect",
        }
        if any(not parent.get(field) for field in required):
            reasons.append("SOURCE_PARENT_CHAIN_FIELDS_INCOMPLETE")
    _validate_pairwise_rows(reasoning, reasons)
    strongest = reasoning.get("strongest_competitor")
    if not isinstance(strongest, dict) or not strongest.get("relative_first") or not strongest.get("relative_second") or not strongest.get("pairwise_row_id"):
        reasons.append("STRONGEST_COMPETITOR_NOT_DERIVED")
    contamination = reasoning.get("contamination_and_answer_memory_audit")
    if not isinstance(contamination, dict):
        reasons.append("CONTAMINATION_AUDIT_MISSING")
    else:
        must_be_true = {
            "original_first_blind_preserved",
            "post_reveal_replays_excluded_from_accuracy",
            "generic_rule_has_no_case_or_option_fixed_selection",
            "bazi_variant_not_selected_by_revealed_result",
            "base_knowledge_not_promoted_from_single_unit",
        }
        if any(contamination.get(field) is not True for field in must_be_true):
            reasons.append("CONTAMINATION_AUDIT_NOT_PASS")
        if contamination.get("case_specific_rule_detected") is True:
            reasons.append("CASE_SPECIFIC_RULE_DETECTED")
        if contamination.get("answer_memorization_rule_detected") is True:
            reasons.append("ANSWER_MEMORIZATION_RULE_DETECTED")
        if contamination.get("status") != "PASS":
            reasons.append("CONTAMINATION_AUDIT_NOT_PASS")
    conclusion = reasoning.get("training_unit_conclusion")
    if not isinstance(conclusion, dict) or conclusion.get("status") != "TRAINING_UNIT_COMPLETE_CANDIDATE":
        reasons.append("TRAINING_UNIT_CONCLUSION_NOT_READY")
    return sorted(set(reasons))


def evaluate_question_training(
    cycle_path: str | Path,
    evidence_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    cycle = read_json(cycle_path)
    evidence = read_json(evidence_path)
    _require(cycle.get("schema") == SCHEMA, "cycle schema invalid", "TRAINING_CYCLE_SCHEMA_INVALID")
    _require(evidence.get("schema") == EVIDENCE_SCHEMA, "evidence schema invalid", "TRAINING_EVIDENCE_SCHEMA_INVALID")
    _require(evidence.get("cycle_id") == cycle.get("cycle_id"), "cycle id mismatch", "TRAINING_CYCLE_ID_MISMATCH")

    current_index = int(cycle["current_unit_index"])
    _require(current_index < len(cycle["units"]), "no active unit", "TRAINING_CYCLE_ALREADY_COMPLETE")
    unit = cycle["units"][current_index]
    _require(evidence.get("unit_id") == unit["unit_id"], "unit id mismatch", "TRAINING_UNIT_ID_MISMATCH")

    first_blind = dict(evidence.get("first_blind_prediction") or {})
    first_blind["unit_id"] = unit["unit_id"]
    first_clean, first_reasons = _clean_prediction_row(first_blind, expected_role=FIRST_BLIND_ROLE)

    correction = dict(evidence.get("correction") or {})
    correction_reasons: list[str] = []
    required_true = {
        "error_diagnosis_complete": "ERROR_DIAGNOSIS_INCOMPLETE",
        "reasoning_update_complete": "REASONING_UPDATE_INCOMPLETE",
        "generic_method_candidate_recorded": "GENERIC_METHOD_NOT_RECORDED",
        "counterexample_tests_complete": "COUNTEREXAMPLE_TESTS_INCOMPLETE",
    }
    for field, reason in required_true.items():
        if correction.get(field) is not True:
            correction_reasons.append(reason)
    if correction.get("patch_validation_status") != "PASS":
        correction_reasons.append("PATCH_VALIDATION_NOT_PASS")
    if correction.get("case_specific_rule_detected") is True:
        correction_reasons.append("CASE_SPECIFIC_RULE_DETECTED")
    if correction.get("answer_memorization_rule_detected") is True:
        correction_reasons.append("ANSWER_MEMORIZATION_RULE_DETECTED")
    reasoning = correction.get("reasoning_correction_object")
    if not isinstance(reasoning, dict):
        correction_reasons.append("REASONING_CORRECTION_OBJECT_MISSING")
        reasoning_reasons = ["REASONING_CORRECTION_OBJECT_MISSING"]
    else:
        reasoning_reasons = _validate_reasoning_correction(reasoning)
        correction_reasons.extend(reasoning_reasons)

    replay_rows = list(evidence.get("post_reveal_training_replays", []))
    replay_rejections: list[dict[str, Any]] = []
    clean_replays: list[dict[str, Any]] = []
    for row in replay_rows:
        clean, reasons = _clean_prediction_row(row, expected_role=POST_REVEAL_ROLE)
        if clean:
            clean_replays.append(row)
        else:
            replay_rejections.append({"attempt_id": row.get("attempt_id"), "reasons": reasons})
    replay_attempts = {str(v.get("attempt_id")) for v in clean_replays if v.get("attempt_id")}
    required_replays = int(cycle["thresholds"]["min_post_reveal_stability_replays"])
    stability_pass = len(replay_attempts) >= required_replays and not replay_rejections
    fit_hits = sum(bool(v.get("matches_revealed_result")) for v in clean_replays)
    fit_rate = _rate(fit_hits, len(clean_replays))

    retention = dict(evidence.get("prior_method_retention") or {})
    prior_count = int(retention.get("prior_completed_unit_count", 0))
    retention_rate = retention.get("retention_rate")
    retention_pass = (
        prior_count == 0
        or (
            isinstance(retention_rate, (int, float))
            and float(retention_rate) >= float(cycle["thresholds"]["prior_method_retention_target"])
        )
    )

    contamination = any(
        reason in {"ANSWER_VISIBILITY_NOT_DENIED", "ANSWER_FREE_INPUT_NOT_PROVEN", "CASE_SPECIFIC_RULE_DETECTED", "ANSWER_MEMORIZATION_RULE_DETECTED", "CONTAMINATION_AUDIT_NOT_PASS"}
        for reason in [*first_reasons, *correction_reasons, *(r for item in replay_rejections for r in item["reasons"])]
    )
    provenance_invalid = any(
        reason in {"SOURCE_PROVENANCE_NOT_PASS", "PAIRWISE_REPLAY_NOT_PASS", "FIRST_BLIND_FREEZE_NOT_PROVEN", "SOURCE_PARENT_CHAINS_INCOMPLETE", "SOURCE_PARENT_CHAIN_FIELDS_INCOMPLETE", "REASONING_CORRECTION_HASH_INVALID"}
        for reason in [*first_reasons, *correction_reasons, *(r for item in replay_rejections for r in item["reasons"])]
    )
    correction_complete = not correction_reasons
    unit_complete = first_clean and correction_complete and stability_pass and retention_pass

    if contamination:
        status = "HOLD_ANSWER_OR_CASE_RULE_CONTAMINATION"
    elif provenance_invalid:
        status = "HOLD_INVALID_PROVENANCE_OR_FREEZE"
    elif unit_complete:
        status = "TRAINING_UNIT_COMPLETE"
    else:
        status = "CONTINUE_CURRENT_UNIT_TRAINING"

    rolling = _rolling_blind_metrics(cycle, first_blind) if first_clean else {
        "eligible_role": FIRST_BLIND_ROLE,
        "status": "NOT_UPDATED_INVALID_FIRST_BLIND_RECORD",
        "ledger": list(cycle.get("blind_accuracy_ledger", [])),
    }

    evaluation = _with_hash({
        "schema": EVALUATION_SCHEMA,
        "evaluation_id": f"EVAL-{slug(cycle['cycle_id'])}-{current_index + 1:03d}-{slug(str(evidence.get('evidence_id', 'EVIDENCE')))}",
        "cycle_id": cycle["cycle_id"],
        "unit_id": unit["unit_id"],
        "status": status,
        "unit_complete": unit_complete,
        "advance_allowed": unit_complete,
        "advance_executed": False,
        "first_blind_prediction": {
            "eligible_for_accuracy": first_clean,
            "top1_correct": first_blind.get("top1_correct") if first_clean else None,
            "top2_hit": first_blind.get("top2_hit") if first_clean else None,
            "reasons": first_reasons,
        },
        "correction": {
            "complete": correction_complete,
            "reasons": sorted(set(correction_reasons)),
            "reasoning_correction_validation": {
                "status": "PASS" if not reasoning_reasons else "FAIL",
                "reasons": reasoning_reasons,
                "object_hash": reasoning.get("object_hash") if isinstance(reasoning, dict) else None,
            },
        },
        "post_reveal_training_replay": {
            "role": "STABILITY_AND_TRAINING_FIT_ONLY",
            "eligible_for_blind_accuracy": False,
            "clean_attempt_count": len(replay_attempts),
            "required_clean_attempt_count": required_replays,
            "matches_revealed_result_count": fit_hits,
            "post_reveal_fit_rate": fit_rate,
            "stability_pass": stability_pass,
            "rejected_rows": replay_rejections,
        },
        "prior_method_retention": {
            "prior_completed_unit_count": prior_count,
            "retention_rate": retention_rate,
            "status": "PASS" if retention_pass else "BELOW_TARGET",
        },
        "rolling_first_blind_accuracy": rolling,
        "claim_boundary": {
            "same_question_post_reveal_fit": "MEASURED_NOT_ACCURACY",
            "distinct_first_blind_accuracy": "MEASURED_ONLY_FROM_FIRST_FROZEN_PREDICTIONS",
            "unseen_generalization": "NOT_PROVEN_UNTIL_FROZEN_UNSEEN_BLOCK",
            "remote_github_actions": "UNVERIFIED",
        },
        "created_at": utc_now(),
    })
    atomic_write_json(output_path, evaluation)
    return evaluation


def advance_cycle(
    cycle_path: str | Path,
    evaluation_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    cycle = read_json(cycle_path)
    evaluation = read_json(evaluation_path)
    _require(cycle.get("schema") == SCHEMA, "cycle schema invalid", "TRAINING_CYCLE_SCHEMA_INVALID")
    _require(evaluation.get("schema") == EVALUATION_SCHEMA, "evaluation schema invalid", "TRAINING_EVALUATION_SCHEMA_INVALID")
    _require(evaluation.get("cycle_id") == cycle.get("cycle_id"), "cycle id mismatch", "TRAINING_CYCLE_ID_MISMATCH")

    next_cycle = json.loads(json.dumps(cycle))
    current_index = int(next_cycle["current_unit_index"])
    unit = next_cycle["units"][current_index]
    _require(evaluation.get("unit_id") == unit["unit_id"], "unit mismatch", "TRAINING_UNIT_ID_MISMATCH")

    if evaluation["status"].startswith("HOLD_"):
        next_cycle["status"] = evaluation["status"]
    elif evaluation.get("unit_complete") is True:
        unit["status"] = "TRAINING_UNIT_COMPLETE"
        unit["completion_evaluation_id"] = evaluation["evaluation_id"]
        if unit["unit_id"] not in next_cycle["completed_training_units"]:
            next_cycle["completed_training_units"].append(unit["unit_id"])
        next_cycle["blind_accuracy_ledger"] = evaluation["rolling_first_blind_accuracy"]["ledger"]
        if current_index + 1 < len(next_cycle["units"]):
            next_cycle["current_unit_index"] = current_index + 1
            next_cycle["status"] = "LEARNING_ACTIVE"
        else:
            rolling = evaluation["rolling_first_blind_accuracy"]
            next_cycle["status"] = (
                "TRAINING_SET_COMPLETE_AWAITING_UNSEEN_BLIND_TEST"
                if rolling.get("rate_gate_pass") is True
                else "TRAINING_SET_COMPLETE_BELOW_ROLLING_TARGET_REQUIRES_RESHAPING"
            )
    else:
        next_cycle["status"] = "LEARNING_ACTIVE"

    next_cycle["updated_at"] = utc_now()
    next_cycle["parent_cycle_hash"] = cycle.get("object_hash")
    next_cycle = _with_hash(next_cycle)
    atomic_write_json(output_path, next_cycle)
    return next_cycle


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="fortune-learning-cycle")
    sub = p.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create")
    create.add_argument("--cycle-id", required=True)
    create.add_argument("--group-id", required=True)
    create.add_argument("--unit-plan", required=True)
    create.add_argument("--output", required=True)
    create.add_argument("--thresholds")
    create.add_argument("--bindings")

    evaluate = sub.add_parser("evaluate-question")
    evaluate.add_argument("--cycle", required=True)
    evaluate.add_argument("--evidence", required=True)
    evaluate.add_argument("--output", required=True)

    advance = sub.add_parser("advance")
    advance.add_argument("--cycle", required=True)
    advance.add_argument("--evaluation", required=True)
    advance.add_argument("--output", required=True)
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "create":
            raw = read_json(args.unit_plan)
            units = raw["units"] if isinstance(raw, dict) else raw
            result = create_cycle(
                args.cycle_id,
                args.group_id,
                units,
                args.output,
                thresholds=read_json(args.thresholds) if args.thresholds else None,
                bindings=read_json(args.bindings) if args.bindings else None,
            )
        elif args.command == "evaluate-question":
            result = evaluate_question_training(args.cycle, args.evidence, args.output)
        else:
            result = advance_cycle(args.cycle, args.evaluation, args.output)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except FortuneError as exc:
        print(json.dumps({"status": exc.status, "error": str(exc)}, ensure_ascii=False), file=__import__("sys").stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
