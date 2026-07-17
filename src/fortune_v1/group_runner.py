from __future__ import annotations

from pathlib import Path
from typing import Any

from .external_runner import freeze_chat_work_prediction, import_chat_work_prediction
from .group import authorize_group_reveal
from .scoring import validate_freeze_receipt
from .snapshot import _contains_forbidden
from .util import FortuneError, atomic_write_json, read_json, sha256_file, slug, utc_now


GROUP_RUN_SCHEMA = "GROUP-TRAINING-RUN-V1"
GROUP_FREEZE_SCHEMA = "GROUP-PREDICTION-FREEZE-V1"
ALLOWED_SESSION_MODES = {"CHAT_ONLY", "WORK"}


def _load_group_head(group_root: Path) -> tuple[dict[str, Any], Path]:
    pointer_path = group_root / "HEAD.json"
    if not pointer_path.is_file():
        raise FortuneError("group HEAD is missing", status="GROUP_HEAD_MISSING")
    pointer = read_json(pointer_path)
    head_path = Path(pointer.get("path", ""))
    if not head_path.is_absolute():
        if not head_path.is_file():
            head_path = group_root / "revisions" / head_path.name
    if not head_path.is_file():
        raise FortuneError("group revision is missing", status="GROUP_HEAD_INVALID")
    return read_json(head_path), head_path


def _validate_manifest(manifest: dict[str, Any], group: dict[str, Any], group_run_id: str,
                       session_id: str, session_mode: str) -> list[dict[str, Any]]:
    if manifest.get("schema") != GROUP_RUN_SCHEMA:
        raise FortuneError("group run manifest schema invalid", status="GROUP_RUN_SCHEMA_INVALID")
    if manifest.get("group_id") != group.get("group_id"):
        raise FortuneError("group id mismatch", status="GROUP_ID_MISMATCH")
    if slug(str(manifest.get("group_run_id", ""))) != slug(group_run_id):
        raise FortuneError("group run id mismatch", status="GROUP_RUN_ID_MISMATCH")
    if manifest.get("session_id") != session_id:
        raise FortuneError("group session id mismatch", status="GROUP_SESSION_ID_MISMATCH")
    if manifest.get("session_mode") != session_mode:
        raise FortuneError("group session mode mismatch", status="GROUP_SESSION_MODE_MISMATCH")
    if manifest.get("answer_data_available") is not False:
        raise FortuneError("group manifest does not attest answer isolation", status="GROUP_ANSWER_ISOLATION_FAILED")
    findings = _contains_forbidden(manifest)
    if findings:
        raise FortuneError(
            "forbidden answer material detected in group manifest: " + ";".join(findings),
            status="GROUP_ANSWER_LEAK_DETECTED",
        )

    rows = manifest.get("case_runs")
    if not isinstance(rows, list):
        raise FortuneError("case_runs must be a list", status="GROUP_CASE_RUNS_INVALID")
    expected_case_ids = list(group.get("case_ids", []))
    row_case_ids = [row.get("case_id") for row in rows if isinstance(row, dict)]
    if len(rows) != len(expected_case_ids):
        raise FortuneError("partial group submission", status="PARTIAL_GROUP_SUBMISSION")
    if row_case_ids != expected_case_ids:
        raise FortuneError("case order or membership mismatch", status="GROUP_CASE_ORDER_MISMATCH")
    if len(set(row_case_ids)) != len(row_case_ids):
        raise FortuneError("duplicate case id", status="DUPLICATE_CASE_ID")

    run_ids = [slug(str(row.get("run_id", ""))) for row in rows]
    if any(not run_id for run_id in run_ids) or len(set(run_ids)) != len(run_ids):
        raise FortuneError("case run ids must be unique and non-empty", status="DUPLICATE_CASE_RUN_ID")
    return rows


