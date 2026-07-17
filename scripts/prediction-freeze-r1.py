#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from fortune_v1.prediction_freeze import (
    create_repair_receipt,
    freeze_case,
    freeze_group,
    validate_group,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Prediction freeze and group validation for semi-automated R1")
    sub = parser.add_subparsers(dest="command", required=True)

    repair = sub.add_parser("repair-receipt")
    repair.add_argument("--validation-report", required=True)
    repair.add_argument("--output", required=True)

    case_freeze = sub.add_parser("freeze-case")
    case_freeze.add_argument("--validated-output", required=True)
    case_freeze.add_argument("--output", required=True)

    group_validate = sub.add_parser("validate-group")
    group_validate.add_argument("--packet-manifest", required=True)
    group_validate.add_argument("--validation-report", action="append", required=True)
    group_validate.add_argument("--validated-output", action="append", required=True)
    group_validate.add_argument("--output", required=True)

    group_freeze = sub.add_parser("freeze-group")
    group_freeze.add_argument("--group-validation", required=True)
    group_freeze.add_argument("--case-freeze", action="append", required=True)
    group_freeze.add_argument("--output-root", required=True)

    args = parser.parse_args()
    if args.command == "repair-receipt":
        result = create_repair_receipt(args.validation_report, args.output)
    elif args.command == "freeze-case":
        result = freeze_case(args.validated_output, args.output)
    elif args.command == "validate-group":
        result = validate_group(
            args.packet_manifest,
            args.validation_report,
            args.validated_output,
            args.output,
        )
    else:
        result = freeze_group(args.group_validation, args.case_freeze, args.output_root)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
