from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .formal import (
    PREDICTION_ACCESS_STARTUP_ORDER_VIOLATION,
    PREDICTION_CONTEXT_VIOLATION,
    invalidate_current_pre_freeze_round,
    quarantine_current_case,
)
from .issue_relay import extract_packet
from .util import TrainingError, atomic_write_json, require_safe_id


PACKET_SCHEMA = "PREDICTION-CONTAMINATION-REPORT-V1"
NON_EXECUTED_STATUS = "PRE-FREEZE_CONTAMINATED_NOT_EXECUTED"


def validate_contamination_report(report: dict[str, Any]) -> dict[str, Any]:
    expected_fields = {"schema", "round_id", "case_id", "reason"}
    if set(report) != expected_fields:
        raise TrainingError("contamination report must contain exactly the four allowed fields")
    if report.get("schema") != PACKET_SCHEMA:
        raise TrainingError(f"contamination report schema must be {PACKET_SCHEMA}")
    require_safe_id(report.get("round_id"), "round_id")
    require_safe_id(report.get("case_id"), "case_id")
    if report.get("reason") not in {
        PREDICTION_CONTEXT_VIOLATION,
        PREDICTION_ACCESS_STARTUP_ORDER_VIOLATION,
    }:
        raise TrainingError("unsupported prediction-contamination reason")
    return report


def parse_contamination_report(issue_body: str) -> dict[str, Any]:
    """Accept the canonical JSON packet or the exact four-line administrative form."""
    try:
        return validate_contamination_report(extract_packet(issue_body))
    except TrainingError as packet_error:
        rows: dict[str, str] = {}
        for raw_line in issue_body.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            key, separator, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if not separator or not key or not value or key in rows:
                raise TrainingError(
                    "contamination report must be valid JSON or exact key-value fields"
                ) from packet_error
            rows[key] = value
        if set(rows) != {"round_id", "case_id", "status", "reason"}:
            raise TrainingError(
                "administrative contamination report must contain exactly "
                "round_id, case_id, status, and reason"
            ) from packet_error
        if rows["status"] != NON_EXECUTED_STATUS:
            raise TrainingError(
                f"administrative contamination status must be {NON_EXECUTED_STATUS}"
            ) from packet_error
        return validate_contamination_report(
            {
                "schema": PACKET_SCHEMA,
                "round_id": rows["round_id"],
                "case_id": rows["case_id"],
                "reason": rows["reason"],
            }
        )


def process_contamination_report(root: Path, report: dict[str, Any]) -> dict[str, Any]:
    report = validate_contamination_report(report)
    if report["reason"] == PREDICTION_ACCESS_STARTUP_ORDER_VIOLATION:
        return invalidate_current_pre_freeze_round(
            root,
            report["round_id"],
            report["case_id"],
            reason=report["reason"],
        )
    return quarantine_current_case(
        root,
        report["round_id"],
        report["case_id"],
        reason=report["reason"],
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Process one owner-submitted prediction-contamination issue"
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--issue-body-file", type=Path, required=True)
    parser.add_argument("--result-file", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = parse_contamination_report(
            args.issue_body_file.read_text(encoding="utf-8")
        )
        result = process_contamination_report(args.root.resolve(), report)
        atomic_write_json(args.result_file, result)
    except (OSError, TrainingError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
