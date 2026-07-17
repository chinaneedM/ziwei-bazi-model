from __future__ import annotations

import json
from pathlib import Path

import pytest

from fortune_v1.prediction_freeze import (
    create_repair_receipt,
    freeze_case,
    freeze_group,
    validate_group,
)


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


def test_repairable_failure_does_not_require_restart(tmp_path: Path) -> None:
    report_path = tmp_path / "report.json"
    output_path = tmp_path / "repair.json"
    _write(
        report_path,
        {
            "case_id": "c1",
            "status": "REPAIRABLE_FAILURE",
            "issues": [{"path": "$.questions[Q1].blind_core", "code": "BLIND_CORE_MISSING"}],
        },
    )
    result = create_repair_receipt(report_path, output_path)
    assert result["repair_class"] == "LOCAL_NODE_REPAIR_ALLOWED"
    assert result["restart_required"] is False


def test_case_freeze_is_non_overwriting(tmp_path: Path) -> None:
    source_path = tmp_path / "validated.json"
    freeze_path = tmp_path / "freeze.json"
    _write(source_path, _validated("c1"))
    first = freeze_case(source_path, freeze_path)
    assert first["status"] == "PREDICTION_FROZEN"
    with pytest.raises(Exception):
        freeze_case(source_path, freeze_path)


def test_group_validation_requires_every_case(tmp_path: Path) -> None:
    manifest_path = tmp_path / "manifest.json"
    output_path = tmp_path / "group-validation.json"
    _write(
        manifest_path,
        {
            "group_id": "dev",
            "group_run_id": "g1",
            "case_count": 2,
            "packets": [{"case_id": "c1"}, {"case_id": "c2"}],
        },
    )
    report_path = tmp_path / "c1-report.json"
    validated_path = tmp_path / "c1-validated.json"
    _write(report_path, {"case_id": "c1", "status": "PASS_READY_FOR_PREDICTION_FREEZE", "issue_count": 0})
    _write(validated_path, _validated("c1"))
    result = validate_group(manifest_path, [report_path], [validated_path], output_path)
    assert result["status"] == "REPAIRABLE_FAILURE"
    assert any(row["case_id"] == "c2" and row["status"] == "MISSING_CASE_ARTIFACT" for row in result["case_rows"])


def test_group_freeze_requires_exact_case_set(tmp_path: Path) -> None:
    validation_path = tmp_path / "group-validation.json"
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
    c1_validated = tmp_path / "c1-validated.json"
    c2_validated = tmp_path / "c2-validated.json"
    c1_freeze = tmp_path / "c1-freeze.json"
    c2_freeze = tmp_path / "c2-freeze.json"
    _write(c1_validated, _validated("c1"))
    _write(c2_validated, _validated("c2"))
    freeze_case(c1_validated, c1_freeze)
    freeze_case(c2_validated, c2_freeze)
    result = freeze_group(validation_path, [c1_freeze, c2_freeze], tmp_path / "groups")
    assert result["status"] == "GROUP_PREDICTION_FROZEN"
    assert result["case_count"] == 2
