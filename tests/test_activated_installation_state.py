from __future__ import annotations

import importlib.util
import subprocess
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "verify-activated-installation-state.py"
SPEC = importlib.util.spec_from_file_location("verify_activated_installation_state", SCRIPT_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ActivatedInstallationStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]
        cls.commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=cls.root, text=True
        ).strip()

    def test_current_candidate_state_passes(self) -> None:
        receipt = MODULE.verify(self.root, self.commit, "candidate", None)
        self.assertEqual(receipt["status"], "PASS", receipt)
        self.assertEqual(receipt["failure_count"], 0, receipt)
        self.assertEqual(receipt["pass_count"], receipt["check_count"])
        self.assertEqual(receipt["formal_open_source_release_permission"], "PASS")
        self.assertEqual(receipt["formal_training_permission"], "READY_FOR_USER_INITIATED_CLEAN_START_ONLY")
        self.assertEqual(receipt["score_eligibility"], "CONDITIONAL_PER_RUN_CAUSAL_USE_RECEIPT_PASS")
        self.assertFalse(receipt["background_execution"])

    def test_wrong_current_commit_fails_closed(self) -> None:
        receipt = MODULE.verify(self.root, "0" * 40, "candidate", None)
        self.assertEqual(receipt["status"], "FAIL")
        failed = {row["check"] for row in receipt["checks"] if row["status"] == "FAIL"}
        self.assertIn("CURRENT_COMMIT", failed)
        self.assertIn("VALIDATED_MAIN_IS_ANCESTOR", failed)

    def test_state_and_contract_are_machine_verified(self) -> None:
        receipt = MODULE.verify(self.root, self.commit, "candidate", None)
        passed = {row["check"] for row in receipt["checks"] if row["status"] == "PASS"}
        self.assertIn("INSTALL_STATE_OBJECT_HASH", passed)
        self.assertIn("INSTALL_STATE_FIELDS", passed)
        self.assertIn("MAIN_READBACK_OBJECT", passed)
        self.assertIn("FINAL_ACTIVATION_RECEIPT", passed)
        self.assertIn("OPEN_SOURCE_RELEASE_CONTRACT_ACTIVATED", passed)


if __name__ == "__main__":
    unittest.main()
