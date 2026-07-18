from __future__ import annotations

from pathlib import Path
from typing import Any

from .scoring import validate_freeze_receipt
from .util import FortuneError, atomic_write_json, read_json, sha256_file, slug, utc_now


def create_dev_group(group_id: str, case_ids: list[str], binding: dict[str, Any], root: str | Path,
                     expected_size: int = 5) -> dict[str, Any]:
    if len(case_ids) != expected_size or len(set(case_ids)) != expected_size:
        raise FortuneError(f"DEV group requires {expected_size} unique cases", status="DEV_GROUP_SIZE_INVALID")
    group_root = Path(root) / slug(group_id)
    if group_root.exists():
        raise FortuneError("group already exists", status="IMMUTABLE_OBJECT_EXISTS")
    result = {
        "schema": "DEV-GROUP-V1",
        "group_id": group_id,
        "revision": 1,
        "case_ids": case_ids,
        "frozen_binding": binding,
        "baseline_freezes": {},
        "reveal_authorized": False,
        "patch_round": 0,
        "same_defect_retries": {},
        "round_net_improvements": [],
        "round_records": [],
        "learning_policy": {
            "model": "ABSORB_DECOMPOSE_FILL_RESHAPE_APPLY_GENERATE",
            "mastery_target": 0.80,
            "arbitrary_round_limit": None,
            "answer_visible_diagnosis_allowed_after_freeze": True,
            "answer_visible_prediction_allowed": False,
            "case_specific_direction_rules_allowed": False,
            "base_knowledge_candidate_allowed": "MULTI_SOURCE_MULTI_UNIT_REVIEW_ONLY",
        },
        "status": "BASELINE_PENDING",
        "created_at": utc_now(),
    }
    target = group_root / "revisions" / "0001.json"
    atomic_write_json(target, result)
    target.chmod(0o444)
    atomic_write_json(group_root / "HEAD.json", {"revision": 1, "path": str(target)}, overwrite=True)
    return result


def _head(group_root: Path) -> tuple[dict[str, Any], Path]:
    pointer = read_json(group_root / "HEAD.json")
    path = Path(pointer["path"])
    if not path.is_absolute():
        candidate = path
        if not candidate.is_file():
            candidate = group_root / "revisions" / path.name
        path = candidate
    return read_json(path), path


def _append(group_root: Path, group: dict[str, Any]) -> dict[str, Any]:
    revision = group["revision"] + 1
    group["revision"] = revision
    group["updated_at"] = utc_now()
    target = group_root / "revisions" / f"{revision:04d}.json"
    atomic_write_json(target, group)
    target.chmod(0o444)
    atomic_write_json(group_root / "HEAD.json", {"revision": revision, "path": str(target)}, overwrite=True)
    return group


def register_baseline_freeze(group_root: str | Path, freeze_receipt_path: str | Path) -> dict[str, Any]:
    root = Path(group_root)
    group, _ = _head(root)

    validation = validate_freeze_receipt(freeze_receipt_path)
    receipt = read_json(freeze_receipt_path)
    run = read_json(validation["prediction_path"])
    case_id = run.get("case_id")
    if not case_id:
        raise FortuneError("frozen prediction case_id missing", status="CASE_ID_MISSING")
    if receipt.get("case_id") not in {None, case_id}:
        raise FortuneError("freeze receipt case_id mismatch", status="CASE_ID_MISMATCH")
    if case_id not in group["case_ids"]:
        raise FortuneError("case not in group", status="CASE_NOT_IN_GROUP")
    if case_id in group["baseline_freezes"]:
        raise FortuneError("case baseline already registered", status="BASELINE_ALREADY_REGISTERED")
    if run.get("binding") != group["frozen_binding"]:
        raise FortuneError("group binding mismatch", status="DEV_GROUP_VERSION_MISMATCH")

    group["baseline_freezes"][case_id] = {
        "run_id": validation["run_id"],
        "receipt_path": str(freeze_receipt_path),
        "receipt_sha256": validation["freeze_receipt_sha256"],
        "prediction_path": validation["prediction_path"],
        "prediction_sha256": validation["prediction_sha256"],
        "contract_path": validation["contract_path"],
        "contract_sha256": validation["contract_sha256"],
        "validation_status": validation["status"],
    }
    if set(group["baseline_freezes"]) == set(group["case_ids"]):
        group["status"] = "BASELINE_GROUP_FROZEN"
    return _append(root, group)


def authorize_group_reveal(group_root: str | Path) -> dict[str, Any]:
    root = Path(group_root)
    group, _ = _head(root)
    if set(group["baseline_freezes"]) != set(group["case_ids"]):
        raise FortuneError("all group baselines must freeze before reveal", status="GROUP_REVEAL_BEFORE_ALL_BASELINES_BLOCKED")

    replay_receipts: dict[str, dict[str, Any]] = {}
    for case_id, registered in group["baseline_freezes"].items():
        if sha256_file(registered["receipt_path"]) != registered["receipt_sha256"]:
            raise FortuneError(f"freeze receipt changed: {case_id}", status="FROZEN_PREDICTION_HASH_MISMATCH")
        validation = validate_freeze_receipt(registered["receipt_path"], registered["run_id"])
        if validation["freeze_receipt_sha256"] != registered["receipt_sha256"]:
            raise FortuneError(f"freeze validation receipt mismatch: {case_id}", status="FROZEN_PREDICTION_HASH_MISMATCH")
        if validation["prediction_sha256"] != registered["prediction_sha256"]:
            raise FortuneError(f"frozen prediction changed: {case_id}", status="FROZEN_PREDICTION_HASH_MISMATCH")
        if validation["contract_sha256"] != registered["contract_sha256"]:
            raise FortuneError(f"frozen contract changed: {case_id}", status="FROZEN_CONTRACT_HASH_MISMATCH")
        replay_receipts[case_id] = validation

    group["reveal_authorized"] = True
    group["status"] = "GROUP_REVEAL_AUTHORIZED"
    group["reveal_authorization_validation"] = {
        case_id: {
            "run_id": validation["run_id"],
            "freeze_receipt_sha256": validation["freeze_receipt_sha256"],
            "prediction_sha256": validation["prediction_sha256"],
            "contract_sha256": validation["contract_sha256"],
            "status": validation["status"],
        }
        for case_id, validation in replay_receipts.items()
    }
    return _append(root, group)


