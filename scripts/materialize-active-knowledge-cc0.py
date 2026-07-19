#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

LIBRARIES = [f"S{i:02d}" for i in range(20)]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def object_hash(value: dict[str, Any]) -> str:
    body = dict(value)
    body.pop("object_hash", None)
    return hashlib.sha256(canonical_bytes(body)).hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def repo_path(root: Path, raw: str) -> Path:
    path = (root / raw).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise SystemExit(f"path escapes repository: {raw}") from exc
    return path


def write_immutable_json(path: Path, value: dict[str, Any]) -> None:
    require(not path.exists(), f"immutable output exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def execute(
    root: Path,
    declaration_raw: str,
    notice_raw: str,
    output_raw: str,
    receipt_raw: str,
    generated_at: str,
    code_commit: str,
) -> dict[str, Any]:
    root = root.resolve()
    pointer_raw = "knowledge/active-release.json"
    pointer_path = repo_path(root, pointer_raw)
    declaration_path = repo_path(root, declaration_raw)
    notice_path = repo_path(root, notice_raw)
    output_path = repo_path(root, output_raw)
    receipt_path = repo_path(root, receipt_raw)

    require(pointer_path.is_file(), "active release pointer missing")
    require(declaration_path.is_file(), "rights declaration missing")
    require(notice_path.is_file(), "CC0 notice missing")

    pointer = read_json(pointer_path)
    require(pointer.get("schema") == "FORTUNE-ACTIVE-KNOWLEDGE-RELEASE-POINTER-V1", "active pointer schema invalid")
    require(pointer.get("formal_release") == "YES", "active pointer is not formal")
    release_id = str(pointer.get("knowledge_release_id") or "")
    require(release_id == "KNOWLEDGE-R17", f"unexpected active release: {release_id}")

    release_manifest_raw = str(pointer.get("manifest_path") or "")
    release_manifest_path = repo_path(root, release_manifest_raw)
    require(release_manifest_path.is_file(), "active source release manifest missing")
    release_manifest = read_json(release_manifest_path)
    require(release_manifest.get("schema") == "FORTUNE-KNOWLEDGE-RELEASE-MANIFEST-V1", "release manifest schema invalid")
    require(release_manifest.get("knowledge_release_id") == release_id, "release ID mismatch")
    require(release_manifest.get("formal_release") == "YES", "source release is not formal")
    require(release_manifest.get("object_hash") == object_hash(release_manifest), "release manifest object hash invalid")
    require(pointer.get("manifest_object_hash") == release_manifest.get("object_hash"), "pointer manifest object hash mismatch")

    declaration = read_json(declaration_path)
    require(declaration.get("schema") == "KNOWLEDGE-RIGHTS-DECLARATION-V1", "rights declaration schema invalid")
    require(declaration.get("status") == "ACCEPTED_USER_A2_DECLARATION", "rights declaration status invalid")
    require(declaration.get("selection") == "A2", "rights declaration selection invalid")
    require(declaration.get("license_expression") == "CC0-1.0", "rights license expression invalid")
    require(declaration.get("public_distribution_allowed") is True, "public distribution not authorized")
    require(declaration.get("commercial_use_allowed") is True, "commercial use not authorized")
    require(declaration.get("modification_allowed") is True, "modification not authorized")
    require(declaration.get("object_hash") == object_hash(declaration), "rights declaration object hash invalid")
    scope = declaration.get("scope") if isinstance(declaration.get("scope"), dict) else {}
    require(scope.get("knowledge_release_id") == release_id, "rights declaration release scope mismatch")
    require(scope.get("active_release_pointer_path") == pointer_raw, "rights declaration pointer scope mismatch")
    require(scope.get("source_release_manifest_path") == release_manifest_raw, "rights declaration source scope mismatch")
    require(scope.get("library_ids") == LIBRARIES, "rights declaration library scope mismatch")

    source_rows = release_manifest.get("source_files")
    require(isinstance(source_rows, list), "source file rows missing")
    require(release_manifest.get("source_file_count") == 20, "source file count invalid")
    require([str(row.get("library_id")) for row in source_rows] == LIBRARIES, "active source set is not exact S00-S19")

    files: list[dict[str, Any]] = []
    for row in source_rows:
        library_id = str(row.get("library_id"))
        rel = str(row.get("repository_relative_path") or "")
        path = repo_path(root, rel)
        require(path.is_file(), f"knowledge file missing: {rel}")
        actual_sha = sha256(path)
        actual_size = path.stat().st_size
        require(actual_sha == row.get("sha256_raw_file_bytes"), f"knowledge hash mismatch: {rel}")
        require(actual_size == row.get("file_size_bytes"), f"knowledge size mismatch: {rel}")
        files.append({
            "library_id": library_id,
            "path": rel,
            "sha256": actual_sha,
            "byte_length": actual_size,
            "source_identity": f"Ziwei-Bazi Model active knowledge library {library_id} bound by {release_id}",
            "source_locator": f"{release_manifest_raw}#{library_id}",
            "author_or_rights_holder": "chinaneedM and project contributors as represented in the A2 declaration",
            "rights_basis": "SPDX_LICENSE",
            "spdx_license_expression": "CC0-1.0",
            "permission_record_path": declaration_raw,
            "attribution_text": None,
            "redistribution_allowed": True,
            "modification_allowed": True,
            "public_display_allowed": True,
            "personal_data_status": "NONE",
            "required_notices": [
                "SPDX-License-Identifier: CC0-1.0",
                notice_raw,
            ],
        })

    manifest = {
        "schema": "OPEN-KNOWLEDGE-PACK-LICENSE-MANIFEST-V1",
        "status": "PASS_PUBLIC_DISTRIBUTION",
        "pack_id": "FORTUNE-S00-S19",
        "release_id": release_id,
        "public_distribution_allowed": True,
        "license_expression": "CC0-1.0",
        "active_release_pointer_path": pointer_raw,
        "active_release_pointer_sha256": sha256(pointer_path),
        "source_release_manifest_path": release_manifest_raw,
        "source_release_manifest_sha256": sha256(release_manifest_path),
        "source_release_manifest_object_hash": release_manifest["object_hash"],
        "rights_declaration_path": declaration_raw,
        "rights_declaration_sha256": sha256(declaration_path),
        "notice_path": notice_raw,
        "manifest_generated_at": generated_at,
        "files": files,
    }
    manifest["object_hash"] = object_hash(manifest)
    write_immutable_json(output_path, manifest)

    receipt = {
        "schema": "ACTIVE-KNOWLEDGE-CC0-MATERIALIZATION-RECEIPT-V1",
        "status": "PASS",
        "generated_at": generated_at,
        "code_commit": code_commit,
        "repository": "chinaneedM/ziwei-bazi-model",
        "active_knowledge_release_id": release_id,
        "active_release_pointer_path": pointer_raw,
        "active_release_pointer_sha256": sha256(pointer_path),
        "source_release_manifest_path": release_manifest_raw,
        "source_release_manifest_sha256": sha256(release_manifest_path),
        "source_release_manifest_object_hash": release_manifest["object_hash"],
        "rights_declaration_path": declaration_raw,
        "rights_declaration_sha256": sha256(declaration_path),
        "license_manifest_path": output_raw,
        "license_manifest_sha256": sha256(output_path),
        "license_manifest_object_hash": manifest["object_hash"],
        "license_expression": "CC0-1.0",
        "checked_library_ids": LIBRARIES,
        "checked_file_count": len(files),
        "public_distribution_allowed": True,
        "independent_legal_verification": False,
        "formal_release_scope": "RIGHTS_AND_HASH_BINDING_ONLY",
    }
    receipt["object_hash"] = object_hash(receipt)
    write_immutable_json(receipt_path, receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--declaration", required=True)
    parser.add_argument("--notice", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--generated-at", required=True)
    parser.add_argument("--code-commit", required=True)
    args = parser.parse_args()
    result = execute(
        Path(args.root),
        args.declaration,
        args.notice,
        args.output,
        args.receipt,
        args.generated_at,
        args.code_commit,
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
