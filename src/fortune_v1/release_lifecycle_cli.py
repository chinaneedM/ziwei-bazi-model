from __future__ import annotations

import argparse
import json

from .method_release_lifecycle import promote_method_candidate, rollback_method_release
from .repository_release import promote_candidate, rollback_release
from .util import FortuneError


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="fortune-release-lifecycle")
    sub = p.add_subparsers(dest="command", required=True)

    def cmd(name: str, *args: tuple[str, dict]):
        q = sub.add_parser(name)
        for flag, kwargs in args:
            q.add_argument(flag, **kwargs)

    cmd("knowledge-promote", ("--candidate-dir", {"required": True}),
        ("--manifest", {"required": True}), ("--releases-root", {"required": True}),
        ("--active-pointer", {"required": True}), ("--receipt", {"required": True}),
        ("--approval-id", {"required": True}), ("--expected-previous-release-id", {}))
    cmd("knowledge-rollback", ("--target-manifest", {"required": True}),
        ("--active-pointer", {"required": True}), ("--receipt", {"required": True}),
        ("--reason", {"required": True}), ("--approval-id", {"required": True}))
    cmd("method-promote", ("--method", {"required": True}),
        ("--releases-root", {"required": True}), ("--active-pointer", {"required": True}),
        ("--receipt", {"required": True}), ("--approval-id", {"required": True}),
        ("--expected-previous-release-id", {}))
    cmd("method-rollback", ("--target-method", {"required": True}),
        ("--active-pointer", {"required": True}), ("--receipt", {"required": True}),
        ("--reason", {"required": True}), ("--approval-id", {"required": True}))
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "knowledge-promote":
            result = promote_candidate(
                args.candidate_dir, args.manifest, args.releases_root,
                args.active_pointer, args.receipt, approval_id=args.approval_id,
                expected_previous_release_id=args.expected_previous_release_id,
            )
        elif args.command == "knowledge-rollback":
            result = rollback_release(
                args.target_manifest, args.active_pointer, args.receipt,
                reason=args.reason, approval_id=args.approval_id,
            )
        elif args.command == "method-promote":
            result = promote_method_candidate(
                args.method, args.releases_root, args.active_pointer,
                args.receipt, approval_id=args.approval_id,
                expected_previous_release_id=args.expected_previous_release_id,
            )
        elif args.command == "method-rollback":
            result = rollback_method_release(
                args.target_method, args.active_pointer, args.receipt,
                reason=args.reason, approval_id=args.approval_id,
            )
        else:
            raise AssertionError(args.command)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    except FortuneError as exc:
        print(json.dumps({"status": exc.status, "error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
