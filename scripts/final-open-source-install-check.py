#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ARCHITECTURE_MERGE_COMMIT = "99ae5d73c22cff1d09e06161ac867368981be5c7"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def object_hash(value: dict[str, Any]) -> str:
    body = dict(value)
    body.pop("object_hash", None)
    return hashlib.sha256(canonical_bytes(body)).hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run(root: Path, command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=root, capture_output=True, text=True, check=False)


def git_output(root: Path, *args: str) -> str:
    proc = run(root, ["git", *args])
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout.strip()


def check_row(name: str, passed: bool, *, path: Path | None, actual: Any, expected: Any) -> dict[str, Any]:
    return {
        "check": name,
        "status": "PASS" if passed else "FAIL",
        "path": path.as_posix() if path else None,
        "file_sha256": sha256(path) if path and path.is_file() else None,
        "actual": actual,
        "expected": expected,
    }


def invoke_json_verifier(root: Path, script: str, visibility: str) -> tuple[dict[str, Any] | None, str | None]:
    proc = run(root, [sys.executable, script, "--root", ".", "--visibility", visibility])
    if proc.returncode not in {0, 2}:
        return None, proc.stderr.strip() or proc.stdout.strip()
    try:
        return json.loads(proc.stdout), None
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON from {script}: {exc}"


