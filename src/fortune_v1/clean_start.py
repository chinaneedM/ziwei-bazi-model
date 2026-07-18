from __future__ import annotations

from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, read_json, sha256_file, slug, utc_now

CLEAN_START_SCHEMA = "GROUP-CLEAN-START-V1"
SKELETON_SCHEMA = "PREDICTION-RUN-V1"
REQUEST_SCHEMA = "GROUP-CLEAN-START-REQUEST-V1"
CURRENT_GROUP_POINTER_SCHEMA = "CURRENT-GROUP-MANIFEST-POINTER-V1"

FORBIDDEN_PREFIXES = [
    ".git/",
    "data/group-reveals/",
    "data/reveals/",
    "data/runs/",
    "data/chat-work-candidates/",
    "reports/relative-replay/",
    "reports/diagnosis/",
    "reports/shadow-rebuild/",
    "training-history/",
]
FORBIDDEN_RESOURCE_TYPES = [
    "pull_request",
    "issue",
    "commit_history",
    "prior_prediction",
    "prior_reveal",
    "grading_result",
    "diagnosis",
    "shadow_rebuild",
]


def _exact_identifier(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise FortuneError(f"missing {field}", status="CLEAN_START_REQUEST_INVALID")
    normalized = slug(value)
    if normalized != value:
        raise FortuneError(f"unsafe {field}", status="CLEAN_START_REQUEST_INVALID")
    return value


def _require_file(path: str | Path, *, status: str) -> Path:
    candidate = Path(path)
    if not candidate.is_file():
        raise FortuneError(f"required file missing: {candidate}", status=status)
    return candidate


def _unique_paths(paths: list[str | Path]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in paths:
        text = str(Path(value))
        if text not in seen:
            seen.add(text)
            output.append(text)
    return output


def _question_skeleton(question: dict[str, Any]) -> dict[str, Any]:
    option_ids = [row["option_id"] for row in question["options"]]
    pairwise = []
    for i, left in enumerate(option_ids):
        for right in option_ids[i + 1:]:
            pairwise.append({
                "left": left,
                "right": right,
                "winner": None,
                "decision_basis": None,
                "distinctive_atom_comparison": {},
            })
    return {
        "question_id": question["question_id"],
        "option_ids": option_ids,
        "top1": None,
        "top2": None,
        "confidence": None,
        "blind_core": None,
        "public_evidence": [],
        "ziwei_track": {},
        "bazi_track": {},
        "evidence_ledger": [],
        "coverage_plan": {
            "status": "INCOMPLETE",
            "distinctive_atom_rows": [],
            "required_source_family_rows": [],
            "actual_route_rows": [],
            "unresolved_required_routes": ["NOT_YET_EXECUTED"],
        },
        "direction_matrix": {option_id: [] for option_id in option_ids},
        "compound_coverage": {option_id: {} for option_id in option_ids},
        "pairwise_rows": pairwise,
        "strongest_competitor_reason": None,
        "most_important_unverified_atom": None,
        "formal_exact_assertion": None,
    }


def create_group_clean_start(
    group_manifest_path: str | Path,
    install_state_path: str | Path,
    output_root: str | Path,
    group_run_id: str,
    session_id: str,
    session_mode: str = "CHAT_ONLY",
    *,
    initial_control_paths: list[str | Path] | None = None,
    bootstrap_receipt: dict[str, Any] | None = None,
    request_receipt: dict[str, Any] | None = None,
) -> dict[str, Any]:
    group_manifest_file = _require_file(group_manifest_path, status="GROUP_MANIFEST_MISSING")
    install_state_file = _require_file(install_state_path, status="INSTALL_STATE_MISSING")
    exact_group_run_id = _exact_identifier(group_run_id, "group_run_id")
    exact_session_id = _exact_identifier(session_id, "session_id")
    output_dir = Path(output_root) / exact_group_run_id
    if output_dir.exists():
        raise FortuneError("clean start output already exists", status="GROUP_RUN_NONOVERWRITE_FAILED")
    group = read_json(group_manifest_file)
    install_state = read_json(install_state_file)
    if group.get("status") != "READY_FOR_BASELINE_PREDICTION":
        raise FortuneError("group is not ready", status="GROUP_NOT_READY")
    if group.get("answer_payload_present") is not False or group.get("runtime_answer_scan") != "PASS":
        raise FortuneError("group answer isolation failed", status="GROUP_ANSWER_ISOLATION_FAILED")
    if install_state.get("status") != "INSTALLED_VALIDATED":
        raise FortuneError("runtime installation is not validated", status="INSTALLATION_NOT_VALIDATED")
    if session_mode not in {"CHAT_ONLY", "WORK"}:
        raise FortuneError("invalid session mode", status="GROUP_SESSION_MODE_INVALID")

    control_paths: list[str | Path] = []
    for path in initial_control_paths or []:
        control_paths.append(_require_file(path, status="BOOTSTRAP_CONTROL_PATH_MISSING"))

    output_dir.mkdir(parents=True, exist_ok=False)
    skeleton_dir = output_dir / "case-skeletons"
    skeleton_dir.mkdir()
    cases = []
    exact_allowed_paths = _unique_paths([*control_paths, group_manifest_file, install_state_file])

    for row in group["cases"]:
        case_path = _require_file(row["path"], status="CASE_INPUT_MISSING")
        case = read_json(case_path)
        if case.get("answer_isolation", {}).get("answer_payload_present") is not False:
            raise FortuneError("case answer isolation failed", status="CASE_ANSWER_ISOLATION_FAILED")
        case_run_id = f"{exact_group_run_id}-{slug(case['case_id'])}"
        skeleton = {
            "schema": SKELETON_SCHEMA,
            "case_id": case["case_id"],
            "dataset_type": case["dataset_type"],
            "run_id": case_run_id,
            "binding": case["binding"],
            "cold_start": True,
            "input_snapshot": {"path": str(case_path), "sha256": sha256_file(case_path)},
            "answer_data_available": False,
            "questions": [_question_skeleton(q) for q in case["questions"]["parsed"]],
            "status": "EMPTY_SKELETON_NOT_VALID_FOR_FREEZE",
        }
        skeleton_path = skeleton_dir / f"{case['case_id']}.json"
        atomic_write_json(skeleton_path, skeleton)
        exact_allowed_paths = _unique_paths([*exact_allowed_paths, case_path, skeleton_path])
        cases.append({
            "case_id": case["case_id"],
            "case_run_id": case_run_id,
            "input_path": str(case_path),
            "input_sha256": sha256_file(case_path),
            "skeleton_path": str(skeleton_path),
            "skeleton_sha256": sha256_file(skeleton_path),
        })

    manifest = {
        "schema": CLEAN_START_SCHEMA,
        "group_id": group["group_id"],
        "group_run_id": exact_group_run_id,
        "group_session_id": exact_session_id,
        "session_mode": session_mode,
        "installation_state": {
            "path": str(install_state_file),
            "sha256": sha256_file(install_state_file),
            "code_commit": install_state["code_commit"],
            "status": install_state["status"],
        },
        "group_manifest": {
            "path": str(group_manifest_file),
            "sha256": sha256_file(group_manifest_file),
            "case_count": group["case_count"],
            "question_count_total": group["question_count_total"],
        },
        "bootstrap_receipt": bootstrap_receipt,
        "start_request_receipt": request_receipt,
        "cases": cases,
        "retrieval_policy": {
            "mode": "EXACT_PATH_ONLY",
            "exact_allowed_paths": exact_allowed_paths,
            "repository_search_allowed": False,
            "history_navigation_allowed": False,
            "forbidden_path_prefixes": FORBIDDEN_PREFIXES,
            "forbidden_resource_types": FORBIDDEN_RESOURCE_TYPES,
        },
        "contamination_policy": {
            "on_forbidden_visibility": "FAIL_CLOSED",
            "public_relative_prediction": None,
            "formal_exact_assertion": None,
            "group_freeze": "NOT_PERFORMED",
            "group_reveal": "NOT_PERFORMED",
        },
        "answer_data_available": False,
        "status": "READY_FOR_CLEAN_GROUP_PREDICTION",
        "created_at": utc_now(),
    }
    manifest_path = output_dir / "clean-start.json"
    atomic_write_json(manifest_path, manifest)
    return {**manifest, "clean_start_path": str(manifest_path), "clean_start_sha256": sha256_file(manifest_path)}


def create_group_clean_start_from_request(
    request_path: str | Path,
    current_group_pointer_path: str | Path = "CURRENT_GROUP_MANIFEST",
) -> dict[str, Any]:
    request_file = _require_file(request_path, status="CLEAN_START_REQUEST_MISSING")
    pointer_file = _require_file(current_group_pointer_path, status="CURRENT_GROUP_MANIFEST_MISSING")
    request = read_json(request_file)
    pointer = read_json(pointer_file)

    if request.get("schema") != REQUEST_SCHEMA or request.get("status") != "REQUESTED":
        raise FortuneError("invalid clean start request", status="CLEAN_START_REQUEST_INVALID")
    if pointer.get("schema") != CURRENT_GROUP_POINTER_SCHEMA or pointer.get("status") != "ACTIVE":
        raise FortuneError("invalid current group pointer", status="CURRENT_GROUP_POINTER_INVALID")
    if request.get("requested_group_id") != pointer.get("group_id"):
        raise FortuneError("request group mismatch", status="CLEAN_START_REQUEST_GROUP_MISMATCH")
    if request.get("allowed_repository") != pointer.get("allowed_repository"):
        raise FortuneError("allowed repository mismatch", status="CLEAN_START_REQUEST_REPOSITORY_MISMATCH")
    if request.get("forbidden_repository") != pointer.get("forbidden_repository"):
        raise FortuneError("forbidden repository mismatch", status="CLEAN_START_REQUEST_REPOSITORY_MISMATCH")
    if request.get("answer_vault_physical_access_test_status") != "PASS_INACCESSIBLE":
        raise FortuneError("answer vault is not physically inaccessible", status="ANSWER_VAULT_ACCESS_TEST_FAILED")
    if request.get("repository_search_used_before_request") is not False:
        raise FortuneError("repository search contaminated request", status="FAIL_CLOSED_CONTAMINATED")
    if request.get("commit_history_used_before_request") is not False:
        raise FortuneError("commit history contaminated request", status="FAIL_CLOSED_CONTAMINATED")
    if request.get("old_run_objects_visible_before_request") is not False:
        raise FortuneError("old run objects contaminated request", status="FAIL_CLOSED_CONTAMINATED")

    group_run_id = _exact_identifier(request.get("group_run_id"), "group_run_id")
    session_id = _exact_identifier(request.get("session_id"), "session_id")
    session_mode = request.get("mode", "CHAT_ONLY")
    mandatory_paths = [pointer_file]
    mandatory_paths.extend(pointer.get("mandatory_initial_paths", []))
    mandatory_paths.append(request_file)

    bootstrap_receipt = {
        "path": str(pointer_file),
        "sha256": sha256_file(pointer_file),
        "schema": pointer["schema"],
        "status": pointer["status"],
    }
    request_receipt = {
        "path": str(request_file),
        "sha256": sha256_file(request_file),
        "schema": request["schema"],
        "answer_vault_physical_access_test_status": request["answer_vault_physical_access_test_status"],
        "precontent_search_status": "PASS_NOT_USED",
        "old_run_visibility_status": "PASS_NOT_VISIBLE",
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
    )


def record_group_contamination(clean_start_path: str | Path, output_path: str | Path,
                               resource_type: str, resource_reference: str) -> dict[str, Any]:
    clean = read_json(clean_start_path)
    receipt = {
        "schema": "GROUP-CONTAMINATION-RECEIPT-V1",
        "group_id": clean["group_id"],
        "group_run_id": clean["group_run_id"],
        "resource_type": resource_type,
        "resource_reference": resource_reference,
        "public_relative_prediction": None,
        "formal_exact_assertion": None,
        "group_freeze": "NOT_PERFORMED",
        "group_reveal": "NOT_PERFORMED",
        "restart_required": True,
        "status": "FAIL_CLOSED_CONTAMINATED",
        "recorded_at": utc_now(),
    }
    atomic_write_json(output_path, receipt)
    return receipt
