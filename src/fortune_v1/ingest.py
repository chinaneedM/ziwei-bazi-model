from __future__ import annotations

import os
import re
import shutil
import stat
import zipfile
from collections import defaultdict
from pathlib import Path, PurePosixPath
from typing import Any

from .util import FortuneError, atomic_write_json, ensure_within, sha256_bytes, sha256_file, slug, utc_now

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
TEXT_EXTENSIONS = {".txt", ".md", ".json", ".csv", ".tsv"}
ANSWER_NAME = re.compile(r"(?:正确答案|标准答案|参考答案|答案|answer|key)", re.I)
QUESTION_NAME = re.compile(r"(?:选择题|题目|问题|question|choice|quiz)", re.I)
ZIWEI_NAME = re.compile(r"(?:紫微|斗数|ziwei|zwds|文字盘)", re.I)
BAZI_NAME = re.compile(r"(?:八字|四柱|bazi|命式)", re.I)
NOTE_NAME = re.compile(r"(?:备注|客观资料|note|remark|metadata)", re.I)
ANSWER_CONTENT = re.compile(r"(?:正确答案|标准答案|参考答案|答案)\s*[:：=]\s*(?:[A-H](?:\s*[,，、/|-]?\s*[A-H]){0,99})", re.I)
TYPE_MARKERS = [ANSWER_NAME, QUESTION_NAME, ZIWEI_NAME, BAZI_NAME, NOTE_NAME]


def _safe_member(info: zipfile.ZipInfo) -> PurePosixPath:
    name = info.filename.replace("\\", "/")
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or any("\x00" in part for part in path.parts):
        raise FortuneError(f"unsafe archive member: {name}", status="ARCHIVE_MEMBER_REJECTED")
    mode = info.external_attr >> 16
    if stat.S_ISLNK(mode):
        raise FortuneError(f"symlink rejected: {name}", status="ARCHIVE_MEMBER_REJECTED")
    return path


def _classify(name: str, data: bytes) -> str:
    suffix = Path(name).suffix.lower()
    hits = []
    if ANSWER_NAME.search(name): hits.append("ANSWER")
    if QUESTION_NAME.search(name): hits.append("QUESTIONS")
    if ZIWEI_NAME.search(name): hits.append("ZIWEI_TEXT")
    if BAZI_NAME.search(name) and suffix in IMAGE_EXTENSIONS: hits.append("BAZI_IMAGE")
    if NOTE_NAME.search(name): hits.append("NOTE")
    if suffix in TEXT_EXTENSIONS:
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text = ""
        if ANSWER_CONTENT.search(text):
            if "ANSWER" not in hits: hits.append("ANSWER")
    hits = list(dict.fromkeys(hits))
    if len(hits) != 1:
        return "AMBIGUOUS" if hits else "UNKNOWN"
    return hits[0]


def _case_key(path: PurePosixPath, package_stem: str) -> str:
    if len(path.parts) > 1:
        return slug(path.parts[0])
    stem = path.stem
    marker = re.search(r"(?:紫微|斗数|ziwei|八字|四柱|bazi|选择题|题目|问题|question|正确答案|标准答案|答案|answer|备注|note)", stem, re.I)
    prefix = stem[:marker.start()].strip(" _-.()（）[]【】") if marker else ""
    return slug(prefix or package_stem)


