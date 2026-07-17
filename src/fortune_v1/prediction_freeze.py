from __future__ import annotations

from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, read_json, sha256_file, slug, utc_now

VALIDATED_OUTPUT_SCHEMA = "VALIDATED-CHAT-PROFESSIONAL-OUTPUT-V1"
VALIDATION_REPORT_SCHEMA = "CHAT-OUTPUT-VALIDATION-V1"
PACKET_MANIFEST_SCHEMA = "CHAT-PROFESSIONAL-PACKET-MANIFEST-V1"
CASE_FREEZE_SCHEMA = "CASE-PREDICTION-FREEZE-V1"
GROUP_FREEZE_SCHEMA = "GROUP-PREDICTION-FREEZE-V1"
GROUP_VALIDATION_SCHEMA = "GROUP-PREDICTION-VALIDATION-V1"
REPAIR_RECEIPT_SCHEMA = "PREDICTION-REPAIR-RECEIPT-V1"


def _validate_case_output(
    path: Path,
    expected_case_id: str | None = None,
    expected_group_run_id: str | None = None,
) -> dict[str, Any]:
    value = read_json(path)
    if value.get("schema") != VALIDATED_OUTPUT_SCHEMA:
        raise FortuneError("wrong validated output schema", status="VALIDATED_OUTPUT_SCHEMA_INVALID")
    if expected_case_id is not None and value.get("case_id") != expected_case_id:
        raise FortuneError("validated output case mismatch", status="VALIDATED_OUTPUT_CASE_MISMATCH")
    if expected_group_run_id is not None and value.get("group_run_id") != expected_group_run_id:
        raise FortuneError("validated output group mismatch", status="VALIDATED_OUTPUT_GROUP_MISMATCH")
    if value.get("answer_data_available") is not False:
        raise FortuneError("answer data visible in prediction output", status="PREDICTION_OUTPUT_CONTAMINATED")
    if value.get("status") != "PASS_READY_FOR_PREDICTION_FREEZE":
        raise FortuneError("case output is not ready for freeze", status="CASE_NOT_READY_FOR_FREEZE")
    questions = value.get("questions", [])
    if not questions:
        raise FortuneError("validated output has no questions", status="CASE_QUESTION_SET_EMPTY")
    question_ids: set[str] = set()
    for question in questions:
        question_id = question.get("question_id")
        if not question_id or question_id in question_ids:
            raise FortuneError("duplicate or missing question id", status="QUESTION_ID_SET_INVALID")
        question_ids.add(question_id)
        expected = question.get("pairwise_row_count_expected")
        actual = question.get("pairwise_row_count_actual")
        if expected is None or expected != actual or len(question.get("pairwise_rows", [])) != expected:
            raise FortuneError("pairwise rows incomplete", status="PAIRWISE_ROWS_INCOMPLETE")
        order = question.get("option_order", [])
        if len(order) < 2 or len(order) != len(set(order)):
            raise FortuneError("option order invalid", status="OPTION_ORDER_INVALID")
        if question.get("top1") != order[0] or question.get("top2") != order[1]:
            raise FortuneError("top selections mismatch option order", status="TOP_SELECTION_ORDER_INVALID")
    return value


def create_repair_receipt(validation_report_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    report_file = Path(validation_report_path)
    report = read_json(report_file)
    if report.get("schema") != VALIDATION_REPORT_SCHEMA:
        raise FortuneError("wrong validation report schema", status="VALIDATION_REPORT_SCHEMA_INVALID")
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
        "packet_sha256": source.get("packet_sha256"),
        "chat_output_sha256": source.get("chat_output_sha256"),
        "answer_data_available": False,
        "questions": source["questions"],
        "prediction_mutability": "IMMUTABLE_AFTER_FREEZE",
        "reveal_access_before_freeze": False,
        "status": "PREDICTION_FROZEN",
        "frozen_at": utc_now(),
    }
    atomic_write_json(output_file, freeze)
    output_file.chmod(0o444)
    return {**freeze, "freeze_path": str(output_file), "freeze_sha256": sha256_file(output_file)}


