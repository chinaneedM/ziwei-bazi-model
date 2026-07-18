from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, canonical_bytes, read_json, sha256_bytes, slug, utc_now

LEARNING_PHASES = (
    "ABSORB",
    "DECOMPOSE",
    "FILL",
    "RESHAPE",
    "APPLY",
    "GENERATE",
)

UNIT_MODES = {"QUESTION", "CASE", "GROUP"}
PATCH_LAYERS = {
    "RETRIEVAL",
    "SEMANTIC",
    "ENTITY",
    "TEMPORAL",
    "ENDPOINT",
    "PAIRWISE",
    "FUSION",
    "METHOD",
    "BASE_KNOWLEDGE",
}

CONTAMINATION_FIELDS = {
    "correct_answer",
    "answer_vector",
    "answer_letter",
    "revealed_answer",
    "ground_truth",
    "postreveal_selection",
}

OPTION_DIRECTION_RE = re.compile(
    r"(?:case|question|example)[-_ ]?[0-9a-z.]+.{0,120}(?:always|must|直接|固定|一律).{0,40}(?:选|choose|rank).{0,12}\b[A-D]\b",
    re.IGNORECASE | re.DOTALL,
)


def _require(condition: bool, message: str, status: str) -> None:
    if not condition:
        raise FortuneError(message, status=status)


def _rate(hits: int, total: int) -> float:
    return hits / total if total else 0.0


def _default_thresholds(unit_mode: str) -> dict[str, Any]:
    return {
        "top1_mastery_rate": 0.80,
        "top2_diagnostic_rate": 0.90,
        "prior_unit_retention_rate": 0.80,
        "min_clean_cold_start_replays": 5 if unit_mode == "QUESTION" else 2,
        "max_regression_damage_questions": 0,
    }


def create_learning_cycle(
    cycle_id: str,
    group_id: str,
    unit_mode: str,
    units: list[dict[str, Any]],
    output_path: str | Path,
    *,
    thresholds: dict[str, Any] | None = None,
    source_baseline_id: str | None = None,
    main_prompt_runtime_id: str | None = None,
    runtime_code_commit: str | None = None,
) -> dict[str, Any]:
    mode = unit_mode.upper()
    _require(mode in UNIT_MODES, f"unsupported unit mode: {unit_mode}", "TRAINING_UNIT_MODE_INVALID")
    _require(bool(units), "learning cycle requires at least one unit", "TRAINING_UNIT_PLAN_EMPTY")

    normalized_units: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(units):
        unit_id = slug(str(raw.get("unit_id") or f"UNIT-{index + 1:03d}"))
        _require(unit_id not in seen, f"duplicate unit_id: {unit_id}", "TRAINING_UNIT_DUPLICATE")
        seen.add(unit_id)
        case_ids = [str(v) for v in raw.get("case_ids", [])]
        question_ids = [str(v) for v in raw.get("question_ids", [])]
        if mode == "QUESTION":
            _require(len(question_ids) == 1, f"{unit_id} must bind exactly one question", "QUESTION_UNIT_SCOPE_INVALID")
        elif mode == "CASE":
            _require(len(case_ids) == 1 and bool(question_ids), f"{unit_id} must bind one case and its questions", "CASE_UNIT_SCOPE_INVALID")
        else:
            _require(bool(case_ids) and bool(question_ids), f"{unit_id} must bind group cases and questions", "GROUP_UNIT_SCOPE_INVALID")
        normalized_units.append(
            {
                "unit_id": unit_id,
                "case_ids": case_ids,
                "question_ids": question_ids,
                "status": "PENDING",
                "mastered_evaluation_id": None,
            }
        )

    merged_thresholds = _default_thresholds(mode)
    if thresholds:
        merged_thresholds.update(thresholds)
    _require(
        0 < float(merged_thresholds["top1_mastery_rate"]) <= 1,
        "top1 mastery rate must be in (0, 1]",
        "TRAINING_THRESHOLD_INVALID",
    )
    _require(
        int(merged_thresholds["min_clean_cold_start_replays"]) >= 1,
        "minimum clean replay count must be positive",
        "TRAINING_THRESHOLD_INVALID",
    )

    result = {
        "schema": "LEARNING-CYCLE-V2",
        "cycle_id": slug(cycle_id),
        "group_id": slug(group_id),
        "dataset_role": "REVEALED_TRAINING_SET",
        "learning_model": {
            "phases": list(LEARNING_PHASES),
            "principle": "ABSORB_DECOMPOSE_FILL_RESHAPE_APPLY_GENERATE",
            "answer_use_boundary": {
                "diagnosis": "ALLOWED_AFTER_IMMUTABLE_FREEZE",
                "prediction": "FORBIDDEN",
                "clean_replay": "FORBIDDEN",
                "patch_direction_rule": "FORBIDDEN",
            },
        },
        "unit_mode": mode,
        "units": normalized_units,
        "current_unit_index": 0,
        "thresholds": merged_thresholds,
        "bindings": {
            "source_baseline_id": source_baseline_id,
            "main_prompt_runtime_id": main_prompt_runtime_id,
            "runtime_code_commit": runtime_code_commit,
        },
        "mastered_units": [],
        "history": [],
        "status": "LEARNING_ACTIVE",
        "generalization_status": "NOT_TESTED_ON_UNSEEN_CASES",
        "created_at": utc_now(),
    }
    result["object_hash"] = sha256_bytes(canonical_bytes({k: v for k, v in result.items() if k != "object_hash"}))
    atomic_write_json(output_path, result)
    return result


