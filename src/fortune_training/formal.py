from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

from .chat_input import compose_chat_input, write_chat_input
from .learning import LEDGER_RELATIVE_PATH, load_learning_ledger
from .runtime import _fernet_from_key, _validate_answers
from .util import (
    TrainingError,
    atomic_write_json,
    canonical_bytes,
    exclusive_write_json,
    load_json,
    next_round_id,
    object_sha256,
    require_outside,
    sha256_file,
    utc_now,
)
from .verify import verify_repository


FORMAL_GROUP_ID = "FORMAL-DEVELOPMENT-001"
FORMAL_GROUP_PATH = Path("training/formal-development-group.json")
FORMAL_ANSWER_DIR = Path("answer-vault/formal")
FORMAL_ANSWER_MANIFEST = FORMAL_ANSWER_DIR / "manifest.json"
PRE_FORMAL_STATE_ARCHIVE = Path("training/history/PRE-FORMAL-STATE.json")
PRE_FORMAL_LEDGER_ARCHIVE = Path("training/history/PRE-FORMAL-LEARNING-LEDGER.json")


def _dataset_case_ids(root: Path) -> list[str]:
    manifest = load_json(root / "case-bank" / "manifest.json")
    partitions = manifest.get("partitions")
    if not isinstance(partitions, dict):
        raise TrainingError("case-bank manifest has no partition mapping")
    case_ids = [
        case_id
        for partition_id in ("DEVELOPMENT", "STAGE_VALIDATION", "FINAL_HOLDOUT")
        for case_id in partitions.get(partition_id, [])
    ]
    if len(case_ids) != len(set(case_ids)) or len(case_ids) != manifest.get("accepted_case_count"):
        raise TrainingError("case-bank partition ids do not cover the accepted corpus exactly once")
    return case_ids


def _load_answer_batch(root: Path, batch_path: Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    require_outside(root, batch_path, "plaintext answer batch")
    payload = load_json(batch_path)
    if not isinstance(payload, dict) or set(payload) != {"schema", "corpus_id", "cases"}:
        raise TrainingError("answer batch must contain exactly schema, corpus_id, and cases")
    manifest = load_json(root / "case-bank" / "manifest.json")
    if payload.get("schema") != "FORTUNE-ANSWER-BATCH-V1":
        raise TrainingError("wrong formal answer-batch schema")
    if payload.get("corpus_id") != manifest.get("corpus_id"):
        raise TrainingError("answer batch corpus_id does not match the case bank")
    rows = payload.get("cases")
    if not isinstance(rows, list):
        raise TrainingError("answer batch cases must be an array")
    by_id: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"case_id", "answers"}:
            raise TrainingError("every answer-batch case must be an object")
        case_id = row.get("case_id")
        if not isinstance(case_id, str) or case_id in by_id:
            raise TrainingError(f"invalid or duplicate answer-batch case: {case_id!r}")
        by_id[case_id] = row
    required = set(_dataset_case_ids(root))
    if set(by_id) != required:
        missing = sorted(required - set(by_id))
        unexpected = sorted(set(by_id) - required)
        raise TrainingError(
            "answer batch must cover all 107 cases exactly once "
            f"(missing={missing[:5]}, unexpected={unexpected[:5]})"
        )
    for case_id, row in by_id.items():
        case = load_json(root / "case-bank" / "cases" / f"{case_id}.json")
        _validate_answers(case, row)
    return manifest, by_id


