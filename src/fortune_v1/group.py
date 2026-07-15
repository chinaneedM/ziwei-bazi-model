from __future__ import annotations

from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, read_json, sha256_file, slug, utc_now


def create_dev_group(group_id: str, case_ids: list[str], binding: dict[str, Any], root: str | Path,
                     expected_size: int = 5) -> dict[str, Any]:
    if len(case_ids) != expected_size or len(set(case_ids)) != expected_size:
        raise FortuneError(f"DEV group requires {expected_size} unique cases", status="DEV_GROUP_SIZE_INVALID")
    group_root = Path(root) / slug(group_id)
    if group_root.exists(): raise FortuneError("group already exists", status="IMMUTABLE_OBJECT_EXISTS")
    result = {"schema": "DEV-GROUP-V1", "group_id": group_id, "revision": 1, "case_ids": case_ids,
              "frozen_binding": binding, "baseline_freezes": {}, "reveal_authorized": False,
              "patch_round": 0, "same_defect_retries": {}, "round_net_improvements": [], "status": "BASELINE_PENDING", "created_at": utc_now()}
    target = group_root / "revisions" / "0001.json"; atomic_write_json(target, result); target.chmod(0o444)
    atomic_write_json(group_root / "HEAD.json", {"revision": 1, "path": str(target)}, overwrite=True)
    return result


def _head(group_root: Path) -> tuple[dict[str, Any], Path]:
    pointer = read_json(group_root / "HEAD.json"); path = Path(pointer["path"])
    return read_json(path), path


def _append(group_root: Path, group: dict[str, Any]) -> dict[str, Any]:
    revision = group["revision"] + 1; group["revision"] = revision; group["updated_at"] = utc_now()
    target = group_root / "revisions" / f"{revision:04d}.json"; atomic_write_json(target, group); target.chmod(0o444)
    atomic_write_json(group_root / "HEAD.json", {"revision": revision, "path": str(target)}, overwrite=True)
    return group


def register_baseline_freeze(group_root: str | Path, freeze_receipt_path: str | Path) -> dict[str, Any]:
    root = Path(group_root); group, _ = _head(root); receipt = read_json(freeze_receipt_path)
    case_id = receipt["case_id"]
    if case_id not in group["case_ids"]: raise FortuneError("case not in group", status="CASE_NOT_IN_GROUP")
    if case_id in group["baseline_freezes"]: raise FortuneError("case baseline already registered", status="BASELINE_ALREADY_REGISTERED")
    run = read_json(receipt["prediction_path"])
    if run["binding"] != group["frozen_binding"]: raise FortuneError("group binding mismatch", status="DEV_GROUP_VERSION_MISMATCH")
    group["baseline_freezes"][case_id] = {"run_id": receipt["run_id"], "receipt_path": str(freeze_receipt_path), "receipt_sha256": sha256_file(freeze_receipt_path)}
    if set(group["baseline_freezes"]) == set(group["case_ids"]): group["status"] = "BASELINE_GROUP_FROZEN"
    return _append(root, group)


def authorize_group_reveal(group_root: str | Path) -> dict[str, Any]:
    root = Path(group_root); group, _ = _head(root)
    if set(group["baseline_freezes"]) != set(group["case_ids"]):
        raise FortuneError("all group baselines must freeze before reveal", status="GROUP_REVEAL_BEFORE_ALL_BASELINES_BLOCKED")
    for case_id, receipt in group["baseline_freezes"].items():
        if sha256_file(receipt["receipt_path"]) != receipt["receipt_sha256"]:
            raise FortuneError(f"freeze receipt changed: {case_id}", status="FROZEN_PREDICTION_HASH_MISMATCH")
    group["reveal_authorized"] = True; group["status"] = "GROUP_REVEAL_AUTHORIZED"
    return _append(root, group)


def record_patch_round(group_root: str | Path, net_improvement: int, regression_damage: int,
                       defect_id: str, case_specific_only: bool = False, base_change_required: bool = False) -> dict[str, Any]:
    root = Path(group_root); group, _ = _head(root)
    group["patch_round"] += 1
    group["round_net_improvements"].append(net_improvement)
    group["same_defect_retries"][defect_id] = group["same_defect_retries"].get(defect_id, 0) + 1
    hold_reasons = []
    if group["patch_round"] >= 5: hold_reasons.append("MAX_GROUP_PATCH_ROUNDS")
    if group["same_defect_retries"][defect_id] > 2: hold_reasons.append("MAX_SAME_DEFECT_RETRIES")
    if len(group["round_net_improvements"]) >= 2 and group["round_net_improvements"][-2:] == [0, 0]: hold_reasons.append("NO_IMPROVEMENT_LIMIT")
    if regression_damage > 0: hold_reasons.append("REGRESSION_DAMAGE")
    if case_specific_only: hold_reasons.append("CASE_SPECIFIC_ONLY")
    if base_change_required: hold_reasons.append("BASE_KNOWLEDGE_CHANGE_REQUIRED")
    group["status"] = "GROUP_HOLD" if hold_reasons else "RETESTING"
    group["hold_reasons"] = hold_reasons
    return _append(root, group)

