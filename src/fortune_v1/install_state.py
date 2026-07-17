from __future__ import annotations

from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, read_json, sha256_file, utc_now


PASS_INSTALL_STATES = {"INSTALL_VALIDATION_CANDIDATE", "INSTALLED_VALIDATED"}


def finalize_installation_state(
    install_receipt_path: str | Path,
    expected_code_commit: str,
    output_path: str | Path,
) -> dict[str, Any]:
    """Create a separate immutable installation-state seal.

    The installation receipt must never contain its own final hash.  This sidecar
    references the already-written receipt bytes and the exact immutable code
    commit.  Any later change to either invalidates the seal mechanically.
    """
    receipt_path = Path(install_receipt_path)
    if not receipt_path.is_file():
        raise FortuneError("installation receipt is missing", status="INSTALL_RECEIPT_MISSING")
    if not expected_code_commit or not expected_code_commit.strip():
        raise FortuneError("expected code commit is required", status="INSTALL_COMMIT_MISSING")

    receipt = read_json(receipt_path)
    receipt_status = receipt.get("status")
    runtime_status = receipt.get("automation_runtime_install_status")
    if receipt_status not in PASS_INSTALL_STATES or runtime_status not in PASS_INSTALL_STATES:
        raise FortuneError(
            "installation receipt has not passed all gates",
            status="INSTALL_RECEIPT_NOT_PASS",
        )
    failed_checks = [
        row.get("check", "UNKNOWN")
        for row in receipt.get("checks", [])
        if row.get("status") != "PASS"
    ]
    if failed_checks:
        raise FortuneError(
            "installation receipt contains non-PASS checks: " + ",".join(failed_checks),
            status="INSTALL_RECEIPT_CHECK_FAILED",
        )

    actual_commit = receipt.get("code_commit")
    if actual_commit != expected_code_commit:
        raise FortuneError(
            f"installation receipt commit mismatch: {actual_commit} != {expected_code_commit}",
            status="INSTALL_RECEIPT_COMMIT_MISMATCH",
        )

    seal = {
        "schema": "INSTALLATION-STATE-SEAL-V1",
        "status": "INSTALLED_VALIDATED",
        "automation_runtime_install_status": "INSTALLED_VALIDATED",
        "code_commit": expected_code_commit,
        "install_receipt_path": str(receipt_path),
        "install_receipt_sha256": sha256_file(receipt_path),
        "source_baseline_status": "IMMUTABLE_VERIFIED",
        "source_internal_install_markers_role": "HISTORICAL_INSTALLATION_PREREQUISITE_ONLY",
        "current_runtime_status_authority": "THIS_SEAL",
        "invalidation_rule": "ANY_CODE_COMMIT_OR_INSTALL_RECEIPT_HASH_CHANGE_REQUIRES_REVALIDATION",
        "generated_at": utc_now(),
    }
    atomic_write_json(output_path, seal, overwrite=True)
    return seal


def validate_installation_state(
    seal_path: str | Path,
    install_receipt_path: str | Path,
    current_code_commit: str,
) -> dict[str, Any]:
    seal_file = Path(seal_path)
    receipt_file = Path(install_receipt_path)
    errors: list[str] = []
    if not seal_file.is_file():
        errors.append("INSTALLATION_STATE_SEAL_MISSING")
    if not receipt_file.is_file():
        errors.append("INSTALL_RECEIPT_MISSING")
    if errors:
        return {"status": "REVALIDATION_REQUIRED", "errors": errors}

    seal = read_json(seal_file)
    if seal.get("status") != "INSTALLED_VALIDATED":
        errors.append("INSTALLATION_STATE_NOT_VALIDATED")
    if seal.get("code_commit") != current_code_commit:
        errors.append("CODE_COMMIT_DRIFT")
    if seal.get("install_receipt_sha256") != sha256_file(receipt_file):
        errors.append("INSTALL_RECEIPT_HASH_DRIFT")
    return {
        "status": "INSTALLED_VALIDATED" if not errors else "REVALIDATION_REQUIRED",
        "errors": errors,
        "code_commit": current_code_commit,
        "seal_path": str(seal_file),
        "install_receipt_path": str(receipt_file),
    }
