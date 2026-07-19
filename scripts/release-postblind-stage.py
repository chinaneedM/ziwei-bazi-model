#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from fortune_v1.staged_access import release_postblind_stage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage-plan", required=True)
    parser.add_argument("--seal-bundle", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = release_postblind_stage(args.stage_plan, args.seal_bundle, args.output)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
