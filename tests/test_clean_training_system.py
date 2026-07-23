from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from cryptography.fernet import Fernet

from fortune_training.chat_input import CHAT_INPUT_RELATIVE_PATH, write_chat_input
from fortune_training.cli import build_parser
from fortune_training.formal import (
    FORMAL_ANSWER_DIR,
    FORMAL_GROUP_PATH,
    PRE_FORMAL_LEDGER_ARCHIVE,
    PRE_FORMAL_STATE_ARCHIVE,
    import_answer_batch,
)
from fortune_training.issue_relay import PACKET_END, PACKET_START, extract_packet, process_packet
from fortune_training.learning import (
    LEDGER_RELATIVE_PATH,
    empty_learning_ledger,
    load_learning_ledger,
    safe_active_rules,
    validate_learning_ledger,
    write_learning_ledger,
)
from fortune_training.policy import passed, required_correct
from fortune_training.runtime import (
    _validate_answers,
    apply_learning,
    encrypt_answer,
    freeze_prediction,
    score_round,
    start_round,
    status,
)
from fortune_training.transport import (
    PUBLIC_KEY_PATH,
    SEALED_BATCH_PATH,
    bootstrap_answer_transport,
    finalize_answer_transport,
    seal_answer_batch,
)
from fortune_training.util import TrainingError, object_sha256
from fortune_training.verify import build_source_manifest, verify_repository


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TAXONOMY = json.loads((PROJECT_ROOT / "config" / "question-taxonomy.json").read_text())
POLICY = json.loads((PROJECT_ROOT / "config" / "training-policy.json").read_text())


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def general_rule(rule_id: str) -> dict:
    return {
        "rule_id": rule_id,
        "topic_tags": ["OTHER"],
        "reasoning_skill_tags": ["EVIDENCE_WEIGHTING"],
        "source_routes": ["S03", "S17"],
        "statement": "Separate structural possibility from a proved event endpoint.",
        "applicability": "When several real-world outcomes share the same broad structure.",
        "limits": "A broad structure cannot prove an exact event by itself.",
        "counterexamples": "A complete actor, action, timing, and endpoint chain may justify precision.",
        "capability_ceiling": "Use as a candidate until independent timing and endpoint evidence agree.",
        "source_basis": "S03 conflict arbitration and S17 endpoint-chain principles.",
        "trigger_conditions": "Several options share the same non-specific symbolic background.",
        "decision_procedure": "Build a separate actor, mechanism, timing, and endpoint chain for each option.",
        "stop_conditions": "Stop at a broad possibility when an exclusive endpoint node is missing.",
    }


