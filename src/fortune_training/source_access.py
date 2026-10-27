from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from .util import TrainingError, atomic_write_bytes, atomic_write_json, load_json, object_sha256


CANONICAL_MANIFEST_PATH = Path("sources/canonical-manifest.json")
DERIVED_ACCESS_ROOT = Path("sources/derived-access")
SOURCE_ACCESS_INDEX_SCHEMA = "CANONICAL-SOURCE-ACCESS-INDEX-R1"
SEGMENTER_ALGORITHM_ID = "STRICT_UTF8_COMPLETE_LINE_MAX_BYTES_R1"
DEFAULT_MAX_SEGMENT_BYTES = 64 * 1024
MAX_ALLOWED_SEGMENT_BYTES = 128 * 1024
R1_MATERIALIZED_SOURCE_IDS = ("S14",)
VIEW_ROLE = "READ_ONLY_LOSSLESS_ACCESS_MIRROR_NOT_SOURCE_AUTHORITY"
DERIVATION = "EXACT_BYTE_CONCATENATION_NO_NORMALIZATION"
COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _run_git(root: Path, *arguments: str) -> bytes:
    try:
        return subprocess.run(
            ["git", "-C", str(root), *arguments],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise TrainingError(
            f"cannot establish source-access Git binding: {' '.join(arguments)}"
        ) from exc


def _strict_json_bytes(payload: bytes, *, label: str) -> Any:
    try:
        text = payload.decode("utf-8", errors="strict")
        return json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TrainingError(f"invalid strict UTF-8 JSON: {label}") from exc


def load_canonical_source_identity(
    root: Path,
    source_id: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = load_json(root / CANONICAL_MANIFEST_PATH)
    sources = manifest.get("sources")
    if (
        manifest.get("schema") != "CANONICAL-SOURCE-MANIFEST-V1"
        or not isinstance(sources, list)
    ):
        raise TrainingError("canonical source manifest is invalid")
    if not all(isinstance(source, dict) for source in sources):
        raise TrainingError("canonical manifest contains a non-object source entry")
    matches = [source for source in sources if source.get("source_id") == source_id]
    if len(matches) != 1:
        raise TrainingError(f"canonical source identity is not unique: {source_id}")
    source = matches[0]
    expected_types = {
        "source_id": str,
        "path": str,
        "bytes": int,
        "sha256": str,
        "runtime_role": str,
    }
    if any(
        not isinstance(source.get(field), expected_type)
        or (field == "bytes" and isinstance(source.get(field), bool))
        for field, expected_type in expected_types.items()
    ):
        raise TrainingError(f"canonical source identity is invalid: {source_id}")
    if source["bytes"] < 0 or not re.fullmatch(r"[0-9a-f]{64}", source["sha256"]):
        raise TrainingError(f"canonical source integrity fields are invalid: {source_id}")
    if not source["path"].startswith("sources/canonical/"):
        raise TrainingError(f"canonical source path is outside authority root: {source_id}")
    return manifest, source


def validate_canonical_bytes(
    root: Path,
    source: dict[str, Any],
) -> bytes:
    path = root / source["path"]
    try:
        payload = path.read_bytes()
    except OSError as exc:
        raise TrainingError(f"cannot read canonical source: {source['source_id']}") from exc
    try:
        text = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise TrainingError(
            f"canonical source is not strict UTF-8: {source['source_id']}"
        ) from exc
    if text.encode("utf-8") != payload:
        raise TrainingError(f"canonical UTF-8 byte replay failed: {source['source_id']}")
    if len(payload) != source["bytes"] or _sha256(payload) != source["sha256"]:
        raise TrainingError(
            f"canonical source does not match manifest identity: {source['source_id']}"
        )
    return payload


def _source_from_manifest(manifest: Any, source_id: str) -> dict[str, Any]:
    if not isinstance(manifest, dict) or not isinstance(manifest.get("sources"), list):
        raise TrainingError("source commit canonical manifest is invalid")
    matches = [
        source
        for source in manifest["sources"]
        if isinstance(source, dict) and source.get("source_id") == source_id
    ]
    if len(matches) != 1:
        raise TrainingError(f"source commit identity is not unique: {source_id}")
    return matches[0]


def validate_source_commit_binding(
    root: Path,
    *,
    source_commit: str,
    source: dict[str, Any],
    canonical_bytes: bytes,
) -> None:
    if not isinstance(source_commit, str) or not COMMIT_SHA.fullmatch(source_commit):
        raise TrainingError("source commit must be an exact lowercase 40-character SHA")
    resolved = _run_git(root, "rev-parse", f"{source_commit}^{{commit}}").decode(
        "ascii", errors="strict"
    ).strip()
    if resolved != source_commit:
        raise TrainingError("source commit does not resolve to the declared exact commit")
    committed_bytes = _run_git(root, "show", f"{source_commit}:{source['path']}")
    if committed_bytes != canonical_bytes:
        raise TrainingError(
            f"source commit canonical bytes do not match checkout: {source['source_id']}"
        )
    committed_manifest = _strict_json_bytes(
        _run_git(root, "show", f"{source_commit}:{CANONICAL_MANIFEST_PATH.as_posix()}"),
        label="source commit canonical manifest",
    )
    committed_source = _source_from_manifest(committed_manifest, source["source_id"])
    if committed_source != source:
        raise TrainingError(
            f"source commit manifest identity does not match checkout: {source['source_id']}"
        )


def _split_complete_lines(
    source_bytes: bytes,
    *,
    source_id: str,
    max_segment_bytes: int,
) -> list[bytes]:
    if (
        not isinstance(max_segment_bytes, int)
        or isinstance(max_segment_bytes, bool)
        or max_segment_bytes <= 0
        or max_segment_bytes > MAX_ALLOWED_SEGMENT_BYTES
    ):
        raise TrainingError("source-access maximum segment bytes is invalid")
    try:
        source_text = source_bytes.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise TrainingError(f"canonical source is not strict UTF-8: {source_id}") from exc
    lines = source_text.splitlines(keepends=True)
    segments: list[bytes] = []
    current: list[bytes] = []
    current_size = 0
    for line_number, line in enumerate(lines, start=1):
        encoded = line.encode("utf-8")
        if len(encoded) > max_segment_bytes:
            raise TrainingError(
                f"canonical line exceeds source-access segment limit: "
                f"{source_id} line {line_number}"
            )
        if current and current_size + len(encoded) > max_segment_bytes:
            segments.append(b"".join(current))
            current = []
            current_size = 0
        current.append(encoded)
        current_size += len(encoded)
    if current:
        segments.append(b"".join(current))
    if b"".join(segments) != source_bytes:
        raise TrainingError(f"lossless source-access segmentation failed: {source_id}")
    return segments


def build_source_access_index(
    root: Path,
    *,
    source_id: str,
    source_commit: str | None = None,
    max_segment_bytes: int = DEFAULT_MAX_SEGMENT_BYTES,
) -> tuple[dict[str, Any], list[bytes]]:
    root = root.resolve()
    _, source = load_canonical_source_identity(root, source_id)
    canonical_bytes = validate_canonical_bytes(root, source)
    if source_commit is None:
        source_commit = _run_git(root, "rev-parse", "HEAD").decode(
            "ascii", errors="strict"
        ).strip()
    validate_source_commit_binding(
        root,
        source_commit=source_commit,
        source=source,
        canonical_bytes=canonical_bytes,
    )
    segments = _split_complete_lines(
        canonical_bytes,
        source_id=source_id,
        max_segment_bytes=max_segment_bytes,
    )
    rows: list[dict[str, Any]] = []
    byte_start = 0
    line_start = 1
    for sequence, payload in enumerate(segments, start=1):
        line_count = len(payload.decode("utf-8", errors="strict").splitlines(keepends=True))
        line_end = line_start + line_count - 1
        path = (
            DERIVED_ACCESS_ROOT / source_id / f"segment-{sequence:04d}.txt"
        ).as_posix()
        rows.append(
            {
                "segment_id": f"{source_id}-{sequence:04d}",
                "sequence": sequence,
                "path": path,
                "byte_start": byte_start,
                "byte_end_exclusive": byte_start + len(payload),
                "bytes": len(payload),
                "line_start": line_start,
                "line_end_inclusive": line_end,
                "sha256": _sha256(payload),
            }
        )
        byte_start += len(payload)
        line_start = line_end + 1
    index = {
        "schema": SOURCE_ACCESS_INDEX_SCHEMA,
        "authority": {
            "view_role": VIEW_ROLE,
            "canonical_manifest_path": CANONICAL_MANIFEST_PATH.as_posix(),
            "canonical_source_is_sole_authority": True,
            "prediction_source_selection_allowed": False,
            "runtime_authority_redefined": False,
            "derivation": DERIVATION,
        },
        "source": {
            "source_id": source["source_id"],
            "canonical_path": source["path"],
            "canonical_bytes": source["bytes"],
            "canonical_sha256": source["sha256"],
            "runtime_role": source["runtime_role"],
            "canonical_source_entry_sha256": object_sha256(source),
        },
        "materialization": {
            "repository": "chinaneedM/ziwei-bazi-model",
            "source_commit": source_commit,
            "segmenter_algorithm_id": SEGMENTER_ALGORITHM_ID,
            "max_segment_bytes": max_segment_bytes,
        },
        "segment_count": len(rows),
        "segments": rows,
    }
    return index, segments


def write_source_access(
    root: Path,
    *,
    source_id: str = "S14",
    source_commit: str | None = None,
    max_segment_bytes: int = DEFAULT_MAX_SEGMENT_BYTES,
) -> dict[str, Any]:
    if source_id not in R1_MATERIALIZED_SOURCE_IDS:
        raise TrainingError(
            "Canonical Source Access Foundation R1 may materialize S14 only"
        )
    root = root.resolve()
    index, segments = build_source_access_index(
        root,
        source_id=source_id,
        source_commit=source_commit,
        max_segment_bytes=max_segment_bytes,
    )
    source_root = root / DERIVED_ACCESS_ROOT / source_id
    source_root.mkdir(parents=True, exist_ok=True)
    expected_paths: set[Path] = {source_root / "index.json"}
    for row, payload in zip(index["segments"], segments, strict=True):
        destination = root / row["path"]
        expected_paths.add(destination)
        atomic_write_bytes(destination, payload)
    atomic_write_json(source_root / "index.json", index)
    for path in source_root.rglob("*"):
        if path.is_file() and path not in expected_paths:
            path.unlink()
    return index