def verify(
    root: Path,
    visibility: str,
    expected_commit: str,
    activation_mode: str,
    tests_passed: bool,
    output: Path | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    checks: list[dict[str, Any]] = []
    current_commit = git_output(root, "rev-parse", "HEAD")
    ref_name = os.environ.get("GITHUB_REF_NAME") or git_output(root, "branch", "--show-current")

    checks.append(check_row(
        "EXACT_COMMIT",
        current_commit == expected_commit,
        path=None,
        actual=current_commit,
        expected=expected_commit,
    ))
    checks.append(check_row(
        "PUBLIC_REPOSITORY_VISIBILITY",
        visibility == "public",
        path=None,
        actual=visibility,
        expected="public",
    ))

    ancestor = run(root, ["git", "merge-base", "--is-ancestor", ARCHITECTURE_MERGE_COMMIT, current_commit]).returncode == 0
    checks.append(check_row(
        "PR36_ARCHITECTURE_MERGED",
        ancestor,
        path=None,
        actual={"current_commit": current_commit, "architecture_merge_commit": ARCHITECTURE_MERGE_COMMIT},
        expected="architecture merge commit is ancestor of current commit",
    ))

    tests_actual = {
        "same_make_target": tests_passed,
        "commands": ["python -m unittest discover -s tests -v", "python -m pytest -q"],
    }
    checks.append(check_row(
        "COMPLETE_TEST_SUITES_IN_SAME_INSTALL_CHECK",
        tests_passed,
        path=None,
        actual=tests_actual,
        expected={"same_make_target": True},
    ))

    public_policy, public_error = invoke_json_verifier(root, "scripts/verify-public-only-repository.py", visibility)
    public_pass = bool(public_policy and public_policy.get("status") == "PASS")
    checks.append(check_row(
        "PUBLIC_ONLY_REPOSITORY_POLICY",
        public_pass,
        path=root / "config/public-repository-policy.json",
        actual=public_policy if public_policy is not None else public_error,
        expected={"status": "PASS", "project_mode": "COMPLETE_OPEN_SOURCE"},
    ))

    release_policy, release_error = invoke_json_verifier(root, "scripts/verify-open-source-release.py", visibility)
    release_pass = bool(
        release_policy
        and release_policy.get("status") == "PASS"
        and release_policy.get("active_knowledge_release_id") == "KNOWLEDGE-R17"
        and release_policy.get("checked_manifest_count") == 1
        and release_policy.get("checked_knowledge_file_count") == 20
        and release_policy.get("failure_count") == 0
    )
    checks.append(check_row(
        "ACTIVE_KNOWLEDGE_R17_CC0_RELEASE",
        release_pass,
        path=root / "config/open-source-release.json",
        actual=release_policy if release_policy is not None else release_error,
        expected={
            "status": "PASS",
            "active_knowledge_release_id": "KNOWLEDGE-R17",
            "checked_manifest_count": 1,
            "checked_knowledge_file_count": 20,
            "failure_count": 0,
        },
    ))

    active_pointer_path = root / "knowledge/active-release.json"
    active_pointer = read_json(active_pointer_path)
    pointer_pass = (
        active_pointer.get("schema") == "FORTUNE-ACTIVE-KNOWLEDGE-RELEASE-POINTER-V1"
        and active_pointer.get("formal_release") == "YES"
        and active_pointer.get("knowledge_release_id") == "KNOWLEDGE-R17"
        and active_pointer.get("manifest_path") == "knowledge/releases/KNOWLEDGE-R17/release-manifest.json"
    )
    checks.append(check_row(
        "ACTIVE_KNOWLEDGE_POINTER",
        pointer_pass,
        path=active_pointer_path,
        actual={key: active_pointer.get(key) for key in ("schema", "formal_release", "knowledge_release_id", "manifest_path")},
        expected={
            "schema": "FORTUNE-ACTIVE-KNOWLEDGE-RELEASE-POINTER-V1",
            "formal_release": "YES",
            "knowledge_release_id": "KNOWLEDGE-R17",
            "manifest_path": "knowledge/releases/KNOWLEDGE-R17/release-manifest.json",
        },
    ))

    rights_receipt_path = root / "reports/open-source-migration/knowledge-rights/KNOWLEDGE-R17-CC0-20260719-01-materialization-receipt.json"
    rights_receipt = read_json(rights_receipt_path)
    rights_pass = (
        rights_receipt.get("schema") == "ACTIVE-KNOWLEDGE-CC0-MATERIALIZATION-RECEIPT-V1"
        and rights_receipt.get("status") == "PASS"
        and rights_receipt.get("active_knowledge_release_id") == "KNOWLEDGE-R17"
        and rights_receipt.get("license_expression") == "CC0-1.0"
        and rights_receipt.get("checked_file_count") == 20
        and rights_receipt.get("public_distribution_allowed") is True
    )
    checks.append(check_row(
        "KNOWLEDGE_RIGHTS_MATERIALIZATION",
        rights_pass,
        path=rights_receipt_path,
        actual={key: rights_receipt.get(key) for key in (
            "schema", "status", "active_knowledge_release_id", "license_expression",
            "checked_file_count", "public_distribution_allowed", "object_hash")},
        expected={
            "status": "PASS",
            "active_knowledge_release_id": "KNOWLEDGE-R17",
            "license_expression": "CC0-1.0",
            "checked_file_count": 20,
            "public_distribution_allowed": True,
        },
    ))

    rights_verify_path = root / "reports/open-source-migration/knowledge-rights/open-source-release-verification.json"
    rights_verify = read_json(rights_verify_path)
    rights_verify_pass = (
        rights_verify.get("status") == "PASS"
        and rights_verify.get("active_knowledge_release_id") == "KNOWLEDGE-R17"
        and rights_verify.get("checked_knowledge_file_count") == 20
        and rights_verify.get("checked_manifest_count") == 1
        and rights_verify.get("failure_count") == 0
    )
    checks.append(check_row(
        "KNOWLEDGE_RIGHTS_VERIFICATION",
        rights_verify_pass,
        path=rights_verify_path,
        actual=rights_verify,
        expected={"status": "PASS", "checked_knowledge_file_count": 20, "checked_manifest_count": 1, "failure_count": 0},
    ))

    public_execution_path = root / "reports/open-source-migration/public-execution-validation-20260719T162000JST.json"
    public_execution = read_json(public_execution_path)
    actions = public_execution.get("github_actions") if isinstance(public_execution.get("github_actions"), dict) else {}
    action_pass = bool(actions) and all(
        isinstance(value, dict) and value.get("conclusion") == "success"
        for value in actions.values()
    )
    public_execution_pass = (
        public_execution.get("status") == "PASS_PUBLIC_CI_AND_SYNTHETIC_E2E"
        and public_execution.get("repository_visibility") == "public"
        and public_execution.get("private_repository_dependency") is False
        and action_pass
    )
    checks.append(check_row(
        "PUBLIC_EXECUTION_VALIDATION",
        public_execution_pass,
        path=public_execution_path,
        actual={
            "status": public_execution.get("status"),
            "repository_visibility": public_execution.get("repository_visibility"),
            "private_repository_dependency": public_execution.get("private_repository_dependency"),
            "github_actions": actions,
        },
        expected={"status": "PASS_PUBLIC_CI_AND_SYNTHETIC_E2E", "repository_visibility": "public", "all_actions": "success"},
    ))

    key_path = root / "reports/open-source-migration/public-answer-key-smoke/PUBLIC-KEY-SMOKE-20260719-01.json"
    key_receipt = read_json(key_path)
    key_pass = (
        key_receipt.get("status") == "PASS"
        and key_receipt.get("secret_present") is True
        and key_receipt.get("fernet_key_accepted") is True
        and key_receipt.get("synthetic_roundtrip") == "PASS"
        and key_receipt.get("secret_value_recorded") is False
        and key_receipt.get("secret_fingerprint_recorded") is False
        and key_receipt.get("plaintext_answer_used") is False
    )
    checks.append(check_row(
        "PUBLIC_ANSWER_KEY_RUNTIME_SMOKE",
        key_pass,
        path=key_path,
        actual=key_receipt,
        expected={"status": "PASS", "fernet_key_accepted": True, "secret_value_recorded": False},
    ))

    synthetic_path = root / "reports/open-source-migration/public-synthetic-e2e/PUBLIC-SYNTHETIC-E2E-20260719-01.json"
    synthetic = read_json(synthetic_path)
    synthetic_pass = (
        synthetic.get("status") == "PASS"
        and synthetic.get("synthetic_non_scoring") is True
        and synthetic.get("answer_data_available_before_group_freeze") is False
        and synthetic.get("all_predictions_frozen_before_reveal") is True
        and synthetic.get("group_freeze_status") == "GROUP_PREDICTION_FREEZE_PASS"
        and synthetic.get("literal_replay_status") == "PASS"
        and synthetic.get("learning_status") == "LEARNING_ACTIVE"
        and synthetic.get("plaintext_committed_to_repository") is False
        and synthetic.get("transient_plaintext_destroyed") is True
        and synthetic.get("transient_workspace_destroyed") is True
        and synthetic.get("secret_value_recorded") is False
    )
    checks.append(check_row(
        "PUBLIC_SYNTHETIC_END_TO_END",
        synthetic_pass,
        path=synthetic_path,
        actual={key: synthetic.get(key) for key in (
            "status", "synthetic_non_scoring", "answer_data_available_before_group_freeze",
            "all_predictions_frozen_before_reveal", "group_freeze_status", "literal_replay_status",
            "learning_status", "plaintext_committed_to_repository", "transient_plaintext_destroyed",
            "transient_workspace_destroyed", "secret_value_recorded", "object_hash")},
        expected={
            "status": "PASS",
            "answer_data_available_before_group_freeze": False,
            "group_freeze_status": "GROUP_PREDICTION_FREEZE_PASS",
            "literal_replay_status": "PASS",
            "learning_status": "LEARNING_ACTIVE",
            "transient_plaintext_destroyed": True,
        },
    ))

    runner_path = root / "config/external-runner.json"
    runner = read_json(runner_path)
    source_delivery = runner.get("source_delivery") if isinstance(runner.get("source_delivery"), dict) else {}
    freeze_gate = runner.get("freeze_gate") if isinstance(runner.get("freeze_gate"), dict) else {}
    quarantine = runner.get("contamination_quarantine") if isinstance(runner.get("contamination_quarantine"), dict) else {}
    runner_pass = (
        runner.get("schema") == "EXTERNAL-RUNNER-INSTALLATION-V2"
        and runner.get("runner_id") == "CHAT_WORK_INTERACTIVE_EXECUTOR"
        and runner.get("user_initiated_session_required") is True
        and runner.get("background_execution") is False
        and runner.get("api_service_required") is False
        and runner.get("answer_data_available") is False
        and runner.get("runtime_repository_vault_credential") == "NONE"
        and set(runner.get("supported_session_modes", [])) == {"CHAT_ONLY", "WORK"}
        and source_delivery.get("project_upload_access") == "DENIED_AND_NOT_USED"
        and source_delivery.get("fallback_policy") == "FAIL_CLOSED_NO_PROJECT_UPLOAD_FALLBACK"
        and freeze_gate.get("status") == "ENFORCED"
        and freeze_gate.get("group_freeze_before_reveal_required") is True
        and freeze_gate.get("answer_access_before_group_freeze") is False
        and quarantine.get("historical_report_access") == "DENIED_AND_NOT_USED"
        and quarantine.get("postreveal_access") == "DENIED_AND_NOT_USED"
        and quarantine.get("shadow_rebuild_access") == "DENIED_AND_NOT_USED"
        and quarantine.get("failure_policy") == "FAIL_CLOSED_SCORE_PROHIBITED"
    )
    checks.append(check_row(
        "USER_INITIATED_EXTERNAL_RUNNER_BOUNDARY",
        runner_pass,
        path=runner_path,
        actual={
            "schema": runner.get("schema"),
            "runner_id": runner.get("runner_id"),
            "user_initiated_session_required": runner.get("user_initiated_session_required"),
            "background_execution": runner.get("background_execution"),
            "answer_data_available": runner.get("answer_data_available"),
            "runtime_repository_vault_credential": runner.get("runtime_repository_vault_credential"),
            "source_delivery": source_delivery,
            "freeze_gate": freeze_gate,
            "contamination_quarantine": quarantine,
        },
        expected="user-initiated, answer-free, fail-closed, no fallback, no private vault credential",
    ))

    branch_pass = activation_mode == "candidate" or ref_name == "main"
    checks.append(check_row(
        "ACTIVATION_MODE_BRANCH_BOUNDARY",
        branch_pass,
        path=None,
        actual={"activation_mode": activation_mode, "ref_name": ref_name},
        expected={"candidate": "any PR/ref descended from architecture merge", "main": "ref_name=main"},
    ))

    all_pass = all(row["status"] == "PASS" for row in checks)
    status = (
        "INSTALLED_VALIDATED_READY_FOR_USER_INITIATED_CLEAN_START"
        if all_pass and activation_mode == "main"
        else "INSTALL_CHECK_PASS_CANDIDATE"
        if all_pass
        else "INSTALL_CHECK_FAIL"
    )
    receipt = {
        "schema": "FINAL-OPEN-SOURCE-INSTALL-CHECK-RECEIPT-V3",
        "status": status,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repository": "chinaneedM/ziwei-bazi-model",
        "repository_visibility": visibility,
        "code_commit": current_commit,
        "ref_name": ref_name,
        "activation_mode": activation_mode,
        "architecture_merge_commit": ARCHITECTURE_MERGE_COMMIT,
        "checks": checks,
        "check_count": len(checks),
        "pass_count": sum(row["status"] == "PASS" for row in checks),
        "failure_count": sum(row["status"] != "PASS" for row in checks),
        "automation_runtime_install_status": status,
        "formal_open_source_release_permission": "PASS" if all_pass else "BLOCKED",
        "formal_training_permission": (
            "READY_FOR_USER_INITIATED_CLEAN_START_ONLY"
            if all_pass and activation_mode == "main"
            else "BLOCKED_PENDING_MAIN_BRANCH_INSTALL_CHECK"
            if all_pass
            else "BLOCKED"
        ),
        "score_eligibility": "CONDITIONAL_PER_RUN_CAUSAL_USE_RECEIPT_PASS",
        "background_execution": False,
        "synthetic_run_scoring_eligibility": "NONE",
    }
    receipt["object_hash"] = object_hash(receipt)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--visibility", required=True, choices=["public", "private", "internal"])
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--activation-mode", required=True, choices=["candidate", "main"])
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    tests_passed = os.environ.get("FORTUNE_INSTALL_TESTS_PASSED") == "1"
    receipt = verify(
        Path(args.root),
        args.visibility,
        args.expected_commit,
        args.activation_mode,
        tests_passed,
        Path(args.output),
    )
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0 if receipt["failure_count"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
