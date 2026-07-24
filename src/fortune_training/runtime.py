from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet, InvalidToken

from .chat_input import write_chat_input
from .learning import (
    load_learning_ledger,
    load_rule_catalog,
    record_first_blind_results,
    register_rules,
    validate_learning_patch_v3,
    validate_question_profile,
    validate_rule_attribution,
    write_learning_ledger,
)
from .policy import (
    MINIMUM_NEW_CASES_BETWEEN_REPLAYS,
    REQUIRED_CONSECUTIVE_INDEPENDENT_PASSES,
    passed,
    required_correct,
)
from .reasoning import (
    FROZEN_SCHEMA,
    PREDICTION_SCHEMA,
    build_completeness_report,
    frozen_content_hash,
    validate_prediction_reasoning,
    validate_question_reasoning,
    validate_replay_remediation,
)
from .util import (
    TrainingError,
    atomic_write_json,
    canonical_bytes,
    exclusive_write_json,
    load_json,
    next_round_id,
    object_sha256,
    require_outside,
    require_safe_id,
    sha256_file,
    utc_now,
)
from .verify import verify_repository


OPENABLE_STATES = {"READY_FOR_ROUND"}
CASE_VISIBLE_STATES = {
    "READY_FOR_ROUND",
    "AWAITING_PREDICTION_FREEZE",
    "PREDICTION_FROZEN",
    "LEARNING_REQUIRED",
}
PATCH_LEAK_PATTERNS = (
    re.compile(r"DEV-EXAMPLE-\d+", re.IGNORECASE),
    re.compile(r"\bQ\d+\b", re.IGNORECASE),
    re.compile(r"(?:正确答案|答案是|选择|应选|correct[_ ]?option).{0,12}\b[A-Z]\b", re.IGNORECASE),
)
PATCH_FORBIDDEN_KEYS = {
    "answer",
    "answers",
    "answer_key",
    "correct_answer",
    "correct_option",
    "option_id",
    "case_id",
    "question_id",
}


def _state_path(root: Path) -> Path:
    return root / "training" / "state.json"


def _load_state(root: Path) -> dict[str, Any]:
    return load_json(_state_path(root))


def _load_group(root: Path, state: dict[str, Any]) -> dict[str, Any]:
    return load_json(root / state["group_path"])


def _current_case_id(state: dict[str, Any], group: dict[str, Any]) -> str:
    replay_case_id = state.get("active_replay_case_id")
    if replay_case_id is not None:
        if replay_case_id not in group["cases"]:
            raise TrainingError("active replay case is not in the training group")
        return replay_case_id
    index = state.get("current_case_index")
    case_order = group["case_order"]
    if not isinstance(index, int) or index < 0 or index >= len(case_order):
        raise TrainingError("there is no active case")
    return case_order[index]


def _case_path(root: Path, group: dict[str, Any], case_id: str) -> Path:
    return root / group["cases"][case_id]


def _questions(case: dict[str, Any]) -> list[dict[str, Any]]:
    return case["questions"]["parsed"]


def _round_dir(root: Path, round_id: str) -> Path:
    require_safe_id(round_id, "round_id")
    return root / "training" / "runs" / round_id


def _schedule_next_round(root: Path, state: dict[str, Any]) -> None:
    group = _load_group(root, state)
    state["active_replay_case_id"] = None
    closed_count = state.get("first_blind_cases_closed", 0)
    queue = state.setdefault("spaced_replay_queue", [])
    eligible = next(
        (
            item
            for item in queue
            if item["eligible_after_first_blind_count"] <= closed_count
        ),
        None,
    )
    if eligible is not None:
        state["active_replay_case_id"] = eligible["case_id"]
        state["cases"][eligible["case_id"]]["status"] = "REPLAY_ACTIVE"
        state["status"] = "READY_FOR_ROUND"
        return
    if state["current_case_index"] < len(group["case_order"]):
        next_case_id = group["case_order"][state["current_case_index"]]
        state["cases"][next_case_id]["status"] = "ACTIVE"
        state["status"] = "READY_FOR_ROUND"
        return
    state["status"] = (
        "FIRST_BLIND_COMPLETE_REPLAY_PENDING" if queue else "GROUP_COMPLETE"
    )


