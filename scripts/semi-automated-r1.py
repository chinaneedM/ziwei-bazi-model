#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from fortune_v1.semi_automated import (
    classify_visibility_event,
    prepare_chat_packets,
    validate_chat_output,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="FORTUNE-V1-SEMI-AUTOMATED-R1")
    sub = parser.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare")
    prepare.add_argument("--clean-start", required=True)
    prepare.add_argument("--output-root", required=True)

    validate = sub.add_parser("validate")
    validate.add_argument("--packet", required=True)
    validate.add_argument("--chat-output", required=True)
    validate.add_argument("--validated-output", required=True)

    visibility = sub.add_parser("classify-visibility")
    visibility.add_argument("--operation-attempted", action="store_true")
    visibility.add_argument("--returned-payload-visible", action="store_true")
    visibility.add_argument("--forbidden-content-visible", action="store_true")
    visibility.add_argument("--answer-bearing-content-visible", action="store_true")

    args = parser.parse_args()
    if args.command == "prepare":
        result = prepare_chat_packets(args.clean_start, args.output_root)
    elif args.command == "validate":
        result = validate_chat_output(args.packet, args.chat_output, args.validated_output)
    else:
        result = classify_visibility_event(
            operation_attempted=args.operation_attempted,
            returned_payload_visible=args.returned_payload_visible,
            forbidden_content_visible=args.forbidden_content_visible,
            answer_bearing_content_visible=args.answer_bearing_content_visible,
        )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
