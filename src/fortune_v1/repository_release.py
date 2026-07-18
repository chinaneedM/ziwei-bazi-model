from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from .contamination import assert_knowledge_source_path, classify_repository_path
from .util import FortuneError, atomic_write_json, canonical_bytes, read_json, sha256_bytes, sha256_file, slug, utc_now

LIBRARIES = tuple(f"S{i:02d}" for i in range(20))
METHOD_STAGES = (
    "INPUT_AND_LITERAL_OPTION_FREEZE", "COMPLETE_KNOWLEDGE_COVERAGE",
    "ZIWEI_BLIND_TRACK", "BAZI_BLIND_TRACK", "NEUTRAL_TIME_FACTS",
    "PERSON_TAIJI_AND_ENTITY_TOPOLOGY", "REALITY_OCCURRENCE_AND_ENDPOINT_CLOSURE",
    "COMMON_ATOM_SUBTRACTION", "OPTION_ATOM_DIRECTION_MATRIX",
    "FULL_PAIRWISE_ADJUDICATION", "TRACK_INDEPENDENCE_AND_FUSION",
    "PUBLIC_RELATIVE_AND_FORMAL_RELEASE",
)


def object_hash(value: dict[str, Any]) -> str:
    body = dict(value)
    body.pop("object_hash", None)
    return sha256_bytes(canonical_bytes(body))


def write_object(path: str | Path, value: dict[str, Any], *, overwrite: bool = False) -> dict[str, Any]:
    body = dict(value)
    body["object_hash"] = object_hash(body)
    atomic_write_json(path, body, overwrite=overwrite)
    return body


def source_rows(source_dir: str | Path) -> list[dict[str, Any]]:
    root = Path(source_dir)
    assert_knowledge_source_path(root)
    found: dict[str, dict[str, Any]] = {}
    for path in sorted(root.glob("S??_*.txt")):
        assert_knowledge_source_path(path)
        lib = path.name[:3].upper()
        if lib not in LIBRARIES or lib in found:
            raise FortuneError(f"invalid or duplicate library: {path.name}", status="KNOWLEDGE_SOURCE_SET_INVALID")
        found[lib] = {
            "library_id": lib,
            "canonical_filename": path.name,
            "repository_relative_path": path.as_posix(),
            "sha256_raw_file_bytes": sha256_file(path),
            "file_size_bytes": path.stat().st_size,
        }
    missing = [lib for lib in LIBRARIES if lib not in found]
    if missing or len(found) != 20:
        raise FortuneError(f"knowledge source set incomplete: {missing}", status="KNOWLEDGE_SOURCE_SET_INVALID")
    return [found[lib] for lib in LIBRARIES]


def build_knowledge_manifest(source_dir: str | Path, output: str | Path, *, release_id: str,
                             repository: str, commit_sha: str, s19_binding_sha256: str,
                             release_kind: str = "CANDIDATE", parent_release_id: str | None = None) -> dict[str, Any]:
    return write_object(output, {
        "schema": "FORTUNE-KNOWLEDGE-RELEASE-MANIFEST-V1",
        "knowledge_release_id": slug(release_id),
        "release_kind": release_kind,
        "parent_release_id": parent_release_id,
        "repository_full_name": repository,
        "repository_commit_sha": commit_sha,
        "source_root": Path(source_dir).as_posix(),
        "source_authority": "GITHUB_REPOSITORY",
        "source_file_count": 20,
        "source_files": source_rows(source_dir),
        "s19_binding_sha256": s19_binding_sha256,
        "immutability": "NO_IN_PLACE_MUTATION",
        "legacy_contamination_policy": "HISTORICAL_AND_RESEARCH_PATHS_PROHIBITED_FROM_RUNTIME_PACKETS",
        "score_eligibility": "BLOCKED_PENDING_CAUSAL_SHADOW_VALIDATION",
        "created_at": utc_now(),
    })