def _close_first_blind_and_advance(root: Path, state: dict[str, Any], case_id: str) -> None:
    group = _load_group(root, state)
    expected_case_id = group["case_order"][state["current_case_index"]]
    if case_id != expected_case_id:
        raise TrainingError("first-blind case does not match the new-case cursor")
    state["cases"][case_id]["status"] = "FIRST_BLIND_CLOSED"
    state["current_case_index"] += 1
    state["first_blind_cases_closed"] = state.get("first_blind_cases_closed", 0) + 1
    _schedule_next_round(root, state)


def _enqueue_spaced_replay(
    state: dict[str, Any],
    case_id: str,
    *,
    after_current_first_blind: bool = False,
) -> None:
    queue = state.setdefault("spaced_replay_queue", [])
    queue[:] = [item for item in queue if item["case_id"] != case_id]
    queue.append(
        {
            "case_id": case_id,
            "eligible_after_first_blind_count": (
                state.get("first_blind_cases_closed", 0)
                + int(after_current_first_blind)
                + MINIMUM_NEW_CASES_BETWEEN_REPLAYS
            ),
        }
    )
    state["cases"][case_id]["remediation_status"] = "QUEUED"


def _finish_replay(root: Path, state: dict[str, Any], case_id: str, did_pass: bool) -> None:
    queue = state.setdefault("spaced_replay_queue", [])
    if did_pass:
        queue[:] = [item for item in queue if item["case_id"] != case_id]
        state["cases"][case_id]["remediation_status"] = "RESOLVED"
    else:
        _enqueue_spaced_replay(state, case_id)
    state["cases"][case_id]["status"] = "FIRST_BLIND_CLOSED"
    state["active_replay_case_id"] = None
    _schedule_next_round(root, state)


def _round_evaluation_kind(state: dict[str, Any], case_id: str) -> str:
    return "SPACED_REPLAY" if state.get("active_replay_case_id") == case_id else "FIRST_BLIND"


def status(root: Path) -> dict[str, Any]:
    state = _load_state(root)
    group = _load_group(root, state)
    current_case = None
    if state["status"] in CASE_VISIBLE_STATES:
        current_case = _current_case_id(state, group)
    current_case_state = state["cases"].get(current_case, {}) if current_case else {}
    ledger = load_learning_ledger(root)
    return {
        "group_id": state["group_id"],
        "status": state["status"],
        "current_case_id": current_case,
        "canonical_source_manifest": state["source_manifest_path"],
        "current_model_release": state["current_model_release"],
        "active_round_id": state["active_round_id"],
        "round_count": state["round_count"],
        "round_limit": None,
        "training_unit": "FIRST_BLIND_CASE_WITH_SPACED_REPLAY",
        "independent_pass_streak": state.get("independent_pass_streak", 0),
        "required_consecutive_independent_passes": REQUIRED_CONSECUTIVE_INDEPENDENT_PASSES,
        "current_case_first_blind_round_id": current_case_state.get("first_blind_round_id"),
        "first_blind_cases_scored": ledger["first_blind_totals"]["cases"],
        "first_blind_questions_scored": ledger["first_blind_totals"]["questions"],
        "first_blind_cases_closed": state.get("first_blind_cases_closed", 0),
        "active_replay_case_id": state.get("active_replay_case_id"),
        "spaced_replay_queue_size": len(state.get("spaced_replay_queue", [])),
        "same_case_replays_count_toward_stage_gate": False,
        "dataset_manifest_path": state.get("dataset_manifest_path"),
        "dataset_runtime_status": state.get("dataset_runtime_status"),
        "mode": state.get("mode", "LEGACY_MIGRATION"),
        "formal_phase": state.get("formal_phase"),
        "recommended_round_id": (
            next_round_id(state)
            if state["status"] in OPENABLE_STATES and state.get("active_round_id") is None
            else None
        ),
    }


