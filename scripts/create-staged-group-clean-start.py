#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from fortune_v1.bootstrap_request import (
    build_preauthorized_request,
    create_group_clean_start_from_bootstrap_request,
)
from fortune_v1.clean_start import create_group_clean_start, record_group_contamination
from fortune_v1.staged_access import harden_clean_start


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create")
    create.add_argument("--group-manifest", required=True)
    create.add_argument("--install-state", required=True)
    create.add_argument("--output-root", required=True)
    create.add_argument("--group-run-id", required=True)
    create.add_argument("--session-id", required=True)
    create.add_argument("--mode", choices=["CHAT_ONLY", "WORK"], default="CHAT_ONLY")

    prepare_request = sub.add_parser("prepare-request")
    prepare_request.add_argument("--current-group-manifest", default="CURRENT_GROUP_MANIFEST")
    prepare_request.add_argument("--output", required=True)
    prepare_request.add_argument("--group-run-id", required=True)
    prepare_request.add_argument("--session-id", required=True)
    prepare_request.add_argument("--mode", choices=["CHAT_ONLY", "WORK"], default="CHAT_ONLY")
    prepare_request.add_argument("--run-purpose", choices=["FIRST_BLIND", "TRAINING_REPLAY"], default="FIRST_BLIND")

    create_request = sub.add_parser("create-from-request")
    create_request.add_argument("--request", required=True)
    create_request.add_argument("--current-group-manifest", default="CURRENT_GROUP_MANIFEST")
    create_request.add_argument("--runtime-preflight-receipt")

    contaminate = sub.add_parser("contaminate")
    contaminate.add_argument("--clean-start", required=True)
    contaminate.add_argument("--output", required=True)
    contaminate.add_argument("--resource-type", required=True)
    contaminate.add_argument("--resource-reference", required=True)

    args = parser.parse_args()
    if args.command == "create":
        legacy = create_group_clean_start(
            args.group_manifest,
            args.install_state,
            args.output_root,
            args.group_run_id,
            args.session_id,
            args.mode,
            args.run_purpose,
        )
        result = harden_clean_start(legacy)
    elif args.command == "prepare-request":
        result = build_preauthorized_request(
            args.current_group_manifest,
            args.output,
            args.group_run_id,
            args.session_id,
            args.mode,
        )
    elif args.command == "create-from-request":
        legacy = create_group_clean_start_from_bootstrap_request(
            args.request,
            args.current_group_manifest,
            args.runtime_preflight_receipt,
        )
        result = harden_clean_start(legacy)
    else:
        result = record_group_contamination(
            args.clean_start,
            args.output,
            args.resource_type,
            args.resource_reference,
        )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
