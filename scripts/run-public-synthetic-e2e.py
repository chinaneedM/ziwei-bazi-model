#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

from fortune_v1.end_to_end import (
    freeze_group_predictions,
    release_group_postblind,
    reveal_and_start_training,
    validate_staged_clean_start,
)
from fortune_v1.public_answer_vault import decrypt_answer_envelope, encrypt_answer_vector
from fortune_v1.training_finalize import finalize_group_training
from fortune_v1.util import atomic_write_json, canonical_bytes, read_json, sha256_bytes, sha256_file, utc_now


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def with_object_hash(value: dict[str, Any]) -> dict[str, Any]:
    result = dict(value)
    result.pop("object_hash", None)
    result["object_hash"] = sha256_bytes(canonical_bytes(result))
    return result


def build_preblind_fixture(root: Path, group_run_id: str, case_id: str) -> tuple[Path, Path]:
    run_root = root / "data" / "group-clean-starts" / group_run_id
    run_id = f"{group_run_id}-{case_id}"

    preblind_input = run_root / "preblind-inputs" / f"{case_id}.json"
    write_json(preblind_input, {
        "schema": "PREBLIND-CASE-INPUT-V1",
        "case_id": case_id,
        "answer_data_available": False,
        "option_visibility": "WITHHELD",
        "question_stems": [{"question_id": "Q1", "stem": "synthetic public E2E question"}],
    })

    skeleton = run_root / "preblind-skeletons" / f"{case_id}.json"
    write_json(skeleton, {
        "schema": "PREBLIND-PREDICTION-SKELETON-V1",
        "case_id": case_id,
        "run_id": run_id,
        "answer_data_available": False,
        "option_visibility": "WITHHELD",
        "questions": [{"question_id": "Q1"}],
    })

    options = run_root / "withheld-options" / f"{case_id}.json"
    write_json(options, {
        "schema": "POSTBLIND-OPTION-PAYLOAD-V1",
        "case_id": case_id,
        "run_id": run_id,
        "questions": [{
            "question_id": "Q1",
            "options": [
                {"option_id": "A", "text": "synthetic option a"},
                {"option_id": "B", "text": "synthetic option b"},
            ],
        }],
    })

    postblind_template = run_root / "withheld-postblind-templates" / f"{case_id}.json"
    write_json(postblind_template, {})
    postblind_source = run_root / "runtime-packets" / case_id / "withheld-postblind-source-packet.json"
    write_json(postblind_source, {})

    stage_plan = run_root / "runtime-packets" / case_id / "stage-access-plan.json"
    write_json(stage_plan, {
        "schema": "FORTUNE-STAGED-ACCESS-PLAN-V1",
        "status": "READY_FOR_PREBLIND_MODELING",
        "case_id": case_id,
        "run_id": run_id,
        "group_run_id": group_run_id,
        "preblind_allowed_paths": [str(preblind_input), str(skeleton)],
        "postblind_withheld_paths": [str(options), str(postblind_template), str(postblind_source)],
    })

    clean_start = run_root / "clean-start.json"
    write_json(clean_start, {
        "schema": "GROUP-CLEAN-START-V1",
        "status": "READY_FOR_PREBLIND_MODELING",
        "group_id": f"GROUP-{group_run_id}",
        "group_run_id": group_run_id,
        "answer_data_available": False,
        "cases": [{
            "case_id": case_id,
            "case_run_id": run_id,
            "preblind_input_path": str(preblind_input),
            "preblind_input_sha256": sha256_file(preblind_input),
            "preblind_skeleton_path": str(skeleton),
            "preblind_skeleton_sha256": sha256_file(skeleton),
        }],
        "retrieval_policy": {"staged_access": {
            "current_stage": "PREBLIND",
            "withheld_paths_not_disclosed_to_prediction_context": True,
            "release_requires": "MACHINE_VALID_DUAL_TRACK_PREBLIND_SEALS_FOR_ALL_QUESTIONS",
        }},
    })

    seals = run_root / "preblind-seals" / f"{case_id}.json"
    write_json(seals, {
        "schema": "PREBLIND-SEAL-BUNDLE-V1",
        "status": "PASS",
        "case_id": case_id,
        "run_id": run_id,
        "group_run_id": group_run_id,
        "option_access_before_all_seals": False,
        "questions": [{
            "question_id": "Q1",
            "sealed_before_option_access": True,
            "ziwei": {"status": "PASS", "model_hash": "1" * 64, "seal_hash": "3" * 64},
            "bazi": {"status": "PASS", "model_hash": "2" * 64, "seal_hash": "4" * 64},
        }],
    })

    release_request = root / "runtime" / "preblind-seal-requests" / f"{group_run_id}.json"
    write_json(release_request, {
        "schema": "GROUP-POSTBLIND-RELEASE-REQUEST-V1",
        "status": "REQUESTED",
        "group_run_id": group_run_id,
        "clean_start_path": str(clean_start),
        "output_root": str(run_root),
        "case_seal_bundles": [{
            "case_id": case_id,
            "seal_bundle_path": str(seals),
            "stage_plan_path": str(stage_plan),
        }],
    })
    return run_root, release_request


