from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any

from .snapshot import ANSWER_KEYS, _contains_forbidden
from .util import FortuneError, atomic_write_json, read_json, sha256_file, slug, utc_now

ZIWEI_LIBS = {f"S{i:02d}" for i in range(5, 11)}
BAZI_LIBS = {f"S{i:02d}" for i in range(11, 17)}
LEDGER_REQUIRED = {"track", "source_library", "method", "knowledge_point", "source_root_atom", "parent_segment", "physical_selector", "conditions", "limitations_negations_exceptions", "target_atom", "semantic_direction", "capability_ceiling", "temporal_role", "evidence_family", "dedup_status", "downstream_effect"}


def prepare_run_contract(snapshot_manifest_path: str | Path, config_path: str | Path,
                         code_commit: str, output_path: str | Path,
                         prompt_snapshot_sha256: str | None = None) -> dict[str, Any]:
    snapshot, config = read_json(snapshot_manifest_path), read_json(config_path)
    questions = read_json(snapshot["questions_path"])["questions"]
    contract = {
        "schema": "PREDICTION-RUN-CONTRACT-V1", "case_id": snapshot["case_id"], "dataset_type": snapshot["dataset_type"],
        "snapshot": {"path": str(snapshot_manifest_path), "sha256": sha256_file(snapshot_manifest_path), "case_input_hash": snapshot["case_input_hash"]},
        "binding": {"library_binding_hash": config["expected_s19_binding_hash"], "main_prompt_runtime_id": config["main_prompt_runtime_id"],
                    "prompt_snapshot_sha256": prompt_snapshot_sha256, "code_commit": code_commit, "schema_version": config["schema_version"]},
        "questions": [{"question_id": q["question_id"], "option_ids": [o["option_id"] for o in q["options"]],
                       "required_pairwise_rows": len(q["options"]) * (len(q["options"]) - 1) // 2} for q in questions],
        "answer_data_available": False,
        "external_runner_contract": "Runner may read only snapshot paths and verified knowledge/base; it must write a new PREDICTION-RUN-V1 object.",
    }
    atomic_write_json(output_path, contract)
    return contract


def _validate_track(track: dict[str, Any], allowed: set[str], forbidden: set[str], label: str) -> list[str]:
    errors = []
    if track.get("validation_status") != "PASS" or track.get("local_seal") is not True:
        errors.append(f"{label}:LOCAL_SEAL_INVALID")
    parents = set(track.get("parent_libraries", []))
    if not parents & allowed: errors.append(f"{label}:LOCAL_PARENT_CHAIN_MISSING")
    if parents & forbidden: errors.append(f"{label}:CROSS_TRACK_PARENT_CONTAMINATION")
    if not track.get("blind_model_hash"): errors.append(f"{label}:BLIND_MODEL_HASH_MISSING")
    return errors


def validate_prediction_run(run: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    errors, checks = [], []
    if run.get("schema") != "PREDICTION-RUN-V1": errors.append("SCHEMA_INVALID")
    if run.get("case_id") != contract["case_id"]: errors.append("CASE_ID_MISMATCH")
    if run.get("dataset_type") != contract["dataset_type"]: errors.append("DATASET_TYPE_MISMATCH")
    if run.get("binding") != contract["binding"]: errors.append("BINDING_MISMATCH")
    if not run.get("run_id"): errors.append("RUN_ID_MISSING")
    if run.get("cold_start") is not True: errors.append("COLD_START_ATTESTATION_MISSING")
    if run.get("input_snapshot") != {"path": contract["snapshot"]["path"], "sha256": contract["snapshot"]["sha256"]}:
        errors.append("INPUT_SNAPSHOT_MISMATCH")
    if _contains_forbidden(run): errors.append("ANSWER_FIELD_OR_TEXT_DETECTED")
    question_map = {q["question_id"]: q for q in run.get("questions", [])}
    if set(question_map) != {q["question_id"] for q in contract["questions"]}: errors.append("QUESTION_SET_MISMATCH")
    for expected in contract["questions"]:
        qid = expected["question_id"]
        if qid not in question_map: continue
        q = question_map[qid]; option_ids = expected["option_ids"]
        if q.get("option_ids") != option_ids: errors.append(f"{qid}:OPTION_IDS_MISMATCH")
        if q.get("top1") not in option_ids or q.get("top2") not in option_ids or q.get("top1") == q.get("top2"):
            errors.append(f"{qid}:TOP1_TOP2_INVALID")
        if not isinstance(q.get("confidence"), (int, float)) or not 0 <= q["confidence"] <= 1: errors.append(f"{qid}:CONFIDENCE_INVALID")
        evidence = q.get("public_evidence", [])
        if not 3 <= len(evidence) <= 5: errors.append(f"{qid}:PUBLIC_EVIDENCE_COUNT_INVALID")
        families = [e.get("evidence_family") for e in evidence]
        if None in families or len(set(families)) != len(families): errors.append(f"{qid}:PUBLIC_EVIDENCE_NOT_DISTINCT")
        pairwise = q.get("pairwise_rows", [])
        expected_count = expected["required_pairwise_rows"]
        pairs = {tuple(sorted((row.get("left"), row.get("right")))) for row in pairwise}
        if len(pairwise) != expected_count or len(pairs) != expected_count: errors.append(f"{qid}:PAIRWISE_MATRIX_INCOMPLETE")
        if any(row.get("winner") not in {row.get("left"), row.get("right")} for row in pairwise): errors.append(f"{qid}:PAIRWISE_WINNER_INVALID")
        decisive = [row for row in pairwise if {row.get("left"), row.get("right")} == {q.get("top1"), q.get("top2")}]
        if len(decisive) != 1 or decisive[0].get("winner") != q.get("top1"): errors.append(f"{qid}:TOP1_TOP2_NOT_DERIVED_FROM_PAIRWISE")
        errors.extend(_validate_track(q.get("ziwei_track", {}), ZIWEI_LIBS, BAZI_LIBS, f"{qid}:ZIWEI"))
        errors.extend(_validate_track(q.get("bazi_track", {}), BAZI_LIBS, ZIWEI_LIBS, f"{qid}:BAZI"))
        if q.get("ziwei_track", {}).get("blind_model_hash") == q.get("bazi_track", {}).get("blind_model_hash"):
            errors.append(f"{qid}:CROSS_TRACK_BLIND_MODEL_COPY")
        ledger = q.get("evidence_ledger", [])
        if len(ledger) < 3: errors.append(f"{qid}:EVIDENCE_LEDGER_TOO_SHORT")
        for index, entry in enumerate(ledger):
            missing = LEDGER_REQUIRED - set(entry)
            if missing: errors.append(f"{qid}:LEDGER_{index}_MISSING_{','.join(sorted(missing))}")
        if not q.get("coverage_plan") or q["coverage_plan"].get("status") != "COMPLETE": errors.append(f"{qid}:COVERAGE_PLAN_MISSING_OR_INCOMPLETE")
        if set(q.get("direction_matrix", {})) != set(option_ids): errors.append(f"{qid}:DIRECTION_MATRIX_MISSING")
        if set(q.get("compound_coverage", {})) != set(option_ids): errors.append(f"{qid}:COMPOUND_COVERAGE_MISSING")
        if "formal_exact_assertion" not in q: errors.append(f"{qid}:FORMAL_EXACT_ASSERTION_MISSING")
        if not q.get("strongest_competitor_reason"): errors.append(f"{qid}:COMPETITOR_REASON_MISSING")
        if not q.get("most_important_unverified_atom"): errors.append(f"{qid}:UNVERIFIED_ATOM_MISSING")
    checks.append({"rule": "PREDICTION_RUN_OBJECT_BODY", "status": "PASS" if not errors else "FAIL"})
    return {"status": "PASS" if not errors else "FAIL", "errors": errors, "checks": checks}


def freeze_prediction(run_path: str | Path, contract_path: str | Path, frozen_root: str | Path) -> dict[str, Any]:
    run, contract = read_json(run_path), read_json(contract_path)
    validation = validate_prediction_run(run, contract)
    run.setdefault("runtime_validation", validation)
    if validation["status"] != "PASS":
        raise FortuneError("prediction run validation failed: " + ";".join(validation["errors"]), status="PREDICTION_RUNTIME_FAIL")
    if run["runtime_validation"].get("status") != "PASS":
        raise FortuneError("runner did not declare runtime PASS", status="PREDICTION_RUNTIME_FAIL")
    run_id = slug(run["run_id"])
    target_dir = Path(frozen_root) / run_id
    if target_dir.exists(): raise FortuneError("run id already exists", status="RUN_ID_ALREADY_EXISTS")
    target_dir.mkdir(parents=True)
    frozen_run = target_dir / "prediction-run.json"
    atomic_write_json(frozen_run, run); frozen_run.chmod(0o444)
    receipt = {
        "schema": "PREDICTION-FREEZE-RECEIPT-V1", "run_id": run_id, "case_id": run["case_id"],
        "prediction_path": str(frozen_run), "prediction_sha256": sha256_file(frozen_run),
        "contract_path": str(contract_path), "contract_sha256": sha256_file(contract_path),
        "runtime_validation": validation, "freeze_status": "PREDICTION_FROZEN",
        "frozen_at": utc_now(), "immutable": True, "non_overwrite": True,
    }
    receipt_path = target_dir / "freeze-receipt.json"
    atomic_write_json(receipt_path, receipt); receipt_path.chmod(0o444)
    return receipt
