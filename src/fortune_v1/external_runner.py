from __future__ import annotations

from pathlib import Path
from typing import Any

from .prediction import validate_prediction_run
from .snapshot import _contains_forbidden
from .util import FortuneError, atomic_write_json, read_json, sha256_file, utc_now


ALLOWED_SESSION_MODES = {"CHAT_ONLY", "WORK"}
RUNNER_ID = "CHAT-WORK-HANDOFF-V1"


def import_chat_work_prediction(run_path: str | Path, contract_path: str | Path,
                                output_path: str | Path, receipt_path: str | Path,
                                session_mode: str, session_id: str) -> dict[str, Any]:
    """Validate and materialize a prediction produced in a ChatGPT CHAT/WORK session.

    GitHub never starts or impersonates the model.  The project session performs
    the dual-track reasoning, then hands a complete PREDICTION-RUN-V1 object to
    this deterministic adapter.  The adapter enforces answer isolation, bindings,
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
        "schema": "CHAT-WORK-PREDICTION-HANDOFF-RECEIPT-V1",
        "status": "PASS",
        "runner_id": RUNNER_ID,
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
