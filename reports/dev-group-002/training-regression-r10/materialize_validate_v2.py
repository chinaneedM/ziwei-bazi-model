#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import materialize_validate as r10

r10.HISTORY = {
    'R1': 'reports/dev-group-002/training-regression-r1/manifest.json',
    'R2': 'reports/dev-group-002/training-regression-r2/formal-readiness-matrix.json',
    'R3': 'reports/dev-group-002/training-regression-r3/progress.json',
    'R4': 'reports/dev-group-002/training-regression-r4/compact-manifest.json',
    'R5': 'reports/dev-group-002/training-regression-r5/manifest.json',
    'R6': 'reports/dev-group-002/training-regression-r6/manifest.json',
    'R7': 'reports/dev-group-002/training-regression-r7/manifest.json',
    'R8': 'reports/dev-group-002/training-regression-r8/manifest.json',
    'R9': 'reports/dev-group-002/training-regression-r9/manifest.json',
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo-root', default='.')
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--validate', action='store_true')
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    if not args.write and not args.validate:
        parser.error('select --write and/or --validate')
    if args.write:
        r10.materialize(root)
    if args.validate:
        result = r10.validate(root)
        result['schema'] = 'DEV-GROUP-002-R10-VALIDATION-V2'
        result['historical_path_binding_fix'] = 'PASS' if result['status'] == 'PASS' else 'FAIL'
        out = root / r10.ROUND_DIR
        out.mkdir(parents=True, exist_ok=True)
        r10.write_json(out / 'validation.json', result)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 0 if result['status'] == 'PASS' else 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
