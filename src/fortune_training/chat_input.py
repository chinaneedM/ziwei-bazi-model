from __future__ import annotations

from pathlib import Path
from typing import Any

from .learning import load_taxonomy, safe_active_rules
from .util import atomic_write_json, load_json, object_sha256, sha256_file


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
    prediction_allowed = (
        state["status"] in OPENABLE_STATES
        and state.get("active_round_id") is None
        and current_case_id is not None
        and current_case_state.get("first_blind_round_id") is None
    )
    recommended_round_id = f"ROUND-{state['round_count'] + 1:03d}" if prediction_allowed else None

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
            "training_unit": "QUESTION_FIRST_BLIND",
            "case_attempt_policy": "ONE_SCORED_FIRST_BLIND_ROUND",
            "same_case_replays_count_toward_validation": False,
            "dataset_manifest_path": state.get("dataset_manifest_path"),
            "dataset_runtime_status": state.get("dataset_runtime_status"),
        },
        "component_hashes": {
            "current_case_sha256": current_case_sha256,
            "current_model_release_sha256": object_sha256(release),
            "question_taxonomy_sha256": object_sha256(taxonomy),
            "canonical_source_manifest_sha256": object_sha256(manifest),
            "reasoning_core_sha256": object_sha256(reasoning_core),
            "knowledge_route_map_sha256": object_sha256(knowledge_route_map),
        },
        "current_case": current_case,
        "question_taxonomy": taxonomy,
        "current_model": {
            "release_id": release_id,
            "reasoning_core": reasoning_core,
            "knowledge_route_map": knowledge_route_map,
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
