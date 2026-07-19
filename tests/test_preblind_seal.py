from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fortune_v1.preblind_seal import prepare_group_seals
from fortune_v1.util import read_json


class PreblindSealTests(unittest.TestCase):
    def write_json(self, path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    def test_machine_builds_dual_track_seals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_root = root / "data/group-clean-starts/RUN"
            skeleton = run_root / "preblind-skeletons/C.json"
            self.write_json(skeleton, {"questions": [{"question_id": "Q1"}]})
            plan = run_root / "runtime-packets/C/stage-access-plan.json"
            self.write_json(plan, {
                "schema": "FORTUNE-STAGED-ACCESS-PLAN-V1",
                "status": "READY_FOR_PREBLIND_MODELING",
                "case_id": "C",
                "run_id": "RUN-C",
                "group_run_id": "RUN",
                "preblind_allowed_paths": [],
                "postblind_withheld_paths": [],
            })
            clean = run_root / "clean-start.json"
            self.write_json(clean, {
                "status": "READY_FOR_PREBLIND_MODELING",
                "answer_data_available": False,
                "group_run_id": "RUN",
                "cases": [{
                    "case_id": "C",
                    "case_run_id": "RUN-C",
                    "preblind_skeleton_path": str(skeleton),
                }],
            })
            model_paths = {}
            for track in ("ziwei", "bazi"):
                model_path = run_root / f"preblind-models/C/Q1-{track}.json"
                self.write_json(model_path, {
                    "schema": "PREBLIND-TRACK-MODEL-V1",
                    "status": "READY_FOR_SEAL",
                    "case_id": "C",
                    "run_id": "RUN-C",
                    "group_run_id": "RUN",
                    "question_id": "Q1",
                    "track": track,
                    "answer_data_available": False,
                    "option_visibility": "WITHHELD",
                    "option_accessed": False,
                    "blind_axis_model": {"track": track},
                    "complete_knowledge_coverage_plan": {"status": "PASS"},
                    "source_route_plan": [],
                })
                model_paths[track] = model_path
            request = root / "request.json"
            self.write_json(request, {
                "schema": "GROUP-PREBLIND-SEAL-AND-RELEASE-REQUEST-V1",
                "status": "REQUESTED",
                "group_run_id": "RUN",
                "clean_start_path": str(clean),
                "output_root": str(run_root),
                "case_model_submissions": [{
                    "case_id": "C",
                    "stage_plan_path": str(plan),
                    "questions": [{
                        "question_id": "Q1",
                        "ziwei_model_path": str(model_paths["ziwei"]),
                        "bazi_model_path": str(model_paths["bazi"]),
                    }],
                }],
            })
            derived = root / "derived.json"
            receipt = prepare_group_seals(request, derived)
            self.assertEqual(receipt["status"], "PASS")
            bundle = read_json(run_root / "preblind-seals/C.json")
            self.assertEqual(bundle["status"], "PASS")
            self.assertNotEqual(
                bundle["questions"][0]["ziwei"]["model_hash"],
                bundle["questions"][0]["bazi"]["model_hash"],
            )
            self.assertEqual(read_json(derived)["schema"], "GROUP-POSTBLIND-RELEASE-REQUEST-V1")


if __name__ == "__main__":
    unittest.main()
