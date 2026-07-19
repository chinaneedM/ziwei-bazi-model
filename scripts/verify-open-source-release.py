#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import tomllib
from pathlib import Path
from typing import Any

CONTRACT_PATH = Path("config/open-source-release.json")
PASS_STATUS = "PASS_PUBLIC_DISTRIBUTION"
ALLOWED_RIGHTS = {"SPDX_LICENSE", "PUBLIC_DOMAIN", "DOCUMENTED_PERMISSION", "PROJECT_ORIGINAL"}
ALLOWED_PERSONAL_DATA = {"NONE", "ANONYMIZED_WITH_PUBLICATION_CONSENT", "PUBLIC_RECORD_WITH_REUSE_ALLOWED"}
LIBRARIES = [f"S{i:02d}" for i in range(20)]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def object_hash(value: dict[str, Any]) -> str:
    body = dict(value)
    body.pop("object_hash", None)
    encoded = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def fail(failures: list[dict[str, str]], code: str, path: str, detail: str) -> None:
    failures.append({"code": code, "path": path, "detail": detail})


def safe_repo_path(root: Path, raw: str, failures: list[dict[str, str]], code: str) -> Path | None:
    path = (root / raw).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        fail(failures, code, raw, "outside repository")
        return None
    return path


def verify(root: Path, visibility: str) -> dict[str, Any]:
    root = root.resolve()
    failures: list[dict[str, str]] = []
    contract_path = root / CONTRACT_PATH
    if not contract_path.is_file():
        fail(failures, "OPEN_SOURCE_RELEASE_CONTRACT_MISSING", str(CONTRACT_PATH), "missing")
        contract: dict[str, Any] = {}
    else:
        contract = read_json(contract_path)
        if contract.get("schema") != "OPEN-SOURCE-RELEASE-CONTRACT-V1":
            fail(failures, "OPEN_SOURCE_RELEASE_CONTRACT_INVALID", str(CONTRACT_PATH), "schema")

    required_visibility = str(contract.get("repository_visibility_required", "public"))
    if visibility != required_visibility:
        fail(failures, "REPOSITORY_VISIBILITY_NOT_PUBLIC", ".", f"actual={visibility} required={required_visibility}")

    for raw in contract.get("required_project_files", []):
        path = root / str(raw)
        if not path.is_file():
            fail(failures, "REQUIRED_OPEN_SOURCE_FILE_MISSING", str(raw), "missing")

    pyproject_path = root / "pyproject.toml"
    if pyproject_path.is_file():
        pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
        project = pyproject.get("project", {})
        if project.get("license") != contract.get("software_license"):
            fail(
                failures,
                "PACKAGE_LICENSE_METADATA_MISMATCH",
                "pyproject.toml",
                f"actual={project.get('license')} required={contract.get('software_license')}",
            )
    else:
        fail(failures, "PYPROJECT_MISSING", "pyproject.toml", "missing")

    pointer_raw = str(contract.get("active_knowledge_release_pointer_path", ""))
    pointer_path = safe_repo_path(root, pointer_raw, failures, "ACTIVE_RELEASE_POINTER_PATH_ESCAPE") if pointer_raw else None
    pointer: dict[str, Any] = {}
    source_manifest: dict[str, Any] = {}
    source_manifest_path: Path | None = None
    active_release_id: str | None = None
    expected_source_rows: list[dict[str, Any]] = []

    if not pointer_raw:
        fail(failures, "ACTIVE_RELEASE_POINTER_NOT_CONFIGURED", str(CONTRACT_PATH), "missing")
    elif pointer_path is None or not pointer_path.is_file():
        fail(failures, "ACTIVE_RELEASE_POINTER_MISSING", pointer_raw, "missing")
    else:
        pointer = read_json(pointer_path)
        if pointer.get("schema") != "FORTUNE-ACTIVE-KNOWLEDGE-RELEASE-POINTER-V1":
            fail(failures, "ACTIVE_RELEASE_POINTER_SCHEMA_INVALID", pointer_raw, str(pointer.get("schema")))
        if pointer.get("formal_release") != "YES":
            fail(failures, "ACTIVE_RELEASE_POINTER_NOT_FORMAL", pointer_raw, str(pointer.get("formal_release")))
        active_release_id = str(pointer.get("knowledge_release_id") or "")
        if not active_release_id:
            fail(failures, "ACTIVE_RELEASE_ID_MISSING", pointer_raw, "missing")
        source_manifest_raw = str(pointer.get("manifest_path") or "")
        source_manifest_path = safe_repo_path(root, source_manifest_raw, failures, "SOURCE_RELEASE_MANIFEST_PATH_ESCAPE") if source_manifest_raw else None
        if not source_manifest_raw:
            fail(failures, "SOURCE_RELEASE_MANIFEST_NOT_BOUND", pointer_raw, "manifest_path missing")
        elif source_manifest_path is None or not source_manifest_path.is_file():
            fail(failures, "SOURCE_RELEASE_MANIFEST_MISSING", source_manifest_raw, "missing")
        else:
            source_manifest = read_json(source_manifest_path)
            if source_manifest.get("schema") != "FORTUNE-KNOWLEDGE-RELEASE-MANIFEST-V1":
                fail(failures, "SOURCE_RELEASE_MANIFEST_SCHEMA_INVALID", source_manifest_raw, str(source_manifest.get("schema")))
            if source_manifest.get("knowledge_release_id") != active_release_id:
                fail(failures, "SOURCE_RELEASE_ID_MISMATCH", source_manifest_raw, f"actual={source_manifest.get('knowledge_release_id')} expected={active_release_id}")
            if source_manifest.get("object_hash") != object_hash(source_manifest):
                fail(failures, "SOURCE_RELEASE_MANIFEST_OBJECT_HASH_MISMATCH", source_manifest_raw, "invalid")
            if pointer.get("manifest_object_hash") != source_manifest.get("object_hash"):
                fail(failures, "ACTIVE_POINTER_MANIFEST_OBJECT_HASH_MISMATCH", pointer_raw, "invalid")
            expected_source_rows = source_manifest.get("source_files", [])
            if not isinstance(expected_source_rows, list):
                expected_source_rows = []
            expected_libraries = [str(row.get("library_id")) for row in expected_source_rows]
            if expected_libraries != LIBRARIES or source_manifest.get("source_file_count") != 20:
                fail(failures, "ACTIVE_SOURCE_SET_NOT_EXACT_S00_S19", source_manifest_raw, str(expected_libraries))

    manifest_rows = contract.get("active_knowledge_pack_manifests", [])
    if not isinstance(manifest_rows, list) or not manifest_rows:
        fail(failures, "ACTIVE_KNOWLEDGE_LICENSE_MANIFESTS_MISSING", str(CONTRACT_PATH), "empty")
        manifest_rows = []

    allowed_expressions = set(str(v) for v in contract.get("allowed_knowledge_license_expressions", []))
    checked_files = 0
    checked_manifests = 0
    active_pointer_sha = sha256(pointer_path) if pointer_path and pointer_path.is_file() else None
    source_manifest_sha = sha256(source_manifest_path) if source_manifest_path and source_manifest_path.is_file() else None
    expected_by_path = {str(row.get("repository_relative_path")): row for row in expected_source_rows}
    expected_paths = [str(row.get("repository_relative_path")) for row in expected_source_rows]

    for raw in manifest_rows:
        manifest_path = safe_repo_path(root, str(raw), failures, "KNOWLEDGE_MANIFEST_PATH_ESCAPE")
        if manifest_path is None:
            continue
        if not manifest_path.is_file():
            fail(failures, "KNOWLEDGE_MANIFEST_MISSING", str(raw), "missing")
            continue
        manifest = read_json(manifest_path)
        checked_manifests += 1
        if manifest.get("schema") != "OPEN-KNOWLEDGE-PACK-LICENSE-MANIFEST-V1":
            fail(failures, "KNOWLEDGE_MANIFEST_SCHEMA_INVALID", str(raw), "schema")
            continue
        if manifest.get("object_hash") != object_hash(manifest):
            fail(failures, "KNOWLEDGE_MANIFEST_OBJECT_HASH_MISMATCH", str(raw), "invalid")
        if manifest.get("status") != PASS_STATUS or manifest.get("public_distribution_allowed") is not True:
            fail(failures, "KNOWLEDGE_PACK_NOT_PUBLICLY_DISTRIBUTABLE", str(raw), str(manifest.get("status")))
        if manifest.get("release_id") != active_release_id:
            fail(failures, "KNOWLEDGE_LICENSE_RELEASE_ID_MISMATCH", str(raw), f"actual={manifest.get('release_id')} expected={active_release_id}")
        expression = str(manifest.get("license_expression") or "")
        if not expression or (allowed_expressions and expression not in allowed_expressions):
            fail(failures, "KNOWLEDGE_LICENSE_EXPRESSION_NOT_ALLOWED", str(raw), expression or "missing")
        if manifest.get("active_release_pointer_path") != pointer_raw:
            fail(failures, "KNOWLEDGE_LICENSE_POINTER_PATH_MISMATCH", str(raw), str(manifest.get("active_release_pointer_path")))
        if manifest.get("active_release_pointer_sha256") != active_pointer_sha:
            fail(failures, "KNOWLEDGE_LICENSE_POINTER_HASH_MISMATCH", str(raw), "invalid")
        expected_source_manifest_raw = str(pointer.get("manifest_path") or "")
        if manifest.get("source_release_manifest_path") != expected_source_manifest_raw:
            fail(failures, "KNOWLEDGE_LICENSE_SOURCE_MANIFEST_PATH_MISMATCH", str(raw), str(manifest.get("source_release_manifest_path")))
        if manifest.get("source_release_manifest_sha256") != source_manifest_sha:
            fail(failures, "KNOWLEDGE_LICENSE_SOURCE_MANIFEST_HASH_MISMATCH", str(raw), "invalid")
        if manifest.get("source_release_manifest_object_hash") != source_manifest.get("object_hash"):
            fail(failures, "KNOWLEDGE_LICENSE_SOURCE_OBJECT_HASH_MISMATCH", str(raw), "invalid")

        declaration_raw = str(manifest.get("rights_declaration_path") or "")
        declaration_path = safe_repo_path(root, declaration_raw, failures, "RIGHTS_DECLARATION_PATH_ESCAPE") if declaration_raw else None
        if not declaration_raw or declaration_path is None or not declaration_path.is_file():
            fail(failures, "RIGHTS_DECLARATION_MISSING", declaration_raw or str(raw), "missing")
        elif manifest.get("rights_declaration_sha256") != sha256(declaration_path):
            fail(failures, "RIGHTS_DECLARATION_HASH_MISMATCH", declaration_raw, "invalid")

        notice_raw = str(manifest.get("notice_path") or "")
        notice_path = safe_repo_path(root, notice_raw, failures, "KNOWLEDGE_NOTICE_PATH_ESCAPE") if notice_raw else None
        if not notice_raw or notice_path is None or not notice_path.is_file():
            fail(failures, "KNOWLEDGE_NOTICE_MISSING", notice_raw or str(raw), "missing")

        files = manifest.get("files", [])
        if not isinstance(files, list) or not files:
            fail(failures, "KNOWLEDGE_MANIFEST_FILES_MISSING", str(raw), "empty")
            continue
        actual_paths = [str(row.get("path", "")) for row in files]
        if actual_paths != expected_paths:
            fail(failures, "KNOWLEDGE_LICENSE_FILE_SET_NOT_ACTIVE_RELEASE", str(raw), f"actual={actual_paths} expected={expected_paths}")

        for row in files:
            rel = str(row.get("path", ""))
            target = safe_repo_path(root, rel, failures, "KNOWLEDGE_FILE_PATH_ESCAPE")
            if target is None:
                continue
            if not target.is_file():
                fail(failures, "KNOWLEDGE_FILE_MISSING", rel, "missing")
                continue
            checked_files += 1
            expected = expected_by_path.get(rel)
            if expected is None:
                fail(failures, "KNOWLEDGE_FILE_NOT_IN_ACTIVE_RELEASE", rel, "unexpected")
                continue
            if row.get("library_id") != expected.get("library_id"):
                fail(failures, "KNOWLEDGE_LIBRARY_ID_MISMATCH", rel, f"actual={row.get('library_id')} expected={expected.get('library_id')}")
            actual_size = target.stat().st_size
            actual_sha = sha256(target)
            expected_size = expected.get("file_size_bytes")
            expected_sha = expected.get("sha256_raw_file_bytes")
            if row.get("byte_length") != actual_size or actual_size != expected_size:
                fail(failures, "KNOWLEDGE_FILE_SIZE_MISMATCH", rel, f"actual={actual_size} license={row.get('byte_length')} release={expected_size}")
            if row.get("sha256") != actual_sha or actual_sha != expected_sha:
                fail(failures, "KNOWLEDGE_FILE_HASH_MISMATCH", rel, f"actual={actual_sha} license={row.get('sha256')} release={expected_sha}")
            if row.get("rights_basis") not in ALLOWED_RIGHTS:
                fail(failures, "KNOWLEDGE_RIGHTS_BASIS_NOT_OPEN", rel, str(row.get("rights_basis")))
            if row.get("redistribution_allowed") is not True:
                fail(failures, "KNOWLEDGE_REDISTRIBUTION_NOT_ALLOWED", rel, "false")
            if row.get("modification_allowed") is not True:
                fail(failures, "KNOWLEDGE_MODIFICATION_NOT_ALLOWED", rel, "false")
            if row.get("public_display_allowed") is not True:
                fail(failures, "KNOWLEDGE_PUBLIC_DISPLAY_NOT_ALLOWED", rel, "false")
            if row.get("personal_data_status") not in ALLOWED_PERSONAL_DATA:
                fail(failures, "KNOWLEDGE_PERSONAL_DATA_STATUS_INVALID", rel, str(row.get("personal_data_status")))
            if row.get("rights_basis") == "SPDX_LICENSE" and row.get("spdx_license_expression") != expression:
                fail(failures, "SPDX_LICENSE_EXPRESSION_MISMATCH", rel, f"actual={row.get('spdx_license_expression')} expected={expression}")
            if row.get("rights_basis") == "DOCUMENTED_PERMISSION" and not row.get("permission_record_path"):
                fail(failures, "PERMISSION_RECORD_MISSING", rel, "missing")

    result = {
        "schema": "OPEN-SOURCE-RELEASE-VERIFICATION-RECEIPT-V1",
        "status": "PASS" if not failures else "FAIL",
        "repository_visibility": visibility,
        "software_license": contract.get("software_license"),
        "active_knowledge_release_id": active_release_id,
        "active_release_pointer_path": pointer_raw or None,
        "active_release_pointer_sha256": active_pointer_sha,
        "source_release_manifest_path": str(pointer.get("manifest_path") or "") or None,
        "source_release_manifest_sha256": source_manifest_sha,
        "checked_manifest_count": checked_manifests,
        "checked_knowledge_file_count": checked_files,
        "failure_count": len(failures),
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--visibility", default=os.environ.get("GITHUB_REPOSITORY_VISIBILITY", "unknown"))
    args = parser.parse_args()
    result = verify(Path(args.root), str(args.visibility).lower())
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
