from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fortune_v1.semi_automated import classify_visibility_event, validate_chat_output


def _write(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


class SemiAutomatedTests(unittest.TestCase):
    def test_empty_operation_attempt_is_not_contamination(self) -> None:
        result = classify_visibility_event(
            operation_attempted=True,
            returned_payload_visible=False,
            forbidden_content_visible=False,
            answer_bearing_content_visible=False,
        )
        self.assertEqual(result["status"], "OPERATION_ATTEMPT_RECORDED_NO_CONTAMINATION")
        self.assertFalse(result["restart_required"])

    def test_answer_visibility_is_fail_closed(self) -> None:
        result = classify_visibility_event(
            operation_attempted=True,
            returned_payload_visible=True,
            forbidden_content_visible=True,
            answer_bearing_content_visible=True,
        )
        self.assertEqual(result["status"], "FAIL_CLOSED_CONTAMINATED")
        self.assertTrue(result["restart_required"])

    def test_validator_materializes_pairwise_rows(self) -> None:
        packet = {
            "schema": "CHAT-PROFESSIONAL-PACKET-V1",
            "group_run_id": "g1",
            "case_id": "c1",
            "case_payload": {
                "questions": {
                    "parsed": [
                        {
                            "question_id": "Q1",
                            "options": [
                                {"option_id": "A", "text": "a"},
                                {"option_id": "B", "text": "b"},
                                {"option_id": "C", "text": "c"},
                            ],
                        }
                    ]
                }
            },
        }
        output = {
            "schema": "CHAT-PROFESSIONAL-OUTPUT-V1",
            "case_id": "c1",
            "questions": [
                {
                    "question_id": "Q1",
                    "option_order": ["B", "A", "C"],
                    "top1": "B",
                    "top2": "A",
                    "confidence": "LOW",
                    "blind_core": "core",
                    "public_evidence": ["e1", "e2", "e3"],
                    "strongest_competitor_reason": "A lacks endpoint",
                    "most_important_unverified_atom": "exact endpoint",
                    "ziwei": {"blind_model": "z", "native_parent_ids": ["S06:x"]},
                    "bazi": {"blind_model": "b", "native_parent_ids": ["S12:y"]},
                    "direction_matrix": {"A": [], "B": [], "C": []},
                    "compound_coverage": {"A": {}, "B": {}, "C": {}},
                }
            ],
        }
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            packet_path = root / "packet.json"
            output_path = root / "output.json"
            validated_path = root / "validated.json"
            _write(packet_path, packet)
            _write(output_path, output)
            report = validate_chat_output(packet_path, output_path, validated_path)
            self.assertEqual(report["status"], "PASS_READY_FOR_PREDICTION_FREEZE")
            validated = json.loads(validated_path.read_text(encoding="utf-8"))
            question = validated["questions"][0]
            self.assertEqual(question["pairwise_row_count_expected"], 3)
            self.assertEqual(question["pairwise_row_count_actual"], 3)
            self.assertEqual(question["pairwise_rows"][0]["winner"], "B")


if __name__ == "__main__":
    unittest.main()
