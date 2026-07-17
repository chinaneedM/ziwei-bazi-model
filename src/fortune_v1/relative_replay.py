from __future__ import annotations

from pathlib import Path
from typing import Any

from .prediction import _validate_pairwise
from .snapshot import _contains_forbidden
from .util import FortuneError, atomic_write_json, read_json, sha256_file, slug, utc_now

ALLOWED_TRACK_STATUSES = {"UNSEALED_REPLAY_ONLY", "VERSION_CONFLICT_UNSEALED"}


def validate_relative_replay(obj: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if obj.get("schema") != "RELATIVE-PREDICTION-REPLAY-V1":
        errors.append("SCHEMA_INVALID")
    if not obj.get("run_id"):
        errors.append("RUN_ID_MISSING")
    if not obj.get("case_id"):
        errors.append("CASE_ID_MISSING")
    if obj.get("cold_start") is not True:
        errors.append("COLD_START_ATTESTATION_MISSING")
    if obj.get("answer_access_performed") is not False:
        errors.append("ANSWER_ACCESS_ATTESTATION_INVALID")
    if obj.get("retrospective_replay") is not True:
        errors.append("RETROSPECTIVE_REPLAY_ATTESTATION_MISSING")
    if obj.get("formal_validity") != "INVALID_UNSEALED":
        errors.append("FORMAL_VALIDITY_MUST_BE_INVALID_UNSEALED")
    if _contains_forbidden(obj):
        errors.append("ANSWER_FIELD_OR_TEXT_DETECTED")

    input_reference = obj.get("input_reference")
    if not isinstance(input_reference, dict):
        errors.append("INPUT_REFERENCE_MISSING")
    else:
        for field in ("kind", "path", "sha256"):
            if not isinstance(input_reference.get(field), str) or not input_reference[field].strip():
                errors.append(f"INPUT_REFERENCE_{field.upper()}_INVALID")

    questions = obj.get("questions")
    if not isinstance(questions, list) or not questions:
        errors.append("QUESTIONS_MISSING")
        questions = []
    seen: set[str] = set()
    for q in questions:
        qid = q.get("question_id") if isinstance(q, dict) else None
        if not isinstance(qid, str) or not qid:
            errors.append("QUESTION_ID_INVALID")
            continue
        if qid in seen:
            errors.append(f"{qid}:DUPLICATE")
        seen.add(qid)
        option_ids = q.get("option_ids")
        if not isinstance(option_ids, list) or len(option_ids) < 2 or len(option_ids) != len(set(option_ids)):
            errors.append(f"{qid}:OPTION_IDS_INVALID")
            continue
        if q.get("top1") not in option_ids or q.get("top2") not in option_ids or q.get("top1") == q.get("top2"):
            errors.append(f"{qid}:TOP1_TOP2_INVALID")
        confidence = q.get("confidence")
        if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            errors.append(f"{qid}:CONFIDENCE_INVALID")
        errors.extend(_validate_pairwise(qid, q, option_ids, len(option_ids) * (len(option_ids) - 1) // 2))
        if q.get("formal_exact_assertion") is not None:
            errors.append(f"{qid}:FORMAL_EXACT_ASSERTION_MUST_BE_NULL")
        tracks = q.get("track_replay_status")
        if not isinstance(tracks, dict):
            errors.append(f"{qid}:TRACK_REPLAY_STATUS_MISSING")
        else:
            for track in ("ziwei", "bazi"):
                status = tracks.get(track)
                if status not in ALLOWED_TRACK_STATUSES:
                    errors.append(f"{qid}:{track.upper()}:TRACK_STATUS_INVALID")
        if not q.get("strongest_competitor_reason"):
            errors.append(f"{qid}:COMPETITOR_REASON_MISSING")
        if not q.get("most_important_unverified_atom"):
            errors.append(f"{qid}:UNVERIFIED_ATOM_MISSING")

    top1_vector = "".join(q.get("top1", "") for q in questions)
    top2_vector = "".join(q.get("top2", "") for q in questions)
    if obj.get("top1_vector") != top1_vector:
        errors.append("TOP1_VECTOR_MISMATCH")
    if obj.get("top2_vector") != top2_vector:
        errors.append("TOP2_VECTOR_MISMATCH")

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "checks": [{"rule": "RELATIVE_REPLAY_BODY", "status": "PASS" if not errors else "FAIL"}],
    }


def freeze_relative_replay(obj_path: str | Path, frozen_root: str | Path) -> dict[str, Any]:
    obj = read_json(obj_path)
    validation = validate_relative_replay(obj)
    if validation["status"] != "PASS":
        raise FortuneError(
            "relative replay validation failed: " + ";".join(validation["errors"]),
            status="RELATIVE_REPLAY_VALIDATION_FAIL",
        )
    run_id = slug(obj["run_id"])
    target_dir = Path(frozen_root) / run_id
    if target_dir.exists():
        raise FortuneError("relative replay run id already exists", status="RUN_ID_ALREADY_EXISTS")
    target_dir.mkdir(parents=True)
    frozen_path = target_dir / "relative-prediction-replay.json"
    frozen = dict(obj)
    frozen["relative_replay_validation"] = validation
    atomic_write_json(frozen_path, frozen)
    frozen_path.chmod(0o444)
    receipt = {
        "schema": "RELATIVE-PREDICTION-FREEZE-RECEIPT-V1",
        "run_id": run_id,
        "case_id": obj["case_id"],
        "relative_prediction_path": str(frozen_path),
        "relative_prediction_sha256": sha256_file(frozen_path),
        "validation": validation,
        "freeze_status": "RELATIVE_REPLAY_FROZEN",
        "formal_prediction_frozen": False,
        "s03_formal_fusion_performed": False,
        "answer_access_performed": False,
        "frozen_at": utc_now(),
        "immutable": True,
        "non_overwrite": True,
    }
    receipt_path = target_dir / "freeze-receipt.json"
    atomic_write_json(receipt_path, receipt)
    receipt_path.chmod(0o444)
    return receipt
