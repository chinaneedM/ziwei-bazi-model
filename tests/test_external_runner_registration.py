from __future__ import annotations

import unittest

from fortune_v1.reporting import _validate_chat_work_runner


class ChatWorkRunnerRegistrationTests(unittest.TestCase):
    @staticmethod
    def _registration() -> dict:
        return {
            "runner_id": "CHAT-WORK-HANDOFF-V1",
            "runner_type": "CHAT_WORK_INTERACTIVE_EXECUTOR",
            "model_or_executor": "CHATGPT_PROJECT_SESSION",
            "interaction_modes": ["CHAT_ONLY", "WORK"],
            "execution_model": "USER_INITIATED_INTERACTIVE_SESSION",
            "background_execution": False,
            "api_service_required": False,
            "adapter": {
                "module": "fortune_v1.external_runner",
                "cli_command": "fortune-v1 chat-work-import",
                "status": "INSTALLED",
                "workflow_path": ".github/workflows/external-runner-smoke.yml",
            },
            "input_contract": "PREDICTION-RUN-CONTRACT-V1",
            "output_schema": "PREDICTION-RUN-V1",
            "timeout_seconds": 1800,
            "failure_status": "CHAT_WORK_PREDICTION_FAILED",
            "no_answer_access_proof": {
                "status": "ENFORCED_PER_RUN",
                "contract_answer_data_available_required_false": True,
                "prediction_forbidden_scan_required": True,
                "active_whitelist_required": True,
                "runtime_repository_vault_credential": "NONE",
                "answer_vault_read_allowed": False,
            },
            "prompt_binding": {
                "runtime_id": "MP-PROFESSIONAL-REASONING-20260715-R16",
                "audit_snapshot_sha256": "832dd43129b6e5d3098c972a55179ccb7e9ab49a9770339a87c94deaa440b017",
                "runtime_authority": "PROJECT_CUSTOM_INSTRUCTIONS",
            },
            "source_binding": "1766aa81fad8134c12f50c18e2e7e7b3523e098113df37bd75a9a88a2cc56654",
            "run_id_nonoverwrite": True,
            "ziwei_bazi_local_seal_requirement": True,
            "case_execution_requires_user_initiated_chat": True,
            "external_prediction_runner_status": "INSTALLED",
        }

    def test_complete_registration_passes(self):
        passed, summary = _validate_chat_work_runner(self._registration())
        self.assertTrue(passed)
        self.assertFalse(summary["api_service_required"])

    def test_api_requirement_is_rejected(self):
        registration = self._registration()
        registration["api_service_required"] = True
        passed, _ = _validate_chat_work_runner(registration)
        self.assertFalse(passed)

    def test_background_execution_claim_is_rejected(self):
        registration = self._registration()
        registration["background_execution"] = True
        passed, _ = _validate_chat_work_runner(registration)
        self.assertFalse(passed)

    def test_missing_work_mode_is_rejected(self):
        registration = self._registration()
        registration["interaction_modes"] = ["CHAT_ONLY"]
        passed, _ = _validate_chat_work_runner(registration)
        self.assertFalse(passed)

    def test_answer_vault_access_is_rejected(self):
        registration = self._registration()
        registration["no_answer_access_proof"]["answer_vault_read_allowed"] = True
        passed, _ = _validate_chat_work_runner(registration)
        self.assertFalse(passed)


if __name__ == "__main__":
    unittest.main()
