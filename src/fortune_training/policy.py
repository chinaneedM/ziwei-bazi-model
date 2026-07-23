from __future__ import annotations

from pathlib import Path
from typing import Any

from .util import TrainingError, load_json


RULE_MIN_SUPPORTING_APPLICATIONS = 3
RULE_MIN_DISTINCT_FUTURE_CASES = 3
RULE_MIN_SUPPORT_RATIO = 0.8
REQUIRED_CONSECUTIVE_INDEPENDENT_PASSES = 3
MINIMUM_NEW_CASES_BETWEEN_REPLAYS = 5


def required_correct(question_count: int) -> int:
    """Return the round-quality threshold: all below five, otherwise ceil(80%)."""
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
        "schema": "GENERALIZATION-TRAINING-POLICY-R2",
        "training_unit": "FIRST_BLIND_CASE_WITH_SPACED_REPLAY",
        "round_limit": None,
        "case_attempt_policy": "ONE_FIRST_BLIND_THEN_SPACED_DIAGNOSTIC_REPLAY",
        "required_consecutive_independent_passes": REQUIRED_CONSECUTIVE_INDEPENDENT_PASSES,
        "independent_pass_requires_distinct_first_blind_case": True,
        "failed_first_blind_resets_independent_passes": True,
        "first_blind_case_advances_after_round_closure": True,
        "failed_round_requires_general_learning_before_advance": True,
        "same_case_replay_counts_as_independent_evidence": False,
        "same_case_replay_counts_toward_stage_gate": False,
        "minimum_new_cases_between_replays": MINIMUM_NEW_CASES_BETWEEN_REPLAYS,
        "replay_purpose": "DIAGNOSTIC_REMEDIATION_ONLY",
        "prediction_must_be_frozen_before_scoring": True,
        "failed_round_updates_model_layer_only": True,
        "canonical_sources_mutable_during_training": False,
        "answer_plaintext_allowed_in_repository": False,
        "performance_reporting": "SEPARATE_FIRST_BLIND_FROM_REPLAY_BY_CASE_TOPIC_AND_REASONING_SKILL",
    }
    for key, value in expected.items():
        if policy.get(key) != value:
            raise TrainingError(f"policy mismatch for {key}: expected {value!r}")
    pass_rule = policy.get("pass_rule", {})
    if pass_rule.get("fewer_than_5_questions") != "ALL_CORRECT":
        raise TrainingError("policy must require all answers correct below five questions")
    if pass_rule.get("5_or_more_questions") != "CEILING_80_PERCENT":
        raise TrainingError("policy must require ceiling 80 percent at five or more questions")
    validation = policy.get("rule_validation", {})
    validation_expected = {
        "minimum_supporting_applications": RULE_MIN_SUPPORTING_APPLICATIONS,
        "minimum_distinct_future_cases": RULE_MIN_DISTINCT_FUTURE_CASES,
        "minimum_support_ratio": RULE_MIN_SUPPORT_RATIO,
        "unrelated_questions_count_as_evidence": False,
        "same_origin_case_counts_as_validation": False,
    }
    for key, value in validation_expected.items():
        if validation.get(key) != value:
            raise TrainingError(f"rule-validation policy mismatch for {key}: expected {value!r}")
    partition = policy.get("dataset_partition_policy", {})
    partition_expected = {
        "manifest": "case-bank/manifest.json",
        "development": "case-bank/partitions/development.json",
        "stage_validation": "case-bank/partitions/stage-validation.json",
        "final_holdout": "case-bank/partitions/final-holdout.json",
        "same_identity_across_partitions_allowed": False,
        "blocked_input_can_enter_partition": False,
        "validation_can_create_rule": False,
        "final_holdout_can_create_rule": False,
        "historical_revealed_cases_count_as_future_validation": False,
        "source_exposed_cases_count_as_first_blind": False,
    }
    for key, value in partition_expected.items():
        if partition.get(key) != value:
            raise TrainingError(f"dataset-partition policy mismatch for {key}: expected {value!r}")
    composite = policy.get("composite_option_policy", {})
    if composite != {
        "atomize_before_prediction": True,
        "record_atom_level_failure_after_reveal": True,
        "whole_option_score_remains_top1_only": True,
    }:
        raise TrainingError("composite-option policy mismatch")
    return policy