def write_prediction_bundle(path: Path, group_run_id: str, case_id: str) -> None:
    write_json(path, {
        "schema": "POSTBLIND-PREDICTION-BUNDLE-V1",
        "status": "READY_FOR_FREEZE",
        "case_id": case_id,
        "run_id": f"{group_run_id}-{case_id}",
        "group_run_id": group_run_id,
        "answer_visible_during_prediction": False,
        "prediction_input_answer_free": True,
        "questions": [{
            "question_id": "Q1",
            "top1": "A",
            "top2": "B",
            "confidence": "MEDIUM",
            "blind_core": "synthetic answer-free blind core",
            "source_provenance_status": "PASS",
            "pairwise_replay_status": "PASS",
            "coverage_plan_status": "PASS",
            "ziwei_track": {"status": "PASS"},
            "bazi_track": {"status": "PASS"},
            "fusion_status": "S03_PERFORMED",
            "evidence_usage_ledger": [{"packet_item_id": "SP-SYNTHETIC-PUBLIC-E2E"}],
            "pairwise_rows": [{
                "left": "A",
                "right": "B",
                "direction": "LEFT_AHEAD",
                "decisive_rule": "DISTINCTIVE_ATOM_DIRECT_SUPPORT",
                "reason": "synthetic deterministic comparison",
                "left_vector": {},
                "right_vector": {},
            }],
            "strongest_competitor": {"relative_first": "A", "relative_second": "B"},
            "formal_exact_assertion": None,
        }],
    })


