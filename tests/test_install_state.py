from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fortune_v1.install_state import finalize_installation_state, validate_installation_state
from fortune_v1.util import FortuneError


class InstallationStateTests(unittest.TestCase):
    def _receipt(self, root: Path, commit: str = "abc") -> Path:
        path = root / "install-receipt.json"
        path.write_text(json.dumps({
            "schema": "INSTALLATION-RECEIPT-V2",
            "status": "INSTALL_VALIDATION_CANDIDATE",
            "automation_runtime_install_status": "INSTALL_VALIDATION_CANDIDATE",
            "code_commit": commit,
            "checks": [{"check": "ALL", "status": "PASS"}],
        }), encoding="utf-8")
        return path

    def test_finalize_creates_separate_validated_seal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            receipt = self._receipt(root)
            seal_path = root / "install-state.json"
            seal = finalize_installation_state(receipt, "abc", seal_path)
            self.assertEqual(seal["status"], "INSTALLED_VALIDATED")
            self.assertEqual(validate_installation_state(seal_path, receipt, "abc")["status"], "INSTALLED_VALIDATED")

    def test_receipt_drift_requires_revalidation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            receipt = self._receipt(root)
            seal_path = root / "install-state.json"
            finalize_installation_state(receipt, "abc", seal_path)
            receipt.write_text(receipt.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            result = validate_installation_state(seal_path, receipt, "abc")
            self.assertEqual(result["status"], "REVALIDATION_REQUIRED")
            self.assertIn("INSTALL_RECEIPT_HASH_DRIFT", result["errors"])

    def test_commit_drift_requires_revalidation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            receipt = self._receipt(root)
            seal_path = root / "install-state.json"
            finalize_installation_state(receipt, "abc", seal_path)
            result = validate_installation_state(seal_path, receipt, "def")
            self.assertEqual(result["status"], "REVALIDATION_REQUIRED")
            self.assertIn("CODE_COMMIT_DRIFT", result["errors"])

    def test_non_pass_check_cannot_be_finalized(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            receipt = self._receipt(root)
            data = json.loads(receipt.read_text(encoding="utf-8"))
            data["checks"][0]["status"] = "FAIL"
            receipt.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(FortuneError):
                finalize_installation_state(receipt, "abc", root / "install-state.json")


if __name__ == "__main__":
    unittest.main()
