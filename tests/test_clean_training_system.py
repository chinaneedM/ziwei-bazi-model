from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from cryptography.fernet import Fernet

from fortune_training.policy import passed, required_correct
from fortune_training.runtime import (
    apply_learning,
    encrypt_answer,
    freeze_prediction,
    score_round,
    start_round,
    status,
)
from fortune_training.util import TrainingError
from fortune_training.verify import build_source_manifest, verify_repository


POLICY = {
    "schema": "CASE-TRAINING-POLICY-V1",
    "training_unit": "CASE",
    "round_limit": None,
    "pass_rule": {
        "fewer_than_5_questions": "ALL_CORRECT",
        "5_or_more_questions": "CEILING_80_PERCENT",
    },
    "consecutive_passing_rounds_required": 3,
    "failed_round_resets_streak": True,
    "prediction_must_be_frozen_before_scoring": True,
    "failed_round_requires_learning_before_retry": True,
    "answer_plaintext_allowed_in_repository": False,
    "repeated_case_rounds_are_first_blind_evaluations": False,
}


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class RuntimeFixture:
    def __init__(self, base: Path, first_question_count: int = 5):
        self.base = base
        self.root = base / "repo"
        self.key = Fernet.generate_key()
        for index in range(20):
            source = self.root / "sources" / "active" / f"S{index:02d}_test.txt"
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text(f"general source {index}\n", encoding="utf-8")
        write_json(self.root / "config" / "training-policy.json", POLICY)
        build_source_manifest(self.root, write=True)
        write_json(
            self.root / "sources" / "releases" / "SOURCE-BASELINE-001.json",
            {
                "schema": "SOURCE-RELEASE-V1",
                "release_id": "SOURCE-BASELINE-001",
                "parent_release": None,
                "base_manifest": "sources/manifest.json",
                "patches": [],
                "training_process_authority": "config/training-policy.json",
            },
        )
        case_order = [f"DEV-EXAMPLE-{index:03d}" for index in range(1, 6)]
        case_paths = {
            case_id: f"examples/DEV-GROUP-002/cases/{case_id}.json" for case_id in case_order
        }
        for index, case_id in enumerate(case_order):
            count = first_question_count if index == 0 else 5
            questions = []
            for question_index in range(1, count + 1):
                questions.append(
                    {
                        "question_id": f"Q{question_index}",
                        "stem": f"question {question_index}",
                        "options": [
                            {"option_id": option, "text": option}
                            for option in ("A", "B", "C", "D")
                        ],
                    }
                )
            write_json(
                self.root / case_paths[case_id],
                {
                    "schema": "TRAINING-CASE-BUNDLE-V2",
                    "case_id": case_id,
                    "group_id": "DEV-GROUP-002",
                    "answer_isolation": {"answer_payload_present": False},
                    "questions": {"question_count": count, "parsed": questions},
                },
            )
        write_json(
            self.root / "examples" / "DEV-GROUP-002" / "group.json",
            {
                "schema": "TRAINING-GROUP-V1",
                "group_id": "DEV-GROUP-002",
                "case_order": case_order,
                "cases": case_paths,
            },
        )
        write_json(
            self.root / "training" / "state.json",
            {
                "schema": "CASE-TRAINING-STATE-V1",
                "group_id": "DEV-GROUP-002",
                "group_path": "examples/DEV-GROUP-002/group.json",
                "policy_path": "config/training-policy.json",
                "source_manifest_path": "sources/manifest.json",
                "current_source_release": "SOURCE-BASELINE-001",
                "current_case_index": 0,
                "status": "READY_FOR_ROUND",
                "active_round_id": None,
                "round_count": 0,
                "round_limit": None,
                "cases": {
                    case_id: {
                        "status": "ACTIVE" if index == 0 else "PENDING",
                        "consecutive_passes": 0,
                        "round_ids": [],
                    }
                    for index, case_id in enumerate(case_order)
                },
            },
        )
        (self.root / "answer-vault" / "encrypted").mkdir(parents=True, exist_ok=True)
        (self.root / "training" / "runs").mkdir(parents=True, exist_ok=True)
        (self.root / "sources" / "patches").mkdir(parents=True, exist_ok=True)
        self.case_id = case_order[0]
        self.question_count = first_question_count
        self.plaintext_answer = base / "trusted-answer.json"
        write_json(
            self.plaintext_answer,
            {
                "case_id": self.case_id,
                "answers": [
                    {"question_id": f"Q{index}", "correct_option": "A"}
                    for index in range(1, first_question_count + 1)
                ],
            },
        )
        encrypt_answer(self.root, self.case_id, self.plaintext_answer, self.key)

    def prediction_file(self, round_id: str, correct_count: int) -> Path:
        path = self.base / f"{round_id}.prediction.json"
        write_json(
            path,
            {
                "case_id": self.case_id,
                "round_id": round_id,
                "predictions": [
                    {
                        "question_id": f"Q{index}",
                        "top1": "A" if index <= correct_count else "B",
                        "top2": "C",
                        "reasoning": "general reasoning",
                    }
                    for index in range(1, self.question_count + 1)
                ],
            },
        )
        return path

    def run_and_score(self, round_id: str, correct_count: int):
        start_round(self.root, round_id)
        freeze_prediction(self.root, round_id, self.prediction_file(round_id, correct_count))
        return score_round(self.root, round_id, self.base / f"{round_id}.review.json", self.key)