def ingest_zip(package_path: str | Path, runtime_root: str | Path, vault_root: str | Path,
               dataset_type: str, max_uncompressed_bytes: int = 512 * 1024 * 1024) -> dict[str, Any]:
    if dataset_type not in {"DEV", "REGRESSION", "FROZEN_EVAL"}:
        raise FortuneError("invalid dataset type", status="INVALID_DATASET_TYPE")
    package = Path(package_path)
    if not zipfile.is_zipfile(package):
        raise FortuneError("V1 deterministic importer accepts ZIP only", status="UNSUPPORTED_ARCHIVE_FORMAT")
    package_hash = sha256_file(package)
    runtime_root, vault_root = Path(runtime_root), Path(vault_root)
    raw_package_target = vault_root / "packages" / f"{package_hash}.zip"
    if raw_package_target.exists():
        if sha256_file(raw_package_target) != package_hash:
            raise FortuneError("raw package path collision", status="VAULT_COLLISION")
    else:
        raw_package_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(package, raw_package_target)
        raw_package_target.chmod(0o400)

    staged: dict[str, list[dict[str, Any]]] = defaultdict(list)
    names: set[str] = set()
    total = 0
    with zipfile.ZipFile(package, "r") as archive:
        for info in sorted(archive.infolist(), key=lambda i: i.filename):
            if info.is_dir(): continue
            member = _safe_member(info)
            member_key = member.as_posix().casefold()
            if member_key in names:
                raise FortuneError(f"duplicate member: {member}", status="ARCHIVE_DUPLICATE_MEMBER")
            names.add(member_key)
            if info.flag_bits & 0x1:
                raise FortuneError(f"encrypted member: {member}", status="ARCHIVE_ENCRYPTED_MEMBER")
            total += info.file_size
            if total > max_uncompressed_bytes:
                raise FortuneError("uncompressed size limit exceeded", status="ARCHIVE_SIZE_LIMIT")
            if info.compress_size and info.file_size / info.compress_size > 200:
                raise FortuneError(f"suspicious compression ratio: {member}", status="ARCHIVE_BOMB_REJECTED")
            data = archive.read(info)
            if len(data) != info.file_size:
                raise FortuneError(f"member size mismatch: {member}", status="ARCHIVE_SIZE_MISMATCH")
            case_id = _case_key(member, package.stem)
            logical_type = _classify(member.name, data)
            staged[case_id].append({"member": member, "data": data, "logical_type": logical_type})

    case_receipts = []
    for case_id, items in sorted(staged.items()):
        counts = defaultdict(int)
        conflicts = []
        for item in items: counts[item["logical_type"]] += 1
        if counts["ZIWEI_TEXT"] != 1: conflicts.append(f"ZIWEI_TEXT_COUNT={counts['ZIWEI_TEXT']}")
        if counts["BAZI_IMAGE"] < 1: conflicts.append("BAZI_IMAGE_COUNT=0")
        if counts["QUESTIONS"] != 1: conflicts.append(f"QUESTIONS_COUNT={counts['QUESTIONS']}")
        if counts["ANSWER"] != 1: conflicts.append(f"ANSWER_COUNT={counts['ANSWER']}")
        if counts["AMBIGUOUS"] or counts["UNKNOWN"]:
            conflicts.append(f"UNCLASSIFIED_COUNT={counts['AMBIGUOUS'] + counts['UNKNOWN']}")
        status = "INPUT_QUARANTINE" if conflicts else "NORMALIZED"
        vault_raw_root = vault_root / "raw" / package_hash / case_id
        runtime_case_root = runtime_root / "cases" / dataset_type / case_id
        safe_rows, private_rows = [], []
        for item in items:
            member: PurePosixPath = item["member"]
            data: bytes = item["data"]
            digest = sha256_bytes(data)
            raw_target = ensure_within(vault_raw_root, vault_raw_root.joinpath(*member.parts))
            raw_target.parent.mkdir(parents=True, exist_ok=True)
            raw_target.write_bytes(data); raw_target.chmod(0o400)
            private_rows.append({"logical_type": item["logical_type"], "original_name": member.as_posix(), "sha256": digest, "bytes": len(data), "raw_path": str(raw_target)})
            if item["logical_type"] == "ANSWER":
                answer_target = vault_root / "answers" / case_id / f"answer{Path(member.name).suffix.lower()}"
                answer_target.parent.mkdir(parents=True, exist_ok=True)
                answer_target.write_bytes(data); answer_target.chmod(0o400)
            elif item["logical_type"] in {"ZIWEI_TEXT", "BAZI_IMAGE", "QUESTIONS", "NOTE"}:
                safe_target = runtime_case_root / "input" / item["logical_type"].lower() / member.name
                safe_target.parent.mkdir(parents=True, exist_ok=True)
                safe_target.write_bytes(data); safe_target.chmod(0o444)
                safe_rows.append({"logical_type": item["logical_type"], "original_name": member.as_posix(), "sha256": digest, "bytes": len(data), "storage_domain": "RUNTIME", "path": str(safe_target)})
        private_manifest = {
            "schema": "RAW-PACKAGE-PRIVATE-MANIFEST-V1", "case_id": case_id, "package_sha256": package_hash,
            "dataset_type": dataset_type, "files": private_rows, "status": status, "conflicts": conflicts, "ingested_at": utc_now(),
        }
        private_path = vault_root / "manifests" / f"{case_id}.json"
        atomic_write_json(private_path, private_manifest)
        private_path.chmod(0o400)
        public_manifest = {
            "schema": "NORMALIZED-CASE-V1", "case_id": case_id, "dataset_type": dataset_type,
            "package_sha256": package_hash, "files": safe_rows, "answer_isolation": {
                "answer_file_count": counts["ANSWER"], "answer_content_disclosed": False,
                "answer_filename_disclosed": False, "vault_reference_disclosed": False,
                "status": "PROGRAMMATICALLY_ISOLATED" if counts["ANSWER"] == 1 else "FAIL"
            }, "status": status, "conflicts": conflicts,
        }
        public_path = runtime_case_root / "normalized-case.json"
        atomic_write_json(public_path, public_manifest)
        public_path.chmod(0o444)
        case_receipts.append({"case_id": case_id, "status": status, "runtime_manifest": str(public_path), "safe_file_count": len(safe_rows), "answer_file_count": counts["ANSWER"]})
    receipt = {
        "schema": "INGEST-RECEIPT-V1", "package_sha256": package_hash, "package_bytes": package.stat().st_size,
        "raw_package_read_only": not bool(raw_package_target.stat().st_mode & stat.S_IWUSR),
        "dataset_type": dataset_type, "cases": case_receipts, "status": "PASS" if all(c["status"] == "NORMALIZED" for c in case_receipts) else "INPUT_QUARANTINE",
        "created_at": utc_now(),
    }
    receipt_path = runtime_root / "receipts" / f"ingest-{package_hash[:16]}.json"
    atomic_write_json(receipt_path, receipt)
    return receipt

