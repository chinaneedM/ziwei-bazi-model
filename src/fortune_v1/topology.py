from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from .util import atomic_write_json, read_json, utc_now


def _github_get(repo: str, token: str) -> tuple[int, dict[str, Any] | None]:
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repo}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28"},
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, None


def verify_topology(config_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    config = read_json(config_path)
    runtime_token = os.getenv("RUNTIME_REPO_TOKEN")
    vault_self_token = os.getenv("VAULT_SELF_TOKEN")
    required_profile = {
        "github_plan_profile": "FREE_PRIVATE_OWNER_CONTROL",
        "grading_topology": "ANSWER_VAULT_INITIATED_REVERSE_GRADING",
        "runtime_repository_vault_credential": "NONE",
        "answer_vault_runtime_credential": "RUNTIME_REPO_TOKEN",
        "branch_protection_status": "NOT_AVAILABLE_ON_CURRENT_PLAN",
        "ruleset_enforcement_status": "NOT_AVAILABLE_ON_CURRENT_PLAN",
        "environment_protection_status": "NOT_AVAILABLE_ON_CURRENT_PLAN",
        "owner_manual_trigger_required": "YES",
    }
    profile_checks = {key: config.get(key) == value for key, value in required_profile.items()}
    if not runtime_token or not vault_self_token:
        result = {
            "schema": "GITHUB-TOPOLOGY-RECEIPT-V2", "status": "FAIL",
            "reason": "ANSWER_VAULT_MACHINE_PROBE_NOT_EXECUTED",
            "checks": {"PHYSICAL_REPOSITORY_SEPARATION": "UNVERIFIED",
                       "TOKEN_REPOSITORY_SCOPE": "UNVERIFIED",
                       "RUNTIME_VAULT_ACCESS_DENIAL": "UNVERIFIED",
                       "GRADING_DIRECTION": "PASS" if profile_checks["grading_topology"] else "FAIL",
                       "FREE_PLAN_CONTROL_LIMITATION": "RECORDED" if all(profile_checks.values()) else "FAIL"},
            "plan_profile": required_profile, "profile_checks": profile_checks,
            "prediction_identity_vault_read": None, "checked_at": utc_now(),
        }
        atomic_write_json(output_path, result, overwrite=True)
        return result

    runtime_repo, vault_repo = config["runtime_repo"], config["answer_vault_repo"]
    rt_runtime, rt_runtime_obj = _github_get(runtime_repo, runtime_token)
    rt_vault, _ = _github_get(vault_repo, runtime_token)
    self_vault, self_vault_obj = _github_get(vault_repo, vault_self_token)
    self_runtime, _ = _github_get(runtime_repo, vault_self_token)
    physical = runtime_repo != vault_repo and rt_runtime == 200 and self_vault == 200
    token_scope = rt_runtime == 200 and rt_vault in {403, 404} and self_vault == 200 and self_runtime in {403, 404}
    runtime_denied = rt_vault in {403, 404}
    grading_direction = config.get("grading_topology") == "ANSWER_VAULT_INITIATED_REVERSE_GRADING"
    limitation_recorded = all(profile_checks.values())
    private = bool(rt_runtime_obj and rt_runtime_obj.get("private") is True and
                   self_vault_obj and self_vault_obj.get("private") is True)
    checks = {
        "PHYSICAL_REPOSITORY_SEPARATION": "PASS" if physical and private else "FAIL",
        "TOKEN_REPOSITORY_SCOPE": "PASS" if token_scope else "FAIL",
        "RUNTIME_VAULT_ACCESS_DENIAL": "PASS" if runtime_denied else "FAIL",
        "GRADING_DIRECTION": "PASS" if grading_direction else "FAIL",
        "FREE_PLAN_CONTROL_LIMITATION": "RECORDED" if limitation_recorded else "FAIL",
    }
    result = {
        "schema": "GITHUB-TOPOLOGY-RECEIPT-V2", "runtime_repo": runtime_repo,
        "answer_vault_repo": vault_repo, "checks": checks, "plan_profile": required_profile,
        "probe_http_status": {"runtime_token_to_runtime": rt_runtime,
                              "runtime_token_to_vault": rt_vault,
                              "vault_self_token_to_vault": self_vault,
                              "vault_self_token_to_runtime": self_runtime},
        "prediction_identity_vault_read": rt_vault == 200,
        "status": "PASS" if all(value in {"PASS", "RECORDED"} for value in checks.values()) else "FAIL",
        "checked_at": utc_now(),
    }
    atomic_write_json(output_path, result, overwrite=True)
    return result


def scan_runtime_workflows(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    workflows = root / ".github" / "workflows"
    texts = {path.relative_to(root).as_posix(): path.read_text(encoding="utf-8")
             for path in workflows.glob("*.y*ml") if path.is_file()}
    obsolete_secret = "ANSWER_" + "VAULT_TOKEN"
    vault_repo_literal = "chinaneedM/fortune-answer-vault"
    violations = []
    for path, text in texts.items():
        if obsolete_secret in text:
            violations.append({"path": path, "rule": "OBSOLETE_VAULT_SECRET_REFERENCE"})
        if vault_repo_literal in text or ("repository:" in text and "answer-vault" in text):
            violations.append({"path": path, "rule": "RUNTIME_WORKFLOW_VAULT_CHECKOUT"})
    if (workflows / "grade-frozen.yml").exists():
        violations.append({"path": ".github/workflows/grade-frozen.yml", "rule": "OBSOLETE_GRADING_WORKFLOW_PRESENT"})
    return {"schema": "RUNTIME-WORKFLOW-VAULT-SCAN-V1", "workflow_count": len(texts),
            "runtime_repository_vault_credential": "NONE" if not violations else "VIOLATION",
            "violations": violations, "status": "PASS" if not violations else "FAIL"}
