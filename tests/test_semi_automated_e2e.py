from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from fortune_v1.prediction_freeze import freeze_case, freeze_group, validate_group
from fortune_v1.semi_automated import prepare_chat_packets, validate_chat_output
from fortune_v1.util import sha256_file


def _write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class SyntheticEndToEndTests(unittest.TestCase):
    def test_clean_start_to_group_freeze_without_answers(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            case_path = root / "synthetic-case.json"
            clean_start_path = root / "clean-start.json"

            case = {
                "case_id": "SYNTHETIC-CASE-001",
                "binding": {
                    "main_prompt_runtime_id": "MP-SYNTHETIC",
                    "source_baseline_id": "SOURCE-SYNTHETIC",
                },
                "answer_isolation": {"answer_payload_present": False},
                "input": {
                    "ziwei": {"summary": "synthetic ziwei input"},
                    "bazi": {"summary": "synthetic bazi input"},
                },
                "questions": {
                    "parsed": [
                        {
                            "question_id": "Q1",
                            "text": "Synthetic relative choice",
                            "options": [
                                {"option_id": "A", "text": "Option A"},
                                {"option_id": "B", "text": "Option B"},
                                {"option_id": "C", "text": "Option C"},
                            ],
                        }
                    ]
                },
            }
            _write(case_path, case)

            clean_start = {
                "schema": "GROUP-CLEAN-START-V1",
                "group_id": "SYNTHETIC-GROUP-001",
                "group_run_id": "SYNTHETIC-RUN-001",
                "status": "READY_FOR_CLEAN_GROUP_PREDICTION",
                "answer_data_available": False,
                "retrieval_policy": {
                    "mode": "EXACT_PATH_ONLY",
                    "repository_search_allowed": False,
                    "history_navigation_allowed": False,
                    "exact_allowed_paths": [str(case_path)],
                },
                "cases": [
                    {
                        "case_id": case["case_id"],
                        "input_path": str(case_path),
                        "input_sha256": sha256_file(case_path),
                    }
                ],
            }
            _write(clean_start_path, clean_start)

            packet_result = prepare_chat_packets(clean_start_path, root / "packets")
            self.assertEqual(packet_result["status"], "READY_FOR_CHAT_PROFESSIONAL_REASONING")
            self.assertEqual(packet_result["case_count"], 1)

            packet_path = Path(packet_result["packets"][0]["packet_path"])
            packet = _read(packet_path)
            self.assertFalse(packet["answer_data_available"])
            self.assertFalse(packet["execution_contract"]["repository_search_allowed"])
            self.assertFalse(packet["execution_contract"]["answer_access_allowed"])

            chat_output = copy.deepcopy(packet["professional_output_template"])
            question = chat_output["questions"][0]
            question.update(
                {
                    "option_order": ["B", "A", "C"],
                    "top1": "B",
                    "top2": "A",
                    "confidence": "LOW",
                    "blind_core": "Synthetic blind core independent of option labels.",
                    "public_evidence": [
                        "Ziwei native structure supports the relative direction.",
                        "Bazi native structure independently supports the direction.",
                        "The strongest competitor lacks the required endpoint.",
                    ],
                    "strongest_competitor_reason": "A lacks the required exact endpoint.",
                    "most_important_unverified_atom": "Synthetic exact endpoint remains unverified.",
                }
            )
            question["ziwei"].update(
                {
                    "blind_model": "Synthetic Ziwei blind model.",
                    "native_parent_ids": ["S06:SYNTHETIC"],
                }
            )
            question["bazi"].update(
                {
                    "blind_model": "Synthetic Bazi blind model.",
                    "native_parent_ids": ["S12:SYNTHETIC"],
                    "variant_status": "SINGLE_LEGAL_VARIANT",
                }
            )
            chat_output["status"] = "COMPLETE_CHAT_PROFESSIONAL_OUTPUT"

            chat_output_path = root / "chat-output.json"
            validated_output_path = root / "validated-output.json"
            validation_report_path = root / "validation-report.json"
            _write(chat_output_path, chat_output)
            validation_report = validate_chat_output(packet_path, chat_output_path, validated_output_path)
            _write(validation_report_path, validation_report)
            self.assertEqual(validation_report["status"], "PASS_READY_FOR_PREDICTION_FREEZE")

            case_freeze_path = root / "case-freeze.json"
            case_freeze = freeze_case(validated_output_path, case_freeze_path)
            self.assertEqual(case_freeze["status"], "PREDICTION_FROZEN")
            self.assertFalse(case_freeze["answer_data_available"])

            group_validation_path = root / "group-validation.json"
            group_validation = validate_group(
                packet_result["manifest_path"],
                [validation_report_path],
                [validated_output_path],
                group_validation_path,
            )
            self.assertEqual(group_validation["status"], "PASS_READY_FOR_GROUP_FREEZE")

            group_freeze = freeze_group(
                group_validation_path,
                [case_freeze_path],
                root / "group-freezes",
            )
            self.assertEqual(group_freeze["status"], "GROUP_PREDICTION_FROZEN")
            self.assertEqual(group_freeze["case_count"], 1)
            self.assertFalse(group_freeze["answer_data_available"])
            self.assertEqual(group_freeze["reveal_permission"], "MAY_BEGIN_ONLY_AFTER_THIS_FILE_EXISTS")


if __name__ == "__main__":
    unittest.main()
