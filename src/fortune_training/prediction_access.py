from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Any

from .util import TrainingError, load_json


PREDICTION_TOOL_POLICY_PATH = Path("config/prediction-tool-policy.json")
POLICY_SCHEMA = "FORMAL-PREDICTION-TOOL-POLICY-V1"
CONTRACT_SCHEMA = "FORMAL-PREDICTION-ACCESS-CONTRACT-V1"

BASE_EXACT_PATHS = {
    "training/state.json",
    "chat-input/current.json",
    "chat-input/prediction-row-template.json",
    "chat-input/runtime-model.json",
    "sources/canonical-manifest.json",
    "config/chat-runtime-performance.json",
    "config/prediction-tool-policy.json",
    "config/model-runtime.json",
    "config/knowledge-route-map.json",
    "config/question-taxonomy.json",
    "config/source-policy.json",
    "config/training-policy.json",
    "model-learning/methods/REASONING-CORE-V3.json",
    "model-learning/runtime-governance.json",
}
ALLOWED_PREFIXES = ("sources/canonical/",)
FORBIDDEN_REPOSITORY_PREFIXES = (
    "answer-vault/",
    "case-bank/raw/",
    "prediction-freeze/",
    "score/",
    "review/",
    "training/history/",
    "training/learning-ledger.json",
    "training/relay-results/",
    "training/runs/",
)


def load_prediction_tool_policy(root: Path) -> dict[str, Any]:
    policy = load_json(root.resolve() / PREDICTION_TOOL_POLICY_PATH)
    required = {
        "schema",
        "phase",
        "default_decision",
        "allowed_repository",
        "allowed_ref",
        "allowed_tool_classes",
        "forbidden_tool_classes",
        "forbidden_context_sources",
        "violation_action",
    }
    if set(policy) != required or policy.get("schema") != POLICY_SCHEMA:
        raise TrainingError("invalid formal prediction tool policy")
    if policy.get("phase") != "PREDICTION" or policy.get("default_decision") != "DENY":
        raise TrainingError("prediction tool policy must fail closed")
    if policy.get("allowed_repository") != "chinaneedM/ziwei-bazi-model":
        raise TrainingError("prediction tool policy points to the wrong repository")
    if policy.get("allowed_ref") != "main":
        raise TrainingError("prediction tool policy must read main")
    if policy.get("allowed_tool_classes") != ["GITHUB_FETCH_FILE"]:
        raise TrainingError("prediction may only use GitHub file fetch")
    required_forbidden_tools = {
        "ATTACHMENT_FILE_READ",
        "FILE_LIBRARY_READ",
        "GITHUB_COMMIT_INSPECTION",
        "GITHUB_DIFF",
        "GITHUB_HISTORY",
        "GITHUB_REPOSITORY_SEARCH",
        "GITHUB_TREE_LISTING",
        "PERSONAL_CONTEXT_SEARCH",
    }
    if set(policy.get("forbidden_tool_classes", [])) != required_forbidden_tools:
        raise TrainingError("prediction tool denylist is incomplete")
    required_forbidden_context = {
        "CHAT_ATTACHMENTS",
        "CROSS_CONVERSATION_MEMORY",
        "FILE_LIBRARY",
        "HISTORICAL_UPLOADS",
        "PERSONAL_CONTEXT",
        "PRIOR_ASSISTANT_OUTPUT",
    }
    if set(policy.get("forbidden_context_sources", [])) != required_forbidden_context:
        raise TrainingError("prediction context denylist is incomplete")
    if policy.get("violation_action") != "ABORT_BEFORE_PREDICTION_AND_QUARANTINE_CASE":
        raise TrainingError("prediction access violation must quarantine before prediction")
    return policy


def _current_model_paths(root: Path, state: dict[str, Any]) -> set[str]:
    release_id = state.get("current_model_release")
    if not isinstance(release_id, str):
        raise TrainingError("training state has no current model release")
    release_path = f"model-learning/releases/{release_id}.json"
    release = load_json(root / release_path)
    if release.get("release_id") != release_id:
        raise TrainingError("current model release id mismatch")
    paths = {release_path}
    patches = release.get("patches")
    if not isinstance(patches, list) or any(
        not isinstance(path, str) or not path.startswith("model-learning/patches/")
        for path in patches
    ):
        raise TrainingError("current model release has invalid patch paths")
    paths.update(patches)
    return paths


def allowed_prediction_paths(root: Path, state: dict[str, Any]) -> dict[str, list[str]]:
    exact = BASE_EXACT_PATHS | _current_model_paths(root.resolve(), state)
    return {
        "exact": sorted(exact),
        "prefixes": list(ALLOWED_PREFIXES),
    }


def build_prediction_access_contract(
    root: Path,
    state: dict[str, Any],
) -> dict[str, Any]:
    policy = load_prediction_tool_policy(root)
    allowed_paths = allowed_prediction_paths(root, state)
    return {
        "schema": CONTRACT_SCHEMA,
        "phase": policy["phase"],
        "enforcement": "DEFAULT_DENY_FAIL_CLOSED",
        "repository": policy["allowed_repository"],
        "ref": policy["allowed_ref"],
        "allowed_tool_classes": policy["allowed_tool_classes"],
        "allowed_repository_paths": allowed_paths,
        "forbidden_repository_prefixes": list(FORBIDDEN_REPOSITORY_PREFIXES),
        "forbidden_tool_classes": policy["forbidden_tool_classes"],
        "forbidden_context_sources": policy["forbidden_context_sources"],
        "file_library_allowed": False,
        "chat_attachments_allowed": False,
        "historical_uploads_allowed": False,
        "cross_conversation_memory_allowed": False,
        "old_predictions_allowed": False,
        "old_reveals_allowed": False,
        "old_diagnostics_allowed": False,
        "answer_related_objects_allowed": False,
        "violation_action": policy["violation_action"],
    }


def assert_prediction_access(
    root: Path,
    state: dict[str, Any],
    *,
    tool_class: str,
    context_source: str,
    repository: str,
    ref: str,
    path: str,
) -> None:
    contract = build_prediction_access_contract(root, state)
    if tool_class not in contract["allowed_tool_classes"]:
        raise TrainingError(f"prediction tool is not allowed: {tool_class}")
    if context_source != "GITHUB_MAIN":
        raise TrainingError(f"prediction context source is not allowed: {context_source}")
    if repository != contract["repository"] or ref != contract["ref"]:
        raise TrainingError("prediction repository read is not pinned to the authorized main")
    normalized = PurePosixPath(path).as_posix().lstrip("/")
    if normalized == "." or ".." in PurePosixPath(normalized).parts:
        raise TrainingError("prediction repository path is invalid")
    exact = set(contract["allowed_repository_paths"]["exact"])
    prefixes = tuple(contract["allowed_repository_paths"]["prefixes"])
    if normalized not in exact and not normalized.startswith(prefixes):
        raise TrainingError(f"prediction repository path is not allowed: {normalized}")
    if normalized.startswith(tuple(contract["forbidden_repository_prefixes"])):
        raise TrainingError(f"prediction repository path is forbidden: {normalized}")
