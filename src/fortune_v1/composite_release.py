from __future__ import annotations

import base64
import gzip
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

from .contamination import assert_knowledge_source_path
from .repository_release import LIBRARIES, object_hash, validate_knowledge_manifest, write_object
from .util import FortuneError, read_json, sha256_bytes, sha256_file, utc_now


DIRECT_PARENT_REUSE = "DIRECT_PARENT_REUSE"
BYTE_PREPEND = "BYTE_PREPEND"
GZIP_BASE64_PREPEND = "GZIP_BASE64_PREPEND"


def _verified_file(root: Path, relative_path: str, expected_sha256: str,
                   expected_size: int, *, label: str) -> Path:
    assert_knowledge_source_path(relative_path)
    path = root / relative_path
    if not path.is_file():
        raise FortuneError(f"{label} missing: {relative_path}", status="COMPOSITE_SOURCE_MISSING")
    if path.stat().st_size != expected_size:
        raise FortuneError(f"{label} size mismatch: {relative_path}", status="COMPOSITE_SOURCE_SIZE_MISMATCH")
    if sha256_file(path) != expected_sha256:
        raise FortuneError(f"{label} hash mismatch: {relative_path}", status="COMPOSITE_SOURCE_HASH_MISMATCH")
    return path


def _decode_gzip_base64_overlay(container: Path, materialization: dict[str, Any], *, label: str) -> bytes:
    try:
        encoded = container.read_bytes()
        compressed = base64.b64decode(encoded, validate=True)
        decoded = gzip.decompress(compressed)
    except (OSError, ValueError) as exc:
        raise FortuneError(f"{label} decode failed", status="COMPOSITE_OVERLAY_DECODE_INVALID") from exc
    if len(decoded) != materialization["overlay_file_size_bytes"]:
        raise FortuneError(f"{label} decoded size mismatch", status="COMPOSITE_SOURCE_SIZE_MISMATCH")
    if sha256_bytes(decoded) != materialization["overlay_sha256_raw_file_bytes"]:
        raise FortuneError(f"{label} decoded hash mismatch", status="COMPOSITE_SOURCE_HASH_MISMATCH")
    return decoded


