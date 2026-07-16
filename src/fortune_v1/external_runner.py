from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .prediction import validate_prediction_run
from .snapshot import _contains_forbidden
from .util import FortuneError, atomic_write_json, canonical_bytes, read_json, sha256_bytes, sha256_file, utc_now


def build_runner_request(snapshot_path: str | Path, contract_path: str | Path,
                         runner_id: str) -> dict[str, Any]:
    """Build the only payload an external prediction executor may receive.

    The payload is derived exclusively from the frozen no-answer snapshot and the
    immutable run contract.  It deliberately carries repository coordinates and
    hashes rather than any answer-vault path or credential.
    """
    snapshot_path = Path(snapshot_path)
    contract_path = Path(contract_path)
    snapshot = read_json(snapshot_path)
    contract = read_json(contract_path)

    if contract.get("answer_data_available") is not False:
        raise FortuneError(
            "run contract does not attest answer isolation",
            status="EXTERNAL_RUNNER_ANSWER_ISOLATION_FAILED",
        )
    if snapshot.get("answer_scan", {}).get("status") != "PASS":
        raise FortuneError(
            "prediction snapshot did not pass answer scan",
            status="EXTERNAL_RUNNER_ANSWER_ISOLATION_FAILED",
        )

    questions_path = Path(snapshot.get("questions_path", ""))
    if not questions_path.is_file():
        raise FortuneError(
            "snapshot question set is missing",
            status="EXTERNAL_RUNNER_INPUT_INVALID",
        )
    questions = read_json(questions_path)

    payload = {
        "schema": "EXTERNAL-PREDICTION-RUNNER-REQUEST-V1",
        "runner_id": runner_id,
        "created_at": utc_now(),
        "answer_data_available": False,
        "contract": contract,
        "snapshot": snapshot,
        "questions": questions,
        "repository_access": {
            "allowed_roots": ["knowledge/base"],
            "forbidden_roots": ["answers", "data/reveals", "shadow-rebuild"],
            "runtime_repository_vault_credential": "NONE",
        },
        "input_receipts": {
            "snapshot_path": str(snapshot_path),
            "snapshot_sha256": sha256_file(snapshot_path),
            "contract_path": str(contract_path),
            "contract_sha256": sha256_file(contract_path),
            "questions_path": str(questions_path),
            "questions_sha256": sha256_file(questions_path),
        },
    }
    findings = _contains_forbidden(payload)
    if findings:
        raise FortuneError(
            "forbidden answer material detected in external runner request: "
            + ";".join(findings),
            status="EXTERNAL_RUNNER_ANSWER_LEAK_DETECTED",
        )
    return payload


def _origin(endpoint: str) -> str:
    parsed = urlparse(endpoint)
    if parsed.scheme not in {"https", "http"} or not parsed.netloc:
        raise FortuneError("external runner endpoint is invalid", status="EXTERNAL_RUNNER_ENDPOINT_INVALID")
    return f"{parsed.scheme}://{parsed.netloc}"


def run_external_prediction(snapshot_path: str | Path, contract_path: str | Path,
                            endpoint: str, output_path: str | Path,
                            receipt_path: str | Path, runner_id: str,
                            *, token: str | None = None,
                            timeout_seconds: int = 1800) -> dict[str, Any]:
    """Invoke a separate executor and accept only a valid PREDICTION-RUN-V1.

    No output file is created unless the remote response passes the complete
    local runtime validator.  Token values are used only in memory and are never
    written to the request, receipt, logs, or repository.
    """
    if timeout_seconds <= 0:
        raise FortuneError("timeout must be positive", status="EXTERNAL_RUNNER_CONFIG_INVALID")

    contract = read_json(contract_path)
    payload = build_runner_request(snapshot_path, contract_path, runner_id)
    request_body = canonical_bytes(payload)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "fortune-training-v1/external-runner",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(endpoint, data=request_body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            status_code = getattr(response, "status", response.getcode())
            response_body = response.read()
    except urllib.error.HTTPError as exc:
        raise FortuneError(
            f"external runner returned HTTP {exc.code}",
            status="EXTERNAL_PREDICTION_RUNNER_FAILED",
        ) from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise FortuneError(
            f"external runner transport failed: {exc}",
            status="EXTERNAL_PREDICTION_RUNNER_FAILED",
        ) from exc

    if status_code != 200:
        raise FortuneError(
            f"external runner returned HTTP {status_code}",
            status="EXTERNAL_PREDICTION_RUNNER_FAILED",
        )
    try:
        run = json.loads(response_body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise FortuneError(
            "external runner response is not valid UTF-8 JSON",
            status="EXTERNAL_PREDICTION_RUNNER_FAILED",
        ) from exc
    if not isinstance(run, dict):
        raise FortuneError(
            "external runner response is not an object",
            status="EXTERNAL_PREDICTION_RUNNER_FAILED",
        )

    validation = validate_prediction_run(run, contract)
    if validation.get("status") != "PASS":
        raise FortuneError(
            "external prediction run failed local validation: "
            + ";".join(validation.get("errors", [])),
            status="EXTERNAL_PREDICTION_RUNNER_FAILED",
        )

    run["runtime_validation"] = validation
    atomic_write_json(output_path, run)
    receipt = {
        "schema": "EXTERNAL-PREDICTION-RUNNER-RECEIPT-V1",
        "status": "PASS",
        "runner_id": runner_id,
        "endpoint_origin": _origin(endpoint),
        "request_sha256": sha256_bytes(request_body),
        "response_sha256": sha256_bytes(response_body),
        "prediction_path": str(output_path),
        "prediction_sha256": sha256_file(output_path),
        "contract_sha256": sha256_file(contract_path),
        "snapshot_sha256": sha256_file(snapshot_path),
        "timeout_seconds": timeout_seconds,
        "token_present": bool(token),
        "token_value_persisted": False,
        "no_answer_access_proof": {
            "answer_data_available": False,
            "request_forbidden_scan": "PASS",
            "runtime_repository_vault_credential": "NONE",
            "forbidden_roots": ["answers", "data/reveals", "shadow-rebuild"],
        },
        "validation": validation,
        "completed_at": utc_now(),
    }
    atomic_write_json(receipt_path, receipt)
    return receipt


def token_from_environment(name: str) -> str | None:
    value = os.getenv(name)
    return value if value else None