def execute(request_path: Path, repository_root: Path, code_commit: str) -> dict[str, Any]:
    request = read_json(request_path)
    require(request.get("schema") == "PUBLIC-SYNTHETIC-E2E-REQUEST-V1", "request schema invalid")
    require(request.get("status") == "REQUESTED", "request status invalid")
    request_id = str(request.get("request_id") or "")
    group_run_id = str(request.get("group_run_id") or "")
    case_id = str(request.get("case_id") or "")
    require(bool(request_id and group_run_id and case_id), "request identity missing")

    receipt_path = repository_root / "reports" / "open-source-migration" / "public-synthetic-e2e" / f"{request_id}.json"
    envelope_path = repository_root / "public-answer-vault" / "encrypted" / f"{group_run_id}.json.fernet"
    require(not receipt_path.exists(), f"immutable receipt already exists: {receipt_path}")
    require(not envelope_path.exists(), f"immutable envelope already exists: {envelope_path}")

    key = os.environ.get("FORTUNE_PUBLIC_ANSWER_KEY", "")
    require(bool(key), "configured public answer key missing")

    temp_parent = Path("/tmp")
    temp_path: Path | None = None
    evidence: dict[str, Any] = {}
    with tempfile.TemporaryDirectory(prefix="fortune-public-synthetic-e2e-", dir=temp_parent) as temp_name:
        temp_path = Path(temp_name)
        run_root, release_request = build_preblind_fixture(temp_path, group_run_id, case_id)
        clean_start = run_root / "clean-start.json"
        clean_validation = validate_staged_clean_start(clean_start)
        require(clean_validation.get("status") == "PASS", "clean-start validation failed")

        release = release_group_postblind(release_request)
        require(release.get("status") == "POSTBLIND_OPTION_CHALLENGE_RELEASED", "postblind release failed")

        prediction = run_root / "postblind-predictions" / f"{case_id}.json"
        write_prediction_bundle(prediction, group_run_id, case_id)
        freeze_request = temp_path / "runtime" / "group-freeze-requests" / f"{group_run_id}.json"
        write_json(freeze_request, {
            "schema": "GROUP-PREDICTION-FREEZE-REQUEST-V1",
            "status": "REQUESTED",
            "group_run_id": group_run_id,
            "group_postblind_access_path": release["output_path"],
            "output_root": str(run_root),
            "case_prediction_bundles": [{
                "case_id": case_id,
                "prediction_bundle_path": str(prediction),
            }],
        })
        freeze = freeze_group_predictions(freeze_request)
        require(freeze.get("status") == "GROUP_PREDICTION_FREEZE_PASS", "group freeze failed")
        require(freeze.get("all_predictions_frozen_before_reveal") is True, "freeze order failed")

        answer_created_after_group_freeze = True
        secure_local = temp_path / "secure-local"
        plaintext_answer = secure_local / f"{group_run_id}.json"
        write_json(plaintext_answer, {
            "schema": "GROUP-ANSWER-VECTOR-V1",
            "status": "REVEALED_FOR_TRAINING_AFTER_FREEZE",
            "group_run_id": group_run_id,
            "raw_answer_string": "A",
            "delimiter": ",",
            "unicode_codepoints": [65],
            "character_offsets": [{"index": 0, "character": "A", "codepoint": 65}],
            "rows": [{"case_id": case_id, "question_id": "Q1", "answer_option_id": "A"}],
        })

        envelope = encrypt_answer_vector(plaintext_answer, envelope_path, key)
        require(envelope.get("status") == "ENCRYPTED_PUBLIC_STORAGE_READY", "encryption failed")
        require(envelope.get("plaintext_not_stored_in_repository") is True, "envelope plaintext policy failed")

        transient_root = temp_path / "transient-answers"
        transient_answer = transient_root / f"{group_run_id}.json"
        decryption = decrypt_answer_envelope(
            envelope_path,
            transient_answer,
            key,
            repository_root=repository_root,
        )
        require(decryption.get("status") == "PASS", "decryption failed")
        require(decryption.get("plaintext_committed_to_repository") is False, "decryption location failed")

        reveal_request = temp_path / "runtime" / "group-reveal-requests" / f"{group_run_id}.json"
        write_json(reveal_request, {
            "schema": "GROUP-REVEAL-TRAINING-REQUEST-V1",
            "status": "REQUESTED",
            "group_run_id": group_run_id,
            "group_prediction_freeze_path": freeze["output_path"],
            "answer_vector_path": f"{group_run_id}.json",
            "answer_vector_transport": "TRANSIENT_DECRYPTED_FROM_PUBLIC_ENVELOPE_AFTER_GROUP_FREEZE",
            "output_root": str(run_root / "training"),
            "cycle_id": f"CYCLE-{group_run_id}",
            "main_prompt_runtime_id": "MP-PROFESSIONAL-REASONING-20260718-R17",
            "knowledge_release_id": "SYNTHETIC-NO-KNOWLEDGE-PROMOTION",
            "method_release_id": "METHOD-R17",
            "model_release_id": "SYNTHETIC-E2E-NONSCORING",
        })
        intake = reveal_and_start_training(reveal_request, answer_root=transient_root)
        require(intake.get("status") == "LEARNING_ACTIVE", "learning intake did not activate")
        require(intake.get("training_unit_count") == 1, "training unit count invalid")
        replay_path = Path(intake["literal_replay_path"])
        replay = read_json(replay_path)
        require(replay.get("status") == "PASS", "literal replay failed")
        require(replay.get("top1_hits") == 1, "synthetic top1 replay mismatch")

        unit_id = intake["first_active_unit"]
        seed = read_json(Path(intake["training_evidence_seeds"][0]["path"]))
        reasoning = with_object_hash({
            "schema": "REASONING-CORRECTION-OBJECT-V2.1",
            "unit_id": unit_id,
            "error_mechanisms": [{"id": "E1", "mechanism": "synthetic scope calibration"}],
            "source_parent_chains": [{
                "library_id": "S02",
                "active_file_sha256": "a" * 64,
                "excerpt_sha256": "b" * 64,
                "line_ranges": ["1-2"],
                "knowledge_point": "synthetic relative scope",
                "applicability_conditions": ["public synthetic fixture only"],
                "capability_ceiling": "RELATIVE_DIRECTION_ONLY",
                "downstream_effect": "closes the synthetic competitor",
            }],
            "corrected_reasoning_order": ["scope", "evidence", "endpoint", "pairwise"],
            "capability_ceiling_and_no_overreach": ["no formal exact assertion"],
            "applicability_conditions": ["public synthetic fixture only"],
            "counterexamples_and_failure_boundaries": ["not a real-case rule"],
            "option_semantics": [
                {"option_id": "A", "concept": "synthetic A"},
                {"option_id": "B", "concept": "synthetic B"},
            ],
            "pairwise_rows": [{
                "row_id": "AB",
                "left": "A",
                "right": "B",
                "direction": "LEFT_AHEAD",
                "decisive_rule": "DISTINCTIVE_ATOM_DIRECT_SUPPORT",
                "reason": "synthetic deterministic comparison",
                "left_vector": {},
                "right_vector": {},
            }],
            "strongest_competitor": {"relative_first": "A", "relative_second": "B", "pairwise_row_id": "AB"},
            "contamination_and_answer_memory_audit": {
                "original_first_blind_preserved": True,
                "post_reveal_replays_excluded_from_accuracy": True,
                "generic_rule_has_no_case_or_option_fixed_selection": True,
                "bazi_variant_not_selected_by_revealed_result": True,
                "base_knowledge_not_promoted_from_single_unit": True,
                "case_specific_rule_detected": False,
                "answer_memorization_rule_detected": False,
                "status": "PASS",
            },
            "training_unit_conclusion": {"status": "TRAINING_UNIT_COMPLETE_CANDIDATE"},
        })
        evidence_path = run_root / "training" / "evidence" / f"001-{unit_id}.json"
        training_evidence = with_object_hash({
            "schema": "QUESTION-TRAINING-EVIDENCE-V2.1",
            "cycle_id": read_json(Path(intake["cycle_path"]))["cycle_id"],
            "unit_id": unit_id,
            "evidence_id": "SYNTHETIC-EVIDENCE-001",
            "first_blind_prediction": seed["first_blind_prediction"],
            "first_blind_observation_hash": seed["first_blind_observation_hash"],
            "correction": {
                "error_diagnosis_complete": True,
                "reasoning_update_complete": True,
                "generic_method_candidate_recorded": True,
                "counterexample_tests_complete": True,
                "patch_validation_status": "PASS",
                "case_specific_rule_detected": False,
                "answer_memorization_rule_detected": False,
                "reasoning_correction_object": reasoning,
            },
            "post_reveal_training_replays": [
                {
                    "evaluation_role": "POST_REVEAL_TRAINING_REPLAY",
                    "attempt_id": f"SYNTHETIC-R{attempt}",
                    "answer_visible_during_prediction": False,
                    "prediction_input_answer_free": True,
                    "case_specific_rule_detected": False,
                    "source_provenance_status": "PASS",
                    "pairwise_replay_status": "PASS",
                    "matches_revealed_result": True,
                }
                for attempt in range(1, 6)
            ],
            "prior_method_retention": {"prior_completed_unit_count": 0, "retention_rate": None},
        })
        write_json(evidence_path, training_evidence)
        evidence_manifest_path = run_root / "training" / "evidence-manifest.json"
        write_json(evidence_manifest_path, with_object_hash({
            "schema": "GROUP-TRAINING-EVIDENCE-MANIFEST-V1",
            "status": "READY_FOR_SERIAL_EVALUATION",
            "group_id": intake["group_id"],
            "group_run_id": group_run_id,
            "training_unit_count": 1,
            "units": [{
                "unit_id": unit_id,
                "evidence_path": str(evidence_path),
                "evidence_sha256": sha256_file(evidence_path),
                "evidence_object_hash": training_evidence["object_hash"],
            }],
        }))
        finalize_request = temp_path / "runtime" / "training-finalize-requests" / f"{group_run_id}.json"
        write_json(finalize_request, with_object_hash({
            "schema": "GROUP-TRAINING-FINALIZE-REQUEST-V1",
            "status": "REQUESTED",
            "group_id": intake["group_id"],
            "group_run_id": group_run_id,
            "run_root": str(run_root),
            "training_intake_path": intake["output_path"],
            "evidence_manifest_path": str(evidence_manifest_path),
            "output_root": str(run_root / "training"),
        }))
        finalization = finalize_group_training(finalize_request)
        require(finalization.get("status") == "TRAINING_FINALIZE_PASS", "synthetic training did not finalize")
        require(finalization.get("training_unit_count") == finalization.get("completed_training_unit_count") == 1, "synthetic training closure count mismatch")

        evidence = {
            "clean_start_validation_status": clean_validation["status"],
            "clean_start_validation_object_hash": clean_validation["object_hash"],
            "postblind_release_status": release["status"],
            "postblind_release_object_hash": release["object_hash"],
            "group_freeze_status": freeze["status"],
            "group_freeze_sha256": sha256_file(freeze["output_path"]),
            "group_freeze_object_hash": freeze["object_hash"],
            "all_predictions_frozen_before_reveal": freeze["all_predictions_frozen_before_reveal"],
            "answer_created_after_group_freeze": answer_created_after_group_freeze,
            "encrypted_envelope_sha256": sha256_file(envelope_path),
            "encrypted_envelope_object_hash": envelope["object_hash"],
            "decryption_status": decryption["status"],
            "decrypted_output_location": decryption["decrypted_output_location"],
            "plaintext_committed_to_repository": decryption["plaintext_committed_to_repository"],
            "literal_replay_status": replay["status"],
            "literal_replay_object_hash": replay["object_hash"],
            "literal_replay_top1_hits": replay["top1_hits"],
            "learning_status": intake["status"],
            "learning_intake_object_hash": intake["object_hash"],
            "training_unit_count": intake["training_unit_count"],
            "training_finalize_status": finalization["status"],
            "training_finalize_object_hash": finalization["object_hash"],
            "completed_training_unit_count": finalization["completed_training_unit_count"],
            "training_set_status": finalization["training_set_status"],
        }

        shutil.rmtree(secure_local)
        shutil.rmtree(transient_root)
        require(not plaintext_answer.exists() and not transient_answer.exists(), "transient plaintext cleanup failed")

    require(temp_path is not None and not temp_path.exists(), "transient workspace was not destroyed")
    receipt = with_object_hash({
        "schema": "PUBLIC-SYNTHETIC-E2E-RECEIPT-V1",
        "status": "PASS",
        "request_id": request_id,
        "request_path": request_path.as_posix(),
        "request_sha256": sha256_file(request_path),
        "repository": "chinaneedM/ziwei-bazi-model",
        "code_commit": code_commit,
        "group_run_id": group_run_id,
        "case_id": case_id,
        "synthetic_non_scoring": True,
        "answer_data_available_before_group_freeze": False,
        **evidence,
        "transient_plaintext_destroyed": True,
        "transient_workspace_destroyed": True,
        "secret_present": True,
        "secret_value_recorded": False,
        "secret_fingerprint_recorded": False,
        "formal_training_permission": "BLOCKED_PENDING_KNOWLEDGE_RIGHTS_AND_RELEASE_ACTIVATION",
        "created_at": utc_now(),
    })
    atomic_write_json(receipt_path, receipt)
    return {**receipt, "receipt_path": receipt_path.as_posix(), "envelope_path": envelope_path.as_posix()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True)
    parser.add_argument("--repository-root", default=".")
    parser.add_argument("--code-commit", required=True)
    args = parser.parse_args()
    result = execute(
        Path(args.request),
        Path(args.repository_root).resolve(),
        args.code_commit,
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
