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
from .util import (
    TrainingError,
    atomic_write_json,
    load_json,
    next_round_id,
    require_safe_id,
)


PACKET_SCHEMA = "PREDICTION-CONTAMINATION-REPORT-V1"
NON_EXECUTED_STATUS = "PRE-FREEZE_CONTAMINATED_NOT_EXECUTED"
RESOLVE_CURRENT_ROUND = "RESOLVE_FROM_MAIN_CURRENT_ACTIVE_ROUND"
ADMINISTRATIVE_FIELDS = {"round_id", "case_id", "status", "reason"}
FORBIDDEN_TRAILING_FIELDS = {
    "answer",
    "answers",
    "expected_answer",
    "prediction",
    "predictions",
    "score",
    "scoring",
    "top1",
    "top2",
}


def validate_contamination_report(report: dict[str, Any]) -> dict[str, Any]:
    expected_fields = {"schema", "round_id", "case_id", "reason"}
    if set(report) != expected_fields:
        raise TrainingError("contamination report must contain exactly the four allowed fields")
    if report.get("schema") != PACKET_SCHEMA:
        raise TrainingError(f"contamination report schema must be {PACKET_SCHEMA}")
    round_id = report.get("round_id")
    if round_id != RESOLVE_CURRENT_ROUND:
        require_safe_id(round_id, "round_id")
    require_safe_id(report.get("case_id"), "case_id")
    if report.get("reason") not in {
        PREDICTION_CONTEXT_VIOLATION,
        PREDICTION_ACCESS_STARTUP_ORDER_VIOLATION,
    }:
        raise TrainingError("unsupported prediction-contamination reason")
    if (
        round_id == RESOLVE_CURRENT_ROUND
        and report.get("reason") != PREDICTION_ACCESS_STARTUP_ORDER_VIOLATION
    ):
        raise TrainingError(
            "automatic current-round resolution is allowed only for a startup-order violation"
        )
    return report


def _parse_administrative_header(issue_body: str) -> dict[str, str]:
    """Parse one exact metadata header while allowing non-machine prose afterwards."""
    lines = issue_body.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)

    header_lines: list[str] = []
    trailing_lines: list[str] = []
    in_trailing = False
    for raw_line in lines:
        if not in_trailing and not raw_line.strip():
            in_trailing = True
            continue
        if in_trailing:
            trailing_lines.append(raw_line)
        else:
            header_lines.append(raw_line)

    rows: dict[str, str] = {}
    for raw_line in header_lines:
        line = raw_line.strip()
        key, separator, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if not separator or not key or not value or key in rows:
            raise TrainingError(
                "contamination report must be valid JSON or begin with an exact "
                "key-value header"
            )
        rows[key] = value
    if set(rows) != ADMINISTRATIVE_FIELDS:
        raise TrainingError(
            "administrative contamination header must contain exactly "
            "round_id, case_id, status, and reason"
        )

    for raw_line in trailing_lines:
        line = raw_line.strip().lstrip("-*").strip()
        key, separator, value = line.partition(":")
        if (
            separator
            and value.strip()
            and key.strip().lower().replace(" ", "_") in FORBIDDEN_TRAILING_FIELDS
        ):
            raise TrainingError(
                "contamination issue prose must not contain answer, prediction, or scoring fields"
            )
    return rows


def parse_contamination_report(issue_body: str) -> dict[str, Any]:
    """Accept canonical JSON or a four-field administrative header plus prose."""
    try:
        return validate_contamination_report(extract_packet(issue_body))
    except TrainingError as packet_error:
        try:
            rows = _parse_administrative_header(issue_body)
        except TrainingError as exc:
            raise exc from packet_error
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
    round_id = report["round_id"]
    if round_id == RESOLVE_CURRENT_ROUND:
        state = load_json(root.resolve() / "training" / "state.json")
        round_id = next_round_id(state)
    if report["reason"] == PREDICTION_ACCESS_STARTUP_ORDER_VIOLATION:
        return invalidate_current_pre_freeze_round(
            root,
            round_id,
            report["case_id"],
            reason=report["reason"],
        )
    return quarantine_current_case(
        root,
        round_id,
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
