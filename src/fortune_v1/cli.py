from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .audit import audit_sources, import_source_package, migrate_verified_sources
from .bazi import freeze_transcription
from .blind_track import create_local_track_seal, seal_blind_track_model
from .diagnosis import classify_errors, create_interface_patch_candidate
from .external_runner import freeze_chat_work_prediction, import_chat_work_prediction
from .group import (
    authorize_group_reveal,
    create_dev_group,
    record_patch_round,
    register_baseline_freeze,
    validate_group_reveal_authorization,
)
from .group_runner import execute_group_handoff, validate_group_training_freeze
from .ingest import ingest_zip
from .install_state import finalize_installation_state, validate_installation_state
from .knowledge import build_locator_index, read_parent_segment, validate_locator_index
from .patching import scan_patch
from .prediction import prepare_run_contract
from .prompt_snapshot import create_prompt_snapshot
from .regression import execute_regression, select_regression
from .reporting import installation_check, render_markdown
from .scoring import grade_frozen_prediction, validate_freeze_receipt
from .snapshot import freeze_static_cache, generate_prediction_snapshot
from .state import transition
from .topology import verify_topology
from .util import FortuneError, atomic_write_json, read_json


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="fortune-v1")
    sub = p.add_subparsers(dest="command", required=True)

    def cmd(name: str, *args: tuple[str, dict]):
        q = sub.add_parser(name)
        for flag, kwargs in args:
            q.add_argument(flag, **kwargs)
        return q

    cmd("audit-sources", ("--source-dir", {"required": True}), ("--config", {"required": True}),
        ("--output", {"required": True}), ("--code-commit", {}))
    cmd("import-source-package", ("--package", {"required": True}),
        ("--expected-zip-sha256", {"required": True}), ("--config", {"required": True}),
        ("--work-root", {"required": True}), ("--reports-dir", {"required": True}),
        ("--migrate-destination", {}), ("--code-commit", {}))
    cmd("migrate-sources", ("--audit", {"required": True}), ("--destination", {"required": True}))
    cmd("prompt-snapshot", ("--runtime-id", {"required": True}), ("--prompt-file", {"required": True}),
        ("--destination", {"required": True}), ("--config", {}))
    cmd("ingest", ("--package", {"required": True}), ("--runtime-root", {"required": True}),
        ("--vault-root", {"required": True}),
        ("--dataset-type", {"required": True, "choices": ["DEV", "REGRESSION", "FROZEN_EVAL"]}))
    cmd("bazi-freeze", ("--case-id", {"required": True}), ("--image", {"required": True}),
        ("--transcription", {"required": True}), ("--output", {"required": True}),
        ("--method", {"default": "HUMAN_VERIFIED_ENTRY"}), ("--method-version", {"default": "1"}))
    cmd("snapshot", ("--case", {"required": True}), ("--output-root", {"required": True}),
        ("--bazi-transcription", {}))
    cmd("cache-freeze", ("--snapshot", {"required": True}), ("--static-object", {"required": True}),
        ("--binding-hash", {"required": True}), ("--schema-version", {"required": True}),
        ("--cache-root", {"required": True}))
    cmd("prepare-run", ("--snapshot", {"required": True}), ("--config", {"required": True}),
        ("--code-commit", {"required": True}), ("--output", {"required": True}),
        ("--prompt-snapshot-sha256", {}))
    cmd("blind-track-seal", ("--candidate", {"required": True}), ("--frozen-root", {"required": True}))
    cmd("local-track-seal", ("--adjudication", {"required": True}),
        ("--blind-receipt", {"required": True}), ("--output", {"required": True}))
    cmd("chat-work-import", ("--run", {"required": True}), ("--contract", {"required": True}),
        ("--mode", {"required": True, "choices": ["CHAT_ONLY", "WORK"]}),
        ("--session-id", {"required": True}), ("--output", {"required": True}),
        ("--receipt", {"required": True}))
    cmd("freeze", ("--run", {"required": True}), ("--contract", {"required": True}),
        ("--handoff-receipt", {"required": True}), ("--frozen-root", {"required": True}))
    cmd("group-chat-work-run", ("--manifest", {"required": True}),
        ("--group-root", {"required": True}), ("--output-root", {"required": True}),
        ("--mode", {"required": True, "choices": ["CHAT_ONLY", "WORK"]}),
        ("--session-id", {"required": True}), ("--group-run-id", {"required": True}))
    cmd("group-verify-freeze", ("--group-freeze", {"required": True}),
        ("--group-run-id", {}), ("--output", {"required": True}))
    cmd("grade", ("--freeze-receipt", {"required": True}), ("--answer", {"required": True}),
        ("--output", {"required": True}), ("--gates", {}), ("--run-id", {}))
    cmd("verify-freeze", ("--freeze-receipt", {"required": True}),
        ("--run-id", {"required": True}), ("--output", {"required": True}))
    cmd("scan-patch", ("--patch", {"required": True}), ("--output", {"required": True}),
        ("--case-fingerprint", {}))
    cmd("index", ("--source-dir", {"required": True}), ("--binding-hash", {"required": True}),
        ("--output", {"required": True}), ("--git-commit", {}))
    cmd("source-read", ("--index", {"required": True}), ("--entry-id", {"required": True}),
        ("--output", {"required": True}))
    cmd("index-validate", ("--index", {"required": True}), ("--output", {"required": True}))
    cmd("regression-select", ("--manifest", {"required": True}),
        ("--affected-tag", {"action": "append", "default": []}),
        ("--full", {"action": "store_true"}), ("--output", {"required": True}))
    cmd("regress", ("--selection", {"required": True}), ("--runner", {}),
        ("--candidate-version", {"required": True}), ("--frozen-version", {"required": True}),
        ("--baseline-results", {}), ("--output", {"required": True}))
    cmd("state", ("--log", {"required": True}),
        ("--machine", {"required": True, "choices": ["DEV", "FROZEN_EVAL", "RELEASE"]}),
        ("--object-id", {"required": True}), ("--to", {"required": True}), ("--evidence", {}))
    cmd("install-check", ("--repo-root", {"required": True}), ("--source-audit", {}),
        ("--binding-receipt", {}), ("--migration-receipt", {}), ("--prompt-snapshot", {}),
        ("--test-report", {}), ("--topology-receipt", {}), ("--answer-workflow-receipt", {}),
        ("--external-runner", {}), ("--code-commit", {}), ("--output", {"required": True}))
    cmd("install-finalize", ("--install-receipt", {"required": True}),
        ("--code-commit", {"required": True}), ("--output", {"required": True}))
    cmd("install-validate", ("--seal", {"required": True}), ("--install-receipt", {"required": True}),
        ("--code-commit", {"required": True}), ("--output", {"required": True}))
    cmd("verify-topology", ("--config", {"required": True}), ("--output", {"required": True}))
    cmd("report", ("--input", {"action": "append", "required": True}), ("--output", {"required": True}))
    cmd("group-create", ("--group-id", {"required": True}),
        ("--case-id", {"action": "append", "required": True}), ("--binding", {"required": True}),
        ("--root", {"required": True}), ("--expected-size", {"type": int, "default": 5}))
    cmd("group-register-freeze", ("--group-root", {"required": True}),
        ("--freeze-receipt", {"required": True}))
    cmd("group-authorize-reveal", ("--group-root", {"required": True}))
    cmd("group-verify-reveal", ("--group-root", {"required": True}),
        ("--case-id", {"required": True}), ("--run-id", {"required": True}),
        ("--output", {"required": True}))
    cmd("group-patch-round", ("--group-root", {"required": True}),
        ("--net-improvement", {"type": int, "required": True}),
        ("--regression-damage", {"type": int, "required": True}),
        ("--defect-id", {"required": True}), ("--case-specific-only", {"action": "store_true"}),
        ("--base-change-required", {"action": "store_true"}))
    cmd("diagnose", ("--reveal", {"required": True}), ("--prediction", {"required": True}),
        ("--output", {"required": True}))
    cmd("patch-candidate", ("--diagnosis", {"required": True}),
        ("--defect-id", {"action": "append", "required": True}), ("--layer", {"required": True}),
        ("--parent-chain", {"required": True}), ("--changes", {"required": True}),
        ("--output", {"required": True}))
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        c = args.command
        if c == "audit-sources":
            result = audit_sources(args.source_dir, args.config, args.output, commit_sha=args.code_commit)
        elif c == "import-source-package":
            result = import_source_package(args.package, args.expected_zip_sha256, args.config,
                                           args.work_root, args.reports_dir,
                                           args.migrate_destination, commit_sha=args.code_commit)
        elif c == "migrate-sources":
            result = migrate_verified_sources(args.audit, args.destination)
        elif c == "prompt-snapshot":
            prompt_config = read_json(args.config) if args.config else {}
            result = create_prompt_snapshot(
                args.runtime_id, args.prompt_file, args.destination,
                expected_sha256=prompt_config.get("expected_main_prompt_sha256_raw_bytes"),
                expected_bytes=prompt_config.get("expected_main_prompt_size_bytes"),
                expected_visible_characters=prompt_config.get("expected_main_prompt_visible_character_count"))
        elif c == "ingest":
            result = ingest_zip(args.package, args.runtime_root, args.vault_root, args.dataset_type)
        elif c == "bazi-freeze":
            result = freeze_transcription(args.case_id, args.image, args.transcription,
                                          args.output, args.method, args.method_version)
        elif c == "snapshot":
            result = generate_prediction_snapshot(args.case, args.output_root, args.bazi_transcription)
        elif c == "cache-freeze":
            result = freeze_static_cache(args.snapshot, args.static_object, args.binding_hash,
                                         args.schema_version, args.cache_root)
        elif c == "prepare-run":
            result = prepare_run_contract(args.snapshot, args.config, args.code_commit,
                                          args.output, args.prompt_snapshot_sha256)
        elif c == "blind-track-seal":
            result = seal_blind_track_model(args.candidate, args.frozen_root)
        elif c == "local-track-seal":
            result = create_local_track_seal(args.adjudication, args.blind_receipt, args.output)
        elif c == "chat-work-import":
            result = import_chat_work_prediction(args.run, args.contract, args.output,
                                                 args.receipt, args.mode, args.session_id)
        elif c == "freeze":
            result = freeze_chat_work_prediction(args.run, args.contract,
                                                 args.handoff_receipt, args.frozen_root)
        elif c == "group-chat-work-run":
            result = execute_group_handoff(args.manifest, args.group_root, args.output_root,
                                           args.mode, args.session_id, args.group_run_id)
        elif c == "group-verify-freeze":
            result = validate_group_training_freeze(args.group_freeze, args.group_run_id)
            atomic_write_json(args.output, result)
        elif c == "grade":
            result = grade_frozen_prediction(args.freeze_receipt, args.answer, args.output,
                                             read_json(args.gates) if args.gates else None, args.run_id)
        elif c == "verify-freeze":
            result = validate_freeze_receipt(args.freeze_receipt, args.run_id)
            atomic_write_json(args.output, result)
        elif c == "scan-patch":
            result = scan_patch(args.patch, args.output, args.case_fingerprint)
        elif c == "index":
            result = build_locator_index(args.source_dir, args.binding_hash, args.output, args.git_commit)
        elif c == "source-read":
            result = read_parent_segment(args.index, args.entry_id)
            atomic_write_json(args.output, result)
        elif c == "index-validate":
            result = validate_locator_index(args.index, args.output)
        elif c == "regression-select":
            result = select_regression(args.manifest, args.affected_tag, args.full)
            atomic_write_json(args.output, result)
        elif c == "regress":
            result = execute_regression(read_json(args.selection), args.runner,
                                        args.candidate_version, args.frozen_version,
                                        args.output, args.baseline_results)
        elif c == "state":
            result = transition(args.log, args.machine, args.object_id, args.to,
                                read_json(args.evidence) if args.evidence else None)
        elif c == "install-check":
            result = installation_check(args.repo_root, args.source_audit, args.prompt_snapshot,
                                        args.test_report, args.topology_receipt, args.external_runner,
                                        args.output, args.binding_receipt, args.migration_receipt,
                                        args.answer_workflow_receipt, args.code_commit)
        elif c == "install-finalize":
            result = finalize_installation_state(args.install_receipt, args.code_commit, args.output)
        elif c == "install-validate":
            result = validate_installation_state(args.seal, args.install_receipt, args.code_commit)
            atomic_write_json(args.output, result, overwrite=True)
        elif c == "verify-topology":
            result = verify_topology(args.config, args.output)
        elif c == "report":
            result = {"output": str(render_markdown(args.input, args.output))}
        elif c == "group-create":
            result = create_dev_group(args.group_id, args.case_id, read_json(args.binding),
                                      args.root, args.expected_size)
        elif c == "group-register-freeze":
            result = register_baseline_freeze(args.group_root, args.freeze_receipt)
        elif c == "group-authorize-reveal":
            result = authorize_group_reveal(args.group_root)
        elif c == "group-verify-reveal":
            result = validate_group_reveal_authorization(args.group_root, args.case_id, args.run_id)
            atomic_write_json(args.output, result)
        elif c == "group-patch-round":
            result = record_patch_round(args.group_root, args.net_improvement,
                                        args.regression_damage, args.defect_id,
                                        args.case_specific_only, args.base_change_required)
        elif c == "diagnose":
            result = classify_errors(args.reveal, args.prediction, args.output)
        elif c == "patch-candidate":
            result = create_interface_patch_candidate(args.diagnosis, args.defect_id,
                                                      args.layer, read_json(args.parent_chain),
                                                      read_json(args.changes), args.output)
        else:
            raise AssertionError(c)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    except FortuneError as exc:
        print(json.dumps({"status": exc.status, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
