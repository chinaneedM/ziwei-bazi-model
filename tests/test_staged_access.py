from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fortune_v1.staged_access import (
    PREBLIND_STATUS,
    harden_clean_start,
    harden_runtime_packets,
    release_postblind_stage,
)


class StagedAccessTests(unittest.TestCase):
    def write_json(self, path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    def fixture(self, root: Path) -> tuple[dict, Path, Path]:
        case_path = root / "training-data/G/cases/CASE-1.json"
        case = {
            "case_id": "CASE-1",
            "dataset_type": "DEV",
            "binding": {"main_prompt_runtime_id": "R17"},
            "answer_isolation": {"answer_payload_present": False, "answer_reference_disclosed": False},
            "bazi": {"transcription": {"pillars": {"year": "甲子"}}},
            "ziwei": {"text": "命宫紫微"},
            "questions": {"parsed": [{
                "question_id": "Q1",
                "stem": "出生家境如何？",
                "options": [
                    {"option_id": "A", "text": "富裕"},
                    {"option_id": "B", "text": "贫穷"},
                ],
            }]},
        }
        self.write_json(case_path, case)
        manifest_path = root / "training-data/G/manifest.json"
        self.write_json(manifest_path, {
            "group_id": "G",
            "cases": [{"case_id": "CASE-1", "path": str(case_path)}],
        })
        output = root / "data/group-clean-starts/RUN-1"
        skeleton = output / "case-skeletons/CASE-1.json"
        self.write_json(skeleton, {
            "schema": "PREDICTION-RUN-V1",
            "case_id": "CASE-1",
            "run_id": "RUN-1-CASE-1",
            "questions": [{"question_id": "Q1", "option_ids": ["A", "B"], "pairwise_rows": [{"left": "A", "right": "B"}]}],
        })
        clean_path = output / "clean-start.json"
        self.write_json(clean_path, {
            "schema": "GROUP-CLEAN-START-V1",
            "group_id": "G",
            "group_run_id": "RUN-1",
            "group_session_id": "SESSION-1",
            "active_runtime_binding": {"main_prompt_runtime_id": "R17"},
            "group_manifest": {"path": str(manifest_path)},
            "cases": [{
                "case_id": "CASE-1",
                "case_run_id": "RUN-1-CASE-1",
                "input_path": str(case_path),
                "input_sha256": "x",
                "skeleton_path": str(skeleton),
                "skeleton_sha256": "y",
            }],
            "retrieval_policy": {"exact_allowed_paths": [str(manifest_path), str(case_path), str(skeleton)]},
            "contamination_policy": {},
            "answer_data_available": False,
            "status": "READY_FOR_CLEAN_GROUP_PREDICTION",
        })
        result = {"clean_start_path": str(clean_path)}
        return result, clean_path, case_path

    def test_clean_start_removes_preblind_option_visibility(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result, clean_path, case_path = self.fixture(Path(tmp))
            hardened = harden_clean_start(result)
            self.assertEqual(hardened["status"], PREBLIND_STATUS)
            allowed = hardened["retrieval_policy"]["exact_allowed_paths"]
            self.assertNotIn(str(case_path), allowed)
            row = hardened["cases"][0]
            preblind = json.loads(Path(row["preblind_input_path"]).read_text(encoding="utf-8"))
            serialized = json.dumps(preblind, ensure_ascii=False)
            self.assertNotIn("option_id", serialized)
            self.assertNotIn("富裕", serialized)
            skeleton = json.loads(Path(row["preblind_skeleton_path"]).read_text(encoding="utf-8"))
            self.assertNotIn("option_ids", json.dumps(skeleton))
            self.assertFalse((clean_path.parent / "case-skeletons/CASE-1.json").exists())

    def test_runtime_hardening_withholds_option_derived_packet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result, clean_path, _ = self.fixture(root)
            clean = harden_clean_start(result)
            output = clean_path.parent
            request_path = root / "runtime/request.json"
            self.write_json(request_path, {"output_root": str(output), "clean_start_path": str(clean_path)})
            case_root = output / "runtime-packets/CASE-1"
            sidecar = output / "case-input-sidecars/CASE-1"
            sidecar.mkdir(parents=True)
            (sidecar / "ziwei.txt").write_text("命宫紫微", encoding="utf-8")
            self.write_json(sidecar / "bazi.json", {"transcription": {"pillars": {"year": "甲子"}}})
            self.write_json(sidecar / "questions.json", {"parsed": [{"options": [{"text": "富裕"}]}]})
            self.write_json(case_root / "source-packet.json", {
                "case_id": "CASE-1", "run_id": "RUN-1-CASE-1", "group_run_id": "RUN-1",
                "knowledge_release_id": "K", "knowledge_manifest_path": "knowledge.json", "knowledge_manifest_object_hash": "h",
                "route_rows": [
                    {"library_id": "S04", "selected_item_count": 2, "route_status": "ITEMS_SELECTED"},
                ],
                "items": [
                    {"packet_item_id": "SAFE", "library_id": "S04", "matched_keywords": ["家境"], "target_question_ids": ["Q1"]},
                    {"packet_item_id": "LEAK", "library_id": "S04", "matched_keywords": ["富裕"], "target_question_ids": ["Q1"]},
                ],
            })
            self.write_json(case_root / "method-packet.json", {"status": "READY"})
            self.write_json(case_root / "run-contract.json", {"status": "READY_FOR_BLIND_PREDICTION", "input_snapshot": {}})
            transport = output / "retrieval-transport-plan.json"
            self.write_json(transport, {
                "status": "READY", "answer_data_available": False,
                "exact_allowed_paths": [str(sidecar / "questions.json"), str(case_root / "source-packet.json"), clean["cases"][0]["preblind_input_path"]],
            })
            legacy_result = {"transport_plan_path": str(transport)}
            hardened = harden_runtime_packets(legacy_result, request_path, clean_path)
            self.assertEqual(hardened["status"], PREBLIND_STATUS)
            packet = json.loads((case_root / "preblind-source-packet.json").read_text(encoding="utf-8"))
            self.assertEqual([row["packet_item_id"] for row in packet["items"]], ["SAFE"])
            plan = json.loads((case_root / "stage-access-plan.json").read_text(encoding="utf-8"))
            for path in plan["postblind_withheld_paths"]:
                self.assertNotIn(path, json.loads(transport.read_text(encoding="utf-8"))["exact_allowed_paths"])
            self.assertFalse((sidecar / "questions.json").exists())

    def test_postblind_release_requires_both_track_seals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan = root / "plan.json"
            self.write_json(plan, {
                "schema": "FORTUNE-STAGED-ACCESS-PLAN-V1",
                "status": PREBLIND_STATUS,
                "case_id": "CASE-1",
                "run_id": "RUN-1-CASE-1",
                "group_run_id": "RUN-1",
                "preblind_allowed_paths": ["safe.json"],
                "postblind_withheld_paths": ["options.json"],
            })
            seals = root / "seals.json"
            self.write_json(seals, {
                "schema": "PREBLIND-SEAL-BUNDLE-V1",
                "status": "PASS",
                "case_id": "CASE-1",
                "run_id": "RUN-1-CASE-1",
                "option_access_before_all_seals": False,
                "questions": [{
                    "question_id": "Q1",
                    "sealed_before_option_access": True,
                    "ziwei": {"status": "PASS", "model_hash": "z-model", "seal_hash": "z-seal"},
                    "bazi": {"status": "PASS", "model_hash": "b-model", "seal_hash": "b-seal"},
                }],
            })
            receipt = release_postblind_stage(plan, seals, root / "release.json")
            self.assertEqual(receipt["status"], "POSTBLIND_OPTION_CHALLENGE_RELEASED")
            self.assertIn("options.json", receipt["allowed_paths_after_release"])


if __name__ == "__main__":
    unittest.main()