class PolicyTests(unittest.TestCase):
    def test_exact_thresholds_and_no_fixed_round_count(self):
        self.assertEqual([required_correct(count) for count in range(1, 5)], [1, 2, 3, 4])
        self.assertEqual(required_correct(5), 4)
        self.assertEqual(required_correct(6), 5)
        self.assertTrue(passed(4, 5))
        self.assertFalse(passed(3, 5))


class RuntimeTests(unittest.TestCase):
    def test_failure_resets_streak_requires_learning_and_three_new_passes(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            self.assertTrue(fixture.run_and_score("R1", 4)["passed"])
            self.assertTrue(fixture.run_and_score("R2", 5)["passed"])
            failed = fixture.run_and_score("R3", 3)
            self.assertFalse(failed["passed"])
            self.assertEqual(status(fixture.root)["consecutive_passes"], 0)
            with self.assertRaises(TrainingError):
                start_round(fixture.root, "BLOCKED-BEFORE-LEARNING")

            patch = fixture.base / "general-patch.json"
            write_json(
                patch,
                {
                    "affected_libraries": ["S03", "S17"],
                    "principles": [
                        {
                            "statement": "Separate structural possibility from a proved event endpoint.",
                            "applicability": "When several real-world outcomes share the same broad structure.",
                            "limits": "A broad structure cannot prove an exact event by itself.",
                            "counterexamples": "A matching structure may manifest through another actor or domain.",
                            "capability_ceiling": "Use as a candidate generator until timing and endpoint evidence agree.",
                            "source_basis": "S03 conflict arbitration and S17 endpoint-chain principles.",
                        }
                    ],
                },
            )
            release = apply_learning(fixture.root, "R3", patch, "LEARNING-001")
            self.assertEqual(release["parent_release"], "SOURCE-BASELINE-001")
            first_retry = start_round(fixture.root, "R4")
            self.assertEqual(first_retry["source_release"], "LEARNING-001")
            freeze_prediction(fixture.root, "R4", fixture.prediction_file("R4", 4))
            score_round(fixture.root, "R4", fixture.base / "R4.review.json", fixture.key)
            fixture.run_and_score("R5", 4)
            fixture.run_and_score("R6", 5)
            current = status(fixture.root)
            self.assertEqual(current["current_case_id"], "DEV-EXAMPLE-002")
            self.assertEqual(current["status"], "READY_FOR_ROUND")
            self.assertEqual(current["round_count"], 6)
            score_text = (fixture.root / "training" / "runs" / "R6" / "score.json").read_text()
            self.assertNotIn("correct_option", score_text)

    def test_less_than_five_requires_all_correct(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary), first_question_count=3)
            score = fixture.run_and_score("SHORT-1", 2)
            self.assertFalse(score["passed"])
            self.assertEqual(score["required_correct"], 3)

    def test_scoring_before_freeze_and_second_freeze_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            start_round(fixture.root, "R1")
            with self.assertRaises(TrainingError):
                score_round(fixture.root, "R1", fixture.base / "early-review.json", fixture.key)
            prediction = fixture.prediction_file("R1", 5)
            freeze_prediction(fixture.root, "R1", prediction)
            with self.assertRaises(TrainingError):
                freeze_prediction(fixture.root, "R1", prediction)

    def test_plaintext_answers_inside_repository_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            inside = fixture.root / "unsafe.answers.json"
            inside.write_text(fixture.plaintext_answer.read_text(), encoding="utf-8")
            with self.assertRaises(TrainingError):
                encrypt_answer(fixture.root, fixture.case_id, inside, fixture.key)

    def test_external_answer_is_read_only_after_freeze(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            envelope = fixture.root / "answer-vault" / "encrypted" / f"{fixture.case_id}.json.fernet"
            envelope.unlink()
            start_round(fixture.root, "R1")
            freeze_prediction(fixture.root, "R1", fixture.prediction_file("R1", 5))
            score = score_round(
                fixture.root,
                "R1",
                fixture.base / "external.review.json",
                answer_file=fixture.plaintext_answer,
            )
            self.assertTrue(score["passed"])
            self.assertEqual(score["answer_source"], "EXTERNAL_POST_FREEZE_FILE")

    def test_external_answer_inside_repository_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            inside = fixture.root / "unsafe-answer-input.json"
            inside.write_text(fixture.plaintext_answer.read_text(), encoding="utf-8")
            start_round(fixture.root, "R1")
            freeze_prediction(fixture.root, "R1", fixture.prediction_file("R1", 5))
            with self.assertRaises(TrainingError):
                score_round(
                    fixture.root,
                    "R1",
                    fixture.base / "unsafe.review.json",
                    answer_file=inside,
                )

    def test_case_specific_learning_patch_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            fixture.run_and_score("R1", 0)
            patch = fixture.base / "leaking-patch.json"
            write_json(
                patch,
                {
                    "affected_libraries": ["S03"],
                    "principles": [
                        {
                            "statement": "DEV-EXAMPLE-001 Q1 should choose A.",
                            "applicability": "always",
                            "limits": "none",
                            "counterexamples": "none",
                            "capability_ceiling": "exact",
                            "source_basis": "memory",
                        }
                    ],
                },
            )
            with self.assertRaises(TrainingError):
                apply_learning(fixture.root, "R1", patch, "LEAKING")


class RepositoryIntegrityTests(unittest.TestCase):
    def test_real_repository_has_one_clean_source_and_case_baseline(self):
        root = Path(__file__).resolve().parents[1]
        result = verify_repository(root)
        self.assertEqual(result["sources"], 20)
        self.assertEqual(result["cases"], 5)
        self.assertEqual(result["questions"], 25)
        self.assertIsNone(result["round_limit"])

    def test_answer_source_readiness_is_explicit(self):
        root = Path(__file__).resolve().parents[1]
        result = verify_repository(root)
        self.assertEqual(result["answer_envelopes"], 0)
        self.assertFalse(result["preloaded_encrypted_answers_ready"])
        self.assertTrue(result["external_post_freeze_answer_supported"])
        self.assertTrue(result["controller_ready"])
        with self.assertRaises(TrainingError):
            verify_repository(root, require_answers=True)


if __name__ == "__main__":
    unittest.main()