def _row_is_clean(row: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if row.get("clean_cold_start") is not True:
        reasons.append("COLD_START_NOT_PROVEN")
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
    return not reasons, reasons


def _scope_rows(rows: list[dict[str, Any]], unit: dict[str, Any]) -> list[dict[str, Any]]:
    question_ids = set(unit.get("question_ids", []))
    case_ids = set(unit.get("case_ids", []))
    scoped = []
    for row in rows:
        if question_ids and row.get("question_id") not in question_ids:
            continue
        if case_ids and row.get("case_id") not in case_ids:
            continue
        scoped.append(row)
    return scoped


def _evaluate_scope(
    rows: list[dict[str, Any]],
    unit: dict[str, Any],
    thresholds: dict[str, Any],
) -> dict[str, Any]:
    scoped = _scope_rows(rows, unit)
    clean_rows: list[dict[str, Any]] = []
    rejected_rows: list[dict[str, Any]] = []
    for row in scoped:
        clean, reasons = _row_is_clean(row)
        if clean:
            clean_rows.append(row)
        else:
            rejected_rows.append(
                {
                    "attempt_id": row.get("attempt_id"),
                    "case_id": row.get("case_id"),
                    "question_id": row.get("question_id"),
                    "reasons": reasons,
                }
            )

    attempts = sorted({str(row.get("attempt_id")) for row in clean_rows if row.get("attempt_id")})
    top1_hits = sum(bool(row.get("top1_correct")) for row in clean_rows)
    top2_hits = sum(bool(row.get("top2_hit")) for row in clean_rows)
    total = len(clean_rows)
    top1_rate = _rate(top1_hits, total)
    top2_rate = _rate(top2_hits, total)
    required_replays = int(thresholds["min_clean_cold_start_replays"])

    reasons: list[str] = []
    if len(attempts) < required_replays:
        reasons.append("INSUFFICIENT_CLEAN_COLD_START_REPLAYS")
    if top1_rate < float(thresholds["top1_mastery_rate"]):
        reasons.append("TOP1_MASTERY_BELOW_THRESHOLD")
    if top2_rate < float(thresholds["top2_diagnostic_rate"]):
        reasons.append("TOP2_DIAGNOSTIC_BELOW_THRESHOLD")
    if rejected_rows:
        reasons.append("REJECTED_REPLAY_ROWS_PRESENT")

    return {
        "unit_id": unit["unit_id"],
        "scoped_row_count": len(scoped),
        "clean_row_count": total,
        "clean_attempt_count": len(attempts),
        "required_clean_attempt_count": required_replays,
        "top1_hits": top1_hits,
        "top1_rate": top1_rate,
        "top2_hits": top2_hits,
        "top2_rate": top2_rate,
        "rejected_rows": rejected_rows,
        "status": "MASTERED" if not reasons else "NOT_MASTERED",
        "reasons": reasons,
    }


def evaluate_learning_cycle(
    cycle_path: str | Path,
    replay_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    cycle = read_json(cycle_path)
    replay = read_json(replay_path)
    _require(cycle.get("schema") == "LEARNING-CYCLE-V2", "learning cycle schema invalid", "TRAINING_CYCLE_SCHEMA_INVALID")
    _require(replay.get("schema") == "CLEAN-COLD-START-REPLAY-V2", "replay schema invalid", "TRAINING_REPLAY_SCHEMA_INVALID")
    _require(replay.get("cycle_id") == cycle.get("cycle_id"), "cycle id mismatch", "TRAINING_CYCLE_ID_MISMATCH")
    _require(replay.get("answer_payload_present") is False, "answer payload present in replay", "TRAINING_ANSWER_CONTAMINATION")
    _require(replay.get("old_prediction_payload_present") is False, "old prediction present in replay", "TRAINING_OLD_OUTPUT_CONTAMINATION")
    _require(replay.get("old_error_explanation_present") is False, "old error explanation present in replay", "TRAINING_OLD_OUTPUT_CONTAMINATION")

    current_index = int(cycle["current_unit_index"])
    _require(current_index < len(cycle["units"]), "cycle has no active unit", "TRAINING_CYCLE_ALREADY_COMPLETE")
    rows = list(replay.get("rows", []))
    current = _evaluate_scope(rows, cycle["units"][current_index], cycle["thresholds"])

    prior_results = []
    prior_retention_failures = []
    for unit in cycle["units"][:current_index]:
        result = _evaluate_scope(rows, unit, cycle["thresholds"])
        prior_results.append(result)
        if result["top1_rate"] < float(cycle["thresholds"]["prior_unit_retention_rate"]):
            prior_retention_failures.append(unit["unit_id"])

    contamination = any(
        reason in {
            "ANSWER_VISIBILITY_NOT_DENIED",
            "ANSWER_FREE_INPUT_NOT_PROVEN",
            "CASE_SPECIFIC_RULE_DETECTED",
        }
        for row in current["rejected_rows"]
        for reason in row["reasons"]
    )
    provenance_invalid = any(
        reason in {"SOURCE_PROVENANCE_NOT_PASS", "PAIRWISE_REPLAY_NOT_PASS"}
        for row in current["rejected_rows"]
        for reason in row["reasons"]
    )
    mastery_pass = (
        current["status"] == "MASTERED"
        and not prior_retention_failures
        and int(replay.get("regression_damage_questions", 0))
        <= int(cycle["thresholds"]["max_regression_damage_questions"])
    )

    if contamination:
        status = "HOLD_ANSWER_OR_CASE_RULE_CONTAMINATION"
        next_phase = None
    elif provenance_invalid:
        status = "HOLD_INVALID_PROVENANCE"
        next_phase = None
    elif mastery_pass:
        status = "PASS"
        next_phase = "GENERATE" if current_index == len(cycle["units"]) - 1 else "APPLY"
    else:
        status = "CONTINUE_LEARNING"
        if current["top1_rate"] == 0:
            next_phase = "DECOMPOSE"
        elif current["clean_attempt_count"] < current["required_clean_attempt_count"]:
            next_phase = "APPLY"
        elif prior_retention_failures:
            next_phase = "RESHAPE"
        else:
            next_phase = "FILL"

    evaluation = {
        "schema": "LEARNING-CYCLE-EVALUATION-V2",
        "evaluation_id": f"EVAL-{slug(cycle['cycle_id'])}-{current_index + 1:03d}-{slug(str(replay.get('replay_id', 'REPLAY')))}",
        "cycle_id": cycle["cycle_id"],
        "unit_mode": cycle["unit_mode"],
        "current_unit_index": current_index,
        "current_unit": current,
        "prior_unit_results": prior_results,
        "prior_retention_failures": prior_retention_failures,
        "regression_damage_questions": int(replay.get("regression_damage_questions", 0)),
        "mastery_pass": mastery_pass,
        "status": status,
        "next_learning_phase": next_phase,
        "claim_boundary": {
            "training_mastery": "MEASURED",
            "unseen_blind_accuracy": "NOT_MEASURED",
            "generalization": "NOT_PROVEN",
        },
        "created_at": utc_now(),
    }
    evaluation["object_hash"] = sha256_bytes(canonical_bytes({k: v for k, v in evaluation.items() if k != "object_hash"}))
    atomic_write_json(output_path, evaluation)
    return evaluation


def advance_learning_cycle(
    cycle_path: str | Path,
    evaluation_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    cycle = read_json(cycle_path)
    evaluation = read_json(evaluation_path)
    _require(cycle.get("schema") == "LEARNING-CYCLE-V2", "learning cycle schema invalid", "TRAINING_CYCLE_SCHEMA_INVALID")
    _require(evaluation.get("schema") == "LEARNING-CYCLE-EVALUATION-V2", "evaluation schema invalid", "TRAINING_EVALUATION_SCHEMA_INVALID")
    _require(evaluation.get("cycle_id") == cycle.get("cycle_id"), "cycle id mismatch", "TRAINING_CYCLE_ID_MISMATCH")

    next_cycle = json.loads(json.dumps(cycle))
    current_index = int(next_cycle["current_unit_index"])
    event = {
        "evaluation_id": evaluation["evaluation_id"],
        "unit_id": next_cycle["units"][current_index]["unit_id"],
        "status": evaluation["status"],
        "mastery_pass": evaluation["mastery_pass"],
        "next_learning_phase": evaluation.get("next_learning_phase"),
        "recorded_at": utc_now(),
    }
    next_cycle["history"].append(event)

    if evaluation["status"].startswith("HOLD_"):
        next_cycle["status"] = evaluation["status"]
    elif evaluation["mastery_pass"]:
        unit = next_cycle["units"][current_index]
        unit["status"] = "MASTERED"
        unit["mastered_evaluation_id"] = evaluation["evaluation_id"]
        if unit["unit_id"] not in next_cycle["mastered_units"]:
            next_cycle["mastered_units"].append(unit["unit_id"])
        if current_index + 1 < len(next_cycle["units"]):
            next_cycle["current_unit_index"] = current_index + 1
            next_cycle["status"] = "LEARNING_ACTIVE"
        else:
            next_cycle["status"] = "TRAINING_SET_MASTERED_AWAITING_UNSEEN_BLIND_TEST"
            next_cycle["generalization_status"] = "REQUIRES_FROZEN_UNSEEN_BLIND_TEST_BLOCK"
    else:
        next_cycle["status"] = "LEARNING_ACTIVE"

    next_cycle["updated_at"] = utc_now()
    next_cycle["parent_cycle_hash"] = cycle.get("object_hash")
    next_cycle["object_hash"] = sha256_bytes(canonical_bytes({k: v for k, v in next_cycle.items() if k != "object_hash"}))
    atomic_write_json(output_path, next_cycle)
    return next_cycle


def validate_learning_patch(
    patch_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    patch = read_json(patch_path)
    layer = str(patch.get("layer", "")).upper()
    _require(layer in PATCH_LAYERS, f"unsupported patch layer: {layer}", "LEARNING_PATCH_LAYER_INVALID")
    _require(patch.get("generalization_scope") in {"ALL_CASES", "ALL_CASES_MATCHING_EXPLICIT_CONDITIONS"}, "generalization scope missing", "LEARNING_PATCH_NOT_GENERALIZED")
    _require(bool(patch.get("mechanism_change")), "mechanism change required", "LEARNING_PATCH_MECHANISM_MISSING")
    _require(bool(patch.get("counterexample_tests")), "counterexample tests required", "LEARNING_PATCH_COUNTEREXAMPLE_MISSING")

    serialized = json.dumps(patch, ensure_ascii=False, sort_keys=True)
    field_hits = sorted(field for field in CONTAMINATION_FIELDS if field in serialized.lower())
    direction_hit = bool(OPTION_DIRECTION_RE.search(serialized))
    case_specific_conditions = patch.get("case_specific_conditions") not in (None, [], {}, False)

    reasons = []
    if field_hits:
        reasons.append("ANSWER_FIELD_PRESENT")
    if direction_hit:
        reasons.append("CASE_OPTION_DIRECTION_RULE")
    if case_specific_conditions:
        reasons.append("CASE_SPECIFIC_CONDITION_PRESENT")

    promotable = not reasons
    knowledge_review = None
    if layer == "BASE_KNOWLEDGE":
        source_parents = patch.get("source_confirmed_parents", [])
        reproduced_units = patch.get("reproduced_unit_ids", [])
        if len(source_parents) < 2:
            reasons.append("BASE_KNOWLEDGE_REQUIRES_TWO_INDEPENDENT_SOURCE_PARENTS")
        if len(set(reproduced_units)) < 2:
            reasons.append("BASE_KNOWLEDGE_REQUIRES_MULTI_UNIT_REPRODUCTION")
        promotable = not reasons
        knowledge_review = "PROMOTABLE_CANDIDATE" if promotable else "RESEARCH_CANDIDATE_ONLY"

    result = {
        "schema": "LEARNING-PATCH-VALIDATION-V2",
        "patch_id": patch.get("patch_id"),
        "layer": layer,
        "status": "PASS" if promotable else "REJECTED",
        "promotable": promotable,
        "knowledge_review": knowledge_review,
        "reasons": reasons,
        "answer_field_hits": field_hits,
        "case_option_direction_rule_detected": direction_hit,
        "created_at": utc_now(),
    }
    atomic_write_json(output_path, result)
    return result


def _read_units(path: str | Path) -> list[dict[str, Any]]:
    value = read_json(path)
    if isinstance(value, dict) and isinstance(value.get("units"), list):
        return value["units"]
    if isinstance(value, list):
        return value
    raise FortuneError("unit plan must be a list or object with units", status="TRAINING_UNIT_PLAN_INVALID")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="fortune-learning-cycle")
    sub = p.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create")
    create.add_argument("--cycle-id", required=True)
    create.add_argument("--group-id", required=True)
    create.add_argument("--unit-mode", choices=sorted(UNIT_MODES), required=True)
    create.add_argument("--unit-plan", required=True)
    create.add_argument("--output", required=True)
    create.add_argument("--thresholds")
    create.add_argument("--source-baseline-id")
    create.add_argument("--main-prompt-runtime-id")
    create.add_argument("--runtime-code-commit")

    evaluate = sub.add_parser("evaluate")
    evaluate.add_argument("--cycle", required=True)
    evaluate.add_argument("--replay", required=True)
    evaluate.add_argument("--output", required=True)

    advance = sub.add_parser("advance")
    advance.add_argument("--cycle", required=True)
    advance.add_argument("--evaluation", required=True)
    advance.add_argument("--output", required=True)

    patch = sub.add_parser("validate-patch")
    patch.add_argument("--patch", required=True)
    patch.add_argument("--output", required=True)
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "create":
            result = create_learning_cycle(
                args.cycle_id,
                args.group_id,
                args.unit_mode,
                _read_units(args.unit_plan),
                args.output,
                thresholds=read_json(args.thresholds) if args.thresholds else None,
                source_baseline_id=args.source_baseline_id,
                main_prompt_runtime_id=args.main_prompt_runtime_id,
                runtime_code_commit=args.runtime_code_commit,
            )
        elif args.command == "evaluate":
            result = evaluate_learning_cycle(args.cycle, args.replay, args.output)
        elif args.command == "advance":
            result = advance_learning_cycle(args.cycle, args.evaluation, args.output)
        else:
            result = validate_learning_patch(args.patch, args.output)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except FortuneError as exc:
        print(json.dumps({"status": exc.status, "error": str(exc)}, ensure_ascii=False), file=__import__("sys").stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
