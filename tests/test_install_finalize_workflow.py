from __future__ import annotations

import unittest
from pathlib import Path


class InstallFinalizeWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = Path(
            ".github/workflows/finalize-installation-state.yml"
        ).read_text(encoding="utf-8")

    def test_runs_only_after_successful_main_runtime_ci(self):
        self.assertIn('workflows: ["runtime-ci"]', self.text)
        self.assertIn("workflow_run.conclusion == 'success'", self.text)
        self.assertIn("workflow_run.head_branch == 'main'", self.text)

    def test_uses_versioned_receipt_and_seal_paths(self):
        self.assertIn('reports/install-receipts/${CODE_COMMIT}.json', self.text)
        self.assertIn('reports/install-states/${CODE_COMMIT}.json', self.text)
        self.assertIn('reports/install-validations/${CODE_COMMIT}.json', self.text)

    def test_finalization_and_replay_are_both_required(self):
        self.assertIn("fortune-v1 install-finalize", self.text)
        self.assertIn("fortune-v1 install-validate", self.text)
        self.assertIn('result.get("status") != "INSTALLED_VALIDATED"', self.text)

    def test_receipt_write_commit_does_not_replace_validated_code_sha(self):
        self.assertIn("github.event.workflow_run.head_sha", self.text)
        self.assertIn('--code-commit "$CODE_COMMIT"', self.text)
        self.assertIn("[skip ci]", self.text)


if __name__ == "__main__":
    unittest.main()
