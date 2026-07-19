from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .runtime import (
    apply_learning,
    encrypt_answer,
    freeze_prediction,
    generate_key,
    score_round,
    start_round,
    status,
)
from .util import TrainingError
from .verify import build_source_manifest, verify_repository


def _repo_root(value: str | None) -> Path:
    if value:
        root = Path(value).resolve()
        if not (root / "config" / "training-policy.json").is_file():
            raise TrainingError(f"not a training repository: {root}")
        return root
    candidate = Path.cwd().resolve()
    for path in (candidate, *candidate.parents):
        if (path / "config" / "training-policy.json").is_file():
            return path
    raise TrainingError("run inside the repository or pass --root")


def _print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Case-by-case fortune prediction training controller")
    parser.add_argument("--root", help="repository root (defaults to current repository)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    verify_parser = subparsers.add_parser("verify", help="verify the clean repository baseline")
    verify_parser.add_argument("--write-manifest", action="store_true", help="rebuild sources/manifest.json first")
    verify_parser.add_argument("--require-answers", action="store_true", help="fail unless every case has an encrypted answer")

    subparsers.add_parser("status", help="show the current training state")

    start_parser = subparsers.add_parser("start", help="start a new round for the current case")
    start_parser.add_argument("round_id")

    freeze_parser = subparsers.add_parser("freeze", help="freeze one complete prediction payload")
    freeze_parser.add_argument("round_id")
    freeze_parser.add_argument("prediction_file", type=Path)

    score_parser = subparsers.add_parser("score", help="score a frozen prediction")
    score_parser.add_argument("round_id")
    score_parser.add_argument("--review-output", required=True, type=Path)
    score_parser.add_argument(
        "--answer-file",
        type=Path,
        help="trusted plaintext answer file outside the repository; read only after freeze",
    )

    learn_parser = subparsers.add_parser("learn", help="activate a general learning patch after a failed round")
    learn_parser.add_argument("round_id")
    learn_parser.add_argument("patch_file", type=Path)
    learn_parser.add_argument("release_id")

    subparsers.add_parser("keygen", help="print a new answer encryption key")

    encrypt_parser = subparsers.add_parser("encrypt-answer", help="encrypt a trusted answer file from outside the repository")
    encrypt_parser.add_argument("case_id")
    encrypt_parser.add_argument("plaintext_file", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "keygen":
            print(generate_key())
            return 0
        root = _repo_root(args.root)
        if args.command == "verify":
            if args.write_manifest:
                build_source_manifest(root, write=True)
            _print_json(verify_repository(root, require_answers=args.require_answers))
        elif args.command == "status":
            _print_json(status(root))
        elif args.command == "start":
            _print_json(start_round(root, args.round_id))
        elif args.command == "freeze":
            _print_json(freeze_prediction(root, args.round_id, args.prediction_file))
        elif args.command == "score":
            _print_json(score_round(root, args.round_id, args.review_output, answer_file=args.answer_file))
        elif args.command == "learn":
            _print_json(apply_learning(root, args.round_id, args.patch_file, args.release_id))
        elif args.command == "encrypt-answer":
            destination = encrypt_answer(root, args.case_id, args.plaintext_file)
            _print_json({"status": "ENCRYPTED", "path": destination.relative_to(root).as_posix()})
        else:
            parser.error(f"unknown command: {args.command}")
    except TrainingError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
