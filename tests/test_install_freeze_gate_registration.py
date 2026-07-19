from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path


class InstallFreezeGateRegistrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registration = json.loads(
            Path("config/external-runner.json").read_text(encoding="utf-8")
        )

    @staticmethod
    def validate(registration: dict) -> tuple[bool, dict]:
        gate = registration.get("freeze_gate") if isinstance(registration.get("freeze_gate"), dict) else {}
        checks = {
            "runner_schema": registration.get("schema") == "EXTERNAL-RUNNER-INSTALLATION-V2",
            "user_started": registration.get("user_initiated_session_required") is True,
            "no_background": registration.get("background_execution") is False,
            "no_answer_data": registration.get("answer_data_available") is False,
            "freeze_status": gate.get("status") == "ENFORCED",
            "receipt_schema": gate.get("required_receipt_schema") == "CHAT-WORK-PREDICTION-HANDOFF-RECEIPT-V1",
            "origin_schema": gate.get("origin_validation_schema") == "CHAT-WORK-HANDOFF-VALIDATION-V1",
            "prediction_hash": gate.get("prediction_hash_replay_required") is True,
            "contract_hash": gate.get("contract_hash_replay_required") is True,
            "binding_replay": gate.get("identity_and_binding_replay_required") is True,
            "group_before_reveal": gate.get("group_freeze_before_reveal_required") is True,
            "no_early_answer": gate.get("answer_access_before_group_freeze") is False,
        }
        return all(checks.values()), checks

    def test_registered_handoff_freeze_gate_passes(self):
        passed, checks = self.validate(self.registration)
        self.assertTrue(passed, checks)
        self.assertTrue(checks["group_before_reveal"])
        self.assertTrue(checks["no_early_answer"])

    def test_missing_freeze_gate_fails_install_validation(self):
        registration = copy.deepcopy(self.registration)
        registration.pop("freeze_gate")
        passed, checks = self.validate(registration)
        self.assertFalse(passed)
        self.assertFalse(checks["freeze_status"])

    def test_weakened_hash_replay_fails_install_validation(self):
        registration = copy.deepcopy(self.registration)
        registration["freeze_gate"]["prediction_hash_replay_required"] = False
        passed, checks = self.validate(registration)
        self.assertFalse(passed)
        self.assertFalse(checks["prediction_hash"])

    def test_early_answer_access_fails_install_validation(self):
        registration = copy.deepcopy(self.registration)
        registration["freeze_gate"]["answer_access_before_group_freeze"] = True
        passed, checks = self.validate(registration)
        self.assertFalse(passed)
        self.assertFalse(checks["no_early_answer"])


if __name__ == "__main__":
    unittest.main()