def start_round(root: Path, round_id: str) -> dict[str, Any]:
    root = root.resolve()
    verify_repository(root)
    state = _load_state(root)
    if state["status"] not in OPENABLE_STATES:
        raise TrainingError(f"cannot start a round while state is {state['status']}")
    if state.get("active_round_id") is not None:
        raise TrainingError("another round is already active")
    if state.get("round_id_prefix") is not None and round_id != next_round_id(state):
        raise TrainingError(f"formal round id must be {next_round_id(state)}")
    group = _load_group(root, state)
    case_id = _current_case_id(state, group)
    case_state = state["cases"][case_id]
    case_path = _case_path(root, group, case_id)
    case = load_json(case_path)
    question_count = len(_questions(case))
    source_manifest_path = root / state["source_manifest_path"]
    source_manifest = load_json(source_manifest_path)
    release_path = root / "model-learning" / "releases" / f"{state['current_model_release']}.json"
    release = load_json(release_path)
    round_path = _round_dir(root, round_id)
    if round_path.exists():
        raise TrainingError(f"round already exists: {round_id}")
    evaluation_kind = _round_evaluation_kind(state, case_id)
    round_record = {
        "schema": "GENERALIZATION-BLIND-ROUND-R2",
        "round_id": round_id,
        "case_id": case_id,
        "evaluation_kind": evaluation_kind,
        "counts_toward_stage_gate": evaluation_kind == "FIRST_BLIND",
        "case_path": case_path.relative_to(root).as_posix(),
        "case_sha256": sha256_file(case_path),
        "question_count": question_count,
        "required_correct": required_correct(question_count),
        "canonical_source_manifest": state["source_manifest_path"],
        "canonical_source_manifest_sha256": object_sha256(source_manifest),
        "model_release": state["current_model_release"],
        "model_release_sha256": object_sha256(release),
        "effective_training_input": "GIT_CANONICAL_S00_S19_PLUS_MODEL_RELEASE",
        "status": "PREDICTION_OPEN",
        "answer_visibility": "PHYSICALLY_UNAVAILABLE_TO_PREDICTION_CONTEXT",
        "question_profile_required": True,
        "prediction_workbook_schema": PREDICTION_SCHEMA,
        "blind_chart_model_required_before_option_comparison": True,
        "dual_track_seal_required": True,
        "reasoning_completeness_gate_required": True,
        "started_at": utc_now(),
    }
    exclusive_write_json(round_path / "round.json", round_record)
    state["active_round_id"] = round_id
    state["status"] = "AWAITING_PREDICTION_FREEZE"
    state["round_count"] += 1
    if evaluation_kind == "FIRST_BLIND":
        case_state["first_blind_round_id"] = round_id
    else:
        case_state.setdefault("replay_round_ids", []).append(round_id)
    case_state["round_ids"].append(round_id)
    atomic_write_json(_state_path(root), state)
    write_chat_input(root)
    return round_record


