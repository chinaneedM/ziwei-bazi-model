from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fortune_v1.training_corrected import create_cycle
from fortune_v1.training_finalize import finalize_group_training
from fortune_v1.util import FortuneError, canonical_bytes, sha256_bytes, sha256_file


def with_hash(value: dict) -> dict:
    body = dict(value)
    body.pop("object_hash", None)
    body["object_hash"] = sha256_bytes(canonical_bytes(body))
    return body


def write_json(path: Path, value: dict, *, hashed: bool = False) -> dict:
    body = with_hash(value) if hashed else value
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return body


def reasoning(unit_id: str) -> dict:
    return with_hash({
        "schema": "REASONING-CORRECTION-OBJECT-V2.1",
        "unit_id": unit_id,
        "error_mechanisms": [{"id": "E1", "mechanism": "synthetic mechanism correction"}],
        "source_parent_chains": [{
            "library_id": "S02",
            "active_file_sha256": "a" * 64,
            "excerpt_sha256": "b" * 64,
            "line_ranges": ["1-2"],
            "knowledge_point": "synthetic exact scope",
            "applicability_conditions": ["synthetic fixture only"],
            "capability_ceiling": "RELATIVE_DIRECTION_ONLY",
            "downstream_effect": "closes synthetic competitor",
        }],
        "corrected_reasoning_order": ["scope", "evidence", "endpoint", "pairwise"],
        "capability_ceiling_and_no_overreach": ["no formal exact assertion"],
        "applicability_conditions": ["synthetic fixture only"],
        "counterexamples_and_failure_boundaries": ["not transferable to real cases"],
        "option_semantics": [
            {"option_id": "A", "concept": "synthetic A"},
            {"option_id": "B", "concept": "synthetic B"},
        ],
        "pairwise_rows": [{
            "row_id": "AB",
            "left": "A",
            "right": "B",
            "direction": "LEFT_AHEAD",
            "decisive_rule": "DISTINCTIVE_ATOM_DIRECT_SUPPORT",
            "reason": "synthetic deterministic fixture",
            "left_vector": {},
            "right_vector": {},
        }],
        "strongest_competitor": {"relative_first": "A", "relative_second": "B", "pairwise_row_id": "AB"},
        "contamination_and_answer_memory_audit": {
            "original_first_blind_preserved": True,
            "post_reveal_replays_excluded_from_accuracy": True,
            "generic_rule_has_no_case_or_option_fixed_selection": True,
            "bazi_variant_not_selected_by_revealed_result": True,
            "base_knowledge_not_promoted_from_single_unit": True,
            "case_specific_rule_detected": False,
            "answer_memorization_rule_detected": False,
            "status": "PASS",
        },
        "training_unit_conclusion": {"status": "TRAINING_UNIT_COMPLETE_CANDIDATE"},
    })


