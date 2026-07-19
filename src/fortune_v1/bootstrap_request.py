from __future__ import annotations

from pathlib import Path
from typing import Any

from .clean_start import (
    CURRENT_GROUP_POINTER_SCHEMA,
    create_group_clean_start,
    create_group_clean_start_from_request,
)
from .util import FortuneError, atomic_write_json, read_json, sha256_file, slug, utc_now

PREAUTHORIZED_REQUEST_SCHEMA = "GROUP-CLEAN-START-REQUEST-V2"
PREAUTHORIZED_REQUEST_ORIGIN = "PREAUTHORIZED_ENGINEERING_BOOTSTRAP"


def _require_file(path: str | Path, *, status: str) -> Path:
    candidate = Path(path)
    if not candidate.is_file():
        raise FortuneError(f"required file missing: {candidate}", status=status)
    return candidate


def _exact_identifier(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise FortuneError(f"missing {field}", status="CLEAN_START_REQUEST_INVALID")
    normalized = slug(value)
    if normalized != value:
        raise FortuneError(f"unsafe {field}", status="CLEAN_START_REQUEST_INVALID")
    return value


def _validate_pointer(pointer: dict[str, Any]) -> None:
    if pointer.get("schema") != CURRENT_GROUP_POINTER_SCHEMA or pointer.get("status") != "ACTIVE":
        raise FortuneError("invalid current group pointer", status="CURRENT_GROUP_POINTER_INVALID")
    if pointer.get("answer_payload_present") is not False:
        raise FortuneError("pointer contains answer payload", status="GROUP_ANSWER_ISOLATION_FAILED")
    if pointer.get("runtime_answer_scan") != "PASS":
        raise FortuneError("pointer answer scan failed", status="GROUP_ANSWER_ISOLATION_FAILED")
    if pointer.get("answer_vault_location_outside_reasoning_context") is not True:
        raise FortuneError("answer vault boundary not established", status="ANSWER_VAULT_ACCESS_TEST_FAILED")


def build_preauthorized_request(
    current_group_pointer_path: str | Path,
    output_path: str | Path,
    group_run_id: str,
    session_id: str,
    mode: str = "CHAT_ONLY",
) -> dict[str, Any]:
    """Materialize a request before the prediction context starts.

    This removes the impossible requirement that a fresh prediction chat must first
    discover hidden pointer fields and yet must not read the repository before the
    request exists.
    """

    pointer_file = _require_file(current_group_pointer_path, status="CURRENT_GROUP_MANIFEST_MISSING")
    pointer = read_json(pointer_file)
    _validate_pointer(pointer)
    exact_group_run_id = _exact_identifier(group_run_id, "group_run_id")
    exact_session_id = _exact_identifier(session_id, "session_id")
    if mode not in {"CHAT_ONLY", "WORK"}:
        raise FortuneError("invalid session mode", status="GROUP_SESSION_MODE_INVALID")

    request = {
        "schema": PREAUTHORIZED_REQUEST_SCHEMA,
        "status": "REQUESTED",
        "request_origin": PREAUTHORIZED_REQUEST_ORIGIN,
        "group_run_id": exact_group_run_id,
        "session_id": exact_session_id,
        "mode": mode,
        "prediction_context_started": False,
        "prediction_context_repository_search_used": False,
        "prediction_context_commit_history_used": False,
        "prediction_context_old_run_objects_visible": False,
        "pointer_path": str(pointer_file),
        "pointer_sha256": sha256_file(pointer_file),
        "requested_group_id": pointer["group_id"],
        "allowed_repository": pointer["allowed_repository"],
        "forbidden_repository": pointer["forbidden_repository"],
        "answer_vault_access_basis": "SINGLE_ALLOWED_REPOSITORY_CHECKOUT_PLUS_ACTIVE_POINTER",
        "future_prediction_entrypoint": str(Path(pointer["output_root"]) / exact_group_run_id / "clean-start.json"),
        "future_prediction_first_repository_action": "FETCH_EXACT_CLEAN_START_PATH_ONLY",
        "created_at": utc_now(),
    }
    target = atomic_write_json(output_path, request)
    return {
        **request,
        "request_path": str(target),
        "request_sha256": sha256_file(target),
    }


def create_group_clean_start_from_bootstrap_request(
    request_path: str | Path,
    current_group_pointer_path: str | Path = "CURRENT_GROUP_MANIFEST",
) -> dict[str, Any]:
    request_file = _require_file(request_path, status="CLEAN_START_REQUEST_MISSING")
    request = read_json(request_file)

    if request.get("schema") != PREAUTHORIZED_REQUEST_SCHEMA:
        return create_group_clean_start_from_request(request_file, current_group_pointer_path)

    pointer_file = _require_file(current_group_pointer_path, status="CURRENT_GROUP_MANIFEST_MISSING")
    pointer = read_json(pointer_file)
    _validate_pointer(pointer)

    if request.get("status") != "REQUESTED":
        raise FortuneError("invalid clean start request", status="CLEAN_START_REQUEST_INVALID")
    if request.get("request_origin") != PREAUTHORIZED_REQUEST_ORIGIN:
        raise FortuneError("invalid request origin", status="CLEAN_START_REQUEST_INVALID")
    if request.get("prediction_context_started") is not False:
        raise FortuneError("prediction context already started", status="FAIL_CLOSED_CONTAMINATED")
    if request.get("prediction_context_repository_search_used") is not False:
        raise FortuneError("prediction context repository search used", status="FAIL_CLOSED_CONTAMINATED")
    if request.get("prediction_context_commit_history_used") is not False:
        raise FortuneError("prediction context commit history used", status="FAIL_CLOSED_CONTAMINATED")
    if request.get("prediction_context_old_run_objects_visible") is not False:
        raise FortuneError("prediction context old run objects visible", status="FAIL_CLOSED_CONTAMINATED")

    if request.get("requested_group_id") != pointer.get("group_id"):
        raise FortuneError("request group mismatch", status="CLEAN_START_REQUEST_GROUP_MISMATCH")
    if request.get("allowed_repository") != pointer.get("allowed_repository"):
        raise FortuneError("allowed repository mismatch", status="CLEAN_START_REQUEST_REPOSITORY_MISMATCH")
    if request.get("forbidden_repository") != pointer.get("forbidden_repository"):
        raise FortuneError("forbidden repository mismatch", status="CLEAN_START_REQUEST_REPOSITORY_MISMATCH")
    if request.get("pointer_sha256") != sha256_file(pointer_file):
        raise FortuneError("pointer changed after request authorization", status="CLEAN_START_REQUEST_POINTER_MISMATCH")

    group_run_id = _exact_identifier(request.get("group_run_id"), "group_run_id")
    session_id = _exact_identifier(request.get("session_id"), "session_id")
    session_mode = request.get("mode", "CHAT_ONLY")
    if session_mode not in {"CHAT_ONLY", "WORK"}:
        raise FortuneError("invalid session mode", status="GROUP_SESSION_MODE_INVALID")

    mandatory_paths: list[str | Path] = [pointer_file]
    mandatory_paths.extend(pointer.get("mandatory_initial_paths", []))
    mandatory_paths.append(request_file)

    bootstrap_receipt = {
        "path": str(pointer_file),
        "sha256": sha256_file(pointer_file),
        "schema": pointer["schema"],
        "status": pointer["status"],
        "bootstrap_mode": "PREAUTHORIZED_BEFORE_PREDICTION_CONTEXT",
    }
    request_receipt = {
        "path": str(request_file),
        "sha256": sha256_file(request_file),
        "schema": request["schema"],
        "request_origin": request["request_origin"],
        "answer_vault_physical_access_test_status": "PASS_INACCESSIBLE_BY_REPOSITORY_BOUNDARY",
        "precontent_search_status": "PASS_PREDICTION_CONTEXT_NOT_STARTED",
        "old_run_visibility_status": "PASS_PREDICTION_CONTEXT_NOT_STARTED",
        "future_prediction_first_repository_action": "FETCH_EXACT_CLEAN_START_PATH_ONLY",
    }
    runtime_binding = {
        "main_prompt_runtime_id": pointer["main_prompt_runtime_id"],
        "knowledge_release_id": pointer["active_knowledge_release_id"],
        "method_release_id": pointer["active_method_release_id"],
        "model_release_id": pointer["active_model_release_id"],
        "learning_policy_id": pointer["active_learning_policy_id"],
    }
    return create_group_clean_start(
        pointer["group_manifest_path"],
        pointer["install_state_path"],
        pointer["output_root"],
        group_run_id,
        session_id,
        session_mode,
        initial_control_paths=mandatory_paths,
        bootstrap_receipt=bootstrap_receipt,
        request_receipt=request_receipt,
        runtime_binding=runtime_binding,
    )
