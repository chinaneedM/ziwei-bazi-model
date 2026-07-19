from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .policy import load_and_validate_policy
from .util import TrainingError, is_within, load_json, object_sha256, sha256_file


SOURCE_ID = re.compile(r"^(S(?:0[0-9]|1[0-9]))_")
ALLOWED_ANSWER_KEYS = {
    "answer_isolation",
    "answer_payload_present",
    "answer_reference_disclosed",
}
FORBIDDEN_CASE_KEYS = {
    "answer",
    "answers",
    "answer_key",
    "correct_answer",
    "correct_option",
    "gold",
    "label",
    "revealed_answer",
}


def build_source_manifest(root: Path) -> dict[str, Any]:
    """Build the immutable Git canonical-source manifest for comparison only."""
    source_dir = root / "sources" / "canonical"
    files = sorted(source_dir.glob("*.txt"))
    entries: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in files:
        match = SOURCE_ID.match(path.name)
        if not match:
            raise TrainingError(f"unexpected source filename: {path.name}")
        source_id = match.group(1)
        if source_id in seen:
            raise TrainingError(f"duplicate source library: {source_id}")
        seen.add(source_id)
        entries.append(
            {
                "source_id": source_id,
                "path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
                "runtime_role": (
                    "TRAINING_LOOP_GUIDANCE"
                    if source_id == "S19"
                    else "PREDICTION_KNOWLEDGE_ONLY"
                ),
            }
        )
    expected = {f"S{index:02d}" for index in range(20)}
    if seen != expected:
        missing = sorted(expected - seen)
        extra = sorted(seen - expected)
        raise TrainingError(f"source set must be exactly S00-S19; missing={missing}, extra={extra}")
    manifest = {
        "schema": "CANONICAL-SOURCE-MANIFEST-V1",
        "source_count": len(entries),
        "process_authority": "config/training-policy.json",
        "runtime_source": "GIT_REPOSITORY_ONLY",
        "mutability": "IMMUTABLE_DURING_TRAINING",
        "sources": entries,
    }
    return manifest