def validate_knowledge_manifest(manifest_path: str | Path, source_dir: str | Path | None = None) -> dict[str, Any]:
    manifest = read_json(manifest_path)
    errors: list[str] = []
    rows = manifest.get("source_files", [])
    if manifest.get("schema") != "FORTUNE-KNOWLEDGE-RELEASE-MANIFEST-V1": errors.append("SCHEMA_INVALID")
    if [row.get("library_id") for row in rows] != list(LIBRARIES): errors.append("LIBRARY_SET_INVALID")
    if manifest.get("object_hash") != object_hash(manifest): errors.append("OBJECT_HASH_MISMATCH")
    try:
        assert_knowledge_source_path(manifest.get("source_root", ""))
    except FortuneError as exc:
        errors.append(exc.status)
    for index, row in enumerate(rows):
        try:
            assert_knowledge_source_path(row.get("repository_relative_path", ""))
        except FortuneError as exc:
            errors.append(f"SOURCE_{index}:{exc.status}")
    readback = []
    if source_dir:
        for row in rows:
            path = Path(source_dir) / row["canonical_filename"]
            status = "PASS"
            if not path.is_file(): status = "MISSING"
            elif sha256_file(path) != row["sha256_raw_file_bytes"]: status = "HASH_MISMATCH"
            elif path.stat().st_size != row["file_size_bytes"]: status = "SIZE_MISMATCH"
            readback.append({"library_id": row["library_id"], "path": path.as_posix(), "status": status})
            if status != "PASS": errors.append(f"{row['library_id']}:{status}")
    return {
        "schema": "FORTUNE-KNOWLEDGE-RELEASE-VALIDATION-V1",
        "knowledge_release_id": manifest.get("knowledge_release_id"),
        "manifest_sha256": sha256_file(manifest_path),
        "source_file_count": len(rows), "readback": readback, "errors": errors,
        "legacy_contamination_gate": "PASS" if not any("PATH_" in error for error in errors) else "FAIL_CLOSED",
        "status": "PASS" if not errors else "FAIL_CLOSED",
    }


def validate_method_release(method_path: str | Path) -> dict[str, Any]:
    method = read_json(method_path)
    errors: list[str] = []
    if method.get("schema") != "FORTUNE-METHOD-RELEASE-V1": errors.append("SCHEMA_INVALID")
    stages = method.get("stages", [])
    ids = [stage.get("stage_id") for stage in stages]
    missing = [stage for stage in METHOD_STAGES if stage not in ids]
    if missing: errors.append("MISSING_STAGES:" + ",".join(missing))
    for stage in stages:
        if not stage.get("rules"): errors.append(f"RULES_MISSING:{stage.get('stage_id')}")
    if method.get("object_hash") != object_hash(method): errors.append("OBJECT_HASH_MISMATCH")
    return {
        "schema": "FORTUNE-METHOD-RELEASE-VALIDATION-V1",
        "method_release_id": method.get("method_release_id"),
        "method_release_sha256": sha256_file(method_path),
        "errors": errors, "status": "PASS" if not errors else "FAIL_CLOSED",
    }


def build_method_packet(method_path: str | Path, output: str | Path) -> dict[str, Any]:
    validation = validate_method_release(method_path)
    if validation["status"] != "PASS":
        raise FortuneError("method release invalid", status="METHOD_RELEASE_INVALID")
    method = read_json(method_path)
    rules = []
    for stage in method["stages"]:
        for rule in stage["rules"]:
            rules.append({"stage_id": stage["stage_id"], "method_rule_id": rule["rule_id"],
                          "source_authority": rule["source_authority"], "requirement": rule["requirement"],
                          "failure_status": rule["failure_status"]})
    return write_object(output, {
        "schema": "FORTUNE-METHOD-PACKET-V1",
        "method_release_id": method["method_release_id"],
        "method_release_path": Path(method_path).as_posix(),
        "method_release_sha256": sha256_file(method_path),
        "mandatory_stage_ids": list(METHOD_STAGES), "rules": rules,
        "answer_or_option_specific_rule_permission": "NO",
        "historical_method_fallback_permission": "NO",
        "created_at": utc_now(),
    })


