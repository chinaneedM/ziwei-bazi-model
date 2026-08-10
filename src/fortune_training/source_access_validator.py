from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from .source_access import (
    CANONICAL_MANIFEST_PATH,
    DEFAULT_MAX_SEGMENT_BYTES,
    DERIVATION,
    DERIVED_ACCESS_ROOT,
    MAX_ALLOWED_SEGMENT_BYTES,
    SEGMENTER_ALGORITHM_ID,
    SOURCE_ACCESS_INDEX_SCHEMA,
    VIEW_ROLE,
)
from .util import TrainingError, load_json, object_sha256


COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _fail(message: str) -> None:
    raise TrainingError(f"canonical source-access validation failed: {message}")


def _canonical_identity(root: Path, source_id: str) -> dict[str, Any]:
    manifest = load_json(root / CANONICAL_MANIFEST_PATH)
    if manifest.get("schema") != "CANONICAL-SOURCE-MANIFEST-V1":
        _fail("canonical manifest schema")
    sources = manifest.get("sources")
    if not isinstance(sources, list):
        _fail("canonical manifest sources")
    matches = [row for row in sources if isinstance(row, dict) and row.get("source_id") == source_id]
    if len(matches) != 1:
        _fail("source identity is missing or duplicated")
    source = matches[0]
    required = {
        "source_id": str,
        "path": str,
        "bytes": int,
        "sha256": str,
        "runtime_role": str,
    }
    if any(
        not isinstance(source.get(key), value_type)
        or (key == "bytes" and isinstance(source.get(key), bool))
        for key, value_type in required.items()
    ):
        _fail("canonical source identity types")
    if source["bytes"] < 0 or not SHA256.fullmatch(source["sha256"]):
        _fail("canonical source integrity identity")
    if not source["path"].startswith("sources/canonical/"):
        _fail("canonical source path authority")
    return source


def _strict_utf8(payload: bytes, label: str) -> str:
    try:
        text = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise TrainingError(
            f"canonical source-access validation failed: invalid UTF-8 in {label}"
        ) from exc
    if text.encode("utf-8") != payload:
        _fail(f"UTF-8 replay mismatch in {label}")
    return text