class RuntimeFixture:
    def __init__(self, base: Path, first_question_count: int = 5, case_count: int = 5):
        self.base = base
        self.root = base / "repo"
        self.key = Fernet.generate_key()
        for index in range(20):
            source = self.root / "sources" / "canonical" / f"S{index:02d}_test.txt"
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text(f"general source {index}\n", encoding="utf-8")
        write_json(self.root / "config" / "training-policy.json", POLICY)
        write_json(self.root / "config" / "question-taxonomy.json", TAXONOMY)
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
        case_order = [f"DEV-EXAMPLE-{index:03d}" for index in range(1, case_count + 1)]
        case_paths = {
            case_id: f"examples/DEV-GROUP-002/cases/{case_id}.json" for case_id in case_order
        }
        for index, case_id in enumerate(case_order):
            count = first_question_count if index == 0 else 5
            questions = [
                {
                    "question_id": f"Q{question_index}",
                    "stem": f"question {question_index}",
                    "options": [
                        {"option_id": option, "text": option}
                        for option in ("A", "B", "C", "D")
                    ],
                }
                for question_index in range(1, count + 1)
            ]
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
                "schema": "GENERALIZATION-TRAINING-STATE-R2",
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
                "first_blind_cases_closed": 0,
                "independent_pass_streak": 0,
                "required_consecutive_independent_passes": 3,
                "active_replay_case_id": None,
                "spaced_replay_queue": [],
                "cases": {
                    case_id: {
                        "status": "ACTIVE" if index == 0 else "PENDING",
                        "first_blind_passed": None,
                        "remediation_status": "NOT_EVALUATED",
                        "first_blind_round_id": None,
                        "replay_round_ids": [],
                        "round_ids": [],
                    }
                    for index, case_id in enumerate(case_order)
                },
            },
        )
        write_learning_ledger(self.root, empty_learning_ledger(self.root))
        (self.root / "answer-vault" / "encrypted").mkdir(parents=True, exist_ok=True)
        (self.root / "training" / "runs").mkdir(parents=True, exist_ok=True)
        (self.root / "model-learning" / "patches").mkdir(parents=True, exist_ok=True)
        write_chat_input(self.root)
        for index, case_id in enumerate(case_order):
            count = first_question_count if index == 0 else 5
            answer_file = base / f"{case_id}.trusted-answer.json"
            write_json(
                answer_file,
                {
                    "case_id": case_id,
                    "answers": [
                        {"question_id": f"Q{question_index}", "correct_option": "A"}
                        for question_index in range(1, count + 1)
                    ],
                },
            )
            encrypt_answer(self.root, case_id, answer_file, self.key)
        self.plaintext_answer = base / f"{case_order[0]}.trusted-answer.json"

    def current_case(self) -> tuple[str, int]:
        current = status(self.root)["current_case_id"]
        group = json.loads((self.root / "examples/DEV-GROUP-002/group.json").read_text())
        case = json.loads((self.root / group["cases"][current]).read_text())
        return current, case["questions"]["question_count"]

    def profile(self, applied_rule_ids: list[str] | None = None) -> dict:
        return {
            "topic_tags": ["OTHER"],
            "subject_tags": ["SELF"],
            "time_scope_tags": ["NATAL"],
            "endpoint_tags": ["OTHER"],
            "reasoning_skill_tags": ["EVIDENCE_WEIGHTING"],
            "source_routes": ["S03", "S17"],
            "applied_rule_ids": applied_rule_ids or [],
        }

    def prediction_file(
        self,
        round_id: str,
        correct_count: int,
        *,
        applied_rule_ids: list[str] | None = None,
        include_profile: bool = True,
    ) -> Path:
        case_id, question_count = self.current_case()
        path = self.base / f"{round_id}.prediction.json"
        rows = []
        for index in range(1, question_count + 1):
            row = {
                "question_id": f"Q{index}",
                "top1": "A" if index <= correct_count else "B",
                "top2": "C",
                "reasoning": "general reasoning",
                "evidence": ["S03", "S17"],
                "strongest_counterevidence": "A competing endpoint may fit the same background.",
                "confidence": 70,
            }
            if include_profile:
                row["question_profile"] = self.profile(applied_rule_ids)
            rows.append(row)
        write_json(
            path,
            {"case_id": case_id, "round_id": round_id, "predictions": rows},
        )
        return path

    def run_and_score(
        self,
        round_id: str,
        correct_count: int,
        *,
        applied_rule_ids: list[str] | None = None,
    ) -> dict:
        start_round(self.root, round_id)
        freeze_prediction(
            self.root,
            round_id,
            self.prediction_file(round_id, correct_count, applied_rule_ids=applied_rule_ids),
        )
        return score_round(self.root, round_id, self.base / f"{round_id}.review.json", self.key)

    def patch_file(self, release_id: str, rule_id: str) -> Path:
        path = self.base / f"{release_id}.patch.json"
        write_json(path, {"learning_type": "REASONING_STRATEGY", "rules": [general_rule(rule_id)]})
        return path


class PolicyTests(unittest.TestCase):
    def test_exact_round_quality_thresholds(self):
        self.assertEqual([required_correct(count) for count in range(1, 5)], [1, 2, 3, 4])
        self.assertEqual(required_correct(5), 4)
        self.assertEqual(required_correct(6), 5)
        self.assertTrue(passed(4, 5))
        self.assertFalse(passed(3, 5))