def import_answer_batch(
    root: Path,
    batch_path: Path,
    key: str | bytes | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    state = load_json(root / "training" / "state.json")
    if state.get("status") != "DATASET_FROZEN_AWAITING_ANSWER_IMPORT":
        raise TrainingError("formal answers may only be imported while the dataset is frozen")
    destination = root / FORMAL_ANSWER_DIR
    if destination.exists():
        raise TrainingError("formal answer vault already exists; refusing a partial or replacement import")
    manifest, by_id = _load_answer_batch(root, batch_path)
    fernet = _fernet_from_key(key)
    vault_parent = destination.parent
    vault_parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".formal-answer-import-", dir=vault_parent))
    try:
        envelope_hashes: dict[str, str] = {}
        for case_id in _dataset_case_ids(root):
            token = fernet.encrypt(canonical_bytes(by_id[case_id]))
            envelope = staging / f"{case_id}.json.fernet"
            with envelope.open("xb") as handle:
                handle.write(token + b"\n")
                handle.flush()
                os.fsync(handle.fileno())
            envelope_hashes[case_id] = sha256_file(envelope)
        vault_manifest = {
            "schema": "FORMAL-ANSWER-VAULT-MANIFEST-V1",
            "corpus_id": manifest["corpus_id"],
            "case_count": len(envelope_hashes),
            "envelope_hashes": envelope_hashes,
            "plaintext_stored_in_repository": False,
            "answer_read_phase": "POST_FREEZE_ONLY",
            "created_at": utc_now(),
        }
        atomic_write_json(staging / "manifest.json", vault_manifest)
        os.replace(staging, destination)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise
    return {
        "status": "FORMAL_ANSWERS_ENCRYPTED",
        "corpus_id": manifest["corpus_id"],
        "answer_envelopes": len(by_id),
        "vault_manifest": FORMAL_ANSWER_MANIFEST.as_posix(),
        "plaintext_stored_in_repository": False,
    }


