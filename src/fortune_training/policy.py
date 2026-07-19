from __future__ import annotations

from pathlib import Path
from typing import Any

from .util import TrainingError, load_json


REQUIRED_CONSECUTIVE_PASSES = 3


def required_correct(question_count: int) -> int:
    """Return the pass threshold: all below five, otherwise ceil(80%)."""
    if not isinstance(question_count, int) or isinstance(question_count, bool) or question_count < 1:
        raise TrainingError("question_count must be a positive integer")
    if question_count < 5:
        return question_count
    return (4 * question_count + 4) // 5


def passed(correct_count: int, question_count: int) -> bool:
    if not isinstance(correct_count, int) or isinstance(correct_count, bool):
        raise TrainingError("correct_count must be an integer")
    if correct_count < 0 or correct_count > question_count:
        raise TrainingError("correct_count is outside the valid range")
    return correct_count >= required_correct(question_count)


def load_and_validate_policy(path: Path) -> dict[str, Any]:
    policy = load_json(path)
    expected = {
        "training_unit": "CASE",
        "round_limit": None,
        "consecutive_passing_rounds_required": REQUIRED_CONSECUTIVE_PASSES,
        "failed_round_resets_streak": True,
        "prediction_must_be_frozen_before_scoring": True,
        "failed_round_requires_learning_before_retry": True,
        "answer_plaintext_allowed_in_repository": False,
        "repeated_case_rounds_are_first_blind_evaluations": False,
    }
    for key, value in expected.items():
        if policy.get(key) != value:
            raise TrainingError(f"policy mismatch for {key}: expected {value!r}")
    pass_rule = policy.get("pass_rule", {})
    if pass_rule.get("fewer_than_5_questions") != "ALL_CORRECT":
        raise TrainingError("policy must require all answers correct below five questions")
    if pass_rule.get("5_or_more_questions") != "CEILING_80_PERCENT":
        raise TrainingError("policy must require ceiling 80 percent at five or more questions")
    return policy