class RuntimeTests(unittest.TestCase):
    def test_first_blind_advances_and_streak_uses_distinct_cases(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            score = fixture.run_and_score("R1", 4)
            self.assertTrue(score["passed"])
            self.assertEqual(score["evaluation_kind"], "FIRST_BLIND")
            self.assertFalse(score["spaced_replay_required"])
            current = status(fixture.root)
            self.assertEqual(current["current_case_id"], "DEV-EXAMPLE-002")
            self.assertEqual(current["independent_pass_streak"], 1)
            self.assertEqual(current["status"], "READY_FOR_ROUND")
            fixture.run_and_score("R2", 5)
            current = status(fixture.root)
            self.assertEqual(current["current_case_id"], "DEV-EXAMPLE-003")
            self.assertEqual(current["independent_pass_streak"], 2)
            third_score = fixture.run_and_score("R3", 5)
            self.assertTrue(third_score["independent_stage_gate_met"])
            current = status(fixture.root)
            self.assertEqual(current["current_case_id"], "DEV-EXAMPLE-004")
            self.assertEqual(current["independent_pass_streak"], 3)
            state = json.loads((fixture.root / "training/state.json").read_text())
            self.assertEqual(state["cases"]["DEV-EXAMPLE-001"]["first_blind_round_id"], "R1")
            self.assertEqual(state["cases"]["DEV-EXAMPLE-001"]["replay_round_ids"], [])

    def test_failure_resets_cross_case_streak_and_advances_after_learning(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            fixture.run_and_score("PASS-1", 5)
            score = fixture.run_and_score("R1", 3)
            self.assertFalse(score["passed"])
            self.assertEqual(score["independent_pass_streak_before"], 1)
            self.assertEqual(score["independent_pass_streak_after"], 0)
            self.assertEqual(status(fixture.root)["status"], "LEARNING_REQUIRED")
            with self.assertRaises(TrainingError):
                start_round(fixture.root, "BLOCKED")
            release = apply_learning(
                fixture.root,
                "R1",
                fixture.patch_file("LEARNING-001", "RULE-GENERAL-ENDPOINT"),
                "LEARNING-001",
            )
            self.assertEqual(release["parent_release"], "MODEL-BASELINE-001")
            self.assertEqual(status(fixture.root)["current_case_id"], "DEV-EXAMPLE-003")
            self.assertEqual(status(fixture.root)["spaced_replay_queue_size"], 1)
            ledger = load_learning_ledger(fixture.root)
            self.assertEqual(ledger["rule_evidence"]["RULE-GENERAL-ENDPOINT"]["status"], "CANDIDATE")

    def test_failed_case_replays_only_after_five_new_cases_and_does_not_count_as_new_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary), case_count=7)
            fixture.run_and_score("FAIL-1", 3)
            apply_learning(
                fixture.root,
                "FAIL-1",
                fixture.patch_file("LEARNING-001", "RULE-GENERAL-ENDPOINT"),
                "LEARNING-001",
            )
            for index in range(2, 7):
                fixture.run_and_score(f"NEW-{index}", 5)
            current = status(fixture.root)
            self.assertEqual(current["current_case_id"], "DEV-EXAMPLE-001")
            self.assertEqual(current["active_replay_case_id"], "DEV-EXAMPLE-001")
            bundle = json.loads((fixture.root / CHAT_INPUT_RELATIVE_PATH).read_text())
            self.assertEqual(bundle["state_summary"]["current_case_id"], "DEV-EXAMPLE-001")
            self.assertEqual(bundle["state_summary"]["evaluation_kind"], "SPACED_REPLAY")
            streak_before = current["independent_pass_streak"]
            replay = fixture.run_and_score("REPLAY-1", 5)
            self.assertEqual(replay["evaluation_kind"], "SPACED_REPLAY")
            current = status(fixture.root)
            self.assertEqual(current["current_case_id"], "DEV-EXAMPLE-007")
            self.assertEqual(current["independent_pass_streak"], streak_before)
            self.assertEqual(current["spaced_replay_queue_size"], 0)
            ledger = load_learning_ledger(fixture.root)
            self.assertEqual(ledger["first_blind_totals"]["cases"], 6)

    def test_question_profile_is_required_and_taxonomy_checked(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            start_round(fixture.root, "R1")
            with self.assertRaises(TrainingError):
                freeze_prediction(
                    fixture.root,
                    "R1",
                    fixture.prediction_file("R1", 5, include_profile=False),
                )

    def test_future_cases_not_replays_validate_candidate_rules(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            fixture.run_and_score("R1", 3)
            apply_learning(
                fixture.root,
                "R1",
                fixture.patch_file("LEARNING-001", "RULE-GENERAL-ENDPOINT"),
                "LEARNING-001",
            )
            fixture.run_and_score("R2", 5, applied_rule_ids=["RULE-GENERAL-ENDPOINT"])
            fixture.run_and_score("R3", 5, applied_rule_ids=["RULE-GENERAL-ENDPOINT"])
            evidence = load_learning_ledger(fixture.root)["rule_evidence"]["RULE-GENERAL-ENDPOINT"]
            self.assertEqual(evidence["status"], "PROVISIONAL")
            fixture.run_and_score("R4", 5, applied_rule_ids=["RULE-GENERAL-ENDPOINT"])
            evidence = load_learning_ledger(fixture.root)["rule_evidence"]["RULE-GENERAL-ENDPOINT"]
            self.assertEqual(evidence["status"], "VALIDATED")
            self.assertEqual(evidence["supporting_applications"], 15)
            self.assertEqual(len(evidence["distinct_support_cases"]), 3)

    def test_unrelated_question_does_not_validate_rule(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            fixture.run_and_score("R1", 3)
            apply_learning(
                fixture.root,
                "R1",
                fixture.patch_file("LEARNING-001", "RULE-GENERAL-ENDPOINT"),
                "LEARNING-001",
            )
            fixture.run_and_score("R2", 5)
            evidence = load_learning_ledger(fixture.root)["rule_evidence"]["RULE-GENERAL-ENDPOINT"]
            self.assertEqual(evidence["applications"], 0)
            self.assertEqual(evidence["status"], "CANDIDATE")

    def test_metrics_are_question_level_by_topic_and_skill(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            fixture.run_and_score("R1", 4)
            ledger = load_learning_ledger(fixture.root)
            self.assertEqual(ledger["first_blind_totals"]["cases"], 1)
            self.assertEqual(ledger["first_blind_totals"]["questions"], 5)
            self.assertEqual(ledger["topic_metrics"]["OTHER"]["top1_correct"], 4)
            self.assertEqual(ledger["reasoning_skill_metrics"]["EVIDENCE_WEIGHTING"]["questions"], 5)

    def test_group_completes_after_one_first_blind_per_case(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            for index in range(1, 6):
                fixture.run_and_score(f"R{index}", 5)
            current = status(fixture.root)
            self.assertEqual(current["status"], "GROUP_COMPLETE")
            self.assertIsNone(current["current_case_id"])
            bundle = json.loads((fixture.root / CHAT_INPUT_RELATIVE_PATH).read_text())
            self.assertFalse(bundle["state_summary"]["prediction_allowed"])
            self.assertIsNone(bundle["state_summary"]["recommended_round_id"])

    def test_chat_input_is_safe_and_points_to_next_unseen_case(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            fixture.run_and_score("R1", 4)
            bundle = json.loads((fixture.root / CHAT_INPUT_RELATIVE_PATH).read_text())
            serialized = json.dumps(bundle, ensure_ascii=False)
            self.assertEqual(bundle["schema"], "CHAT-PREDICTION-INPUT-V2")
            self.assertEqual(bundle["state_summary"]["current_case_id"], "DEV-EXAMPLE-002")
            self.assertEqual(
                bundle["state_summary"]["training_unit"],
                "FIRST_BLIND_CASE_WITH_SPACED_REPLAY",
            )
            self.assertEqual(bundle["state_summary"]["independent_pass_streak"], 1)
            self.assertEqual(bundle["state_summary"]["required_consecutive_independent_passes"], 3)
            self.assertEqual(bundle["current_model"]["knowledge_cards"]["card_count"], 0)
            self.assertEqual(
                bundle["current_model"]["knowledge_cards"]["authority"],
                "DERIVED_ROUTING_AND_PROCEDURE_ONLY",
            )
            self.assertNotIn("general reasoning", serialized)
            self.assertNotIn('"top1_correct"', serialized)
            self.assertNotIn('"correct_option"', serialized)

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

    def test_external_answer_is_read_only_after_freeze(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            case_id, _ = fixture.current_case()
            (fixture.root / "answer-vault" / "encrypted" / f"{case_id}.json.fernet").unlink()
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

    def test_unscored_question_is_excluded_from_threshold_and_learning_metrics(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            case_id, _ = fixture.current_case()
            answer_file = fixture.base / "answer-with-unscored.json"
            write_json(
                answer_file,
                {
                    "case_id": case_id,
                    "answers": [
                        *[
                            {"question_id": f"Q{index}", "correct_option": "A"}
                            for index in range(1, 5)
                        ],
                        {
                            "question_id": "Q5",
                            "scoring_status": "UNSCORED",
                            "reason_code": "NO_VALID_OPTION",
                        },
                    ],
                },
            )
            start_round(fixture.root, "R1")
            freeze_prediction(
                fixture.root,
                "R1",
                fixture.prediction_file("R1", 4),
            )
            review_path = fixture.base / "unscored.review.json"
            score = score_round(
                fixture.root,
                "R1",
                review_path,
                answer_file=answer_file,
            )
            self.assertTrue(score["passed"])
            self.assertEqual(score["question_count"], 5)
            self.assertEqual(score["scoreable_question_count"], 4)
            self.assertEqual(score["unscored_question_count"], 1)
            self.assertEqual(score["required_correct"], 4)
            detailed = json.loads(review_path.read_text(encoding="utf-8"))
            self.assertFalse(detailed["questions"][-1]["is_scored"])
            self.assertNotIn("correct_option", detailed["questions"][-1])
            ledger = load_learning_ledger(fixture.root)
            self.assertEqual(ledger["first_blind_totals"]["cases"], 1)
            self.assertEqual(ledger["first_blind_totals"]["questions"], 4)

    def test_case_specific_learning_rule_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            fixture.run_and_score("R1", 0)
            rule = general_rule("RULE-LEAKING")
            rule["statement"] = "DEV-EXAMPLE-001 Q1 should choose A."
            patch = fixture.base / "leaking-patch.json"
            write_json(patch, {"learning_type": "REASONING_STRATEGY", "rules": [rule]})
            with self.assertRaises(TrainingError):
                apply_learning(fixture.root, "R1", patch, "LEAKING")


class IssueRelayTests(unittest.TestCase):
    def packet(self, fixture: RuntimeFixture, round_id: str, correct_count: int) -> dict:
        case_id, question_count = fixture.current_case()
        prediction = json.loads(fixture.prediction_file(round_id, correct_count).read_text())
        failed = correct_count < required_correct(question_count)
        packet = {
            "schema": "TRAINING-ISSUE-PACKET-V2",
            "round_id": round_id,
            "case_id": case_id,
            "predictions": prediction["predictions"],
            "expected_result": "FAIL" if failed else "PASS",
        }
        if failed:
            packet["learning_release_id"] = f"LEARNING-{round_id}"
            packet["learning_patch"] = {
                "learning_type": "REASONING_STRATEGY",
                "rules": [general_rule(f"RULE-{round_id}")],
            }
        return packet

    def test_extract_and_process_passing_issue(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            packet = self.packet(fixture, "ISSUE-PASS-1", 4)
            body = f"header\n{PACKET_START}\n```json\n{json.dumps(packet)}\n```\n{PACKET_END}\n"
            result = process_packet(fixture.root, extract_packet(body), fixture.key)
            self.assertTrue(result["passed"])
            self.assertEqual(result["evaluation_kind"], "FIRST_BLIND")
            self.assertEqual(result["next_case_id"], "DEV-EXAMPLE-002")
            self.assertEqual(result["independent_pass_streak"], 1)
            self.assertFalse(result["answers_published"])

    def test_extract_accepts_raw_json_and_single_code_block(self):
        packet = {"schema": "TRAINING-ISSUE-PACKET-V2", "round_id": "RAW-1"}
        self.assertEqual(extract_packet(json.dumps(packet)), packet)
        self.assertEqual(extract_packet(f"```json\n{json.dumps(packet)}\n```"), packet)

    def test_failed_issue_creates_candidate_rules_and_queues_replay(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            packet = self.packet(fixture, "ISSUE-FAIL-1", 3)
            result = process_packet(fixture.root, packet, fixture.key)
            self.assertFalse(result["passed"])
            self.assertEqual(result["learning_release"], "LEARNING-ISSUE-FAIL-1")
            self.assertEqual(result["learning_rules_created"], ["RULE-ISSUE-FAIL-1"])
            self.assertEqual(result["next_case_id"], "DEV-EXAMPLE-002")
            self.assertEqual(result["independent_pass_streak"], 0)
            self.assertEqual(result["spaced_replay_queue_size"], 1)

    def test_expected_result_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            packet = self.packet(fixture, "ISSUE-MISMATCH-1", 4)
            packet["expected_result"] = "FAIL"
            packet["learning_release_id"] = "LEARNING-MISMATCH"
            packet["learning_patch"] = {
                "learning_type": "REASONING_STRATEGY",
                "rules": [general_rule("RULE-MISMATCH")],
            }
            with self.assertRaises(TrainingError):
                process_packet(fixture.root, packet, fixture.key)


class RepositoryIntegrityTests(unittest.TestCase):
    def test_retired_rule_is_valid_but_not_exposed_to_prediction(self):
        ledger = load_learning_ledger(PROJECT_ROOT)
        retired_rule = "RULE-HEALTH-SEVERITY-ENDPOINT-COMPARISON"
        self.assertEqual(ledger["rule_evidence"][retired_rule]["status"], "RETIRED")
        state = json.loads(
            (PROJECT_ROOT / "training/state.json").read_text(encoding="utf-8")
        )
        release = json.loads(
            (
                PROJECT_ROOT
                / "model-learning/releases"
                / f"{state['current_model_release']}.json"
            ).read_text(encoding="utf-8")
        )
        validate_learning_ledger(PROJECT_ROOT, ledger, release)
        self.assertNotIn(
            retired_rule,
            {rule["rule_id"] for rule in safe_active_rules(PROJECT_ROOT, release)},
        )

    def test_training_relay_commits_learning_ledger(self):
        workflow = (
            PROJECT_ROOT / ".github/workflows/training-issue-relay.yml"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "git add training/state.json training/learning-ledger.json",
            workflow,
        )

    def test_real_repository_has_generalization_r2_training_baseline(self):
        result = verify_repository(PROJECT_ROOT)
        self.assertEqual(result["sources"], 20)
        self.assertEqual(result["cases"], 107)
        self.assertEqual(result["questions"], 511)
        self.assertEqual(result["case_bank"]["blocked_cases"], [])
        self.assertFalse(result["case_bank"]["answer_payload_present"])
        self.assertEqual(result["legacy_controller_group"]["cases"], 5)
        self.assertEqual(result["training_unit"], "FIRST_BLIND_CASE_WITH_SPACED_REPLAY")
        self.assertFalse(result["same_case_replays_count_toward_stage_gate"])
        self.assertEqual(result["required_consecutive_independent_passes"], 3)
        self.assertTrue(result["question_taxonomy_ready"])
        self.assertTrue(result["learning_ledger_ready"])
        bundle = json.loads((PROJECT_ROOT / CHAT_INPUT_RELATIVE_PATH).read_text())
        self.assertEqual(bundle["current_model"]["knowledge_cards"]["card_count"], 23)

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

    def test_learning_ledger_tampering_fails_verification(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            ledger = load_learning_ledger(fixture.root)
            ledger["first_blind_totals"]["questions"] = -1
            write_json(fixture.root / LEDGER_RELATIVE_PATH, ledger)
            with self.assertRaises(TrainingError):
                verify_repository(fixture.root)

    def test_answer_source_readiness_is_explicit(self):
        result = verify_repository(PROJECT_ROOT)
        self.assertEqual(
            result["preloaded_encrypted_answers_ready"],
            result["answer_envelopes"] == result["answer_envelopes_required"],
        )
        self.assertTrue(result["external_post_freeze_answer_supported"])


class FormalActivationTests(unittest.TestCase):
    def test_five_option_cases_are_not_merged_and_unscored_rows_are_strict(self):
        five_option_questions = []
        for case_path in sorted((PROJECT_ROOT / "case-bank/cases").glob("CASE-*.json")):
            case = json.loads(case_path.read_text(encoding="utf-8"))
            for question in case["questions"]["parsed"]:
                option_ids = [row["option_id"] for row in question["options"]]
                self.assertIn(option_ids, [list("ABCD"), list("ABCDE")])
                if option_ids == list("ABCDE"):
                    five_option_questions.append(
                        (case["case_id"], question["question_id"])
                    )
        self.assertEqual(len(five_option_questions), 29)
        case = json.loads(
            (PROJECT_ROOT / "case-bank/cases/CASE-077.json").read_text(
                encoding="utf-8"
            )
        )
        payload = {
            "case_id": "CASE-077",
            "answers": [
                (
                    {
                        "question_id": question["question_id"],
                        "scoring_status": "UNSCORED",
                        "reason_code": "NO_VALID_OPTION",
                    }
                    if question["question_id"] == "Q3"
                    else {
                        "question_id": question["question_id"],
                        "correct_option": "A",
                    }
                )
                for question in case["questions"]["parsed"]
            ],
        }
        normalized = _validate_answers(case, payload)
        self.assertEqual(normalized["Q3"]["scoring_status"], "UNSCORED")
        self.assertEqual(
            sum(row["scoring_status"] == "SCORED" for row in normalized.values()),
            4,
        )

    def test_atomic_107_answer_import_activation_and_no_reveal_rehearsal(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "repo"
            shutil.copytree(
                PROJECT_ROOT,
                root,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
            )
            formal_vault = root / FORMAL_ANSWER_DIR
            if formal_vault.exists():
                shutil.rmtree(formal_vault)
            transport_dir = root / "answer-vault/import-transport"
            if transport_dir.exists():
                shutil.rmtree(transport_dir)
            archived_state = root / PRE_FORMAL_STATE_ARCHIVE
            if archived_state.is_file():
                archived_ledger = root / PRE_FORMAL_LEDGER_ARCHIVE
                if not archived_ledger.is_file():
                    self.fail("formal test fixture is missing the pre-formal ledger archive")
                shutil.copyfile(archived_state, root / "training/state.json")
                shutil.copyfile(
                    archived_ledger,
                    root / LEDGER_RELATIVE_PATH,
                )
                (root / FORMAL_GROUP_PATH).unlink(missing_ok=True)
                archived_state.unlink()
                archived_ledger.unlink()
                write_chat_input(root)

            manifest = json.loads((root / "case-bank/manifest.json").read_text())
            case_ids = [
                case_id
                for partition_id in ("DEVELOPMENT", "STAGE_VALIDATION", "FINAL_HOLDOUT")
                for case_id in manifest["partitions"][partition_id]
            ]
            rows = []
            for case_id in case_ids:
                case = json.loads(
                    (root / "case-bank/cases" / f"{case_id}.json").read_text()
                )
                rows.append(
                    {
                        "case_id": case_id,
                        "answers": [
                            (
                                {
                                    "question_id": question["question_id"],
                                    "scoring_status": "UNSCORED",
                                    "reason_code": "NO_VALID_OPTION",
                                }
                                if case_id == "CASE-077"
                                and question["question_id"] == "Q3"
                                else {
                                    "question_id": question["question_id"],
                                    "correct_option": "A",
                                }
                            )
                            for question in case["questions"]["parsed"]
                        ],
                    }
                )
            batch = {
                "schema": "FORTUNE-ANSWER-BATCH-V2",
                "corpus_id": manifest["corpus_id"],
                "cases": rows,
            }
            batch_path = base / "trusted-answers.json"
            write_json(batch_path, {**batch, "cases": rows[:-1]})
            key = Fernet.generate_key()
            with self.assertRaises(TrainingError):
                import_answer_batch(root, batch_path, key)
            self.assertFalse(formal_vault.exists())

            write_json(batch_path, batch)
            transport = bootstrap_answer_transport(root, key)
            self.assertTrue(transport["private_key_encrypted"])
            sealed_output = base / "answer-batch.sealed.json"
            seal_answer_batch(
                root,
                root / PUBLIC_KEY_PATH,
                batch_path,
                sealed_output,
            )
            shutil.copyfile(sealed_output, root / SEALED_BATCH_PATH)
            finalized = finalize_answer_transport(root, key)
            self.assertEqual(finalized["answer_envelopes"], 107)
            self.assertEqual(finalized["scoreable_questions"], 510)
            self.assertEqual(finalized["unscored_questions"], 1)
            self.assertEqual(finalized["current_case_id"], "CASE-002")
            self.assertEqual(finalized["recommended_round_id"], "FORMAL-ROUND-001")
            self.assertEqual(finalized["no_reveal_rehearsal"], "NO_REVEAL_REHEARSAL_PASS")
            self.assertTrue(finalized["transport_material_removed"])
            result = verify_repository(root, require_answers=True)
            self.assertEqual(result["answer_envelopes"], 107)
            self.assertEqual(result["active_controller_group"]["cases"], 63)
            self.assertEqual(result["active_controller_group"]["mode"], "FORMAL_CASE_BANK")


if __name__ == "__main__":
    unittest.main()