def verify_formal_answer_vault(
    root: Path,
    key: str | bytes | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    fernet = _fernet_from_key(key)
    case_ids = _dataset_case_ids(root)
    for case_id in case_ids:
        envelope = root / FORMAL_ANSWER_DIR / f"{case_id}.json.fernet"
        try:
            plaintext = fernet.decrypt(envelope.read_bytes().strip())
        except FileNotFoundError as exc:
            raise TrainingError(f"missing formal encrypted answer: {case_id}") from exc
        except Exception as exc:
            raise TrainingError(f"formal answer envelope failed decryption: {case_id}") from exc
        try:
            import json

            payload = json.loads(plaintext.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise TrainingError(f"formal answer envelope is invalid JSON: {case_id}") from exc
        case = load_json(root / "case-bank" / "cases" / f"{case_id}.json")
        _validate_answers(case, payload)
    return {
        "status": "FORMAL_ANSWER_VAULT_VERIFIED",
        "answer_envelopes": len(case_ids),
        "plaintext_disclosed": False,
    }


def _formal_group(root: Path) -> dict[str, Any]:
    partition = load_json(root / "case-bank" / "partitions" / "development.json")
    schedule = partition.get("first_blind_schedule")
    cases = partition.get("cases")
    if not isinstance(schedule, list) or not schedule:
        raise TrainingError("development partition has no first-blind schedule")
    if not isinstance(cases, dict) or not set(schedule).issubset(cases):
        raise TrainingError("development first-blind schedule has invalid case mapping")
    return {
        "schema": "TRAINING-GROUP-V1",
        "group_id": FORMAL_GROUP_ID,
        "partition_id": "DEVELOPMENT",
        "case_order": schedule,
        "cases": {case_id: cases[case_id] for case_id in schedule},
        "excluded_revealed_or_source_exposed_cases": sorted(set(partition["case_order"]) - set(schedule)),
    }


def activate_formal_controller(
    root: Path,
    key: str | bytes | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    verify_repository(root, require_answers=True)
    answer_check = verify_formal_answer_vault(root, key)
    old_state = load_json(root / "training" / "state.json")
    if old_state.get("status") != "DATASET_FROZEN_AWAITING_ANSWER_IMPORT":
        raise TrainingError("formal controller activation requires the frozen pre-activation state")
    if old_state.get("active_round_id") is not None:
        raise TrainingError("formal controller cannot activate while a round is active")
    group = _formal_group(root)
    group_path = root / FORMAL_GROUP_PATH
    if group_path.exists():
        raise TrainingError("formal group file already exists")
    old_chat_input = load_json(root / "chat-input" / "current.json")
    old_ledger = load_learning_ledger(root)
    state_archive = root / PRE_FORMAL_STATE_ARCHIVE
    ledger_archive = root / PRE_FORMAL_LEDGER_ARCHIVE
    if state_archive.exists() or ledger_archive.exists():
        raise TrainingError("pre-formal history archive already exists")
    new_state = {
        "schema": "GENERALIZATION-TRAINING-STATE-R2",
        "mode": "FORMAL_CASE_BANK",
        "formal_phase": "DEVELOPMENT",
        "group_id": FORMAL_GROUP_ID,
        "group_path": FORMAL_GROUP_PATH.as_posix(),
        "policy_path": old_state["policy_path"],
        "source_manifest_path": old_state["source_manifest_path"],
        "current_model_release": old_state["current_model_release"],
        "current_case_index": 0,
        "status": "READY_FOR_ROUND",
        "dataset_manifest_path": "case-bank/manifest.json",
        "dataset_runtime_status": "FORMAL_DEVELOPMENT_ACTIVE",
        "active_round_id": None,
        "round_count": 0,
        "round_id_prefix": "FORMAL-ROUND",
        "round_limit": None,
        "first_blind_cases_closed": 0,
        "independent_pass_streak": 0,
        "required_consecutive_independent_passes": 3,
        "active_replay_case_id": None,
        "spaced_replay_queue": [],
        "cases": {
            case_id: {
                "status": "ACTIVE" if index == 0 else "PENDING",
                "first_blind_passed": None,
                "remediation_status": "NOT_EVALUATED",
                "first_blind_round_id": None,
                "replay_round_ids": [],
                "round_ids": [],
            }
            for index, case_id in enumerate(group["case_order"])
        },
        "formal_activation": {
            "activated_at": utc_now(),
            "answer_vault_manifest": FORMAL_ANSWER_MANIFEST.as_posix(),
            "answer_vault_manifest_sha256": sha256_file(root / FORMAL_ANSWER_MANIFEST),
            "verified_answer_envelopes": answer_check["answer_envelopes"],
            "previous_state_archive": PRE_FORMAL_STATE_ARCHIVE.as_posix(),
            "previous_ledger_archive": PRE_FORMAL_LEDGER_ARCHIVE.as_posix(),
        },
    }
    try:
        exclusive_write_json(state_archive, old_state)
        exclusive_write_json(ledger_archive, old_ledger)
        exclusive_write_json(group_path, group)
        atomic_write_json(root / "training" / "state.json", new_state)
        write_chat_input(root)
        verification = verify_repository(root, require_answers=True)
    except Exception:
        atomic_write_json(root / "training" / "state.json", old_state)
        atomic_write_json(root / "chat-input" / "current.json", old_chat_input)
        group_path.unlink(missing_ok=True)
        state_archive.unlink(missing_ok=True)
        ledger_archive.unlink(missing_ok=True)
        raise
    return {
        "status": "FORMAL_CONTROLLER_ACTIVE",
        "group_id": FORMAL_GROUP_ID,
        "formal_phase": "DEVELOPMENT",
        "scheduled_first_blind_cases": len(group["case_order"]),
        "current_case_id": group["case_order"][0],
        "recommended_round_id": next_round_id(new_state),
        "answers_disclosed": False,
        "verification": verification["status"],
    }


def rehearse_formal_no_reveal(root: Path) -> dict[str, Any]:
    root = root.resolve()
    verification = verify_repository(root, require_answers=True)
    state = load_json(root / "training" / "state.json")
    if state.get("mode") != "FORMAL_CASE_BANK" or state.get("formal_phase") != "DEVELOPMENT":
        raise TrainingError("formal no-reveal rehearsal requires the active development controller")
    if state.get("status") != "READY_FOR_ROUND" or state.get("active_round_id") is not None:
        raise TrainingError("formal no-reveal rehearsal requires a clean ready-for-round state")
    bundle = compose_chat_input(root)
    summary = bundle["state_summary"]
    if (
        bundle.get("contains_answers") is not False
        or bundle.get("contains_old_predictions") is not False
        or bundle.get("contains_scores_or_reviews") is not False
        or summary.get("prediction_allowed") is not True
    ):
        raise TrainingError("formal Chat bundle failed the answer-isolation rehearsal")
    return {
        "status": "NO_REVEAL_REHEARSAL_PASS",
        "formal_phase": state["formal_phase"],
        "current_case_id": summary["current_case_id"],
        "recommended_round_id": summary["recommended_round_id"],
        "prediction_allowed": True,
        "answer_payload_read": False,
        "answers_disclosed": False,
        "current_case_sha256": bundle["component_hashes"]["current_case_sha256"],
        "chat_input_sha256": object_sha256(bundle),
        "verification": verification["status"],
    }
