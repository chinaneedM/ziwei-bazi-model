from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterable

from .util import FortuneError, atomic_write_json, read_json, sha256_bytes, sha256_file, utc_now

LIB_RE = re.compile(r"(?<![A-Z0-9])S(0\d|1\d)(?!\d)", re.I)
CLAUSE_PATTERNS = {
    "conditions": re.compile(r"(?:若|当|如|须|必须|只有|条件|前提)[^。；;\n]*"),
    "negations": re.compile(r"(?:不得|不能|不可|不等于|并非|无)[^。；;\n]*"),
    "limitations": re.compile(r"(?:仅|只限|上限|限制|不足以|至多)[^。；;\n]*"),
    "exceptions": re.compile(r"(?:除非|例外|但若|然而)[^。；;\n]*"),
    "alternatives": re.compile(r"(?:否则|亦可能|替代|另一|或为)[^。；;\n]*"),
}


def _paragraphs(data: bytes) -> Iterable[tuple[int, int, int, int, str]]:
    """Yield exact UTF-8 paragraph byte and line ranges without normalizing bytes."""
    text = data.decode("utf-8")
    byte_cursor = 0
    line_cursor = 1
    current: list[str] = []
    start_byte = 0
    start_line = 1
    for line in text.splitlines(keepends=True):
        encoded = line.encode("utf-8")
        if line.strip():
            if not current:
                start_byte, start_line = byte_cursor, line_cursor
            current.append(line)
        elif current:
            segment = "".join(current)
            yield start_byte, byte_cursor, start_line, line_cursor - 1, segment
            current = []
        byte_cursor += len(encoded)
        line_cursor += 1
    if current:
        segment = "".join(current)
        yield start_byte, len(data), start_line, line_cursor - 1, segment


def build_locator_index(source_dir: str | Path, binding_hash: str, output_path: str | Path,
                        git_commit: str | None = None) -> dict[str, Any]:
    source_root = Path(source_dir)
    sources, entries = [], []
    for path in sorted(source_root.iterdir()):
        if not path.is_file() or path.name == "manifest.json":
            continue
        match = LIB_RE.search(path.name)
        if not match:
            continue
        lib = f"S{match.group(1)}".upper()
        if lib == "S00" or lib == "S19":
            continue
        data = path.read_bytes()
        digest = sha256_bytes(data)
        sources.append({"library_id": lib, "path": str(path), "sha256": digest, "bytes": len(data), "git_commit": git_commit})
        for ordinal, (b0, b1, l0, l1, segment) in enumerate(_paragraphs(data), 1):
            normalized = " ".join(segment.split())
            if not normalized:
                continue
            root_atom = re.split(r"[。；;]", normalized, maxsplit=1)[0][:240]
            entry = {
                "entry_id": f"{lib}-P{ordinal:07d}", "library_id": lib, "source_path": str(path),
                "source_sha256": digest, "source_git_commit": git_commit, "root_atom": root_atom,
                "parent_segment": {"sha256": sha256_bytes(segment.encode("utf-8")), "locator": "EXACT_SOURCE_BYTE_RANGE"},
                "line_start": l0, "line_end": l1, "byte_start": b0, "byte_end": b1,
            }
            for key, pattern in CLAUSE_PATTERNS.items():
                entry[key] = pattern.findall(segment)
            entries.append(entry)
    result = {
        "schema": "KNOWLEDGE-LOCATOR-INDEX-V1", "binding_hash": binding_hash,
        "generated_at": utc_now(), "sources": sources, "entries": entries,
        "scope": [f"S{i:02d}" for i in range(1, 19)], "s19_indexed": False,
    }
    atomic_write_json(output_path, result)
    return result