def _validate_source_policy(root: Path) -> dict[str, Any]:
    policy = load_json(root / "config" / "source-policy.json")
    if policy.get("schema") != "SOURCE-AUTHORITY-POLICY-V1":
        raise TrainingError("wrong source authority policy schema")
    expected = {
        "original_project_library_role": "ARCHIVAL_READ_ONLY_NOT_RUNTIME",
        "original_project_library_deletion_required": False,
        "runtime_source": "GIT_REPOSITORY_ONLY",
        "git_canonical_path": "sources/canonical",
        "git_canonical_mutable_during_training": False,
        "model_learning_path": "model-learning",
        "model_learning_mutable_during_training": True,
        "conflict_resolution": "IGNORE_EXTERNAL_ORIGINAL_AND_USE_GIT_RUNTIME",
    }
    for key, value in expected.items():
        if policy.get(key) != value:
            raise TrainingError(f"source policy mismatch for {key}: expected {value!r}")
    manifest_hash = policy.get("canonical_manifest_sha256")
    if not isinstance(manifest_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", manifest_hash):
        raise TrainingError("source policy needs a valid canonical_manifest_sha256 lock")
    return policy


def _validate_answer_policy(root: Path) -> dict[str, Any]:
    policy = load_json(root / "config" / "answer-policy.json")
    if policy.get("schema") != "PUBLIC-REPOSITORY-ANSWER-POLICY-V1":
        raise TrainingError("wrong public-repository answer policy schema")
    expected = {
        "repository_visibility": "PUBLIC",
        "private_answer_repository_required": False,
        "plaintext_answers_allowed": False,
        "encrypted_answer_envelopes_allowed": True,
        "decryption_keys_allowed": False,
        "answer_read_phase": "POST_FREEZE_ONLY",
    }
    for key, value in expected.items():
        if policy.get(key) != value:
            raise TrainingError(f"answer policy mismatch for {key}: expected {value!r}")
    return policy


def _check_answer_free(value: Any, location: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = key.lower()
            if lowered in FORBIDDEN_CASE_KEYS:
                raise TrainingError(f"answer-bearing key in case input: {location}.{key}")
            if "answer" in lowered and lowered not in ALLOWED_ANSWER_KEYS:
                raise TrainingError(f"suspicious answer key in case input: {location}.{key}")
            _check_answer_free(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _check_answer_free(child, f"{location}[{index}]")


def _validate_case(root: Path, case_id: str, relative_path: str) -> int:
    case = load_json(root / relative_path)
    if case.get("case_id") != case_id:
        raise TrainingError(f"case id mismatch in {relative_path}")
    if case.get("group_id") != "DEV-GROUP-002":
        raise TrainingError(f"unexpected group id in {relative_path}")
    if case.get("answer_isolation", {}).get("answer_payload_present") is not False:
        raise TrainingError(f"case does not declare answer isolation: {relative_path}")
    binding = case.get("binding", {})
    if binding.get("source_manifest") != "sources/canonical-manifest.json":
        raise TrainingError(f"case does not bind the Git canonical source lock: {relative_path}")
    if binding.get("training_policy") != "config/training-policy.json":
        raise TrainingError(f"case does not bind the training policy: {relative_path}")
    _check_answer_free(case)
    questions = case.get("questions", {}).get("parsed")
    if not isinstance(questions, list) or not questions:
        raise TrainingError(f"case has no parsed questions: {relative_path}")
    declared = case.get("questions", {}).get("question_count")
    if declared != len(questions):
        raise TrainingError(f"question count mismatch in {relative_path}")
    seen_questions: set[str] = set()
    for question in questions:
        question_id = question.get("question_id")
        if not isinstance(question_id, str) or question_id in seen_questions:
            raise TrainingError(f"invalid or duplicate question id in {relative_path}")
        seen_questions.add(question_id)
        options = question.get("options")
        if not isinstance(options, list) or len(options) < 2:
            raise TrainingError(f"question {question_id} needs at least two options")
        option_ids = [option.get("option_id") for option in options]
        if any(not isinstance(item, str) for item in option_ids) or len(set(option_ids)) != len(option_ids):
            raise TrainingError(f"invalid option ids for {case_id}/{question_id}")
    return len(questions)


def _validate_release_chain(root: Path, release_id: str, seen: set[str] | None = None) -> dict[str, Any]:
    if seen is None:
        seen = set()
    if release_id in seen:
        raise TrainingError(f"model release cycle detected at {release_id}")
    seen.add(release_id)
    release_path = root / "model-learning" / "releases" / f"{release_id}.json"
    release = load_json(release_path)
    if release.get("release_id") != release_id:
        raise TrainingError(f"model release id mismatch: {release_id}")
    if release.get("schema") != "MODEL-RELEASE-V1":
        raise TrainingError(f"wrong model release schema: {release_id}")
    if release.get("base_source_manifest") != "sources/canonical-manifest.json":
        raise TrainingError(f"model release has the wrong base source manifest: {release_id}")
    if release.get("training_process_authority") != "config/training-policy.json":
        raise TrainingError(f"model release has the wrong process authority: {release_id}")
    if release.get("canonical_sources_mutated") is not False:
        raise TrainingError(f"model release may not mutate canonical sources: {release_id}")
    patches = release.get("patches")
    if not isinstance(patches, list) or len(set(patches)) != len(patches):
        raise TrainingError(f"invalid patch list in model release: {release_id}")
    patch_root = (root / "model-learning" / "patches").resolve()
    for relative_path in patches:
        if not isinstance(relative_path, str):
            raise TrainingError(f"invalid patch path in model release: {release_id}")
        patch_path = (root / relative_path).resolve()
        if not is_within(patch_root, patch_path) or not patch_path.is_file():
            raise TrainingError(
                f"model release patch is missing or outside model-learning/patches: {relative_path}"
            )
        patch = load_json(patch_path)
        if patch.get("schema") != "MODEL-LEARNING-PATCH-V1":
            raise TrainingError(f"wrong model learning patch schema: {relative_path}")
        if patch.get("contains_case_answer_mapping") is not False:
            raise TrainingError(f"model learning patch is not answer-isolated: {relative_path}")
        if patch.get("modifies_canonical_source_files") is not False:
            raise TrainingError(f"model learning patch attempts to mutate canonical sources: {relative_path}")
    parent_id = release.get("parent_release")
    if parent_id is None:
        if release_id != "MODEL-BASELINE-001" or patches:
            raise TrainingError("only an empty MODEL-BASELINE-001 may be a root release")
    else:
        if not isinstance(parent_id, str):
            raise TrainingError(f"invalid parent model release: {release_id}")
        parent = _validate_release_chain(root, parent_id, seen)
        if not patches or patches[:-1] != parent["patches"]:
            raise TrainingError(f"model release must append exactly one patch: {release_id}")
        latest_patch = load_json(root / patches[-1])
        if release.get("latest_patch_sha256") != object_sha256(latest_patch):
            raise TrainingError(f"latest patch hash mismatch: {release_id}")
    return release


def _validate_state(root: Path, state: dict[str, Any], group: dict[str, Any]) -> None:
    case_order = group["case_order"]
    index = state.get("current_case_index")
    if not isinstance(index, int) or index < 0 or index > len(case_order):
        raise TrainingError("invalid current_case_index")
    if state.get("status") == "GROUP_COMPLETE":
        if index != len(case_order):
            raise TrainingError("GROUP_COMPLETE requires every case to be finished")
    elif index >= len(case_order):
        raise TrainingError("non-complete state must have a current case")
    rounds: list[str] = []
    for case_id in case_order:
        case_state = state["cases"][case_id]
        if not isinstance(case_state.get("round_ids"), list):
            raise TrainingError(f"invalid round list for {case_id}")
        streak = case_state.get("consecutive_passes")
        if not isinstance(streak, int) or streak < 0 or streak > 3:
            raise TrainingError(f"invalid consecutive pass count for {case_id}")
        rounds.extend(case_state["round_ids"])
    if len(rounds) != len(set(rounds)):
        raise TrainingError("a round id appears more than once")
    if state.get("round_count") != len(rounds):
        raise TrainingError("round_count does not match the case round lists")
    for round_id in rounds:
        if not (root / "training" / "runs" / round_id / "round.json").is_file():
            raise TrainingError(f"state references a missing round: {round_id}")
    active_round = state.get("active_round_id")
    needs_active = state.get("status") in {"AWAITING_PREDICTION_FREEZE", "PREDICTION_FROZEN"}
    if needs_active != isinstance(active_round, str):
        raise TrainingError("active_round_id does not match the training status")
    if isinstance(active_round, str) and active_round not in rounds:
        raise TrainingError("active_round_id is absent from the round lists")


def verify_repository(root: Path, *, require_answers: bool = False) -> dict[str, Any]:
    root = root.resolve()
    policy = load_and_validate_policy(root / "config" / "training-policy.json")
    source_policy = _validate_source_policy(root)
    _validate_answer_policy(root)
    expected_manifest = build_source_manifest(root)
    manifest = load_json(root / "sources" / "canonical-manifest.json")
    if source_policy["canonical_manifest_sha256"] != object_sha256(manifest):
        raise TrainingError("canonical source manifest lock hash changed")
    if manifest != expected_manifest:
        raise TrainingError(
            "canonical S00-S19 changed or sources/canonical-manifest.json is not the frozen lock"
        )

    group = load_json(root / "examples" / "DEV-GROUP-002" / "group.json")
    case_order = group.get("case_order")
    cases = group.get("cases")
    if not isinstance(case_order, list) or len(case_order) != 5 or len(set(case_order)) != 5:
        raise TrainingError("the clean baseline must contain exactly five ordered cases")
    if not isinstance(cases, dict) or set(cases) != set(case_order):
        raise TrainingError("group case mapping does not match case order")
    question_counts = {case_id: _validate_case(root, case_id, cases[case_id]) for case_id in case_order}

    release = load_json(root / "model-learning" / "releases" / "MODEL-BASELINE-001.json")
    if release.get("patches") != [] or release.get("parent_release") is not None:
        raise TrainingError("baseline model release must not contain learning patches")

    state = load_json(root / "training" / "state.json")
    if state.get("group_id") != group.get("group_id"):
        raise TrainingError("training state group mismatch")
    if state.get("round_limit") is not None or policy.get("round_limit") is not None:
        raise TrainingError("training rounds must be unlimited")
    if state.get("source_manifest_path") != "sources/canonical-manifest.json":
        raise TrainingError("training state must bind the frozen Git canonical manifest")
    current_release = state.get("current_model_release")
    if not isinstance(current_release, str) or not (
        root / "model-learning" / "releases" / f"{current_release}.json"
    ).is_file():
        raise TrainingError("training state points to a missing model release")
    if state.get("round_count") == 0 and current_release != "MODEL-BASELINE-001":
        raise TrainingError("an unused clean state must begin at MODEL-BASELINE-001")
    if set(state.get("cases", {})) != set(case_order):
        raise TrainingError("training state case set mismatch")
    _validate_state(root, state, group)
    _validate_release_chain(root, current_release)

    encrypted_dir = root / "answer-vault" / "encrypted"
    answer_count = sum((encrypted_dir / f"{case_id}.json.fernet").is_file() for case_id in case_order)
    if require_answers and answer_count != len(case_order):
        raise TrainingError(f"formal training requires {len(case_order)} encrypted answers; found {answer_count}")

    return {
        "status": "PASS",
        "sources": expected_manifest["source_count"],
        "runtime_source": "GIT_REPOSITORY_ONLY",
        "canonical_sources_immutable": True,
        "model_learning_separate": True,
        "cases": len(case_order),
        "questions": sum(question_counts.values()),
        "answer_envelopes": answer_count,
        "answer_envelopes_required": len(case_order),
        "preloaded_encrypted_answers_ready": answer_count == len(case_order),
        "external_post_freeze_answer_supported": True,
        "controller_ready": True,
        "round_limit": None,
        "consecutive_passes_required": 3,
    }