def _validate_prediction(
    root: Path,
    case: dict[str, Any],
    round_record: dict[str, Any],
    payload: Any,
) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise TrainingError("prediction payload must be an object")
    expected_top_level = {
        "schema",
        "case_id",
        "round_id",
        "blind_chart_model",
        "cross_question_consistency",
        "replay_remediation",
        "predictions",
    }
    if set(payload) != expected_top_level or payload.get("schema") != PREDICTION_SCHEMA:
        raise TrainingError(
            f"prediction payload must use {PREDICTION_SCHEMA} and its exact top-level fields"
        )
    if payload.get("case_id") != round_record["case_id"] or payload.get("round_id") != round_record["round_id"]:
        raise TrainingError("prediction case_id or round_id mismatch")
    if any("answer" in str(key).lower() for key in payload):
        raise TrainingError("prediction payload may not contain answer fields")
    predictions = payload.get("predictions")
    if not isinstance(predictions, list):
        raise TrainingError("predictions must be an array")
    question_map = {question["question_id"]: question for question in _questions(case)}
    if len(predictions) != len(question_map):
        raise TrainingError("prediction must cover every question exactly once")
    blind_chart_model, cross_question_consistency = validate_prediction_reasoning(
        case=case,
        payload=payload,
        predictions=predictions,
    )
    replay_remediation = validate_replay_remediation(
        payload.get("replay_remediation"),
        required=round_record["evaluation_kind"] == "SPACED_REPLAY",
    )
    normalized: list[dict[str, Any]] = []
    rule_catalog = load_rule_catalog(root)
    known_rule_ids = set(rule_catalog)
    learning_ledger = load_learning_ledger(root)
    seen: set[str] = set()
    for row in predictions:
        if not isinstance(row, dict):
            raise TrainingError("every prediction row must be an object")
        expected_row_fields = {
            "question_id",
            "top1",
            "top2",
            "public_summary",
            "question_profile",
            "rule_attribution",
            "question_semantic_model",
            "ziwei_track_seal",
            "bazi_track_seal",
            "cross_track_arbitration",
            "evidence_ledger",
            "final_ranking",
            "option_comparison_matrix",
            "adversarial_review",
            "confidence_components",
            "counterfactual_analysis",
        }
        if set(row) != expected_row_fields:
            raise TrainingError(
                f"every prediction row must contain the complete {PREDICTION_SCHEMA} structure"
            )
        if any("answer" in str(key).lower() for key in row):
            raise TrainingError("prediction rows may not contain answer fields")
        question_id = row.get("question_id")
        if question_id not in question_map or question_id in seen:
            raise TrainingError(f"invalid or duplicate prediction question: {question_id!r}")
        seen.add(question_id)
        valid_options = {option["option_id"] for option in question_map[question_id]["options"]}
        top1 = row.get("top1")
        top2 = row.get("top2")
        if top1 not in valid_options:
            raise TrainingError(f"invalid top1 for {question_id}: {top1!r}")
        if top2 not in valid_options or top2 == top1:
            raise TrainingError(f"invalid top2 for {question_id}: {top2!r}")
        profile = validate_question_profile(
            root,
            row.get("question_profile"),
            known_rule_ids=known_rule_ids,
        )
        rule_attribution = validate_rule_attribution(
            root,
            row.get("rule_attribution"),
            profile=profile,
            catalog=rule_catalog,
            ledger=learning_ledger,
        )
        public_summary = row.get("public_summary")
        if not isinstance(public_summary, str) or not public_summary.strip():
            raise TrainingError(f"{question_id} needs a non-empty public_summary")
        structured = validate_question_reasoning(
            row=row,
            option_ids=[option["option_id"] for option in question_map[question_id]["options"]],
            source_routes=profile["source_routes"],
            top1=top1,
            top2=top2,
            decisive_rule_ids=rule_attribution["decisive_rule_ids"],
        )
        normalized.append(
            {
                "question_id": question_id,
                "top1": top1,
                "top2": top2,
                "public_summary": public_summary.strip(),
                "question_profile": profile,
                "rule_attribution": rule_attribution,
                **structured,
            }
        )
    normalized.sort(key=lambda item: list(question_map).index(item["question_id"]))
    return {
        "schema": FROZEN_SCHEMA,
        "case_id": round_record["case_id"],
        "round_id": round_record["round_id"],
        "blind_chart_model": blind_chart_model,
        "cross_question_consistency": cross_question_consistency,
        "replay_remediation": replay_remediation,
        "predictions": normalized,
        "reasoning_completeness_report": build_completeness_report(
            blind_chart_model,
            normalized,
            cross_question_consistency,
        ),
        "frozen_at": utc_now(),
    }


def freeze_prediction(root: Path, round_id: str, prediction_path: Path) -> dict[str, Any]:
    root = root.resolve()
    state = _load_state(root)
    if state.get("active_round_id") != round_id or state.get("status") != "AWAITING_PREDICTION_FREEZE":
        raise TrainingError("this round is not awaiting prediction freeze")
    round_path = _round_dir(root, round_id)
    round_record = load_json(round_path / "round.json")
    if round_record.get("status") != "PREDICTION_OPEN":
        raise TrainingError("round prediction is not open")
    case = load_json(root / round_record["case_path"])
    frozen = _validate_prediction(root, case, round_record, load_json(prediction_path))
    frozen["prediction_sha256"] = frozen_content_hash(frozen)
    exclusive_write_json(round_path / "prediction-freeze.json", frozen)
    round_record["status"] = "PREDICTION_FROZEN"
    round_record["prediction_sha256"] = frozen["prediction_sha256"]
    round_record["frozen_at"] = frozen["frozen_at"]
    atomic_write_json(round_path / "round.json", round_record)
    state["status"] = "PREDICTION_FROZEN"
    atomic_write_json(_state_path(root), state)
    write_chat_input(root)
    return frozen


def _fernet_from_key(key: str | bytes | None) -> Fernet:
    if key is None:
        key = os.environ.get("FORTUNE_ANSWER_KEY")
    if not key:
        raise TrainingError("FORTUNE_ANSWER_KEY is required")
    if isinstance(key, str):
        key = key.encode("ascii")
    try:
        return Fernet(key)
    except (ValueError, TypeError) as exc:
        raise TrainingError("FORTUNE_ANSWER_KEY is invalid") from exc