def validate_group(
    packet_manifest_path: str | Path,
    case_validation_report_paths: list[str | Path],
    case_validated_output_paths: list[str | Path],
    output_path: str | Path,
) -> dict[str, Any]:
    manifest_file = Path(packet_manifest_path)
    manifest = read_json(manifest_file)
    if manifest.get("schema") != PACKET_MANIFEST_SCHEMA:
        raise FortuneError("wrong packet manifest schema", status="PACKET_MANIFEST_SCHEMA_INVALID")
    if manifest.get("status") != "READY_FOR_CHAT_PROFESSIONAL_REASONING":
        raise FortuneError("packet manifest is not ready", status="PACKET_MANIFEST_NOT_READY")
    group_run_id = manifest.get("group_run_id")
    packet_rows = manifest.get("packets", [])
    expected_case_ids = [row.get("case_id") for row in packet_rows]
    if not expected_case_ids or None in expected_case_ids or len(expected_case_ids) != len(set(expected_case_ids)):
        raise FortuneError("packet manifest case set invalid", status="PACKET_MANIFEST_CASE_SET_INVALID")
    if manifest.get("case_count") != len(expected_case_ids):
        raise FortuneError("packet manifest count mismatch", status="PACKET_MANIFEST_COUNT_MISMATCH")
    expected_rows = {row["case_id"]: row for row in packet_rows}

    reports: dict[str, dict[str, Any]] = {}
    duplicate_report_ids: set[str] = set()
    for raw_path in case_validation_report_paths:
        report_file = Path(raw_path)
        report = read_json(report_file)
        if report.get("schema") != VALIDATION_REPORT_SCHEMA:
            raise FortuneError("wrong case validation report schema", status="VALIDATION_REPORT_SCHEMA_INVALID")
        case_id = report.get("case_id")
        if not case_id:
            raise FortuneError("validation report missing case id", status="VALIDATION_REPORT_CASE_ID_MISSING")
        if case_id in reports:
            duplicate_report_ids.add(case_id)
        reports[case_id] = {
            "path": str(report_file),
            "sha256": sha256_file(report_file),
            "status": report.get("status"),
            "issue_count": report.get("issue_count"),
            "validated_output_path": report.get("validated_output_path"),
            "validated_output_sha256": report.get("validated_output_sha256"),
        }

    outputs: dict[str, dict[str, Any]] = {}
    duplicate_output_ids: set[str] = set()
    for raw_path in case_validated_output_paths:
        output_file = Path(raw_path)
        output = read_json(output_file)
        case_id = output.get("case_id")
        if not case_id:
            raise FortuneError("validated output missing case id", status="VALIDATED_OUTPUT_CASE_ID_MISSING")
        if case_id in outputs:
            duplicate_output_ids.add(case_id)
        outputs[case_id] = {
            "path": str(output_file),
            "sha256": sha256_file(output_file),
            "status": output.get("status"),
            "group_run_id": output.get("group_run_id"),
            "schema": output.get("schema"),
            "question_count": len(output.get("questions", [])),
        }

    case_rows = []
    group_status = "PASS_READY_FOR_GROUP_FREEZE"
    for case_id in expected_rows:
        report = reports.get(case_id)
        output = outputs.get(case_id)
        reasons: list[str] = []
        if case_id in duplicate_report_ids:
            reasons.append("DUPLICATE_VALIDATION_REPORT")
        if case_id in duplicate_output_ids:
            reasons.append("DUPLICATE_VALIDATED_OUTPUT")
        if report is None or output is None:
            status = "MISSING_CASE_ARTIFACT"
            reasons.append(status)
        elif report["status"] == "FAIL_CLOSED_CONTAMINATED":
            status = "FAIL_CLOSED_CONTAMINATED"
            reasons.append(status)
        else:
            if output["schema"] != VALIDATED_OUTPUT_SCHEMA:
                reasons.append("VALIDATED_OUTPUT_SCHEMA_INVALID")
            if output["group_run_id"] != group_run_id:
                reasons.append("VALIDATED_OUTPUT_GROUP_MISMATCH")
            if report["validated_output_sha256"] != output["sha256"]:
                reasons.append("REPORT_OUTPUT_HASH_MISMATCH")
            if report["validated_output_path"] != output["path"]:
                reasons.append("REPORT_OUTPUT_PATH_MISMATCH")
            if report["status"] != output["status"]:
                reasons.append("REPORT_OUTPUT_STATUS_MISMATCH")
            if report["status"] != "PASS_READY_FOR_PREDICTION_FREEZE":
                reasons.append("CASE_VALIDATION_NOT_PASS")
            status = "PASS_READY_FOR_CASE_FREEZE" if not reasons else "REPAIRABLE_FAILURE"

        if status == "FAIL_CLOSED_CONTAMINATED":
            group_status = "FAIL_CLOSED_CONTAMINATED"
        elif status != "PASS_READY_FOR_CASE_FREEZE" and group_status != "FAIL_CLOSED_CONTAMINATED":
            group_status = "REPAIRABLE_FAILURE"
        case_rows.append(
            {
                "case_id": case_id,
                "status": status,
                "reasons": reasons,
                "validation_report": report,
                "validated_output": output,
            }
        )

    unknown_case_ids = sorted((set(reports) | set(outputs)) - set(expected_rows))
    if (unknown_case_ids or duplicate_report_ids or duplicate_output_ids) and group_status == "PASS_READY_FOR_GROUP_FREEZE":
        group_status = "REPAIRABLE_FAILURE"

    result = {
        "schema": GROUP_VALIDATION_SCHEMA,
        "group_id": manifest.get("group_id"),
        "group_run_id": group_run_id,
        "packet_manifest_path": str(manifest_file),
        "packet_manifest_sha256": sha256_file(manifest_file),
        "expected_case_count": manifest.get("case_count"),
        "actual_case_count": len([row for row in case_rows if row["status"] == "PASS_READY_FOR_CASE_FREEZE"]),
        "case_rows": case_rows,
        "unknown_case_ids": unknown_case_ids,
        "duplicate_validation_report_case_ids": sorted(duplicate_report_ids),
        "duplicate_validated_output_case_ids": sorted(duplicate_output_ids),
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
    group_run_id = validation.get("group_run_id")
    expected_rows = {row["case_id"]: row for row in validation["case_rows"]}
    if any(row.get("status") != "PASS_READY_FOR_CASE_FREEZE" for row in expected_rows.values()):
        raise FortuneError("group contains non-pass case", status="GROUP_CASE_STATUS_INVALID")

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
        if freeze.get("group_run_id") != group_run_id:
            raise FortuneError("case freeze belongs to another group", status="CASE_FREEZE_GROUP_MISMATCH")
        expected_output = expected_rows.get(case_id, {}).get("validated_output")
        if expected_output is None:
            raise FortuneError("case freeze not present in validation", status="CASE_FREEZE_NOT_VALIDATED")
        if freeze.get("validated_output_sha256") != expected_output.get("sha256"):
            raise FortuneError("case freeze source hash mismatch", status="CASE_FREEZE_SOURCE_MISMATCH")
        seen.add(case_id)
        freeze_rows.append({"case_id": case_id, "path": str(freeze_file), "sha256": sha256_file(freeze_file)})
    if seen != set(expected_rows):
        raise FortuneError("case freeze set does not match group", status="GROUP_CASE_FREEZE_SET_MISMATCH")

    output_dir = Path(output_root) / slug(group_run_id)
    if output_dir.exists():
        raise FortuneError("group freeze output already exists", status="GROUP_FREEZE_NONOVERWRITE_FAILED")
    output_dir.mkdir(parents=True, exist_ok=False)
    output_file = output_dir / "group-freeze.json"
    group_freeze = {
        "schema": GROUP_FREEZE_SCHEMA,
        "group_id": validation["group_id"],
        "group_run_id": group_run_id,
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
    output_file.chmod(0o444)
    return {**group_freeze, "group_freeze_path": str(output_file), "group_freeze_sha256": sha256_file(output_file)}
