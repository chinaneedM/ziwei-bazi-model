from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

from .util import atomic_write_json, read_json, sha256_file, utc_now


def _git_commit(repo: Path) -> str | None:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True)
    return proc.stdout.strip() if proc.returncode == 0 else None


def installation_check(repo_root: str | Path, source_audit_path: str | Path | None,
                       prompt_snapshot_path: str | Path | None, test_report_path: str | Path | None,
                       topology_receipt_path: str | Path | None, external_runner: str | None,
                       output_path: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    checks = []
    def add(name: str, passed: bool, evidence: Any) -> None:
        checks.append({"check": name, "status": "PASS" if passed else "FAIL", "evidence": evidence})
    source = read_json(source_audit_path) if source_audit_path and Path(source_audit_path).exists() else None
    add("SOURCE_BASELINE_20_FILES_AND_BINDING", bool(source and source.get("status") == "PASS"), None if not source else {"status": source.get("status"), "missing": source.get("missing"), "duplicates": source.get("duplicates")})
    prompt = read_json(prompt_snapshot_path) if prompt_snapshot_path and Path(prompt_snapshot_path).exists() else None
    add("MAIN_PROMPT_AUDIT_SNAPSHOT", bool(prompt and prompt.get("authority_statement") == "AUDIT_COPY_ONLY_NOT_RUNTIME_AUTHORITY"), None if not prompt else {"runtime_id": prompt.get("runtime_id"), "sha256": prompt.get("snapshot_sha256")})
    tests = read_json(test_report_path) if test_report_path and Path(test_report_path).exists() else None
    add("STATIC_AND_SYNTHETIC_TESTS", bool(tests and tests.get("status") == "PASS"), tests)
    topology = read_json(topology_receipt_path) if topology_receipt_path and Path(topology_receipt_path).exists() else None
    add("TWO_REPOSITORY_IDENTITY_ISOLATION", bool(topology and topology.get("status") == "PASS" and topology.get("prediction_identity_vault_read") is False), topology)
    runner_ok = bool(external_runner and Path(external_runner).is_file() and os.access(external_runner, os.X_OK))
    add("EXTERNAL_PREDICTION_RUNNER", runner_ok, external_runner or "MISSING")
    commit = _git_commit(root)
    add("IMMUTABLE_GIT_COMMIT", bool(commit), commit)
    schema_count = len(list((root / "schemas").glob("*.schema.json")))
    add("SCHEMA_SET", schema_count >= 7, {"count": schema_count})
    all_pass = all(c["status"] == "PASS" for c in checks)
    status = "INSTALL_VALIDATION_CANDIDATE" if all_pass else "SCHEMA_DEFINED_NOT_INSTALLED"
    result = {
        "schema": "INSTALLATION-RECEIPT-V1", "generated_at": utc_now(), "repository_root": str(root),
        "code_commit": commit, "checks": checks, "status": status,
        "s19_update_candidate": ({"AUTOMATION_RUNTIME_INSTALL_STATUS": "INSTALLED_VALIDATED", "basis_receipt_sha256": "COMPUTED_AFTER_WRITE"} if all_pass else None),
    }
    atomic_write_json(output_path, result, overwrite=True)
    if all_pass:
        result["s19_update_candidate"]["basis_receipt_sha256"] = sha256_file(output_path)
        atomic_write_json(output_path, result, overwrite=True)
    return result


def render_markdown(report_paths: list[str | Path], output_path: str | Path) -> Path:
    sections = ["# Fortune V1 build and validation report", "", f"Generated: {utc_now()}", ""]
    for report_path in report_paths:
        path = Path(report_path)
        if not path.exists():
            sections.extend([f"## {path.name}", "", "Status: MISSING", ""]); continue
        obj = read_json(path)
        sections.extend([f"## {path.name}", "", f"- Schema: `{obj.get('schema', 'UNKNOWN')}`", f"- Status: `{obj.get('status', obj.get('decision', 'UNKNOWN'))}`", f"- SHA256: `{sha256_file(path)}`", ""])
        if obj.get("missing"): sections.append(f"- Missing: `{', '.join(obj['missing'])}`")
        if obj.get("duplicates"): sections.append(f"- Duplicates: `{', '.join(obj['duplicates'])}`")
        if obj.get("reason"): sections.append(f"- Reason: `{obj['reason']}`")
        sections.append("")
    target = Path(output_path); target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(sections), encoding="utf-8")
    return target