def generate_key() -> str:
    return Fernet.generate_key().decode("ascii")


def _validate_answers(
    case: dict[str, Any],
    payload: Any,
) -> dict[str, dict[str, str | None]]:
    if not isinstance(payload, dict) or payload.get("case_id") != case.get("case_id"):
        raise TrainingError("answer case_id mismatch")
    rows = payload.get("answers")
    if not isinstance(rows, list):
        raise TrainingError("answers must be an array")
    questions = {question["question_id"]: question for question in _questions(case)}
    answer_map: dict[str, dict[str, str | None]] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise TrainingError("every answer row must be an object")
        question_id = row.get("question_id")
        if question_id not in questions or question_id in answer_map:
            raise TrainingError(f"invalid or duplicate answer question: {question_id!r}")
        if set(row) == {"question_id", "correct_option"}:
            correct = row.get("correct_option")
            valid_options = {
                option["option_id"] for option in questions[question_id]["options"]
            }
            if correct not in valid_options:
                raise TrainingError(f"invalid correct option for {question_id}")
            answer_map[question_id] = {
                "scoring_status": "SCORED",
                "correct_option": correct,
            }
        elif set(row) == {"question_id", "scoring_status", "reason_code"}:
            if (
                row.get("scoring_status") != "UNSCORED"
                or row.get("reason_code") != "NO_VALID_OPTION"
            ):
                raise TrainingError(f"invalid unscored declaration for {question_id}")
            answer_map[question_id] = {
                "scoring_status": "UNSCORED",
                "correct_option": None,
                "reason_code": "NO_VALID_OPTION",
            }
        else:
            raise TrainingError(f"answer row has unexpected fields for {question_id}")
    if set(answer_map) != set(questions):
        raise TrainingError("answer payload must cover every question exactly once")
    return answer_map


def encrypt_answer(root: Path, case_id: str, plaintext_path: Path, key: str | bytes | None = None) -> Path:
    root = root.resolve()
    require_safe_id(case_id, "case_id")
    require_outside(root, plaintext_path, "plaintext answer input")
    case_bank_path = root / "case-bank" / "cases" / f"{case_id}.json"
    if case_bank_path.is_file():
        raise TrainingError("formal case answers must use the atomic import-answer-batch command")
    else:
        group = load_json(root / "examples" / "DEV-GROUP-002" / "group.json")
        if case_id not in group["cases"]:
            raise TrainingError(f"unknown case: {case_id}")
        case = load_json(root / group["cases"][case_id])
    payload = load_json(plaintext_path)
    _validate_answers(case, payload)
    token = _fernet_from_key(key).encrypt(canonical_bytes(payload))
    destination = root / "answer-vault" / "encrypted" / f"{case_id}.json.fernet"
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with destination.open("xb") as handle:
            handle.write(token + b"\n")
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise TrainingError(f"encrypted answer already exists: {destination}") from exc
    return destination


