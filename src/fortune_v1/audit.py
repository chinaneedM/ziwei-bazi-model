from __future__ import annotations

import json
import random
import re
import stat
import zipfile
from collections import defaultdict
from pathlib import Path, PurePosixPath
from typing import Any

from .util import FortuneError, atomic_write_json, immutable_copy, read_json, sha256_bytes, sha256_file, utc_now

LIBRARY_IDS = [f"S{i:02d}" for i in range(20)]
BINDING_LIBRARY_IDS = LIBRARY_IDS[:19]
LIBRARY_ID_LINE_RE = re.compile(r"(?m)^LIBRARY_ID=(S(?:0\d|1\d))\s*$")
PATCH_ID_LINE_RE = re.compile(r"(?m)^PATCH_ID=([^\r\n]+)\s*$")
BINDING_HEADER = "LIBRARY_ID\tACTIVE_FILE_ID\tCANONICAL_FILENAME\tSHA256_RAW_FILE_BYTES\tFILE_SIZE_BYTES"


def _evidence(path: str | Path, field_path: str, actual: Any, expected: Any,
              status: str, commit_sha: str | None = None) -> dict[str, Any]:
    p = Path(path)
    return {
        "real_path": str(p), "file_sha256": sha256_file(p) if p.is_file() else None,
        "object_field_path": field_path, "actual": actual, "expected": expected,
        "difference": None if actual == expected else {"actual": actual, "expected": expected},
        "status": status, "corresponding_commit_sha": commit_sha,
    }


def _active_library_id(data: bytes, path: str | Path) -> tuple[str, int]:
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise FortuneError(f"UTF-8 source required: {path}: {exc}", status="SOURCE_UTF8_INVALID") from exc
    matches = LIBRARY_ID_LINE_RE.findall(text)
    if not matches:
        raise FortuneError(f"no internal LIBRARY_ID: {path}", status="LIBRARY_ID_MISSING")
    library_id = matches[0]
    if library_id not in LIBRARY_IDS:
        raise FortuneError(f"invalid internal LIBRARY_ID: {library_id}", status="LIBRARY_ID_INVALID")
    return library_id, len(matches)


def _active_patch_id(text: str) -> str | None:
    match = PATCH_ID_LINE_RE.search(text)
    return match.group(1).strip() if match else None


