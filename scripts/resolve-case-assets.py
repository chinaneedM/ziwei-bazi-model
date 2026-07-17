#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--group-id", required=True)
    parser.add_argument("--registry", default="config/case-asset-registry.json")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    registry_path = ROOT / args.registry
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    if registry.get("schema") != "CASE-ASSET-REGISTRY-V1":
        raise SystemExit("invalid registry schema")

    resolved = []
    for case in registry.get("cases", []):
        if args.group_id in case.get("groups", []):
            resolved.append({
                "canonical_case_id": case["canonical_case_id"],
                "runtime_sha256": case["current_runtime_sha256"],
                "answer_lookup_key": case["canonical_case_id"],
                "answer_reuse": case["answer_reuse"],
            })

    if not resolved:
        raise SystemExit("group has no registered case assets")

    result = {
        "schema": "RESOLVED-CASE-ASSET-SET-V1",
        "group_id": args.group_id,
        "asset_set_id": registry["asset_set_id"],
        "case_count": len(resolved),
        "cases": resolved,
        "answer_binding": "CANONICAL_CASE_ID_NOT_GROUP_ID",
        "reupload_required": False,
        "status": "PASS",
    }
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
