from __future__ import annotations

from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, read_json, sha256_file, slug, utc_now

CLEAN_START_SCHEMA = "GROUP-CLEAN-START-V1"
SKELETON_SCHEMA = "PREDICTION-RUN-V1"

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


def create_group_clean_start(group_manifest_path: str | Path, install_state_path: str | Path,
                             output_root: str | Path, group_run_id: str,
                             session_id: str, session_mode: str = "CHAT_ONLY") -> dict[str, Any]:
    group_manifest_file = Path(group_manifest_path)
    install_state_file = Path(install_state_path)
    output_dir = Path(output_root) / slug(group_run_id)
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

    output_dir.mkdir(parents=True, exist_ok=False)
    skeleton_dir = output_dir / "case-skeletons"
    skeleton_dir.mkdir()
    cases = []
    exact_allowed_paths = [str(group_manifest_file), str(install_state_file)]

    for row in group["cases"]:
        case_path = Path(row["path"])
        case = read_json(case_path)
        if case.get("answer_isolation", {}).get("answer_payload_present") is not False:
            raise FortuneError("case answer isolation failed", status="CASE_ANSWER_ISOLATION_FAILED")
        case_run_id = f"{slug(group_run_id)}-{slug(case['case_id'])}"
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
        exact_allowed_paths.extend([str(case_path), str(skeleton_path)])
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
        "group_run_id": slug(group_run_id),
        "group_session_id": session_id,
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
