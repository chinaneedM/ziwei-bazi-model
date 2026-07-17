from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from fortune_v1.reporting import _validate_chat_work_runner


class InstallFreezeGateRegistrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registration = json.loads(
            Path("config/external-runner.json").read_text(encoding="utf-8")
        )

    def test_registered_handoff_freeze_gate_passes(self):
        passed, summary = _validate_chat_work_runner(self.registration)
        self.assertTrue(passed)
        self.assertEqual(summary["freeze_gate_status"], "ENFORCED")
        self.assertTrue(summary["checks"]["freeze_gate"])

    def test_missing_freeze_gate_fails_install_validation(self):
        registration = copy.deepcopy(self.registration)
        registration.pop("freeze_gate")
        passed, summary = _validate_chat_work_runner(registration)
        self.assertFalse(passed)
        self.assertFalse(summary["checks"]["freeze_gate"])

    def test_weakened_hash_replay_fails_install_validation(self):
        registration = copy.deepcopy(self.registration)
        registration["freeze_gate"]["prediction_hash_replay_required"] = False
        passed, summary = _validate_chat_work_runner(registration)
        self.assertFalse(passed)
        self.assertFalse(summary["checks"]["freeze_gate"])


if __name__ == "__main__":
    unittest.main()
