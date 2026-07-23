from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .chat_input import write_chat_input
from .case_bank import case_bank_report, validate_case_bank
from .formal import (
    activate_formal_controller,
    import_answer_batch,
    rehearse_formal_no_reveal,
    verify_formal_answer_vault,
)
from .learning import public_learning_summary
from .transport import (
    bootstrap_answer_transport,
    finalize_answer_transport,
    seal_answer_batch,
)
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
from .verify import verify_repository


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
    verify_parser.add_argument("--require-answers", action="store_true", help="fail unless every case has an encrypted answer")

    subparsers.add_parser("status", help="show the current training state")
    subparsers.add_parser("report", help="show answer-free question-level learning metrics")
    subparsers.add_parser("case-bank-verify", help="verify the answer-free 107-case corpus")
    subparsers.add_parser("case-bank-report", help="show answer-free corpus coverage and quality")
    subparsers.add_parser("chat-input", help="rebuild the answer-isolated Chat prediction input")

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
    import_parser = subparsers.add_parser(
        "import-answer-batch",
        help="atomically validate and encrypt the complete 107-case answer batch",
    )
    import_parser.add_argument("plaintext_batch", type=Path)
    subparsers.add_parser(
        "verify-formal-answers",
        help="verify all formal answer envelopes without publishing mappings",
    )
    subparsers.add_parser(
        "activate-formal",
        help="atomically switch from the migration controller to formal development",
    )
    subparsers.add_parser(
        "rehearse-formal",
        help="verify the formal Chat bundle without starting or revealing a round",
    )
    subparsers.add_parser(
        "answer-transport-bootstrap",
        help="create a public import key while keeping its private key encrypted",
    )
    seal_parser = subparsers.add_parser(
        "answer-transport-seal",
        help="seal a repository-external plaintext answer batch for GitHub Actions",
    )
    seal_parser.add_argument("public_key", type=Path)
    seal_parser.add_argument("plaintext_batch", type=Path)
    seal_parser.add_argument("sealed_output", type=Path)
    subparsers.add_parser(
        "answer-transport-finalize",
        help="decrypt the sealed batch inside Actions, import, activate, and rehearse",
    )
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
            _print_json(verify_repository(root, require_answers=args.require_answers))
        elif args.command == "status":
            _print_json(status(root))
        elif args.command == "report":
            _print_json(public_learning_summary(root))
        elif args.command == "case-bank-verify":
            _print_json(validate_case_bank(root))
        elif args.command == "case-bank-report":
            _print_json(case_bank_report(root))
        elif args.command == "chat-input":
            _print_json(write_chat_input(root))
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
        elif args.command == "import-answer-batch":
            _print_json(import_answer_batch(root, args.plaintext_batch))
        elif args.command == "verify-formal-answers":
            _print_json(verify_formal_answer_vault(root))
        elif args.command == "activate-formal":
            _print_json(activate_formal_controller(root))
        elif args.command == "rehearse-formal":
            _print_json(rehearse_formal_no_reveal(root))
        elif args.command == "answer-transport-bootstrap":
            _print_json(bootstrap_answer_transport(root))
        elif args.command == "answer-transport-seal":
            _print_json(
                seal_answer_batch(
                    root,
                    args.public_key,
                    args.plaintext_batch,
                    args.sealed_output,
                )
            )
        elif args.command == "answer-transport-finalize":
            _print_json(finalize_answer_transport(root))
        else:
            parser.error(f"unknown command: {args.command}")
    except TrainingError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
