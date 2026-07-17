from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fortune_v1.prediction_freeze import (
    create_repair_receipt,
    freeze_case,
    freeze_group,
    validate_group,
)
from fortune_v1.util import FortuneError


def _write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def _validated(case_id: str, group_run_id: str = "g1") -> dict:
    return {
        "schema": "VALIDATED-CHAT-PROFESSIONAL-OUTPUT-V1",
        "case_id": case_id,
        "group_run_id": group_run_id,
        "answer_data_available": False,
        "status": "PASS_READY_FOR_PREDICTION_FREEZE",
        "questions": [
            {
                "question_id": "Q1",
                "option_order": ["B", "A", "C"],
                "top1": "B",
                "top2": "A",
                "pairwise_row_count_expected": 3,
                "pairwise_row_count_actual": 3,
                "pairwise_rows": [],
            }
        ],
    }


class PredictionFreezeTests(unittest.TestCase):
    def test_repairable_failure_does_not_require_restart(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            report_path = root / "report.json"
            output_path = root / "repair.json"
            _write(
                report_path,
                {
                    "case_id": "c1",
                    "status": "REPAIRABLE_FAILURE",
                    "issues": [{"path": "$.questions[Q1].blind_core", "code": "BLIND_CORE_MISSING"}],
                },
            )
            result = create_repair_receipt(report_path, output_path)
            self.assertEqual(result["repair_class"], "LOCAL_NODE_REPAIR_ALLOWED")
            self.assertFalse(result["restart_required"])

    def test_case_freeze_is_non_overwriting(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            source_path = root / "validated.json"
            freeze_path = root / "freeze.json"
            _write(source_path, _validated("c1"))
            first = freeze_case(source_path, freeze_path)
            self.assertEqual(first["status"], "PREDICTION_FROZEN")
            with self.assertRaises(FortuneError):
                freeze_case(source_path, freeze_path)

    def test_group_validation_requires_every_case(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            manifest_path = root / "manifest.json"
            output_path = root / "group-validation.json"
            _write(
                manifest_path,
                {
                    "group_id": "dev",
                    "group_run_id": "g1",
                    "case_count": 2,
                    "packets": [{"case_id": "c1"}, {"case_id": "c2"}],
                },
            )
            report_path = root / "c1-report.json"
            validated_path = root / "c1-validated.json"
            _write(report_path, {"case_id": "c1", "status": "PASS_READY_FOR_PREDICTION_FREEZE", "issue_count": 0})
            _write(validated_path, _validated("c1"))
            result = validate_group(manifest_path, [report_path], [validated_path], output_path)
            self.assertEqual(result["status"], "REPAIRABLE_FAILURE")
            self.assertTrue(any(row["case_id"] == "c2" and row["status"] == "MISSING_CASE_ARTIFACT" for row in result["case_rows"]))

    def test_group_freeze_requires_exact_case_set(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            validation_path = root / "group-validation.json"
            _write(
                validation_path,
                {
                    "schema": "GROUP-PREDICTION-VALIDATION-V1",
                    "group_id": "dev",
                    "group_run_id": "g1",
                    "answer_data_available": False,
                    "status": "PASS_READY_FOR_GROUP_FREEZE",
                    "case_rows": [{"case_id": "c1"}, {"case_id": "c2"}],
                },
            )
            c1_validated = root / "c1-validated.json"
            c2_validated = root / "c2-validated.json"
            c1_freeze = root / "c1-freeze.json"
            c2_freeze = root / "c2-freeze.json"
            _write(c1_validated, _validated("c1"))
            _write(c2_validated, _validated("c2"))
            freeze_case(c1_validated, c1_freeze)
            freeze_case(c2_validated, c2_freeze)
            result = freeze_group(validation_path, [c1_freeze, c2_freeze], root / "groups")
            self.assertEqual(result["status"], "GROUP_PREDICTION_FROZEN")
            self.assertEqual(result["case_count"], 2)


if __name__ == "__main__":
    unittest.main()