def _git_bytes(root: Path, *arguments: str) -> bytes:
    try:
        return subprocess.run(
            ["git", "-C", str(root), *arguments],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise TrainingError(
            "canonical source-access validation failed: source commit is unavailable"
        ) from exc


def _validate_commit(
    root: Path,
    *,
    commit: Any,
    source: dict[str, Any],
    canonical_bytes: bytes,
    require_available: bool,
) -> bool:
    if not isinstance(commit, str) or not COMMIT_SHA.fullmatch(commit):
        _fail("invalid exact source commit")
    try:
        resolved = _git_bytes(root, "rev-parse", f"{commit}^{{commit}}").decode(
            "ascii", errors="strict"
        ).strip()
    except TrainingError:
        if require_available:
            raise
        return False
    if resolved != commit:
        _fail("source commit resolution mismatch")
    if _git_bytes(root, "show", f"{commit}:{source['path']}") != canonical_bytes:
        _fail("source commit canonical bytes mismatch")
    manifest_payload = _git_bytes(
        root, "show", f"{commit}:{CANONICAL_MANIFEST_PATH.as_posix()}"
    )
    try:
        committed_manifest = json.loads(_strict_utf8(manifest_payload, "source commit manifest"))
    except json.JSONDecodeError as exc:
        raise TrainingError(
            "canonical source-access validation failed: invalid source commit manifest"
        ) from exc
    matches = [
        row
        for row in committed_manifest.get("sources", [])
        if isinstance(row, dict) and row.get("source_id") == source["source_id"]
    ]
    if len(matches) != 1 or matches[0] != source:
        _fail("source commit manifest identity mismatch")
    return True


def validate_source_access(
    root: Path,
    *,
    source_id: str = "S14",
    require_source_commit: bool = True,
) -> dict[str, Any]:
    root = root.resolve()
    source = _canonical_identity(root, source_id)
    try:
        canonical_bytes = (root / source["path"]).read_bytes()
    except OSError as exc:
        raise TrainingError(
            "canonical source-access validation failed: canonical source unavailable"
        ) from exc
    _strict_utf8(canonical_bytes, "canonical source")
    if len(canonical_bytes) != source["bytes"] or _sha256(canonical_bytes) != source["sha256"]:
        _fail("canonical source does not match manifest")

    source_root = root / DERIVED_ACCESS_ROOT / source_id
    index_path = source_root / "index.json"
    index = load_json(index_path)
    if set(index) != {
        "schema",
        "authority",
        "source",
        "materialization",
        "segment_count",
        "segments",
    } or index.get("schema") != SOURCE_ACCESS_INDEX_SCHEMA:
        _fail("index schema")
    expected_authority = {
        "view_role": VIEW_ROLE,
        "canonical_manifest_path": CANONICAL_MANIFEST_PATH.as_posix(),
        "canonical_source_is_sole_authority": True,
        "prediction_source_selection_allowed": False,
        "runtime_authority_redefined": False,
        "derivation": DERIVATION,
    }
    if index.get("authority") != expected_authority:
        _fail("authority boundary")
    expected_source = {
        "source_id": source["source_id"],
        "canonical_path": source["path"],
        "canonical_bytes": source["bytes"],
        "canonical_sha256": source["sha256"],
        "runtime_role": source["runtime_role"],
        "canonical_source_entry_sha256": object_sha256(source),
    }
    if index.get("source") != expected_source:
        _fail("index source identity")
    materialization = index.get("materialization")
    if not isinstance(materialization, dict) or set(materialization) != {
        "repository",
        "source_commit",
        "segmenter_algorithm_id",
        "max_segment_bytes",
    }:
        _fail("materialization metadata")
    max_bytes = materialization.get("max_segment_bytes")
    if (
        materialization.get("repository") != "chinaneedM/ziwei-bazi-model"
        or materialization.get("segmenter_algorithm_id") != SEGMENTER_ALGORITHM_ID
        or not isinstance(max_bytes, int)
        or isinstance(max_bytes, bool)
        or max_bytes <= 0
        or max_bytes > MAX_ALLOWED_SEGMENT_BYTES
    ):
        _fail("materialization configuration")
    if source_id == "S14" and max_bytes != DEFAULT_MAX_SEGMENT_BYTES:
        _fail("S14 configured maximum")
    source_commit_verified = _validate_commit(
        root,
        commit=materialization.get("source_commit"),
        source=source,
        canonical_bytes=canonical_bytes,
        require_available=require_source_commit,
    )

    rows = index.get("segments")
    if not isinstance(rows, list) or index.get("segment_count") != len(rows):
        _fail("segment count")
    line_bytes = [
        line.encode("utf-8")
        for line in _strict_utf8(canonical_bytes, "canonical source").splitlines(keepends=True)
    ]
    line_offsets = [0]
    for line in line_bytes:
        line_offsets.append(line_offsets[-1] + len(line))

    expected_files = {index_path.resolve()}
    reconstructed: list[bytes] = []
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    next_byte = 0
    next_line = 1
    for expected_sequence, row in enumerate(rows, start=1):
        if not isinstance(row, dict) or set(row) != {
            "segment_id",
            "sequence",
            "path",
            "byte_start",
            "byte_end_exclusive",
            "bytes",
            "line_start",
            "line_end_inclusive",
            "sha256",
        }:
            _fail("segment row type")
        expected_path = (
            DERIVED_ACCESS_ROOT / source_id / f"segment-{expected_sequence:04d}.txt"
        ).as_posix()
        expected_id = f"{source_id}-{expected_sequence:04d}"
        path_value = row.get("path")
        segment_id = row.get("segment_id")
        if (
            row.get("sequence") != expected_sequence
            or segment_id != expected_id
            or path_value != expected_path
            or segment_id in seen_ids
            or path_value in seen_paths
        ):
            _fail("segment order, identity, or path")
        seen_ids.add(segment_id)
        seen_paths.add(path_value)
        segment_path = (root / path_value).resolve()
        if source_root.resolve() not in segment_path.parents:
            _fail("segment path escapes source-access root")
        expected_files.add(segment_path)
        try:
            payload = segment_path.read_bytes()
        except OSError as exc:
            raise TrainingError(
                f"canonical source-access validation failed: missing segment {path_value}"
            ) from exc
        _strict_utf8(payload, path_value)
        byte_start = row.get("byte_start")
        byte_end = row.get("byte_end_exclusive")
        byte_count = row.get("bytes")
        line_start = row.get("line_start")
        line_end = row.get("line_end_inclusive")
        if (
            not all(
                isinstance(value, int) and not isinstance(value, bool)
                for value in (byte_start, byte_end, byte_count, line_start, line_end)
            )
            or byte_start != next_byte
            or byte_end != byte_start + byte_count
            or byte_count != len(payload)
            or byte_count > max_bytes
            or line_start != next_line
            or line_end < line_start
            or line_end > len(line_bytes)
            or not isinstance(row.get("sha256"), str)
            or not SHA256.fullmatch(row["sha256"])
            or _sha256(payload) != row["sha256"]
        ):
            _fail(f"segment metadata or hash: {expected_id}")
        expected_byte_start = line_offsets[line_start - 1]
        expected_byte_end = line_offsets[line_end]
        if (
            byte_start != expected_byte_start
            or byte_end != expected_byte_end
            or payload != canonical_bytes[expected_byte_start:expected_byte_end]
        ):
            _fail(f"segment byte/line replay: {expected_id}")
        reconstructed.append(payload)
        next_byte = byte_end
        next_line = line_end + 1

    if canonical_bytes and not rows:
        _fail("non-empty source has no segments")
    if next_byte != len(canonical_bytes):
        _fail("gap or incomplete byte coverage")
    if line_bytes and next_line != len(line_bytes) + 1:
        _fail("gap or incomplete line coverage")
    combined = b"".join(reconstructed)
    if (
        combined != canonical_bytes
        or len(combined) != source["bytes"]
        or _sha256(combined) != source["sha256"]
    ):
        _fail("round-trip reconstruction")
    actual_files = {path.resolve() for path in source_root.rglob("*") if path.is_file()}
    if actual_files != expected_files:
        _fail("missing, duplicate, or unexpected segment file")
    return {
        "status": "PASS",
        "source_id": source_id,
        "canonical_bytes": len(combined),
        "canonical_sha256": _sha256(combined),
        "source_commit": materialization["source_commit"],
        "source_commit_verified": source_commit_verified,
        "segment_count": len(rows),
        "max_segment_bytes": max_bytes,
        "round_trip_exact": True,
    }
