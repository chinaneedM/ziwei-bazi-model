from __future__ import annotations

from pathlib import Path
from typing import Any

from .prediction import freeze_prediction, validate_prediction_run
from .snapshot import _contains_forbidden
from .util import FortuneError, atomic_write_json, read_json, sha256_file, slug, utc_now


ALLOWED_SESSION_MODES = {"CHAT_ONLY", "WORK"}
RUNNER_ID = "CHAT-WORK-HANDOFF-V1"
HANDOFF_SCHEMA = "CHAT-WORK-PREDICTION-HANDOFF-RECEIPT-V1"


def import_chat_work_prediction(run_path: str | Path, contract_path: str | Path,
                                output_path: str | Path, receipt_path: str | Path,
                                session_mode: str, session_id: str) -> dict[str, Any]:
    """Validate and materialize a prediction produced in a ChatGPT CHAT/WORK session.

    GitHub never starts or impersonates the model. The project session performs
    the dual-track reasoning, then hands a complete PREDICTION-RUN-V1 object to
    this deterministic adapter. The adapter enforces answer isolation, bindings,
    object completeness and non-overwrite before the prediction can be frozen.
    """
    if session_mode not in ALLOWED_SESSION_MODES:
        raise FortuneError(
            f"unsupported session mode: {session_mode}",
            status="CHAT_WORK_SESSION_MODE_INVALID",
        )
    if not session_id or not session_id.strip():
        raise FortuneError("session id is required", status="CHAT_WORK_SESSION_ID_INVALID")

    run_path = Path(run_path)
    contract_path = Path(contract_path)
    run = read_json(run_path)
    contract = read_json(contract_path)

    if contract.get("answer_data_available") is not False:
        raise FortuneError(
            "run contract does not attest answer isolation",
            status="CHAT_WORK_ANSWER_ISOLATION_FAILED",
        )
    findings = _contains_forbidden(run)
    if findings:
        raise FortuneError(
            "forbidden answer material detected in prediction: " + ";".join(findings),
            status="CHAT_WORK_ANSWER_LEAK_DETECTED",
        )

    validation = validate_prediction_run(run, contract)
    if validation.get("status") != "PASS":
        raise FortuneError(
            "CHAT/WORK prediction failed local validation: "
            + ";".join(validation.get("errors", [])),
            status="CHAT_WORK_PREDICTION_FAILED",
        )

    run["execution_context"] = {
        "runner_id": RUNNER_ID,
        "session_mode": session_mode,
        "session_id": session_id.strip(),
        "interaction_model": "USER_INITIATED_CHATGPT_PROJECT_SESSION",
        "background_execution": False,
        "api_service_required": False,
        "answer_data_available": False,
        "imported_at": utc_now(),
    }
    run["runtime_validation"] = validation
    atomic_write_json(output_path, run)

    receipt = {
        "schema": HANDOFF_SCHEMA,
        "status": "PASS",
        "runner_id": RUNNER_ID,
        "run_id": slug(run["run_id"]),
        "case_id": run["case_id"],
        "binding": run["binding"],
        "session_mode": session_mode,
        "session_id": session_id.strip(),
        "interaction_model": "USER_INITIATED_CHATGPT_PROJECT_SESSION",
        "api_service_required": False,
        "background_execution": False,
        "source_prediction_path": str(run_path),
        "source_prediction_sha256": sha256_file(run_path),
        "prediction_path": str(output_path),
        "prediction_sha256": sha256_file(output_path),
        "contract_path": str(contract_path),
        "contract_sha256": sha256_file(contract_path),
        "no_answer_access_proof": {
            "answer_data_available": False,
            "prediction_forbidden_scan": "PASS",
            "contract_answer_isolation": "PASS",
            "runtime_repository_vault_credential": "NONE",
        },
        "prediction_run_validation": validation,
        "ziwei_bazi_independent_local_seals": "PASS",
        "run_id_nonoverwrite": True,
        "completed_at": utc_now(),
    }
    atomic_write_json(receipt_path, receipt)
    return receipt


def validate_chat_work_handoff(run_path: str | Path, contract_path: str | Path,
                               receipt_path: str | Path) -> dict[str, Any]:
    run_file = Path(run_path)
    contract_file = Path(contract_path)
    receipt_file = Path(receipt_path)
    if not receipt_file.is_file():
        raise FortuneError("CHAT/WORK handoff receipt is missing", status="HANDOFF_RECEIPT_MISSING")

    run = read_json(run_file)
    receipt = read_json(receipt_file)
    errors: list[str] = []
    if receipt.get("schema") != HANDOFF_SCHEMA:
        errors.append("HANDOFF_SCHEMA_INVALID")
    if receipt.get("status") != "PASS" or receipt.get("runner_id") != RUNNER_ID:
        errors.append("HANDOFF_STATUS_INVALID")
    if receipt.get("run_id") != slug(run.get("run_id", "")):
        errors.append("HANDOFF_RUN_ID_MISMATCH")
    if receipt.get("case_id") != run.get("case_id"):
        errors.append("HANDOFF_CASE_ID_MISMATCH")
    if receipt.get("binding") != run.get("binding"):
        errors.append("HANDOFF_BINDING_MISMATCH")
    if receipt.get("prediction_sha256") != sha256_file(run_file):
        errors.append("HANDOFF_PREDICTION_HASH_MISMATCH")
    if receipt.get("contract_sha256") != sha256_file(contract_file):
        errors.append("HANDOFF_CONTRACT_HASH_MISMATCH")
    proof = receipt.get("no_answer_access_proof", {})
    if proof.get("answer_data_available") is not False:
        errors.append("HANDOFF_ANSWER_ISOLATION_INVALID")
    if proof.get("prediction_forbidden_scan") != "PASS":
        errors.append("HANDOFF_FORBIDDEN_SCAN_INVALID")
    if receipt.get("prediction_run_validation", {}).get("status") != "PASS":
        errors.append("HANDOFF_RUNTIME_VALIDATION_INVALID")
    if errors:
        raise FortuneError(
            "CHAT/WORK handoff validation failed: " + ";".join(errors),
            status="HANDOFF_RECEIPT_INVALID",
        )
    return {
        "schema": "CHAT-WORK-HANDOFF-VALIDATION-V1",
        "status": "PASS",
        "run_id": receipt["run_id"],
        "case_id": receipt["case_id"],
        "handoff_receipt_path": str(receipt_file),
        "handoff_receipt_sha256": sha256_file(receipt_file),
        "prediction_sha256": receipt["prediction_sha256"],
        "contract_sha256": receipt["contract_sha256"],
    }


def freeze_chat_work_prediction(run_path: str | Path, contract_path: str | Path,
                                handoff_receipt_path: str | Path,
                                frozen_root: str | Path) -> dict[str, Any]:
    origin_validation = validate_chat_work_handoff(
        run_path, contract_path, handoff_receipt_path
    )
    receipt = freeze_prediction(run_path, contract_path, frozen_root)
    receipt["prediction_origin"] = "CHAT_WORK_HANDOFF_VERIFIED"
    receipt["handoff_receipt_path"] = str(handoff_receipt_path)
    receipt["handoff_receipt_sha256"] = origin_validation["handoff_receipt_sha256"]
    receipt["origin_validation"] = origin_validation
    receipt_path = Path(frozen_root) / receipt["run_id"] / "freeze-receipt.json"
    receipt_path.chmod(0o644)
    atomic_write_json(receipt_path, receipt, overwrite=True)
    receipt_path.chmod(0o444)
    return receipt
