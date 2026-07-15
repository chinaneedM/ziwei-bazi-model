from __future__ import annotations

import random
import re
from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, immutable_copy, read_json, sha256_bytes, sha256_file, utc_now

LIB_RE = re.compile(r"(?<![A-Z0-9])S(0\d|1\d)(?!\d)", re.IGNORECASE)
HEX64_RE = re.compile(r"\b[0-9a-fA-F]{64}\b")


def discover_sources(source_dir: str | Path) -> dict[str, list[Path]]:
    found: dict[str, list[Path]] = {}
    for path in sorted(Path(source_dir).iterdir()):
        if not path.is_file():
            continue
        match = LIB_RE.search(path.name)
        if match:
            found.setdefault(f"S{match.group(1)}".upper(), []).append(path)
    return found


def _encoding_checks(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
        encoding = "UTF8_VALID"
    except UnicodeDecodeError as exc:
        return {"status": "FAIL", "encoding": "UTF8_INVALID", "error": str(exc)}
    lines = text.splitlines()
    longest = max((len(line.encode("utf-8")) for line in lines), default=0)
    chinese = sum(1 for char in text if "\u4e00" <= char <= "\u9fff")
    return {
        "status": "PASS",
        "encoding": encoding,
        "line_count": len(lines),
        "max_line_bytes": longest,
        "contains_chinese": chinese > 0,
        "nul_bytes": data.count(b"\x00"),
    }


def _sample_receipts(path: Path, seed: str) -> list[dict[str, Any]]:
    data = path.read_bytes()
    if not data:
        return []
    window = min(256, len(data))
    points = [0, max(0, len(data) // 2 - window // 2), max(0, len(data) - window)]
    rng = random.Random(seed)
    if len(data) > window:
        points.append(rng.randrange(0, len(data) - window + 1))
    receipts = []
    for offset in dict.fromkeys(points):
        chunk = data[offset:offset + window]
        receipts.append({"offset": offset, "bytes": len(chunk), "sha256": sha256_bytes(chunk)})
    return receipts


def _control_root(text: str, expected: str) -> dict[str, Any]:
    count = text.count(expected)
    return {"expected": expected, "occurrences": count, "status": "PASS" if count >= 1 else "FAIL"}


def _extract_binding_table(s19_text: str) -> tuple[str | None, list[dict[str, Any]], str | None]:
    marker_pairs = [
        ("BEGIN_ACTIVE_BINDING_TABLE", "END_ACTIVE_BINDING_TABLE"),
        ("ACTIVE_BINDING_TABLE_BEGIN", "ACTIVE_BINDING_TABLE_END"),
        ("BEGIN S00-S18 ACTIVE BINDING TABLE", "END S00-S18 ACTIVE BINDING TABLE"),
    ]
    block = None
    for begin, end in marker_pairs:
        start = s19_text.find(begin)
        finish = s19_text.find(end, start + len(begin)) if start >= 0 else -1
        if start >= 0 and finish >= 0:
            block = s19_text[start + len(begin):finish].strip("\r\n")
            break
    rows: list[dict[str, Any]] = []
    if block is not None:
        for line_no, line in enumerate(block.splitlines(), 1):
            lib = LIB_RE.search(line)
            hashes = HEX64_RE.findall(line)
            byte_match = re.search(r"(?:BYTE(?:S|_COUNT)?|SIZE)\s*[:=]\s*(\d+)", line, re.I)
            if lib and hashes:
                rows.append({
                    "library_id": f"S{lib.group(1)}".upper(),
                    "sha256": hashes[0].lower(),
                    "bytes": int(byte_match.group(1)) if byte_match else None,
                    "line": line_no,
                })
    declared = None
    match = re.search(r"(?:ACTIVE_BINDING_TABLE_SHA256|S19_ACTIVE_BINDING_TABLE_SHA256)\s*[:=]\s*([0-9a-fA-F]{64})", s19_text)
    if match:
        declared = match.group(1).lower()
    return block, rows, declared


def audit_sources(source_dir: str | Path, config_path: str | Path, report_path: str | Path) -> dict[str, Any]:
    config = read_json(config_path)
    discovered = discover_sources(source_dir)
    required = config["required_libraries"]
    missing = [lib for lib in required if lib not in discovered]
    duplicates = {lib: [str(p) for p in paths] for lib, paths in discovered.items() if len(paths) != 1}
    files: dict[str, Any] = {}
    for lib, paths in discovered.items():
        files[lib] = []
        for path in paths:
            files[lib].append({
                "path": str(path), "sha256": sha256_file(path), "bytes": path.stat().st_size,
                "encoding": _encoding_checks(path), "samples": _sample_receipts(path, f"{lib}:{path.name}"),
            })

    control: dict[str, Any] = {}
    for lib, expected in config["expected_control_roots"].items():
        if len(discovered.get(lib, [])) == 1:
            text = discovered[lib][0].read_text(encoding="utf-8")
            control[lib] = _control_root(text, expected)
        else:
            control[lib] = {"expected": expected, "occurrences": 0, "status": "FAIL", "reason": "MISSING_OR_DUPLICATE"}

    binding: dict[str, Any] = {"status": "FAIL", "reason": "S19_MISSING_OR_DUPLICATE"}
    if len(discovered.get("S19", [])) == 1:
        s19_text = discovered["S19"][0].read_text(encoding="utf-8")
        block, rows, declared = _extract_binding_table(s19_text)
        row_map = {row["library_id"]: row for row in rows}
        comparisons = []
        for lib in [f"S{i:02d}" for i in range(19)]:
            actual = files.get(lib, [{}])[0] if len(files.get(lib, [])) == 1 else None
            declared_row = row_map.get(lib)
            comparisons.append({
                "library_id": lib,
                "declared": declared_row,
                "actual": None if actual is None else {"sha256": actual["sha256"], "bytes": actual["bytes"]},
                "status": "PASS" if actual and declared_row and declared_row["sha256"] == actual["sha256"] and
                (declared_row["bytes"] is None or declared_row["bytes"] == actual["bytes"]) else "FAIL",
            })
        computed = sha256_bytes(block.encode("utf-8")) if block is not None else None
        expected_hash = config["expected_s19_binding_hash"]
        binding = {
            "markers_found": block is not None, "row_count": len(rows), "rows": comparisons,
            "declared_hash": declared, "computed_block_hash": computed, "expected_hash": expected_hash,
            "hash_status": "PASS" if declared == expected_hash and computed == expected_hash else "FAIL",
        }
        binding["status"] = "PASS" if binding["hash_status"] == "PASS" and all(r["status"] == "PASS" for r in comparisons) else "FAIL"

    index_scope_ok = "S19" not in config["knowledge_index_scope"] and config["knowledge_index_scope"] == [f"S{i:02d}" for i in range(1, 19)]
    overall = not missing and not duplicates and all(v["status"] == "PASS" for v in control.values()) and binding["status"] == "PASS" and index_scope_ok
    report = {
        "schema": "SOURCE-AUDIT-REPORT-V1", "generated_at": utc_now(), "source_dir": str(Path(source_dir)),
        "required_count": len(required), "unique_library_count": len(discovered), "missing": missing,
        "duplicates": duplicates, "files": files, "control_roots": control, "binding_table": binding,
        "s00_index_scope": config["knowledge_index_scope"], "s00_excludes_s19": index_scope_ok,
        "status": "PASS" if overall else "HOLD_SOURCE_BASELINE_UNVERIFIED",
    }
    atomic_write_json(report_path, report, overwrite=True)
    return report


def migrate_verified_sources(audit_report_path: str | Path, destination: str | Path) -> dict[str, Any]:
    report = read_json(audit_report_path)
    if report["status"] != "PASS":
        raise FortuneError("source audit has not passed", status="HOLD_SOURCE_BASELINE_UNVERIFIED")
    dest = Path(destination)
    receipts = []
    for lib in [f"S{i:02d}" for i in range(20)]:
        item = report["files"][lib][0]
        source = Path(item["path"])
        suffix = source.suffix.lower() or ".txt"
        receipt = immutable_copy(source, dest / f"{lib}{suffix}")
        receipt["library_id"] = lib
        receipts.append(receipt)
    manifest = {"schema": "IMMUTABLE-SOURCE-BASELINE-V1", "created_at": utc_now(), "files": receipts}
    atomic_write_json(dest / "manifest.json", manifest)
    return manifest

