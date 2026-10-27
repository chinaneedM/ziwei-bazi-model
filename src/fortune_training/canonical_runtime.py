from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from .util import TrainingError, atomic_write_json, load_json, object_sha256


CANONICAL_MANIFEST_PATH = Path("sources/canonical-manifest.json")
RUNTIME_MANIFEST_PATH = Path("sources/canonical-runtime-manifest.json")
RUNTIME_SEGMENT_ROOT = Path("sources/canonical-runtime")
RUNTIME_MANIFEST_SCHEMA = "CANONICAL-RUNTIME-SEGMENT-MANIFEST-V1"
MAX_SEGMENT_BYTES = 512 * 1024
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _split_source(
    source_bytes: bytes,
    *,
    source_id: str,
    max_segment_bytes: int,
) -> tuple[list[bytes], list[dict[str, Any]], list[dict[str, Any]]]:
    try:
        source_text = source_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise TrainingError(f"canonical source is not UTF-8: {source_id}") from exc
    lines = source_text.splitlines(keepends=True)
    if not lines and source_bytes:
        lines = [source_text]

    segments: list[bytes] = []
    segment_rows: list[dict[str, Any]] = []
    line_to_segment: dict[int, int] = {}
    current: list[bytes] = []
    current_bytes = 0
    start_line = 1
    byte_start = 0

    def flush(end_line: int) -> None:
        nonlocal current, current_bytes, start_line, byte_start
        if not current:
            return
        payload = b"".join(current)
        index = len(segments)
        segments.append(payload)
        path = (
            RUNTIME_SEGMENT_ROOT
            / source_id
            / f"segment-{index + 1:04d}.txt"
        ).as_posix()
        segment_rows.append(
            {
                "sequence": index + 1,
                "path": path,
                "bytes": len(payload),
                "sha256": _sha256_bytes(payload),
                "byte_start": byte_start,
                "byte_end_exclusive": byte_start + len(payload),
                "line_start": start_line,
                "line_end": end_line,
            }
        )
        for line_number in range(start_line, end_line + 1):
            line_to_segment[line_number] = index
        byte_start += len(payload)
        start_line = end_line + 1
        current = []
        current_bytes = 0

    for line_number, line in enumerate(lines, start=1):
        encoded = line.encode("utf-8")
        if len(encoded) > max_segment_bytes:
            raise TrainingError(
                f"canonical line exceeds runtime segment limit: "
                f"{source_id} line {line_number}"
            )
        if current and current_bytes + len(encoded) > max_segment_bytes:
            flush(line_number - 1)
        current.append(encoded)
        current_bytes += len(encoded)
    flush(len(lines))

    if b"".join(segments) != source_bytes:
        raise TrainingError(f"lossless canonical split failed: {source_id}")

    headings: list[dict[str, Any]] = []
    for line_number, line in enumerate(lines, start=1):
        match = HEADING.match(line.rstrip("\r\n"))
        if match:
            headings.append(
                {
                    "level": len(match.group(1)),
                    "title": match.group(2),
                    "line": line_number,
                }
            )
    for index, heading in enumerate(headings):
        end_line = len(lines)
        for following in headings[index + 1 :]:
            if following["level"] <= heading["level"]:
                end_line = following["line"] - 1
                break
        start_segment = line_to_segment[heading["line"]]
        end_segment = line_to_segment[end_line]
        heading["segment_paths"] = [
            segment_rows[segment_index]["path"]
            for segment_index in range(start_segment, end_segment + 1)
        ]
        heading["line_end"] = end_line

    return segments, segment_rows, headings


