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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(failures: list[dict[str, str]], code: str, path: str, detail: str) -> None:
    failures.append({"code": code, "path": path, "detail": detail})


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

    manifest_rows = contract.get("active_knowledge_pack_manifests", [])
    if not isinstance(manifest_rows, list) or not manifest_rows:
        fail(failures, "ACTIVE_KNOWLEDGE_LICENSE_MANIFESTS_MISSING", str(CONTRACT_PATH), "empty")
        manifest_rows = []

    checked_files = 0
    checked_manifests = 0
    for raw in manifest_rows:
        manifest_path = (root / str(raw)).resolve()
        try:
            manifest_path.relative_to(root)
        except ValueError:
            fail(failures, "KNOWLEDGE_MANIFEST_PATH_ESCAPE", str(raw), "outside repository")
            continue
        if not manifest_path.is_file():
            fail(failures, "KNOWLEDGE_MANIFEST_MISSING", str(raw), "missing")
            continue
        manifest = read_json(manifest_path)
        checked_manifests += 1
        if manifest.get("schema") != "OPEN-KNOWLEDGE-PACK-LICENSE-MANIFEST-V1":
            fail(failures, "KNOWLEDGE_MANIFEST_SCHEMA_INVALID", str(raw), "schema")
            continue
        if manifest.get("status") != PASS_STATUS or manifest.get("public_distribution_allowed") is not True:
            fail(failures, "KNOWLEDGE_PACK_NOT_PUBLICLY_DISTRIBUTABLE", str(raw), str(manifest.get("status")))
        files = manifest.get("files", [])
        if not isinstance(files, list) or not files:
            fail(failures, "KNOWLEDGE_MANIFEST_FILES_MISSING", str(raw), "empty")
            continue
        for row in files:
            rel = str(row.get("path", ""))
            target = (root / rel).resolve()
            try:
                target.relative_to(root)
            except ValueError:
                fail(failures, "KNOWLEDGE_FILE_PATH_ESCAPE", rel, "outside repository")
                continue
            if not target.is_file():
                fail(failures, "KNOWLEDGE_FILE_MISSING", rel, "missing")
                continue
            checked_files += 1
            actual_size = target.stat().st_size
            actual_sha = sha256(target)
            if row.get("byte_length") != actual_size:
                fail(failures, "KNOWLEDGE_FILE_SIZE_MISMATCH", rel, f"actual={actual_size} expected={row.get('byte_length')}")
            if row.get("sha256") != actual_sha:
                fail(failures, "KNOWLEDGE_FILE_HASH_MISMATCH", rel, f"actual={actual_sha} expected={row.get('sha256')}")
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
            if row.get("rights_basis") == "SPDX_LICENSE" and not row.get("spdx_license_expression"):
                fail(failures, "SPDX_LICENSE_EXPRESSION_MISSING", rel, "missing")
            if row.get("rights_basis") == "DOCUMENTED_PERMISSION" and not row.get("permission_record_path"):
                fail(failures, "PERMISSION_RECORD_MISSING", rel, "missing")

    result = {
        "schema": "OPEN-SOURCE-RELEASE-VERIFICATION-RECEIPT-V1",
        "status": "PASS" if not failures else "FAIL",
        "repository_visibility": visibility,
        "software_license": contract.get("software_license"),
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
