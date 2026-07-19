from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "verify-public-only-repository.py"
SPEC = importlib.util.spec_from_file_location("verify_public_only_repository", SCRIPT_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PublicRepositoryPolicyTests(unittest.TestCase):
    def write(self, path: Path, body: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")

    def required_files(self) -> list[str]:
        return [
            "LICENSE",
            "NOTICE",
            "README.md",
            "CONTRIBUTING.md",
            "GOVERNANCE.md",
            "SECURITY.md",
            "docs/open-source-architecture.md",
            "licenses/README.md",
            "licenses/knowledge-pack-manifest.schema.json",
            "config/open-source-release.json",
        ]

    def policy(self, root: Path) -> None:
        self.write(root / "config/public-repository-policy.json", json.dumps({
            "schema": "PUBLIC-REPOSITORY-POLICY-V1",
            "project_mode": "COMPLETE_OPEN_SOURCE",
            "required_repository_visibility": "public",
            "single_repository_runtime": True,
            "required_software_license": "Apache-2.0",
            "open_source_release_contract_path": "config/open-source-release.json",
            "required_open_source_files": self.required_files(),
            "allowed_answer_secret_names": ["FORTUNE_PUBLIC_ANSWER_KEY"],
            "forbidden_literals": ["private-answer-repository", "OLD_ANSWER_TOKEN"],
            "active_scan_roots": [".github/workflows", "src", "scripts", "runtime", "config", "pyproject.toml"],
            "plaintext_answer_repository_patterns": ["public-answer-vault/**/*.json", "public-answer-vault/**/*.txt"],
            "allowed_public_answer_patterns": ["public-answer-vault/README.md", "public-answer-vault/encrypted/*.json.fernet"],
        }, indent=2))

    def fixture(self, root: Path) -> None:
        self.policy(root)
        for path in self.required_files():
            self.write(root / path, f"fixture {path}\n")
        self.write(root / "pyproject.toml", "[project]\nname='fixture'\nversion='1.0.0'\nlicense='Apache-2.0'\n")
        self.write(root / ".github/workflows/ci.yml", "steps:\n  - uses: actions/checkout@v4\n")
        self.write(root / "src/example.py", "SECRET = '${{ secrets.FORTUNE_PUBLIC_ANSWER_KEY }}'\n")
        self.write(root / "public-answer-vault/README.md", "encrypted only\n")
        self.write(root / "public-answer-vault/encrypted/RUN.json.fernet", "ciphertext\n")

    def test_public_single_repository_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            result = MODULE.verify(root, "public")
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["project_mode"], "COMPLETE_OPEN_SOURCE")
            self.assertEqual(result["software_license"], "Apache-2.0")

    def test_private_visibility_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            result = MODULE.verify(root, "private")
            self.assertEqual(result["status"], "FAIL")
            self.assertIn("REPOSITORY_VISIBILITY_NOT_PUBLIC", {row["code"] for row in result["failures"]})

    def test_cross_repository_checkout_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            self.write(root / ".github/workflows/ci.yml", "with:\n  repository: owner/other-repo\n")
            result = MODULE.verify(root, "public")
            self.assertIn("CROSS_REPOSITORY_CHECKOUT_FORBIDDEN", {row["code"] for row in result["failures"]})

    def test_plaintext_answer_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            self.write(root / "public-answer-vault/encrypted/RUN.json", '{"answer":"A"}\n')
            result = MODULE.verify(root, "public")
            self.assertIn("PLAINTEXT_ANSWER_FILE_FORBIDDEN", {row["code"] for row in result["failures"]})

    def test_missing_open_source_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            (root / "GOVERNANCE.md").unlink()
            result = MODULE.verify(root, "public")
            self.assertIn("REQUIRED_OPEN_SOURCE_FILE_MISSING", {row["code"] for row in result["failures"]})

    def test_package_license_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            self.write(root / "pyproject.toml", "[project]\nname='fixture'\nversion='1.0.0'\nlicense='Proprietary'\n")
            result = MODULE.verify(root, "public")
            self.assertIn("PACKAGE_LICENSE_METADATA_MISMATCH", {row["code"] for row in result["failures"]})


if __name__ == "__main__":
    unittest.main()