def _encoding_checks(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        return {"status": "FAIL", "encoding": "UTF8_INVALID", "error": str(exc)}
    lines = text.splitlines()
    return {
        "status": "PASS", "encoding": "UTF8_VALID", "line_count": len(lines),
        "max_line_bytes": max((len(line.encode("utf-8")) for line in lines), default=0),
        "contains_chinese": any("\u4e00" <= char <= "\u9fff" for char in text),
        "nul_bytes": data.count(b"\x00"), "bom": data.startswith(b"\xef\xbb\xbf"),
        "crlf_count": data.count(b"\r\n"), "lf_count": data.count(b"\n"),
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
    return [{"offset": offset, "bytes": len(data[offset:offset + window]),
             "sha256": sha256_bytes(data[offset:offset + window])} for offset in dict.fromkeys(points)]


def _parse_active_binding_table(s19_text: str) -> dict[str, Any]:
    lines = s19_text.splitlines()
    header_indexes = [i for i, line in enumerate(lines) if line == BINDING_HEADER]
    if not header_indexes:
        raise FortuneError("active S19 binding header missing", status="S19_BINDING_TABLE_MISSING")
    header_index = header_indexes[0]
    rows: list[dict[str, Any]] = []
    for position, line in enumerate(lines[header_index + 1:header_index + 20]):
        columns = line.split("\t")
        if len(columns) != 5:
            raise FortuneError(f"invalid S19 binding row: {line!r}", status="S19_BINDING_ROW_INVALID")
        library_id, active_file_id, canonical_filename, digest, size = columns
        expected_id = f"S{position:02d}"
        if library_id != expected_id or not re.fullmatch(r"[0-9a-f]{64}", digest) or not size.isdigit():
            raise FortuneError(f"invalid S19 binding row: {line!r}", status="S19_BINDING_ROW_INVALID")
        rows.append({"library_id": library_id, "active_file_id": active_file_id,
                     "canonical_filename": canonical_filename, "sha256_raw_file_bytes": digest,
                     "file_size_bytes": int(size), "source_line_number": header_index + 2 + position,
                     "raw_line": line})
    normalized = BINDING_HEADER + "\n" + "\n".join(row["raw_line"] for row in rows) + "\n"
    declared = re.findall(r"(?m)^ACTIVE_BINDING_TABLE_SHA256_UTF8_LF=([0-9a-f]{64})\s*$", s19_text)
    methods = re.findall(r"(?m)^ACTIVE_BINDING_TABLE_HASH_METHOD=([^\r\n]+)\s*$", s19_text)
    return {"header": BINDING_HEADER, "header_line_number": header_index + 1, "rows": rows,
            "normalized_utf8_lf_trailing_lf": normalized,
            "computed_sha256_utf8_lf": sha256_bytes(normalized.encode("utf-8")),
            "declared_sha256_utf8_lf": declared[0] if declared else None,
            "declared_hash_occurrences": len(declared), "hash_method": methods[0] if methods else None,
            "historical_table_header_count": len(header_indexes)}


def _safe_member(info: zipfile.ZipInfo) -> PurePosixPath:
    path = PurePosixPath(info.filename.replace("\\", "/"))
    mode = info.external_attr >> 16
    if path.is_absolute() or ".." in path.parts or any("\x00" in part for part in path.parts):
        raise FortuneError(f"unsafe source package member: {info.filename}", status="ARCHIVE_MEMBER_REJECTED")
    if stat.S_ISLNK(mode):
        raise FortuneError(f"source package symlink rejected: {info.filename}", status="ARCHIVE_MEMBER_REJECTED")
    if info.flag_bits & 0x1:
        raise FortuneError(f"encrypted source package member: {info.filename}", status="ARCHIVE_ENCRYPTED_MEMBER")
    return path


def _write_read_only(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != data:
        raise FortuneError(f"immutable path collision: {path}", status="IMMUTABLE_OBJECT_EXISTS")
    if not path.exists():
        path.write_bytes(data)
    path.chmod(0o400)


def _inventory_directory(source_dir: str | Path) -> dict[str, list[dict[str, Any]]]:
    found: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for path in sorted(Path(source_dir).iterdir()):
        if not path.is_file() or path.name.endswith(".json"):
            continue
        data = path.read_bytes()
        library_id, occurrences = _active_library_id(data, path)
        found[library_id].append({"path": path, "library_id": library_id,
                                  "library_id_occurrences": occurrences,
                                  "sha256": sha256_bytes(data), "bytes": len(data)})
    return dict(found)


def audit_sources(source_dir: str | Path, config_path: str | Path, report_path: str | Path,
                  *, commit_sha: str | None = None) -> dict[str, Any]:
    config = read_json(config_path)
    discovered = _inventory_directory(source_dir)
    missing = [lib for lib in LIBRARY_IDS if lib not in discovered]
    duplicates = {lib: [str(row["path"]) for row in rows] for lib, rows in discovered.items() if len(rows) != 1}
    files: dict[str, list[dict[str, Any]]] = {}
    for lib, rows in discovered.items():
        files[lib] = []
        for row in rows:
            path = row["path"]
            files[lib].append({"path": str(path), "canonical_filename": path.name,
                               "library_id": lib, "library_id_readback": row["library_id"],
                               "library_id_occurrences": row["library_id_occurrences"],
                               "sha256": row["sha256"], "bytes": row["bytes"],
                               "encoding": _encoding_checks(path),
                               "samples": _sample_receipts(path, f"{lib}:{row['sha256']}"),
                               "corresponding_commit_sha": commit_sha})
    control: dict[str, Any] = {}
    for lib, expected in config["expected_control_roots"].items():
        if len(discovered.get(lib, [])) != 1:
            control[lib] = {"expected": expected, "occurrences": 0, "status": "FAIL", "reason": "MISSING_OR_DUPLICATE"}
            continue
        path = discovered[lib][0]["path"]
        text = path.read_text(encoding="utf-8")
        occurrences = len(re.findall(rf"(?m)^PATCH_ID={re.escape(expected)}\s*$", text))
        actual = _active_patch_id(text)
        passed = occurrences == 1 and actual == expected
        control[lib] = {"expected": expected, "actual_active_patch_id": actual,
                        "occurrences": occurrences, "status": "PASS" if passed else "FAIL",
                        "evidence": _evidence(path, f"control_roots.{lib}.PATCH_ID", actual, expected,
                                              "PASS" if passed else "FAIL", commit_sha)}
    binding: dict[str, Any] = {"status": "FAIL", "reason": "S19_MISSING_OR_DUPLICATE"}
    if len(discovered.get("S19", [])) == 1:
        s19_path = discovered["S19"][0]["path"]
        parsed = _parse_active_binding_table(s19_path.read_text(encoding="utf-8"))
        row_map = {row["library_id"]: row for row in parsed["rows"]}
        comparisons = []
        for lib in BINDING_LIBRARY_IDS:
            declared = row_map.get(lib)
            actual = files.get(lib, [None])[0] if len(files.get(lib, [])) == 1 else None
            actual_tuple = None if not actual else {"library_id": actual["library_id_readback"],
                                                     "canonical_filename": actual["canonical_filename"],
                                                     "sha256_raw_file_bytes": actual["sha256"],
                                                     "file_size_bytes": actual["bytes"]}
            expected_tuple = None if not declared else {"library_id": declared["library_id"],
                                                         "canonical_filename": declared["canonical_filename"],
                                                         "sha256_raw_file_bytes": declared["sha256_raw_file_bytes"],
                                                         "file_size_bytes": declared["file_size_bytes"]}
            passed = actual_tuple == expected_tuple
            comparisons.append({"library_id": lib, "declared": expected_tuple, "actual": actual_tuple,
                                "difference": None if passed else {"actual": actual_tuple, "expected": expected_tuple},
                                "status": "PASS" if passed else "FAIL",
                                "evidence": None if not actual else _evidence(actual["path"], f"binding_table.rows.{lib}",
                                                                             actual_tuple, expected_tuple,
                                                                             "PASS" if passed else "FAIL", commit_sha)})
        expected_hash = config["expected_s19_binding_hash"]
        hash_pass = parsed["declared_sha256_utf8_lf"] == expected_hash and parsed["computed_sha256_utf8_lf"] == expected_hash
        binding = {**{k: v for k, v in parsed.items() if k != "normalized_utf8_lf_trailing_lf"},
                   "expected_sha256_utf8_lf": expected_hash, "rows": comparisons,
                   "hash_status": "PASS" if hash_pass else "FAIL",
                   "status": "PASS" if hash_pass and all(row["status"] == "PASS" for row in comparisons) else "FAIL",
                   "evidence": _evidence(s19_path, "binding_table.computed_sha256_utf8_lf",
                                         parsed["computed_sha256_utf8_lf"], expected_hash,
                                         "PASS" if hash_pass else "FAIL", commit_sha)}
    index_scope_ok = config["knowledge_index_scope"] == [f"S{i:02d}" for i in range(1, 19)]
    encodings_ok = all(row["encoding"]["status"] == "PASS" for rows in files.values() for row in rows)
    overall = not missing and not duplicates and encodings_ok and index_scope_ok and all(
        row["status"] == "PASS" for row in control.values()) and binding.get("status") == "PASS"
    report = {"schema": "SOURCE-AUDIT-REPORT-V2", "generated_at": utc_now(),
              "source_dir": str(Path(source_dir)),
              "identity_rule": "INTERNAL_LIBRARY_ID+RAW_SHA256+FILE_SIZE+ACTIVE_S19_BINDING",
              "transport_filename_is_identity": False, "required_count": 20,
              "unique_library_count": len(discovered), "missing": missing, "duplicates": duplicates,
              "files": files, "control_roots": control, "binding_table": binding,
              "s00_index_scope": config["knowledge_index_scope"], "s00_excludes_s19": index_scope_ok,
              "migration_permission": "YES" if overall else "NO",
              "baseline_tag_permission": "YES" if overall else "NO",
              "installed_validated_permission": "NO", "corresponding_commit_sha": commit_sha,
              "status": "PASS" if overall else "HOLD_SOURCE_BASELINE_UNVERIFIED"}
    atomic_write_json(report_path, report, overwrite=True)
    return report


def migrate_verified_sources(audit_report_path: str | Path, destination: str | Path,
                             receipt_path: str | Path | None = None,
                             *, baseline_commit_sha: str | None = None,
                             baseline_tag: str | None = None) -> dict[str, Any]:
    report = read_json(audit_report_path)
    if report.get("status") != "PASS" or report.get("migration_permission") != "YES":
        raise FortuneError("source audit has not passed", status="HOLD_SOURCE_BASELINE_UNVERIFIED")
    dest = Path(destination)
    receipts = []
    for lib in LIBRARY_IDS:
        item = report["files"][lib][0]
        source, target = Path(item["path"]), dest / item["canonical_filename"]
        copy = immutable_copy(source, target)
        copy.update({"library_id": lib, "canonical_filename": item["canonical_filename"],
                     "source_path": str(source),
                     "status": "MIGRATED" if copy["sha256"] == item["sha256"] and copy["bytes"] == item["bytes"] else "FAIL"})
        receipts.append(copy)
    passed = all(row["status"] == "MIGRATED" for row in receipts)
    receipt = {"schema": "SOURCE-MIGRATION-RECEIPT-V2", "created_at": utc_now(),
               "audit_report_path": str(Path(audit_report_path)), "audit_report_sha256": sha256_file(audit_report_path),
               "destination": str(dest), "files": receipts, "baseline_commit_sha": baseline_commit_sha,
               "baseline_tag": baseline_tag, "source_file_count": len(receipts),
               "migration_permission": "YES" if passed else "NO", "installed_validated_permission": "NO",
               "status": "MIGRATED" if passed else "FAIL"}
    atomic_write_json(Path(receipt_path) if receipt_path else dest / "migration-receipt.json", receipt, overwrite=True)
    return receipt


def import_source_package(package_path: str | Path, expected_zip_sha256: str,
                          config_path: str | Path, work_root: str | Path,
                          reports_dir: str | Path, migrate_destination: str | Path | None = None,
                          *, commit_sha: str | None = None) -> dict[str, Any]:
    package, work_root, reports_dir = Path(package_path), Path(work_root), Path(reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    actual_package_sha = sha256_file(package)
    if actual_package_sha != expected_zip_sha256:
        raise FortuneError("source ZIP SHA256 mismatch", status="SOURCE_PACKAGE_SHA256_MISMATCH")
    if not zipfile.is_zipfile(package):
        raise FortuneError("source package is not a ZIP", status="UNSUPPORTED_ARCHIVE_FORMAT")
    raw_package_root = (Path(migrate_destination).parent / "source-packages") if migrate_destination is not None else (work_root / "raw-package")
    raw_package = raw_package_root / "fortune-source-baseline-S00-S19-R16.zip"
    if raw_package.exists() and sha256_file(raw_package) != actual_package_sha:
        raise FortuneError("raw source package collision", status="IMMUTABLE_OBJECT_EXISTS")
    if not raw_package.exists():
        immutable_copy(package, raw_package)
    raw_package.chmod(0o400)
    raw_members_root = work_root / "raw-members"
    member_records: list[dict[str, Any]] = []
    seen_names: set[str] = set()
    package_manifest: dict[str, Any] | None = None
    total_uncompressed = 0
    with zipfile.ZipFile(package, "r") as archive:
        for info in sorted(archive.infolist(), key=lambda row: row.filename):
            if info.is_dir():
                continue
            member = _safe_member(info)
            folded = member.as_posix().casefold()
            if folded in seen_names:
                raise FortuneError(f"duplicate source ZIP member: {member}", status="ARCHIVE_DUPLICATE_MEMBER")
            seen_names.add(folded)
            total_uncompressed += info.file_size
            if total_uncompressed > 512 * 1024 * 1024:
                raise FortuneError("source ZIP uncompressed limit exceeded", status="ARCHIVE_SIZE_LIMIT")
            if info.compress_size and info.file_size / info.compress_size > 500:
                raise FortuneError(f"suspicious compression ratio: {member}", status="ARCHIVE_BOMB_REJECTED")
            data = archive.read(info)
            if len(data) != info.file_size:
                raise FortuneError(f"source member size mismatch: {member}", status="ARCHIVE_SIZE_MISMATCH")
            raw_member_path = raw_members_root.joinpath(*member.parts)
            _write_read_only(raw_member_path, data)
            record: dict[str, Any] = {"transport_member_name": member.as_posix(),
                                      "raw_member_path": str(raw_member_path),
                                      "sha256_raw_file_bytes": sha256_bytes(data), "file_size_bytes": len(data),
                                      "compressed_size_bytes": info.compress_size, "crc32": f"{info.CRC:08x}",
                                      "status": "RAW_READ_ONLY"}
            if member.parts and member.parts[0] == "sources":
                lib, occurrences = _active_library_id(data, member.as_posix())
                record.update({"library_id": lib, "library_id_occurrences": occurrences,
                               "active_patch_id": _active_patch_id(data.decode("utf-8"))})
            elif member.as_posix() == "source-baseline-manifest.json":
                package_manifest = json.loads(data.decode("utf-8"))
            member_records.append(record)
    if package_manifest is None:
        raise FortuneError("source-baseline-manifest.json missing", status="SOURCE_PACKAGE_MANIFEST_MISSING")
    manifest_by_lib = {row["library_id"]: row for row in package_manifest.get("files", [])}
    config = read_json(config_path)
    candidates: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in member_records:
        if record.get("library_id"):
            candidates[record["library_id"]].append(record)
    s19_manifest = manifest_by_lib.get("S19")
    s19_candidates = [row for row in candidates.get("S19", []) if s19_manifest and
                      row["sha256_raw_file_bytes"] == s19_manifest["sha256"] and
                      row["file_size_bytes"] == s19_manifest["size_bytes"] and
                      row.get("active_patch_id") == config["expected_control_roots"]["S19"]]
    if len(s19_candidates) != 1:
        raise FortuneError("unique active S19 could not be resolved", status="S19_ACTIVE_VERSION_NOT_UNIQUE")
    active_s19 = s19_candidates[0]
    s19_path = Path(active_s19["raw_member_path"])
    binding = _parse_active_binding_table(s19_path.read_text(encoding="utf-8"))
    binding_rows = {row["library_id"]: row for row in binding["rows"]}
    expected_binding_hash = config["expected_s19_binding_hash"]
    binding_hash_pass = binding["declared_sha256_utf8_lf"] == expected_binding_hash and binding["computed_sha256_utf8_lf"] == expected_binding_hash
    if not binding_hash_pass:
        raise FortuneError("S19 active binding hash mismatch", status="S19_BINDING_HASH_MISMATCH")
    staging, historical = work_root / "staging", work_root / "historical-audit"
    if staging.exists() and any(staging.iterdir()):
        raise FortuneError("clean staging directory required", status="STAGING_NOT_CLEAN")
    staging.mkdir(parents=True, exist_ok=True)
    historical.mkdir(parents=True, exist_ok=True)
    normalization_rows: list[dict[str, Any]] = []
    duplicate_rows: list[dict[str, Any]] = []
    quarantine_rows: list[dict[str, Any]] = []
    for lib in BINDING_LIBRARY_IDS:
        expected, rows = binding_rows[lib], candidates.get(lib, [])
        matching = [row for row in rows if row["sha256_raw_file_bytes"] == expected["sha256_raw_file_bytes"] and row["file_size_bytes"] == expected["file_size_bytes"]]
        if not matching:
            raise FortuneError(f"no {lib} version matches active S19", status="ACTIVE_SOURCE_VERSION_MISSING")
        chosen = sorted(matching, key=lambda row: row["transport_member_name"])[0]
        chosen_bytes = Path(chosen["raw_member_path"]).read_bytes()
        for duplicate in matching[1:]:
            if Path(duplicate["raw_member_path"]).read_bytes() != chosen_bytes:
                raise FortuneError(f"{lib} physical bytes disagree despite claimed match", status="ACTIVE_SOURCE_PHYSICAL_CONFLICT")
            duplicate_rows.append({"library_id": lib, "transport_member_name": duplicate["transport_member_name"],
                                   "duplicate_of": chosen["transport_member_name"],
                                   "sha256": duplicate["sha256_raw_file_bytes"], "bytes": duplicate["file_size_bytes"],
                                   "status": "IDENTICAL_BYTE_DUPLICATE_DEDUPED"})
        target = staging / expected["canonical_filename"]
        copy = immutable_copy(chosen["raw_member_path"], target)
        normalization_rows.append({"library_id": lib, "transport_member_name": chosen["transport_member_name"],
                                   "raw_member_path": chosen["raw_member_path"],
                                   "canonical_filename": expected["canonical_filename"], "staging_path": str(target),
                                   "sha256_raw_file_bytes": copy["sha256"], "file_size_bytes": copy["bytes"],
                                   "status": "ACTIVE_NORMALIZED_COPY"})
        for other in rows:
            if other in matching:
                continue
            qtarget = historical / f"{lib}-{other['sha256_raw_file_bytes'][:16]}-{Path(other['transport_member_name']).name}"
            immutable_copy(other["raw_member_path"], qtarget)
            quarantine_rows.append({"library_id": lib, "transport_member_name": other["transport_member_name"],
                                    "sha256": other["sha256_raw_file_bytes"], "bytes": other["file_size_bytes"],
                                    "historical_path": str(qtarget), "reason": "NOT_MATCHING_ACTIVE_S19_BINDING",
                                    "status": "HISTORICAL_AUDIT_ONLY"})
    s19_target = staging / s19_manifest["canonical_filename"]
    s19_copy = immutable_copy(active_s19["raw_member_path"], s19_target)
    normalization_rows.append({"library_id": "S19", "transport_member_name": active_s19["transport_member_name"],
                               "raw_member_path": active_s19["raw_member_path"],
                               "canonical_filename": s19_manifest["canonical_filename"], "staging_path": str(s19_target),
                               "sha256_raw_file_bytes": s19_copy["sha256"], "file_size_bytes": s19_copy["bytes"],
                               "status": "ACTIVE_NORMALIZED_COPY"})
    for declared in package_manifest.get("excluded_or_quarantined", []):
        quarantine_rows.append({**declared, "status": "DECLARED_HISTORICAL_NOT_PRESENT_IN_ACTIVE_PACKAGE",
                                "historical_path": None})
    raw_manifest = {"schema": "RAW-SOURCE-PACKAGE-MANIFEST-V1", "created_at": utc_now(),
                    "uploaded_transport_name": package.name, "raw_package_path": str(raw_package),
                    "raw_package_sha256": actual_package_sha, "expected_raw_package_sha256": expected_zip_sha256,
                    "raw_package_bytes": package.stat().st_size,
                    "raw_package_read_only": not bool(raw_package.stat().st_mode & stat.S_IWUSR),
                    "member_count": len(member_records), "members": member_records, "status": "PASS",
                    "corresponding_commit_sha": commit_sha}
    normalization = {"schema": "SOURCE-NORMALIZATION-MAP-V1",
                     "identity_rule": "LIBRARY_ID+SHA256_RAW_FILE_BYTES+FILE_SIZE_BYTES+S19_CURRENT_ACTIVE_BINDING_TABLE",
                     "filename_suffix_numbers_are_transport_only": True, "original_files_overwritten_or_renamed": False,
                     "files": sorted(normalization_rows, key=lambda row: row["library_id"]),
                     "status": "PASS" if len(normalization_rows) == 20 else "FAIL",
                     "corresponding_commit_sha": commit_sha}
    duplicates_report = {"schema": "DUPLICATE-AND-QUARANTINE-REPORT-V1",
                         "identical_byte_duplicates": duplicate_rows, "quarantined_or_historical": quarantine_rows,
                         "active_source_count": len(normalization_rows), "status": "PASS",
                         "corresponding_commit_sha": commit_sha}
    raw_manifest_path, normalization_path = reports_dir / "raw-package-manifest.json", reports_dir / "normalization-map.json"
    duplicate_path = reports_dir / "duplicate-and-quarantine-report.json"
    atomic_write_json(raw_manifest_path, raw_manifest, overwrite=True)
    atomic_write_json(normalization_path, normalization, overwrite=True)
    atomic_write_json(duplicate_path, duplicates_report, overwrite=True)
    source_audit_path = reports_dir / "source-audit.json"
    staging_audit_path = reports_dir / "source-audit-staging.json" if migrate_destination is not None else source_audit_path
    source_audit = audit_sources(staging, config_path, staging_audit_path, commit_sha=commit_sha)
    migration = None
    final_s19_path = s19_target
    if migrate_destination is not None:
        if source_audit["status"] != "PASS":
            raise FortuneError("source audit failed; migration denied", status="HOLD_SOURCE_BASELINE_UNVERIFIED")
        migration = migrate_verified_sources(staging_audit_path, migrate_destination,
                                              reports_dir / "migration-receipt.json")
        source_audit = audit_sources(migrate_destination, config_path, source_audit_path, commit_sha=commit_sha)
        final_s19_path = Path(migrate_destination) / s19_manifest["canonical_filename"]
    binding_receipt = {"schema": "BINDING-TABLE-RECOMPUTE-RECEIPT-V1", "s19_path": str(final_s19_path),
                       "s19_sha256": sha256_file(final_s19_path),
                       "object_field_path": "active_binding_table.header_and_S00_to_S18_rows",
                       "hash_method": binding["hash_method"], "row_count": len(binding["rows"]),
                       "declared_sha256_utf8_lf": binding["declared_sha256_utf8_lf"],
                       "computed_sha256_utf8_lf": binding["computed_sha256_utf8_lf"],
                       "expected_sha256_utf8_lf": expected_binding_hash,
                       "difference": None if binding_hash_pass else {"declared": binding["declared_sha256_utf8_lf"],
                                                                    "computed": binding["computed_sha256_utf8_lf"],
                                                                    "expected": expected_binding_hash},
                       "rows": binding["rows"],
                       "status": "PASS" if binding_hash_pass and source_audit["binding_table"]["status"] == "PASS" else "FAIL",
                       "corresponding_commit_sha": commit_sha}
    binding_path = reports_dir / "binding-table-recompute-receipt.json"
    atomic_write_json(binding_path, binding_receipt, overwrite=True)
    return {"schema": "SOURCE-PACKAGE-IMPORT-RESULT-V1", "raw_package_manifest": str(raw_manifest_path),
            "normalization_map": str(normalization_path), "duplicate_and_quarantine_report": str(duplicate_path),
            "source_audit": str(source_audit_path), "binding_table_recompute_receipt": str(binding_path),
            "migration_receipt": str(reports_dir / "migration-receipt.json") if migration else None,
            "status": "PASS" if source_audit["status"] == "PASS" and binding_receipt["status"] == "PASS" else "FAIL"}
