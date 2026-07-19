from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts/process-group-start-signal.py"
WORKFLOW_PATH = ROOT / ".github/workflows/repository-group-start-signal.yml"

SPEC = importlib.util.spec_from_file_location("process_group_start_signal", SCRIPT_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class GroupStartSignalTransportTests(unittest.TestCase):
    def test_signal_schema_and_fields_are_minimal(self) -> None:
        self.assertEqual(MODULE.SIGNAL_SCHEMA, "GROUP-RUNTIME-START-SIGNAL-V1")
        self.assertEqual(
            MODULE.ALLOWED_FIELDS,
            {"schema", "status", "group", "session", "mode"},
        )

    def test_workflow_accepts_only_exact_signal_directory(self) -> None:
        text = WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn("runtime/group-start-signals/*.json", text)
        self.assertIn("git diff-tree --no-commit-id --name-only", text)
        self.assertNotIn("repository search", text.lower())
        self.assertNotIn("commit history", text.lower())

    def test_workflow_runs_repository_processors_and_validators(self) -> None:
        text = WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn("scripts/process-group-start-signal.py", text)
        self.assertIn("tests.test_bootstrap_request", text)
        self.assertIn("tests.test_clean_start", text)
        self.assertIn("tests.test_staged_access", text)
        self.assertIn("tests.test_end_to_end_pipeline", text)
        self.assertIn("runtime_validation_status", text)
        self.assertIn("prediction_context_started", text)

    def test_generated_write_scope_is_restricted(self) -> None:
        text = WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn("runtime/clean-start-requests/*.json", text)
        self.assertIn("data/group-clean-starts/*/*", text)
        self.assertIn("reports/clean-start-preauthorization/*.json", text)
        self.assertNotIn("git add .", text)
        self.assertNotIn("git add -A", text)

    def test_receipt_preserves_future_context_and_scoring_boundaries(self) -> None:
        text = SCRIPT_PATH.read_text(encoding="utf-8")
        self.assertIn("NOT_STARTED_REQUIRES_FRESH_PREDICTION_CONTEXT", text)
        self.assertIn("NONE_BEFORE_PREDICTION_FREEZE_AND_CAUSAL_USE_RECEIPT", text)
        self.assertIn("FETCH_EXACT_CLEAN_START_PATH_ONLY", text)
        self.assertIn('clean.get("answer_data_available") is False', text)


if __name__ == "__main__":
    unittest.main()
