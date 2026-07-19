from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet, InvalidToken

from .policy import REQUIRED_CONSECUTIVE_PASSES, passed, required_correct
from .util import (
    TrainingError,
    atomic_write_json,
    canonical_bytes,
    exclusive_write_json,
    load_json,
    object_sha256,
    require_outside,
    require_safe_id,
    sha256_file,
    utc_now,
)
from .verify import verify_repository


OPENABLE_STATES = {"READY_FOR_ROUND", "CONFIRMATION_REQUIRED"}
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
PATCH_PRINCIPLE_FIELDS = {
    "statement",
    "applicability",
    "limits",
    "counterexamples",
    "capability_ceiling",
    "source_basis",
}


def _state_path(root: Path) -> Path:
    return root / "training" / "state.json"


def _load_state(root: Path) -> dict[str, Any]:
    return load_json(_state_path(root))


def _load_group(root: Path, state: dict[str, Any]) -> dict[str, Any]:
    return load_json(root / state["group_path"])


def _current_case_id(state: dict[str, Any], group: dict[str, Any]) -> str:
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


def status(root: Path) -> dict[str, Any]:
    state = _load_state(root)
    group = _load_group(root, state)
    current_case = None
    if state["status"] != "GROUP_COMPLETE":
        current_case = _current_case_id(state, group)
    return {
        "group_id": state["group_id"],
        "status": state["status"],
        "current_case_id": current_case,
        "current_source_release": state["current_source_release"],
        "active_round_id": state["active_round_id"],
        "round_count": state["round_count"],
        "round_limit": None,
        "consecutive_passes": state["cases"].get(current_case, {}).get("consecutive_passes") if current_case else None,
        "consecutive_passes_required": REQUIRED_CONSECUTIVE_PASSES,
    }


def start_round(root: Path, round_id: str) -> dict[str, Any]:
    root = root.resolve()
    verify_repository(root)
    state = _load_state(root)
    if state["status"] not in OPENABLE_STATES:
        raise TrainingError(f"cannot start a round while state is {state['status']}")
    if state.get("active_round_id") is not None:
        raise TrainingError("another round is already active")
    group = _load_group(root, state)
    case_id = _current_case_id(state, group)
    case_path = _case_path(root, group, case_id)
    case = load_json(case_path)
    question_count = len(_questions(case))
    release_path = root / "sources" / "releases" / f"{state['current_source_release']}.json"
    release = load_json(release_path)
    round_path = _round_dir(root, round_id)
    if round_path.exists():
        raise TrainingError(f"round already exists: {round_id}")
    round_record = {
        "schema": "CASE-TRAINING-ROUND-V1",
        "round_id": round_id,
        "case_id": case_id,
        "case_path": case_path.relative_to(root).as_posix(),
        "case_sha256": sha256_file(case_path),
        "question_count": question_count,
        "required_correct": required_correct(question_count),
        "source_release": state["current_source_release"],
        "source_release_sha256": object_sha256(release),
        "status": "PREDICTION_OPEN",
        "answer_visibility": "PHYSICALLY_UNAVAILABLE_TO_PREDICTION_CONTEXT",
        "started_at": utc_now(),
    }
    exclusive_write_json(round_path / "round.json", round_record)
    state["active_round_id"] = round_id
    state["status"] = "AWAITING_PREDICTION_FREEZE"
    state["round_count"] += 1
    state["cases"][case_id]["round_ids"].append(round_id)
    atomic_write_json(_state_path(root), state)
    return round_record