def validate_prompt_snapshot_receipt(receipt_path: str | Path,
                                     expected_runtime_id: str | None = None) -> dict[str, Any]:
    receipt_file = Path(receipt_path)
    receipt = read_json(receipt_file)
    errors: list[str] = []
    if receipt.get("schema") != "MAIN-PROMPT-AUDIT-SNAPSHOT-V1":
        errors.append("PROMPT_SNAPSHOT_SCHEMA_INVALID")
    if receipt.get("status") != "PASS":
        errors.append("PROMPT_SNAPSHOT_STATUS_NOT_PASS")
    if receipt.get("object_hash") != object_hash(receipt):
        errors.append("PROMPT_SNAPSHOT_RECEIPT_OBJECT_HASH_MISMATCH")
    if expected_runtime_id and receipt.get("runtime_id") != expected_runtime_id:
        errors.append("PROMPT_RUNTIME_ID_MISMATCH")
    for label, path in (("RECEIPT", receipt_file), ("SNAPSHOT", Path(receipt.get("snapshot_path", "")))):
        classification = classify_repository_path(path)
        if classification.get("classification") != "VERSIONED_MODEL_OBJECT":
            errors.append(f"PROMPT_{label}_PATH_NOT_VERSIONED_MODEL")
    snapshot_path = Path(receipt.get("snapshot_path", ""))
    if not snapshot_path.is_file():
        errors.append("PROMPT_SNAPSHOT_MISSING")
    else:
        if sha256_file(snapshot_path) != receipt.get("snapshot_sha256"):
            errors.append("PROMPT_SNAPSHOT_HASH_MISMATCH")
        if snapshot_path.stat().st_size != receipt.get("snapshot_bytes"):
            errors.append("PROMPT_SNAPSHOT_SIZE_MISMATCH")
    return {
        "schema": "MAIN-PROMPT-AUDIT-SNAPSHOT-VALIDATION-V1",
        "runtime_id": receipt.get("runtime_id"),
        "receipt_path": receipt_file.as_posix(),
        "receipt_sha256": sha256_file(receipt_file),
        "snapshot_path": snapshot_path.as_posix(),
        "snapshot_sha256": receipt.get("snapshot_sha256"),
        "snapshot_bytes": receipt.get("snapshot_bytes"),
        "errors": errors,
        "status": "PASS" if not errors else "FAIL_CLOSED",
    }


def build_model_release(knowledge_manifest_path: str | Path, method_release_path: str | Path,
                        prompt_snapshot_receipt_path: str | Path, output: str | Path, *,
                        model_release_id: str, main_prompt_runtime_id: str,
                        code_commit_sha: str, source_packet_schema: str = "FORTUNE-SOURCE-PACKET-V1") -> dict[str, Any]:
    knowledge = read_json(knowledge_manifest_path)
    method = read_json(method_release_path)
    if validate_knowledge_manifest(knowledge_manifest_path)["status"] != "PASS":
        raise FortuneError("knowledge manifest invalid", status="MODEL_KNOWLEDGE_INVALID")
    if validate_method_release(method_release_path)["status"] != "PASS":
        raise FortuneError("method release invalid", status="MODEL_METHOD_INVALID")
    prompt_validation = validate_prompt_snapshot_receipt(
        prompt_snapshot_receipt_path, expected_runtime_id=main_prompt_runtime_id,
    )
    if prompt_validation["status"] != "PASS":
        raise FortuneError("prompt snapshot invalid", status="MODEL_PROMPT_SNAPSHOT_INVALID")
    if method.get("main_prompt_runtime_id") not in {None, main_prompt_runtime_id}:
        raise FortuneError("method prompt binding mismatch", status="MODEL_METHOD_PROMPT_BINDING_MISMATCH")
    if knowledge.get("prompt_runtime_id") not in {None, main_prompt_runtime_id}:
        raise FortuneError("knowledge prompt binding mismatch", status="MODEL_KNOWLEDGE_PROMPT_BINDING_MISMATCH")
    return write_object(output, {
        "schema": "FORTUNE-MODEL-RELEASE-V1", "model_release_id": slug(model_release_id),
        "main_prompt_runtime_id": main_prompt_runtime_id,
        "main_prompt_snapshot_path": prompt_validation["snapshot_path"],
        "main_prompt_snapshot_sha256": prompt_validation["snapshot_sha256"],
        "main_prompt_snapshot_size_bytes": prompt_validation["snapshot_bytes"],
        "main_prompt_snapshot_receipt_path": Path(prompt_snapshot_receipt_path).as_posix(),
        "main_prompt_snapshot_receipt_sha256": prompt_validation["receipt_sha256"],
        "knowledge_release_id": knowledge["knowledge_release_id"],
        "knowledge_manifest_path": Path(knowledge_manifest_path).as_posix(),
        "knowledge_manifest_sha256": sha256_file(knowledge_manifest_path),
        "method_release_id": method["method_release_id"],
        "method_release_path": Path(method_release_path).as_posix(),
        "method_release_sha256": sha256_file(method_release_path),
        "code_commit_sha": code_commit_sha,
        "s19_binding_sha256": knowledge["s19_binding_sha256"],
        "source_packet_schema": source_packet_schema,
        "source_files": knowledge["source_files"],
        "project_upload_fallback_permission": "NO",
        "historical_training_trace_permission": "NO",
        "research_hypothesis_direct_runtime_permission": "NO",
        "score_eligibility": "BLOCKED_PENDING_REPOSITORY_ONLY_SHADOW_VALIDATION",
        "formal_release": "NO", "created_at": utc_now(),
    })


