from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fortune_v1.runtime_request import build_runtime_packet_request
from fortune_v1.util import FortuneError, sha256_file


class RuntimePacketRequestTests(unittest.TestCase):
    def write(self, path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    def fixture(self, root: Path) -> tuple[Path, dict[str, Path]]:
        preblind = root / "run/preblind.json"
        skeleton = root / "run/skeleton.json"
        self.write(preblind, {"schema": "PREBLIND-CASE-INPUT-V1"})
        self.write(skeleton, {
            "schema": "PREBLIND-PREDICTION-SKELETON-V1",
            "option_visibility": "WITHHELD",
            "answer_data_available": False,
            "questions": [{"question_id": "Q1"}],
        })
        clean = root / "run/clean-start.json"
        self.write(clean, {
            "status": "READY_FOR_PREBLIND_MODELING",
            "group_id": "GROUP-1",
            "group_run_id": "RUN-1",
            "answer_data_available": False,
            "active_runtime_binding": {
                "main_prompt_runtime_id": "R17",
                "knowledge_release_id": "K17",
                "method_release_id": "M17",
                "model_release_id": "MODEL17",
                "learning_policy_id": "L17",
            },
            "retrieval_policy": {"staged_access": {
                "current_stage": "PREBLIND",
                "withheld_paths_not_disclosed_to_prediction_context": True,
                "release_requires": "MACHINE_VALID_DUAL_TRACK_PREBLIND_SEALS_FOR_ALL_QUESTIONS",
            }},
            "cases": [{
                "case_id": "CASE-1",
                "preblind_input_path": str(preblind),
                "preblind_input_sha256": sha256_file(preblind),
                "preblind_skeleton_path": str(skeleton),
                "preblind_skeleton_sha256": sha256_file(skeleton),
            }],
        })
        specs = {
            "knowledge": ("FORTUNE-ACTIVE-KNOWLEDGE-RELEASE-POINTER-V1", "knowledge_release_id", "K17", "manifest_path", "manifest_object_hash"),
            "method": ("FORTUNE-ACTIVE-METHOD-RELEASE-POINTER-V1", "method_release_id", "M17", "method_release_path", "method_release_object_hash"),
            "model": ("FORTUNE-ACTIVE-MODEL-RELEASE-POINTER-V1", "model_release_id", "MODEL17", "model_release_path", "model_release_object_hash"),
        }
        pointers: dict[str, Path] = {}
        for name, (schema, id_field, release_id, path_field, hash_field) in specs.items():
            release = root / f"{name}/release.json"
            self.write(release, {id_field: release_id, "object_hash": f"{name[0]}" * 64})
            pointer = root / f"{name}/active.json"
            body = {
                "schema": schema,
                "formal_release": "YES",
                id_field: release_id,
                path_field: str(release),
                hash_field: f"{name[0]}" * 64,
            }
            if name == "method":
                body["main_prompt_runtime_id"] = "R17"
            self.write(pointer, body)
            pointers[name] = pointer
        return clean, pointers

    def test_request_is_derived_from_clean_start_and_active_releases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            clean, pointers = self.fixture(root)
            result = build_runtime_packet_request(
                clean,
                root / "run/control/runtime-request.json",
                knowledge_pointer_path=pointers["knowledge"],
                method_pointer_path=pointers["method"],
                model_pointer_path=pointers["model"],
            )
            self.assertEqual(result["schema"], "GROUP-RUNTIME-PACKET-REQUEST-V2")
            self.assertEqual(result["clean_start_sha256"], sha256_file(clean))
            self.assertFalse(result["answer_data_available"])
            self.assertEqual(result["bindings"]["model_release_id"], "MODEL17")

    def test_release_binding_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            clean, pointers = self.fixture(root)
            body = json.loads(clean.read_text(encoding="utf-8"))
            body["active_runtime_binding"]["method_release_id"] = "OTHER"
            self.write(clean, body)
            with self.assertRaises(FortuneError) as caught:
                build_runtime_packet_request(
                    clean,
                    root / "request.json",
                    knowledge_pointer_path=pointers["knowledge"],
                    method_pointer_path=pointers["method"],
                    model_pointer_path=pointers["model"],
                )
            self.assertEqual(caught.exception.status, "RUNTIME_BINDING_MISMATCH")


if __name__ == "__main__":
    unittest.main()
