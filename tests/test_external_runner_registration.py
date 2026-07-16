from __future__ import annotations

import unittest

from fortune_v1.reporting import _validate_live_external_runner


class ExternalRunnerRegistrationTests(unittest.TestCase):
    @staticmethod
    def _registration() -> dict:
        return {
            "runner_id": "FORTUNE-EXTERNAL-DUAL-TRACK-V1",
            "runner_type": "EXTERNAL_DUAL_TRACK_PREDICTION_EXECUTOR",
            "model_or_executor": "REMOTE-MODEL-SERVICE-V1",
            "input_contract": "PREDICTION-RUN-CONTRACT-V1",
            "output_schema": "PREDICTION-RUN-V1",
            "timeout_seconds": 1800,
            "failure_status": "EXTERNAL_PREDICTION_RUNNER_FAILED",
            "code_commit": "a" * 40,
            "source_binding": "b" * 64,
            "prompt_binding": {
                "runtime_id": "MP-PROFESSIONAL-REASONING-20260715-R16",
                "audit_snapshot_sha256": "c" * 64,
            },
            "run_id_nonoverwrite": True,
            "ziwei_bazi_local_seal_requirement": True,
            "no_answer_access_proof": {
                "status": "PASS",
                "answer_data_available": False,
                "request_forbidden_scan": "PASS",
                "runtime_repository_vault_credential": "NONE",
                "token_value_persisted": False,
                "live_receipt_sha256": "d" * 64,
            },
            "activation_receipt": {
                "status": "PASS",
                "fresh_unrevealed_dev_case": True,
                "prediction_run_validation": "PASS",
                "ziwei_bazi_independent_local_seals": "PASS",
                "frozen_before_reveal": True,
                "run_id_nonoverwrite": True,
            },
            "external_prediction_runner_status": "INSTALLED",
        }

    def test_complete_live_registration_passes(self):
        passed, summary = _validate_live_external_runner(self._registration())
        self.assertTrue(passed)
        self.assertEqual(summary["activation_status"], "PASS")

    def test_status_string_without_live_proof_fails(self):
        registration = self._registration()
        registration["no_answer_access_proof"] = {
            "status": "PENDING_LIVE_PROVIDER_ATTESTATION"
        }
        passed, _ = _validate_live_external_runner(registration)
        self.assertFalse(passed)

    def test_unbound_or_fixture_executor_fails(self):
        for executor in ["UNBOUND_REMOTE_DUAL_TRACK_EXECUTOR", "FIXTURE", "PLACEHOLDER"]:
            with self.subTest(executor=executor):
                registration = self._registration()
                registration["model_or_executor"] = executor
                passed, _ = _validate_live_external_runner(registration)
                self.assertFalse(passed)

    def test_reveal_or_overwrite_gap_fails(self):
        registration = self._registration()
        registration["activation_receipt"]["frozen_before_reveal"] = False
        passed, _ = _validate_live_external_runner(registration)
        self.assertFalse(passed)


if __name__ == "__main__":
    unittest.main()
