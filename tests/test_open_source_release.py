from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "verify-open-source-release.py"
SPEC = importlib.util.spec_from_file_location("verify_open_source_release", SCRIPT_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class OpenSourceReleaseTests(unittest.TestCase):
    def write(self, path: Path, body: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")

    @staticmethod
    def digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    @staticmethod
    def object_hash(value: dict) -> str:
        body = dict(value)
        body.pop("object_hash", None)
        encoded = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def write_object(self, path: Path, value: dict) -> dict:
        body = dict(value)
        body["object_hash"] = self.object_hash(body)
        self.write(path, json.dumps(body, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
        return body

    def fixture(self, root: Path, *, include_manifest: bool = True) -> None:
        required = [
            "LICENSE",
            "NOTICE",
            "README.md",
            "CONTRIBUTING.md",
            "GOVERNANCE.md",
            "SECURITY.md",
            "docs/open-source-architecture.md",
            "licenses/README.md",
            "licenses/knowledge-pack-manifest.schema.json",
        ]
        for path in required:
            self.write(root / path, f"fixture {path}\n")
        self.write(
            root / "pyproject.toml",
            "[project]\nname='fixture'\nversion='1.0.0'\nlicense='Apache-2.0'\n",
        )

        release_rows = []
        license_rows = []
        for index in range(20):
            library_id = f"S{index:02d}"
            rel = f"knowledge/releases/FIXTURE/files/{library_id}_fixture.txt"
            source = root / rel
            self.write(source, f"open fixture {library_id}\n")
            digest = self.digest(source)
            release_rows.append({
                "library_id": library_id,
                "canonical_filename": source.name,
                "repository_relative_path": rel,
                "sha256_raw_file_bytes": digest,
                "file_size_bytes": source.stat().st_size,
            })
            license_rows.append({
                "library_id": library_id,
                "path": rel,
                "sha256": digest,
                "byte_length": source.stat().st_size,
                "source_identity": f"project fixture {library_id}",
                "source_locator": f"release row {library_id}",
                "author_or_rights_holder": "fixture owner",
                "rights_basis": "SPDX_LICENSE",
                "spdx_license_expression": "CC0-1.0",
                "permission_record_path": "licenses/knowledge-packs/FIXTURE/rights-declaration.json",
                "attribution_text": None,
                "redistribution_allowed": True,
                "modification_allowed": True,
                "public_display_allowed": True,
                "personal_data_status": "NONE",
                "required_notices": ["SPDX-License-Identifier: CC0-1.0"],
            })

        release_manifest_path = root / "knowledge/releases/FIXTURE/release-manifest.json"
        release_manifest = self.write_object(release_manifest_path, {
            "schema": "FORTUNE-KNOWLEDGE-RELEASE-MANIFEST-V1",
            "knowledge_release_id": "FIXTURE-1",
            "formal_release": "YES",
            "source_file_count": 20,
            "source_files": release_rows,
        })
        pointer_path = root / "knowledge/active-release.json"
        pointer = self.write_object(pointer_path, {
            "schema": "FORTUNE-ACTIVE-KNOWLEDGE-RELEASE-POINTER-V1",
            "formal_release": "YES",
            "knowledge_release_id": "FIXTURE-1",
            "manifest_path": "knowledge/releases/FIXTURE/release-manifest.json",
            "manifest_object_hash": release_manifest["object_hash"],
        })

        declaration_path = root / "licenses/knowledge-packs/FIXTURE/rights-declaration.json"
        declaration = self.write_object(declaration_path, {
            "schema": "KNOWLEDGE-RIGHTS-DECLARATION-V1",
            "status": "ACCEPTED",
            "selection": "A2",
            "license_expression": "CC0-1.0",
        })
        notice_path = root / "licenses/knowledge-packs/FIXTURE/CC0-NOTICE.md"
        self.write(notice_path, "SPDX-License-Identifier: CC0-1.0\n")

        manifest_path = "licenses/knowledge-packs/FIXTURE/manifest.json"
        if include_manifest:
            self.write_object(root / manifest_path, {
                "schema": "OPEN-KNOWLEDGE-PACK-LICENSE-MANIFEST-V1",
                "status": "PASS_PUBLIC_DISTRIBUTION",
                "pack_id": "FORTUNE-S00-S19",
                "release_id": "FIXTURE-1",
                "public_distribution_allowed": True,
                "license_expression": "CC0-1.0",
                "active_release_pointer_path": "knowledge/active-release.json",
                "active_release_pointer_sha256": self.digest(pointer_path),
                "source_release_manifest_path": "knowledge/releases/FIXTURE/release-manifest.json",
                "source_release_manifest_sha256": self.digest(release_manifest_path),
                "source_release_manifest_object_hash": release_manifest["object_hash"],
                "rights_declaration_path": "licenses/knowledge-packs/FIXTURE/rights-declaration.json",
                "rights_declaration_sha256": self.digest(declaration_path),
                "notice_path": "licenses/knowledge-packs/FIXTURE/CC0-NOTICE.md",
                "files": license_rows,
            })

        self.write(root / "config/open-source-release.json", json.dumps({
            "schema": "OPEN-SOURCE-RELEASE-CONTRACT-V1",
            "software_license": "Apache-2.0",
            "repository_visibility_required": "public",
            "required_project_files": required,
            "active_knowledge_release_pointer_path": "knowledge/active-release.json",
            "allowed_knowledge_license_expressions": ["CC0-1.0"],
            "active_knowledge_pack_manifests": [manifest_path] if include_manifest else [],
        }, indent=2))

    def test_complete_open_source_release_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            result = MODULE.verify(root, "public")
            self.assertEqual(result["status"], "PASS", result)
            self.assertEqual(result["active_knowledge_release_id"], "FIXTURE-1")
            self.assertEqual(result["checked_manifest_count"], 1)
            self.assertEqual(result["checked_knowledge_file_count"], 20)

    def test_missing_manifests_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root, include_manifest=False)
            result = MODULE.verify(root, "public")
            self.assertEqual(result["status"], "FAIL")
            self.assertIn("ACTIVE_KNOWLEDGE_LICENSE_MANIFESTS_MISSING", {row["code"] for row in result["failures"]})

    def test_hash_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            manifest_path = root / "licenses/knowledge-packs/FIXTURE/manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["files"][0]["sha256"] = "0" * 64
            manifest["object_hash"] = self.object_hash(manifest)
            self.write(manifest_path, json.dumps(manifest, indent=2))
            result = MODULE.verify(root, "public")
            self.assertIn("KNOWLEDGE_FILE_HASH_MISMATCH", {row["code"] for row in result["failures"]})

    def test_non_open_rights_basis_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            manifest_path = root / "licenses/knowledge-packs/FIXTURE/manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["files"][0]["rights_basis"] = "UNKNOWN"
            manifest["object_hash"] = self.object_hash(manifest)
            self.write(manifest_path, json.dumps(manifest, indent=2))
            result = MODULE.verify(root, "public")
            self.assertIn("KNOWLEDGE_RIGHTS_BASIS_NOT_OPEN", {row["code"] for row in result["failures"]})

    def test_license_manifest_cannot_bind_wrong_release_file_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            manifest_path = root / "licenses/knowledge-packs/FIXTURE/manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["files"] = manifest["files"][:-1]
            manifest["object_hash"] = self.object_hash(manifest)
            self.write(manifest_path, json.dumps(manifest, indent=2))
            result = MODULE.verify(root, "public")
            self.assertIn("KNOWLEDGE_LICENSE_FILE_SET_NOT_ACTIVE_RELEASE", {row["code"] for row in result["failures"]})

    def test_pointer_hash_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            manifest_path = root / "licenses/knowledge-packs/FIXTURE/manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["active_release_pointer_sha256"] = "0" * 64
            manifest["object_hash"] = self.object_hash(manifest)
            self.write(manifest_path, json.dumps(manifest, indent=2))
            result = MODULE.verify(root, "public")
            self.assertIn("KNOWLEDGE_LICENSE_POINTER_HASH_MISMATCH", {row["code"] for row in result["failures"]})


if __name__ == "__main__":
    unittest.main()
