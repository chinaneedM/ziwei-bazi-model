from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from cryptography.fernet import Fernet

from fortune_training.chat_input import CHAT_INPUT_RELATIVE_PATH, write_chat_input
from fortune_training.policy import passed, required_correct
from fortune_training.runtime import (
    apply_learning,
    encrypt_answer,
    freeze_prediction,
    score_round,
    start_round,
    status,
)
from fortune_training.cli import build_parser
from fortune_training.issue_relay import PACKET_END, PACKET_START, extract_packet, process_packet
from fortune_training.util import TrainingError, object_sha256
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
    "failed_round_updates_model_layer_only": True,
    "canonical_sources_mutable_during_training": False,
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
            source = self.root / "sources" / "canonical" / f"S{index:02d}_test.txt"
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text(f"general source {index}\n", encoding="utf-8")
        write_json(self.root / "config" / "training-policy.json", POLICY)
        source_manifest = build_source_manifest(self.root)
        write_json(
            self.root / "config" / "source-policy.json",
            {
                "schema": "SOURCE-AUTHORITY-POLICY-V1",
                "original_project_library_role": "ARCHIVAL_READ_ONLY_NOT_RUNTIME",
                "original_project_library_deletion_required": False,
                "runtime_source": "GIT_REPOSITORY_ONLY",
                "git_canonical_path": "sources/canonical",
                "git_canonical_mutable_during_training": False,
                "canonical_manifest_sha256": object_sha256(source_manifest),
                "model_learning_path": "model-learning",
                "model_learning_mutable_during_training": True,
                "conflict_resolution": "IGNORE_EXTERNAL_ORIGINAL_AND_USE_GIT_RUNTIME",
            },
        )
        write_json(
            self.root / "config" / "answer-policy.json",
            {
                "schema": "PUBLIC-REPOSITORY-ANSWER-POLICY-V1",
                "repository_visibility": "PUBLIC",
                "private_answer_repository_required": False,
                "plaintext_answers_allowed": False,
                "encrypted_answer_envelopes_allowed": True,
                "decryption_keys_allowed": False,
                "answer_read_phase": "POST_FREEZE_ONLY",
            },
        )
        write_json(self.root / "sources" / "canonical-manifest.json", source_manifest)
        write_json(
            self.root / "model-learning" / "releases" / "MODEL-BASELINE-001.json",
            {
                "schema": "MODEL-RELEASE-V1",
                "release_id": "MODEL-BASELINE-001",
                "parent_release": None,
                "base_source_manifest": "sources/canonical-manifest.json",
                "patches": [],
                "training_process_authority": "config/training-policy.json",
                "canonical_sources_mutated": False,
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
                    "binding": {
                        "source_manifest": "sources/canonical-manifest.json",
                        "training_policy": "config/training-policy.json",
                    },
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
                "source_manifest_path": "sources/canonical-manifest.json",
                "current_model_release": "MODEL-BASELINE-001",
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
        (self.root / "model-learning" / "patches").mkdir(parents=True, exist_ok=True)
        write_chat_input(self.root)
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
        for case_id in case_order[1:]:
            answer_file = base / f"{case_id}.trusted-answer.json"
            write_json(
                answer_file,
                {
                    "case_id": case_id,
                    "answers": [
                        {"question_id": f"Q{index}", "correct_option": "A"}
                        for index in range(1, 6)
                    ],
                },
            )
            encrypt_answer(self.root, case_id, answer_file, self.key)

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
    def test_chat_input_contains_only_current_safe_prediction_material(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            fixture.run_and_score("R1", 4)
            bundle = json.loads((fixture.root / CHAT_INPUT_RELATIVE_PATH).read_text())
            serialized = json.dumps(bundle, ensure_ascii=False)
            self.assertEqual(bundle["schema"], "CHAT-PREDICTION-INPUT-V1")
            self.assertEqual(bundle["state_summary"]["current_case_id"], fixture.case_id)
            self.assertTrue(bundle["state_summary"]["prediction_allowed"])
            self.assertFalse(bundle["contains_old_predictions"])
            self.assertNotIn("general reasoning", serialized)
            self.assertNotIn('"top1"', serialized)
            self.assertNotIn("prediction-freeze.json", serialized)

    def test_chat_input_tampering_fails_repository_verification(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            path = fixture.root / CHAT_INPUT_RELATIVE_PATH
            bundle = json.loads(path.read_text())
            bundle["contains_old_predictions"] = True
            write_json(path, bundle)
            with self.assertRaises(TrainingError):
                verify_repository(fixture.root)

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
            canonical_before = build_source_manifest(fixture.root)
            write_json(
                patch,
                {
                    "learning_type": "REASONING_STRATEGY",
                    "related_source_libraries": ["S03", "S17"],
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
            self.assertEqual(release["parent_release"], "MODEL-BASELINE-001")
            self.assertEqual(build_source_manifest(fixture.root), canonical_before)
            self.assertTrue(
                (fixture.root / "model-learning" / "patches" / "LEARNING-001.json").is_file()
            )
            first_retry = start_round(fixture.root, "R4")
            self.assertEqual(first_retry["model_release"], "LEARNING-001")
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
                    "learning_type": "REASONING_STRATEGY",
                    "related_source_libraries": ["S03"],
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


class IssueRelayTests(unittest.TestCase):
    def _packet(self, fixture: RuntimeFixture, round_id: str, correct_count: int) -> dict:
        prediction = json.loads(fixture.prediction_file(round_id, correct_count).read_text())
        packet = {
            "schema": "TRAINING-ISSUE-PACKET-V1",
            "round_id": round_id,
            "case_id": fixture.case_id,
            "predictions": prediction["predictions"],
            "expected_result": "PASS"
            if correct_count >= required_correct(fixture.question_count)
            else "FAIL",
        }
        if packet["expected_result"] == "FAIL":
            packet["learning_release_id"] = f"LEARNING-{round_id}"
            packet["learning_patch"] = {
                "learning_type": "REASONING_STRATEGY",
                "related_source_libraries": ["S03", "S17"],
                "principles": [
                    {
                        "statement": "Separate a possible structure from a proved real-world endpoint.",
                        "applicability": "When several outcomes share the same broad symbolic structure.",
                        "limits": "The broad structure cannot establish an exact event without timing evidence.",
                        "counterexamples": "The same structure may manifest through another person or domain.",
                        "capability_ceiling": "Use only to generate candidates before endpoint adjudication.",
                        "source_basis": "S03 conflict arbitration and S17 endpoint-chain principles.",
                    }
                ],
            }
        return packet

    def test_extract_and_process_passing_issue(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            packet = self._packet(fixture, "ISSUE-PASS-1", 4)
            body = (
                f"header\n{PACKET_START}\n```json\n"
                f"{json.dumps(packet)}\n```\n{PACKET_END}\n"
            )
            result = process_packet(fixture.root, extract_packet(body), fixture.key)
            self.assertTrue(result["passed"])
            self.assertEqual(result["consecutive_passes"], 1)
            self.assertFalse(result["answers_published"])

    def test_extract_accepts_raw_json_issue_body(self):
        packet = {
            "schema": "TRAINING-ISSUE-PACKET-V1",
            "round_id": "RAW-JSON-1",
        }
        self.assertEqual(extract_packet(json.dumps(packet)), packet)

    def test_extract_accepts_single_json_code_block(self):
        packet = {
            "schema": "TRAINING-ISSUE-PACKET-V1",
            "round_id": "FENCED-JSON-1",
        }
        body = f"```json\n{json.dumps(packet)}\n```"
        self.assertEqual(extract_packet(body), packet)

    def test_extract_rejects_partial_legacy_marker(self):
        with self.assertRaises(TrainingError):
            extract_packet(f"{PACKET_START}\n{{}}")

    def test_failed_issue_requires_and_applies_general_learning(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            packet = self._packet(fixture, "ISSUE-FAIL-1", 3)
            result = process_packet(fixture.root, packet, fixture.key)
            self.assertFalse(result["passed"])
            self.assertEqual(result["learning_release"], "LEARNING-ISSUE-FAIL-1")
            self.assertEqual(status(fixture.root)["status"], "READY_FOR_ROUND")

    def test_issue_expected_result_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            packet = self._packet(fixture, "ISSUE-MISMATCH-1", 4)
            packet["expected_result"] = "FAIL"
            packet["learning_release_id"] = "LEARNING-ISSUE-MISMATCH-1"
            packet["learning_patch"] = self._packet(fixture, "TEMP", 0)["learning_patch"]
            with self.assertRaises(TrainingError):
                process_packet(fixture.root, packet, fixture.key)


class RepositoryIntegrityTests(unittest.TestCase):
    def test_real_repository_has_one_clean_source_and_case_baseline(self):
        root = Path(__file__).resolve().parents[1]
        result = verify_repository(root)
        self.assertEqual(result["sources"], 20)
        self.assertEqual(result["cases"], 5)
        self.assertEqual(result["questions"], 25)
        self.assertIsNone(result["round_limit"])
        self.assertEqual(result["runtime_source"], "GIT_REPOSITORY_ONLY")
        self.assertTrue(result["canonical_sources_immutable"])
        self.assertTrue(result["model_learning_separate"])

    def test_canonical_sources_cannot_be_silently_rebaselined(self):
        parser = build_parser()
        subparsers = next(action for action in parser._actions if action.dest == "command")
        verify_parser = subparsers.choices["verify"]
        option_strings = {option for action in verify_parser._actions for option in action.option_strings}
        self.assertNotIn("--write-manifest", option_strings)

    def test_canonical_source_mutation_fails_verification(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            source = fixture.root / "sources" / "canonical" / "S03_test.txt"
            source.write_text("tampered\n", encoding="utf-8")
            with self.assertRaises(TrainingError):
                verify_repository(fixture.root)

    def test_answer_source_readiness_is_explicit(self):
        root = Path(__file__).resolve().parents[1]
        result = verify_repository(root)
        self.assertGreaterEqual(result["answer_envelopes"], 0)
        self.assertLessEqual(result["answer_envelopes"], result["answer_envelopes_required"])
        self.assertEqual(
            result["preloaded_encrypted_answers_ready"],
            result["answer_envelopes"] == result["answer_envelopes_required"],
        )
        self.assertTrue(result["external_post_freeze_answer_supported"])
        self.assertTrue(result["controller_ready"])
        if result["preloaded_encrypted_answers_ready"]:
            self.assertEqual(verify_repository(root, require_answers=True)["status"], "PASS")
        else:
            with self.assertRaises(TrainingError):
                verify_repository(root, require_answers=True)


if __name__ == "__main__":
    unittest.main()