def read_parent_segment(index_path: str | Path, entry_id: str) -> dict[str, Any]:
    index = read_json(index_path)
    matches = [e for e in index["entries"] if e["entry_id"] == entry_id]
    if len(matches) != 1:
        raise FortuneError(f"entry not unique: {entry_id}", status="SOURCE_ENTRY_NOT_FOUND")
    entry = matches[0]
    path = Path(entry["source_path"])
    if sha256_file(path) != entry["source_sha256"]:
        raise FortuneError("source hash changed", status="SOURCE_HASH_MISMATCH")
    data = path.read_bytes()[entry["byte_start"]:entry["byte_end"]]
    if sha256_bytes(data) != entry["parent_segment"]["sha256"]:
        raise FortuneError("parent segment hash mismatch", status="PARENT_SEGMENT_HASH_MISMATCH")
    return {
        "schema": "SOURCE-PARENT-SEGMENT-READ-V1", "entry_id": entry_id,
        "library_id": entry["library_id"], "source_path": entry["source_path"],
        "source_sha256": entry["source_sha256"], "source_git_commit": entry.get("source_git_commit"),
        "byte_start": entry["byte_start"], "byte_end": entry["byte_end"],
        "line_start": entry["line_start"], "line_end": entry["line_end"],
        "parent_segment_sha256": sha256_bytes(data), "text": data.decode("utf-8"),
        "conditions": entry["conditions"], "negations": entry["negations"],
        "limitations": entry["limitations"], "exceptions": entry["exceptions"], "alternatives": entry["alternatives"],
    }


def validate_locator_index(index_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    index = read_json(index_path)
    source_by_path = {row["path"]: row for row in index["sources"]}
    cached: dict[str, bytes] = {}
    source_checks = []
    failures = []
    for path_text, source in source_by_path.items():
        path = Path(path_text)
        if not path.is_file():
            failures.append({"source_path": path_text, "rule": "PARENT_FILE_MISSING"})
            continue
        data = path.read_bytes()
        cached[path_text] = data
        actual_hash = sha256_bytes(data)
        passed = actual_hash == source["sha256"] and len(data) == source["bytes"]
        source_checks.append({"library_id": source["library_id"], "source_path": path_text,
                              "actual_sha256": actual_hash, "expected_sha256": source["sha256"],
                              "actual_bytes": len(data), "expected_bytes": source["bytes"],
                              "status": "PASS" if passed else "FAIL"})
        if not passed:
            failures.append({"source_path": path_text, "rule": "PARENT_FILE_HASH_OR_SIZE_MISMATCH"})
    entry_checks = 0
    for entry in index["entries"]:
        data = cached.get(entry["source_path"])
        if data is None:
            failures.append({"entry_id": entry["entry_id"], "rule": "PARENT_FILE_UNAVAILABLE"})
            continue
        start, end = entry["byte_start"], entry["byte_end"]
        range_valid = isinstance(start, int) and isinstance(end, int) and 0 <= start < end <= len(data)
        if not range_valid:
            failures.append({"entry_id": entry["entry_id"], "rule": "BYTE_RANGE_INVALID"})
            continue
        segment = data[start:end]
        if sha256_bytes(segment) != entry["parent_segment"]["sha256"]:
            failures.append({"entry_id": entry["entry_id"], "rule": "PARENT_SEGMENT_READBACK_HASH_MISMATCH"})
            continue
        entry_checks += 1
    result = {"schema": "KNOWLEDGE-LOCATOR-INDEX-VALIDATION-V1", "index_path": str(Path(index_path)),
              "index_sha256": sha256_file(index_path), "binding_hash": index["binding_hash"],
              "source_count": len(index["sources"]), "source_checks": source_checks,
              "entry_count": len(index["entries"]), "entries_checked": entry_checks,
              "byte_ranges_checked": entry_checks, "parent_segments_read_back": entry_checks,
              "s19_indexed": index.get("s19_indexed"), "failures": failures,
              "status": "PASS" if not failures and entry_checks == len(index["entries"]) else "FAIL"}
    atomic_write_json(output_path, result, overwrite=True)
    return result
