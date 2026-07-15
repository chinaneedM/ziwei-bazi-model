from __future__ import annotations

from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, immutable_copy, sha256_file, utc_now


def create_prompt_snapshot(runtime_id: str, prompt_file: str | Path, destination: str | Path,
                           attestation: dict[str, Any] | None = None) -> dict[str, Any]:
    source = Path(prompt_file)
    if not source.is_file() or source.stat().st_size == 0:
        raise FortuneError("prompt snapshot source is missing or empty", status="PROMPT_SNAPSHOT_INVALID")
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    prompt_target = destination / "main_prompt.txt"
    copy = immutable_copy(source, prompt_target)
    manifest = {
        "schema": "MAIN-PROMPT-AUDIT-SNAPSHOT-V1", "runtime_id": runtime_id,
        "snapshot_sha256": copy["sha256"], "snapshot_bytes": copy["bytes"], "captured_at": utc_now(),
        "authority_statement": "AUDIT_COPY_ONLY_NOT_RUNTIME_AUTHORITY", "runtime_attestation": attestation,
    }
    atomic_write_json(destination / "snapshot.json", manifest)
    return manifest

