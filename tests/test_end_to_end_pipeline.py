from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fortune_v1.end_to_end import (
    freeze_group_predictions,
    release_group_postblind,
    reveal_and_start_training,
    validate_staged_clean_start,
)
from fortune_v1.util import FortuneError, sha256_file


class EndToEndPipelineTests(unittest.TestCase):
    def write_json(self, path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    def fixture(self, root: Path) -> tuple[Path, Path, Path]:
        run_root = root / "data/group-clean-starts/RUN-1"
        case_id = "CASE-1"
        run_id = "RUN-1-CASE-1"

        preblind_input = run_root / "preblind-inputs/CASE-1.json"
        self.write_json(preblind_input, {
            "schema": "PREBLIND-CASE-INPUT-V1",
            "case_id": case_id,
            "answer_data_available": False,
            "option_visibility": "WITHHELD",
            "question_stems": [{"question_id": "Q1", "stem": "synthetic question"}],
        })
        skeleton = run_root / "preblind-skeletons/CASE-1.json"
        self.write_json(skeleton, {
            "schema": "PREBLIND-PREDICTION-SKELETON-V1",
            "case_id": case_id,
            "run_id": run_id,
            "answer_data_available": False,
            "option_visibility": "WITHHELD",
            "questions": [{"question_id": "Q1"}],
        })
        options = run_root / "withheld-options/CASE-1.json"
        self.write_json(options, {
            "schema": "POSTBLIND-OPTION-PAYLOAD-V1",
            "case_id": case_id,
            "run_id": run_id,
            "questions": [{
                "question_id": "Q1",
                "options": [{"option_id": "A", "text": "a"}, {"option_id": "B", "text": "b"}],
            }],
        })
        postblind_template = run_root / "withheld-postblind-templates/CASE-1.json"
        self.write_json(postblind_template, {})
        postblind_source = run_root / "runtime-packets/CASE-1/withheld-postblind-source-packet.json"
        self.write_json(postblind_source, {})
        stage_plan = run_root / "runtime-packets/CASE-1/stage-access-plan.json"
        self.write_json(stage_plan, {
            "schema": "FORTUNE-STAGED-ACCESS-PLAN-V1",
            "status": "READY_FOR_PREBLIND_MODELING",
            "case_id": case_id,
            "run_id": run_id,
            "group_run_id": "RUN-1",
            "preblind_allowed_paths": [str(preblind_input), str(skeleton)],
            "postblind_withheld_paths": [str(options), str(postblind_template), str(postblind_source)],
        })
        clean_start = run_root / "clean-start.json"
        self.write_json(clean_start, {
            "schema": "GROUP-CLEAN-START-V1",
            "status": "READY_FOR_PREBLIND_MODELING",
            "group_id": "GROUP-1",
            "group_run_id": "RUN-1",
            "answer_data_available": False,
            "cases": [{
                "case_id": case_id,
                "case_run_id": run_id,
                "preblind_input_path": str(preblind_input),
                "preblind_input_sha256": sha256_file(preblind_input),
                "preblind_skeleton_path": str(skeleton),
                "preblind_skeleton_sha256": sha256_file(skeleton),
            }],
            "retrieval_policy": {"staged_access": {
                "current_stage": "PREBLIND",
                "withheld_paths_not_disclosed_to_prediction_context": True,
                "release_requires": "MACHINE_VALID_DUAL_TRACK_PREBLIND_SEALS_FOR_ALL_QUESTIONS",
            }},
        })
        seals = run_root / "preblind-seals/CASE-1.json"
        self.write_json(seals, {
            "schema": "PREBLIND-SEAL-BUNDLE-V1",
            "status": "PASS",
            "case_id": case_id,
            "run_id": run_id,
            "group_run_id": "RUN-1",
            "option_access_before_all_seals": False,
            "questions": [{
                "question_id": "Q1",
                "sealed_before_option_access": True,
                "ziwei": {"status": "PASS", "model_hash": "1" * 64, "seal_hash": "3" * 64},
                "bazi": {"status": "PASS", "model_hash": "2" * 64, "seal_hash": "4" * 64},
            }],
        })
        release_request = root / "runtime/preblind-seal-requests/RUN-1.json"
        self.write_json(release_request, {
            "schema": "GROUP-POSTBLIND-RELEASE-REQUEST-V1",
            "status": "REQUESTED",
            "group_run_id": "RUN-1",
            "clean_start_path": str(clean_start),
            "output_root": str(run_root),
            "case_seal_bundles": [{
                "case_id": case_id,
                "seal_bundle_path": str(seals),
                "stage_plan_path": str(stage_plan),
            }],
        })
        return run_root, clean_start, release_request

    def prediction_bundle(self, path: Path, *, pairwise: bool = True) -> Path:
        rows = [{
            "left": "A",
            "right": "B",
            "direction": "LEFT_AHEAD",
            "decisive_rule": "DISTINCTIVE_ATOM_DIRECT_SUPPORT",
            "reason": "synthetic decisive comparison",
            "left_vector": {},
            "right_vector": {},
        }] if pairwise else []
        self.write_json(path, {
            "schema": "POSTBLIND-PREDICTION-BUNDLE-V1",
            "status": "READY_FOR_FREEZE",
            "case_id": "CASE-1",
            "run_id": "RUN-1-CASE-1",
            "group_run_id": "RUN-1",
            "answer_visible_during_prediction": False,
            "prediction_input_answer_free": True,
            "questions": [{
                "question_id": "Q1",
                "top1": "A",
                "top2": "B",
                "confidence": "MEDIUM",
                "blind_core": "synthetic blind core",
                "source_provenance_status": "PASS",
                "pairwise_replay_status": "PASS",
                "coverage_plan_status": "PASS",
                "ziwei_track": {"status": "PASS"},
                "bazi_track": {"status": "PASS"},
                "fusion_status": "S03_PERFORMED",
                "evidence_usage_ledger": [{"packet_item_id": "SP-SYNTHETIC"}],
                "pairwise_rows": rows,
                "strongest_competitor": {"relative_first": "A", "relative_second": "B"},
                "formal_exact_assertion": None,
            }],
        })
        return path

    def test_clean_to_reveal_and_learning_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_root, clean_start, release_request = self.fixture(root)
            self.assertEqual(validate_staged_clean_start(clean_start)["status"], "PASS")
            access = release_group_postblind(release_request)
            self.assertEqual(access["status"], "POSTBLIND_OPTION_CHALLENGE_RELEASED")

            prediction = self.prediction_bundle(run_root / "postblind-predictions/CASE-1.json")
            freeze_request = root / "runtime/group-freeze-requests/RUN-1.json"
            self.write_json(freeze_request, {
                "schema": "GROUP-PREDICTION-FREEZE-REQUEST-V1",
                "status": "REQUESTED",
                "group_run_id": "RUN-1",
                "group_postblind_access_path": access["output_path"],
                "output_root": str(run_root),
                "case_prediction_bundles": [{"case_id": "CASE-1", "prediction_bundle_path": str(prediction)}],
            })
            freeze = freeze_group_predictions(freeze_request)
            self.assertEqual(freeze["status"], "GROUP_PREDICTION_FREEZE_PASS")

            answer_root = root / "answer-vault"
            answer = answer_root / "RUN-1.json"
            self.write_json(answer, {
                "schema": "GROUP-ANSWER-VECTOR-V1",
                "status": "REVEALED_FOR_TRAINING_AFTER_FREEZE",
                "raw_answer_string": "A",
                "delimiter": ",",
                "unicode_codepoints": [65],
                "character_offsets": [{"index": 0, "character": "A", "codepoint": 65}],
                "rows": [{"case_id": "CASE-1", "question_id": "Q1", "answer_option_id": "A"}],
            })
            reveal_request = root / "runtime/group-reveal-requests/RUN-1.json"
            self.write_json(reveal_request, {
                "schema": "GROUP-REVEAL-TRAINING-REQUEST-V1",
                "status": "REQUESTED",
                "group_run_id": "RUN-1",
                "group_prediction_freeze_path": freeze["output_path"],
                "answer_vector_path": "RUN-1.json",
                "output_root": str(run_root / "training"),
                "cycle_id": "CYCLE-1",
            })
            intake = reveal_and_start_training(reveal_request, answer_root=answer_root)
            self.assertEqual(intake["status"], "LEARNING_ACTIVE")
            self.assertEqual(intake["training_unit_count"], 1)

    def test_incomplete_pairwise_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_root, _, release_request = self.fixture(root)
            access = release_group_postblind(release_request)
            prediction = self.prediction_bundle(run_root / "postblind-predictions/CASE-1.json", pairwise=False)
            freeze_request = root / "runtime/group-freeze-requests/RUN-1.json"
            self.write_json(freeze_request, {
                "schema": "GROUP-PREDICTION-FREEZE-REQUEST-V1",
                "status": "REQUESTED",
                "group_run_id": "RUN-1",
                "group_postblind_access_path": access["output_path"],
                "output_root": str(run_root),
                "case_prediction_bundles": [{"case_id": "CASE-1", "prediction_bundle_path": str(prediction)}],
            })
            with self.assertRaises(FortuneError) as caught:
                freeze_group_predictions(freeze_request)
            self.assertEqual(caught.exception.status, "PAIRWISE_ROW_COUNT_INVALID")


if __name__ == "__main__":
    unittest.main()