def _decrypt_answers(
    root: Path,
    case: dict[str, Any],
    key: str | bytes | None,
) -> dict[str, dict[str, str | None]]:
    case_id = case["case_id"]
    if (root / "case-bank" / "cases" / f"{case_id}.json").is_file():
        envelope = root / "answer-vault" / "formal" / f"{case_id}.json.fernet"
    else:
        envelope = root / "answer-vault" / "encrypted" / f"{case_id}.json.fernet"
    try:
        token = envelope.read_bytes().strip()
    except FileNotFoundError as exc:
        raise TrainingError(f"missing encrypted answer for {case['case_id']}") from exc
    try:
        plaintext = _fernet_from_key(key).decrypt(token)
    except InvalidToken as exc:
        raise TrainingError("answer envelope cannot be decrypted with this key") from exc
    try:
        import json

        payload = json.loads(plaintext.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise TrainingError("decrypted answer payload is invalid") from exc
    return _validate_answers(case, payload)


def score_round(
    root: Path,
    round_id: str,
    review_output: Path,
    key: str | bytes | None = None,
    answer_file: Path | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    require_outside(root, review_output, "detailed review output")
    if review_output.exists():
        raise TrainingError(f"detailed review output already exists: {review_output}")
    state = _load_state(root)
    if state.get("active_round_id") != round_id or state.get("status") != "PREDICTION_FROZEN":
        raise TrainingError("this round is not frozen and ready for scoring")
    round_path = _round_dir(root, round_id)
    if (round_path / "score.json").exists():
        raise TrainingError("round score is immutable and already exists")
    round_record = load_json(round_path / "round.json")
    frozen = load_json(round_path / "prediction-freeze.json")
    if round_record.get("prediction_sha256") != frozen_content_hash(frozen):
        raise TrainingError("frozen prediction hash mismatch")
    case = load_json(root / round_record["case_path"])
    if answer_file is not None:
        require_outside(root, answer_file, "plaintext answer input")
        answers = _validate_answers(case, load_json(answer_file))
        answer_source = "EXTERNAL_POST_FREEZE_FILE"
    else:
        answers = _decrypt_answers(root, case, key)
        answer_source = "ENCRYPTED_REPOSITORY_ENVELOPE"
    prediction_map = {row["question_id"]: row["top1"] for row in frozen["predictions"]}
    review_rows = []
    correct_count = 0
    scoreable_question_count = 0
    for question in _questions(case):
        question_id = question["question_id"]
        predicted = prediction_map[question_id]
        answer = answers[question_id]
        if answer["scoring_status"] == "UNSCORED":
            review_rows.append(
                {
                    "question_id": question_id,
                    "predicted_option": predicted,
                    "is_scored": False,
                    "is_correct": None,
                    "unscored_reason_code": answer["reason_code"],
                }
            )
            continue
        correct = answer["correct_option"]
        is_correct = predicted == correct
        scoreable_question_count += 1
        correct_count += int(is_correct)
        review_rows.append(
            {
                "question_id": question_id,
                "predicted_option": predicted,
                "correct_option": correct,
                "is_scored": True,
                "is_correct": is_correct,
            }
        )
    if scoreable_question_count < 1:
        raise TrainingError("a round must contain at least one scoreable question")
    total_question_count = len(review_rows)
    did_pass = passed(correct_count, scoreable_question_count)
    case_state = state["cases"][round_record["case_id"]]
    top2_covered = sum(
        1
        for prediction, review in zip(frozen["predictions"], review_rows)
        if review["is_scored"]
        and (
            review["is_correct"]
            or prediction.get("top2") == review["correct_option"]
        )
    )
    aggregate = {
        "schema": "GENERALIZATION-ROUND-SCORE-R3",
        "round_id": round_id,
        "case_id": round_record["case_id"],
        "evaluation_kind": round_record["evaluation_kind"],
        "correct_count": correct_count,
        "top2_covered_count": top2_covered,
        "question_count": total_question_count,
        "scoreable_question_count": scoreable_question_count,
        "unscored_question_count": total_question_count - scoreable_question_count,
        "required_correct": required_correct(scoreable_question_count),
        "accuracy": correct_count / scoreable_question_count,
        "top2_coverage": top2_covered / scoreable_question_count,
        "passed": did_pass,
        "advances_after_learning_if_failed": round_record["evaluation_kind"] == "FIRST_BLIND",
        "independent_pass_streak_before": state.get("independent_pass_streak", 0),
        "scored_at": utc_now(),
        "detailed_answers_stored_in_repository": False,
        "answer_source": answer_source,
    }
    if not did_pass:
        if round_record["evaluation_kind"] == "FIRST_BLIND":
            state["independent_pass_streak"] = 0
            case_state["first_blind_passed"] = False
        aggregate["independent_pass_streak_after"] = state.get("independent_pass_streak", 0)
        aggregate["spaced_replay_required"] = True
        state["status"] = "LEARNING_REQUIRED"
        case_state["status"] = "LEARNING_PENDING"
    else:
        if round_record["evaluation_kind"] == "FIRST_BLIND":
            state["independent_pass_streak"] = state.get("independent_pass_streak", 0) + 1
            case_state["first_blind_passed"] = True
            case_state["remediation_status"] = "NOT_REQUIRED"
            aggregate["spaced_replay_required"] = False
            _close_first_blind_and_advance(root, state, round_record["case_id"])
        else:
            aggregate["spaced_replay_required"] = False
            _finish_replay(root, state, round_record["case_id"], True)
        aggregate["independent_pass_streak_after"] = state.get("independent_pass_streak", 0)
    aggregate["independent_stage_gate_met"] = (
        state.get("independent_pass_streak", 0)
        >= REQUIRED_CONSECUTIVE_INDEPENDENT_PASSES
    )
    if round_record["evaluation_kind"] == "SPACED_REPLAY":
        first_round_id = case_state["first_blind_round_id"]
        first_dir = _round_dir(root, first_round_id)
        first_frozen = load_json(first_dir / "prediction-freeze.json")
        first_score = load_json(first_dir / "score.json")
        first_predictions = {
            row["question_id"]: row["top1"] for row in first_frozen["predictions"]
        }
        repaired = regressed = stable_correct = stable_incorrect = 0
        for review in review_rows:
            if not review["is_scored"]:
                continue
            original_correct = (
                first_predictions[review["question_id"]] == review["correct_option"]
            )
            current_correct = review["is_correct"]
            repaired += int(not original_correct and current_correct)
            regressed += int(original_correct and not current_correct)
            stable_correct += int(original_correct and current_correct)
            stable_incorrect += int(not original_correct and not current_correct)
        first_completeness = first_frozen.get("reasoning_completeness_report")
        current_completeness = frozen.get("reasoning_completeness_report")
        remediation_input = frozen["replay_remediation"]
        remediation_report = {
            "schema": "REPLAY-REMEDIATION-REPORT-V1",
            "round_id": round_id,
            "case_id": round_record["case_id"],
            "first_blind_round_id": first_round_id,
            "counts_as_first_blind_evidence": False,
            "counts_toward_stage_gate": False,
            "original_root_causes": remediation_input["original_root_causes"],
            "remediation_type": remediation_input["remediation_type"],
            "new_idea_executed": remediation_input["new_idea_executed"],
            "changed_steps": remediation_input["changed_steps"],
            "predicted_mechanism_of_improvement": remediation_input[
                "predicted_mechanism_of_improvement"
            ],
            "original_failed_answers_repaired": repaired,
            "original_correct_answers_regressed": regressed,
            "stable_correct_answers": stable_correct,
            "stable_incorrect_answers": stable_incorrect,
            "score_delta_from_first_blind": (
                aggregate["accuracy"] - first_score["accuracy"]
            ),
            "reasoning_completeness_comparison": {
                "first_blind_schema": first_frozen.get("schema"),
                "replay_schema": frozen.get("schema"),
                "first_blind_valid_evidence_entries": (
                    first_completeness.get("valid_evidence_entries")
                    if isinstance(first_completeness, dict)
                    else None
                ),
                "replay_valid_evidence_entries": current_completeness[
                    "valid_evidence_entries"
                ],
                "legacy_first_blind_detail_unavailable": first_completeness is None,
            },
            "new_error_risks": remediation_input["new_error_risks"],
            "mechanism_confirmation": (
                "SUPPORTED_BY_REPAIR_WITHOUT_NET_REGRESSION"
                if repaired > regressed
                else "NOT_YET_CONFIRMED"
            ),
            "answer_mapping_stored": False,
        }
        exclusive_write_json(round_path / "replay-remediation.json", remediation_report)
        aggregate["replay_remediation_report"] = (
            round_path / "replay-remediation.json"
        ).relative_to(root).as_posix()
    detailed_review = {
        "schema": "CASE-ROUND-DETAILED-REVIEW-V2",
        "round_id": round_id,
        "case_id": round_record["case_id"],
        "score": aggregate,
        "questions": review_rows,
    }
    exclusive_write_json(review_output, detailed_review)
    exclusive_write_json(round_path / "score.json", aggregate)
    round_record["status"] = "SCORED"
    round_record["score_sha256"] = object_sha256(aggregate)
    round_record["passed"] = did_pass
    round_record["scored_at"] = aggregate["scored_at"]
    atomic_write_json(round_path / "round.json", round_record)
    state["active_round_id"] = None

    if round_record["evaluation_kind"] == "FIRST_BLIND":
        ledger = load_learning_ledger(root)
        record_first_blind_results(
            ledger,
            case_id=round_record["case_id"],
            predictions=frozen["predictions"],
            review_rows=review_rows,
        )
        write_learning_ledger(root, ledger)

    atomic_write_json(_state_path(root), state)
    write_chat_input(root)
    return aggregate


def _walk_patch(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in PATCH_FORBIDDEN_KEYS:
                raise TrainingError(f"case-specific or answer-bearing patch key: {path}.{key}")
            _walk_patch(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk_patch(child, f"{path}[{index}]")


def _validate_learning_patch(root: Path, payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise TrainingError("learning patch must be an object")
    _walk_patch(payload)
    serialized = canonical_bytes(payload).decode("utf-8")
    for pattern in PATCH_LEAK_PATTERNS:
        if pattern.search(serialized):
            raise TrainingError("learning patch contains case-, question-, or answer-specific material")
    group = _load_group(root, _load_state(root))
    for case_path in group["cases"].values():
        case = load_json(root / case_path)
        for question in _questions(case):
            unique_texts = [question.get("stem", ""), *(row.get("text", "") for row in question["options"])]
            for text in unique_texts:
                normalized = " ".join(str(text).split())
                if len(normalized) >= 8 and normalized in serialized:
                    raise TrainingError("learning patch copies a case-specific question or option text")
    return validate_learning_patch_v3(root, payload)


def apply_learning(root: Path, round_id: str, patch_input: Path, release_id: str) -> dict[str, Any]:
    root = root.resolve()
    require_safe_id(release_id, "release_id")
    require_outside(root, patch_input, "learning patch input")
    state = _load_state(root)
    if state.get("status") != "LEARNING_REQUIRED":
        raise TrainingError("learning is only accepted after a failed round")
    group = _load_group(root, state)
    current_case_id = _current_case_id(state, group)
    if state["cases"][current_case_id].get("round_ids", [])[-1:] != [round_id]:
        raise TrainingError("learning must close the most recent failed round")
    round_path = _round_dir(root, round_id)
    round_record = load_json(round_path / "round.json")
    score = load_json(round_path / "score.json")
    if score.get("passed") is not False or round_record.get("passed") is not False:
        raise TrainingError("learning can only close a failed round")
    if round_record["case_id"] != current_case_id:
        raise TrainingError("learning round is not for the current case")
    patch_payload = _validate_learning_patch(root, load_json(patch_input))
    patch_record = {
        "schema": "MODEL-LEARNING-PATCH-V3",
        "release_id": release_id,
        "created_at": utc_now(),
        "content": patch_payload,
        "contains_case_answer_mapping": False,
        "modifies_canonical_source_files": False,
        "validation_status": (
            "CANDIDATE_RULES"
            if patch_payload["remediation_type"] == "NEW_GENERAL_RULE"
            else "ACTIVE_PROCESS_CORRECTION"
        ),
    }
    patch_path = root / "model-learning" / "patches" / f"{release_id}.json"
    release_path = root / "model-learning" / "releases" / f"{release_id}.json"
    if patch_path.exists() or release_path.exists():
        raise TrainingError(f"learning release already exists: {release_id}")
    exclusive_write_json(patch_path, patch_record)
    parent_id = state["current_model_release"]
    parent_path = root / "model-learning" / "releases" / f"{parent_id}.json"
    parent = load_json(parent_path)
    release = {
        "schema": "MODEL-RELEASE-V1",
        "release_id": release_id,
        "parent_release": parent_id,
        "base_source_manifest": "sources/canonical-manifest.json",
        "patches": [*parent.get("patches", []), patch_path.relative_to(root).as_posix()],
        "latest_patch_sha256": object_sha256(patch_record),
        "training_process_authority": "config/training-policy.json",
        "canonical_sources_mutated": False,
    }
    exclusive_write_json(release_path, release)
    round_record["model_learning_release"] = release_id
    round_record["status"] = "LEARNING_APPLIED"
    atomic_write_json(round_path / "round.json", round_record)
    ledger = load_learning_ledger(root)
    register_rules(ledger, patch_payload["rules"])
    for change in patch_payload["rule_status_changes"]:
        rule_id = change["rule_id"]
        ledger["rule_evidence"][rule_id]["status"] = "RETIRED"
        ledger["attributed_rule_evidence"][rule_id]["status"] = "RETIRED"
    write_learning_ledger(root, ledger)
    state["current_model_release"] = release_id
    if round_record["evaluation_kind"] == "FIRST_BLIND":
        _enqueue_spaced_replay(
            state,
            current_case_id,
            after_current_first_blind=True,
        )
        _close_first_blind_and_advance(root, state, current_case_id)
    else:
        _finish_replay(root, state, current_case_id, False)
    atomic_write_json(_state_path(root), state)
    write_chat_input(root)
    return release
