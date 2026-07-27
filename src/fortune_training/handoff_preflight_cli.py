from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .chat_input import HANDOFF_TARGET_MAX_CHARACTERS
from .handoff_probe import validate_handoff
from .util import TrainingError, atomic_write_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Normalize and fully validate a Chat-to-Work prediction handoff"
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--issue-title", required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        handoff, report = validate_handoff(
            args.root,
            issue_title=args.issue_title,
            issue_body=args.input.read_text(encoding="utf-8"),
            include_preflight_report=True,
        )
        compact = json.dumps(
            handoff,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        if len(compact) > HANDOFF_TARGET_MAX_CHARACTERS:
            raise TrainingError(
                "normalized handoff exceeds the target Issue body size"
            )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(compact + "\n", encoding="utf-8")
        atomic_write_json(args.report, report)
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    except (OSError, TrainingError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
