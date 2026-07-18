from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any

from .util import atomic_write_json, read_json, utc_now

STAGE_ORDER = [
    "DEFECT_REPRODUCTION",
    "AFFECTED_FAILURES",
    "CURRENT_DEV_GROUP",
    "RELATED_HISTORY",
    "CORE_HISTORY",
    "FULL_REGRESSION",
]


def select_regression(manifest_path: str | Path, affected_tags: list[str], full: bool = False) -> dict[str, Any]:
    manifest = read_json(manifest_path)
    cases = manifest.get("cases", [])
    selected = {}
    selected["DEFECT_REPRODUCTION"] = [c for c in cases if c.get("role") == "DEFECT_REPRODUCTION"]
    selected["AFFECTED_FAILURES"] = [
        c for c in cases
        if set(c.get("tags", [])) & set(affected_tags) and c.get("previous_status") == "FAIL"
    ]
    selected["CURRENT_DEV_GROUP"] = [
        c for c in cases
        if c.get("dataset_type") == "DEV" and c.get("group") == manifest.get("current_dev_group")
    ]
    selected["RELATED_HISTORY"] = [
        c for c in cases
        if set(c.get("tags", [])) & set(affected_tags) and c.get("dataset_type") == "REGRESSION"
    ]
    selected["CORE_HISTORY"] = [c for c in cases if c.get("core") is True]
    selected["FULL_REGRESSION"] = cases if full else []
    return {
        "schema": "REGRESSION-SELECTION-V2",
        "affected_tags": affected_tags,
        "stages": selected,
        "mastery_policy": manifest.get(
            "mastery_policy",
            {
                "top1_rate": 0.80,
                "top2_rate": 0.90,
                "zero_regression_damage": True,
            },
        ),
        "selected_at": utc_now(),
    }


def _parse_runner_metrics(stdout: str) -> dict[str, Any] | None:
    for line in reversed([line.strip() for line in stdout.splitlines() if line.strip()]):
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(value, dict):
            continue
        if "question_count" not in value:
            continue
        return value
    return None


def execute_regression(selection: dict[str, Any], runner: str | None, candidate_version: str,
                       frozen_version: str, output_path: str | Path,
                       baseline_results: str | Path | None = None) -> dict[str, Any]:
    if not runner:
        result = {
            "schema": "PATCH-AND-REGRESSION-V2",
            "candidate_version": candidate_version,
            "frozen_version": frozen_version,
            "stages": [],
            "damage": 0,
            "decision": "GROUP_HOLD",
            "reason": "EXTERNAL_RUNNER_MISSING",
            "created_at": utc_now(),
        }
        atomic_write_json(output_path, result)
        return result

    baseline = read_json(baseline_results) if baseline_results else {"case_results": {}}
    policy = selection.get("mastery_policy", {})
    target_top1 = float(policy.get("top1_rate", 0.80))
    target_top2 = float(policy.get("top2_rate", 0.90))
    zero_damage = bool(policy.get("zero_regression_damage", True))

    stages: list[dict[str, Any]] = []
    candidate_results: dict[str, str] = {}
    total_questions = 0
    total_top1 = 0
    total_top2 = 0
    metric_case_count = 0
    contamination_findings: list[dict[str, Any]] = []

    for stage_name in STAGE_ORDER:
        cases = selection["stages"].get(stage_name, [])
        rows = []
        for case in cases:
            case_id = case["case_id"]
            env = os.environ.copy()
            env.update({
                "FORTUNE_CASE_ID": case_id,
                "FORTUNE_CANDIDATE_VERSION": candidate_version,
                "FORTUNE_FROZEN_VERSION": frozen_version,
            })
            proc = subprocess.run(
                [runner, case_id],
                capture_output=True,
                text=True,
                env=env,
                timeout=int(case.get("timeout_seconds", 1800)),
            )
            status = "PASS" if proc.returncode == 0 else "FAIL"
            metrics = _parse_runner_metrics(proc.stdout)
            row = {
                "case_id": case_id,
                "status": status,
                "returncode": proc.returncode,
                "stdout_sha256": hashlib.sha256(proc.stdout.encode()).hexdigest(),
                "stderr_sha256": hashlib.sha256(proc.stderr.encode()).hexdigest(),
                "metrics": metrics,
            }
            rows.append(row)
            candidate_results[case_id] = status

            if metrics:
                metric_case_count += 1
                questions = int(metrics.get("question_count", 0))
                total_questions += questions
                total_top1 += int(metrics.get("top1_hits", 0))
                total_top2 += int(metrics.get("top2_hits", 0))
                contamination_reasons = []
                if metrics.get("answer_payload_present") is not False:
                    contamination_reasons.append("ANSWER_PAYLOAD_NOT_DENIED")
                if metrics.get("old_prediction_payload_present") is not False:
                    contamination_reasons.append("OLD_PREDICTION_PAYLOAD_NOT_DENIED")
                if metrics.get("case_specific_rule_detected") is True:
                    contamination_reasons.append("CASE_SPECIFIC_RULE_DETECTED")
                if metrics.get("clean_cold_start") is not True:
                    contamination_reasons.append("CLEAN_COLD_START_NOT_PROVEN")
                if contamination_reasons:
                    contamination_findings.append({
                        "case_id": case_id,
                        "reasons": contamination_reasons,
                    })

        stages.append({
            "stage": stage_name,
            "cases": rows,
            "status": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
        })
        if any(r["status"] == "FAIL" for r in rows):
            break

    damage = sum(
        1
        for case_id, old in baseline.get("case_results", {}).items()
        if old == "PASS" and candidate_results.get(case_id) == "FAIL"
    )
    all_pass = len(stages) == len(STAGE_ORDER) and all(s["status"] == "PASS" for s in stages)
    top1_rate = total_top1 / total_questions if total_questions else None
    top2_rate = total_top2 / total_questions if total_questions else None

    mastery_measured = total_questions > 0
    mastery_pass = bool(
        mastery_measured
        and top1_rate is not None
        and top2_rate is not None
        and top1_rate >= target_top1
        and top2_rate >= target_top2
    )

    if contamination_findings:
        decision = "REJECTED_CONTAMINATION"
    elif not all_pass:
        decision = "REJECTED"
    elif zero_damage and damage > 0:
        decision = "CONTINUE_LEARNING_REGRESSION_REPAIR"
    elif mastery_measured and not mastery_pass:
        decision = "CONTINUE_LEARNING_BELOW_MASTERY"
    elif mastery_pass:
        decision = "TRAINING_MASTERY_GATE_PASS"
    else:
        decision = "REGRESSION_PASS_COMPATIBILITY_NO_MASTERY_METRICS"

    result = {
        "schema": "PATCH-AND-REGRESSION-V2",
        "regression_id": f"REG-{candidate_version}",
        "candidate_version": candidate_version,
        "frozen_version": frozen_version,
        "stages": stages,
        "damage": damage,
        "damage_tolerance": 0 if zero_damage else policy.get("damage_tolerance"),
        "mastery": {
            "measured": mastery_measured,
            "metric_case_count": metric_case_count,
            "question_count": total_questions,
            "top1_hits": total_top1,
            "top1_rate": top1_rate,
            "top1_target": target_top1,
            "top2_hits": total_top2,
            "top2_rate": top2_rate,
            "top2_target": target_top2,
            "status": "PASS" if mastery_pass else "NOT_PASS",
            "claim_boundary": "TRAINING_SET_ONLY_NOT_UNSEEN_GENERALIZATION",
        },
        "contamination_findings": contamination_findings,
        "decision": decision,
        "created_at": utc_now(),
    }
    atomic_write_json(output_path, result)
    return result
