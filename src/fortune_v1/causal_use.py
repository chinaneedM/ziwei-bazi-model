from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .contamination import runtime_reference_violations
from .repository_release import METHOD_STAGES, object_hash, write_object
from .util import read_json, sha256_file, utc_now

RUN_CONTRACT_SCHEMA = "REPOSITORY-PREDICTION-RUN-CONTRACT-V1"
PROJECT_PATTERNS = (
    re.compile(r"(?:^|[/\\])mnt[/\\]data(?:[/\\]|$)", re.I),
    re.compile(r"file_[0-9a-f]{16,}", re.I),
    re.compile(r"PROJECT[_ -]?UPLOAD", re.I),
)


def build_run_contract(model_release_path: str | Path, source_packet_path: str | Path,
                       method_packet_path: str | Path, case_freeze_path: str | Path,
                       output: str | Path, *, run_id: str, case_id: str,
                       dataset_type: str, question_rows: list[dict[str, Any]]) -> dict[str, Any]:
    model = read_json(model_release_path); source = read_json(source_packet_path)
    method = read_json(method_packet_path); case = read_json(case_freeze_path)
    normalized_questions = []
    for row in question_rows:
        options = row.get("option_ids")
        if not options and isinstance(row.get("options"), list):
            options = [item.get("option_id") or item.get("id") for item in row["options"]]
        options = [item for item in (options or []) if item]
        normalized_questions.append({
            "question_id": row.get("question_id"), "option_ids": options,
            "required_pairwise_rows": row.get("required_pairwise_rows", len(options) * (len(options) - 1) // 2),
        })
    binding = {
        "model_release_id": model["model_release_id"],
        "main_prompt_runtime_id": model["main_prompt_runtime_id"],
        "knowledge_release_id": model["knowledge_release_id"],
        "method_release_id": model["method_release_id"],
        "code_commit_sha": model["code_commit_sha"],
        "s19_binding_sha256": model["s19_binding_sha256"],
        "source_packet_schema": source["schema"],
        "source_packet_sha256": sha256_file(source_packet_path),
        "method_packet_sha256": sha256_file(method_packet_path),
    }
    return write_object(output, {
        "schema": RUN_CONTRACT_SCHEMA, "run_id": run_id, "case_id": case_id,
        "dataset_type": dataset_type,
        "snapshot": {"path": Path(case_freeze_path).as_posix(),
                     "sha256": sha256_file(case_freeze_path),
                     "case_input_hash": case.get("case_input_hash") or case.get("object_hash")},
        "binding": binding,
        "model_release": {"path": Path(model_release_path).as_posix(), "sha256": sha256_file(model_release_path)},
        "source_packet": {"path": Path(source_packet_path).as_posix(), "sha256": sha256_file(source_packet_path)},
        "method_packet": {"path": Path(method_packet_path).as_posix(), "sha256": sha256_file(method_packet_path)},
        "questions": normalized_questions,
        "answer_data_available": False,
        "answer_isolation_declaration": "PHYSICALLY_INACCESSIBLE",
        "project_upload_access": "DENIED_AND_NOT_USED",
        "legacy_contamination_access": "DENIED_AND_NOT_USED",
        "historical_training_trace_access": "DENIED_AND_NOT_USED",
        "research_hypothesis_access": "DENIED_UNLESS_PROMOTED_AND_RELEASE_BOUND",
        "fallback_policy": "FAIL_CLOSED_NO_PROJECT_UPLOAD_FALLBACK",
        "contract_frozen_before_reasoning": True,
        "source_authority": "GITHUB_REPOSITORY_SOURCE_PACKET_ONLY",
        "formal_release": "NO", "created_at": utc_now(),
    })


def _project_refs(value: Any, path: str = "$") -> list[str]:
    refs: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items(): refs.extend(_project_refs(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value): refs.extend(_project_refs(child, f"{path}[{index}]"))
    elif isinstance(value, str) and any(pattern.search(value) for pattern in PROJECT_PATTERNS):
        refs.append(path)
    return refs


def validate_causal_use(prediction_path: str | Path, contract_path: str | Path,
                        output: str | Path | None = None) -> dict[str, Any]:
    prediction = read_json(prediction_path); contract = read_json(contract_path); errors: list[str] = []
    if contract.get("schema") != RUN_CONTRACT_SCHEMA: errors.append("RUN_CONTRACT_SCHEMA_INVALID")
    if contract.get("contract_frozen_before_reasoning") is not True: errors.append("CONTRACT_NOT_FROZEN_BEFORE_REASONING")
    if contract.get("answer_data_available") is not False: errors.append("ANSWER_ISOLATION_FAILED")
    if contract.get("project_upload_access") != "DENIED_AND_NOT_USED": errors.append("PROJECT_UPLOAD_NON_USE_NOT_PROVEN")
    if contract.get("legacy_contamination_access") != "DENIED_AND_NOT_USED": errors.append("LEGACY_CONTAMINATION_NON_USE_NOT_PROVEN")
    if contract.get("historical_training_trace_access") != "DENIED_AND_NOT_USED": errors.append("HISTORICAL_TRAINING_TRACE_NON_USE_NOT_PROVEN")
    if contract.get("research_hypothesis_access") != "DENIED_UNLESS_PROMOTED_AND_RELEASE_BOUND": errors.append("RESEARCH_HYPOTHESIS_ACCESS_POLICY_INVALID")
    if contract.get("fallback_policy") != "FAIL_CLOSED_NO_PROJECT_UPLOAD_FALLBACK": errors.append("SILENT_FALLBACK_POLICY_INVALID")

    loaded: dict[str, dict[str, Any]] = {}
    for key, label in (("model_release", "MODEL_RELEASE"), ("source_packet", "SOURCE_PACKET"), ("method_packet", "METHOD_PACKET")):
        row = contract.get(key, {}); path = Path(row.get("path", "")); expected = row.get("sha256")
        if not path.is_file(): errors.append(label + "_MISSING"); loaded[key] = {}; continue
        if sha256_file(path) != expected: errors.append(label + "_HASH_MISMATCH")
        loaded[key] = read_json(path)

    model = loaded.get("model_release", {}); source = loaded.get("source_packet", {})
    method = loaded.get("method_packet", {}); binding = contract.get("binding", {})
    if model.get("model_release_id") != binding.get("model_release_id"): errors.append("MODEL_RELEASE_MISMATCH")
    if model.get("main_prompt_runtime_id") != binding.get("main_prompt_runtime_id"): errors.append("MAIN_PROMPT_BINDING_MISMATCH")
    if model.get("code_commit_sha") != binding.get("code_commit_sha"): errors.append("CODE_COMMIT_BINDING_MISMATCH")
    if model.get("s19_binding_sha256") != binding.get("s19_binding_sha256"): errors.append("S19_BINDING_MISMATCH")
    if model.get("project_upload_fallback_permission") not in {None, "NO"}: errors.append("MODEL_PROJECT_FALLBACK_PERMISSION_INVALID")
    if model.get("historical_training_trace_permission") not in {None, "NO"}: errors.append("MODEL_HISTORICAL_TRACE_PERMISSION_INVALID")
    if model.get("research_hypothesis_direct_runtime_permission") not in {None, "NO"}: errors.append("MODEL_RESEARCH_DIRECT_RUNTIME_PERMISSION_INVALID")
    if source.get("knowledge_release_id") != binding.get("knowledge_release_id"): errors.append("KNOWLEDGE_RELEASE_MISMATCH")
    if method.get("method_release_id") != binding.get("method_release_id"): errors.append("METHOD_RELEASE_MISMATCH")
    if contract.get("source_packet", {}).get("sha256") != binding.get("source_packet_sha256"): errors.append("SOURCE_PACKET_BINDING_MISMATCH")
    if contract.get("method_packet", {}).get("sha256") != binding.get("method_packet_sha256"): errors.append("METHOD_PACKET_BINDING_MISMATCH")

    model_sources = {row.get("library_id"): row for row in model.get("source_files", [])}
    for index, item in enumerate(source.get("items", [])):
        parent = model_sources.get(item.get("library_id"))
        if not parent: errors.append(f"SOURCE_PACKET_ITEM_{index}:MODEL_LIBRARY_UNRESOLVED"); continue
        if item.get("source_sha256") != parent.get("sha256_raw_file_bytes"):
            errors.append(f"SOURCE_PACKET_ITEM_{index}:MODEL_SOURCE_HASH_MISMATCH")
        if item.get("source_size_bytes") != parent.get("file_size_bytes"):
            errors.append(f"SOURCE_PACKET_ITEM_{index}:MODEL_SOURCE_SIZE_MISMATCH")
        if item.get("repository_relative_path") != parent.get("repository_relative_path"):
            errors.append(f"SOURCE_PACKET_ITEM_{index}:MODEL_SOURCE_PATH_MISMATCH")
    items = {item.get("packet_item_id"): item for item in source.get("items", [])}
    valid_rules = {(row.get("stage_id"), row.get("method_rule_id")) for row in method.get("rules", [])}
    ledger_count = 0; stage_count = 0
    for question in prediction.get("questions", []):
        qid = question.get("question_id")
        for index, row in enumerate(question.get("evidence_ledger", [])):
            ledger_count += 1; item = items.get(row.get("packet_item_id")); prefix = f"{qid}:LEDGER_{index}"
            if not item: errors.append(prefix + ":PACKET_ITEM_UNRESOLVED"); continue
            if row.get("source_library") != item.get("library_id"): errors.append(prefix + ":LIBRARY_MISMATCH")
            supplied_hash = row.get("source_file_sha256") or row.get("source_sha256")
            if supplied_hash != item.get("source_sha256"): errors.append(prefix + ":SOURCE_HASH_MISMATCH")
            if row.get("source_root_atom") != item.get("source_root_atom"): errors.append(prefix + ":ROOT_ATOM_MISMATCH")
        receipts = {row.get("stage_id"): row for row in question.get("method_stage_receipts", []) if isinstance(row, dict)}
        for stage in METHOD_STAGES:
            receipt = receipts.get(stage)
            if not receipt: errors.append(f"{qid}:{stage}:STAGE_RECEIPT_MISSING"); continue
            stage_count += 1
            if receipt.get("status") not in {"EXECUTED", "EFFECTIVE", "NOT_APPLICABLE_WITH_REASON"}:
                errors.append(f"{qid}:{stage}:STAGE_STATUS_INVALID")
            rule_ids = receipt.get("method_rule_ids", [])
            if not rule_ids or any((stage, rule_id) not in valid_rules for rule_id in rule_ids):
                errors.append(f"{qid}:{stage}:METHOD_RULE_BINDING_INVALID")
    if ledger_count == 0: errors.append("EVIDENCE_LEDGER_EMPTY")
    refs = _project_refs(prediction) + _project_refs({key: contract.get(key) for key in ("snapshot", "model_release", "source_packet", "method_packet")})
    if refs: errors.append("PROJECT_UPLOAD_REFERENCE_DETECTED:" + ",".join(sorted(set(refs))))
    contamination = runtime_reference_violations({
        "prediction": prediction,
        "contract": contract,
        "model_release": model,
        "source_packet": source,
        "method_packet": method,
    })
    if contamination:
        errors.append(
            "LEGACY_CONTAMINATION_REFERENCE_DETECTED:" +
            ",".join(sorted({row["object_path"] for row in contamination}))
        )
    if prediction.get("binding") != contract.get("binding"): errors.append("PREDICTION_CONTRACT_BINDING_MISMATCH")

    receipt = {
        "schema": "FORTUNE-CAUSAL-USE-RECEIPT-V1",
        "status": "PASS" if not errors else "FAIL_CLOSED",
        "run_id": prediction.get("run_id"), "case_id": prediction.get("case_id"),
        "model_release_id": binding.get("model_release_id"),
        "knowledge_release_id": binding.get("knowledge_release_id"),
        "method_release_id": binding.get("method_release_id"),
        "evidence_ledger_rows_checked": ledger_count,
        "method_stage_receipts_checked": stage_count,
        "project_upload_reference_paths": sorted(set(refs)),
        "legacy_contamination_reference_rows": contamination,
        "legacy_contamination_scan_status": "PASS" if not contamination else "FAIL_CLOSED",
        "errors": errors,
        "score_eligibility": "ELIGIBLE" if not errors else "PROHIBITED",
        "formal_release": "NO", "validated_at": utc_now(),
    }
    receipt["object_hash"] = object_hash(receipt)
    if output: write_object(output, receipt, overwrite=True)
    return receipt
