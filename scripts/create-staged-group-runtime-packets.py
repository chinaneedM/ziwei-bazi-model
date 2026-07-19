#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile

from fortune_v1.staged_access import build_legacy_runtime_inputs, harden_runtime_packets


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True)
    parser.add_argument("--max-per-question", type=int, default=8)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="fortune-staged-runtime-") as tmp:
        legacy_request, canonical_clean = build_legacy_runtime_inputs(args.request, tmp)
        completed = subprocess.run(
            [
                sys.executable,
                "scripts/create-group-runtime-packets.py",
                "--request",
                str(legacy_request),
                "--max-per-question",
                str(args.max_per_question),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        legacy_result = json.loads(completed.stdout)
    result = harden_runtime_packets(legacy_result, args.request, canonical_clean)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