def validate_group_reveal_authorization(group_root: str | Path, expected_case_id: str,
                                        expected_run_id: str) -> dict[str, Any]:
    root = Path(group_root)
    group, head_path = _head(root)
    if group.get("schema") != "DEV-GROUP-V1":
        raise FortuneError("group schema invalid", status="GROUP_REVEAL_NOT_AUTHORIZED")
    if group.get("status") != "GROUP_REVEAL_AUTHORIZED" or group.get("reveal_authorized") is not True:
        raise FortuneError("group reveal is not authorized", status="GROUP_REVEAL_NOT_AUTHORIZED")
    if set(group.get("baseline_freezes", {})) != set(group.get("case_ids", [])):
        raise FortuneError("group baselines incomplete", status="GROUP_REVEAL_BEFORE_ALL_BASELINES_BLOCKED")
    registered = group["baseline_freezes"].get(expected_case_id)
    if not isinstance(registered, dict):
        raise FortuneError("case is not registered in authorized group", status="CASE_NOT_IN_GROUP")
    if registered.get("run_id") != slug(expected_run_id):
        raise FortuneError("group RUN_ID mismatch", status="FREEZE_RUN_ID_MISMATCH")

    validation = validate_freeze_receipt(registered["receipt_path"], expected_run_id)
    if validation["freeze_receipt_sha256"] != registered.get("receipt_sha256"):
        raise FortuneError("registered freeze receipt changed", status="FROZEN_PREDICTION_HASH_MISMATCH")
    if validation["prediction_sha256"] != registered.get("prediction_sha256"):
        raise FortuneError("registered prediction changed", status="FROZEN_PREDICTION_HASH_MISMATCH")
    if validation["contract_sha256"] != registered.get("contract_sha256"):
        raise FortuneError("registered contract changed", status="FROZEN_CONTRACT_HASH_MISMATCH")

    run = read_json(validation["prediction_path"])
    if run.get("case_id") != expected_case_id:
        raise FortuneError("frozen prediction case mismatch", status="CASE_ID_MISMATCH")
    if run.get("binding") != group.get("frozen_binding"):
        raise FortuneError("group binding mismatch", status="DEV_GROUP_VERSION_MISMATCH")

    return {
        "schema": "GROUP-REVEAL-AUTHORIZATION-VALIDATION-V1",
        "group_id": group["group_id"],
        "case_id": expected_case_id,
        "run_id": validation["run_id"],
        "group_revision": group["revision"],
        "group_head_path": str(head_path),
        "group_head_sha256": sha256_file(head_path),
        "freeze_receipt_sha256": validation["freeze_receipt_sha256"],
        "prediction_sha256": validation["prediction_sha256"],
        "contract_sha256": validation["contract_sha256"],
        "status": "PASS",
    }


def record_patch_round(group_root: str | Path, net_improvement: int, regression_damage: int,
                       defect_id: str, case_specific_only: bool = False, base_change_required: bool = False) -> dict[str, Any]:
    """Record one learning round without imposing an arbitrary maximum retry count.

    A revealed training set may be studied repeatedly. HOLD is reserved for contamination
    or an invalid case-specific direction rule. Lack of improvement routes the next round
    back to decomposition/reshaping; it does not terminate learning.
    """
    root = Path(group_root)
    group, _ = _head(root)
    group["patch_round"] += 1
    group["round_net_improvements"].append(net_improvement)
    group["same_defect_retries"][defect_id] = group["same_defect_retries"].get(defect_id, 0) + 1

    round_record = {
        "round": group["patch_round"],
        "defect_id": defect_id,
        "net_improvement": net_improvement,
        "regression_damage": regression_damage,
        "case_specific_only": case_specific_only,
        "base_change_required": base_change_required,
        "recorded_at": utc_now(),
    }
    group.setdefault("round_records", []).append(round_record)

    hold_reasons: list[str] = []
    if case_specific_only:
        hold_reasons.append("CASE_SPECIFIC_DIRECTION_RULE_OR_CONTAMINATION")

    if hold_reasons:
        group["status"] = "GROUP_HOLD"
        next_phase = None
    elif base_change_required:
        group["status"] = "KNOWLEDGE_REVIEW_REQUIRED"
        next_phase = "FILL"
    elif regression_damage > 0:
        group["status"] = "REGRESSION_REPAIR_REQUIRED"
        next_phase = "RESHAPE"
    elif len(group["round_net_improvements"]) >= 2 and group["round_net_improvements"][-2:] == [0, 0]:
        group["status"] = "METHOD_RETHINK_REQUIRED"
        next_phase = "DECOMPOSE"
    else:
        group["status"] = "RETESTING"
        next_phase = "APPLY"

    group["hold_reasons"] = hold_reasons
    group["next_learning_phase"] = next_phase
    group["training_continues"] = not bool(hold_reasons)
    group["generalization_status"] = "NOT_PROVEN_UNTIL_UNSEEN_BLIND_TEST"
    return _append(root, group)
