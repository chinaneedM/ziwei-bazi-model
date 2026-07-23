from __future__ import annotations

from pathlib import Path
from typing import Any

from .learning import load_taxonomy, safe_active_rules
from .policy import (
    MINIMUM_NEW_CASES_BETWEEN_REPLAYS,
    REQUIRED_CONSECUTIVE_INDEPENDENT_PASSES,
)
from .util import atomic_write_json, load_json, next_round_id, object_sha256, sha256_file


CHAT_INPUT_RELATIVE_PATH = Path("chat-input/current.json")
CHAT_INPUT_RAW_URL = (
    "https://raw.githubusercontent.com/chinaneedM/ziwei-bazi-model/"
    "main/chat-input/current.json"
)
OPENABLE_STATES = {"READY_FOR_ROUND"}
CASE_VISIBLE_STATES = {
    "READY_FOR_ROUND",
    "AWAITING_PREDICTION_FREEZE",
    "PREDICTION_FROZEN",
    "LEARNING_REQUIRED",
}


def compose_chat_input(root: Path) -> dict[str, Any]:
    root = root.resolve()
    state = load_json(root / "training" / "state.json")
    group = load_json(root / state["group_path"])
    manifest = load_json(root / state["source_manifest_path"])
    taxonomy = load_taxonomy(root)

    current_case_id = None
    current_case = None
    current_case_sha256 = None
    current_case_state: dict[str, Any] = {}
    if state["status"] in CASE_VISIBLE_STATES:
        current_case_id = state.get("active_replay_case_id")
        if current_case_id is None:
            current_case_id = group["case_order"][state["current_case_index"]]
        current_case_state = state["cases"][current_case_id]
        case_path = root / group["cases"][current_case_id]
        current_case = load_json(case_path)
        current_case_sha256 = sha256_file(case_path)

    release_id = state["current_model_release"]
    release = load_json(root / "model-learning" / "releases" / f"{release_id}.json")
    active_rules = safe_active_rules(root, release)
    model_runtime_path = root / "config" / "model-runtime.json"
    model_runtime = load_json(model_runtime_path) if model_runtime_path.is_file() else None
    reasoning_core = (
        load_json(root / model_runtime["reasoning_core"])
        if model_runtime is not None
        else None
    )
    knowledge_route_map = (
        load_json(root / model_runtime["knowledge_route_map"])
        if model_runtime is not None
        else None
    )
    knowledge_card_payloads = (
        [load_json(root / relative_path) for relative_path in model_runtime["knowledge_card_sources"]]
        if model_runtime is not None
        else []
    )
    knowledge_cards = [
        card
        for payload in knowledge_card_payloads
        for card in payload.get("cards", [])
    ]
    prediction_allowed = (
        state["status"] in OPENABLE_STATES
        and state.get("active_round_id") is None
        and current_case_id is not None
    )
    recommended_round_id = next_round_id(state) if prediction_allowed else None

    return {
        "schema": "CHAT-PREDICTION-INPUT-V2",
        "repository": "chinaneedM/ziwei-bazi-model",
        "branch": "main",
        "state_summary": {
            "status": state["status"],
            "current_case_id": current_case_id,
            "current_model_release": release_id,
            "round_count": state["round_count"],
            "prediction_allowed": prediction_allowed,
            "recommended_round_id": recommended_round_id,
            "training_unit": "FIRST_BLIND_CASE_WITH_SPACED_REPLAY",
            "case_attempt_policy": "ONE_FIRST_BLIND_THEN_SPACED_DIAGNOSTIC_REPLAY",
            "evaluation_kind": (
                "SPACED_REPLAY"
                if state.get("active_replay_case_id") == current_case_id
                else "FIRST_BLIND"
            ),
            "independent_pass_streak": state.get("independent_pass_streak", 0),
            "required_consecutive_independent_passes": (
                REQUIRED_CONSECUTIVE_INDEPENDENT_PASSES
            ),
            "failed_first_blind_resets_independent_passes": True,
            "same_case_replay_counts_toward_stage_gate": False,
            "minimum_new_cases_between_replays": MINIMUM_NEW_CASES_BETWEEN_REPLAYS,
            "spaced_replay_queue_size": len(state.get("spaced_replay_queue", [])),
            "dataset_manifest_path": state.get("dataset_manifest_path"),
            "dataset_runtime_status": state.get("dataset_runtime_status"),
            "mode": state.get("mode", "LEGACY_MIGRATION"),
            "formal_phase": state.get("formal_phase"),
        },
        "component_hashes": {
            "current_case_sha256": current_case_sha256,
            "current_model_release_sha256": object_sha256(release),
            "question_taxonomy_sha256": object_sha256(taxonomy),
            "canonical_source_manifest_sha256": object_sha256(manifest),
            "reasoning_core_sha256": object_sha256(reasoning_core),
            "knowledge_route_map_sha256": object_sha256(knowledge_route_map),
            "knowledge_cards_sha256": object_sha256(knowledge_cards),
        },
        "current_case": current_case,
        "question_taxonomy": taxonomy,
        "current_model": {
            "release_id": release_id,
            "reasoning_core": reasoning_core,
            "knowledge_route_map": knowledge_route_map,
            "knowledge_cards": {
                "authority": "DERIVED_ROUTING_AND_PROCEDURE_ONLY",
                "card_count": len(knowledge_cards),
                "cards": knowledge_cards,
            },
            "active_rules": active_rules,
            "rule_application_policy": {
                "VALIDATED": "May be used normally within its declared scope.",
                "PROVISIONAL": "Use as a low-weight hypothesis and never as sole evidence.",
                "CANDIDATE": "Use only when scope matches; never as sole evidence.",
                "CHALLENGED": "Treat as a warning or counter-hypothesis, not a decisive rule.",
            },
        },
        "prediction_output_contract": {
            "packet_schema_after_reveal": "TRAINING-ISSUE-PACKET-V2",
            "each_question_must_include": [
                "top1",
                "top2",
                "reasoning",
                "evidence",
                "strongest_counterevidence",
                "confidence",
                "question_profile",
            ],
            "question_profile_fields": [
                "topic_tags",
                "subject_tags",
                "time_scope_tags",
                "endpoint_tags",
                "reasoning_skill_tags",
                "source_routes",
                "applied_rule_ids",
            ],
            "tagging_rule": (
                "Classify every question before reveal using only its stem/options and the no-answer chart. "
                "Use only taxonomy values. List a rule in applied_rule_ids only when it materially affects "
                "the frozen reasoning; unrelated questions do not validate that rule."
            ),
            "failure_learning_rule": (
                "After reveal, a failed round must propose one or more generic candidate rules. Rules may "
                "contain no case id, question id, answer letter, option position, or copied option sentence. "
                "Each unique rule_id starts with RULE- and uses uppercase letters, digits, and hyphens only."
            ),
        },
        "chat_work_handoff_contract": {
            "schema": "CHAT-WORK-HANDOFF-CONTRACT-V1",
            "transport": "GITHUB_ISSUE_DURABLE_RECEIPT",
            "issue_title": (
                f"[PREDICTION HANDOFF] {recommended_round_id} {current_case_id}"
                if prediction_allowed
                else None
            ),
            "handoff_schema": "CHAT-WORK-PREDICTION-HANDOFF-V1",
            "binding": {
                "case_id": current_case_id,
                "round_id": recommended_round_id,
                "evaluation_kind": (
                    "SPACED_REPLAY"
                    if state.get("active_replay_case_id") == current_case_id
                    else "FIRST_BLIND"
                ),
                "model_release": release_id,
                "current_case_sha256": current_case_sha256,
                "current_model_release_sha256": object_sha256(release),
                "canonical_source_manifest_sha256": object_sha256(manifest),
            },
            "handoff_required_fields": [
                "schema",
                "binding",
                "predictions",
            ],
            "handoff_forbidden_fields": [
                "answer",
                "correct_option",
                "score",
                "review",
                "expected_result",
                "learning_release_id",
                "learning_patch",
            ],
            "chat_freeze_rule": (
                "After all predictions are frozen, create exactly one GitHub Issue using issue_title "
                "and CHAT-WORK-PREDICTION-HANDOFF-V1. Copy binding exactly and preserve the complete "
                "prediction rows. This is the only Chat-side GitHub write allowed."
            ),
            "work_acceptance_rule": (
                "Read the unique open handoff Issue for binding.round_id; never reconstruct predictions "
                "from conversation memory. Validate every binding value against this current bundle and "
                "stop before scoring if the receipt is missing, duplicated, stale, or mismatched."
            ),
            "training_issue_input_contract": {
                "schema": "TRAINING-ISSUE-PACKET-V2",
                "allowed_top_level_fields": [
                    "schema",
                    "round_id",
                    "case_id",
                    "predictions",
                    "expected_result",
                    "learning_release_id",
                    "learning_patch",
                ],
                "pass_required_fields": [
                    "schema",
                    "round_id",
                    "case_id",
                    "predictions",
                    "expected_result",
                ],
                "pass_forbidden_fields": [
                    "learning_release_id",
                    "learning_patch",
                ],
                "fail_required_fields": [
                    "schema",
                    "round_id",
                    "case_id",
                    "predictions",
                    "expected_result",
                    "learning_release_id",
                    "learning_patch",
                ],
                "result_only_fields_forbidden_in_input": [
                    "evaluation_kind",
                    "accuracy",
                    "correct_count",
                    "top2_coverage",
                    "learning_release",
                    "next_case_id",
                    "next_status",
                ],
            },
        },
        "canonical_source_manifest": manifest,
        "prediction_access_contract": {
            "git_read_scope": "THIS_EXACT_FILE_ONLY",
            "permitted_git_url": CHAT_INPUT_RAW_URL,
            "canonical_sources": (
                "Use only the project S00-S19 read-only mirrors whose source ids match "
                "canonical_source_manifest; S02 (8) is forbidden and S02 (9) is active."
            ),
            "project_source_precondition": (
                model_runtime.get("chat_source_access")
                if model_runtime is not None
                else {
                    "mode": "LEGACY_TEST_FIXTURE",
                    "fail_closed_when_project_sources_unavailable": True,
                }
            ),
            "forbidden_git_operations": [
                "repository search",
                "code search",
                "commit search or commit inspection",
                "history, diff, branch, tree, or directory listing",
                "opening training/runs, prediction-freeze, score, review, relay-results, learning-ledger, or answer-vault",
            ],
            "forbidden_prediction_inputs": [
                "old predictions",
                "old answer mappings",
                "scores or detailed reviews",
                "answer envelopes or keys",
            ],
            "unexpected_output_rule": (
                "If any tool unexpectedly returns an old prediction, answer mapping, score, or review, "
                "stop without predicting and discard that Chat conversation."
            ),
        },
        "contains_old_predictions": False,
        "contains_answers": False,
        "contains_scores_or_reviews": False,
    }


def write_chat_input(root: Path) -> dict[str, Any]:
    payload = compose_chat_input(root)
    atomic_write_json(root.resolve() / CHAT_INPUT_RELATIVE_PATH, payload)
    return payload
