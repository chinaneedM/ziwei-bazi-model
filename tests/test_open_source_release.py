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
        data = root / "knowledge/open-packs/FIXTURE/source.txt"
        self.write(data, "open fixture\n")
        digest = hashlib.sha256(data.read_bytes()).hexdigest()
        manifest_path = "licenses/manifests/FIXTURE.json"
        if include_manifest:
            self.write(root / manifest_path, json.dumps({
                "schema": "OPEN-KNOWLEDGE-PACK-LICENSE-MANIFEST-V1",
                "status": "PASS_PUBLIC_DISTRIBUTION",
                "pack_id": "FIXTURE",
                "release_id": "FIXTURE-1",
                "public_distribution_allowed": True,
                "files": [{
                    "path": "knowledge/open-packs/FIXTURE/source.txt",
                    "sha256": digest,
                    "byte_length": data.stat().st_size,
                    "source_identity": "project test fixture",
                    "rights_basis": "PROJECT_ORIGINAL",
                    "redistribution_allowed": True,
                    "modification_allowed": True,
                    "public_display_allowed": True,
                    "personal_data_status": "NONE",
                }],
            }, indent=2))
        self.write(root / "config/open-source-release.json", json.dumps({
            "schema": "OPEN-SOURCE-RELEASE-CONTRACT-V1",
            "software_license": "Apache-2.0",
            "repository_visibility_required": "public",
            "required_project_files": required,
            "active_knowledge_pack_manifests": [manifest_path] if include_manifest else [],
        }, indent=2))

    def test_complete_open_source_release_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            result = MODULE.verify(root, "public")
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["checked_manifest_count"], 1)
            self.assertEqual(result["checked_knowledge_file_count"], 1)

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
            manifest_path = root / "licenses/manifests/FIXTURE.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["files"][0]["sha256"] = "0" * 64
            self.write(manifest_path, json.dumps(manifest, indent=2))
            result = MODULE.verify(root, "public")
            self.assertIn("KNOWLEDGE_FILE_HASH_MISMATCH", {row["code"] for row in result["failures"]})

    def test_non_open_rights_basis_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            manifest_path = root / "licenses/manifests/FIXTURE.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["files"][0]["rights_basis"] = "UNKNOWN"
            self.write(manifest_path, json.dumps(manifest, indent=2))
            result = MODULE.verify(root, "public")
            self.assertIn("KNOWLEDGE_RIGHTS_BASIS_NOT_OPEN", {row["code"] for row in result["failures"]})


if __name__ == "__main__":
    unittest.main()