def promote_candidate(candidate_dir: str | Path, manifest_path: str | Path, releases_root: str | Path,
                      active_pointer: str | Path, receipt_path: str | Path, *, approval_id: str,
                      expected_previous_release_id: str | None = None) -> dict[str, Any]:
    validation = validate_knowledge_manifest(manifest_path, candidate_dir)
    if validation["status"] != "PASS": raise FortuneError("candidate invalid", status="CANDIDATE_INVALID")
    current = read_json(active_pointer) if Path(active_pointer).exists() else {}
    if expected_previous_release_id is not None and current.get("knowledge_release_id") != expected_previous_release_id:
        raise FortuneError("active pointer moved", status="ACTIVE_POINTER_COMPARE_AND_SWAP_FAILED")
    manifest = read_json(manifest_path)
    target = Path(releases_root) / slug(manifest["knowledge_release_id"])
    if target.exists(): raise FortuneError("release already exists", status="IMMUTABLE_OBJECT_EXISTS")
    shutil.copytree(candidate_dir, target)
    target_manifest = target / Path(manifest_path).name
    if validate_knowledge_manifest(target_manifest, target)["status"] != "PASS":
        shutil.rmtree(target); raise FortuneError("release readback failed", status="RELEASE_READBACK_FAILED")
    write_object(active_pointer, {
        "schema": "FORTUNE-ACTIVE-KNOWLEDGE-RELEASE-POINTER-V1",
        "knowledge_release_id": manifest["knowledge_release_id"],
        "manifest_path": target_manifest.as_posix(), "manifest_sha256": sha256_file(target_manifest),
        "previous_release_id": current.get("knowledge_release_id"), "approval_id": approval_id,
        "activation_reason": "CANDIDATE_PROMOTION", "activated_at": utc_now(),
    }, overwrite=True)
    return write_object(receipt_path, {
        "schema": "FORTUNE-KNOWLEDGE-PROMOTION-RECEIPT-V1", "status": "PASS",
        "knowledge_release_id": manifest["knowledge_release_id"],
        "previous_release_id": current.get("knowledge_release_id"), "approval_id": approval_id,
        "release_manifest_sha256": sha256_file(target_manifest), "completed_at": utc_now(),
    })


def rollback_release(target_manifest_path: str | Path, active_pointer: str | Path,
                     receipt_path: str | Path, *, reason: str, approval_id: str) -> dict[str, Any]:
    target = read_json(target_manifest_path)
    if validate_knowledge_manifest(target_manifest_path)["status"] != "PASS":
        raise FortuneError("rollback target invalid", status="ROLLBACK_TARGET_INVALID")
    current = read_json(active_pointer)
    write_object(active_pointer, {
        "schema": "FORTUNE-ACTIVE-KNOWLEDGE-RELEASE-POINTER-V1",
        "knowledge_release_id": target["knowledge_release_id"],
        "manifest_path": Path(target_manifest_path).as_posix(),
        "manifest_sha256": sha256_file(target_manifest_path),
        "previous_release_id": current.get("knowledge_release_id"),
        "activation_reason": "ROLLBACK", "approval_id": approval_id, "activated_at": utc_now(),
    }, overwrite=True)
    return write_object(receipt_path, {
        "schema": "FORTUNE-KNOWLEDGE-ROLLBACK-RECEIPT-V1", "status": "PASS",
        "from_release_id": current.get("knowledge_release_id"),
        "to_release_id": target["knowledge_release_id"], "reason": reason,
        "approval_id": approval_id, "completed_at": utc_now(),
    })
