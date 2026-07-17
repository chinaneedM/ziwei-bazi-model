from __future__ import annotations

from pathlib import Path
from typing import Any

from .snapshot import _contains_forbidden
from .util import FortuneError, atomic_write_json, canonical_bytes, read_json, sha256_bytes, sha256_file, slug, utc_now

TRACK_LIBS = {
    "ZIWEI": {f"S{i:02d}" for i in range(5, 11)},
    "BAZI": {f"S{i:02d}" for i in range(11, 17)},
}
SHARED_LIBS = {"S01", "S02", "S04", "S17", "S18"}
FORBIDDEN_BLIND_KEYS = {
    "question_id", "option_id", "option_ids", "options", "top1", "top2",
    "pairwise_rows", "direction_matrix", "compound_coverage", "formal_exact_assertion",
}


def _walk_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(str(key).lower())
            keys |= _walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            keys |= _walk_keys(child)
    return keys


def validate_blind_track_model(obj: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if obj.get("schema") != "BLIND-TRACK-MODEL-V1": errors.append("SCHEMA_INVALID")
    track = obj.get("track")
    if track not in TRACK_LIBS: errors.append("TRACK_INVALID")
    if not obj.get("case_id"): errors.append("CASE_ID_MISSING")
    if obj.get("phase") != "PRE_OPTION": errors.append("PHASE_NOT_PRE_OPTION")
    if obj.get("option_visibility") is not False: errors.append("OPTION_VISIBILITY_NOT_FALSE")
    if obj.get("other_track_visibility") is not False: errors.append("OTHER_TRACK_VISIBILITY_NOT_FALSE")
    if obj.get("answer_access_performed") is not False: errors.append("ANSWER_ACCESS_ATTESTATION_INVALID")
    if _contains_forbidden(obj): errors.append("ANSWER_FIELD_OR_TEXT_DETECTED")
    if _walk_keys(obj) & FORBIDDEN_BLIND_KEYS: errors.append("OPTION_OR_ADJUDICATION_KEY_DETECTED")
    parents = obj.get("parent_libraries")
    if not isinstance(parents, list) or not parents: errors.append("PARENT_LIBRARIES_MISSING")
    elif track in TRACK_LIBS:
        parent_set = set(parents)
        if not parent_set & TRACK_LIBS[track]: errors.append("LOCAL_PARENT_CHAIN_MISSING")
        other = "BAZI" if track == "ZIWEI" else "ZIWEI"
        if parent_set & TRACK_LIBS[other]: errors.append("CROSS_TRACK_PARENT_CONTAMINATION")
        if not parent_set <= TRACK_LIBS[track] | SHARED_LIBS: errors.append("UNKNOWN_PARENT_LIBRARY")
    body = obj.get("blind_model")
    if not isinstance(body, dict) or not body: errors.append("BLIND_MODEL_BODY_MISSING")
    return {"status": "PASS" if not errors else "FAIL", "errors": errors}


def seal_blind_track_model(candidate_path: str | Path, frozen_root: str | Path) -> dict[str, Any]:
    obj = read_json(candidate_path)
    validation = validate_blind_track_model(obj)
    if validation["status"] != "PASS":
        raise FortuneError("blind track validation failed: " + ";".join(validation["errors"]), status="BLIND_TRACK_VALIDATION_FAIL")
    model_hash = sha256_bytes(canonical_bytes(obj["blind_model"]))
    seal_id = slug(f"BLIND-{obj['case_id']}-{obj['track']}-{model_hash[:16]}")
    target_dir = Path(frozen_root) / seal_id
    if target_dir.exists(): raise FortuneError("blind seal already exists", status="RUN_ID_ALREADY_EXISTS")
    target_dir.mkdir(parents=True)
    frozen_path = target_dir / "blind-track-model.json"
    frozen = dict(obj)
    frozen["blind_model_hash"] = model_hash
    frozen["machine_validation"] = validation
    atomic_write_json(frozen_path, frozen)
    frozen_path.chmod(0o444)
    receipt = {
        "schema": "BLIND-TRACK-SEAL-RECEIPT-V1",
        "seal_id": seal_id,
        "case_id": obj["case_id"],
        "track": obj["track"],
        "blind_model_hash": model_hash,
        "body_hash": sha256_file(frozen_path),
        "validation_status": "PASS",
        "validation_errors": [],
        "frozen_path": str(frozen_path),
        "sealed_at": utc_now(),
        "option_visibility": False,
        "other_track_visibility": False,
        "answer_access_performed": False,
        "immutable": True,
        "non_overwrite": True,
    }
    receipt_path = target_dir / "blind-track-seal-receipt.json"
    atomic_write_json(receipt_path, receipt)
    receipt_path.chmod(0o444)
    return receipt


def validate_local_adjudication(obj: dict[str, Any], blind_receipt: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if obj.get("schema") != "TRACK-LOCAL-ADJUDICATION-V1": errors.append("SCHEMA_INVALID")
    if obj.get("case_id") != blind_receipt.get("case_id"): errors.append("CASE_ID_MISMATCH")
    if obj.get("track") != blind_receipt.get("track"): errors.append("TRACK_MISMATCH")
    if obj.get("blind_model_hash") != blind_receipt.get("blind_model_hash"): errors.append("BLIND_MODEL_HASH_MISMATCH")
    if not obj.get("question_id"): errors.append("QUESTION_ID_MISSING")
    if not obj.get("s18_local_adjudication_object_id"): errors.append("S18_OBJECT_ID_MISSING")
    if obj.get("answer_access_performed") is not False: errors.append("ANSWER_ACCESS_ATTESTATION_INVALID")
    if obj.get("other_track_visibility") is not False: errors.append("OTHER_TRACK_VISIBILITY_NOT_FALSE")
    if _contains_forbidden(obj): errors.append("ANSWER_FIELD_OR_TEXT_DETECTED")
    parents = obj.get("parent_object_ids")
    if not isinstance(parents, list) or not parents: errors.append("PARENT_OBJECTS_MISSING")
    return {"status": "PASS" if not errors else "FAIL", "errors": errors}


def create_local_track_seal(adjudication_path: str | Path, blind_receipt_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    adjudication = read_json(adjudication_path)
    blind_receipt = read_json(blind_receipt_path)
    validation = validate_local_adjudication(adjudication, blind_receipt)
    if validation["status"] != "PASS":
        raise FortuneError("local adjudication validation failed: " + ";".join(validation["errors"]), status="LOCAL_ADJUDICATION_VALIDATION_FAIL")
    body_hash = sha256_file(adjudication_path)
    report_id = slug(f"TRACK-VALIDATION-{adjudication['case_id']}-{adjudication['question_id']}-{adjudication['track']}-{body_hash[:12]}")
    seal_base = {
        "seal_id": slug(f"LOCAL-{adjudication['case_id']}-{adjudication['question_id']}-{adjudication['track']}-{body_hash[:12]}"),
        "body_hash": body_hash,
        "machine_validation_report_id": report_id,
        "validation_status": "PASS",
        "s18_local_adjudication_object_id": adjudication["s18_local_adjudication_object_id"],
        "parent_object_ids": [blind_receipt["seal_id"], *adjudication["parent_object_ids"]],
    }
    seal = dict(seal_base)
    seal["canonical_hash"] = sha256_bytes(canonical_bytes(seal_base))
    atomic_write_json(output_path, seal)
    return seal
