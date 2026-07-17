from __future__ import annotations

from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, read_json, sha256_file, slug, utc_now

VALIDATED_OUTPUT_SCHEMA = "VALIDATED-CHAT-PROFESSIONAL-OUTPUT-V1"
CASE_FREEZE_SCHEMA = "CASE-PREDICTION-FREEZE-V1"
GROUP_FREEZE_SCHEMA = "GROUP-PREDICTION-FREEZE-V1"
GROUP_VALIDATION_SCHEMA = "GROUP-PREDICTION-VALIDATION-V1"
REPAIR_RECEIPT_SCHEMA = "PREDICTION-REPAIR-RECEIPT-V1"


def _validate_case_output(path: Path, expected_case_id: str | None = None) -> dict[str, Any]:
    value = read_json(path)
    if value.get("schema") != VALIDATED_OUTPUT_SCHEMA:
        raise FortuneError("wrong validated output schema", status="VALIDATED_OUTPUT_SCHEMA_INVALID")
    if expected_case_id is not None and value.get("case_id") != expected_case_id:
        raise FortuneError("validated output case mismatch", status="VALIDATED_OUTPUT_CASE_MISMATCH")
    if value.get("answer_data_available") is not False:
        raise FortuneError("answer data visible in prediction output", status="PREDICTION_OUTPUT_CONTAMINATED")
    if value.get("status") != "PASS_READY_FOR_PREDICTION_FREEZE":
        raise FortuneError("case output is not ready for freeze", status="CASE_NOT_READY_FOR_FREEZE")
    questions = value.get("questions", [])
    if not questions:
        raise FortuneError("validated output has no questions", status="CASE_QUESTION_SET_EMPTY")
    for question in questions:
        expected = question.get("pairwise_row_count_expected")
        actual = question.get("pairwise_row_count_actual")
        if expected is None or expected != actual:
            raise FortuneError("pairwise rows incomplete", status="PAIRWISE_ROWS_INCOMPLETE")
        order = question.get("option_order", [])
        if len(order) < 2 or question.get("top1") != order[0] or question.get("top2") != order[1]:
            raise FortuneError("top selections mismatch option order", status="TOP_SELECTION_ORDER_INVALID")
    return value


