from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class FortuneError(RuntimeError):
    """Base error carrying a stable machine status."""

    status = "ERROR"

    def __init__(self, message: str, *, status: str | None = None) -> None:
        super().__init__(message)
        if status:
            self.status = status


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str | Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def atomic_write_json(path: str | Path, value: Any, *, overwrite: bool = False) -> Path:
    target = Path(path)
    if target.exists() and not overwrite:
        raise FortuneError(f"immutable object already exists: {target}", status="IMMUTABLE_OBJECT_EXISTS")
    target.parent.mkdir(parents=True, exist_ok=True)
    body = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(body)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, target)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
    return target


def immutable_copy(src: str | Path, dst: str | Path) -> dict[str, Any]:
    source, target = Path(src), Path(dst)
    if target.exists():
        raise FortuneError(f"immutable target exists: {target}", status="IMMUTABLE_OBJECT_EXISTS")
    data = source.read_bytes()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    target.chmod(0o444)
    return {"path": str(target), "sha256": sha256_bytes(data), "bytes": len(data)}


def slug(value: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z._-]+", "-", value.strip()).strip("-.")
    if not cleaned:
        raise FortuneError("empty or unsafe identifier", status="INVALID_IDENTIFIER")
    return cleaned


def ensure_within(root: Path, candidate: Path) -> Path:
    root_resolved = root.resolve()
    candidate_resolved = candidate.resolve()
    if root_resolved != candidate_resolved and root_resolved not in candidate_resolved.parents:
        raise FortuneError(f"path escapes root: {candidate}", status="PATH_TRAVERSAL_REJECTED")
    return candidate_resolved


def object_receipt(path: str | Path, *, git_commit: str | None = None) -> dict[str, Any]:
    p = Path(path)
    return {
        "path": str(p),
        "sha256": sha256_file(p),
        "bytes": p.stat().st_size,
        "git_commit": git_commit,
    }

