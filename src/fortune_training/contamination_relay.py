from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .formal import PREDICTION_CONTEXT_VIOLATION, quarantine_current_case
from .issue_relay import extract_packet
from .util import TrainingError, atomic_write_json, require_safe_id


PACKET_SCHEMA = "PREDICTION-CONTAMINATION-REPORT-V1"


def validate_contamination_report(report: dict[str, Any]) -> dict[str, Any]:
    expected_fields = {"schema", "round_id", "case_id", "reason"}
    if set(report) != expected_fields:
        raise TrainingError("contamination report must contain exactly the four allowed fields")
    if report.get("schema") != PACKET_SCHEMA:
        raise TrainingError(f"contamination report schema must be {PACKET_SCHEMA}")
    require_safe_id(report.get("round_id"), "round_id")
    require_safe_id(report.get("case_id"), "case_id")
    if report.get("reason") != PREDICTION_CONTEXT_VIOLATION:
        raise TrainingError("unsupported prediction-contamination reason")
    return report


def process_contamination_report(root: Path, report: dict[str, Any]) -> dict[str, Any]:
    report = validate_contamination_report(report)
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
        report = extract_packet(args.issue_body_file.read_text(encoding="utf-8"))
        result = process_contamination_report(args.root.resolve(), report)
        atomic_write_json(args.result_file, result)
    except (OSError, TrainingError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