def execute_group_handoff(manifest_path: str | Path, group_root: str | Path,
                          output_root: str | Path, session_mode: str,
                          session_id: str, group_run_id: str) -> dict[str, Any]:
    """Import and freeze every answer-free case run in one active CHAT/WORK session.

    The model still creates each complete PREDICTION-RUN-V1 child independently. This
    deterministic runner validates and freezes the ordered group without requiring a
    new conversation or a per-case continue command.
    """
    if session_mode not in ALLOWED_SESSION_MODES:
        raise FortuneError("unsupported session mode", status="GROUP_SESSION_MODE_INVALID")
    if not session_id.strip() or not group_run_id.strip():
        raise FortuneError("session and group run ids are required", status="GROUP_RUN_ID_INVALID")

    manifest_file = Path(manifest_path)
    group_dir = Path(group_root)
    output_dir = Path(output_root) / slug(group_run_id)
    if output_dir.exists():
        raise FortuneError("group run already exists", status="GROUP_RUN_NONOVERWRITE_FAILED")

    group, group_head_path = _load_group_head(group_dir)
    manifest = read_json(manifest_file)
    rows = _validate_manifest(manifest, group, group_run_id, session_id, session_mode)

    output_dir.mkdir(parents=True, exist_ok=False)
    case_results: list[dict[str, Any]] = []
    seen_source_paths: set[str] = set()

    for row in rows:
        case_id = str(row["case_id"])
        run_path = Path(row.get("run_path", ""))
        contract_path = Path(row.get("contract_path", ""))
        if not run_path.is_file() or not contract_path.is_file():
            raise FortuneError(f"case input missing: {case_id}", status="GROUP_CASE_INPUT_MISSING")
        source_key = f"{run_path.resolve()}::{contract_path.resolve()}"
        if source_key in seen_source_paths:
            raise FortuneError("duplicate case source paths", status="DUPLICATE_CASE_SOURCE")
        seen_source_paths.add(source_key)

        source_run = read_json(run_path)
        if source_run.get("case_id") != case_id:
            raise FortuneError("manifest and prediction case mismatch", status="CASE_ID_MISMATCH")
        if slug(str(source_run.get("run_id", ""))) != slug(str(row.get("run_id", ""))):
            raise FortuneError("manifest and prediction run mismatch", status="FREEZE_RUN_ID_MISMATCH")
        if source_run.get("binding") != group.get("frozen_binding"):
            raise FortuneError("group binding mismatch", status="DEV_GROUP_VERSION_MISMATCH")
        prior_case_refs = row.get("prior_case_object_refs", [])
        if prior_case_refs not in (None, []):
            raise FortuneError("later case references prior case objects", status="CROSS_CASE_CONTEXT_CONTAMINATION")

        case_dir = output_dir / slug(case_id)
        case_dir.mkdir(parents=True, exist_ok=False)
        imported_path = case_dir / "prediction.json"
        handoff_receipt_path = case_dir / "handoff-receipt.json"
        frozen_root = case_dir / "frozen"

        handoff = import_chat_work_prediction(
            run_path,
            contract_path,
            imported_path,
            handoff_receipt_path,
            session_mode,
            session_id,
        )
        freeze = freeze_chat_work_prediction(
            imported_path,
            contract_path,
            handoff_receipt_path,
            frozen_root,
        )
        validation = validate_freeze_receipt(
            frozen_root / freeze["run_id"] / "freeze-receipt.json",
            freeze["run_id"],
        )
        case_results.append({
            "case_id": case_id,
            "case_run_id": freeze["run_id"],
            "handoff_receipt_path": str(handoff_receipt_path),
            "handoff_receipt_sha256": sha256_file(handoff_receipt_path),
            "freeze_receipt_path": str(frozen_root / freeze["run_id"] / "freeze-receipt.json"),
            "freeze_receipt_sha256": validation["freeze_receipt_sha256"],
            "prediction_path": validation["prediction_path"],
            "prediction_sha256": validation["prediction_sha256"],
            "contract_path": validation["contract_path"],
            "contract_sha256": validation["contract_sha256"],
            "status": validation["status"],
            "prior_case_context_scan": "PASS",
        })

    freeze_object = {
        "schema": GROUP_FREEZE_SCHEMA,
        "group_id": group["group_id"],
        "group_run_id": slug(group_run_id),
        "group_session_id": session_id,
        "session_mode": session_mode,
        "expected_case_count": len(group["case_ids"]),
        "completed_case_count": len(case_results),
        "case_order": group["case_ids"],
        "case_runs": case_results,
        "group_binding": group["frozen_binding"],
        "group_head_path": str(group_head_path),
        "group_head_sha256": sha256_file(group_head_path),
        "source_manifest_path": str(manifest_file),
        "source_manifest_sha256": sha256_file(manifest_file),
        "answer_data_available_during_prediction": False,
        "partial_group_freeze": False,
        "cross_case_prediction_context": "ADMINISTRATIVE_ONLY",
        "status": "PASS_GROUP_FROZEN",
        "frozen_at": utc_now(),
    }
    freeze_path = output_dir / "group-freeze.json"
    atomic_write_json(freeze_path, freeze_object)
    freeze_path.chmod(0o444)
    return {**freeze_object, "group_freeze_path": str(freeze_path), "group_freeze_sha256": sha256_file(freeze_path)}


