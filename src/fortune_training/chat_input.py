from __future__ import annotations

from pathlib import Path
from typing import Any

from .policy import REQUIRED_CONSECUTIVE_PASSES
from .util import atomic_write_json, load_json, object_sha256, sha256_file


CHAT_INPUT_RELATIVE_PATH = Path("chat-input/current.json")
CHAT_INPUT_RAW_URL = (
    "https://raw.githubusercontent.com/chinaneedM/ziwei-bazi-model/"
    "main/chat-input/current.json"
)
OPENABLE_STATES = {"READY_FOR_ROUND", "CONFIRMATION_REQUIRED"}


def compose_chat_input(root: Path) -> dict[str, Any]:
    root = root.resolve()
    state = load_json(root / "training" / "state.json")
    group = load_json(root / state["group_path"])
    manifest = load_json(root / state["source_manifest_path"])

    current_case_id = None
    current_case = None
    current_case_sha256 = None
    consecutive_passes = None
    if state["status"] != "GROUP_COMPLETE":
        current_case_id = group["case_order"][state["current_case_index"]]
        case_path = root / group["cases"][current_case_id]
        current_case = load_json(case_path)
        current_case_sha256 = sha256_file(case_path)
        consecutive_passes = state["cases"][current_case_id]["consecutive_passes"]

    release_id = state["current_model_release"]
    release = load_json(root / "model-learning" / "releases" / f"{release_id}.json")
    patches = [
        {"path": path, "record": load_json(root / path)}
        for path in release.get("patches", [])
    ]
    prediction_allowed = (
        state["status"] in OPENABLE_STATES
        and state.get("active_round_id") is None
        and current_case_id is not None
    )
    recommended_round_id = f"ROUND-{state['round_count'] + 1:03d}" if prediction_allowed else None

    return {
        "schema": "CHAT-PREDICTION-INPUT-V1",
        "repository": "chinaneedM/ziwei-bazi-model",
        "branch": "main",
        "state_summary": {
            "status": state["status"],
            "current_case_id": current_case_id,
            "current_model_release": release_id,
            "round_count": state["round_count"],
            "consecutive_passes": consecutive_passes,
            "consecutive_passes_required": REQUIRED_CONSECUTIVE_PASSES,
            "prediction_allowed": prediction_allowed,
            "recommended_round_id": recommended_round_id,
        },
        "component_hashes": {
            "current_case_sha256": current_case_sha256,
            "current_model_release_sha256": object_sha256(release),
            "canonical_source_manifest_sha256": object_sha256(manifest),
        },
        "current_case": current_case,
        "current_model": {
            "release": release,
            "active_patches": patches,
        },
        "canonical_source_manifest": manifest,
        "prediction_access_contract": {
            "git_read_scope": "THIS_EXACT_FILE_ONLY",
            "permitted_git_url": CHAT_INPUT_RAW_URL,
            "canonical_sources": (
                "Use only the project S00-S19 read-only mirrors whose source ids match "
                "canonical_source_manifest; S02 (8) is forbidden and S02 (9) is active."
            ),
            "forbidden_git_operations": [
                "repository search",
                "code search",
                "commit search or commit inspection",
                "history, diff, branch, tree, or directory listing",
                "opening training/runs, prediction-freeze, score, review, relay-results, or answer-vault",
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