def build_canonical_runtime_manifest(
    root: Path,
    *,
    write_segments: bool = False,
) -> dict[str, Any]:
    root = root.resolve()
    canonical_manifest = load_json(root / CANONICAL_MANIFEST_PATH)
    sources = canonical_manifest.get("sources")
    if (
        canonical_manifest.get("schema") != "CANONICAL-SOURCE-MANIFEST-V1"
        or not isinstance(sources, list)
    ):
        raise TrainingError("canonical manifest is invalid")

    source_rows: list[dict[str, Any]] = []
    expected_segment_paths: set[str] = set()
    total_segments = 0
    for source in sources:
        source_id = source.get("source_id")
        source_path = source.get("path")
        if not isinstance(source_id, str) or not isinstance(source_path, str):
            raise TrainingError("canonical manifest source identity is invalid")
        path = root / source_path
        payload = path.read_bytes()
        if len(payload) != source.get("bytes") or _sha256_bytes(payload) != source.get(
            "sha256"
        ):
            raise TrainingError(f"canonical source does not match manifest: {source_id}")
        segments, segment_rows, headings = _split_source(
            payload,
            source_id=source_id,
            max_segment_bytes=MAX_SEGMENT_BYTES,
        )
        for segment, segment_row in zip(segments, segment_rows):
            relative = segment_row["path"]
            expected_segment_paths.add(relative)
            if write_segments:
                destination = root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(segment)
        source_index = {
            "schema": "CANONICAL-RUNTIME-SOURCE-INDEX-V1",
            "source_id": source_id,
            "canonical_path": source_path,
            "canonical_bytes": source["bytes"],
            "canonical_sha256": source["sha256"],
            "segment_count": len(segment_rows),
            "segments": segment_rows,
            "heading_routes": headings,
        }
        source_index_path = (
            RUNTIME_SEGMENT_ROOT / source_id / "index.json"
        ).as_posix()
        expected_segment_paths.add(source_index_path)
        if write_segments:
            atomic_write_json(root / source_index_path, source_index)
        source_rows.append(
            {
                "source_id": source_id,
                "canonical_path": source_path,
                "canonical_bytes": source["bytes"],
                "canonical_sha256": source["sha256"],
                "segment_count": len(segment_rows),
                "runtime_index_path": source_index_path,
                "runtime_index_sha256": object_sha256(source_index),
            }
        )
        total_segments += len(segment_rows)

    if write_segments:
        runtime_root = root / RUNTIME_SEGMENT_ROOT
        actual_paths = {
            path.relative_to(root).as_posix()
            for path in runtime_root.rglob("*")
            if path.is_file()
        }
        for stale in sorted(actual_paths - expected_segment_paths):
            (root / stale).unlink()

    return {
        "schema": RUNTIME_MANIFEST_SCHEMA,
        "repository": "chinaneedM/ziwei-bazi-model",
        "ref": "main",
        "authority": {
            "canonical_manifest_path": CANONICAL_MANIFEST_PATH.as_posix(),
            "canonical_manifest_sha256": object_sha256(canonical_manifest),
            "canonical_path_prefix": "sources/canonical/",
            "runtime_view_role": "LOSSLESS_READ_VIEW_NOT_INDEPENDENT_AUTHORITY",
            "derivation": "UTF8_LINE_PRESERVING_EXACT_CONCATENATION",
        },
        "max_segment_bytes": MAX_SEGMENT_BYTES,
        "source_count": len(source_rows),
        "segment_count": total_segments,
        "sources": source_rows,
    }


def write_canonical_runtime(root: Path) -> dict[str, Any]:
    manifest = build_canonical_runtime_manifest(root, write_segments=True)
    atomic_write_json(root.resolve() / RUNTIME_MANIFEST_PATH, manifest)
    return manifest


def validate_canonical_runtime(root: Path) -> dict[str, Any]:
    root = root.resolve()
    committed = load_json(root / RUNTIME_MANIFEST_PATH)
    expected = build_canonical_runtime_manifest(root)
    if committed != expected:
        raise TrainingError(
            "canonical runtime segments or manifest are stale relative to canonical S00-S19"
        )

    expected_paths: set[str] = set()
    for source in committed["sources"]:
        source_index_path = source["runtime_index_path"]
        expected_paths.add(source_index_path)
        source_index = load_json(root / source_index_path)
        if object_sha256(source_index) != source["runtime_index_sha256"]:
            raise TrainingError(
                f"canonical runtime source index mismatch: {source['source_id']}"
            )
        if (
            source_index.get("source_id") != source["source_id"]
            or source_index.get("canonical_path") != source["canonical_path"]
            or source_index.get("canonical_bytes") != source["canonical_bytes"]
            or source_index.get("canonical_sha256") != source["canonical_sha256"]
            or source_index.get("segment_count") != source["segment_count"]
        ):
            raise TrainingError(
                f"canonical runtime source index binding mismatch: {source['source_id']}"
            )
        reconstructed: list[bytes] = []
        for segment in source_index["segments"]:
            path = segment["path"]
            expected_paths.add(path)
            payload = (root / path).read_bytes()
            if (
                len(payload) != segment["bytes"]
                or len(payload) > committed["max_segment_bytes"]
                or _sha256_bytes(payload) != segment["sha256"]
            ):
                raise TrainingError(f"canonical runtime segment mismatch: {path}")
            reconstructed.append(payload)
        combined = b"".join(reconstructed)
        if (
            len(combined) != source["canonical_bytes"]
            or _sha256_bytes(combined) != source["canonical_sha256"]
        ):
            raise TrainingError(
                f"canonical runtime reconstruction mismatch: {source['source_id']}"
            )

    actual_paths = {
        path.relative_to(root).as_posix()
        for path in (root / RUNTIME_SEGMENT_ROOT).rglob("*")
        if path.is_file()
    }
    if actual_paths != expected_paths:
        raise TrainingError("canonical runtime segment set is incomplete or contains extras")
    return committed
