from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .training_corrected import advance_cycle, evaluate_question_training
from .util import FortuneError, atomic_write_json, canonical_bytes, read_json, sha256_bytes, sha256_file, utc_now

REQUEST_SCHEMA = "GROUP-TRAINING-FINALIZE-REQUEST-V1"
MANIFEST_SCHEMA = "GROUP-TRAINING-EVIDENCE-MANIFEST-V1"
RECEIPT_SCHEMA = "GROUP-TRAINING-FINALIZE-RECEIPT-V1"
COMPLETE_STATUSES = {
    "TRAINING_SET_COMPLETE_AWAITING_UNSEEN_BLIND_TEST",
    "TRAINING_SET_COMPLETE_BELOW_ROLLING_TARGET_REQUIRES_RESHAPING",
}


def _require(condition: bool, message: str, status: str) -> None:
    if not condition:
        raise FortuneError(message, status=status)


def _hash_matches(value: dict[str, Any]) -> bool:
    expected = value.get("object_hash")
    actual = sha256_bytes(canonical_bytes({k: v for k, v in value.items() if k != "object_hash"}))
    return isinstance(expected, str) and expected == actual


def _resolve_within(root: Path, value: str | Path, status: str) -> Path:
    exact_root = root.resolve()
    path = Path(value).resolve()
    _require(exact_root == path or exact_root in path.parents, f"path escapes run root: {value}", status)
    return path


