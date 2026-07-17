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
from fortune_v1.util import FortuneError, sha256_file


def _write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def _validated(case_id: str, group_run_id: str = "g1") -> dict:
    return {
        "schema": "VALIDATED-CHAT-PROFESSIONAL-OUTPUT-V1",
        "case_id": case_id,
        "group_run_id": group_run_id,
        "packet_sha256": "packet-hash",
        "chat_output_sha256": "chat-output-hash",
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
                "pairwise_rows": [
                    {"left": "B", "right": "A", "winner": "B"},
                    {"left": "B", "right": "C", "winner": "B"},
                    {"left": "A", "right": "C", "winner": "A"},
                ],
            }
        ],
    }


def _report(case_id: str, validated_path: Path, status: str = "PASS_READY_FOR_PREDICTION_FREEZE") -> dict:
    return {
        "schema": "CHAT-OUTPUT-VALIDATION-V1",
        "case_id": case_id,
        "status": status,
        "issue_count": 0,
        "issues": [],
        "validated_output_path": str(validated_path),
        "validated_output_sha256": sha256_file(validated_path),
    }


def _manifest(case_ids: list[str], group_run_id: str = "g1") -> dict:
    return {
        "schema": "CHAT-PROFESSIONAL-PACKET-MANIFEST-V1",
        "group_id": "dev",
        "group_run_id": group_run_id,
        "case_count": len(case_ids),
        "packets": [{"case_id": case_id} for case_id in case_ids],
        "status": "READY_FOR_CHAT_PROFESSIONAL_REASONING",
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
                    "schema": "CHAT-OUTPUT-VALIDATION-V1",
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
            self.assertEqual(first["validated_output_sha256"], sha256_file(source_path))
            with self.assertRaises(FortuneError):
                freeze_case(source_path, freeze_path)

    def test_group_validation_requires_every_case(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            manifest_path = root / "manifest.json"
            output_path = root / "group-validation.json"
            _write(manifest_path, _manifest(["c1", "c2"]))
            report_path = root / "c1-report.json"
            validated_path = root / "c1-validated.json"
            _write(validated_path, _validated("c1"))
            _write(report_path, _report("c1", validated_path))
            result = validate_group(manifest_path, [report_path], [validated_path], output_path)
            self.assertEqual(result["status"], "REPAIRABLE_FAILURE")
            self.assertTrue(any(row["case_id"] == "c2" and row["status"] == "MISSING_CASE_ARTIFACT" for row in result["case_rows"]))

    def test_group_validation_rejects_cross_group_output(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            manifest_path = root / "manifest.json"
            validated_path = root / "validated.json"
            report_path = root / "report.json"
            group_validation_path = root / "group-validation.json"
            _write(manifest_path, _manifest(["c1"], group_run_id="g1"))
            _write(validated_path, _validated("c1", group_run_id="g2"))
            _write(report_path, _report("c1", validated_path))
            result = validate_group(manifest_path, [report_path], [validated_path], group_validation_path)
            self.assertEqual(result["status"], "REPAIRABLE_FAILURE")
            self.assertIn("VALIDATED_OUTPUT_GROUP_MISMATCH", result["case_rows"][0]["reasons"])

    def test_group_validation_rejects_report_output_hash_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            manifest_path = root / "manifest.json"
            validated_path = root / "validated.json"
            report_path = root / "report.json"
            group_validation_path = root / "group-validation.json"
            _write(manifest_path, _manifest(["c1"]))
            _write(validated_path, _validated("c1"))
            report = _report("c1", validated_path)
            report["validated_output_sha256"] = "tampered"
            _write(report_path, report)
            result = validate_group(manifest_path, [report_path], [validated_path], group_validation_path)
            self.assertEqual(result["status"], "REPAIRABLE_FAILURE")
            self.assertIn("REPORT_OUTPUT_HASH_MISMATCH", result["case_rows"][0]["reasons"])

    def test_group_validation_rejects_duplicate_case_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            manifest_path = root / "manifest.json"
            validated_a = root / "validated-a.json"
            validated_b = root / "validated-b.json"
            report_a = root / "report-a.json"
            report_b = root / "report-b.json"
            group_validation_path = root / "group-validation.json"
            _write(manifest_path, _manifest(["c1"]))
            _write(validated_a, _validated("c1"))
            _write(validated_b, _validated("c1"))
            _write(report_a, _report("c1", validated_a))
            _write(report_b, _report("c1", validated_b))
            result = validate_group(
                manifest_path,
                [report_a, report_b],
                [validated_a, validated_b],
                group_validation_path,
            )
            self.assertEqual(result["status"], "REPAIRABLE_FAILURE")
            self.assertEqual(result["duplicate_validation_report_case_ids"], ["c1"])
            self.assertEqual(result["duplicate_validated_output_case_ids"], ["c1"])

    def test_group_freeze_requires_exact_bound_case_set(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            c1_validated = root / "c1-validated.json"
            c2_validated = root / "c2-validated.json"
            _write(c1_validated, _validated("c1"))
            _write(c2_validated, _validated("c2"))
            validation_path = root / "group-validation.json"
            _write(
                validation_path,
                {
                    "schema": "GROUP-PREDICTION-VALIDATION-V1",
                    "group_id": "dev",
                    "group_run_id": "g1",
                    "answer_data_available": False,
                    "status": "PASS_READY_FOR_GROUP_FREEZE",
                    "case_rows": [
                        {
                            "case_id": "c1",
                            "status": "PASS_READY_FOR_CASE_FREEZE",
                            "validated_output": {"sha256": sha256_file(c1_validated)},
                        },
                        {
                            "case_id": "c2",
                            "status": "PASS_READY_FOR_CASE_FREEZE",
                            "validated_output": {"sha256": sha256_file(c2_validated)},
                        },
                    ],
                },
            )
            c1_freeze = root / "c1-freeze.json"
            c2_freeze = root / "c2-freeze.json"
            freeze_case(c1_validated, c1_freeze)
            freeze_case(c2_validated, c2_freeze)
            result = freeze_group(validation_path, [c1_freeze, c2_freeze], root / "groups")
            self.assertEqual(result["status"], "GROUP_PREDICTION_FROZEN")
            self.assertEqual(result["case_count"], 2)

    def test_group_freeze_rejects_cross_group_case_freeze(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            validated_path = root / "validated.json"
            freeze_path = root / "case-freeze.json"
            _write(validated_path, _validated("c1", group_run_id="g2"))
            freeze_case(validated_path, freeze_path)
            validation_path = root / "group-validation.json"
            _write(
                validation_path,
                {
                    "schema": "GROUP-PREDICTION-VALIDATION-V1",
                    "group_id": "dev",
                    "group_run_id": "g1",
                    "answer_data_available": False,
                    "status": "PASS_READY_FOR_GROUP_FREEZE",
                    "case_rows": [
                        {
                            "case_id": "c1",
                            "status": "PASS_READY_FOR_CASE_FREEZE",
                            "validated_output": {"sha256": sha256_file(validated_path)},
                        }
                    ],
                },
            )
            with self.assertRaises(FortuneError) as raised:
                freeze_group(validation_path, [freeze_path], root / "groups")
            self.assertEqual(raised.exception.status, "CASE_FREEZE_GROUP_MISMATCH")


if __name__ == "__main__":
    unittest.main()
