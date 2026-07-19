from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fortune_v1.bootstrap_request import build_preauthorized_request, create_group_clean_start_from_bootstrap_request
from fortune_v1.end_to_end import freeze_group_predictions, release_group_postblind, reveal_and_start_training
from fortune_v1.staged_access import harden_clean_start
from fortune_v1.training_finalize import finalize_group_training
from fortune_v1.util import canonical_bytes, sha256_bytes, sha256_file


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


def correction(unit_id: str) -> dict:
    return with_hash({
        "schema": "REASONING-CORRECTION-OBJECT-V2.1",
        "unit_id": unit_id,
        "error_mechanisms": [{"id": "E1", "mechanism": "synthetic scope correction"}],
        "source_parent_chains": [{
            "library_id": "S02",
            "active_file_sha256": "a" * 64,
            "excerpt_sha256": "b" * 64,
            "line_ranges": ["1-2"],
            "knowledge_point": "synthetic relative scope",
            "applicability_conditions": ["five-case integration fixture only"],
            "capability_ceiling": "RELATIVE_DIRECTION_ONLY",
            "downstream_effect": "closes the synthetic competitor",
        }],
        "corrected_reasoning_order": ["scope", "evidence", "endpoint", "pairwise"],
        "capability_ceiling_and_no_overreach": ["no formal exact assertion"],
        "applicability_conditions": ["five-case integration fixture only"],
        "counterexamples_and_failure_boundaries": ["not a real-case decision rule"],
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
            "reason": "synthetic deterministic comparison",
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


class V1RuntimeFullClosureTests(unittest.TestCase):
    def test_clean_request_through_five_case_training_finalize(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            group_run_id = "GROUP-RUN-FIVE-CASE-CLOSURE"
            group_id = "DEV-GROUP-002"
            cases = []
            for case_index in range(1, 6):
                case_id = f"DEV-EXAMPLE-{case_index:03d}"
                case_path = root / "training-data" / group_id / "cases" / f"{case_id}.json"
                questions = [{
                    "question_id": f"Q{question_index}",
                    "stem": f"synthetic question {question_index}",
                    "options": [
                        {"option_id": "A", "text": "synthetic A"},
                        {"option_id": "B", "text": "synthetic B"},
                    ],
                } for question_index in range(1, 6)]
                write_json(case_path, {
                    "case_id": case_id,
                    "dataset_type": "DEV_SYNTHETIC_INTEGRATION",
                    "binding": {"main_prompt_runtime_id": "R17"},
                    "answer_isolation": {"answer_payload_present": False},
                    "bazi": {"pillars": ["A", "B", "C", "D"]},
                    "ziwei": {"chart": "synthetic frozen chart"},
                    "questions": {"parsed": questions},
                })
                cases.append({"case_id": case_id, "path": str(case_path)})

            group_manifest = root / "training-data" / group_id / "group-manifest.json"
            write_json(group_manifest, {
                "group_id": group_id,
                "case_count": 5,
                "question_count_total": 25,
                "status": "READY_FOR_BASELINE_PREDICTION",
                "answer_payload_present": False,
                "runtime_answer_scan": "PASS",
                "cases": cases,
            })
            install_state = root / "reports/install-state.json"
            write_json(install_state, {"status": "INSTALLED_VALIDATED", "code_commit": "a" * 40})
            pointer = root / "CURRENT_GROUP_MANIFEST"
            write_json(pointer, {
                "schema": "CURRENT-GROUP-MANIFEST-POINTER-V1",
                "status": "ACTIVE",
                "group_id": group_id,
                "main_prompt_runtime_id": "MP-PROFESSIONAL-REASONING-20260718-R17",
                "active_knowledge_release_id": "KNOWLEDGE-R17",
                "active_method_release_id": "METHOD-R17",
                "active_model_release_id": "MODEL-R17-REPOSITORY-ACTIVE-V1",
                "active_learning_policy_id": "LEARNING-POLICY-EXAMPLE-CLEAN-BLIND-REPLAY-R1",
                "group_manifest_path": str(group_manifest),
                "install_state_path": str(install_state),
                "output_root": str(root / "data/group-clean-starts"),
                "allowed_repository": "chinaneedM/ziwei-bazi-model",
                "mandatory_initial_paths": [],
                "answer_payload_present": False,
                "runtime_answer_scan": "PASS",
                "answer_vault_location_outside_reasoning_context": True,
            })
            clean_request = root / "runtime/clean-start-requests/five-case.json"
            build_preauthorized_request(
                pointer,
                clean_request,
                group_run_id,
                "SESSION-FIVE-CASE",
                run_purpose="TRAINING_REPLAY",
            )
            clean = harden_clean_start(create_group_clean_start_from_bootstrap_request(clean_request, pointer))
            self.assertEqual(clean["status"], "READY_FOR_PREBLIND_MODELING")
            self.assertEqual(clean["start_request_receipt"]["new_first_blind_score_eligibility"], "NONE")
            run_root = Path(clean["clean_start_path"]).parent

            seal_requests = []
            for case_row in clean["cases"]:
                case_id = case_row["case_id"]
                stage_plan = run_root / "runtime-packets" / case_id / "stage-access-plan.json"
                write_json(stage_plan, {
                    "schema": "FORTUNE-STAGED-ACCESS-PLAN-V1",
                    "status": "READY_FOR_PREBLIND_MODELING",
                    "case_id": case_id,
                    "run_id": case_row["case_run_id"],
                    "group_run_id": group_run_id,
                    "preblind_allowed_paths": [case_row["preblind_input_path"], case_row["preblind_skeleton_path"]],
                    "postblind_withheld_paths": [
                        str(run_root / "withheld-options" / f"{case_id}.json"),
                        str(run_root / "withheld-postblind-templates" / f"{case_id}.json"),
                    ],
                })
                seal = run_root / "preblind-seals" / f"{case_id}.json"
                write_json(seal, {
                    "schema": "PREBLIND-SEAL-BUNDLE-V1",
                    "status": "PASS",
                    "case_id": case_id,
                    "run_id": case_row["case_run_id"],
                    "group_run_id": group_run_id,
                    "option_access_before_all_seals": False,
                    "questions": [{
                        "question_id": f"Q{question_index}",
                        "sealed_before_option_access": True,
                        "ziwei": {"status": "PASS", "model_hash": "1" * 64, "seal_hash": "3" * 64},
                        "bazi": {"status": "PASS", "model_hash": "2" * 64, "seal_hash": "4" * 64},
                    } for question_index in range(1, 6)],
                })
                seal_requests.append({"case_id": case_id, "seal_bundle_path": str(seal), "stage_plan_path": str(stage_plan)})

            release_request = root / "runtime/preblind-seal-requests/five-case.json"
            write_json(release_request, {
                "schema": "GROUP-POSTBLIND-RELEASE-REQUEST-V1",
                "status": "REQUESTED",
                "group_run_id": group_run_id,
                "clean_start_path": clean["clean_start_path"],
                "output_root": str(run_root),
                "case_seal_bundles": seal_requests,
            })
            released = release_group_postblind(release_request)
            self.assertEqual(released["case_count"], 5)

            predictions = []
            for case_row in clean["cases"]:
                case_id = case_row["case_id"]
                prediction = run_root / "postblind-predictions" / f"{case_id}.json"
                write_json(prediction, {
                    "schema": "POSTBLIND-PREDICTION-BUNDLE-V1",
                    "status": "READY_FOR_FREEZE",
                    "case_id": case_id,
                    "run_id": case_row["case_run_id"],
                    "group_run_id": group_run_id,
                    "answer_visible_during_prediction": False,
                    "prediction_input_answer_free": True,
                    "questions": [{
                        "question_id": f"Q{question_index}",
                        "top1": "A",
                        "top2": "B",
                        "confidence": "MEDIUM",
                        "blind_core": "synthetic answer-free blind core",
                        "source_provenance_status": "PASS",
                        "pairwise_replay_status": "PASS",
                        "coverage_plan_status": "PASS",
                        "ziwei_track": {"status": "PASS"},
                        "bazi_track": {"status": "PASS"},
                        "fusion_status": "S03_PERFORMED",
                        "evidence_usage_ledger": [{"packet_item_id": "SYNTHETIC"}],
                        "pairwise_rows": [{
                            "left": "A", "right": "B", "direction": "LEFT_AHEAD",
                            "decisive_rule": "DISTINCTIVE_ATOM_DIRECT_SUPPORT",
                            "reason": "synthetic deterministic comparison",
                            "left_vector": {}, "right_vector": {},
                        }],
                        "strongest_competitor": {"relative_first": "A", "relative_second": "B"},
                    } for question_index in range(1, 6)],
                })
                predictions.append({"case_id": case_id, "prediction_bundle_path": str(prediction)})

            freeze_request = root / "runtime/group-freeze-requests/five-case.json"
            write_json(freeze_request, {
                "schema": "GROUP-PREDICTION-FREEZE-REQUEST-V1",
                "status": "REQUESTED",
                "group_run_id": group_run_id,
                "group_postblind_access_path": released["output_path"],
                "output_root": str(run_root),
                "case_prediction_bundles": predictions,
            })
            freeze = freeze_group_predictions(freeze_request)
            self.assertEqual(freeze["case_count"], 5)
            self.assertEqual(freeze["question_count"], 25)

            answers = root / "transient-answers"
            answer_path = answers / "five-case.json"
            answer_rows = [
                {"case_id": f"DEV-EXAMPLE-{case_index:03d}", "question_id": f"Q{question_index}", "answer_option_id": "A"}
                for case_index in range(1, 6)
                for question_index in range(1, 6)
            ]
            write_json(answer_path, {
                "schema": "GROUP-ANSWER-VECTOR-V1",
                "status": "REVEALED_FOR_TRAINING_AFTER_FREEZE",
                "group_run_id": group_run_id,
                "raw_answer_string": ",".join("A" for _ in answer_rows),
                "delimiter": ",",
                "rows": answer_rows,
            })
            reveal_request = root / "runtime/group-reveal-requests/five-case.json"
            write_json(reveal_request, {
                "schema": "GROUP-REVEAL-TRAINING-REQUEST-V1",
                "status": "REQUESTED",
                "group_run_id": group_run_id,
                "group_prediction_freeze_path": freeze["output_path"],
                "answer_vector_path": answer_path.name,
                "output_root": str(run_root / "training"),
                "cycle_id": f"CYCLE-{group_run_id}",
                "new_first_blind_score_eligibility": "NONE",
            })
            intake = reveal_and_start_training(reveal_request, answer_root=answers)
            self.assertEqual(intake["training_unit_count"], 25)

            evidence_rows = []
            cycle = json.loads(Path(intake["cycle_path"]).read_text(encoding="utf-8"))
            for index, seed_row in enumerate(intake["training_evidence_seeds"], start=1):
                seed = json.loads(Path(seed_row["path"]).read_text(encoding="utf-8"))
                unit_id = seed["unit_id"]
                evidence_path = run_root / "training/evidence" / f"{index:03d}-{unit_id}.json"
                evidence = write_json(evidence_path, {
                    "schema": "QUESTION-TRAINING-EVIDENCE-V2.1",
                    "cycle_id": cycle["cycle_id"],
                    "unit_id": unit_id,
                    "evidence_id": f"EVIDENCE-{index:03d}",
                    "first_blind_prediction": seed["first_blind_prediction"],
                    "first_blind_observation_hash": seed["first_blind_observation_hash"],
                    "correction": {
                        "error_diagnosis_complete": True,
                        "reasoning_update_complete": True,
                        "generic_method_candidate_recorded": True,
                        "counterexample_tests_complete": True,
                        "patch_validation_status": "PASS",
                        "case_specific_rule_detected": False,
                        "answer_memorization_rule_detected": False,
                        "reasoning_correction_object": correction(unit_id),
                    },
                    "post_reveal_training_replays": [{
                        "evaluation_role": "POST_REVEAL_TRAINING_REPLAY",
                        "attempt_id": f"{unit_id}-R{attempt}",
                        "answer_visible_during_prediction": False,
                        "prediction_input_answer_free": True,
                        "case_specific_rule_detected": False,
                        "source_provenance_status": "PASS",
                        "pairwise_replay_status": "PASS",
                        "matches_revealed_result": True,
                    } for attempt in range(1, 6)],
                    "prior_method_retention": {
                        "prior_completed_unit_count": index - 1,
                        "retention_rate": None if index == 1 else 1.0,
                    },
                }, hashed=True)
                evidence_rows.append({
                    "unit_id": unit_id,
                    "evidence_path": str(evidence_path),
                    "evidence_sha256": sha256_file(evidence_path),
                    "evidence_object_hash": evidence["object_hash"],
                })

            manifest_path = run_root / "training/evidence-manifest.json"
            manifest = write_json(manifest_path, {
                "schema": "GROUP-TRAINING-EVIDENCE-MANIFEST-V1",
                "status": "READY_FOR_SERIAL_EVALUATION",
                "group_id": group_id,
                "group_run_id": group_run_id,
                "training_unit_count": 25,
                "units": evidence_rows,
            }, hashed=True)
            finalize_request = root / "runtime/training-finalize-requests/five-case.json"
            write_json(finalize_request, {
                "schema": "GROUP-TRAINING-FINALIZE-REQUEST-V1",
                "status": "REQUESTED",
                "group_id": group_id,
                "group_run_id": group_run_id,
                "run_root": str(run_root),
                "training_intake_path": intake["output_path"],
                "evidence_manifest_path": str(manifest_path),
                "output_root": str(run_root / "training"),
            }, hashed=True)
            self.assertEqual(manifest["training_unit_count"], 25)
            receipt = finalize_group_training(finalize_request)
            self.assertEqual(receipt["status"], "TRAINING_FINALIZE_PASS")
            self.assertEqual(receipt["case_count"], 5)
            self.assertEqual(receipt["completed_training_unit_count"], 25)
            self.assertEqual(receipt["new_first_blind_score_eligibility"], "NONE")
            self.assertTrue(all(row["status"] == "CASE_TRAINING_COMPLETE" for row in receipt["cases"]))


if __name__ == "__main__":
    unittest.main()
