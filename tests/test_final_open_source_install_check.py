from __future__ import annotations

import importlib.util
import subprocess
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "final-open-source-install-check.py"
SPEC = importlib.util.spec_from_file_location("final_open_source_install_check", SCRIPT_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class FinalOpenSourceInstallCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]
        cls.commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=cls.root, text=True
        ).strip()

    def test_current_repository_candidate_passes(self) -> None:
        receipt = MODULE.verify(
            self.root,
            "public",
            self.commit,
            "candidate",
            True,
            None,
        )
        self.assertEqual(receipt["status"], "INSTALL_CHECK_PASS_CANDIDATE", receipt)
        self.assertEqual(receipt["failure_count"], 0, receipt)
        self.assertEqual(receipt["pass_count"], receipt["check_count"])
        self.assertEqual(receipt["formal_open_source_release_permission"], "PASS")
        self.assertEqual(receipt["formal_training_permission"], "BLOCKED_PENDING_MAIN_BRANCH_INSTALL_CHECK")
        self.assertEqual(receipt["score_eligibility"], "CONDITIONAL_PER_RUN_CAUSAL_USE_RECEIPT_PASS")

    def test_private_visibility_fails_closed(self) -> None:
        receipt = MODULE.verify(
            self.root,
            "private",
            self.commit,
            "candidate",
            True,
            None,
        )
        self.assertEqual(receipt["status"], "INSTALL_CHECK_FAIL")
        self.assertGreater(receipt["failure_count"], 0)
        failed = {row["check"] for row in receipt["checks"] if row["status"] == "FAIL"}
        self.assertIn("PUBLIC_REPOSITORY_VISIBILITY", failed)
        self.assertIn("PUBLIC_ONLY_REPOSITORY_POLICY", failed)
        self.assertIn("ACTIVE_KNOWLEDGE_R17_CC0_RELEASE", failed)

    def test_missing_same_target_test_evidence_fails_closed(self) -> None:
        receipt = MODULE.verify(
            self.root,
            "public",
            self.commit,
            "candidate",
            False,
            None,
        )
        self.assertEqual(receipt["status"], "INSTALL_CHECK_FAIL")
        failed = {row["check"] for row in receipt["checks"] if row["status"] == "FAIL"}
        self.assertIn("COMPLETE_TEST_SUITES_IN_SAME_INSTALL_CHECK", failed)

    def test_wrong_expected_commit_fails_closed(self) -> None:
        receipt = MODULE.verify(
            self.root,
            "public",
            "0" * 40,
            "candidate",
            True,
            None,
        )
        self.assertEqual(receipt["status"], "INSTALL_CHECK_FAIL")
        failed = {row["check"] for row in receipt["checks"] if row["status"] == "FAIL"}
        self.assertIn("EXACT_COMMIT", failed)


if __name__ == "__main__":
    unittest.main()
