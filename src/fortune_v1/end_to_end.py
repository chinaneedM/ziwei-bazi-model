from __future__ import annotations

import argparse
import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

from .staged_access import release_postblind_stage
from .training_corrected import create_cycle, default_thresholds
from .util import (
    FortuneError,
    atomic_write_json,
    canonical_bytes,
    read_json,
    sha256_bytes,
    sha256_file,
    slug,
    utc_now,
)

PREBLIND_STATUS = "READY_FOR_PREBLIND_MODELING"
POSTBLIND_STATUS = "POSTBLIND_OPTION_CHALLENGE_RELEASED"
GROUP_FREEZE_STATUS = "GROUP_PREDICTION_FREEZE_PASS"


def _require(condition: bool, message: str, status: str) -> None:
    if not condition:
        raise FortuneError(message, status=status)


def _with_hash(value: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(value)
    result.pop("object_hash", None)
    result["object_hash"] = sha256_bytes(canonical_bytes(result))
    return result


def _write_new(path: str | Path, value: dict[str, Any]) -> dict[str, Any]:
    body = _with_hash(value)
    atomic_write_json(path, body)
    return body


def _path_from_rows(rows: list[str], marker: str, status: str) -> Path:
    matches = [Path(v) for v in rows if marker in str(v)]
    _require(len(matches) == 1, f"expected exactly one {marker} path", status)
    return matches[0]


def validate_staged_clean_start(clean_start_path: str | Path) -> dict[str, Any]:
    clean_path = Path(clean_start_path)
    clean = read_json(clean_path)
    _require(clean.get("status") == PREBLIND_STATUS, "clean start status invalid", "CLEAN_START_STAGE_INVALID")
    _require(clean.get("answer_data_available") is False, "answer data available", "ANSWER_ISOLATION_FAILED")
    staged = clean.get("retrieval_policy", {}).get("staged_access", {})
    _require(staged.get("current_stage") == "PREBLIND", "PREBLIND stage missing", "CLEAN_START_STAGE_INVALID")
    _require(staged.get("withheld_paths_not_disclosed_to_prediction_context") is True, "withheld path disclosure gate failed", "WITHHELD_PATH_DISCLOSURE_FAILED")
    _require(staged.get("release_requires") == "MACHINE_VALID_DUAL_TRACK_PREBLIND_SEALS_FOR_ALL_QUESTIONS", "release rule mismatch", "RELEASE_RULE_INVALID")
    case_rows = clean.get("cases", [])
    _require(bool(case_rows), "clean start has no cases", "CLEAN_START_CASES_MISSING")
    checked = []
    for row in case_rows:
        preblind_input = Path(row.get("preblind_input_path", ""))
        skeleton = Path(row.get("preblind_skeleton_path", ""))
        _require(preblind_input.is_file(), f"preblind input missing: {preblind_input}", "PREBLIND_INPUT_MISSING")
        _require(skeleton.is_file(), f"preblind skeleton missing: {skeleton}", "PREBLIND_SKELETON_MISSING")
        _require(sha256_file(preblind_input) == row.get("preblind_input_sha256"), "preblind input hash mismatch", "PREBLIND_INPUT_HASH_MISMATCH")
        _require(sha256_file(skeleton) == row.get("preblind_skeleton_sha256"), "preblind skeleton hash mismatch", "PREBLIND_SKELETON_HASH_MISMATCH")
        skeleton_body = read_json(skeleton)
        _require(skeleton_body.get("schema") == "PREBLIND-PREDICTION-SKELETON-V1", "skeleton schema invalid", "PREBLIND_SKELETON_SCHEMA_INVALID")
        _require(skeleton_body.get("option_visibility") == "WITHHELD", "option visibility invalid", "PREBLIND_OPTION_VISIBILITY_FAILED")
        _require(skeleton_body.get("answer_data_available") is False, "answer data available in skeleton", "ANSWER_ISOLATION_FAILED")
        _require(bool(skeleton_body.get("questions")), "skeleton question rows missing", "PREBLIND_QUESTION_ROWS_MISSING")
        checked.append({"case_id": row["case_id"], "preblind_input_path": str(preblind_input), "preblind_skeleton_path": str(skeleton)})
    return _with_hash({
        "schema": "STAGED-CLEAN-START-VALIDATION-RECEIPT-V1",
        "status": "PASS",
        "group_run_id": clean["group_run_id"],
        "clean_start_path": str(clean_path),
        "clean_start_sha256": sha256_file(clean_path),
        "case_count": len(checked),
        "cases": checked,
        "answer_data_available": False,
        "validated_at": utc_now(),
    })


def _validate_preblind_bundle(plan: dict[str, Any], skeleton: dict[str, Any], bundle: dict[str, Any]) -> None:
    _require(plan.get("schema") == "FORTUNE-STAGED-ACCESS-PLAN-V1", "stage plan schema invalid", "STAGE_PLAN_SCHEMA_INVALID")
    _require(plan.get("status") == PREBLIND_STATUS, "stage plan status invalid", "STAGE_PLAN_STATUS_INVALID")
    _require(bundle.get("schema") == "PREBLIND-SEAL-BUNDLE-V1", "seal bundle schema invalid", "PREBLIND_SEAL_SCHEMA_INVALID")
    _require(bundle.get("status") == "PASS", "seal bundle not PASS", "PREBLIND_SEAL_NOT_PASS")
    _require(bundle.get("case_id") == plan.get("case_id"), "seal case mismatch", "PREBLIND_SEAL_IDENTITY_MISMATCH")
    _require(bundle.get("run_id") == plan.get("run_id"), "seal run mismatch", "PREBLIND_SEAL_IDENTITY_MISMATCH")
    _require(bundle.get("group_run_id") == plan.get("group_run_id"), "seal group mismatch", "PREBLIND_SEAL_IDENTITY_MISMATCH")
    _require(bundle.get("option_access_before_all_seals") is False, "option access occurred before seal", "PREBLIND_OPTION_ACCESS_CONTAMINATION")
    expected = [str(v["question_id"]) for v in skeleton.get("questions", [])]
    rows = bundle.get("questions", [])
    actual = [str(v.get("question_id")) for v in rows]
    _require(actual == expected, "seal question order/set mismatch", "PREBLIND_SEAL_QUESTION_SET_MISMATCH")
    for row in rows:
        _require(row.get("sealed_before_option_access") is True, "question not sealed before option access", "PREBLIND_SEAL_ORDER_FAILED")
        for track in ("ziwei", "bazi"):
            receipt = row.get(track, {})
            _require(receipt.get("status") == "PASS", f"{track} seal not PASS", "PREBLIND_TRACK_SEAL_INVALID")
            for field in ("model_hash", "seal_hash"):
                value = receipt.get(field)
                _require(isinstance(value, str) and len(value) == 64, f"invalid {track} {field}", "PREBLIND_TRACK_SEAL_INVALID")
        _require(row.get("ziwei", {}).get("model_hash") != row.get("bazi", {}).get("model_hash"), "track model hashes must be independent", "TRACK_INDEPENDENCE_FAILED")


def release_group_postblind(request_path: str | Path) -> dict[str, Any]:
    request = read_json(request_path)
    _require(request.get("schema") == "GROUP-POSTBLIND-RELEASE-REQUEST-V1", "release request schema invalid", "POSTBLIND_REQUEST_INVALID")
    _require(request.get("status") == "REQUESTED", "release request status invalid", "POSTBLIND_REQUEST_INVALID")
    clean_path = Path(request["clean_start_path"])
    clean = read_json(clean_path)
    validation = validate_staged_clean_start(clean_path)
    _require(clean.get("group_run_id") == request.get("group_run_id"), "group run mismatch", "POSTBLIND_REQUEST_IDENTITY_MISMATCH")
    case_rows = {row["case_id"]: row for row in clean["cases"]}
    seal_rows = request.get("case_seal_bundles", [])
    _require({v.get("case_id") for v in seal_rows} == set(case_rows), "seal bundle case set mismatch", "PREBLIND_SEAL_CASE_SET_MISMATCH")
    output_root = Path(request.get("output_root") or clean_path.parent)
    receipts = []
    for seal_row in seal_rows:
        case_id = seal_row["case_id"]
        case = case_rows[case_id]
        plan_path = Path(seal_row.get("stage_plan_path") or output_root / "runtime-packets" / case_id / "stage-access-plan.json")
        skeleton_path = Path(case["preblind_skeleton_path"])
        bundle_path = Path(seal_row["seal_bundle_path"])
        _require(plan_path.is_file(), f"stage plan missing: {plan_path}", "STAGE_PLAN_MISSING")
        _require(bundle_path.is_file(), f"seal bundle missing: {bundle_path}", "PREBLIND_SEAL_BUNDLE_MISSING")
        plan = read_json(plan_path)
        skeleton = read_json(skeleton_path)
        bundle = read_json(bundle_path)
        _validate_preblind_bundle(plan, skeleton, bundle)
        receipt_path = output_root / "postblind-access" / f"{case_id}.json"
        receipt = release_postblind_stage(plan_path, bundle_path, receipt_path)
        receipts.append({
            "case_id": case_id,
            "run_id": case["case_run_id"],
            "stage_plan_path": str(plan_path),
            "seal_bundle_path": str(bundle_path),
            "receipt_path": str(receipt_path),
            "receipt_sha256": sha256_file(receipt_path),
            "receipt_object_hash": receipt.get("object_hash"),
        })
    group_receipt_path = output_root / "group-postblind-access.json"
    result = _write_new(group_receipt_path, {
        "schema": "GROUP-POSTBLIND-ACCESS-RECEIPT-V1",
        "status": POSTBLIND_STATUS,
        "group_id": clean["group_id"],
        "group_run_id": clean["group_run_id"],
        "clean_start_path": str(clean_path),
        "clean_start_sha256": sha256_file(clean_path),
        "clean_start_validation_hash": validation["object_hash"],
        "case_count": len(receipts),
        "cases": receipts,
        "answer_data_available": False,
        "released_at": utc_now(),
    })
    return {**result, "output_path": str(group_receipt_path)}


def _question_options(option_payload: dict[str, Any]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for row in option_payload.get("questions", []):
        ids = [str(v.get("option_id")) for v in row.get("options", [])]
        _require(len(ids) >= 2 and len(ids) == len(set(ids)), "option set invalid", "OPTION_SET_INVALID")
        result[str(row["question_id"])] = ids
    _require(bool(result), "option payload empty", "OPTION_SET_INVALID")
    return result


def _validate_pairwise(question: dict[str, Any], option_ids: list[str]) -> None:
    rows = question.get("pairwise_rows", [])
    expected_count = len(option_ids) * (len(option_ids) - 1) // 2
    _require(len(rows) == expected_count, "pairwise row count invalid", "PAIRWISE_ROW_COUNT_INVALID")
    seen: set[tuple[str, str]] = set()
    winners: dict[str, int] = {v: 0 for v in option_ids}
    for row in rows:
        left, right = str(row.get("left", "")), str(row.get("right", ""))
        pair = tuple(sorted((left, right)))
        _require(left in option_ids and right in option_ids and left != right and pair not in seen, "pairwise pair invalid", "PAIRWISE_PAIR_SET_INVALID")
        seen.add(pair)
        direction = row.get("direction")
        _require(direction in {"LEFT_AHEAD", "RIGHT_AHEAD", "TRUE_TIE"}, "pairwise direction invalid", "PAIRWISE_DIRECTION_INVALID")
        _require(bool(row.get("decisive_rule")) and bool(row.get("reason")), "pairwise decision payload incomplete", "PAIRWISE_PAYLOAD_INCOMPLETE")
        _require(isinstance(row.get("left_vector"), dict) and isinstance(row.get("right_vector"), dict), "pairwise vectors missing", "PAIRWISE_VECTOR_MISSING")
        if direction == "LEFT_AHEAD":
            winners[left] += 1
        elif direction == "RIGHT_AHEAD":
            winners[right] += 1
    _require(len(seen) == expected_count, "pairwise pair set incomplete", "PAIRWISE_PAIR_SET_INVALID")
    ranked = sorted(option_ids, key=lambda item: (-winners[item], option_ids.index(item)))
    _require(question.get("top1") == ranked[0], "top1 not derived from pairwise matrix", "TOP1_PAIRWISE_DERIVATION_FAILED")
    _require(question.get("top2") == ranked[1], "top2 not derived from pairwise matrix", "TOP2_PAIRWISE_DERIVATION_FAILED")
    competitor = question.get("strongest_competitor") or {}
    _require(competitor.get("relative_first") == ranked[0] and competitor.get("relative_second") == ranked[1], "strongest competitor not derived", "STRONGEST_COMPETITOR_INVALID")


def _validate_prediction_bundle(bundle: dict[str, Any], case_receipt: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, list[str]]]:
    _require(bundle.get("schema") == "POSTBLIND-PREDICTION-BUNDLE-V1", "prediction bundle schema invalid", "PREDICTION_BUNDLE_SCHEMA_INVALID")
    _require(bundle.get("status") == "READY_FOR_FREEZE", "prediction bundle not ready", "PREDICTION_BUNDLE_NOT_READY")
    _require(bundle.get("case_id") == case_receipt.get("case_id"), "prediction case mismatch", "PREDICTION_BUNDLE_IDENTITY_MISMATCH")
    _require(bundle.get("run_id") == case_receipt.get("run_id"), "prediction run mismatch", "PREDICTION_BUNDLE_IDENTITY_MISMATCH")
    _require(bundle.get("answer_visible_during_prediction") is False, "answer visible during prediction", "ANSWER_VISIBILITY_CONTAMINATION")
    _require(bundle.get("prediction_input_answer_free") is True, "answer-free input not proven", "ANSWER_ISOLATION_FAILED")
    access = read_json(case_receipt["receipt_path"])
    option_path = _path_from_rows(access.get("released_paths", []), "/withheld-options/", "OPTION_PAYLOAD_PATH_INVALID")
    option_payload = read_json(option_path)
    options = _question_options(option_payload)
    rows = bundle.get("questions", [])
    _require([str(v.get("question_id")) for v in rows] == list(options), "prediction question order/set mismatch", "PREDICTION_QUESTION_SET_MISMATCH")
    for row in rows:
        qid = str(row["question_id"])
        option_ids = options[qid]
        _require(row.get("top1") in option_ids and row.get("top2") in option_ids and row.get("top1") != row.get("top2"), "top choices invalid", "TOP_SELECTION_INVALID")
        _require(bool(row.get("confidence")) and bool(row.get("blind_core")), "public prediction payload incomplete", "PUBLIC_PREDICTION_INCOMPLETE")
        _require(row.get("source_provenance_status") == "PASS", "source provenance not PASS", "SOURCE_PROVENANCE_NOT_PASS")
        _require(row.get("pairwise_replay_status") == "PASS", "pairwise replay not PASS", "PAIRWISE_REPLAY_NOT_PASS")
        _require(row.get("coverage_plan_status") == "PASS", "coverage plan not PASS", "COVERAGE_PLAN_NOT_PASS")
        _require(row.get("ziwei_track", {}).get("status") == "PASS", "Ziwei track not PASS", "ZIWEI_TRACK_INVALID")
        _require(row.get("bazi_track", {}).get("status") == "PASS", "Bazi track not PASS", "BAZI_TRACK_INVALID")
        _require(row.get("fusion_status") in {"S03_PERFORMED", "S03_NOT_PERFORMED_VALID_REASON"}, "fusion state invalid", "FUSION_STATUS_INVALID")
        _require(isinstance(row.get("evidence_usage_ledger"), list) and bool(row["evidence_usage_ledger"]), "evidence ledger missing", "EVIDENCE_LEDGER_MISSING")
        _validate_pairwise(row, option_ids)
    return rows, options


def freeze_group_predictions(request_path: str | Path) -> dict[str, Any]:
    request = read_json(request_path)
    _require(request.get("schema") == "GROUP-PREDICTION-FREEZE-REQUEST-V1", "freeze request schema invalid", "GROUP_FREEZE_REQUEST_INVALID")
    _require(request.get("status") == "REQUESTED", "freeze request status invalid", "GROUP_FREEZE_REQUEST_INVALID")
    access_path = Path(request["group_postblind_access_path"])
    access = read_json(access_path)
    _require(access.get("status") == POSTBLIND_STATUS, "postblind access not released", "POSTBLIND_ACCESS_NOT_RELEASED")
    _require(access.get("group_run_id") == request.get("group_run_id"), "group run mismatch", "GROUP_FREEZE_IDENTITY_MISMATCH")
    case_receipts = {row["case_id"]: row for row in access.get("cases", [])}
    prediction_rows = request.get("case_prediction_bundles", [])
    _require({v.get("case_id") for v in prediction_rows} == set(case_receipts), "prediction case set mismatch", "PREDICTION_CASE_SET_MISMATCH")
    output_root = Path(request.get("output_root") or access_path.parent)
    freezes = []
    total_questions = 0
    for row in prediction_rows:
        case_id = row["case_id"]
        bundle_path = Path(row["prediction_bundle_path"])
        _require(bundle_path.is_file(), f"prediction bundle missing: {bundle_path}", "PREDICTION_BUNDLE_MISSING")
        bundle = read_json(bundle_path)
        question_rows, _ = _validate_prediction_bundle(bundle, case_receipts[case_id])
        freeze_path = output_root / "prediction-freezes" / f"{case_id}.json"
        freeze = _write_new(freeze_path, {
            "schema": "CASE-PREDICTION-FREEZE-V1",
            "status": "CASE_PREDICTION_FREEZE_PASS",
            "group_run_id": access["group_run_id"],
            "case_id": case_id,
            "run_id": case_receipts[case_id]["run_id"],
            "prediction_bundle_path": str(bundle_path),
            "prediction_bundle_sha256": sha256_file(bundle_path),
            "question_count": len(question_rows),
            "questions": question_rows,
            "answer_data_available": False,
            "frozen_before_reveal": True,
            "frozen_at": utc_now(),
        })
        freezes.append({"case_id": case_id, "run_id": case_receipts[case_id]["run_id"], "freeze_path": str(freeze_path), "freeze_sha256": sha256_file(freeze_path), "freeze_object_hash": freeze["object_hash"], "question_count": len(question_rows)})
        total_questions += len(question_rows)
    group_path = output_root / "group-prediction-freeze.json"
    result = _write_new(group_path, {
        "schema": "GROUP-PREDICTION-FREEZE-V1",
        "status": GROUP_FREEZE_STATUS,
        "group_id": access["group_id"],
        "group_run_id": access["group_run_id"],
        "group_postblind_access_path": str(access_path),
        "group_postblind_access_sha256": sha256_file(access_path),
        "case_count": len(freezes),
        "question_count": total_questions,
        "cases": freezes,
        "answer_data_available": False,
        "all_predictions_frozen_before_reveal": True,
        "frozen_at": utc_now(),
    })
    return {**result, "output_path": str(group_path)}


def _literal_answer_rows(answer: dict[str, Any], expected_keys: list[str]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    _require(answer.get("schema") == "GROUP-ANSWER-VECTOR-V1", "answer vector schema invalid", "ANSWER_VECTOR_SCHEMA_INVALID")
    _require(answer.get("status") == "REVEALED_FOR_TRAINING_AFTER_FREEZE", "answer vector status invalid", "ANSWER_VECTOR_STATUS_INVALID")
    raw = answer.get("raw_answer_string")
    delimiter = answer.get("delimiter", ",")
    _require(isinstance(raw, str) and bool(raw), "raw answer string missing", "ANSWER_VECTOR_LITERAL_MISSING")
    parsed_a = [v.strip() for v in raw.split(delimiter) if v.strip()]
    parsed_b = re.findall(r"[0-9A-Za-z]+", raw)
    rows = answer.get("rows", [])
    row_values = [str(v.get("answer_option_id")) for v in rows]
    row_keys = [f"{v.get('case_id')}::{v.get('question_id')}" for v in rows]
    _require(parsed_a == parsed_b == row_values, "independent answer parsing mismatch", "ANSWER_VECTOR_LITERAL_REPLAY_MISMATCH")
    _require(row_keys == expected_keys, "answer row order/set mismatch", "ANSWER_VECTOR_QUESTION_SET_MISMATCH")
    codepoints = [ord(ch) for ch in raw]
    offsets = [{"index": index, "character": ch, "codepoint": ord(ch)} for index, ch in enumerate(raw)]
    if "unicode_codepoints" in answer:
        _require(answer["unicode_codepoints"] == codepoints, "answer codepoint mismatch", "ANSWER_VECTOR_CODEPOINT_MISMATCH")
    if "character_offsets" in answer:
        _require(answer["character_offsets"] == offsets, "answer offset mismatch", "ANSWER_VECTOR_OFFSET_MISMATCH")
    return rows, {"raw_answer_string": raw, "delimiter": delimiter, "unicode_codepoints": codepoints, "character_offsets": offsets, "parser_a": parsed_a, "parser_b": parsed_b}


def reveal_and_start_training(request_path: str | Path, *, answer_root: str | Path | None = None) -> dict[str, Any]:
    request = read_json(request_path)
    _require(request.get("schema") == "GROUP-REVEAL-TRAINING-REQUEST-V1", "reveal request schema invalid", "REVEAL_REQUEST_INVALID")
    _require(request.get("status") == "REQUESTED", "reveal request status invalid", "REVEAL_REQUEST_INVALID")
    freeze_path = Path(request["group_prediction_freeze_path"])
    freeze = read_json(freeze_path)
    _require(freeze.get("status") == GROUP_FREEZE_STATUS, "group freeze not PASS", "GROUP_FREEZE_NOT_PASS")
    _require(freeze.get("all_predictions_frozen_before_reveal") is True, "freeze order invalid", "GROUP_FREEZE_ORDER_INVALID")
    _require(freeze.get("group_run_id") == request.get("group_run_id"), "group run mismatch", "REVEAL_REQUEST_IDENTITY_MISMATCH")
    answer_path = Path(request["answer_vector_path"])
    if answer_root is not None:
        root = Path(answer_root).resolve()
        answer_path = (root / answer_path).resolve()
        _require(root == answer_path or root in answer_path.parents, "answer path escapes answer root", "ANSWER_VECTOR_PATH_INVALID")
    _require(answer_path.is_file(), f"answer vector missing: {answer_path}", "ANSWER_VECTOR_MISSING")
    frozen_questions: list[dict[str, Any]] = []
    expected_keys: list[str] = []
    for case_row in freeze["cases"]:
        case_freeze = read_json(case_row["freeze_path"])
        _require(case_freeze.get("status") == "CASE_PREDICTION_FREEZE_PASS", "case freeze invalid", "CASE_FREEZE_NOT_PASS")
        for q in case_freeze["questions"]:
            key = f"{case_row['case_id']}::{q['question_id']}"
            expected_keys.append(key)
            frozen_questions.append({"key": key, "case_id": case_row["case_id"], "question_id": q["question_id"], "top1": q["top1"], "top2": q["top2"], "case_freeze_path": case_row["freeze_path"], "case_freeze_hash": case_row["freeze_object_hash"], "source_provenance_status": q["source_provenance_status"], "pairwise_replay_status": q["pairwise_replay_status"]})
    answer = read_json(answer_path)
    answer_rows, literal = _literal_answer_rows(answer, expected_keys)
    answer_map = {f"{v['case_id']}::{v['question_id']}": str(v["answer_option_id"]) for v in answer_rows}
    replay_rows = []
    top1_hits = 0
    top2_hits = 0
    for q in frozen_questions:
        revealed = answer_map[q["key"]]
        top1_correct = q["top1"] == revealed
        top2_hit = revealed in {q["top1"], q["top2"]}
        top1_hits += int(top1_correct)
        top2_hits += int(top2_hit)
        replay_rows.append({
            "distinct_question_key": q["key"],
            "case_id": q["case_id"],
            "question_id": q["question_id"],
            "revealed_option_id": revealed,
            "frozen_top1": q["top1"],
            "frozen_top2": q["top2"],
            "top1_correct": top1_correct,
            "top2_hit": top2_hit,
            "prediction_freeze_hash": q["case_freeze_hash"],
            "evaluation_role": "FIRST_BLIND_PREDICTION",
            "answer_visible_during_prediction": False,
            "prediction_input_answer_free": True,
            "frozen_before_reveal": True,
            "case_specific_rule_detected": False,
            "source_provenance_status": q["source_provenance_status"],
            "pairwise_replay_status": q["pairwise_replay_status"],
        })
    output_root = Path(request.get("output_root") or freeze_path.parent / "training")
    replay_path = output_root / "answer-vector-literal-replay.json"
    replay = _write_new(replay_path, {
        "schema": "ANSWER-VECTOR-LITERAL-REPLAY-V1",
        "status": "PASS",
        "group_id": freeze["group_id"],
        "group_run_id": freeze["group_run_id"],
        "group_prediction_freeze_path": str(freeze_path),
        "group_prediction_freeze_sha256": sha256_file(freeze_path),
        "answer_vector_path": str(answer_path),
        "answer_vector_sha256": sha256_file(answer_path),
        "literal_replay": literal,
        "question_count": len(replay_rows),
        "top1_hits": top1_hits,
        "top1_rate": top1_hits / len(replay_rows),
        "top2_hits": top2_hits,
        "top2_rate": top2_hits / len(replay_rows),
        "rows": replay_rows,
        "replayed_at": utc_now(),
    })
    units = [{"unit_id": slug(q["key"]), "case_ids": [q["case_id"]], "question_ids": [q["question_id"]]} for q in frozen_questions]
    unit_plan_path = output_root / "learning-unit-plan.json"
    unit_plan = _write_new(unit_plan_path, {"schema": "LEARNING-UNIT-PLAN-V1", "group_id": freeze["group_id"], "group_run_id": freeze["group_run_id"], "units": units})
    cycle_path = output_root / "learning-cycle.json"
    cycle = create_cycle(
        request.get("cycle_id") or f"CYCLE-{freeze['group_run_id']}",
        freeze["group_id"],
        units,
        cycle_path,
        thresholds=request.get("thresholds") or default_thresholds(),
        bindings={
            "group_run_id": freeze["group_run_id"],
            "group_prediction_freeze_hash": freeze.get("object_hash"),
            "answer_vector_literal_replay_hash": replay["object_hash"],
            "main_prompt_runtime_id": request.get("main_prompt_runtime_id"),
            "knowledge_release_id": request.get("knowledge_release_id"),
            "method_release_id": request.get("method_release_id"),
            "model_release_id": request.get("model_release_id"),
        },
    )
    seed_dir = output_root / "training-evidence-seeds"
    seed_rows = []
    for row in replay_rows:
        unit_id = slug(row["distinct_question_key"])
        seed_path = seed_dir / f"{unit_id}.json"
        seed = _write_new(seed_path, {
            "schema": "QUESTION-TRAINING-EVIDENCE-SEED-V1",
            "status": "AWAITING_REASONING_CORRECTION_AND_STABILITY_REPLAYS",
            "cycle_id": cycle["cycle_id"],
            "unit_id": unit_id,
            "first_blind_prediction": row,
            "correction_required": True,
            "minimum_post_reveal_stability_replays": cycle["thresholds"]["min_post_reveal_stability_replays"],
            "answer_memorization_forbidden": True,
            "created_at": utc_now(),
        })
        seed_rows.append({"unit_id": unit_id, "path": str(seed_path), "object_hash": seed["object_hash"]})
    intake_path = output_root / "group-training-intake.json"
    intake = _write_new(intake_path, {
        "schema": "GROUP-TRAINING-INTAKE-V1",
        "status": "LEARNING_ACTIVE",
        "group_id": freeze["group_id"],
        "group_run_id": freeze["group_run_id"],
        "cycle_path": str(cycle_path),
        "cycle_object_hash": cycle["object_hash"],
        "unit_plan_path": str(unit_plan_path),
        "unit_plan_object_hash": unit_plan["object_hash"],
        "literal_replay_path": str(replay_path),
        "literal_replay_object_hash": replay["object_hash"],
        "training_unit_count": len(seed_rows),
        "training_evidence_seeds": seed_rows,
        "first_active_unit": seed_rows[0]["unit_id"],
        "created_at": utc_now(),
    })
    return {**intake, "output_path": str(intake_path)}


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="fortune-group-pipeline")
    sub = p.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate-clean-start")
    validate.add_argument("--clean-start", required=True)
    validate.add_argument("--output")
    release = sub.add_parser("release-postblind")
    release.add_argument("--request", required=True)
    freeze = sub.add_parser("freeze-group")
    freeze.add_argument("--request", required=True)
    reveal = sub.add_parser("reveal-and-start-training")
    reveal.add_argument("--request", required=True)
    reveal.add_argument("--answer-root")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "validate-clean-start":
            result = validate_staged_clean_start(args.clean_start)
            if args.output:
                atomic_write_json(args.output, result)
        elif args.command == "release-postblind":
            result = release_group_postblind(args.request)
        elif args.command == "freeze-group":
            result = freeze_group_predictions(args.request)
        else:
            result = reveal_and_start_training(args.request, answer_root=args.answer_root)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (FortuneError, RuntimeError) as exc:
        status = getattr(exc, "status", "PIPELINE_RUNTIME_ERROR")
        print(json.dumps({"status": status, "error": str(exc)}, ensure_ascii=False), file=__import__("sys").stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