def validate_group_training_freeze(freeze_path: str | Path, expected_group_run_id: str | None = None) -> dict[str, Any]:
    path = Path(freeze_path)
    freeze = read_json(path)
    errors: list[str] = []
    if freeze.get("schema") != GROUP_FREEZE_SCHEMA:
        errors.append("GROUP_FREEZE_SCHEMA_INVALID")
    if freeze.get("status") != "PASS_GROUP_FROZEN":
        errors.append("GROUP_FREEZE_STATUS_INVALID")
    if expected_group_run_id and freeze.get("group_run_id") != slug(expected_group_run_id):
        errors.append("GROUP_RUN_ID_MISMATCH")
    rows = freeze.get("case_runs", [])
    if freeze.get("completed_case_count") != freeze.get("expected_case_count"):
        errors.append("PARTIAL_GROUP_FREEZE")
    if len(rows) != freeze.get("expected_case_count"):
        errors.append("PARTIAL_GROUP_FREEZE")
    case_ids = [row.get("case_id") for row in rows if isinstance(row, dict)]
    run_ids = [row.get("case_run_id") for row in rows if isinstance(row, dict)]
    if case_ids != freeze.get("case_order") or len(set(case_ids)) != len(case_ids):
        errors.append("GROUP_CASE_ORDER_MISMATCH")
    if len(set(run_ids)) != len(run_ids):
        errors.append("DUPLICATE_CASE_RUN_ID")
    for row in rows:
        receipt_path = row.get("freeze_receipt_path")
        if not receipt_path or not Path(receipt_path).is_file():
            errors.append("CASE_FREEZE_RECEIPT_MISSING")
            continue
        validation = validate_freeze_receipt(receipt_path, row.get("case_run_id"))
        if validation.get("freeze_receipt_sha256") != row.get("freeze_receipt_sha256"):
            errors.append("CASE_FREEZE_RECEIPT_HASH_MISMATCH")
        if validation.get("prediction_sha256") != row.get("prediction_sha256"):
            errors.append("CASE_PREDICTION_HASH_MISMATCH")
        if validation.get("contract_sha256") != row.get("contract_sha256"):
            errors.append("CASE_CONTRACT_HASH_MISMATCH")
    if errors:
        raise FortuneError("group freeze validation failed: " + ";".join(errors), status="GROUP_FREEZE_INVALID")
    return {
        "schema": "GROUP-PREDICTION-FREEZE-VALIDATION-V1",
        "group_id": freeze["group_id"],
        "group_run_id": freeze["group_run_id"],
        "case_count": len(rows),
        "group_freeze_path": str(path),
        "group_freeze_sha256": sha256_file(path),
        "status": "PASS",
    }
