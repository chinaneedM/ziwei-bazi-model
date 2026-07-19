from __future__ import annotations

import unittest
from pathlib import Path


class InstallFinalizeWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = Path(
            ".github/workflows/finalize-installation-state.yml"
        ).read_text(encoding="utf-8")

    def test_runs_only_after_successful_main_final_install_check(self):
        self.assertIn('workflows: ["final-install-check"]', self.text)
        self.assertIn("workflow_run.conclusion == 'success'", self.text)
        self.assertIn("workflow_run.head_branch == 'main'", self.text)

    def test_replays_v3_on_exact_validated_commit(self):
        self.assertIn("github.event.workflow_run.head_sha", self.text)
        self.assertIn('ref: ${{ github.event.workflow_run.head_sha }}', self.text)
        self.assertIn('EXPECTED_COMMIT="$CODE_COMMIT"', self.text)
        self.assertIn("ACTIVATION_MODE=main", self.text)
        self.assertIn("make install-check", self.text)

    def test_enforces_installed_status_and_training_boundaries(self):
        self.assertIn("FINAL-OPEN-SOURCE-INSTALL-CHECK-RECEIPT-V3", self.text)
        self.assertIn("INSTALLED_VALIDATED_READY_FOR_USER_INITIATED_CLEAN_START", self.text)
        self.assertIn("READY_FOR_USER_INITIATED_CLEAN_START_ONLY", self.text)
        self.assertIn("CONDITIONAL_PER_RUN_CAUSAL_USE_RECEIPT_PASS", self.text)
        self.assertIn("background execution boundary invalid", self.text)

    def test_readback_is_artifact_only_and_cannot_mutate_main(self):
        self.assertIn("permissions:\n  contents: read", self.text)
        self.assertIn("actions/upload-artifact@v4", self.text)
        self.assertNotIn("git commit", self.text)
        self.assertNotIn("git push", self.text)
        self.assertNotIn("git rebase", self.text)
        self.assertNotIn("fortune-v1 install-finalize", self.text)
        self.assertNotIn("fortune-v1 install-validate", self.text)


if __name__ == "__main__":
    unittest.main()
