from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fortune_v1.group import create_dev_group, record_patch_round
from fortune_v1.training import (
    advance_learning_cycle,
    create_learning_cycle,
    evaluate_learning_cycle,
    validate_learning_patch,
)


def write_json(path: Path, value: object) -> Path:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def clean_row(attempt: int, *, correct: bool, question_id: str = "Q1") -> dict:
    return {
        "attempt_id": f"A{attempt}",
        "case_id": "DEV-EXAMPLE-001",
        "question_id": question_id,
        "top1_correct": correct,
        "top2_hit": True,
        "clean_cold_start": True,
        "answer_visible_during_prediction": False,
        "prediction_input_answer_free": True,
        "case_specific_rule_detected": False,
        "source_provenance_status": "PASS",
        "pairwise_replay_status": "PASS",
    }


class LearningCycleV2Tests(unittest.TestCase):
    def test_question_unit_reaches_eighty_percent_mastery(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = [{"unit_id": "Q1-TRAIN", "case_ids": ["DEV-EXAMPLE-001"], "question_ids": ["Q1"]}]
            cycle_path = root / "cycle.json"
            create_learning_cycle("CYCLE-1", "DEV-GROUP-002", "QUESTION", plan, cycle_path)

            replay = {
                "schema": "CLEAN-COLD-START-REPLAY-V2",
                "replay_id": "REPLAY-1",
                "cycle_id": "CYCLE-1",
                "answer_payload_present": False,
                "old_prediction_payload_present": False,
                "old_error_explanation_present": False,
                "regression_damage_questions": 0,
                "rows": [clean_row(i, correct=i != 5) for i in range(1, 6)],
            }
            replay_path = write_json(root / "replay.json", replay)
            evaluation_path = root / "evaluation.json"
            evaluation = evaluate_learning_cycle(cycle_path, replay_path, evaluation_path)

            self.assertEqual(evaluation["status"], "PASS")
            self.assertTrue(evaluation["mastery_pass"])
            self.assertAlmostEqual(evaluation["current_unit"]["top1_rate"], 0.8)
            self.assertEqual(evaluation["claim_boundary"]["generalization"], "NOT_PROVEN")

            next_cycle = advance_learning_cycle(cycle_path, evaluation_path, root / "cycle-next.json")
            self.assertEqual(next_cycle["status"], "TRAINING_SET_MASTERED_AWAITING_UNSEEN_BLIND_TEST")

    def test_answer_visibility_causes_hold(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = [{"unit_id": "Q1", "case_ids": ["DEV-EXAMPLE-001"], "question_ids": ["Q1"]}]
            cycle_path = root / "cycle.json"
            create_learning_cycle("CYCLE-2", "DEV-GROUP-002", "QUESTION", plan, cycle_path)
            rows = [clean_row(i, correct=True) for i in range(1, 6)]
            rows[0]["answer_visible_during_prediction"] = True
            replay_path = write_json(
                root / "replay.json",
                {
                    "schema": "CLEAN-COLD-START-REPLAY-V2",
                    "replay_id": "REPLAY-2",
                    "cycle_id": "CYCLE-2",
                    "answer_payload_present": False,
                    "old_prediction_payload_present": False,
                    "old_error_explanation_present": False,
                    "rows": rows,
                },
            )
            evaluation = evaluate_learning_cycle(cycle_path, replay_path, root / "evaluation.json")
            self.assertEqual(evaluation["status"], "HOLD_ANSWER_OR_CASE_RULE_CONTAMINATION")

    def test_old_round_limits_do_not_stop_learning(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            group = create_dev_group(
                "DEV-GROUP-TEST",
                [f"CASE-{i}" for i in range(5)],
                {"source": "R16"},
                root,
            )
            group_root = root / "DEV-GROUP-TEST"
            for _ in range(7):
                group = record_patch_round(group_root, 0, 0, "SAME-DEFECT")
            self.assertEqual(group["status"], "METHOD_RETHINK_REQUIRED")
            self.assertTrue(group["training_continues"])
            self.assertEqual(group["hold_reasons"], [])

    def test_base_knowledge_patch_requires_independent_sources_and_units(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            invalid_patch = {
                "patch_id": "PATCH-1",
                "layer": "BASE_KNOWLEDGE",
                "generalization_scope": "ALL_CASES",
                "mechanism_change": "Refine conditional source direction",
                "counterexample_tests": ["opposite structure"],
                "source_confirmed_parents": ["PARENT-1"],
                "reproduced_unit_ids": ["UNIT-1"],
            }
            invalid_path = write_json(root / "invalid.json", invalid_patch)
            invalid = validate_learning_patch(invalid_path, root / "invalid-result.json")
            self.assertEqual(invalid["status"], "REJECTED")
            self.assertEqual(invalid["knowledge_review"], "RESEARCH_CANDIDATE_ONLY")

            valid_patch = dict(invalid_patch)
            valid_patch["patch_id"] = "PATCH-2"
            valid_patch["source_confirmed_parents"] = ["PARENT-1", "PARENT-2"]
            valid_patch["reproduced_unit_ids"] = ["UNIT-1", "UNIT-2"]
            valid_path = write_json(root / "valid.json", valid_patch)
            valid = validate_learning_patch(valid_path, root / "valid-result.json")
            self.assertEqual(valid["status"], "PASS")
            self.assertTrue(valid["promotable"])

    def test_case_specific_answer_rule_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            patch = {
                "patch_id": "PATCH-BAD",
                "layer": "METHOD",
                "generalization_scope": "ALL_CASES",
                "mechanism_change": "For case DEV-EXAMPLE-001 always choose B",
                "counterexample_tests": ["other case"],
            }
            patch_path = write_json(root / "bad.json", patch)
            result = validate_learning_patch(patch_path, root / "bad-result.json")
            self.assertEqual(result["status"], "REJECTED")
            self.assertIn("CASE_OPTION_DIRECTION_RULE", result["reasons"])


if __name__ == "__main__":
    unittest.main()