def materialize_knowledge_release(manifest_path: str | Path, repository_root: str | Path,
                                   output_dir: str | Path, receipt_path: str | Path | None = None,
                                   *, overwrite: bool = False) -> dict[str, Any]:
    manifest_file = Path(manifest_path)
    manifest = read_json(manifest_file)
    root = Path(repository_root)
    target = Path(output_dir)
    rows = manifest.get("source_files", [])
    if manifest.get("schema") != "FORTUNE-KNOWLEDGE-RELEASE-MANIFEST-V1":
        raise FortuneError("knowledge manifest schema invalid", status="COMPOSITE_MANIFEST_INVALID")
    if manifest.get("object_hash") != object_hash(manifest):
        raise FortuneError("knowledge manifest object hash mismatch", status="COMPOSITE_MANIFEST_INVALID")
    if [row.get("library_id") for row in rows] != list(LIBRARIES):
        raise FortuneError("ordered S00-S19 rows required", status="COMPOSITE_MANIFEST_INVALID")
    assert_knowledge_source_path(target)
    if target.exists() and not overwrite:
        raise FortuneError(f"materialization target exists: {target}", status="IMMUTABLE_OBJECT_EXISTS")
    target.parent.mkdir(parents=True, exist_ok=True)

    receipt_rows: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix=f".{target.name}.", dir=target.parent) as temp_name:
        staged = Path(temp_name) / target.name
        staged.mkdir()
        for row in rows:
            lib = row["library_id"]
            materialization = row.get("source_materialization") or {"mode": DIRECT_PARENT_REUSE}
            mode = materialization.get("mode")
            destination = staged / row["canonical_filename"]
            decoded_overlay_sha256 = None
            decoded_overlay_size_bytes = None
            if mode == DIRECT_PARENT_REUSE:
                relative = materialization.get("parent_repository_relative_path") or row.get("repository_relative_path")
                source = _verified_file(
                    root, relative, row["sha256_raw_file_bytes"], row["file_size_bytes"],
                    label=f"{lib} parent",
                )
                shutil.copyfile(source, destination)
                parents = [relative]
            elif mode == BYTE_PREPEND:
                base = _verified_file(
                    root,
                    materialization["base_repository_relative_path"],
                    materialization["base_sha256_raw_file_bytes"],
                    materialization["base_file_size_bytes"],
                    label=f"{lib} base",
                )
                overlay = _verified_file(
                    root,
                    materialization["overlay_repository_relative_path"],
                    materialization["overlay_sha256_raw_file_bytes"],
                    materialization["overlay_file_size_bytes"],
                    label=f"{lib} overlay",
                )
                with destination.open("wb") as out, overlay.open("rb") as left, base.open("rb") as right:
                    shutil.copyfileobj(left, out)
                    shutil.copyfileobj(right, out)
                    out.flush()
                    os.fsync(out.fileno())
                parents = [
                    materialization["overlay_repository_relative_path"],
                    materialization["base_repository_relative_path"],
                ]
            elif mode == GZIP_BASE64_PREPEND:
                base = _verified_file(
                    root,
                    materialization["base_repository_relative_path"],
                    materialization["base_sha256_raw_file_bytes"],
                    materialization["base_file_size_bytes"],
                    label=f"{lib} base",
                )
                container = _verified_file(
                    root,
                    materialization["overlay_container_repository_relative_path"],
                    materialization["overlay_container_sha256_raw_file_bytes"],
                    materialization["overlay_container_file_size_bytes"],
                    label=f"{lib} overlay container",
                )
                decoded = _decode_gzip_base64_overlay(container, materialization, label=f"{lib} overlay")
                decoded_overlay_sha256 = sha256_bytes(decoded)
                decoded_overlay_size_bytes = len(decoded)
                with destination.open("wb") as out, base.open("rb") as right:
                    out.write(decoded)
                    shutil.copyfileobj(right, out)
                    out.flush()
                    os.fsync(out.fileno())
                parents = [
                    materialization["overlay_container_repository_relative_path"],
                    materialization["base_repository_relative_path"],
                ]
            else:
                raise FortuneError(f"unsupported materialization mode: {mode}",
                                   status="COMPOSITE_MATERIALIZATION_MODE_INVALID")

            status = "PASS"
            if destination.stat().st_size != row["file_size_bytes"]:
                status = "SIZE_MISMATCH"
            elif sha256_file(destination) != row["sha256_raw_file_bytes"]:
                status = "HASH_MISMATCH"
            receipt_rows.append({
                "library_id": lib,
                "mode": mode,
                "parent_paths": parents,
                "decoded_overlay_sha256": decoded_overlay_sha256,
                "decoded_overlay_size_bytes": decoded_overlay_size_bytes,
                "output_filename": destination.name,
                "output_sha256": sha256_file(destination),
                "output_size_bytes": destination.stat().st_size,
                "status": status,
            })
            if status != "PASS":
                raise FortuneError(f"{lib} materialized output {status.lower()}",
                                   status="COMPOSITE_MATERIALIZED_OUTPUT_INVALID")
        if target.exists():
            shutil.rmtree(target)
        staged.replace(target)

    readback = validate_knowledge_manifest(manifest_file, target)
    status = "PASS" if readback["status"] == "PASS" else "FAIL_CLOSED"
    receipt = {
        "schema": "FORTUNE-COMPOSITE-KNOWLEDGE-MATERIALIZATION-RECEIPT-V1",
        "status": status,
        "knowledge_release_id": manifest.get("knowledge_release_id"),
        "manifest_path": manifest_file.as_posix(),
        "manifest_sha256": sha256_file(manifest_file),
        "repository_root": root.as_posix(),
        "output_dir": target.as_posix(),
        "source_content_commit_sha": manifest.get("repository_commit_sha"),
        "source_file_count": len(receipt_rows),
        "rows": receipt_rows,
        "readback_status": readback["status"],
        "readback_errors": readback["errors"],
        "formal_release": "NO",
        "score_eligibility": "BLOCKED_PENDING_CAUSAL_SHADOW_VALIDATION",
        "materialized_at": utc_now(),
    }
    receipt["object_hash"] = object_hash(receipt)
    if receipt_path:
        write_object(receipt_path, receipt, overwrite=overwrite)
    if status != "PASS":
        raise FortuneError("materialized release failed readback",
                           status="COMPOSITE_MATERIALIZATION_READBACK_FAILED")
    return receipt