class TrainingFinalizeTests(unittest.TestCase):
    def fixture(self, root: Path, *, case_count: int = 5, questions_per_case: int = 5) -> tuple[Path, Path, list[Path]]:
        group_run_id = "GROUP-RUN-FINALIZE-1"
        group_id = "DEV-GROUP-002"
        run_root = root / "data" / "group-clean-starts" / group_run_id
        training_root = run_root / "training"
        units = []
        observations = {}
        for case_index in range(1, case_count + 1):
            case_id = f"DEV-EXAMPLE-{case_index:03d}"
            for question_index in range(1, questions_per_case + 1):
                question_id = f"Q{question_index}"
                unit_id = f"{case_id}-{question_id}"
                observation = {
                    "distinct_question_key": f"{case_id}::{question_id}",
                    "case_id": case_id,
                    "question_id": question_id,
                    "revealed_option_id": "A",
                    "frozen_top1": "A",
                    "frozen_top2": "B",
                    "top1_correct": True,
                    "top2_hit": True,
                    "prediction_freeze_hash": f"{case_index:02d}{question_index:02d}".ljust(64, "0"),
                    "evaluation_role": "FIRST_BLIND_PREDICTION",
                    "answer_visible_during_prediction": False,
                    "prediction_input_answer_free": True,
                    "frozen_before_reveal": True,
                    "case_specific_rule_detected": False,
                    "source_provenance_status": "PASS",
                    "pairwise_replay_status": "PASS",
                }
                observation_hash = sha256_bytes(canonical_bytes(observation))
                units.append({
                    "unit_id": unit_id,
                    "case_ids": [case_id],
                    "question_ids": [question_id],
                    "first_blind_observation_hash": observation_hash,
                })
                observations[unit_id] = (observation, observation_hash)

        cycle_path = training_root / "learning-cycle.json"
        cycle = create_cycle(
            f"CYCLE-{group_run_id}",
            group_id,
            units,
            cycle_path,
            bindings={"group_run_id": group_run_id, "new_first_blind_score_eligibility": "NONE"},
        )
        intake_path = training_root / "group-training-intake.json"
        intake = write_json(intake_path, {
            "schema": "GROUP-TRAINING-INTAKE-V1",
            "status": "LEARNING_ACTIVE",
            "group_id": group_id,
            "group_run_id": group_run_id,
            "cycle_path": str(cycle_path),
            "cycle_object_hash": cycle["object_hash"],
            "training_unit_count": len(units),
            "new_first_blind_score_eligibility": "NONE",
        }, hashed=True)

        evidence_rows = []
        evidence_paths = []
        for index, unit in enumerate(units):
            observation, observation_hash = observations[unit["unit_id"]]
            replay_rows = [
                {
                    "evaluation_role": "POST_REVEAL_TRAINING_REPLAY",
                    "attempt_id": f"{unit['unit_id']}-R{attempt}",
                    "answer_visible_during_prediction": False,
                    "prediction_input_answer_free": True,
                    "case_specific_rule_detected": False,
                    "source_provenance_status": "PASS",
                    "pairwise_replay_status": "PASS",
                    "matches_revealed_result": True,
                }
                for attempt in range(1, 6)
            ]
            evidence_path = training_root / "evidence" / f"{index + 1:03d}-{unit['unit_id']}.json"
            evidence = write_json(evidence_path, {
                "schema": "QUESTION-TRAINING-EVIDENCE-V2.1",
                "cycle_id": cycle["cycle_id"],
                "unit_id": unit["unit_id"],
                "evidence_id": f"EVIDENCE-{index + 1:03d}",
                "first_blind_prediction": observation,
                "first_blind_observation_hash": observation_hash,
                "correction": {
                    "error_diagnosis_complete": True,
                    "reasoning_update_complete": True,
                    "generic_method_candidate_recorded": True,
                    "counterexample_tests_complete": True,
                    "patch_validation_status": "PASS",
                    "case_specific_rule_detected": False,
                    "answer_memorization_rule_detected": False,
                    "reasoning_correction_object": reasoning(unit["unit_id"]),
                },
                "post_reveal_training_replays": replay_rows,
                "prior_method_retention": {
                    "prior_completed_unit_count": index,
                    "retention_rate": None if index == 0 else 1.0,
                },
            }, hashed=True)
            evidence_rows.append({
                "unit_id": unit["unit_id"],
                "evidence_path": str(evidence_path),
                "evidence_sha256": sha256_file(evidence_path),
                "evidence_object_hash": evidence["object_hash"],
            })
            evidence_paths.append(evidence_path)

        manifest_path = training_root / "evidence-manifest.json"
        write_json(manifest_path, {
            "schema": "GROUP-TRAINING-EVIDENCE-MANIFEST-V1",
            "status": "READY_FOR_SERIAL_EVALUATION",
            "group_id": group_id,
            "group_run_id": group_run_id,
            "training_unit_count": len(units),
            "units": evidence_rows,
        }, hashed=True)
        request_path = root / "runtime" / "training-finalize-requests" / f"{group_run_id}.json"
        write_json(request_path, {
            "schema": "GROUP-TRAINING-FINALIZE-REQUEST-V1",
            "status": "REQUESTED",
            "group_id": group_id,
            "group_run_id": group_run_id,
            "run_root": str(run_root),
            "training_intake_path": str(intake_path),
            "evidence_manifest_path": str(manifest_path),
            "output_root": str(training_root),
        }, hashed=True)
        self.assertEqual(intake["training_unit_count"], len(units))
        return request_path, manifest_path, evidence_paths

    def test_five_case_twenty_five_unit_training_finalizes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            request, _, _ = self.fixture(Path(tmp))
            result = finalize_group_training(request)
            self.assertEqual(result["status"], "TRAINING_FINALIZE_PASS")
            self.assertEqual(result["case_count"], 5)
            self.assertEqual(result["training_unit_count"], 25)
            self.assertEqual(result["completed_training_unit_count"], 25)
            self.assertTrue(all(row["status"] == "CASE_TRAINING_COMPLETE" for row in result["cases"]))
            final_cycle = json.loads(Path(result["final_cycle_path"]).read_text(encoding="utf-8"))
            self.assertEqual(final_cycle["current_unit_index"], 25)
            self.assertEqual(len(final_cycle["completed_training_units"]), 25)

    def test_missing_evidence_fails_closed_before_false_finalize(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            request, _, evidence = self.fixture(Path(tmp), case_count=1, questions_per_case=2)
            evidence[-1].unlink()
            with self.assertRaises(FortuneError) as caught:
                finalize_group_training(request)
            self.assertEqual(caught.exception.status, "TRAINING_EVIDENCE_MISSING")
            training_root = Path(tmp) / "data/group-clean-starts/GROUP-RUN-FINALIZE-1/training"
            self.assertFalse((training_root / "evaluations").exists())
            self.assertFalse((training_root / "cycle-states").exists())
            self.assertFalse((training_root / "training-finalize-receipt.json").exists())

    def test_tampered_evidence_hash_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            request, _, evidence = self.fixture(Path(tmp), case_count=1, questions_per_case=1)
            body = json.loads(evidence[0].read_text(encoding="utf-8"))
            body["unit_id"] = "TAMPERED"
            evidence[0].write_text(json.dumps(body), encoding="utf-8")
            with self.assertRaises(FortuneError) as caught:
                finalize_group_training(request)
            self.assertEqual(caught.exception.status, "TRAINING_EVIDENCE_HASH_INVALID")


if __name__ == "__main__":
    unittest.main()