def _validate_prediction(case: dict[str, Any], round_record: dict[str, Any], payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise TrainingError("prediction payload must be an object")
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
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in predictions:
        if not isinstance(row, dict):
            raise TrainingError("every prediction row must be an object")
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
        if top2 is not None and (top2 not in valid_options or top2 == top1):
            raise TrainingError(f"invalid top2 for {question_id}: {top2!r}")
        normalized.append(
            {
                "question_id": question_id,
                "top1": top1,
                "top2": top2,
                "reasoning": row.get("reasoning", ""),
                "evidence": row.get("evidence", []),
            }
        )
    normalized.sort(key=lambda item: list(question_map).index(item["question_id"]))
    return {
        "schema": "FROZEN-PREDICTION-V1",
        "case_id": round_record["case_id"],
        "round_id": round_record["round_id"],
        "predictions": normalized,
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
    frozen = _validate_prediction(case, round_record, load_json(prediction_path))
    frozen["prediction_sha256"] = object_sha256(frozen["predictions"])
    exclusive_write_json(round_path / "prediction-freeze.json", frozen)
    round_record["status"] = "PREDICTION_FROZEN"
    round_record["prediction_sha256"] = frozen["prediction_sha256"]
    round_record["frozen_at"] = frozen["frozen_at"]
    atomic_write_json(round_path / "round.json", round_record)
    state["status"] = "PREDICTION_FROZEN"
    atomic_write_json(_state_path(root), state)
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


def _validate_answers(case: dict[str, Any], payload: Any) -> dict[str, str]:
    if not isinstance(payload, dict) or payload.get("case_id") != case.get("case_id"):
        raise TrainingError("answer case_id mismatch")
    rows = payload.get("answers")
    if not isinstance(rows, list):
        raise TrainingError("answers must be an array")
    questions = {question["question_id"]: question for question in _questions(case)}
    answer_map: dict[str, str] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise TrainingError("every answer row must be an object")
        question_id = row.get("question_id")
        correct = row.get("correct_option")
        if question_id not in questions or question_id in answer_map:
            raise TrainingError(f"invalid or duplicate answer question: {question_id!r}")
        valid_options = {option["option_id"] for option in questions[question_id]["options"]}
        if correct not in valid_options:
            raise TrainingError(f"invalid correct option for {question_id}")
        answer_map[question_id] = correct
    if set(answer_map) != set(questions):
        raise TrainingError("answer payload must cover every question exactly once")
    return answer_map


def encrypt_answer(root: Path, case_id: str, plaintext_path: Path, key: str | bytes | None = None) -> Path:
    root = root.resolve()
    require_safe_id(case_id, "case_id")
    require_outside(root, plaintext_path, "plaintext answer input")
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


def _decrypt_answers(root: Path, case: dict[str, Any], key: str | bytes | None) -> dict[str, str]:
    envelope = root / "answer-vault" / "encrypted" / f"{case['case_id']}.json.fernet"
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
    if round_record.get("prediction_sha256") != object_sha256(frozen["predictions"]):
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
    for question in _questions(case):
        question_id = question["question_id"]
        predicted = prediction_map[question_id]
        correct = answers[question_id]
        is_correct = predicted == correct
        correct_count += int(is_correct)
        review_rows.append(
            {
                "question_id": question_id,
                "predicted_option": predicted,
                "correct_option": correct,
                "is_correct": is_correct,
            }
        )
    question_count = len(review_rows)
    did_pass = passed(correct_count, question_count)
    case_state = state["cases"][round_record["case_id"]]
    streak_before = case_state["consecutive_passes"]
    streak_after = streak_before + 1 if did_pass else 0
    case_state["consecutive_passes"] = streak_after
    aggregate = {
        "schema": "CASE-ROUND-SCORE-V1",
        "round_id": round_id,
        "case_id": round_record["case_id"],
        "correct_count": correct_count,
        "question_count": question_count,
        "required_correct": required_correct(question_count),
        "accuracy": correct_count / question_count,
        "passed": did_pass,
        "consecutive_passes_before": streak_before,
        "consecutive_passes_after": streak_after,
        "scored_at": utc_now(),
        "detailed_answers_stored_in_repository": False,
        "answer_source": answer_source,
    }
    detailed_review = {
        "schema": "CASE-ROUND-DETAILED-REVIEW-V1",
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

    if not did_pass:
        state["status"] = "LEARNING_REQUIRED"
        case_state["status"] = "ACTIVE"
    elif streak_after < REQUIRED_CONSECUTIVE_PASSES:
        state["status"] = "CONFIRMATION_REQUIRED"
        case_state["status"] = "ACTIVE"
    else:
        case_state["status"] = "COMPLETE"
        state["current_case_index"] += 1
        group = _load_group(root, state)
        if state["current_case_index"] >= len(group["case_order"]):
            state["status"] = "GROUP_COMPLETE"
        else:
            next_case = group["case_order"][state["current_case_index"]]
            state["cases"][next_case]["status"] = "ACTIVE"
            state["status"] = "READY_FOR_ROUND"
    atomic_write_json(_state_path(root), state)
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
    group = load_json(root / "examples" / "DEV-GROUP-002" / "group.json")
    for case_path in group["cases"].values():
        case = load_json(root / case_path)
        for question in _questions(case):
            unique_texts = [question.get("stem", ""), *(row.get("text", "") for row in question["options"])]
            for text in unique_texts:
                normalized = " ".join(str(text).split())
                if len(normalized) >= 8 and normalized in serialized:
                    raise TrainingError("learning patch copies a case-specific question or option text")
    affected = payload.get("affected_libraries")
    if not isinstance(affected, list) or not affected:
        raise TrainingError("learning patch needs affected_libraries")
    valid_libraries = {f"S{index:02d}" for index in range(20)}
    if any(item not in valid_libraries for item in affected) or len(set(affected)) != len(affected):
        raise TrainingError("affected_libraries must be unique S00-S19 ids")
    principles = payload.get("principles")
    if not isinstance(principles, list) or not principles:
        raise TrainingError("learning patch needs at least one general principle")
    for index, principle in enumerate(principles):
        if not isinstance(principle, dict) or not PATCH_PRINCIPLE_FIELDS.issubset(principle):
            raise TrainingError(f"principle {index} lacks required generalization fields")
        if any(not principle[field] for field in PATCH_PRINCIPLE_FIELDS):
            raise TrainingError(f"principle {index} has an empty required field")
    return payload


def apply_learning(root: Path, round_id: str, patch_input: Path, release_id: str) -> dict[str, Any]:
    root = root.resolve()
    require_safe_id(release_id, "release_id")
    require_outside(root, patch_input, "learning patch input")
    state = _load_state(root)
    if state.get("status") != "LEARNING_REQUIRED":
        raise TrainingError("learning is only accepted after a failed round")
    group = _load_group(root, state)
    current_case_id = _current_case_id(state, group)
    if state["cases"][current_case_id]["round_ids"][-1] != round_id:
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
        "schema": "GENERAL-LEARNING-PATCH-V1",
        "release_id": release_id,
        "derived_from_failed_round": round_id,
        "created_at": utc_now(),
        "content": patch_payload,
        "contains_case_answer_mapping": False,
    }
    patch_path = root / "sources" / "patches" / f"{release_id}.json"
    release_path = root / "sources" / "releases" / f"{release_id}.json"
    if patch_path.exists() or release_path.exists():
        raise TrainingError(f"learning release already exists: {release_id}")
    exclusive_write_json(patch_path, patch_record)
    parent_id = state["current_source_release"]
    parent_path = root / "sources" / "releases" / f"{parent_id}.json"
    parent = load_json(parent_path)
    release = {
        "schema": "SOURCE-RELEASE-V1",
        "release_id": release_id,
        "parent_release": parent_id,
        "base_manifest": "sources/manifest.json",
        "patches": [*parent.get("patches", []), patch_path.relative_to(root).as_posix()],
        "latest_patch_sha256": object_sha256(patch_record),
        "training_process_authority": "config/training-policy.json",
    }
    exclusive_write_json(release_path, release)
    round_record["learning_release"] = release_id
    round_record["status"] = "LEARNING_APPLIED"
    atomic_write_json(round_path / "round.json", round_record)
    state["current_source_release"] = release_id
    state["status"] = "READY_FOR_ROUND"
    atomic_write_json(_state_path(root), state)
    return release