def create_repair_receipt(validation_report_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    report_file = Path(validation_report_path)
    report = read_json(report_file)
    status = report.get("status")
    if status == "FAIL_CLOSED_CONTAMINATED":
        repair_class = "NON_REPAIRABLE_RESTART_REQUIRED"
        restart_required = True
    elif status == "REPAIRABLE_FAILURE":
        repair_class = "LOCAL_NODE_REPAIR_ALLOWED"
        restart_required = False
    elif status == "PASS_READY_FOR_PREDICTION_FREEZE":
        repair_class = "NO_REPAIR_REQUIRED"
        restart_required = False
    else:
        repair_class = "UNKNOWN_STATUS_MANUAL_REVIEW"
        restart_required = False
    receipt = {
        "schema": REPAIR_RECEIPT_SCHEMA,
        "case_id": report.get("case_id"),
        "validation_report_path": str(report_file),
        "validation_report_sha256": sha256_file(report_file),
        "source_status": status,
        "repair_class": repair_class,
        "restart_required": restart_required,
        "issue_rows": report.get("issues", []),
        "allowed_repair_scope": [] if restart_required else sorted({row.get("path", "$") for row in report.get("issues", [])}),
        "created_at": utc_now(),
    }
    atomic_write_json(output_path, receipt)
    return receipt


def freeze_case(validated_output_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    source_file = Path(validated_output_path)
    source = _validate_case_output(source_file)
    output_file = Path(output_path)
    if output_file.exists():
        raise FortuneError("case freeze already exists", status="CASE_FREEZE_NONOVERWRITE_FAILED")
    freeze = {
        "schema": CASE_FREEZE_SCHEMA,
        "case_id": source["case_id"],
        "group_run_id": source["group_run_id"],
        "validated_output_path": str(source_file),
        "validated_output_sha256": sha256_file(source_file),
        "answer_data_available": False,
        "questions": source["questions"],
        "prediction_mutability": "IMMUTABLE_AFTER_FREEZE",
        "reveal_access_before_freeze": False,
        "status": "PREDICTION_FROZEN",
        "frozen_at": utc_now(),
    }
    atomic_write_json(output_file, freeze)
    return {**freeze, "freeze_path": str(output_file), "freeze_sha256": sha256_file(output_file)}


def validate_group(
    packet_manifest_path: str | Path,
    case_validation_report_paths: list[str | Path],
    case_validated_output_paths: list[str | Path],
    output_path: str | Path,
) -> dict[str, Any]:
    manifest_file = Path(packet_manifest_path)
    manifest = read_json(manifest_file)
    expected_rows = {row["case_id"]: row for row in manifest.get("packets", [])}
    reports: dict[str, dict[str, Any]] = {}
    for raw_path in case_validation_report_paths:
        report_file = Path(raw_path)
        report = read_json(report_file)
        case_id = report.get("case_id")
        reports[case_id] = {
            "path": str(report_file),
            "sha256": sha256_file(report_file),
            "status": report.get("status"),
            "issue_count": report.get("issue_count"),
        }
    outputs: dict[str, dict[str, Any]] = {}
    for raw_path in case_validated_output_paths:
        output_file = Path(raw_path)
        output = read_json(output_file)
        case_id = output.get("case_id")
        outputs[case_id] = {
            "path": str(output_file),
            "sha256": sha256_file(output_file),
            "status": output.get("status"),
            "question_count": len(output.get("questions", [])),
        }

    case_rows = []
    group_status = "PASS_READY_FOR_GROUP_FREEZE"
    for case_id in expected_rows:
        report = reports.get(case_id)
        output = outputs.get(case_id)
        if report is None or output is None:
            status = "MISSING_CASE_ARTIFACT"
            group_status = "REPAIRABLE_FAILURE"
        elif report["status"] == "FAIL_CLOSED_CONTAMINATED":
            status = "FAIL_CLOSED_CONTAMINATED"
            group_status = "FAIL_CLOSED_CONTAMINATED"
        elif report["status"] != "PASS_READY_FOR_PREDICTION_FREEZE" or output["status"] != "PASS_READY_FOR_PREDICTION_FREEZE":
            status = "REPAIRABLE_FAILURE"
            if group_status != "FAIL_CLOSED_CONTAMINATED":
                group_status = "REPAIRABLE_FAILURE"
        else:
            status = "PASS_READY_FOR_CASE_FREEZE"
        case_rows.append({"case_id": case_id, "status": status, "validation_report": report, "validated_output": output})

    unknown_case_ids = sorted((set(reports) | set(outputs)) - set(expected_rows))
    if unknown_case_ids and group_status == "PASS_READY_FOR_GROUP_FREEZE":
        group_status = "REPAIRABLE_FAILURE"

    result = {
        "schema": GROUP_VALIDATION_SCHEMA,
        "group_id": manifest.get("group_id"),
        "group_run_id": manifest.get("group_run_id"),
        "packet_manifest_path": str(manifest_file),
        "packet_manifest_sha256": sha256_file(manifest_file),
        "expected_case_count": manifest.get("case_count"),
        "actual_case_count": len([row for row in case_rows if row["status"] == "PASS_READY_FOR_CASE_FREEZE"]),
        "case_rows": case_rows,
        "unknown_case_ids": unknown_case_ids,
        "answer_data_available": False,
        "status": group_status,
        "restart_required": group_status == "FAIL_CLOSED_CONTAMINATED",
        "generated_at": utc_now(),
    }
    atomic_write_json(output_path, result)
    return result


def freeze_group(group_validation_path: str | Path, case_freeze_paths: list[str | Path], output_root: str | Path) -> dict[str, Any]:
    validation_file = Path(group_validation_path)
    validation = read_json(validation_file)
    if validation.get("schema") != GROUP_VALIDATION_SCHEMA:
        raise FortuneError("wrong group validation schema", status="GROUP_VALIDATION_SCHEMA_INVALID")
    if validation.get("status") != "PASS_READY_FOR_GROUP_FREEZE":
        raise FortuneError("group validation did not pass", status="GROUP_NOT_READY_FOR_FREEZE")
    if validation.get("answer_data_available") is not False:
        raise FortuneError("answer data visible before group freeze", status="GROUP_FREEZE_CONTAMINATED")

    expected_case_ids = {row["case_id"] for row in validation["case_rows"]}
    freeze_rows = []
    seen: set[str] = set()
    for raw_path in case_freeze_paths:
        freeze_file = Path(raw_path)
        freeze = read_json(freeze_file)
        if freeze.get("schema") != CASE_FREEZE_SCHEMA or freeze.get("status") != "PREDICTION_FROZEN":
            raise FortuneError("invalid case freeze", status="CASE_FREEZE_INVALID")
        case_id = freeze.get("case_id")
        if case_id in seen:
            raise FortuneError("duplicate case freeze", status="DUPLICATE_CASE_FREEZE")
        seen.add(case_id)
        freeze_rows.append({"case_id": case_id, "path": str(freeze_file), "sha256": sha256_file(freeze_file)})
    if seen != expected_case_ids:
        raise FortuneError("case freeze set does not match group", status="GROUP_CASE_FREEZE_SET_MISMATCH")

    output_dir = Path(output_root) / slug(validation["group_run_id"])
    if output_dir.exists():
        raise FortuneError("group freeze output already exists", status="GROUP_FREEZE_NONOVERWRITE_FAILED")
    output_dir.mkdir(parents=True, exist_ok=False)
    output_file = output_dir / "group-freeze.json"
    group_freeze = {
        "schema": GROUP_FREEZE_SCHEMA,
        "group_id": validation["group_id"],
        "group_run_id": validation["group_run_id"],
        "group_validation_path": str(validation_file),
        "group_validation_sha256": sha256_file(validation_file),
        "case_freezes": sorted(freeze_rows, key=lambda row: row["case_id"]),
        "case_count": len(freeze_rows),
        "answer_data_available": False,
        "prediction_mutability": "IMMUTABLE_AFTER_FREEZE",
        "reveal_permission": "MAY_BEGIN_ONLY_AFTER_THIS_FILE_EXISTS",
        "status": "GROUP_PREDICTION_FROZEN",
        "frozen_at": utc_now(),
    }
    atomic_write_json(output_file, group_freeze)
    return {**group_freeze, "group_freeze_path": str(output_file), "group_freeze_sha256": sha256_file(output_file)}
