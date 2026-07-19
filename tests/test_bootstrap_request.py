from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fortune_v1.bootstrap_request import (
    PREAUTHORIZED_REQUEST_SCHEMA,
    build_preauthorized_request,
    create_group_clean_start_from_bootstrap_request,
)
from fortune_v1.util import FortuneError, canonical_bytes, sha256_bytes


class BootstrapRequestTests(unittest.TestCase):
    def write_json(self, path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    def fixture(self, root: Path) -> Path:
        case_path = root / "cases" / "CASE-1.json"
        self.write_json(case_path, {
            "case_id": "CASE-1",
            "dataset_type": "DEV",
            "binding": {"main_prompt_runtime_id": "R17", "source_baseline_tag": "S00-S19"},
            "answer_isolation": {"answer_payload_present": False},
            "bazi": {"pillars": ["A", "B", "C", "D"]},
            "ziwei": {"chart": "frozen"},
            "questions": {"parsed": [{
                "question_id": "Q1",
                "stem": "question without options",
                "options": [
                    {"option_id": "A", "text": "a"},
                    {"option_id": "B", "text": "b"},
                ],
            }]},
        })
        group_path = root / "training-data" / "GROUP-1" / "manifest.json"
        self.write_json(group_path, {
            "group_id": "GROUP-1",
            "case_count": 1,
            "question_count_total": 1,
            "status": "READY_FOR_BASELINE_PREDICTION",
            "answer_payload_present": False,
            "runtime_answer_scan": "PASS",
            "cases": [{"case_id": "CASE-1", "path": str(case_path)}],
        })
        install_path = root / "reports" / "install-state.json"
        self.write_json(install_path, {"status": "INSTALLED_VALIDATED", "code_commit": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"})
        control = root / "config" / "runtime.json"
        self.write_json(control, {"runtime": "R17"})
        pointer = root / "CURRENT_GROUP_MANIFEST"
        self.write_json(pointer, {
            "schema": "CURRENT-GROUP-MANIFEST-POINTER-V1",
            "status": "ACTIVE",
            "group_id": "GROUP-1",
            "main_prompt_runtime_id": "MP-PROFESSIONAL-REASONING-20260718-R17",
            "active_knowledge_release_id": "KNOWLEDGE-R17",
            "active_method_release_id": "METHOD-R17",
            "active_model_release_id": "MODEL-R17-REPOSITORY-ACTIVE-V1",
            "active_learning_policy_id": "LEARNING-POLICY-EXAMPLE-CLEAN-BLIND-REPLAY-R1",
            "group_manifest_path": str(group_path),
            "install_state_path": str(install_path),
            "output_root": str(root / "data" / "group-clean-starts"),
            "allowed_repository": "chinaneedM/ziwei-bazi-model",
            "forbidden_repository": "chinaneedM/fortune-answer-vault",
            "mandatory_initial_paths": [str(control)],
            "answer_payload_present": False,
            "runtime_answer_scan": "PASS",
            "answer_vault_location_outside_reasoning_context": True,
        })
        return pointer

    def test_preauthorized_request_removes_hidden_field_bootstrap_loop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pointer = self.fixture(root)
            request_path = root / "runtime" / "clean-start-requests" / "RUN-3.json"
            request = build_preauthorized_request(pointer, request_path, "RUN-3", "SESSION-3")
            self.assertEqual(request["schema"], PREAUTHORIZED_REQUEST_SCHEMA)
            self.assertFalse(request["prediction_context_started"])
            self.assertEqual(request["run_purpose"], "FIRST_BLIND")
            self.assertNotIn("forbidden_repository", request)
            self.assertEqual(request["future_prediction_first_repository_action"], "FETCH_EXACT_CLEAN_START_PATH_ONLY")
            self.assertEqual(
                request["future_prediction_entrypoint"],
                str(root / "data" / "group-clean-starts" / "RUN-3" / "clean-start.json"),
            )

    def test_preauthorized_request_creates_clean_start_without_prediction_search(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pointer = self.fixture(root)
            request_path = root / "runtime" / "clean-start-requests" / "RUN-4.json"
            build_preauthorized_request(pointer, request_path, "RUN-4", "SESSION-4")
            result = create_group_clean_start_from_bootstrap_request(request_path, pointer)
            self.assertEqual(result["group_run_id"], "RUN-4")
            self.assertEqual(result["group_id"], "GROUP-1")
            self.assertFalse(result["answer_data_available"])
            self.assertEqual(
                result["start_request_receipt"]["precontent_search_status"],
                "PASS_PREDICTION_CONTEXT_NOT_STARTED",
            )
            self.assertEqual(
                result["start_request_receipt"]["answer_vault_physical_access_test_status"],
                "PASS_INACCESSIBLE_BY_REPOSITORY_BOUNDARY",
            )

    def test_training_replay_uses_purpose_not_an_unrecognized_origin(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pointer = self.fixture(root)
            request_path = root / "runtime" / "clean-start-requests" / "RUN-REPLAY.json"
            request = build_preauthorized_request(
                pointer,
                request_path,
                "RUN-REPLAY",
                "SESSION-REPLAY",
                run_purpose="TRAINING_REPLAY",
            )
            self.assertEqual(request["request_origin"], "PREAUTHORIZED_ENGINEERING_BOOTSTRAP")
            self.assertEqual(request["run_purpose"], "TRAINING_REPLAY")
            self.assertEqual(request["new_first_blind_score_eligibility"], "NONE")
            result = create_group_clean_start_from_bootstrap_request(request_path, pointer)
            self.assertEqual(result["start_request_receipt"]["run_purpose"], "TRAINING_REPLAY")
            self.assertEqual(result["start_request_receipt"]["new_first_blind_score_eligibility"], "NONE")

    def test_exact_commit_runtime_preflight_is_bound_into_clean_start(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pointer = self.fixture(root)
            request_path = root / "runtime" / "clean-start-requests" / "RUN-PREFLIGHT.json"
            build_preauthorized_request(pointer, request_path, "RUN-PREFLIGHT", "SESSION-PREFLIGHT")
            receipt_path = root / "install-preflight.json"
            receipt = {
                "schema": "FINAL-OPEN-SOURCE-INSTALL-CHECK-RECEIPT-V3",
                "status": "INSTALL_CHECK_PASS_CANDIDATE",
                "code_commit": "a" * 40,
                "failure_count": 0,
                "formal_open_source_release_permission": "PASS",
            }
            receipt["object_hash"] = sha256_bytes(canonical_bytes(receipt))
            self.write_json(receipt_path, receipt)
            result = create_group_clean_start_from_bootstrap_request(
                request_path,
                pointer,
                receipt_path,
            )
            self.assertEqual(result["runtime_preflight_receipt"]["object_hash"], receipt["object_hash"])
            self.assertEqual(result["runtime_preflight_receipt"]["code_commit"], "a" * 40)

    def test_pointer_change_after_authorization_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pointer = self.fixture(root)
            request_path = root / "runtime" / "clean-start-requests" / "RUN-5.json"
            build_preauthorized_request(pointer, request_path, "RUN-5", "SESSION-5")
            pointer_body = json.loads(pointer.read_text(encoding="utf-8"))
            pointer_body["active_method_release_id"] = "METHOD-R18"
            self.write_json(pointer, pointer_body)
            with self.assertRaises(FortuneError) as caught:
                create_group_clean_start_from_bootstrap_request(request_path, pointer)
            self.assertEqual(caught.exception.status, "CLEAN_START_REQUEST_POINTER_MISMATCH")

    def test_answer_vault_boundary_is_verified_from_pointer_not_model_claim(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pointer = self.fixture(root)
            pointer_body = json.loads(pointer.read_text(encoding="utf-8"))
            pointer_body["answer_vault_location_outside_reasoning_context"] = False
            self.write_json(pointer, pointer_body)
            request_path = root / "runtime" / "clean-start-requests" / "RUN-6.json"
            with self.assertRaises(FortuneError) as caught:
                build_preauthorized_request(pointer, request_path, "RUN-6", "SESSION-6")
            self.assertEqual(caught.exception.status, "ANSWER_VAULT_ACCESS_TEST_FAILED")

    def test_prediction_context_visibility_flags_still_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pointer = self.fixture(root)
            request_path = root / "runtime" / "clean-start-requests" / "RUN-7.json"
            build_preauthorized_request(pointer, request_path, "RUN-7", "SESSION-7")
            request_body = json.loads(request_path.read_text(encoding="utf-8"))
            request_body["prediction_context_repository_search_used"] = True
            self.write_json(request_path, request_body)
            with self.assertRaises(FortuneError) as caught:
                create_group_clean_start_from_bootstrap_request(request_path, pointer)
            self.assertEqual(caught.exception.status, "FAIL_CLOSED_CONTAMINATED")


if __name__ == "__main__":
    unittest.main()
