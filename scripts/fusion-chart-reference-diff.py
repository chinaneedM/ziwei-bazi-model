#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from fortune_training.fusion_chart_acceptance import compare_reference_snapshot


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare Wenmo/Wenzhen-style reference snapshots without promoting them to authority"
    )
    parser.add_argument("local", type=Path)
    parser.add_argument("reference", type=Path)
    parser.add_argument("--disputed-path", action="append", default=[])
    parser.add_argument("--expected-profile-path", action="append", default=[])
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    local = json.loads(args.local.read_text(encoding="utf-8"))
    reference = json.loads(args.reference.read_text(encoding="utf-8"))
    differences = compare_reference_snapshot(
        local,
        reference,
        disputed_paths=tuple(args.disputed_path),
        expected_profile_paths=tuple(args.expected_profile_path),
    )
    payload = {
        "schema": "FUSION-CHART-REFERENCE-DIFFERENTIAL-R1",
        "status": "DIFFERENCES_FOUND" if differences else "MATCH",
        "reference_role": "REFERENCE_IMPLEMENTATION_ONLY_NOT_CANONICAL_AUTHORITY",
        "difference_count": len(differences),
        "differences": [
            {
                "path": row.path,
                "local_value": row.local_value,
                "reference_value": row.reference_value,
                "classification": row.classification.value,
                "note": row.note,
            }
            for row in differences
        ],
        "automatic_algorithm_change_authorized": False,
    }
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(text, encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
