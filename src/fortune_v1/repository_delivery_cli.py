from __future__ import annotations

import argparse
import json

from .causal_use import build_run_contract, validate_causal_use
from .composite_release import materialize_knowledge_release
from .contamination import build_contamination_inventory, validate_runtime_object
from .repository_release import (
    build_knowledge_manifest, build_method_packet, build_model_release,
    rollback_release, validate_knowledge_manifest, validate_method_release,
)
from .source_delivery import build_source_catalog, build_source_packet
from .util import FortuneError, atomic_write_json, read_json


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="fortune-repository-delivery")
    sub = p.add_subparsers(dest="command", required=True)
    def cmd(name: str, *args: tuple[str, dict]):
        q = sub.add_parser(name)
        for flag, kwargs in args: q.add_argument(flag, **kwargs)
    cmd("knowledge-manifest", ("--source-dir", {"required": True}), ("--output", {"required": True}),
        ("--release-id", {"required": True}), ("--repository", {"required": True}),
        ("--commit", {"required": True}), ("--s19-binding-sha256", {"required": True}),
        ("--release-kind", {"default": "CANDIDATE"}), ("--parent-release-id", {}))
    cmd("knowledge-validate", ("--manifest", {"required": True}), ("--source-dir", {}),
        ("--output", {"required": True}))
    cmd("knowledge-materialize", ("--manifest", {"required": True}),
        ("--repository-root", {"required": True}), ("--output-dir", {"required": True}),
        ("--receipt", {"required": True}))
    cmd("method-validate", ("--method", {"required": True}), ("--output", {"required": True}))
    cmd("method-packet", ("--method", {"required": True}), ("--output", {"required": True}))
    cmd("source-catalog", ("--manifest", {"required": True}), ("--source-dir", {"required": True}),
        ("--output", {"required": True}))
    cmd("source-packet", ("--catalog", {"required": True}), ("--coverage-plan", {"required": True}),
        ("--case-freeze", {"required": True}), ("--output", {"required": True}))
    cmd("model-release", ("--knowledge-manifest", {"required": True}),
        ("--method", {"required": True}), ("--prompt-snapshot-receipt", {"required": True}),
        ("--output", {"required": True}), ("--model-release-id", {"required": True}),
        ("--main-prompt-runtime-id", {"required": True}), ("--code-commit", {"required": True}))
    cmd("run-contract", ("--model-release", {"required": True}),
        ("--source-packet", {"required": True}), ("--method-packet", {"required": True}),
        ("--case-freeze", {"required": True}), ("--questions", {"required": True}),
        ("--output", {"required": True}), ("--run-id", {"required": True}),
        ("--case-id", {"required": True}), ("--dataset-type", {"required": True}))
    cmd("causal-validate", ("--prediction", {"required": True}),
        ("--contract", {"required": True}), ("--output", {"required": True}))
    cmd("contamination-inventory", ("--repository-root", {"required": True}),
        ("--output", {"required": True}))
    cmd("contamination-validate", ("--input", {"required": True}),
        ("--output", {"required": True}))
    cmd("rollback", ("--target-manifest", {"required": True}),
        ("--active-pointer", {"required": True}), ("--receipt", {"required": True}),
        ("--reason", {"required": True}), ("--approval-id", {"required": True}))
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "knowledge-manifest":
            result = build_knowledge_manifest(args.source_dir, args.output, release_id=args.release_id,
                repository=args.repository, commit_sha=args.commit,
                s19_binding_sha256=args.s19_binding_sha256,
                release_kind=args.release_kind, parent_release_id=args.parent_release_id)
        elif args.command == "knowledge-validate":
            result = validate_knowledge_manifest(args.manifest, args.source_dir)
            atomic_write_json(args.output, result, overwrite=True)
        elif args.command == "knowledge-materialize":
            result = materialize_knowledge_release(
                args.manifest, args.repository_root, args.output_dir, args.receipt,
            )
        elif args.command == "method-validate":
            result = validate_method_release(args.method); atomic_write_json(args.output, result, overwrite=True)
        elif args.command == "method-packet": result = build_method_packet(args.method, args.output)
        elif args.command == "source-catalog": result = build_source_catalog(args.manifest, args.source_dir, args.output)
        elif args.command == "source-packet": result = build_source_packet(args.catalog, args.coverage_plan, args.case_freeze, args.output)
        elif args.command == "model-release": result = build_model_release(
            args.knowledge_manifest, args.method, args.prompt_snapshot_receipt, args.output,
            model_release_id=args.model_release_id, main_prompt_runtime_id=args.main_prompt_runtime_id,
            code_commit_sha=args.code_commit)
        elif args.command == "run-contract":
            questions = read_json(args.questions); questions = questions.get("questions", questions)
            result = build_run_contract(args.model_release, args.source_packet, args.method_packet,
                args.case_freeze, args.output, run_id=args.run_id, case_id=args.case_id,
                dataset_type=args.dataset_type, question_rows=questions)
        elif args.command == "causal-validate": result = validate_causal_use(args.prediction, args.contract, args.output)
        elif args.command == "contamination-inventory": result = build_contamination_inventory(args.repository_root, args.output)
        elif args.command == "contamination-validate": result = validate_runtime_object(args.input, args.output)
        elif args.command == "rollback": result = rollback_release(args.target_manifest, args.active_pointer,
            args.receipt, reason=args.reason, approval_id=args.approval_id)
        else: raise AssertionError(args.command)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)); return 0
    except FortuneError as exc:
        print(json.dumps({"status": exc.status, "error": str(exc)}, ensure_ascii=False)); return 2


if __name__ == "__main__": raise SystemExit(main())
