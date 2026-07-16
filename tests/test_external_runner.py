from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fortune_v1.external_runner import import_chat_work_prediction
from fortune_v1.util import FortuneError


class ChatWorkRunnerTests(unittest.TestCase):
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

    def _fixtures(self, root: Path):
        contract_path = root / "contract.json"
        run_path = root / "submitted-run.json"
        contract = {
            "schema": "PREDICTION-RUN-CONTRACT-V1",
            "case_id": "CASE-1",
            "dataset_type": "DEV",
            "snapshot": {
                "path": "data/snapshots/SNAP-1/manifest.json",
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
        run = {
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
        run_path.write_text(json.dumps(run), encoding="utf-8")
        return run_path, contract_path, run, contract

    def test_chat_only_handoff_passes_without_api(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_path, contract_path, _, _ = self._fixtures(root)
            output = root / "prediction-run.json"
            receipt_path = root / "handoff-receipt.json"
            receipt = import_chat_work_prediction(
                run_path, contract_path, output, receipt_path,
                "CHAT_ONLY", "CASE-1-SESSION",
            )
            self.assertEqual(receipt["status"], "PASS")
            self.assertFalse(receipt["api_service_required"])
            self.assertFalse(receipt["background_execution"])
            self.assertEqual(receipt["prediction_run_validation"]["status"], "PASS")
            persisted = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(persisted["execution_context"]["session_mode"], "CHAT_ONLY")

    def test_work_mode_is_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_path, contract_path, _, _ = self._fixtures(root)
            receipt = import_chat_work_prediction(
                run_path, contract_path,
                root / "prediction-run.json", root / "handoff-receipt.json",
                "WORK", "WORK-SESSION-1",
            )
            self.assertEqual(receipt["session_mode"], "WORK")

    def test_answer_bearing_contract_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_path, contract_path, _, contract = self._fixtures(root)
            contract["answer_data_available"] = True
            contract_path.write_text(json.dumps(contract), encoding="utf-8")
            with self.assertRaises(FortuneError) as ctx:
                import_chat_work_prediction(
                    run_path, contract_path,
                    root / "prediction-run.json", root / "handoff-receipt.json",
                    "CHAT_ONLY", "SESSION-1",
                )
            self.assertEqual(ctx.exception.status, "CHAT_WORK_ANSWER_ISOLATION_FAILED")

    def test_invalid_prediction_fails_without_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_path, contract_path, run, _ = self._fixtures(root)
            run["questions"][0]["pairwise_rows"] = []
            run_path.write_text(json.dumps(run), encoding="utf-8")
            output = root / "prediction-run.json"
            receipt = root / "handoff-receipt.json"
            with self.assertRaises(FortuneError) as ctx:
                import_chat_work_prediction(
                    run_path, contract_path, output, receipt,
                    "CHAT_ONLY", "SESSION-1",
                )
            self.assertEqual(ctx.exception.status, "CHAT_WORK_PREDICTION_FAILED")
            self.assertFalse(output.exists())
            self.assertFalse(receipt.exists())

    def test_invalid_mode_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_path, contract_path, _, _ = self._fixtures(root)
            with self.assertRaises(FortuneError) as ctx:
                import_chat_work_prediction(
                    run_path, contract_path,
                    root / "prediction-run.json", root / "handoff-receipt.json",
                    "API", "SESSION-1",
                )
            self.assertEqual(ctx.exception.status, "CHAT_WORK_SESSION_MODE_INVALID")


if __name__ == "__main__":
    unittest.main()
