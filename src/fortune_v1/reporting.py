from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from .topology import scan_runtime_workflows
from .util import atomic_write_json, read_json, sha256_file, utc_now


def _git_commit(repo: Path) -> str | None:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True)
    return proc.stdout.strip() if proc.returncode == 0 else None


def _check(name: str, passed: bool, path: str | Path | None, field_path: str,
           actual: Any, expected: Any, commit_sha: str | None,
           *, non_pass_state: str = "FAIL") -> dict[str, Any]:
    p = Path(path) if path else None
    return {"check": name, "real_path": str(p) if p else None,
            "file_sha256": sha256_file(p) if p and p.is_file() else None,
            "object_field_path": field_path, "actual": actual, "expected": expected,
            "difference": None if actual == expected else {"actual": actual, "expected": expected},
            "status": "PASS" if passed else non_pass_state,
            "corresponding_commit_sha": commit_sha}


def installation_check(repo_root: str | Path, source_audit_path: str | Path | None,
                       prompt_snapshot_path: str | Path | None, test_report_path: str | Path | None,
                       topology_receipt_path: str | Path | None, external_runner: str | None,
                       output_path: str | Path, binding_receipt_path: str | Path | None = None,
                       migration_receipt_path: str | Path | None = None,
                       answer_workflow_receipt_path: str | Path | None = None,
                       code_commit_override: str | None = None) -> dict[str, Any]:
    root = Path(repo_root)
    commit = code_commit_override or _git_commit(root)
    config_path = root / "config" / "github-topology.json"
    config = read_json(config_path)
    checks: list[dict[str, Any]] = []

    source = read_json(source_audit_path) if source_audit_path and Path(source_audit_path).is_file() else None
    source_actual = None if source is None else {"status": source.get("status"),
                                                 "unique_library_count": source.get("unique_library_count"),
                                                 "missing": source.get("missing"), "duplicates": source.get("duplicates")}
    checks.append(_check("SOURCE_BASELINE_20_FILES", bool(source and source.get("status") == "PASS" and
                                                          source.get("unique_library_count") == 20),
                         source_audit_path, "$.status+$.unique_library_count", source_actual,
                         {"status": "PASS", "unique_library_count": 20, "missing": [], "duplicates": {}}, commit))

    binding = read_json(binding_receipt_path) if binding_receipt_path and Path(binding_receipt_path).is_file() else None
    expected_binding = "1766aa81fad8134c12f50c18e2e7e7b3523e098113df37bd75a9a88a2cc56654"
    binding_actual = None if binding is None else {"status": binding.get("status"),
                                                   "declared": binding.get("declared_sha256_utf8_lf"),
                                                   "computed": binding.get("computed_sha256_utf8_lf"),
                                                   "row_count": binding.get("row_count")}
    checks.append(_check("S19_ACTIVE_BINDING_TABLE_RECOMPUTE", bool(binding and binding.get("status") == "PASS" and
                                                                    binding.get("declared_sha256_utf8_lf") == expected_binding and
                                                                    binding.get("computed_sha256_utf8_lf") == expected_binding and
                                                                    binding.get("row_count") == 19),
                         binding_receipt_path, "$.status+hashes+$.row_count", binding_actual,
                         {"status": "PASS", "declared": expected_binding, "computed": expected_binding, "row_count": 19}, commit))

    migration = read_json(migration_receipt_path) if migration_receipt_path and Path(migration_receipt_path).is_file() else None
    migration_actual = None if migration is None else {"status": migration.get("status"),
                                                       "source_file_count": migration.get("source_file_count"),
                                                       "baseline_commit_sha": migration.get("baseline_commit_sha"),
                                                       "baseline_tag": migration.get("baseline_tag"),
                                                       "baseline_tag_status": migration.get("baseline_tag_status")}
    migration_pass = bool(migration and migration.get("status") == "MIGRATED" and
                          migration.get("source_file_count") == 20 and migration.get("baseline_commit_sha") and
                          migration.get("baseline_tag") and migration.get("baseline_tag_status") == "VERIFIED")
    checks.append(_check("SOURCE_MIGRATION_AND_IMMUTABLE_BASELINE", migration_pass,
                         migration_receipt_path, "$.status+$.baseline_commit_sha+$.baseline_tag",
                         migration_actual, {"status": "MIGRATED", "source_file_count": 20,
                                            "baseline_commit_sha": "NON_NULL", "baseline_tag": "NON_NULL",
                                            "baseline_tag_status": "VERIFIED"}, commit))

    prompt = read_json(prompt_snapshot_path) if prompt_snapshot_path and Path(prompt_snapshot_path).is_file() else None
    prompt_actual = None if prompt is None else {"status": prompt.get("status"),
                                                 "runtime_id": prompt.get("runtime_id"),
                                                 "authority": prompt.get("authority_statement"),
                                                 "sha256": prompt.get("snapshot_sha256"),
                                                 "bytes": prompt.get("snapshot_bytes"),
                                                 "visible": prompt.get("actual", {}).get("visible_character_count")}
    prompt_expected = {"status": "PASS", "runtime_id": "MP-PROFESSIONAL-REASONING-20260715-R16",
                       "authority": "AUDIT_COPY_ONLY_NOT_RUNTIME_AUTHORITY",
                       "sha256": "832dd43129b6e5d3098c972a55179ccb7e9ab49a9770339a87c94deaa440b017",
                       "bytes": 14988, "visible": 6047}
    checks.append(_check("MAIN_PROMPT_AUDIT_SNAPSHOT", prompt_actual == prompt_expected,
                         prompt_snapshot_path, "$.status+$.runtime_id+$.authority_statement+$.actual",
                         prompt_actual, prompt_expected, commit))

    tests = read_json(test_report_path) if test_report_path and Path(test_report_path).is_file() else None
    checks.append(_check("STATIC_AND_SYNTHETIC_TESTS", bool(tests and tests.get("status") == "PASS"),
                         test_report_path, "$.status", None if tests is None else tests.get("status"), "PASS", commit))

    workflow_scan = scan_runtime_workflows(root)
    checks.append(_check("RUNTIME_REPOSITORY_VAULT_CREDENTIAL_NONE", workflow_scan["status"] == "PASS",
                         root / ".github" / "workflows", "runtime_workflow_scan.status",
                         workflow_scan, {"status": "PASS", "runtime_repository_vault_credential": "NONE"}, commit))

    topology = read_json(topology_receipt_path) if topology_receipt_path and Path(topology_receipt_path).is_file() else None
    for component in ["PHYSICAL_REPOSITORY_SEPARATION", "TOKEN_REPOSITORY_SCOPE",
                      "RUNTIME_VAULT_ACCESS_DENIAL", "GRADING_DIRECTION"]:
        actual = None if topology is None else topology.get("checks", {}).get(component)
        checks.append(_check(component, actual == "PASS", topology_receipt_path,
                             f"$.checks.{component}", actual, "PASS", commit))
    limitation_actual = None if topology is None else topology.get("checks", {}).get("FREE_PLAN_CONTROL_LIMITATION")
    checks.append(_check("FREE_PLAN_CONTROL_LIMITATION_RECORDED", limitation_actual == "RECORDED",
                         topology_receipt_path, "$.checks.FREE_PLAN_CONTROL_LIMITATION",
                         limitation_actual, "RECORDED", commit))

    profile_expected = {"github_plan_profile": "FREE_PRIVATE_OWNER_CONTROL",
                        "grading_topology": "ANSWER_VAULT_INITIATED_REVERSE_GRADING",
                        "runtime_repository_vault_credential": "NONE",
                        "answer_vault_runtime_credential": "RUNTIME_REPO_TOKEN",
                        "branch_protection_status": "NOT_AVAILABLE_ON_CURRENT_PLAN",
                        "ruleset_enforcement_status": "NOT_AVAILABLE_ON_CURRENT_PLAN",
                        "environment_protection_status": "NOT_AVAILABLE_ON_CURRENT_PLAN",
                        "owner_manual_trigger_required": "YES"}
    profile_actual = {key: config.get(key) for key in profile_expected}
    checks.append(_check("FREE_PRIVATE_OWNER_CONTROL_PROFILE", profile_actual == profile_expected,
                         config_path, "$.github_plan_profile+grading_and_control_fields",
                         profile_actual, profile_expected, commit))

    answer_workflow = read_json(answer_workflow_receipt_path) if answer_workflow_receipt_path and Path(answer_workflow_receipt_path).is_file() else None
    answer_actual = None if answer_workflow is None else {"status": answer_workflow.get("status"),
                                                         "repository": answer_workflow.get("repository"),
                                                         "workflow_path": answer_workflow.get("workflow_path"),
                                                         "readback_sha256": answer_workflow.get("readback_sha256")}
    answer_pass = bool(answer_workflow and answer_workflow.get("status") == "PASS" and
                       answer_workflow.get("repository") == "chinaneedM/fortune-answer-vault" and
                       answer_workflow.get("readback_sha256"))
    checks.append(_check("ANSWER_VAULT_WORKFLOW_INSTALLED_AND_READBACK", answer_pass,
                         answer_workflow_receipt_path, "$.status+$.repository+$.readback_sha256",
                         answer_actual, {"status": "PASS", "repository": "chinaneedM/fortune-answer-vault",
                                         "workflow_path": ".github/workflows/grade-frozen-prediction.yml",
                                         "readback_sha256": "NON_NULL"}, commit))

    runner = read_json(external_runner) if external_runner and Path(external_runner).is_file() else None
    required_runner_fields = ["runner_id", "runner_type", "model_or_executor", "input_contract", "output_schema",
                              "timeout_seconds", "failure_status", "no_answer_access_proof", "code_commit",
                              "prompt_binding", "source_binding", "run_id_nonoverwrite",
                              "ziwei_bazi_local_seal_requirement"]
    runner_pass = bool(runner and runner.get("external_prediction_runner_status") == "INSTALLED" and
                       all(runner.get(key) not in {None, ""} for key in required_runner_fields if key not in {"prompt_binding", "no_answer_access_proof"}) and
                       isinstance(runner.get("prompt_binding"), dict) and isinstance(runner.get("no_answer_access_proof"), dict) and
                       runner.get("run_id_nonoverwrite") is True and runner.get("ziwei_bazi_local_seal_requirement") is True)
    checks.append(_check("EXTERNAL_PREDICTION_RUNNER", runner_pass, external_runner,
                         "$.external_prediction_runner_status+required_contract_fields",
                         None if runner is None else {"status": runner.get("external_prediction_runner_status"),
                                                     "runner_id": runner.get("runner_id")},
                         {"status": "INSTALLED", "runner_id": "NON_NULL"}, commit))

    checks.append(_check("IMMUTABLE_GIT_COMMIT", bool(commit), root / ".git", "HEAD", commit, "NON_NULL", commit))
    schema_count = len(list((root / "schemas").glob("*.schema.json")))
    checks.append(_check("SCHEMA_SET", schema_count >= 9, root / "schemas", "*.schema.json.count",
                         schema_count, ">=9", commit))
    all_pass = all(row["status"] == "PASS" for row in checks)
    status = "INSTALL_VALIDATION_CANDIDATE" if all_pass else "SCHEMA_DEFINED_NOT_INSTALLED"
    result = {"schema": "INSTALLATION-RECEIPT-V2", "generated_at": utc_now(),
              "repository_root": str(root), "code_commit": commit, "checks": checks,
              "github_plan_profile": "FREE_PRIVATE_OWNER_CONTROL",
              "grading_topology": "ANSWER_VAULT_INITIATED_REVERSE_GRADING",
              "automation_runtime_install_status": status,
              "status": status,
              "s19_installed_validated_status_update_candidate": ({
                  "AUTOMATION_RUNTIME_INSTALL_STATUS": "INSTALLED_VALIDATED",
                  "basis_receipt_sha256": "COMPUTED_AFTER_WRITE"} if all_pass else None)}
    atomic_write_json(output_path, result, overwrite=True)
    if all_pass:
        result["s19_installed_validated_status_update_candidate"]["basis_receipt_sha256"] = sha256_file(output_path)
        atomic_write_json(output_path, result, overwrite=True)
    return result


def render_markdown(report_paths: list[str | Path], output_path: str | Path) -> Path:
    sections = ["# Fortune V1 build and validation report", "", f"Generated: {utc_now()}", ""]
    for report_path in report_paths:
        path = Path(report_path)
        if not path.exists():
            sections.extend([f"## {path.name}", "", "Status: MISSING", ""])
            continue
        obj = read_json(path)
        sections.extend([f"## {path.name}", "", f"- Schema: `{obj.get('schema', 'UNKNOWN')}`",
                         f"- Status: `{obj.get('status', obj.get('decision', 'UNKNOWN'))}`",
                         f"- SHA256: `{sha256_file(path)}`", ""])
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(sections), encoding="utf-8")
    return target
