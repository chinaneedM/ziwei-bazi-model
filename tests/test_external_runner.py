from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fortune_v1.external_runner import build_runner_request, run_external_prediction
from fortune_v1.util import FortuneError


class _Response:
    def __init__(self, payload: dict, status: int = 200) -> None:
        self._body = json.dumps(payload).encode("utf-8")
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self) -> bytes:
        return self._body

    def getcode(self) -> int:
        return self.status


class ExternalRunnerTests(unittest.TestCase):
    def _fixtures(self, root: Path):
        questions_path = root / "questions.json"
        snapshot_path = root / "snapshot.json"
        contract_path = root / "contract.json"

        questions = {
            "schema": "QUESTION-SET-V1",
            "questions": [{
                "question_id": "Q1",
                "stem": "Select the stronger relative outcome.",
                "options": [
                    {"option_id": "A", "text": "Outcome one"},
                    {"option_id": "B", "text": "Outcome two"},
                ],
            }],
        }
        questions_path.write_text(json.dumps(questions), encoding="utf-8")
        snapshot = {
            "schema": "PREDICTION-INPUT-SNAPSHOT-V1",
            "snapshot_id": "SNAP-1",
            "case_id": "CASE-1",
            "dataset_type": "DEV",
            "case_input_hash": "b" * 64,
            "files": [],
            "questions_path": str(questions_path),
            "answer_scan": {"status": "PASS", "findings": []},
        }
        snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")
        contract = {
            "schema": "PREDICTION-RUN-CONTRACT-V1",
            "case_id": "CASE-1",
            "dataset_type": "DEV",
            "snapshot": {
                "path": str(snapshot_path),
                "sha256": "a" * 64,
                "case_input_hash": "b" * 64,
            },
            "binding": {
                "library_binding_hash": "c" * 64,
                "main_prompt_runtime_id": "MP-PROFESSIONAL-REASONING-20260715-R16",
                "prompt_snapshot_sha256": "d" * 64,
                "code_commit": "e" * 40,
                "schema_version": "FORTUNE-AUTOMATION-V1",
            },
            "questions": [{
                "question_id": "Q1",
                "option_ids": ["A", "B"],
                "required_pairwise_rows": 1,
            }],
            "answer_data_available": False,
        }
        contract_path.write_text(json.dumps(contract), encoding="utf-8")
        return questions_path, snapshot_path, contract_path, contract

    @staticmethod
    def _ledger_entry(track: str, source: str, family: str) -> dict:
        return {
            "track": track,
            "source_library": source,
            "method": "TEST_METHOD",
            "knowledge_point": "test knowledge",
            "source_root_atom": "root",
            "parent_segment": "segment",
            "physical_selector": "selector",
            "conditions": [],
            "limitations_negations_exceptions": [],
            "target_atom": "target",
            "semantic_direction": "SUPPORT",
            "capability_ceiling": "RELATIVE_ONLY",
            "temporal_role": "STRUCTURAL",
            "evidence_family": family,
            "dedup_status": "UNIQUE",
            "downstream_effect": "changed ranking",
        }

    def _valid_run(self, contract: dict) -> dict:
        return {
            "schema": "PREDICTION-RUN-V1",
            "run_id": "RUN-1",
            "case_id": "CASE-1",
            "dataset_type": "DEV",
            "binding": contract["binding"],
            "cold_start": True,
            "input_snapshot": {
                "path": contract["snapshot"]["path"],
                "sha256": contract["snapshot"]["sha256"],
            },
            "questions": [{
                "question_id": "Q1",
                "option_ids": ["A", "B"],
                "top1": "A",
                "top2": "B",
                "confidence": 0.6,
                "blind_core": "Independent blind model.",
                "public_evidence": [
                    {"evidence_family": "F1"},
                    {"evidence_family": "F2"},
                    {"evidence_family": "F3"},
                ],
                "strongest_competitor_reason": "B has weaker compound coverage.",
                "most_important_unverified_atom": "Exact endpoint remains unverified.",
                "ziwei_track": {
                    "validation_status": "PASS",
                    "local_seal": True,
                    "parent_libraries": ["S05"],
                    "blind_model_hash": "ziwei-model-hash",
                },
                "bazi_track": {
                    "validation_status": "PASS",
                    "local_seal": True,
                    "parent_libraries": ["S11"],
                    "blind_model_hash": "bazi-model-hash",
                },
                "fusion": {"status": "NO_INCREMENT"},
                "coverage_plan": {"status": "COMPLETE"},
                "evidence_ledger": [
                    self._ledger_entry("ZIWEI", "S05", "L1"),
                    self._ledger_entry("BAZI", "S11", "L2"),
                    self._ledger_entry("ZIWEI", "S08", "L3"),
                ],
                "direction_matrix": {"A": {}, "B": {}},
                "compound_coverage": {"A": {}, "B": {}},
                "pairwise_rows": [{"left": "A", "right": "B", "winner": "A"}],
                "formal_exact_assertion": None,
            }],
            "runtime_validation": {"status": "PASS", "checks": []},
        }

    def test_request_is_answer_isolated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, snapshot_path, contract_path, _ = self._fixtures(root)
            payload = build_runner_request(snapshot_path, contract_path, "RUNNER-1")
            self.assertFalse(payload["answer_data_available"])
            self.assertEqual(payload["repository_access"]["runtime_repository_vault_credential"], "NONE")
            serialized = json.dumps(payload, ensure_ascii=False)
            self.assertNotIn("correct_answer", serialized)
            self.assertNotIn("answer_key", serialized)

    def test_invalid_contract_is_rejected_before_transport(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, snapshot_path, contract_path, contract = self._fixtures(root)
            contract["answer_data_available"] = True
            contract_path.write_text(json.dumps(contract), encoding="utf-8")
            with self.assertRaises(FortuneError) as ctx:
                build_runner_request(snapshot_path, contract_path, "RUNNER-1")
            self.assertEqual(ctx.exception.status, "EXTERNAL_RUNNER_ANSWER_ISOLATION_FAILED")

    def test_valid_remote_run_is_written_with_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, snapshot_path, contract_path, contract = self._fixtures(root)
            output_path = root / "prediction-run.json"
            receipt_path = root / "runner-receipt.json"
            response = _Response(self._valid_run(contract))
            with patch("urllib.request.urlopen", return_value=response):
                receipt = run_external_prediction(
                    snapshot_path,
                    contract_path,
                    "https://runner.example/v1/predict",
                    output_path,
                    receipt_path,
                    "RUNNER-1",
                    token="secret-used-in-memory-only",
                    timeout_seconds=30,
                )
            self.assertEqual(receipt["status"], "PASS")
            self.assertTrue(output_path.is_file())
            self.assertTrue(receipt_path.is_file())
            self.assertFalse(receipt["token_value_persisted"])
            self.assertEqual(receipt["no_answer_access_proof"]["request_forbidden_scan"], "PASS")
            persisted = receipt_path.read_text(encoding="utf-8")
            self.assertNotIn("secret-used-in-memory-only", persisted)

    def test_invalid_remote_run_fails_closed_without_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, snapshot_path, contract_path, contract = self._fixtures(root)
            output_path = root / "prediction-run.json"
            receipt_path = root / "runner-receipt.json"
            invalid = self._valid_run(contract)
            invalid["questions"][0]["pairwise_rows"] = []
            with patch("urllib.request.urlopen", return_value=_Response(invalid)):
                with self.assertRaises(FortuneError) as ctx:
                    run_external_prediction(
                        snapshot_path,
                        contract_path,
                        "https://runner.example/v1/predict",
                        output_path,
                        receipt_path,
                        "RUNNER-1",
                    )
            self.assertEqual(ctx.exception.status, "EXTERNAL_PREDICTION_RUNNER_FAILED")
            self.assertFalse(output_path.exists())
            self.assertFalse(receipt_path.exists())


if __name__ == "__main__":
    unittest.main()
