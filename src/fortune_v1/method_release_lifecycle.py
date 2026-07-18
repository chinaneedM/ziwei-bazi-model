from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from .repository_release import validate_method_release, write_object
from .util import FortuneError, read_json, sha256_file, slug, utc_now


def promote_method_candidate(method_path: str | Path, releases_root: str | Path,
                             active_pointer: str | Path, receipt_path: str | Path, *,
                             approval_id: str, expected_previous_release_id: str | None = None) -> dict[str, Any]:
    validation = validate_method_release(method_path)
    if validation["status"] != "PASS":
        raise FortuneError("method candidate invalid", status="METHOD_CANDIDATE_INVALID")
    current = read_json(active_pointer) if Path(active_pointer).exists() else {}
    if expected_previous_release_id is not None and current.get("method_release_id") != expected_previous_release_id:
        raise FortuneError("active method pointer moved", status="ACTIVE_POINTER_COMPARE_AND_SWAP_FAILED")
    method = read_json(method_path)
    target_dir = Path(releases_root) / slug(method["method_release_id"])
    target = target_dir / "method-release.json"
    if target_dir.exists():
        raise FortuneError("method release already exists", status="IMMUTABLE_OBJECT_EXISTS")
    target_dir.mkdir(parents=True)
    shutil.copy2(method_path, target)
    target.chmod(0o444)
    if validate_method_release(target)["status"] != "PASS":
        shutil.rmtree(target_dir)
        raise FortuneError("method release readback failed", status="METHOD_RELEASE_READBACK_FAILED")
    write_object(active_pointer, {
        "schema": "FORTUNE-ACTIVE-METHOD-RELEASE-POINTER-V1",
        "method_release_id": method["method_release_id"],
        "method_release_path": target.as_posix(),
        "method_release_sha256": sha256_file(target),
        "previous_release_id": current.get("method_release_id"),
        "approval_id": approval_id, "activation_reason": "CANDIDATE_PROMOTION",
        "activated_at": utc_now(),
    }, overwrite=True)
    return write_object(receipt_path, {
        "schema": "FORTUNE-METHOD-PROMOTION-RECEIPT-V1", "status": "PASS",
        "method_release_id": method["method_release_id"],
        "previous_release_id": current.get("method_release_id"),
        "approval_id": approval_id, "method_release_sha256": sha256_file(target),
        "completed_at": utc_now(),
    })


def rollback_method_release(target_method_path: str | Path, active_pointer: str | Path,
                            receipt_path: str | Path, *, reason: str, approval_id: str) -> dict[str, Any]:
    method = read_json(target_method_path)
    if validate_method_release(target_method_path)["status"] != "PASS":
        raise FortuneError("method rollback target invalid", status="METHOD_ROLLBACK_TARGET_INVALID")
    current = read_json(active_pointer)
    write_object(active_pointer, {
        "schema": "FORTUNE-ACTIVE-METHOD-RELEASE-POINTER-V1",
        "method_release_id": method["method_release_id"],
        "method_release_path": Path(target_method_path).as_posix(),
        "method_release_sha256": sha256_file(target_method_path),
        "previous_release_id": current.get("method_release_id"),
        "approval_id": approval_id, "activation_reason": "ROLLBACK", "activated_at": utc_now(),
    }, overwrite=True)
    return write_object(receipt_path, {
        "schema": "FORTUNE-METHOD-ROLLBACK-RECEIPT-V1", "status": "PASS",
        "from_release_id": current.get("method_release_id"),
        "to_release_id": method["method_release_id"], "reason": reason,
        "approval_id": approval_id, "completed_at": utc_now(),
    })
