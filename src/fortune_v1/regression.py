from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, read_json, sha256_file, utc_now

STAGE_ORDER = ["DEFECT_REPRODUCTION", "AFFECTED_FAILURES", "CURRENT_DEV_GROUP", "RELATED_HISTORY", "CORE_HISTORY", "FULL_REGRESSION"]


def select_regression(manifest_path: str | Path, affected_tags: list[str], full: bool = False) -> dict[str, Any]:
    manifest = read_json(manifest_path)
    cases = manifest.get("cases", [])
    selected = {}
    selected["DEFECT_REPRODUCTION"] = [c for c in cases if c.get("role") == "DEFECT_REPRODUCTION"]
    selected["AFFECTED_FAILURES"] = [c for c in cases if set(c.get("tags", [])) & set(affected_tags) and c.get("previous_status") == "FAIL"]
    selected["CURRENT_DEV_GROUP"] = [c for c in cases if c.get("dataset_type") == "DEV" and c.get("group") == manifest.get("current_dev_group")]
    selected["RELATED_HISTORY"] = [c for c in cases if set(c.get("tags", [])) & set(affected_tags) and c.get("dataset_type") == "REGRESSION"]
    selected["CORE_HISTORY"] = [c for c in cases if c.get("core") is True]
    selected["FULL_REGRESSION"] = cases if full else []
    return {"schema": "REGRESSION-SELECTION-V1", "affected_tags": affected_tags, "stages": selected, "selected_at": utc_now()}


def execute_regression(selection: dict[str, Any], runner: str | None, candidate_version: str,
                       frozen_version: str, output_path: str | Path, baseline_results: str | Path | None = None) -> dict[str, Any]:
    if not runner:
        result = {"schema": "PATCH-AND-REGRESSION-V1", "candidate_version": candidate_version,
                  "frozen_version": frozen_version, "stages": [], "damage": 0,
                  "decision": "GROUP_HOLD", "reason": "EXTERNAL_RUNNER_MISSING", "created_at": utc_now()}
        atomic_write_json(output_path, result); return result
    baseline = read_json(baseline_results) if baseline_results else {"case_results": {}}
    stages, candidate_results = [], {}
    for stage_name in STAGE_ORDER:
        cases = selection["stages"].get(stage_name, [])
        rows = []
        for case in cases:
            case_id = case["case_id"]
            env = os.environ.copy(); env.update({"FORTUNE_CASE_ID": case_id, "FORTUNE_CANDIDATE_VERSION": candidate_version, "FORTUNE_FROZEN_VERSION": frozen_version})
            proc = subprocess.run([runner, case_id], capture_output=True, text=True, env=env, timeout=int(case.get("timeout_seconds", 1800)))
            status = "PASS" if proc.returncode == 0 else "FAIL"
            rows.append({"case_id": case_id, "status": status, "returncode": proc.returncode,
                         "stdout_sha256": __import__("hashlib").sha256(proc.stdout.encode()).hexdigest(),
                         "stderr_sha256": __import__("hashlib").sha256(proc.stderr.encode()).hexdigest()})
            candidate_results[case_id] = status
        stages.append({"stage": stage_name, "cases": rows, "status": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"})
        if any(r["status"] == "FAIL" for r in rows): break
    damage = sum(1 for case_id, old in baseline.get("case_results", {}).items() if old == "PASS" and candidate_results.get(case_id) == "FAIL")
    all_pass = len(stages) == len(STAGE_ORDER) and all(s["status"] == "PASS" for s in stages)
    decision = "REGRESSION_PASS" if all_pass and damage == 0 else "REJECTED"
    result = {"schema": "PATCH-AND-REGRESSION-V1", "regression_id": f"REG-{candidate_version}",
              "candidate_version": candidate_version, "frozen_version": frozen_version, "stages": stages,
              "damage": damage, "damage_tolerance": 0, "decision": decision, "created_at": utc_now()}
    atomic_write_json(output_path, result); return result

