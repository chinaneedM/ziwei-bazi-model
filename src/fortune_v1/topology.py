from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, read_json, utc_now


def _github_get(repo: str, token: str) -> tuple[int, dict[str, Any] | None]:
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repo}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"},
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, None


def verify_topology(config_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    config = read_json(config_path)
    prediction = os.getenv("FORTUNE_PREDICTION_GITHUB_TOKEN")
    grader = os.getenv("FORTUNE_GRADER_GITHUB_TOKEN")
    if not prediction or not grader:
        result = {"schema": "GITHUB-TOPOLOGY-RECEIPT-V1", "status": "FAIL", "reason": "IDENTITY_TOKENS_MISSING",
                  "prediction_identity_vault_read": None, "checked_at": utc_now()}
        atomic_write_json(output_path, result, overwrite=True); return result
    runtime_repo, vault_repo = config["runtime_repo"], config["answer_vault_repo"]
    p_runtime, p_runtime_obj = _github_get(runtime_repo, prediction)
    p_vault, _ = _github_get(vault_repo, prediction)
    g_runtime, g_runtime_obj = _github_get(runtime_repo, grader)
    g_vault, g_vault_obj = _github_get(vault_repo, grader)
    checks = {
        "prediction_runtime_read": p_runtime == 200,
        "prediction_vault_denied": p_vault in {403, 404},
        "grader_runtime_read": g_runtime == 200,
        "grader_vault_read": g_vault == 200,
        "runtime_private": bool(p_runtime_obj and p_runtime_obj.get("private") is True),
        "vault_private": bool(g_vault_obj and g_vault_obj.get("private") is True),
        "repositories_distinct": runtime_repo != vault_repo,
    }
    result = {"schema": "GITHUB-TOPOLOGY-RECEIPT-V1", "runtime_repo": runtime_repo, "answer_vault_repo": vault_repo,
              "checks": checks, "prediction_identity_vault_read": p_vault == 200,
              "status": "PASS" if all(checks.values()) else "FAIL", "checked_at": utc_now()}
    atomic_write_json(output_path, result, overwrite=True); return result

