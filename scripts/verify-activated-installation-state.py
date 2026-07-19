#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def object_hash(value: dict[str, Any]) -> str:
    body = dict(value)
    body.pop("object_hash", None)
    return hashlib.sha256(canonical_bytes(body)).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)


def add(checks: list[dict[str, Any]], name: str, passed: bool, actual: Any, expected: Any, path: str | None = None) -> None:
    checks.append({
        "check": name,
        "status": "PASS" if passed else "FAIL",
        "path": path,
        "actual": actual,
        "expected": expected,
    })


def verify(root: Path, expected_current_commit: str, activation_mode: str, output: Path | None = None) -> dict[str, Any]:
    root = root.resolve()
    checks: list[dict[str, Any]] = []

    current_proc = git(root, "rev-parse", "HEAD")
    current = current_proc.stdout.strip() if current_proc.returncode == 0 else None
    add(checks, "CURRENT_COMMIT", current == expected_current_commit, current, expected_current_commit)

    state_path = root / "reports/install-state.json"
    state = read_json(state_path)
    state_hash_ok = state.get("object_hash") == object_hash(state)
    add(checks, "INSTALL_STATE_OBJECT_HASH", state_hash_ok, state.get("object_hash"), object_hash(state), state_path.relative_to(root).as_posix())

    state_fields = {
        "schema": "INSTALLATION-STATE-SEAL-V1",
        "status": "INSTALLED_VALIDATED",
        "automation_runtime_install_status": "INSTALLED_VALIDATED_READY_FOR_USER_INITIATED_CLEAN_START",
        "formal_open_source_release_permission": "PASS",
        "formal_training_permission": "READY_FOR_USER_INITIATED_CLEAN_START_ONLY",
        "score_eligibility": "CONDITIONAL_PER_RUN_CAUSAL_USE_RECEIPT_PASS",
        "background_execution": False,
        "open_source_project_mode": "COMPLETE_OPEN_SOURCE",
        "software_license": "Apache-2.0",
        "active_knowledge_release_id": "KNOWLEDGE-R17",
        "knowledge_license_expression": "CC0-1.0",
        "synthetic_run_scoring_eligibility": "NONE",
        "private_repository_dependency_status": "REMOVED",
        "next_allowed_action": "USER_INITIATED_CLEAN_START",
    }
    actual_state_fields = {key: state.get(key) for key in state_fields}
    add(checks, "INSTALL_STATE_FIELDS", actual_state_fields == state_fields, actual_state_fields, state_fields, state_path.relative_to(root).as_posix())

    validated_main = str(state.get("validated_main_commit") or "")
    ancestor_proc = git(root, "merge-base", "--is-ancestor", validated_main, expected_current_commit) if validated_main else None
    ancestor_ok = bool(ancestor_proc and ancestor_proc.returncode == 0)
    add(checks, "VALIDATED_MAIN_IS_ANCESTOR", ancestor_ok, {"validated_main": validated_main, "current": expected_current_commit}, "validated_main is ancestor of current")

    readback_raw = str(state.get("main_readback_path") or "")
    readback_path = root / readback_raw
    readback = read_json(readback_path)
    readback_ok = (
        readback.get("object_hash") == object_hash(readback)
        and readback.get("object_hash") == state.get("main_readback_object_hash")
        and readback.get("status") == "PASS"
        and readback.get("validated_main_commit") == validated_main
        and readback.get("check_count") == 14
        and readback.get("pass_count") == 14
        and readback.get("failure_count") == 0
        and readback.get("formal_training_permission") == "READY_FOR_USER_INITIATED_CLEAN_START_ONLY"
        and readback.get("background_execution") is False
    )
    add(checks, "MAIN_READBACK_OBJECT", readback_ok, {
        "path": readback_raw,
        "sha256": sha256(readback_path),
        "object_hash": readback.get("object_hash"),
        "status": readback.get("status"),
        "validated_main_commit": readback.get("validated_main_commit"),
    }, {
        "object_hash": state.get("main_readback_object_hash"),
        "status": "PASS",
        "validated_main_commit": validated_main,
    }, readback_raw)

    activation_raw = str(state.get("activation_receipt_path") or "")
    activation_path = root / activation_raw
    activation = read_json(activation_path)
    activation_ok = (
        activation.get("object_hash") == object_hash(activation)
        and activation.get("object_hash") == state.get("activation_receipt_object_hash")
        and activation.get("status") == "PASS_MAIN_RUNTIME_VALIDATION_READY_FOR_STATE_ACTIVATION"
        and activation.get("install_v3_merge_commit_sha") == validated_main
        and activation.get("formal_open_source_release_permission") == "PASS"
        and activation.get("formal_training_permission") == "READY_FOR_USER_INITIATED_CLEAN_START_ONLY"
        and activation.get("background_execution") is False
    )
    add(checks, "FINAL_ACTIVATION_RECEIPT", activation_ok, {
        "path": activation_raw,
        "sha256": sha256(activation_path),
        "object_hash": activation.get("object_hash"),
        "status": activation.get("status"),
    }, {
        "object_hash": state.get("activation_receipt_object_hash"),
        "status": "PASS_MAIN_RUNTIME_VALIDATION_READY_FOR_STATE_ACTIVATION",
    }, activation_raw)

    contract_path = root / "config/open-source-release.json"
    contract = read_json(contract_path)
    gate_results = contract.get("release_gate_results") if isinstance(contract.get("release_gate_results"), dict) else {}
    gates_ok = bool(gate_results) and all(value in {"PASS", "PASS_NONSCORING"} for value in gate_results.values())
    contract_ok = (
        contract.get("schema") == "OPEN-SOURCE-RELEASE-CONTRACT-V1"
        and contract.get("status") == "INSTALLED_VALIDATED"
        and contract.get("formal_open_source_release_allowed") is True
        and contract.get("formal_training_permission") == "READY_FOR_USER_INITIATED_CLEAN_START_ONLY"
        and contract.get("score_eligibility") == "CONDITIONAL_PER_RUN_CAUSAL_USE_RECEIPT_PASS"
        and contract.get("background_execution") is False
        and contract.get("validated_main_commit") == validated_main
        and contract.get("main_install_readback_object_hash") == readback.get("object_hash")
        and contract.get("activation_receipt_object_hash") == activation.get("object_hash")
        and gates_ok
    )
    add(checks, "OPEN_SOURCE_RELEASE_CONTRACT_ACTIVATED", contract_ok, {
        "status": contract.get("status"),
        "formal_open_source_release_allowed": contract.get("formal_open_source_release_allowed"),
        "formal_training_permission": contract.get("formal_training_permission"),
        "validated_main_commit": contract.get("validated_main_commit"),
        "release_gate_results": gate_results,
    }, {
        "status": "INSTALLED_VALIDATED",
        "formal_open_source_release_allowed": True,
        "formal_training_permission": "READY_FOR_USER_INITIATED_CLEAN_START_ONLY",
        "validated_main_commit": validated_main,
        "all_release_gates": "PASS_OR_PASS_NONSCORING",
    }, contract_path.relative_to(root).as_posix())

    mode_ok = activation_mode in {"candidate", "main"}
    add(checks, "ACTIVATION_MODE", mode_ok, activation_mode, "candidate or main")

    failure_count = sum(row["status"] != "PASS" for row in checks)
    receipt = {
        "schema": "ACTIVATED-INSTALLATION-STATE-VERIFICATION-V1",
        "status": "PASS" if failure_count == 0 else "FAIL",
        "repository": "chinaneedM/ziwei-bazi-model",
        "code_commit": current,
        "activation_mode": activation_mode,
        "validated_main_commit": validated_main or None,
        "check_count": len(checks),
        "pass_count": sum(row["status"] == "PASS" for row in checks),
        "failure_count": failure_count,
        "checks": checks,
        "formal_open_source_release_permission": "PASS" if failure_count == 0 else "BLOCKED",
        "formal_training_permission": "READY_FOR_USER_INITIATED_CLEAN_START_ONLY" if failure_count == 0 else "BLOCKED",
        "score_eligibility": "CONDITIONAL_PER_RUN_CAUSAL_USE_RECEIPT_PASS",
        "background_execution": False,
    }
    receipt["object_hash"] = object_hash(receipt)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--expected-current-commit", required=True)
    parser.add_argument("--activation-mode", required=True, choices=["candidate", "main"])
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    receipt = verify(Path(args.root), args.expected_current_commit, args.activation_mode, Path(args.output))
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0 if receipt["failure_count"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