def finalize_group_training(request_path: str | Path) -> dict[str, Any]:
    request_file = Path(request_path)
    request = read_json(request_file)
    _require(request.get("schema") == REQUEST_SCHEMA, "training finalize request schema invalid", "TRAINING_FINALIZE_REQUEST_INVALID")
    _require(request.get("status") == "REQUESTED", "training finalize request status invalid", "TRAINING_FINALIZE_REQUEST_INVALID")
    _require(_hash_matches(request), "training finalize request hash invalid", "TRAINING_FINALIZE_REQUEST_HASH_INVALID")

    run_root = Path(str(request.get("run_root", ""))).resolve()
    _require(run_root.is_dir(), "training run root missing", "TRAINING_RUN_ROOT_MISSING")
    output_root = _resolve_within(run_root, request.get("output_root") or run_root / "training", "TRAINING_OUTPUT_PATH_INVALID")
    intake_path = _resolve_within(run_root, request.get("training_intake_path", ""), "TRAINING_INTAKE_PATH_INVALID")
    manifest_path = _resolve_within(run_root, request.get("evidence_manifest_path", ""), "TRAINING_EVIDENCE_PATH_INVALID")
    _require(intake_path.is_file(), "training intake missing", "TRAINING_INTAKE_MISSING")
    _require(manifest_path.is_file(), "training evidence manifest missing", "TRAINING_EVIDENCE_MANIFEST_MISSING")

    intake = read_json(intake_path)
    manifest = read_json(manifest_path)
    _require(intake.get("schema") == "GROUP-TRAINING-INTAKE-V1", "training intake schema invalid", "TRAINING_INTAKE_INVALID")
    _require(intake.get("status") == "LEARNING_ACTIVE", "training intake not active", "TRAINING_INTAKE_INVALID")
    _require(_hash_matches(intake), "training intake hash invalid", "TRAINING_INTAKE_HASH_INVALID")
    _require(manifest.get("schema") == MANIFEST_SCHEMA, "training evidence manifest schema invalid", "TRAINING_EVIDENCE_MANIFEST_INVALID")
    _require(manifest.get("status") == "READY_FOR_SERIAL_EVALUATION", "training evidence manifest not ready", "TRAINING_EVIDENCE_MANIFEST_INVALID")
    _require(_hash_matches(manifest), "training evidence manifest hash invalid", "TRAINING_EVIDENCE_MANIFEST_HASH_INVALID")

    for field in ("group_id", "group_run_id"):
        expected = request.get(field)
        _require(expected == intake.get(field) == manifest.get(field), f"training {field} mismatch", "TRAINING_FINALIZE_IDENTITY_MISMATCH")

    cycle_path = _resolve_within(run_root, intake.get("cycle_path", ""), "TRAINING_CYCLE_PATH_INVALID")
    _require(cycle_path.is_file(), "learning cycle missing", "TRAINING_CYCLE_MISSING")
    cycle = read_json(cycle_path)
    _require(_hash_matches(cycle), "learning cycle hash invalid", "TRAINING_CYCLE_HASH_INVALID")
    _require(cycle.get("object_hash") == intake.get("cycle_object_hash"), "learning cycle intake hash mismatch", "TRAINING_CYCLE_HASH_INVALID")
    _require(cycle.get("group_id") == request.get("group_id"), "learning cycle group mismatch", "TRAINING_FINALIZE_IDENTITY_MISMATCH")

    units = list(cycle.get("units", []))
    rows = list(manifest.get("units", []))
    expected_unit_ids = [str(row.get("unit_id")) for row in units]
    actual_unit_ids = [str(row.get("unit_id")) for row in rows]
    _require(actual_unit_ids == expected_unit_ids, "training evidence unit order/set mismatch", "TRAINING_EVIDENCE_UNIT_SET_MISMATCH")
    _require(len(set(actual_unit_ids)) == len(actual_unit_ids), "duplicate training evidence unit", "TRAINING_EVIDENCE_UNIT_SET_MISMATCH")
    _require(intake.get("training_unit_count") == len(units), "training intake unit count mismatch", "TRAINING_UNIT_COUNT_MISMATCH")
    _require(manifest.get("training_unit_count") == len(units), "training evidence unit count mismatch", "TRAINING_UNIT_COUNT_MISMATCH")

    # Preflight the complete manifest before writing a single evaluation or cycle
    # state.  A missing/tampered later unit must not leave a partial training run.
    preflight: list[tuple[dict[str, Any], dict[str, Any], Path, dict[str, Any]]] = []
    for unit, row in zip(units, rows, strict=True):
        evidence_path = _resolve_within(run_root, row.get("evidence_path", ""), "TRAINING_EVIDENCE_PATH_INVALID")
        _require(evidence_path.is_file(), f"training evidence missing: {evidence_path}", "TRAINING_EVIDENCE_MISSING")
        _require(row.get("evidence_sha256") == sha256_file(evidence_path), "training evidence file hash mismatch", "TRAINING_EVIDENCE_HASH_INVALID")
        evidence = read_json(evidence_path)
        _require(_hash_matches(evidence), "training evidence object hash invalid", "TRAINING_EVIDENCE_HASH_INVALID")
        _require(evidence.get("object_hash") == row.get("evidence_object_hash"), "training evidence manifest object hash mismatch", "TRAINING_EVIDENCE_HASH_INVALID")
        _require(evidence.get("unit_id") == unit.get("unit_id"), "training evidence unit mismatch", "TRAINING_UNIT_ID_MISMATCH")
        _require(
            evidence.get("first_blind_observation_hash") == unit.get("first_blind_observation_hash"),
            "training evidence first-blind binding mismatch",
            "FIRST_BLIND_OBSERVATION_MISMATCH",
        )
        preflight.append((unit, row, evidence_path, evidence))

    evaluation_dir = output_root / "evaluations"
    cycle_dir = output_root / "cycle-states"
    evaluation_dir.mkdir(parents=True, exist_ok=True)
    cycle_dir.mkdir(parents=True, exist_ok=True)
    evaluations: list[dict[str, Any]] = []
    current_cycle_path = cycle_path
    last_evaluation: dict[str, Any] | None = None

    for index, (unit, row, evidence_path, evidence) in enumerate(preflight, start=1):
        evaluation_path = evaluation_dir / f"{index:03d}-{unit['unit_id']}.json"
        evaluation = evaluate_question_training(current_cycle_path, evidence_path, evaluation_path)
        _require(evaluation.get("status") == "TRAINING_UNIT_COMPLETE", f"training unit did not complete: {unit['unit_id']}", "TRAINING_UNIT_INCOMPLETE")
        next_cycle_path = cycle_dir / f"{index:03d}-{unit['unit_id']}.json"
        next_cycle = advance_cycle(current_cycle_path, evaluation_path, next_cycle_path)
        evaluations.append({
            "index": index,
            "unit_id": unit["unit_id"],
            "case_id": unit.get("case_ids", [None])[0],
            "question_id": unit.get("question_ids", [None])[0],
            "evidence_path": str(evidence_path),
            "evidence_sha256": sha256_file(evidence_path),
            "evidence_object_hash": evidence["object_hash"],
            "evaluation_path": str(evaluation_path),
            "evaluation_sha256": sha256_file(evaluation_path),
            "evaluation_object_hash": evaluation["object_hash"],
            "cycle_state_path": str(next_cycle_path),
            "cycle_state_sha256": sha256_file(next_cycle_path),
            "cycle_state_object_hash": next_cycle["object_hash"],
            "status": evaluation["status"],
        })
        last_evaluation = evaluation
        current_cycle_path = next_cycle_path

    final_cycle = read_json(current_cycle_path)
    _require(final_cycle.get("status") in COMPLETE_STATUSES, "final cycle status invalid", "TRAINING_FINALIZE_INCOMPLETE")
    _require(final_cycle.get("current_unit_index") == len(units), "final cycle index incomplete", "TRAINING_FINALIZE_INCOMPLETE")
    _require(len(final_cycle.get("completed_training_units", [])) == len(units), "completed training unit count mismatch", "TRAINING_FINALIZE_INCOMPLETE")

    case_order: list[str] = []
    case_counts: dict[str, int] = {}
    for unit in units:
        case_id = str(unit.get("case_ids", [""])[0])
        if case_id not in case_counts:
            case_order.append(case_id)
            case_counts[case_id] = 0
        case_counts[case_id] += 1
    cases = [
        {
            "case_id": case_id,
            "question_unit_count": case_counts[case_id],
            "completed_question_unit_count": sum(1 for row in evaluations if row["case_id"] == case_id and row["status"] == "TRAINING_UNIT_COMPLETE"),
            "status": "CASE_TRAINING_COMPLETE",
        }
        for case_id in case_order
    ]

    receipt_path = output_root / "training-finalize-receipt.json"
    receipt = {
        "schema": RECEIPT_SCHEMA,
        "status": "TRAINING_FINALIZE_PASS",
        "group_id": request["group_id"],
        "group_run_id": request["group_run_id"],
        "training_intake_path": str(intake_path),
        "training_intake_sha256": sha256_file(intake_path),
        "training_intake_object_hash": intake["object_hash"],
        "evidence_manifest_path": str(manifest_path),
        "evidence_manifest_sha256": sha256_file(manifest_path),
        "evidence_manifest_object_hash": manifest["object_hash"],
        "case_count": len(cases),
        "training_unit_count": len(units),
        "completed_training_unit_count": len(evaluations),
        "cases": cases,
        "evaluations": evaluations,
        "final_cycle_path": str(current_cycle_path),
        "final_cycle_sha256": sha256_file(current_cycle_path),
        "final_cycle_object_hash": final_cycle["object_hash"],
        "training_set_status": final_cycle["status"],
        "rolling_first_blind_accuracy": (last_evaluation or {}).get("rolling_first_blind_accuracy"),
        "new_first_blind_score_eligibility": intake.get("new_first_blind_score_eligibility"),
        "post_reveal_replays_count_as_accuracy": False,
        "unseen_generalization_status": final_cycle.get("generalization_status"),
        "formal_model_release_promotion": "NOT_PERFORMED_REQUIRES_SEPARATE_CANDIDATE_PROMOTION_GATE",
        "answer_memorization_rule_permission": "NO",
        "completed_at": utc_now(),
    }
    receipt["object_hash"] = sha256_bytes(canonical_bytes(receipt))
    target = atomic_write_json(receipt_path, receipt)
    return {**receipt, "output_path": str(target), "output_sha256": sha256_file(target)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="fortune-training-finalize")
    parser.add_argument("--request", required=True)
    args = parser.parse_args(argv)
    try:
        result = finalize_group_training(args.request)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except FortuneError as exc:
        print(json.dumps({"status": exc.status, "error": str(exc)}, ensure_ascii=False), file=__import__("sys").stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
