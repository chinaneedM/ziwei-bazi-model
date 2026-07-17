from __future__ import annotations

import unittest

from fortune_v1.prediction import validate_prediction_run


class PredictionValidatorHardeningTests(unittest.TestCase):
    def _contract(self):
        return {
            "case_id": "CASE-1",
            "dataset_type": "DEV",
            "snapshot": {"path": "snapshot.json", "sha256": "snap"},
            "binding": {"library_binding_hash": "bind", "main_prompt_runtime_id": "R16", "prompt_snapshot_sha256": "prompt", "code_commit": "commit", "schema_version": "1"},
            "questions": [{"question_id": "Q1", "option_ids": ["A", "B"], "required_pairwise_rows": 1}],
        }

    def _seal(self, prefix):
        return {
            "seal_id": f"{prefix}-seal",
            "canonical_hash": f"{prefix}-canonical",
            "body_hash": f"{prefix}-body",
            "machine_validation_report_id": f"{prefix}-report",
            "validation_status": "PASS",
            "s18_local_adjudication_object_id": f"{prefix}-s18",
            "parent_object_ids": [f"{prefix}-parent"],
        }

    def _track(self, prefix, library):
        return {
            "validation_status": "PASS",
            "local_seal": self._seal(prefix),
            "parent_libraries": [library],
            "blind_model_hash": f"{prefix}-blind",
        }

    def _run(self):
        direction = lambda atom: [{"atom_id": atom, "status": "UNKNOWN", "parent_ids": []}]
        compound = lambda atom: {
            "material_required_atom_ids": [atom],
            "satisfied_atom_ids": [],
            "partial_atom_ids": [],
            "missing_atom_ids": [atom],
            "contradicted_atom_ids": [],
            "reference_period_status": "UNKNOWN",
            "coverage_status": "PARTIAL_NO_DIRECTION",
        }
        return {
            "schema": "PREDICTION-RUN-V1",
            "case_id": "CASE-1",
            "dataset_type": "DEV",
            "binding": self._contract()["binding"],
            "run_id": "RUN-1",
            "cold_start": True,
            "input_snapshot": {"path": "snapshot.json", "sha256": "snap"},
            "questions": [{
                "question_id": "Q1",
                "option_ids": ["A", "B"],
                "top1": "A",
                "top2": "B",
                "confidence": 0.4,
                "public_evidence": [
                    {"evidence_family": "F1"},
                    {"evidence_family": "F2"},
                    {"evidence_family": "F3"},
                ],
                "pairwise_rows": [{
                    "left": "A", "right": "B", "winner": "A",
                    "decision_basis": "forced low-information decision",
                    "distinctive_atom_comparison": {"A": "unknown", "B": "unknown"},
                }],
                "ziwei_track": self._track("ziwei", "S07"),
                "bazi_track": self._track("bazi", "S16"),
                "evidence_ledger": [{
                    "track": "ZIWEI", "source_library": "S07", "method": "test",
                    "knowledge_point": "test", "source_root_atom": "root",
                    "parent_segment": "parent", "physical_selector": "selector",
                    "conditions": [], "limitations_negations_exceptions": [],
                    "target_atom": "A1", "semantic_direction": "UNKNOWN",
                    "capability_ceiling": "L1", "temporal_role": "STATIC",
                    "evidence_family": "F1", "dedup_status": "UNIQUE",
                    "downstream_effect": "NO_RANK_CHANGE",
                }],
                "coverage_plan": {
                    "status": "COMPLETE",
                    "distinctive_atom_rows": [{"atom": "A1"}],
                    "required_source_family_rows": [{"family": "S07"}],
                    "actual_route_rows": [{"route": "S07"}],
                    "unresolved_required_routes": [],
                },
                "direction_matrix": {"A": direction("A1"), "B": direction("B1")},
                "compound_coverage": {"A": compound("A1"), "B": compound("B1")},
                "formal_exact_assertion": None,
                "strongest_competitor_reason": "B is the only rival",
                "most_important_unverified_atom": "A1",
            }],
        }

    def test_complete_object_passes_with_one_real_ledger_row(self):
        result = validate_prediction_run(self._run(), self._contract())
        self.assertEqual(result["status"], "PASS", result["errors"])
        self.assertNotIn("Q1:EVIDENCE_LEDGER_TOO_SHORT", result["errors"])

    def test_boolean_local_seal_is_rejected(self):
        run = self._run()
        run["questions"][0]["ziwei_track"]["local_seal"] = True
        result = validate_prediction_run(run, self._contract())
        self.assertIn("Q1:ZIWEI:LOCAL_SEAL_BODY_MISSING", result["errors"])

    def test_pairwise_row_requires_literal_decision_payload(self):
        run = self._run()
        del run["questions"][0]["pairwise_rows"][0]["decision_basis"]
        result = validate_prediction_run(run, self._contract())
        self.assertIn("Q1:PAIRWISE_0_DECISION_BASIS_MISSING", result["errors"])

    def test_unresolved_required_route_fails_closed(self):
        run = self._run()
        run["questions"][0]["coverage_plan"]["unresolved_required_routes"] = ["S09"]
        result = validate_prediction_run(run, self._contract())
        self.assertIn("Q1:COVERAGE_PLAN_HAS_UNRESOLVED_REQUIRED_ROUTES", result["errors"])


if __name__ == "__main__":
    unittest.main()
