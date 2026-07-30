from __future__ import annotations

import json
import base64
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from fortune_training.chat_input import (
    CHAT_RUNTIME_MODEL_RELATIVE_PATH,
    CHAT_INPUT_RELATIVE_PATH,
    GITHUB_ISSUE_BODY_MAX_CHARACTERS,
    HANDOFF_TARGET_MAX_CHARACTERS,
    write_chat_input,
)
from fortune_training.cli import build_parser
from fortune_training.canonical_runtime import (
    MAX_SEGMENT_BYTES,
    RUNTIME_MANIFEST_PATH,
    validate_canonical_runtime,
    write_canonical_runtime,
)
from fortune_training.formal import (
    FORMAL_ANSWER_DIR,
    FORMAL_GROUP_PATH,
    PRE_FORMAL_LEDGER_ARCHIVE,
    PRE_FORMAL_STATE_ARCHIVE,
    PREDICTION_CANONICAL_RUNTIME_READ_GATE_FAILURE,
    PRE_FREEZE_RUNTIME_GATE_FAILED_NOT_EXECUTED,
    import_answer_batch,
    invalidate_current_pre_freeze_round,
    quarantine_current_case,
)
from fortune_training.contamination_relay import validate_contamination_report
from fortune_training.issue_relay import PACKET_END, PACKET_START, extract_packet, process_packet
from fortune_training.handoff_probe import (
    process_handoff_probe,
    unseal_private_review,
    validate_handoff,
)
from fortune_training.handoff_preflight import normalize_handoff
from fortune_training.learning import (
    LEDGER_RELATIVE_PATH,
    empty_learning_ledger,
    load_learning_ledger,
    safe_active_rules,
    validate_learning_ledger,
    write_learning_ledger,
)
from fortune_training.maintenance import maintenance_due, run_maintenance
from fortune_training.policy import passed, required_correct
from fortune_training.prediction_access import (
    PREDICTION_ACCESS_CONTRACT_PATH,
    PostPredictionHandoffSession,
    PredictionAccessSession,
    assert_prediction_access,
    load_post_prediction_handoff_policy,
)
from fortune_training.reasoning import build_completeness_report, frozen_content_hash
from fortune_training.runtime import (
    _validate_answers,
    apply_learning,
    encrypt_answer,
    freeze_prediction,
    score_round,
    start_round,
    status,
)
from fortune_training.transport import (
    PUBLIC_KEY_PATH,
    SEALED_BATCH_PATH,
    bootstrap_answer_transport,
    finalize_answer_transport,
    seal_answer_batch,
)
from fortune_training.util import TrainingError, object_sha256
from fortune_training.verify import (
    _validate_model_runtime_policy,
    build_source_manifest,
    verify_repository,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TAXONOMY = json.loads((PROJECT_ROOT / "config" / "question-taxonomy.json").read_text())
POLICY = json.loads((PROJECT_ROOT / "config" / "training-policy.json").read_text())
PREDICTION_TOOL_POLICY = json.loads(
    (PROJECT_ROOT / "config" / "prediction-tool-policy.json").read_text()
)
POST_PREDICTION_HANDOFF_POLICY = json.loads(
    (
        PROJECT_ROOT
        / "config"
        / "post-prediction-handoff-policy.json"
    ).read_text()
)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def general_rule(rule_id: str) -> dict:
    return {
        "rule_id": rule_id,
        "topic_tags": ["OTHER"],
        "reasoning_skill_tags": ["EVIDENCE_WEIGHTING"],
        "source_routes": ["S03", "S17"],
        "statement": "Separate structural possibility from a proved event endpoint.",
        "applicability": "When several real-world outcomes share the same broad structure.",
        "limits": "A broad structure cannot prove an exact event by itself.",
        "counterexamples": "A complete actor, action, timing, and endpoint chain may justify precision.",
        "capability_ceiling": "Use as a candidate until independent timing and endpoint evidence agree.",
        "source_basis": "S03 conflict arbitration and S17 endpoint-chain principles.",
        "trigger_conditions": "Several options share the same non-specific symbolic background.",
        "decision_procedure": "Build a separate actor, mechanism, timing, and endpoint chain for each option.",
        "stop_conditions": "Stop at a broad possibility when an exclusive endpoint node is missing.",
    }


def learning_correction(
    *,
    remediation_type: str = "NEW_GENERAL_RULE",
    rules: list[dict] | None = None,
) -> dict:
    return {
        "schema": "MODEL-LEARNING-CORRECTION-V3",
        "learning_type": "REASONING_STRATEGY",
        "root_causes": ["EVIDENCE_WEIGHTING"],
        "remediation_type": remediation_type,
        "correction": {
            "statement": "Require a complete actor, mechanism, timing, and endpoint chain.",
            "applicability": "Use when broad structures support several competing outcomes.",
            "limitations": "The procedure cannot create missing chart facts.",
            "expected_effect": "Reduce unsupported endpoint selection.",
            "capability_ceiling": "Retain uncertainty when an endpoint remains unclosed.",
            "source_basis": "S03 conflict arbitration and S17 endpoint closure.",
            "reasoning": "The correction targets a general execution or weighting defect.",
        },
        "rules": rules or [],
        "rule_status_changes": [],
    }


class RuntimeFixture:
    def __init__(self, base: Path, first_question_count: int = 5, case_count: int = 5):
        self.base = base
        self.root = base / "repo"
        self.key = Fernet.generate_key()
        for index in range(20):
            source = self.root / "sources" / "canonical" / f"S{index:02d}_test.txt"
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text(f"general source {index}\n", encoding="utf-8")
        write_json(self.root / "config" / "training-policy.json", POLICY)
        write_json(
            self.root / "config" / "prediction-tool-policy.json",
            PREDICTION_TOOL_POLICY,
        )
        write_json(
            self.root / "config" / "post-prediction-handoff-policy.json",
            POST_PREDICTION_HANDOFF_POLICY,
        )
        write_json(self.root / "config" / "question-taxonomy.json", TAXONOMY)
        source_manifest = build_source_manifest(self.root)
        write_json(self.root / "sources" / "canonical-manifest.json", source_manifest)
        runtime_manifest = write_canonical_runtime(self.root)
        write_json(
            self.root / "config" / "source-policy.json",
            {
                "schema": "SOURCE-AUTHORITY-POLICY-V2",
                "external_project_sources_required": False,
                "project_file_library_sources_runtime_allowed": False,
                "runtime_canonical_authority": "GIT_MAIN_SOURCES_CANONICAL_ONLY",
                "runtime_source": "GIT_REPOSITORY_ONLY",
                "git_repository": "chinaneedM/ziwei-bazi-model",
                "git_ref": "main",
                "git_canonical_path": "sources/canonical",
                "git_canonical_mutable_during_training": False,
                "canonical_manifest_sha256": object_sha256(source_manifest),
                "canonical_runtime_manifest_path": RUNTIME_MANIFEST_PATH.as_posix(),
                "canonical_runtime_manifest_sha256": object_sha256(
                    runtime_manifest
                ),
                "canonical_runtime_derivation": (
                    "UTF8_LINE_PRESERVING_EXACT_CONCATENATION"
                ),
                "canonical_runtime_authority_role": (
                    "LOSSLESS_READ_VIEW_NOT_INDEPENDENT_AUTHORITY"
                ),
                "model_learning_path": "model-learning",
                "model_learning_mutable_during_training": True,
                "conflict_resolution": (
                    "REJECT_PROJECT_OR_FILE_LIBRARY_SOURCE_AND_USE_GIT_MAIN_CANONICAL"
                ),
            },
        )
        write_json(
            self.root / "config" / "answer-policy.json",
            {
                "schema": "PUBLIC-REPOSITORY-ANSWER-POLICY-V1",
                "repository_visibility": "PUBLIC",
                "private_answer_repository_required": False,
                "plaintext_answers_allowed": False,
                "encrypted_answer_envelopes_allowed": True,
                "decryption_keys_allowed": False,
                "answer_read_phase": "POST_FREEZE_ONLY",
            },
        )
        shutil.copy2(
            PROJECT_ROOT / "config" / "chat-runtime-performance.json",
            self.root / "config" / "chat-runtime-performance.json",
        )
        write_json(
            self.root / "model-learning" / "releases" / "MODEL-BASELINE-001.json",
            {
                "schema": "MODEL-RELEASE-V1",
                "release_id": "MODEL-BASELINE-001",
                "parent_release": None,
                "base_source_manifest": "sources/canonical-manifest.json",
                "patches": [],
                "training_process_authority": "config/training-policy.json",
                "canonical_sources_mutated": False,
            },
        )
        case_order = [f"DEV-EXAMPLE-{index:03d}" for index in range(1, case_count + 1)]
        case_paths = {
            case_id: f"examples/DEV-GROUP-002/cases/{case_id}.json" for case_id in case_order
        }
        for index, case_id in enumerate(case_order):
            count = first_question_count if index == 0 else 5
            questions = [
                {
                    "question_id": f"Q{question_index}",
                    "stem": f"question {question_index}",
                    "options": [
                        {"option_id": option, "text": option}
                        for option in ("A", "B", "C", "D")
                    ],
                }
                for question_index in range(1, count + 1)
            ]
            write_json(
                self.root / case_paths[case_id],
                {
                    "schema": "TRAINING-CASE-BUNDLE-V2",
                    "case_id": case_id,
                    "group_id": "DEV-GROUP-002",
                    "answer_isolation": {"answer_payload_present": False},
                    "binding": {
                        "source_manifest": "sources/canonical-manifest.json",
                        "training_policy": "config/training-policy.json",
                    },
                    "questions": {"question_count": count, "parsed": questions},
                },
            )
        write_json(
            self.root / "examples" / "DEV-GROUP-002" / "group.json",
            {
                "schema": "TRAINING-GROUP-V1",
                "group_id": "DEV-GROUP-002",
                "case_order": case_order,
                "cases": case_paths,
            },
        )
        write_json(
            self.root / "training" / "state.json",
            {
                "schema": "GENERALIZATION-TRAINING-STATE-R2",
                "group_id": "DEV-GROUP-002",
                "group_path": "examples/DEV-GROUP-002/group.json",
                "policy_path": "config/training-policy.json",
                "source_manifest_path": "sources/canonical-manifest.json",
                "current_model_release": "MODEL-BASELINE-001",
                "current_case_index": 0,
                "status": "READY_FOR_ROUND",
                "active_round_id": None,
                "round_count": 0,
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
                    for index, case_id in enumerate(case_order)
                },
            },
        )
        write_learning_ledger(self.root, empty_learning_ledger(self.root))
        (self.root / "answer-vault" / "encrypted").mkdir(parents=True, exist_ok=True)
        (self.root / "training" / "runs").mkdir(parents=True, exist_ok=True)
        (self.root / "model-learning" / "patches").mkdir(parents=True, exist_ok=True)
        write_chat_input(self.root)
        for index, case_id in enumerate(case_order):
            count = first_question_count if index == 0 else 5
            answer_file = base / f"{case_id}.trusted-answer.json"
            write_json(
                answer_file,
                {
                    "case_id": case_id,
                    "answers": [
                        {"question_id": f"Q{question_index}", "correct_option": "A"}
                        for question_index in range(1, count + 1)
                    ],
                },
            )
            encrypt_answer(self.root, case_id, answer_file, self.key)
        self.plaintext_answer = base / f"{case_order[0]}.trusted-answer.json"

    def current_case(self) -> tuple[str, int]:
        current = status(self.root)["current_case_id"]
        group = json.loads((self.root / "examples/DEV-GROUP-002/group.json").read_text())
        case = json.loads((self.root / group["cases"][current]).read_text())
        return current, case["questions"]["question_count"]

    def profile(self, applied_rule_ids: list[str] | None = None) -> dict:
        return {
            "topic_tags": ["OTHER"],
            "subject_tags": ["SELF"],
            "time_scope_tags": ["NATAL"],
            "endpoint_tags": ["OTHER"],
            "reasoning_skill_tags": ["EVIDENCE_WEIGHTING"],
            "source_routes": ["S03", "S17"],
            "applied_rule_ids": applied_rule_ids or [],
        }

    def prediction_file(
        self,
        round_id: str,
        correct_count: int,
        *,
        applied_rule_ids: list[str] | None = None,
        include_profile: bool = True,
    ) -> Path:
        case_id, question_count = self.current_case()
        path = self.base / f"{round_id}.prediction.json"
        rows = []
        for index in range(1, question_count + 1):
            top1 = "A" if index <= correct_count else "B"
            top2 = "C"
            option_ids = ["A", "B", "C", "D"]
            ranking = [top1, top2, *[option for option in option_ids if option not in {top1, top2}]]
            ziwei_evidence_id = f"Z-{index}"
            bazi_evidence_id = f"B-{index}"
            row = {
                "question_id": f"Q{index}",
                "top1": top1,
                "top2": top2,
                "public_summary": "The selected option has the strongest relative endpoint closure.",
            }
            if include_profile:
                row["question_profile"] = self.profile(applied_rule_ids)
                row["rule_attribution"] = {
                    "decisive_rule_ids": applied_rule_ids or [],
                    "supporting_rule_ids": [],
                    "counterevidence_rule_ids": [],
                    "decision_changed": bool(applied_rule_ids),
                }
                row["question_semantic_model"] = {
                    "target": "relative event outcome",
                    "subject": "the chart native",
                    "time_range": "the stated scope",
                    "action_subject": "the relevant actor",
                    "reality_object": "the stated real-world object",
                    "event_process": "background, trigger, action, and completion",
                    "completion_endpoint": "observable completion",
                    "magnitude": "relative among the offered choices",
                    "is_composite_narrative": False,
                    "option_atoms": {
                        option: {
                            "required_atoms": [f"{option} required atom"],
                            "distinctive_atoms": [f"{option} distinctive atom"],
                            "severe_irreversible_or_high_precision_atoms": [],
                        }
                        for option in option_ids
                    },
                    "shared_non_discriminating_atoms": ["shared background"],
                    "ambiguities": [],
                }
                row["evidence_ledger"] = [
                    {
                        "evidence_id": ziwei_evidence_id,
                        "track": "ZIWEI",
                        "layer": "NATAL",
                        "chart_fact": f"Ziwei synthetic chart fact {index}",
                        "source_route": "S03",
                        "knowledge_point": "Separate structural capacity from completed endpoint.",
                        "applicability_conditions": ["Ziwei chart fact is present"],
                        "conditions_satisfied": ["Synthetic Ziwei fixture condition is present"],
                        "supports_option_atoms": [f"{top1}:{top1} required atom"],
                        "contradicts_option_atoms": [f"{top2}:{top2} distinctive atom"],
                        "alternative_explanation": "The same structure may remain only background.",
                        "evidence_family_id": f"ZF-{index}",
                        "independence_status": "INDEPENDENT",
                        "reliability": "HIGH",
                        "capability_ceiling": "Does not prove an exact endpoint alone.",
                        "decision_impact": "SUPPORTING",
                        "limitations": "Synthetic fixture has no domain-specific claim.",
                    },
                    {
                        "evidence_id": bazi_evidence_id,
                        "track": "BAZI",
                        "layer": "PERIOD",
                        "chart_fact": f"Bazi synthetic chart fact {index}",
                        "source_route": "S17",
                        "knowledge_point": "Close person, action, object, and endpoint separately.",
                        "applicability_conditions": ["Bazi period fact is present"],
                        "conditions_satisfied": ["Synthetic Bazi fixture condition is present"],
                        "supports_option_atoms": [f"{top1}:{top1} distinctive atom"],
                        "contradicts_option_atoms": [],
                        "alternative_explanation": "The period signal may mark preparation only.",
                        "evidence_family_id": f"BF-{index}",
                        "independence_status": "INDEPENDENT",
                        "reliability": "MEDIUM",
                        "capability_ceiling": "Does not create an unstated real-world action.",
                        "decision_impact": "SUPPORTING",
                        "limitations": "Synthetic fixture has no exact timing claim.",
                    },
                ]
                endpoint_chain = {
                    "subject": "relevant actor",
                    "action": "observable action",
                    "object": "real-world object",
                    "endpoint": "completed outcome",
                }
                row["ziwei_track_seal"] = {
                    "top1": top1,
                    "top2": top2,
                    "ranking": ranking,
                    "core_structure": "Synthetic Ziwei structure supports a relative ranking.",
                    "dynamic_trigger": "Synthetic timing is treated as a trigger, not an endpoint.",
                    "endpoint_chain": endpoint_chain,
                    "supporting_evidence_ids": [ziwei_evidence_id],
                    "contradicting_evidence_ids": [],
                    "alternative_explanations": ["Background without completion"],
                    "unresolved_links": [],
                    "capability_ceiling": "Relative choice only.",
                    "confidence": 70,
                }
                row["bazi_track_seal"] = {
                    "top1": top1,
                    "top2": top2,
                    "ranking": ranking,
                    "strength_and_pattern": "Synthetic strength and pattern candidates were compared.",
                    "method_competition": "Fuyi, regulation, and structural change were compared.",
                    "luck_timing": "Period signal is separated from real-world completion.",
                    "endpoint_chain": endpoint_chain,
                    "supporting_evidence_ids": [bazi_evidence_id],
                    "contradicting_evidence_ids": [],
                    "alternative_explanations": ["Preparation without completion"],
                    "unresolved_links": [],
                    "capability_ceiling": "Relative choice only.",
                    "confidence": 70,
                }
                row["cross_track_arbitration"] = {
                    "agreement_layers": ["relative endpoint direction"],
                    "conflict_layers": [],
                    "conflict_origin": "No material synthetic conflict.",
                    "shared_reality_assumption_risk": "The tracks use separate chart facts.",
                    "stronger_track_for_topic": "EQUAL",
                    "decision": "Fuse equal independent support while retaining limits.",
                    "confidence_reduction_required": False,
                }
                row["final_ranking"] = ranking
                row["option_comparison_matrix"] = {
                    "options": {
                        option: {
                            "required_atom_completion": [f"{option} atom reviewed"],
                            "distinctive_atom_completion": [f"{option} distinction reviewed"],
                            "severe_atoms_have_independent_evidence": True,
                            "ziwei_support_evidence_ids": (
                                [ziwei_evidence_id] if option == top1 else []
                            ),
                            "bazi_support_evidence_ids": (
                                [bazi_evidence_id] if option == top1 else []
                            ),
                            "reality_closure": "Compared at the same endpoint standard.",
                            "timing_closure": "Compared at the same time-layer standard.",
                            "direct_counterevidence_ids": (
                                [ziwei_evidence_id] if option == top2 else []
                            ),
                            "unknown_atoms": [],
                            "shared_background_zeroed": True,
                            "final_rank": ranking.index(option) + 1,
                            "final_rank_reason": "Ranked by distinctive atom closure.",
                        }
                        for option in option_ids
                    },
                    "pairwise": [
                        {
                            "left": left,
                            "right": right,
                            "winner": (
                                left
                                if ranking.index(left) < ranking.index(right)
                                else right
                            ),
                            "reason": "The winner has stronger distinctive endpoint closure.",
                        }
                        for left_index, left in enumerate(option_ids)
                        for right in option_ids[left_index + 1 :]
                    ],
                }
                row["adversarial_review"] = {
                    "top1_weakest_required_atom": f"{top1} required atom",
                    "strongest_competitor": top2,
                    "strongest_reversal_evidence_ids": [ziwei_evidence_id],
                    "ignored_alternative_explanations": ["Background without completion"],
                    "option_wording_inducement": "Checked and not used as chart evidence.",
                    "annual_signal_overweighting": "Checked; timing is not treated as completion.",
                    "bazi_posthoc_agreement": "Checked; Bazi was independently sealed.",
                    "duplicate_evidence_stacking": "Checked by evidence family.",
                    "background_as_endpoint": "Checked and rejected.",
                    "participation_as_action": "Checked and rejected.",
                    "valence_as_mechanism": "Checked and rejected.",
                    "known_rule_execution_omissions": "NONE",
                    "precision_beyond_capability": "No precision beyond the relative choice.",
                    "reversal_test": {
                        "removed_evidence_ids": [ziwei_evidence_id],
                        "ranking_before": ranking,
                        "ranking_after_removal": [top2, top1, *ranking[2:]],
                        "top2_best_explanation": "Top2 could fit the shared background.",
                        "top1_survives": False,
                        "reason": "Removing the strongest evidence temporarily reverses Top1.",
                    },
                }
                row["confidence_components"] = {
                    "input_confidence": 70,
                    "natal_structure_confidence": 70,
                    "subject_confidence": 70,
                    "mechanism_confidence": 70,
                    "timing_confidence": 70,
                    "reality_endpoint_confidence": 70,
                    "cross_track_agreement": 70,
                    "top1_top2_separation": 70,
                    "overall_confidence": 70,
                }
                row["counterfactual_analysis"] = {
                    "full_model_ranking": ranking,
                    "canonical_only_ranking": ranking,
                    "ziwei_only_ranking": ranking,
                    "bazi_only_ranking": ranking,
                    "fused_ranking": ranking,
                    "decisive_rule_ablations": [
                        {
                            "rule_id": rule_id,
                            "ranking_without_rule": [top2, top1, *ranking[2:]],
                            "changes_top1": True,
                            "reason": "The declared decisive rule changes the leading option.",
                        }
                        for rule_id in (applied_rule_ids or [])
                    ],
                }
            rows.append(row)
        state = json.loads((self.root / "training/state.json").read_text())
        replay_remediation = (
            {
                "original_root_causes": ["EVIDENCE_WEIGHTING"],
                "remediation_type": "EXECUTION_GATE",
                "new_idea_executed": "Applied the evidence and endpoint completeness gate.",
                "changed_steps": ["Evidence family grouping", "Full option comparison"],
                "predicted_mechanism_of_improvement": "Reduce repeated background-as-endpoint errors.",
                "new_error_risks": ["Possible underconfidence"],
            }
            if state.get("active_replay_case_id") == case_id
            else None
        )
        write_json(
            path,
            {
                "schema": "PREDICTION-WORKBOOK-V2",
                "case_id": case_id,
                "round_id": round_id,
                "blind_chart_model": {
                    "schema": "BLIND-CHART-MODEL-V1",
                    "input_reliability": {
                        "gender": "known",
                        "calendar": "known",
                        "birth_time": "known",
                        "birth_place": "known",
                        "four_pillars": "known synthetic pillars",
                        "ziwei_coordinates": "known synthetic coordinates",
                        "major_periods": "known synthetic periods",
                        "missing_fields": [],
                        "conflicting_fields": [],
                        "unreliable_fields": [],
                        "forbidden_inferences": ["Do not invent unstated endpoints"],
                    },
                    "ziwei_static_model": {
                        "chart_facts": ["Synthetic Ziwei fact"],
                        "palace_and_star_structures": ["Synthetic palace structure"],
                        "transformations_and_lines": ["Synthetic transformation structure"],
                        "advanced_method_applicability": ["Advanced method conditions checked"],
                        "structural_conflicts": [],
                        "limitations": ["Fixture does not assert real divination content"],
                    },
                    "bazi_static_model": {
                        "chart_facts": ["Synthetic Bazi fact"],
                        "seasonal_strength_candidates": ["Synthetic strength candidate"],
                        "pattern_candidates": ["Synthetic pattern candidate"],
                        "method_competition": ["Synthetic method comparison"],
                        "relations_and_structural_changes": ["Synthetic relation"],
                        "useful_harmful_candidates": ["Synthetic useful candidate"],
                        "unresolved_disputes": [],
                        "limitations": ["Fixture does not assert real divination content"],
                    },
                    "shared_life_structure": {
                        "personality_and_behavior": ["Synthetic behavior structure"],
                        "family_roles": ["Synthetic family structure"],
                        "marriage_capacity": ["Synthetic marriage capacity"],
                        "children_axis": ["Synthetic children axis"],
                        "career_and_wealth": ["Synthetic career structure"],
                        "health_capacity": ["Synthetic health capacity"],
                        "migration_assets_social": ["Synthetic migration structure"],
                        "period_themes": ["Synthetic period theme"],
                        "major_conflicts": [],
                        "unknowns": [],
                    },
                },
                "cross_question_consistency": {
                    "checks": [
                        {
                            "question_id": f"Q{index}",
                            "consistent": True,
                            "conflicts": [],
                            "resolution": "Uses the shared blind chart model.",
                        }
                        for index in range(1, question_count + 1)
                    ],
                    "unresolved_conflicts": [],
                },
                "replay_remediation": replay_remediation,
                "predictions": rows,
            },
        )
        return path

    def run_and_score(
        self,
        round_id: str,
        correct_count: int,
        *,
        applied_rule_ids: list[str] | None = None,
    ) -> dict:
        start_round(self.root, round_id)
        freeze_prediction(
            self.root,
            round_id,
            self.prediction_file(round_id, correct_count, applied_rule_ids=applied_rule_ids),
        )
        return score_round(self.root, round_id, self.base / f"{round_id}.review.json", self.key)

    def patch_file(self, release_id: str, rule_id: str) -> Path:
        path = self.base / f"{release_id}.patch.json"
        write_json(
            path,
            learning_correction(rules=[general_rule(rule_id)]),
        )
        return path


class PolicyTests(unittest.TestCase):
    def test_exact_round_quality_thresholds(self):
        self.assertEqual([required_correct(count) for count in range(1, 5)], [1, 2, 3, 4])
        self.assertEqual(required_correct(5), 4)
        self.assertEqual(required_correct(6), 5)
        self.assertTrue(passed(4, 5))
        self.assertFalse(passed(3, 5))

    def test_validation_and_holdout_cannot_create_rules(self):
        partition = POLICY["dataset_partition_policy"]
        self.assertFalse(partition["validation_can_create_rule"])
        self.assertFalse(partition["final_holdout_can_create_rule"])
        self.assertFalse(
            POLICY["maintenance_policy"][
                "canonical_sources_mutable_during_maintenance"
            ]
        )


class MaintenanceTests(unittest.TestCase):
    def test_short_maintenance_runs_at_twenty_five_first_blind_questions(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary), case_count=6)
            for index in range(1, 6):
                fixture.run_and_score(f"R{index}", 5)
            due = maintenance_due(fixture.root)
            self.assertTrue(due["short_due"])
            result = run_maintenance(fixture.root)
            self.assertTrue(result["performed"])
            self.assertEqual(result["maintenance_type"], "SHORT")
            self.assertFalse(maintenance_due(fixture.root)["due"])
            self.assertTrue(
                (
                    fixture.root
                    / "training/maintenance-reports/MAINTENANCE-001.json"
                ).is_file()
            )
            report = json.loads(
                (
                    fixture.root
                    / "training/maintenance-reports/MAINTENANCE-001.json"
                ).read_text()
            )
            degradation = report["reasoning_degradation"]
            self.assertEqual(degradation["sample_status"], "INSUFFICIENT_SAMPLE")
            self.assertFalse(
                degradation["question_distribution_monitoring"][
                    "automatic_model_change"
                ]
            )
            self.assertTrue(report["training_statistics_unchanged"])

    def test_overconfidence_anomaly_can_trigger_before_fixed_milestone(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary), case_count=6)
            for index in range(1, 6):
                fixture.run_and_score(f"R{index}", 0)
                apply_learning(
                    fixture.root,
                    f"R{index}",
                    fixture.patch_file(
                        f"LEARNING-{index}",
                        f"RULE-OVERCONFIDENT-{index}",
                    ),
                    f"LEARNING-{index}",
                )
            due = maintenance_due(fixture.root)
            self.assertTrue(due["anomaly_due"])
            self.assertIn(
                "OVERCONFIDENCE",
                {row["code"] for row in due["anomalies"]},
            )


class RuntimeTests(unittest.TestCase):
    def test_first_blind_advances_and_streak_uses_distinct_cases(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            score = fixture.run_and_score("R1", 4)
            self.assertTrue(score["passed"])
            self.assertEqual(score["evaluation_kind"], "FIRST_BLIND")
            self.assertFalse(score["spaced_replay_required"])
            current = status(fixture.root)
            self.assertEqual(current["current_case_id"], "DEV-EXAMPLE-002")
            self.assertEqual(current["independent_pass_streak"], 1)
            self.assertEqual(current["status"], "READY_FOR_ROUND")
            fixture.run_and_score("R2", 5)
            current = status(fixture.root)
            self.assertEqual(current["current_case_id"], "DEV-EXAMPLE-003")
            self.assertEqual(current["independent_pass_streak"], 2)
            third_score = fixture.run_and_score("R3", 5)
            self.assertTrue(third_score["independent_stage_gate_met"])
            current = status(fixture.root)
            self.assertEqual(current["current_case_id"], "DEV-EXAMPLE-004")
            self.assertEqual(current["independent_pass_streak"], 3)
            state = json.loads((fixture.root / "training/state.json").read_text())
            self.assertEqual(state["cases"]["DEV-EXAMPLE-001"]["first_blind_round_id"], "R1")
            self.assertEqual(state["cases"]["DEV-EXAMPLE-001"]["replay_round_ids"], [])

    def test_failure_resets_cross_case_streak_and_advances_after_learning(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            fixture.run_and_score("PASS-1", 5)
            score = fixture.run_and_score("R1", 3)
            self.assertFalse(score["passed"])
            self.assertEqual(score["independent_pass_streak_before"], 1)
            self.assertEqual(score["independent_pass_streak_after"], 0)
            self.assertEqual(status(fixture.root)["status"], "LEARNING_REQUIRED")
            with self.assertRaises(TrainingError):
                start_round(fixture.root, "BLOCKED")
            release = apply_learning(
                fixture.root,
                "R1",
                fixture.patch_file("LEARNING-001", "RULE-GENERAL-ENDPOINT"),
                "LEARNING-001",
            )
            self.assertEqual(release["parent_release"], "MODEL-BASELINE-001")
            self.assertEqual(status(fixture.root)["current_case_id"], "DEV-EXAMPLE-003")
            self.assertEqual(status(fixture.root)["spaced_replay_queue_size"], 1)
            ledger = load_learning_ledger(fixture.root)
            self.assertEqual(ledger["rule_evidence"]["RULE-GENERAL-ENDPOINT"]["status"], "CANDIDATE")

    def test_failed_first_blind_prefers_next_new_case_over_older_due_replay(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary), case_count=8)
            fixture.run_and_score("FAIL-1", 3)
            apply_learning(
                fixture.root,
                "FAIL-1",
                fixture.patch_file("LEARNING-001", "RULE-GENERAL-ENDPOINT"),
                "LEARNING-001",
            )
            for index in range(2, 7):
                fixture.run_and_score(f"NEW-{index}", 5)
            self.assertEqual(
                status(fixture.root)["active_replay_case_id"],
                "DEV-EXAMPLE-001",
            )
            fixture.run_and_score("REPLAY-1", 5)
            self.assertEqual(
                status(fixture.root)["current_case_id"],
                "DEV-EXAMPLE-007",
            )

            state_path = fixture.root / "training" / "state.json"
            state = json.loads(state_path.read_text())
            state["spaced_replay_queue"].append(
                {
                    "case_id": "DEV-EXAMPLE-002",
                    "eligible_after_first_blind_count": 6,
                },
            )
            state["cases"]["DEV-EXAMPLE-002"]["remediation_status"] = "QUEUED"
            write_json(state_path, state)
            write_chat_input(fixture.root)

            fixture.run_and_score("FAIL-7", 3)
            apply_learning(
                fixture.root,
                "FAIL-7",
                fixture.patch_file(
                    "LEARNING-007",
                    "RULE-FAILED-FIRST-BLIND-NEXT-NEW",
                ),
                "LEARNING-007",
            )
            current = status(fixture.root)
            self.assertEqual(current["current_case_id"], "DEV-EXAMPLE-008")
            self.assertIsNone(current["active_replay_case_id"])
            self.assertEqual(current["spaced_replay_queue_size"], 2)

    def test_failed_case_replays_only_after_five_new_cases_and_does_not_count_as_new_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary), case_count=7)
            fixture.run_and_score("FAIL-1", 3)
            apply_learning(
                fixture.root,
                "FAIL-1",
                fixture.patch_file("LEARNING-001", "RULE-GENERAL-ENDPOINT"),
                "LEARNING-001",
            )
            for index in range(2, 7):
                fixture.run_and_score(f"NEW-{index}", 5)
            current = status(fixture.root)
            self.assertEqual(current["current_case_id"], "DEV-EXAMPLE-001")
            self.assertEqual(current["active_replay_case_id"], "DEV-EXAMPLE-001")
            bundle = json.loads((fixture.root / CHAT_INPUT_RELATIVE_PATH).read_text())
            self.assertEqual(bundle["state_summary"]["current_case_id"], "DEV-EXAMPLE-001")
            self.assertEqual(bundle["state_summary"]["evaluation_kind"], "SPACED_REPLAY")
            streak_before = current["independent_pass_streak"]
            replay = fixture.run_and_score("REPLAY-1", 5)
            self.assertEqual(replay["evaluation_kind"], "SPACED_REPLAY")
            current = status(fixture.root)
            self.assertEqual(current["current_case_id"], "DEV-EXAMPLE-007")
            self.assertEqual(current["independent_pass_streak"], streak_before)
            self.assertEqual(current["spaced_replay_queue_size"], 0)
            ledger = load_learning_ledger(fixture.root)
            self.assertEqual(ledger["first_blind_totals"]["cases"], 6)

    def test_failed_replay_returns_to_new_case_before_another_due_replay(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary), case_count=8)
            fixture.run_and_score("FAIL-1", 3)
            apply_learning(
                fixture.root,
                "FAIL-1",
                fixture.patch_file("LEARNING-001", "RULE-GENERAL-ENDPOINT"),
                "LEARNING-001",
            )
            for index in range(2, 7):
                fixture.run_and_score(f"NEW-{index}", 5)
            self.assertEqual(
                status(fixture.root)["active_replay_case_id"],
                "DEV-EXAMPLE-001",
            )
            state_path = fixture.root / "training" / "state.json"
            state = json.loads(state_path.read_text())
            state["spaced_replay_queue"].insert(
                1,
                {
                    "case_id": "DEV-EXAMPLE-002",
                    "eligible_after_first_blind_count": 6,
                },
            )
            state["cases"]["DEV-EXAMPLE-002"]["remediation_status"] = "QUEUED"
            write_json(state_path, state)
            write_chat_input(fixture.root)
            fixture.run_and_score("REPLAY-FAIL", 3)
            apply_learning(
                fixture.root,
                "REPLAY-FAIL",
                fixture.patch_file(
                    "LEARNING-REPLAY-FAIL",
                    "RULE-REPLAY-FAIL-GATE",
                ),
                "LEARNING-REPLAY-FAIL",
            )
            current = status(fixture.root)
            self.assertEqual(current["current_case_id"], "DEV-EXAMPLE-007")
            self.assertIsNone(current["active_replay_case_id"])
            self.assertEqual(current["spaced_replay_queue_size"], 2)

    def test_question_profile_is_required_and_taxonomy_checked(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            start_round(fixture.root, "R1")
            with self.assertRaises(TrainingError):
                freeze_prediction(
                    fixture.root,
                    "R1",
                    fixture.prediction_file("R1", 5, include_profile=False),
                )

    def test_future_cases_not_replays_validate_candidate_rules(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            fixture.run_and_score("R1", 3)
            apply_learning(
                fixture.root,
                "R1",
                fixture.patch_file("LEARNING-001", "RULE-GENERAL-ENDPOINT"),
                "LEARNING-001",
            )
            fixture.run_and_score("R2", 5, applied_rule_ids=["RULE-GENERAL-ENDPOINT"])
            fixture.run_and_score("R3", 5, applied_rule_ids=["RULE-GENERAL-ENDPOINT"])
            evidence = load_learning_ledger(fixture.root)["rule_evidence"]["RULE-GENERAL-ENDPOINT"]
            self.assertEqual(evidence["status"], "PROVISIONAL")
            fixture.run_and_score("R4", 5, applied_rule_ids=["RULE-GENERAL-ENDPOINT"])
            evidence = load_learning_ledger(fixture.root)["rule_evidence"]["RULE-GENERAL-ENDPOINT"]
            self.assertEqual(evidence["status"], "VALIDATED")
            self.assertEqual(evidence["supporting_applications"], 15)
            self.assertEqual(len(evidence["distinct_support_cases"]), 3)

    def test_unrelated_question_does_not_validate_rule(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            fixture.run_and_score("R1", 3)
            apply_learning(
                fixture.root,
                "R1",
                fixture.patch_file("LEARNING-001", "RULE-GENERAL-ENDPOINT"),
                "LEARNING-001",
            )
            fixture.run_and_score("R2", 5)
            evidence = load_learning_ledger(fixture.root)["rule_evidence"]["RULE-GENERAL-ENDPOINT"]
            self.assertEqual(evidence["applications"], 0)
            self.assertEqual(evidence["status"], "CANDIDATE")

    def test_metrics_are_question_level_by_topic_and_skill(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            fixture.run_and_score("R1", 4)
            ledger = load_learning_ledger(fixture.root)
            self.assertEqual(ledger["first_blind_totals"]["cases"], 1)
            self.assertEqual(ledger["first_blind_totals"]["questions"], 5)
            self.assertEqual(ledger["topic_metrics"]["OTHER"]["top1_correct"], 4)
            self.assertEqual(ledger["reasoning_skill_metrics"]["EVIDENCE_WEIGHTING"]["questions"], 5)

    def test_group_completes_after_one_first_blind_per_case(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            for index in range(1, 6):
                fixture.run_and_score(f"R{index}", 5)
            current = status(fixture.root)
            self.assertEqual(current["status"], "GROUP_COMPLETE")
            self.assertIsNone(current["current_case_id"])
            bundle = json.loads((fixture.root / CHAT_INPUT_RELATIVE_PATH).read_text())
            self.assertFalse(bundle["state_summary"]["prediction_allowed"])
            self.assertIsNone(bundle["state_summary"]["recommended_round_id"])

    def test_chat_input_is_safe_and_points_to_next_unseen_case(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            fixture.run_and_score("R1", 4)
            bundle = json.loads((fixture.root / CHAT_INPUT_RELATIVE_PATH).read_text())
            serialized = json.dumps(bundle, ensure_ascii=False)
            self.assertEqual(bundle["schema"], "CHAT-PREDICTION-INPUT-V3")
            handoff = bundle["chat_work_handoff_contract"]
            self.assertEqual(handoff["schema"], "CHAT-WORK-HANDOFF-CONTRACT-V2")
            self.assertEqual(
                handoff["binding"]["case_id"],
                bundle["state_summary"]["current_case_id"],
            )
            self.assertEqual(
                handoff["binding"]["round_id"],
                bundle["state_summary"]["recommended_round_id"],
            )
            self.assertEqual(
                handoff["binding"]["model_release"],
                bundle["state_summary"]["current_model_release"],
            )
            self.assertNotIn(
                "evaluation_kind",
                handoff["training_issue_input_contract"]["allowed_top_level_fields"],
            )
            self.assertIn(
                "learning_release_id",
                handoff["training_issue_input_contract"]["pass_forbidden_fields"],
            )
            handoff_template = handoff["handoff_payload_template"]
            self.assertIn(
                "prediction_access_execution_receipt",
                handoff["handoff_required_fields"],
            )
            access_receipt = handoff_template[
                "prediction_access_execution_receipt"
            ]
            self.assertEqual(
                access_receipt["first_repository_read"],
                "chat-input/prediction-access-contract.json",
            )
            self.assertEqual(access_receipt["pre_contract_repository_reads"], [])
            self.assertTrue(
                access_receipt["contract_executed_before_followup_reads"]
            )
            self.assertEqual(
                access_receipt["required_followup_reads"],
                ["training/state.json", "chat-input/current.json"],
            )
            self.assertEqual(
                set(handoff_template["blind_chart_model"]),
                {
                    "schema",
                    "input_reliability",
                    "ziwei_static_model",
                    "bazi_static_model",
                    "shared_life_structure",
                },
            )
            template_ref = handoff["prediction_row_template_ref"]
            prediction_template = json.loads(
                (fixture.root / template_ref["path"]).read_text()
            )
            self.assertEqual(
                object_sha256(prediction_template),
                template_ref["sha256"],
            )
            for track_name in ("ziwei_track_seal", "bazi_track_seal"):
                track = prediction_template[track_name]
                self.assertIn(
                    "EXCLUSIVE_FROM_CONTRADICTING_SET",
                    track["supporting_evidence_ids"][0],
                )
                self.assertIsInstance(track["confidence"], str)
            reversal = prediction_template["adversarial_review"]["reversal_test"]
            self.assertIn("DERIVED_FROM_RANKING", reversal["top1_survives"])
            confidence = prediction_template["confidence_components"]
            self.assertIn(
                "WEAKEST_NON_OVERALL_COMPONENT",
                confidence["overall_confidence"],
            )
            ablations = prediction_template["counterfactual_analysis"][
                "decisive_rule_ablations"
            ]
            self.assertEqual(len(ablations), 1)
            self.assertEqual(
                set(ablations[0]),
                {"rule_id", "ranking_without_rule", "changes_top1", "reason"},
            )
            self.assertEqual(
                set(prediction_template),
                {
                    "question_id",
                    "top1",
                    "top2",
                    "public_summary",
                    "question_profile",
                    "rule_attribution",
                    "question_semantic_model",
                    "ziwei_track_seal",
                    "bazi_track_seal",
                    "cross_track_arbitration",
                    "evidence_ledger",
                    "final_ranking",
                    "option_comparison_matrix",
                    "adversarial_review",
                    "confidence_components",
                    "counterfactual_analysis",
                },
            )
            constraints = handoff["serialization_constraints"]
            self.assertTrue(constraints["exact_fields_only"])
            self.assertFalse(constraints["chat_local_preflight_required"])
            self.assertEqual(
                constraints["confidence_unit"],
                "INTEGER_PERCENT_0_TO_100",
            )
            self.assertIn(
                "disjoint", constraints["track_evidence_partition_rule"]
            )
            self.assertIn(
                "weakest", constraints["overall_confidence_cap_rule"]
            )
            self.assertIn(
                "exactly one", constraints["decisive_rule_ablation_rule"]
            )
            self.assertIn(
                "Derive top1_survives",
                constraints["reversal_test_consistency_rule"],
            )
            self.assertEqual(
                constraints["normalization_authority"],
                "GITHUB_CONTROLLER",
            )
            self.assertEqual(
                constraints["chat_required_capabilities"],
                ["GITHUB_FETCH_FILE", "GITHUB_CREATE_ISSUE"],
            )
            self.assertIn(
                "CHALLENGED",
                constraints["rule_status_normalization"],
            )
            self.assertEqual(
                constraints["github_issue_body_hard_limit_characters"],
                GITHUB_ISSUE_BODY_MAX_CHARACTERS,
            )
            self.assertEqual(
                constraints["target_max_characters"],
                HANDOFF_TARGET_MAX_CHARACTERS,
            )
            self.assertLess(
                HANDOFF_TARGET_MAX_CHARACTERS,
                GITHUB_ISSUE_BODY_MAX_CHARACTERS,
            )
            self.assertEqual(bundle["state_summary"]["current_case_id"], "DEV-EXAMPLE-002")
            self.assertEqual(
                bundle["state_summary"]["training_unit"],
                "FIRST_BLIND_CASE_WITH_SPACED_REPLAY",
            )
            self.assertEqual(bundle["state_summary"]["independent_pass_streak"], 1)
            self.assertEqual(bundle["state_summary"]["required_consecutive_independent_passes"], 3)
            self.assertEqual(bundle["current_model"]["knowledge_cards"]["card_count"], 0)
            self.assertEqual(
                bundle["current_model"]["knowledge_cards"]["authority"],
                "DERIVED_ROUTING_AND_PROCEDURE_ONLY",
            )
            self.assertNotIn("general reasoning", serialized)
            access = bundle["prediction_access_contract"]
            self.assertEqual(access["enforcement"], "DEFAULT_DENY_FAIL_CLOSED")
            self.assertEqual(access["allowed_tool_classes"], ["GITHUB_FETCH_FILE"])
            self.assertFalse(access["file_library_allowed"])
            self.assertFalse(access["chat_attachments_allowed"])
            self.assertFalse(access["historical_uploads_allowed"])
            self.assertFalse(access["cross_conversation_memory_allowed"])
            self.assertNotIn('"top1_correct"', serialized)
            self.assertNotIn('"correct_option"', serialized)

    def test_prediction_access_is_main_only_and_fail_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            state = json.loads((fixture.root / "training/state.json").read_text())
            allowed = {
                "tool_class": "GITHUB_FETCH_FILE",
                "context_source": "GITHUB_MAIN",
                "repository": "chinaneedM/ziwei-bazi-model",
                "ref": "main",
            }
            for path in (
                "chat-input/prediction-access-contract.json",
                "training/state.json",
                "chat-input/current.json",
                "chat-input/runtime-model.json",
                "chat-input/prediction-row-template.json",
                "sources/canonical-runtime-manifest.json",
                "sources/canonical-runtime/S03/index.json",
                "sources/canonical-runtime/S03/segment-0001.txt",
                "model-learning/releases/MODEL-BASELINE-001.json",
                "config/training-policy.json",
            ):
                assert_prediction_access(
                    fixture.root,
                    state,
                    path=path,
                    **allowed,
                )
            denied_requests = (
                {**allowed, "path": "answer-vault/formal/CASE-001.json.fernet"},
                {**allowed, "path": "training/runs/ROUND-001/round.json"},
                {**allowed, "path": "model-learning/releases/MODEL-LEARNING-015.json"},
                {**allowed, "path": "case-bank/cases/CASE-001.json"},
                {**allowed, "path": "README.md"},
                {**allowed, "path": "sources/canonical/S03_test.txt"},
                {
                    **allowed,
                    "tool_class": "FILE_LIBRARY_READ",
                    "context_source": "FILE_LIBRARY",
                    "path": "sources/canonical-runtime/S03/segment-0001.txt",
                },
                {
                    **allowed,
                    "tool_class": "ATTACHMENT_FILE_READ",
                    "context_source": "CHAT_ATTACHMENTS",
                    "path": "sources/canonical-runtime/S03/segment-0001.txt",
                },
                {
                    **allowed,
                    "tool_class": "PERSONAL_CONTEXT_SEARCH",
                    "context_source": "PERSONAL_CONTEXT",
                    "path": "training/state.json",
                },
                {**allowed, "ref": "old-branch", "path": "training/state.json"},
            )
            for request in denied_requests:
                with self.subTest(request=request):
                    with self.assertRaises(TrainingError):
                        assert_prediction_access(
                            fixture.root,
                            state,
                            **request,
                        )

    def test_prediction_access_contract_must_be_first_repository_read(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            contract = json.loads(
                (fixture.root / PREDICTION_ACCESS_CONTRACT_PATH).read_text()
            )
            common = {
                "tool_class": "GITHUB_FETCH_FILE",
                "context_source": "GITHUB_MAIN",
                "repository": "chinaneedM/ziwei-bazi-model",
                "ref": "main",
            }

            session = PredictionAccessSession()
            with self.assertRaises(TrainingError):
                session.authorize_repository_read(
                    **common,
                    path="training/state.json",
                )
            with self.assertRaises(TrainingError):
                session.authorize_bootstrap_fetch(
                    **common,
                    path="chat-input/current.json",
                )

            session.authorize_bootstrap_fetch(
                **common,
                path=PREDICTION_ACCESS_CONTRACT_PATH.as_posix(),
            )
            with self.assertRaises(TrainingError):
                session.authorize_repository_read(
                    **common,
                    path="training/state.json",
                )
            session.execute_contract(contract)
            session.authorize_repository_read(
                **common,
                path="training/state.json",
            )
            session.authorize_repository_read(
                **common,
                path="chat-input/current.json",
            )
            with self.assertRaises(TrainingError):
                session.authorize_repository_read(
                    **common,
                    path="answer-vault/formal/CASE-001.json.fernet",
                )

    def test_post_prediction_handoff_requires_freeze_and_allows_one_issue(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            bundle = json.loads(
                (fixture.root / CHAT_INPUT_RELATIVE_PATH).read_text()
            )
            handoff = bundle["chat_work_handoff_contract"]
            session = PostPredictionHandoffSession(
                fixture.root,
                contract=bundle["prediction_access_contract"],
                expected_binding=handoff["binding"],
                expected_issue_title=handoff["issue_title"],
            )
            request = {
                "tool_class": "GITHUB_CREATE_ISSUE",
                "repository": "chinaneedM/ziwei-bazi-model",
                "ref": "main",
                "issue_title": handoff["issue_title"],
            }
            with self.assertRaisesRegex(TrainingError, "denied during prediction"):
                session.authorize_issue_create(**request)
            with self.assertRaisesRegex(TrainingError, "freeze is required"):
                session.enter_post_prediction_handoff(
                    prediction_frozen=False,
                    workbook_schema_complete=True,
                    binding=handoff["binding"],
                    receipt=handoff["handoff_payload_template"][
                        "prediction_access_execution_receipt"
                    ],
                )
            session.enter_post_prediction_handoff(
                prediction_frozen=True,
                workbook_schema_complete=True,
                binding=handoff["binding"],
                receipt=handoff["handoff_payload_template"][
                    "prediction_access_execution_receipt"
                ],
            )
            self.assertEqual(session.phase, "POST_PREDICTION_HANDOFF")
            session.authorize_issue_create(**request)
            with self.assertRaisesRegex(TrainingError, "only one"):
                session.authorize_issue_create(**request)

    def test_git_only_runtime_without_project_sources_is_complete(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            self.assertFalse((fixture.root / "project-sources").exists())
            self.assertFalse((fixture.root / "file-library").exists())
            contract = json.loads(
                (fixture.root / PREDICTION_ACCESS_CONTRACT_PATH).read_text()
            )
            bundle = json.loads(
                (fixture.root / CHAT_INPUT_RELATIVE_PATH).read_text()
            )
            common = {
                "tool_class": "GITHUB_FETCH_FILE",
                "context_source": "GITHUB_MAIN",
                "repository": "chinaneedM/ziwei-bazi-model",
                "ref": "main",
            }
            startup = PredictionAccessSession()
            startup.authorize_bootstrap_fetch(
                **common,
                path=PREDICTION_ACCESS_CONTRACT_PATH.as_posix(),
            )
            startup.execute_contract(contract)
            startup.authorize_repository_read(
                **common,
                path="sources/canonical-runtime/S00/segment-0001.txt",
            )
            startup.authorize_repository_read(
                **common,
                path=CHAT_RUNTIME_MODEL_RELATIVE_PATH.as_posix(),
            )
            for tool_class, context_source in (
                ("FILE_LIBRARY_READ", "FILE_LIBRARY"),
                ("ATTACHMENT_FILE_READ", "CHAT_ATTACHMENTS"),
                ("PERSONAL_CONTEXT_SEARCH", "PERSONAL_CONTEXT"),
            ):
                with self.assertRaises(TrainingError):
                    startup.authorize_repository_read(
                        tool_class=tool_class,
                        context_source=context_source,
                        repository="chinaneedM/ziwei-bazi-model",
                        ref="main",
                        path="sources/canonical-runtime/S00/segment-0001.txt",
                    )
            runtime_model = json.loads(
                (fixture.root / CHAT_RUNTIME_MODEL_RELATIVE_PATH).read_text()
            )
            self.assertFalse(
                runtime_model["knowledge_workbench_chat_read_allowed"]
            )
            self.assertEqual(
                runtime_model["knowledge_card_runtime_authority"],
                "chat-input/runtime-model.json#knowledge_cards",
            )
            policy = load_post_prediction_handoff_policy(fixture.root)
            self.assertFalse(policy["chat_local_preflight_required"])
            handoff = bundle["chat_work_handoff_contract"]
            post = PostPredictionHandoffSession(
                fixture.root,
                contract=contract,
                expected_binding=handoff["binding"],
                expected_issue_title=handoff["issue_title"],
            )
            post.enter_post_prediction_handoff(
                prediction_frozen=True,
                workbook_schema_complete=True,
                binding=handoff["binding"],
                receipt=handoff["handoff_payload_template"][
                    "prediction_access_execution_receipt"
                ],
            )
            post.authorize_issue_create(
                tool_class="GITHUB_CREATE_ISSUE",
                repository="chinaneedM/ziwei-bazi-model",
                ref="main",
                issue_title=handoff["issue_title"],
            )

    def test_short_chat_commands_cannot_reintroduce_state_first_startup(self):
        prompt = (
            Path(__file__).resolve().parents[1]
            / "docs"
            / "PROJECT-BOOTSTRAP-R1.txt"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "PREDICTION_STARTUP_FIRST_ACTION=GITHUB_FETCH_FILE "
            "main/chat-input/prediction-access-contract.json",
            prompt,
        )
        self.assertIn(
            "first and only first repository read",
            prompt,
        )
        retired = (
            Path(__file__).resolve().parents[1]
            / "docs"
            / "PROJECT-MAIN-PROMPT-R2.txt"
        ).read_text(encoding="utf-8")
        self.assertIn("PROJECT_INSTRUCTION_STATUS=RETIRED", retired)
        self.assertNotIn("PROJECT_INSTRUCTION_STATUS=ACTIVE", retired)

    def test_non_executed_contaminated_round_is_skipped_without_counting(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            state_path = fixture.root / "training/state.json"
            state = json.loads(state_path.read_text())
            state["round_id_prefix"] = "FORMAL-ROUND"
            state["round_sequence"] = 1
            state["non_executed_rounds"] = [
                {
                    "round_id": "FORMAL-ROUND-001",
                    "case_id": "QUARANTINED-CASE",
                    "status": "PRE-FREEZE_CONTAMINATED_NOT_EXECUTED",
                    "prediction_frozen": False,
                    "scored": False,
                    "counts_toward_first_blind": False,
                    "prediction_directions_retained": False,
                    "reason": "PREDICTION_CONTEXT_ALLOWLIST_VIOLATION",
                    "recorded_at": "2026-07-25T00:00:00Z",
                }
            ]
            write_json(state_path, state)
            write_chat_input(fixture.root)
            started = start_round(fixture.root, "FORMAL-ROUND-002")
            updated = json.loads(state_path.read_text())
            self.assertEqual(started["round_id"], "FORMAL-ROUND-002")
            self.assertEqual(updated["round_count"], 1)
            self.assertEqual(updated["round_sequence"], 2)
            self.assertEqual(
                updated["non_executed_rounds"][0]["status"],
                "PRE-FREEZE_CONTAMINATED_NOT_EXECUTED",
            )
    def test_scoring_before_freeze_and_second_freeze_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            start_round(fixture.root, "R1")
            with self.assertRaises(TrainingError):
                score_round(fixture.root, "R1", fixture.base / "early-review.json", fixture.key)
            prediction = fixture.prediction_file("R1", 5)
            freeze_prediction(fixture.root, "R1", prediction)
            with self.assertRaises(TrainingError):
                freeze_prediction(fixture.root, "R1", prediction)

    def test_external_answer_is_read_only_after_freeze(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            case_id, _ = fixture.current_case()
            (fixture.root / "answer-vault" / "encrypted" / f"{case_id}.json.fernet").unlink()
            start_round(fixture.root, "R1")
            freeze_prediction(fixture.root, "R1", fixture.prediction_file("R1", 5))
            score = score_round(
                fixture.root,
                "R1",
                fixture.base / "external.review.json",
                answer_file=fixture.plaintext_answer,
            )
            self.assertTrue(score["passed"])
            self.assertEqual(score["answer_source"], "EXTERNAL_POST_FREEZE_FILE")

    def test_unscored_question_is_excluded_from_threshold_and_learning_metrics(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            case_id, _ = fixture.current_case()
            answer_file = fixture.base / "answer-with-unscored.json"
            write_json(
                answer_file,
                {
                    "case_id": case_id,
                    "answers": [
                        *[
                            {"question_id": f"Q{index}", "correct_option": "A"}
                            for index in range(1, 5)
                        ],
                        {
                            "question_id": "Q5",
                            "scoring_status": "UNSCORED",
                            "reason_code": "NO_VALID_OPTION",
                        },
                    ],
                },
            )
            start_round(fixture.root, "R1")
            freeze_prediction(
                fixture.root,
                "R1",
                fixture.prediction_file("R1", 4),
            )
            review_path = fixture.base / "unscored.review.json"
            score = score_round(
                fixture.root,
                "R1",
                review_path,
                answer_file=answer_file,
            )
            self.assertTrue(score["passed"])
            self.assertEqual(score["question_count"], 5)
            self.assertEqual(score["scoreable_question_count"], 4)
            self.assertEqual(score["unscored_question_count"], 1)
            self.assertEqual(score["required_correct"], 4)
            detailed = json.loads(review_path.read_text(encoding="utf-8"))
            self.assertFalse(detailed["questions"][-1]["is_scored"])
            self.assertNotIn("correct_option", detailed["questions"][-1])
            ledger = load_learning_ledger(fixture.root)
            self.assertEqual(ledger["first_blind_totals"]["cases"], 1)
            self.assertEqual(ledger["first_blind_totals"]["questions"], 4)

    def test_case_specific_learning_rule_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            fixture.run_and_score("R1", 0)
            rule = general_rule("RULE-LEAKING")
            rule["statement"] = "DEV-EXAMPLE-001 Q1 should choose A."
            patch = fixture.base / "leaking-patch.json"
            write_json(patch, learning_correction(rules=[rule]))
            with self.assertRaises(TrainingError):
                apply_learning(fixture.root, "R1", patch, "LEAKING")


class ReasoningExecutionLayerTests(unittest.TestCase):
    def test_high_confidence_unclosed_link_is_counted_as_an_integer(self):
        report = build_completeness_report(
            {},
            [
                {
                    "evidence_ledger": [
                        {
                            "evidence_family_id": "FAMILY-1",
                            "decision_impact": "SUPPORTING",
                        }
                    ],
                    "cross_track_arbitration": {"conflict_layers": []},
                    "counterfactual_analysis": {"decisive_rule_ablations": []},
                    "confidence_components": {"overall_confidence": 80},
                    "ziwei_track_seal": {"unresolved_links": ["unclosed endpoint"]},
                    "bazi_track_seal": {"unresolved_links": []},
                }
            ],
            {"unresolved_conflicts": []},
        )
        self.assertEqual(report["high_confidence_with_unclosed_critical_link"], 1)

    def assert_freeze_rejected(self, mutate) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            path = fixture.prediction_file("R1", 4)
            payload = json.loads(path.read_text())
            mutate(payload)
            write_json(path, payload)
            start_round(fixture.root, "R1")
            with self.assertRaises(TrainingError):
                freeze_prediction(fixture.root, "R1", path)
            self.assertFalse(
                (fixture.root / "training/runs/R1/prediction-freeze.json").exists()
            )

    def test_missing_blind_chart_or_independent_track_seal_is_rejected(self):
        self.assert_freeze_rejected(lambda payload: payload.pop("blind_chart_model"))
        self.assert_freeze_rejected(
            lambda payload: payload["predictions"][0].pop("ziwei_track_seal")
        )
        self.assert_freeze_rejected(
            lambda payload: payload["predictions"][0].pop("bazi_track_seal")
        )

    def test_source_only_evidence_and_missing_applicability_are_rejected(self):
        self.assert_freeze_rejected(
            lambda payload: payload["predictions"][0]["evidence_ledger"][0].update(
                {"chart_fact": ""}
            )
        )
        self.assert_freeze_rejected(
            lambda payload: payload["predictions"][0]["evidence_ledger"][0].update(
                {"applicability_conditions": []}
            )
        )

    def test_same_chart_fact_must_share_one_evidence_family(self):
        def mutate(payload):
            row = payload["predictions"][0]
            duplicate = dict(row["evidence_ledger"][0])
            duplicate["evidence_id"] = "Z-DUPLICATE"
            duplicate["evidence_family_id"] = "DIFFERENT-FAMILY"
            row["evidence_ledger"].append(duplicate)

        self.assert_freeze_rejected(mutate)

    def test_full_option_matrix_and_real_reversal_test_are_required(self):
        self.assert_freeze_rejected(
            lambda payload: payload["predictions"][0][
                "option_comparison_matrix"
            ]["pairwise"].pop()
        )
        self.assert_freeze_rejected(
            lambda payload: payload["predictions"][0]["adversarial_review"][
                "reversal_test"
            ].update({"removed_evidence_ids": []})
        )

    def test_overall_confidence_cannot_exceed_weakest_component(self):
        self.assert_freeze_rejected(
            lambda payload: payload["predictions"][0][
                "confidence_components"
            ].update({"overall_confidence": 80})
        )

    def test_timing_only_and_unproved_high_precision_atoms_are_rejected(self):
        def timing_only(payload):
            for evidence in payload["predictions"][0]["evidence_ledger"]:
                evidence["layer"] = "YEAR"

        self.assert_freeze_rejected(timing_only)
        def add_unproved_top1_precision(payload):
            row = payload["predictions"][0]
            top1 = row["top1"]
            row["question_semantic_model"]["option_atoms"][top1].update(
                {
                    "severe_irreversible_or_high_precision_atoms": [
                        "exact irreversible endpoint"
                    ]
                }
            )
            row["option_comparison_matrix"]["options"][top1][
                "severe_atoms_have_independent_evidence"
            ] = False

        self.assert_freeze_rejected(add_unproved_top1_precision)

    def test_noncomposite_specific_year_question_can_use_timing_only_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            path = fixture.prediction_file("R1", 4)
            payload = json.loads(path.read_text())
            row = payload["predictions"][0]
            row["question_semantic_model"]["is_composite_narrative"] = False
            row["question_profile"]["time_scope_tags"] = ["SPECIFIC_YEAR"]
            for evidence in row["evidence_ledger"]:
                evidence["layer"] = "YEAR"
            write_json(path, payload)
            start_round(fixture.root, "R1")
            frozen = freeze_prediction(fixture.root, "R1", path)
            self.assertEqual(frozen["schema"], "FROZEN-PREDICTION-V2")

    def test_noncomposite_period_window_question_can_use_timing_only_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            path = fixture.prediction_file("R1", 4)
            payload = json.loads(path.read_text())
            row = payload["predictions"][0]
            row["question_semantic_model"]["is_composite_narrative"] = False
            row["question_profile"]["time_scope_tags"] = ["OTHER"]
            windows = ["12-21岁", "22-31岁", "32-41岁", "42-51岁"]
            for option_id, window in zip(
                row["question_semantic_model"]["option_atoms"],
                windows,
                strict=True,
            ):
                row["question_semantic_model"]["option_atoms"][option_id] = {
                    "required_atoms": [window],
                    "distinctive_atoms": [window],
                    "severe_irreversible_or_high_precision_atoms": [],
                }
            for evidence in row["evidence_ledger"]:
                evidence["layer"] = "PERIOD"
            write_json(path, payload)
            start_round(fixture.root, "R1")
            frozen = freeze_prediction(fixture.root, "R1", path)
            self.assertEqual(frozen["schema"], "FROZEN-PREDICTION-V2")

    def test_noncomposite_nontemporal_question_rejects_timing_only_evidence(self):
        def make_timing_only(payload):
            row = payload["predictions"][0]
            row["question_semantic_model"]["is_composite_narrative"] = False
            row["question_profile"]["time_scope_tags"] = ["OTHER"]
            for evidence in row["evidence_ledger"]:
                evidence["layer"] = "PERIOD"

        self.assert_freeze_rejected(make_timing_only)

    def test_unproved_high_precision_atom_on_losing_option_remains_comparable(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            path = fixture.prediction_file("R1", 4)
            payload = json.loads(path.read_text())
            row = payload["predictions"][0]
            losing_option = row["final_ranking"][-1]
            row["question_semantic_model"]["option_atoms"][losing_option].update(
                {
                    "severe_irreversible_or_high_precision_atoms": [
                        "unclosed losing-option endpoint"
                    ]
                }
            )
            write_json(path, payload)
            start_round(fixture.root, "R1")
            frozen = freeze_prediction(fixture.root, "R1", path)
            self.assertEqual(frozen["schema"], "FROZEN-PREDICTION-V2")

    def test_decisive_rule_must_change_top1_under_ablation(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            fixture.run_and_score("R1", 0)
            apply_learning(
                fixture.root,
                "R1",
                fixture.patch_file("LEARNING-1", "RULE-ABLATION"),
                "LEARNING-1",
            )
            path = fixture.prediction_file(
                "R2",
                4,
                applied_rule_ids=["RULE-ABLATION"],
            )
            payload = json.loads(path.read_text())
            row = payload["predictions"][0]
            row["counterfactual_analysis"]["decisive_rule_ablations"][0][
                "ranking_without_rule"
            ] = row["final_ranking"]
            write_json(path, payload)
            start_round(fixture.root, "R2")
            with self.assertRaises(TrainingError):
                freeze_prediction(fixture.root, "R2", path)

    def test_failed_round_can_publish_non_rule_process_correction(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            fixture.run_and_score("R1", 0)
            patch = fixture.base / "execution-gate.json"
            write_json(
                patch,
                learning_correction(
                    remediation_type="EXECUTION_GATE",
                    rules=[],
                ),
            )
            release = apply_learning(
                fixture.root,
                "R1",
                patch,
                "LEARNING-EXECUTION-GATE",
            )
            self.assertEqual(release["release_id"], "LEARNING-EXECUTION-GATE")
            self.assertEqual(load_learning_ledger(fixture.root)["rule_evidence"], {})
            bundle = json.loads(
                (fixture.root / CHAT_INPUT_RELATIVE_PATH).read_text()
            )
            self.assertEqual(
                json.loads(
                    (
                        fixture.root
                        / bundle["current_model"]["compiled_runtime_model_ref"][
                            "path"
                        ]
                    ).read_text()
                )["active_process_corrections"][-1]["remediation_type"],
                "EXECUTION_GATE",
            )

    def test_retired_rule_cannot_enter_a_new_prediction(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            fixture.run_and_score("R1", 0)
            apply_learning(
                fixture.root,
                "R1",
                fixture.patch_file("LEARNING-1", "RULE-TO-RETIRE"),
                "LEARNING-1",
            )
            ledger = load_learning_ledger(fixture.root)
            ledger["rule_evidence"]["RULE-TO-RETIRE"]["status"] = "RETIRED"
            ledger["attributed_rule_evidence"]["RULE-TO-RETIRE"][
                "status"
            ] = "RETIRED"
            write_learning_ledger(fixture.root, ledger)
            write_chat_input(fixture.root)
            path = fixture.prediction_file(
                "R2",
                4,
                applied_rule_ids=["RULE-TO-RETIRE"],
            )
            start_round(fixture.root, "R2")
            with self.assertRaises(TrainingError):
                freeze_prediction(fixture.root, "R2", path)

    def test_spaced_replay_records_targeted_repair_without_answer_mapping(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary), case_count=7)
            fixture.run_and_score("R1", 0)
            patch = fixture.base / "execution-gate.json"
            write_json(
                patch,
                learning_correction(
                    remediation_type="EXECUTION_GATE",
                    rules=[],
                ),
            )
            apply_learning(fixture.root, "R1", patch, "LEARNING-GATE")
            for index in range(2, 7):
                fixture.run_and_score(f"R{index}", 5)
            self.assertEqual(status(fixture.root)["active_replay_case_id"], "DEV-EXAMPLE-001")
            replay_score = fixture.run_and_score("R7", 5)
            report = json.loads(
                (
                    fixture.root
                    / replay_score["replay_remediation_report"]
                ).read_text()
            )
            self.assertEqual(report["original_failed_answers_repaired"], 5)
            self.assertEqual(report["original_correct_answers_regressed"], 0)
            self.assertFalse(report["counts_as_first_blind_evidence"])
            self.assertNotIn("correct_option", json.dumps(report))

    def test_invalid_issue_preflight_does_not_consume_active_case(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            prediction = json.loads(
                fixture.prediction_file("ISSUE-1", 4).read_text()
            )
            before = json.loads(
                (fixture.root / "training/state.json").read_text()
            )
            packet = {
                "schema": "TRAINING-ISSUE-PACKET-V3",
                "round_id": "ISSUE-1",
                "case_id": prediction["case_id"],
                "blind_chart_model": None,
                "cross_question_consistency": prediction[
                    "cross_question_consistency"
                ],
                "replay_remediation": None,
                "predictions": prediction["predictions"],
                "expected_result": "PASS",
            }
            with self.assertRaises(TrainingError):
                process_packet(fixture.root, packet, fixture.key)
            after = json.loads((fixture.root / "training/state.json").read_text())
            self.assertEqual(after, before)
            self.assertFalse((fixture.root / "training/runs/ISSUE-1").exists())

    def test_legacy_frozen_prediction_hash_remains_parseable(self):
        legacy = {
            "schema": "FROZEN-PREDICTION-V1",
            "predictions": [{"question_id": "Q1", "top1": "A"}],
        }
        self.assertEqual(
            frozen_content_hash(legacy),
            object_sha256(legacy["predictions"]),
        )


class IssueRelayTests(unittest.TestCase):
    def packet(self, fixture: RuntimeFixture, round_id: str, correct_count: int) -> dict:
        case_id, question_count = fixture.current_case()
        prediction = json.loads(fixture.prediction_file(round_id, correct_count).read_text())
        failed = correct_count < required_correct(question_count)
        packet = {
            "schema": "TRAINING-ISSUE-PACKET-V3",
            "round_id": round_id,
            "case_id": case_id,
            "blind_chart_model": prediction["blind_chart_model"],
            "cross_question_consistency": prediction[
                "cross_question_consistency"
            ],
            "replay_remediation": prediction["replay_remediation"],
            "predictions": prediction["predictions"],
            "expected_result": "FAIL" if failed else "PASS",
        }
        if failed:
            packet["learning_release_id"] = f"LEARNING-{round_id}"
            packet["learning_patch"] = learning_correction(
                rules=[general_rule(f"RULE-{round_id}")]
            )
        return packet

    def test_extract_and_process_passing_issue(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            packet = self.packet(fixture, "ISSUE-PASS-1", 4)
            body = f"header\n{PACKET_START}\n```json\n{json.dumps(packet)}\n```\n{PACKET_END}\n"
            result = process_packet(fixture.root, extract_packet(body), fixture.key)
            self.assertTrue(result["passed"])
            self.assertEqual(result["evaluation_kind"], "FIRST_BLIND")
            self.assertEqual(result["next_case_id"], "DEV-EXAMPLE-002")
            self.assertEqual(result["independent_pass_streak"], 1)
            self.assertFalse(result["answers_published"])

    def test_extract_accepts_raw_json_and_single_code_block(self):
        packet = {"schema": "TRAINING-ISSUE-PACKET-V3", "round_id": "RAW-1"}
        self.assertEqual(extract_packet(json.dumps(packet)), packet)
        self.assertEqual(extract_packet(f"```json\n{json.dumps(packet)}\n```"), packet)

    def test_failed_issue_creates_candidate_rules_and_queues_replay(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            packet = self.packet(fixture, "ISSUE-FAIL-1", 3)
            result = process_packet(fixture.root, packet, fixture.key)
            self.assertFalse(result["passed"])
            self.assertEqual(result["learning_release"], "LEARNING-ISSUE-FAIL-1")
            self.assertEqual(result["learning_rules_created"], ["RULE-ISSUE-FAIL-1"])
            self.assertEqual(result["next_case_id"], "DEV-EXAMPLE-002")
            self.assertEqual(result["independent_pass_streak"], 0)
            self.assertEqual(result["spaced_replay_queue_size"], 1)

    def test_expected_result_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            packet = self.packet(fixture, "ISSUE-MISMATCH-1", 4)
            packet["expected_result"] = "FAIL"
            packet["learning_release_id"] = "LEARNING-MISMATCH"
            packet["learning_patch"] = learning_correction(
                rules=[general_rule("RULE-MISMATCH")]
            )
            with self.assertRaises(TrainingError):
                process_packet(fixture.root, packet, fixture.key)


class HandoffProbeTests(unittest.TestCase):
    @staticmethod
    def handoff_for(
        fixture: RuntimeFixture,
        *,
        correct_count: int = 3,
        applied_rule_ids: list[str] | None = None,
    ) -> tuple[dict, dict]:
        bundle = json.loads((fixture.root / CHAT_INPUT_RELATIVE_PATH).read_text())
        contract = bundle["chat_work_handoff_contract"]
        prediction = json.loads(
            fixture.prediction_file(
                contract["binding"]["round_id"],
                correct_count,
                applied_rule_ids=applied_rule_ids,
            ).read_text()
        )
        return contract, {
            "schema": "CHAT-WORK-PREDICTION-HANDOFF-V2",
            "binding": contract["binding"],
            "prediction_access_execution_receipt": contract[
                "handoff_payload_template"
            ]["prediction_access_execution_receipt"],
            "blind_chart_model": prediction["blind_chart_model"],
            "cross_question_consistency": prediction[
                "cross_question_consistency"
            ],
            "replay_remediation": prediction["replay_remediation"],
            "predictions": prediction["predictions"],
        }

    def test_probe_returns_work_private_review_without_persisting_answers(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            contract, handoff = self.handoff_for(fixture)
            private_key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
            public_der = private_key.public_key().public_bytes(
                serialization.Encoding.DER,
                serialization.PublicFormat.SubjectPublicKeyInfo,
            )
            encoded_public_key = base64.b64encode(public_der).decode("ascii")
            summary, sealed = process_handoff_probe(
                fixture.root,
                issue_title=contract["issue_title"],
                issue_body=json.dumps(handoff),
                encoded_public_key=encoded_public_key,
                key=fixture.key,
            )
            private_review = unseal_private_review(sealed, private_key)
            self.assertFalse(summary["passed"])
            self.assertFalse(summary["repository_mutated"])
            self.assertEqual(
                private_review["detailed_review"]["questions"][3]["correct_option"],
                "A",
            )
            self.assertNotIn("correct_option", json.dumps(summary))
            self.assertNotIn("correct_option", json.dumps(sealed))
            self.assertFalse(summary["preflight"]["changed"])

    def test_handoff_fails_closed_without_exact_startup_access_receipt(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            contract, handoff = self.handoff_for(fixture)
            receipt = handoff.pop("prediction_access_execution_receipt")
            with self.assertRaisesRegex(TrainingError, "complete V2 reasoning workbook"):
                validate_handoff(
                    fixture.root,
                    issue_title=contract["issue_title"],
                    issue_body=json.dumps(handoff),
                )

            handoff["prediction_access_execution_receipt"] = {
                **receipt,
                "first_repository_read": "training/state.json",
            }
            with self.assertRaisesRegex(TrainingError, "contract-first"):
                validate_handoff(
                    fixture.root,
                    issue_title=contract["issue_title"],
                    issue_body=json.dumps(handoff),
                )

    def test_handoff_rejects_neutral_background_used_as_counterevidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            contract, handoff = self.handoff_for(fixture)
            evidence = handoff["predictions"][0]["evidence_ledger"][0]
            evidence["independence_status"] = "NEUTRAL_BACKGROUND"
            evidence["decision_impact"] = "COUNTEREVIDENCE"
            evidence["contradicts_option_atoms"] = []
            with self.assertRaisesRegex(
                TrainingError,
                "neutral background must have NEUTRAL decision_impact",
            ):
                validate_handoff(
                    fixture.root,
                    issue_title=contract["issue_title"],
                    issue_body=json.dumps(handoff),
                )

            evidence["decision_impact"] = "NEUTRAL"
            evidence["contradicts_option_atoms"] = ["C:C distinctive atom"]
            with self.assertRaisesRegex(
                TrainingError,
                "neutral background may not contradict option atoms",
            ):
                validate_handoff(
                    fixture.root,
                    issue_title=contract["issue_title"],
                    issue_body=json.dumps(handoff),
                )

    def test_handoff_rejects_neutral_background_in_counterevidence_indexes(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            contract, handoff = self.handoff_for(fixture)
            prediction = handoff["predictions"][0]
            evidence = prediction["evidence_ledger"][1]
            evidence["independence_status"] = "NEUTRAL_BACKGROUND"
            evidence["decision_impact"] = "NEUTRAL"
            evidence_id = evidence["evidence_id"]

            prediction["bazi_track_seal"]["contradicting_evidence_ids"] = [
                evidence_id
            ]
            with self.assertRaisesRegex(
                TrainingError,
                "contradicting evidence must be non-neutral",
            ):
                validate_handoff(
                    fixture.root,
                    issue_title=contract["issue_title"],
                    issue_body=json.dumps(handoff),
                )

            prediction["bazi_track_seal"]["contradicting_evidence_ids"] = []
            prediction["option_comparison_matrix"]["options"]["D"][
                "direct_counterevidence_ids"
            ] = [evidence_id]
            with self.assertRaisesRegex(
                TrainingError,
                "direct counterevidence must be non-neutral",
            ):
                validate_handoff(
                    fixture.root,
                    issue_title=contract["issue_title"],
                    issue_body=json.dumps(handoff),
                )

    def test_preflight_normalizes_fractional_confidence_before_validation(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            contract, handoff = self.handoff_for(fixture)
            for row in handoff["predictions"]:
                row["ziwei_track_seal"]["confidence"] = 0.7
                row["bazi_track_seal"]["confidence"] = 0.7
                for field in row["confidence_components"]:
                    row["confidence_components"][field] = 0.7
            normalized, report = validate_handoff(
                fixture.root,
                issue_title=contract["issue_title"],
                issue_body=json.dumps(handoff),
                include_preflight_report=True,
            )
            self.assertTrue(report["changed"])
            self.assertEqual(
                normalized["predictions"][0]["ziwei_track_seal"]["confidence"],
                70,
            )
            self.assertEqual(
                normalized["predictions"][0]["confidence_components"][
                    "overall_confidence"
                ],
                70,
            )
            self.assertEqual(
                {row["top1"] for row in normalized["predictions"]},
                {row["top1"] for row in handoff["predictions"]},
            )

    def test_preflight_normalizes_known_composite_replay_remediation_type(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            normalized, report = normalize_handoff(
                fixture.root,
                {
                    "replay_remediation": {
                        "remediation_type": (
                            "EXECUTION_GATE_AND_RULE_WEIGHT_CHANGE"
                        ),
                    },
                    "predictions": [],
                },
            )
            self.assertEqual(
                normalized["replay_remediation"]["remediation_type"],
                "EXECUTION_GATE",
            )
            self.assertEqual(
                report["changes"],
                [
                    {
                        "kind": "REPLAY_REMEDIATION_ALIAS_TO_PRIMARY",
                        "from": "EXECUTION_GATE_AND_RULE_WEIGHT_CHANGE",
                        "to": "EXECUTION_GATE",
                        "secondary_types": ["RULE_WEIGHT_CHANGE"],
                    }
                ],
            )

    def test_preflight_normalizes_ambiguous_independence_status_by_family(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            normalized, report = normalize_handoff(
                fixture.root,
                {
                    "predictions": [
                        {
                            "question_id": "Q1",
                            "evidence_ledger": [
                                {
                                    "evidence_id": "Q1-Z1",
                                    "evidence_family_id": "Q1-FAMILY-A",
                                    "independence_status": "INDEPENDENT_SAME_FAMILY",
                                },
                                {
                                    "evidence_id": "Q1-Z2",
                                    "evidence_family_id": "Q1-FAMILY-A",
                                    "independence_status": "INDEPENDENT_SAME_FAMILY",
                                },
                                {
                                    "evidence_id": "Q1-B1",
                                    "evidence_family_id": "Q1-FAMILY-B",
                                    "independence_status": "INDEPENDENT_SAME_FAMILY",
                                },
                                {
                                    "evidence_id": "Q1-R1",
                                    "evidence_family_id": "Q1-BACKGROUND",
                                    "independence_status": "NEUTRAL_BACKGROUND",
                                },
                            ],
                        }
                    ],
                },
            )
            self.assertEqual(
                [
                    row["independence_status"]
                    for row in normalized["predictions"][0]["evidence_ledger"]
                ],
                [
                    "INDEPENDENT",
                    "SAME_FAMILY",
                    "INDEPENDENT",
                    "NEUTRAL_BACKGROUND",
                ],
            )
            changes = [
                row
                for row in report["changes"]
                if row["kind"] == "EVIDENCE_INDEPENDENCE_STATUS_ALIAS"
            ]
            self.assertEqual([row["to"] for row in changes], [
                "INDEPENDENT",
                "SAME_FAMILY",
                "INDEPENDENT",
            ])

    def test_preflight_normalizes_known_profile_tag_aliases(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            normalized, report = normalize_handoff(
                fixture.root,
                {
                    "predictions": [
                        {
                            "question_id": "Q1",
                            "question_profile": {
                                "subject_tags": [
                                    "SELF",
                                    "HOUSEHOLD_UNIT",
                                    "FRIEND",
                                    "COWORKER",
                                ],
                                "time_scope_tags": [
                                    "LIFE_STAGE",
                                    "MULTI_YEAR_SEQUENCE",
                                ],
                                "endpoint_tags": [
                                    "HEALTH_CONDITION",
                                    "SURGERY",
                                ],
                                "applied_rule_ids": [],
                            },
                            "rule_attribution": {},
                        }
                    ]
                },
            )
            profile = normalized["predictions"][0]["question_profile"]
            self.assertEqual(
                profile["subject_tags"],
                [
                    "SELF",
                    "FAMILY",
                    "FRIEND_BUSINESS_PARTNER",
                    "EXTERNAL_ACTOR",
                ],
            )
            self.assertEqual(
                profile["time_scope_tags"],
                ["ADULTHOOD", "MULTI_YEAR_PERIOD"],
            )
            self.assertEqual(
                profile["endpoint_tags"],
                ["HEALTH_CONDITION"],
            )
            self.assertEqual(
                len(
                    [
                        change
                        for change in report["changes"]
                        if change["kind"] == "PROFILE_TAG_ALIAS"
                    ]
                ),
                6,
            )

    def test_preflight_declares_source_routes_used_by_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            normalized, report = normalize_handoff(
                fixture.root,
                {
                    "predictions": [
                        {
                            "question_id": "Q1",
                            "question_profile": {
                                "source_routes": ["S03"],
                                "applied_rule_ids": [],
                            },
                            "evidence_ledger": [
                                {
                                    "evidence_id": "Q1-ZW-01",
                                    "source_route": "S07",
                                },
                                {
                                    "evidence_id": "Q1-REAL-01",
                                    "source_route": "S17",
                                },
                                {
                                    "evidence_id": "Q1-ZW-02",
                                    "source_route": "S07",
                                },
                            ],
                            "rule_attribution": {},
                        }
                    ]
                },
            )
            self.assertEqual(
                normalized["predictions"][0]["question_profile"]["source_routes"],
                ["S03", "S07", "S17"],
            )
            self.assertIn(
                {
                    "kind": "EVIDENCE_SOURCE_ROUTES_DECLARED",
                    "question_id": "Q1",
                    "source_routes": ["S07", "S17"],
                },
                report["changes"],
            )

    def test_preflight_normalizes_source_route_range_to_primary_route(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            normalized, report = normalize_handoff(
                fixture.root,
                {
                    "predictions": [
                        {
                            "question_id": "Q1",
                            "question_profile": {
                                "source_routes": ["S08"],
                                "applied_rule_ids": [],
                            },
                            "evidence_ledger": [
                                {
                                    "evidence_id": "Q1-ZW-01",
                                    "source_route": "S04-S08",
                                }
                            ],
                            "rule_attribution": {},
                        }
                    ]
                },
            )
            prediction = normalized["predictions"][0]
            self.assertEqual(
                prediction["evidence_ledger"][0]["source_route"],
                "S04",
            )
            self.assertEqual(
                prediction["question_profile"]["source_routes"],
                ["S08", "S04"],
            )
            self.assertIn(
                {
                    "kind": "EVIDENCE_SOURCE_ROUTE_RANGE_TO_PRIMARY",
                    "question_id": "Q1",
                    "evidence_id": "Q1-ZW-01",
                    "from": "S04-S08",
                    "to": "S04",
                    "covered_source_routes": [
                        "S04",
                        "S05",
                        "S06",
                        "S07",
                        "S08",
                    ],
                },
                report["changes"],
            )

    def test_preflight_rejects_invalid_source_route_range_alias(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            with self.assertRaisesRegex(
                TrainingError,
                "invalid source_route range alias",
            ):
                normalize_handoff(
                    fixture.root,
                    {
                        "predictions": [
                            {
                                "question_id": "Q1",
                                "question_profile": {
                                    "source_routes": ["S04"],
                                    "applied_rule_ids": [],
                                },
                                "evidence_ledger": [
                                    {
                                        "evidence_id": "Q1-ZW-01",
                                        "source_route": "S08-S04",
                                    }
                                ],
                                "rule_attribution": {},
                            }
                        ]
                    },
                )

    def test_preflight_removes_cross_track_ids_from_independent_seals(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            normalized, report = normalize_handoff(
                fixture.root,
                {
                    "predictions": [
                        {
                            "question_id": "Q1",
                            "evidence_ledger": [
                                {"evidence_id": "Q1-ZW-01", "track": "ZIWEI"},
                                {"evidence_id": "Q1-BZ-01", "track": "BAZI"},
                                {"evidence_id": "Q1-REAL-01", "track": "REALITY"},
                            ],
                            "ziwei_track_seal": {
                                "supporting_evidence_ids": ["Q1-ZW-01"],
                                "contradicting_evidence_ids": ["Q1-REAL-01"],
                            },
                            "bazi_track_seal": {
                                "supporting_evidence_ids": ["Q1-BZ-01"],
                                "contradicting_evidence_ids": [
                                    "Q1-ZW-01",
                                    "Q1-REAL-01",
                                ],
                            },
                        }
                    ]
                },
            )
            prediction = normalized["predictions"][0]
            self.assertEqual(
                prediction["ziwei_track_seal"]["contradicting_evidence_ids"],
                [],
            )
            self.assertEqual(
                prediction["bazi_track_seal"]["contradicting_evidence_ids"],
                [],
            )
            changes = [
                change
                for change in report["changes"]
                if change["kind"] == "CROSS_TRACK_SEAL_EVIDENCE_REMOVED"
            ]
            self.assertEqual(len(changes), 2)
            self.assertEqual(
                changes[1]["evidence_ids"],
                ["Q1-ZW-01", "Q1-REAL-01"],
            )

    def test_preflight_declares_attributed_rule_as_applied(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            rule_id = "RULE-ATTRIBUTED-BUT-UNDECLARED"
            normalized, report = normalize_handoff(
                fixture.root,
                {
                    "predictions": [
                        {
                            "question_id": "Q1",
                            "question_profile": {
                                "applied_rule_ids": [],
                            },
                            "rule_attribution": {
                                "decisive_rule_ids": [],
                                "supporting_rule_ids": [],
                                "counterevidence_rule_ids": [rule_id],
                                "decision_changed": False,
                            },
                        }
                    ]
                },
            )
            profile = normalized["predictions"][0]["question_profile"]
            self.assertEqual(profile["applied_rule_ids"], [rule_id])
            self.assertIn(
                {
                    "kind": "ATTRIBUTED_RULES_DECLARED_AS_APPLIED",
                    "question_id": "Q1",
                    "rule_ids": [rule_id],
                },
                report["changes"],
            )

    def test_preflight_classifies_missing_applied_rule_as_supporting(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            rule_id = "RULE-MISSING-ATTRIBUTION"
            normalized, report = normalize_handoff(
                fixture.root,
                {
                    "predictions": [
                        {
                            "question_id": "Q1",
                            "question_profile": {
                                "applied_rule_ids": [rule_id],
                            },
                            "rule_attribution": {
                                "decisive_rule_ids": [],
                                "supporting_rule_ids": [],
                                "counterevidence_rule_ids": [],
                                "decision_changed": False,
                            },
                        }
                    ]
                },
            )
            attribution = normalized["predictions"][0]["rule_attribution"]
            self.assertEqual(attribution["supporting_rule_ids"], [rule_id])
            self.assertEqual(attribution["counterevidence_rule_ids"], [])
            self.assertIn(
                {
                    "kind": "MISSING_RULE_ATTRIBUTION_CLASSIFIED",
                    "question_id": "Q1",
                    "supporting_rule_ids": [rule_id],
                    "counterevidence_rule_ids": [],
                },
                report["changes"],
            )

    def test_preflight_derives_top1_precision_support_flag_from_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            normalized, report = normalize_handoff(
                fixture.root,
                {
                    "predictions": [
                        {
                            "question_id": "Q1",
                            "top1": "B",
                            "question_semantic_model": {
                                "option_atoms": {
                                    "B": {
                                        "severe_irreversible_or_high_precision_atoms": [
                                            "exact endpoint"
                                        ]
                                    }
                                }
                            },
                            "evidence_ledger": [
                                {
                                    "evidence_id": "Q1-Z1",
                                    "independence_status": "INDEPENDENT",
                                    "supports_option_atoms": ["B:exact endpoint"],
                                }
                            ],
                            "option_comparison_matrix": {
                                "options": {
                                    "B": {
                                        "severe_atoms_have_independent_evidence": False
                                    }
                                }
                            },
                        }
                    ]
                },
            )
            self.assertTrue(
                normalized["predictions"][0]["option_comparison_matrix"][
                    "options"
                ]["B"]["severe_atoms_have_independent_evidence"]
            )
            self.assertIn(
                {
                    "kind": "TOP1_PRECISION_SUPPORT_FLAG_DERIVED",
                    "question_id": "Q1",
                    "top1": "B",
                    "supporting_evidence_ids": ["Q1-Z1"],
                },
                report["changes"],
            )

    def test_preflight_recovers_explicit_natal_fact_from_mixed_year_row(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            normalized, report = normalize_handoff(
                fixture.root,
                {
                    "predictions": [
                        {
                            "question_id": "Q1",
                            "evidence_ledger": [
                                {
                                    "evidence_id": "Q1-Z1",
                                    "layer": "YEAR",
                                    "chart_fact": "流年触发本命夫妻宫原有结构",
                                    "decision_impact": "DECISIVE",
                                },
                                {
                                    "evidence_id": "Q1-B1",
                                    "layer": "YEAR",
                                    "chart_fact": "流年角色显化",
                                    "decision_impact": "SUPPORTING",
                                },
                            ],
                        }
                    ]
                },
            )
            self.assertEqual(
                normalized["predictions"][0]["evidence_ledger"][0]["layer"],
                "NATAL",
            )
            self.assertIn(
                {
                    "kind": "MIXED_STATIC_TIMING_EVIDENCE_LAYER_TO_NATAL",
                    "question_id": "Q1",
                    "evidence_id": "Q1-Z1",
                    "from": "YEAR",
                    "to": "NATAL",
                },
                report["changes"],
            )

    def test_preflight_recovers_ziwei_static_structure_from_mixed_period_row(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            normalized, report = normalize_handoff(
                fixture.root,
                {
                    "predictions": [
                        {
                            "question_id": "Q1",
                            "evidence_ledger": [
                                {
                                    "evidence_id": "Q1-Z1",
                                    "track": "ZIWEI",
                                    "layer": "PERIOD",
                                    "chart_fact": (
                                        "24-33夫妻大限，夫妻陀罗天刑年解"
                                    ),
                                    "decision_impact": "SUPPORTING",
                                }
                            ],
                        }
                    ]
                },
            )
            self.assertEqual(
                normalized["predictions"][0]["evidence_ledger"][0]["layer"],
                "NATAL",
            )
            self.assertIn(
                {
                    "kind": "MIXED_STATIC_TIMING_EVIDENCE_LAYER_TO_NATAL",
                    "question_id": "Q1",
                    "evidence_id": "Q1-Z1",
                    "from": "PERIOD",
                    "to": "NATAL",
                },
                report["changes"],
            )

    def test_preflight_reclassifies_option_matrix_support_by_evidence_track(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            normalized, report = normalize_handoff(
                fixture.root,
                {
                    "predictions": [
                        {
                            "question_id": "Q1",
                            "evidence_ledger": [
                                {"evidence_id": "Q1-ZW-01", "track": "ZIWEI"},
                                {"evidence_id": "Q1-BZ-01", "track": "BAZI"},
                                {"evidence_id": "Q1-REAL-01", "track": "REALITY"},
                            ],
                            "option_comparison_matrix": {
                                "options": {
                                    "A": {
                                        "ziwei_support_evidence_ids": [
                                            "Q1-BZ-01",
                                            "Q1-ZW-01",
                                            "Q1-REAL-01",
                                        ],
                                        "bazi_support_evidence_ids": [],
                                    }
                                }
                            },
                        }
                    ]
                },
            )
            option = normalized["predictions"][0][
                "option_comparison_matrix"
            ]["options"]["A"]
            self.assertEqual(
                option["ziwei_support_evidence_ids"],
                ["Q1-ZW-01"],
            )
            self.assertEqual(
                option["bazi_support_evidence_ids"],
                ["Q1-BZ-01"],
            )
            self.assertIn(
                {
                    "kind": "OPTION_MATRIX_SUPPORT_EVIDENCE_RECLASSIFIED",
                    "question_id": "Q1",
                    "option_id": "A",
                    "ziwei_support_evidence_ids": ["Q1-ZW-01"],
                    "bazi_support_evidence_ids": ["Q1-BZ-01"],
                    "removed_non_track_evidence_ids": ["Q1-REAL-01"],
                },
                report["changes"],
            )

    def test_preflight_normalizes_legacy_rule_ablation_shape(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            normalized, report = normalize_handoff(
                fixture.root,
                {
                    "predictions": [
                        {
                            "question_id": "Q1",
                            "counterfactual_analysis": {
                                "full_model_ranking": ["D", "B", "A", "C"],
                                "decisive_rule_ablations": [
                                    {
                                        "rule_id": "RULE-LEGACY-ABLATION",
                                        "ranking_without_rule": [
                                            "B",
                                            "D",
                                            "A",
                                            "C",
                                        ],
                                        "top1_changes": True,
                                    }
                                ],
                            },
                        }
                    ]
                },
            )
            ablation = normalized["predictions"][0][
                "counterfactual_analysis"
            ]["decisive_rule_ablations"][0]
            self.assertNotIn("top1_changes", ablation)
            self.assertTrue(ablation["changes_top1"])
            self.assertEqual(
                ablation["reason"],
                "Removing the declared decisive rule changes Top1 from D to B.",
            )
            self.assertIn(
                {
                    "kind": "RULE_ABLATION_FIELD_ALIAS",
                    "question_id": "Q1",
                    "rule_id": "RULE-LEGACY-ABLATION",
                    "from": "top1_changes",
                    "to": "changes_top1",
                },
                report["changes"],
            )
            self.assertIn(
                {
                    "kind": "RULE_ABLATION_REASON_DERIVED",
                    "question_id": "Q1",
                    "rule_id": "RULE-LEGACY-ABLATION",
                    "top1_before": "D",
                    "top1_after": "B",
                },
                report["changes"],
            )

    def test_preflight_moves_challenged_rule_to_counterevidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            fixture.run_and_score("R1", 0)
            rule_id = "RULE-CHALLENGED-PREFLIGHT"
            apply_learning(
                fixture.root,
                "R1",
                fixture.patch_file("LEARNING-1", rule_id),
                "LEARNING-1",
            )
            ledger = load_learning_ledger(fixture.root)
            ledger["rule_evidence"][rule_id]["status"] = "CHALLENGED"
            ledger["attributed_rule_evidence"][rule_id]["status"] = "CHALLENGED"
            write_learning_ledger(fixture.root, ledger)
            handoff = {
                "predictions": [
                    {
                        "question_id": "Q1",
                        "question_profile": {"applied_rule_ids": [rule_id]},
                        "rule_attribution": {
                            "decisive_rule_ids": [rule_id],
                            "supporting_rule_ids": [],
                            "counterevidence_rule_ids": [],
                            "decision_changed": True,
                        },
                        "counterfactual_analysis": {
                            "decisive_rule_ablations": [{"rule_id": rule_id}]
                        },
                    }
                ]
            }
            normalized, report = normalize_handoff(fixture.root, handoff)
            attribution = normalized["predictions"][0]["rule_attribution"]
            self.assertEqual(attribution["decisive_rule_ids"], [])
            self.assertEqual(
                attribution["counterevidence_rule_ids"],
                [rule_id],
            )
            self.assertFalse(attribution["decision_changed"])
            self.assertEqual(
                normalized["predictions"][0]["counterfactual_analysis"][
                    "decisive_rule_ablations"
                ],
                [],
            )
            self.assertTrue(report["changed"])

    def test_preflight_fails_closed_for_retired_rule(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            fixture.run_and_score("R1", 0)
            rule_id = "RULE-RETIRED-PREFLIGHT"
            apply_learning(
                fixture.root,
                "R1",
                fixture.patch_file("LEARNING-1", rule_id),
                "LEARNING-1",
            )
            ledger = load_learning_ledger(fixture.root)
            ledger["rule_evidence"][rule_id]["status"] = "RETIRED"
            ledger["attributed_rule_evidence"][rule_id]["status"] = "RETIRED"
            write_learning_ledger(fixture.root, ledger)
            handoff = {
                "predictions": [
                    {
                        "question_id": "Q1",
                        "question_profile": {"applied_rule_ids": [rule_id]},
                        "rule_attribution": {},
                    }
                ]
            }
            with self.assertRaises(TrainingError):
                normalize_handoff(fixture.root, handoff)


class RepositoryIntegrityTests(unittest.TestCase):
    def test_work_environment_bootstrap_is_versioned_and_executable(self):
        bootstrap = PROJECT_ROOT / "scripts/bootstrap-work-env.sh"
        self.assertTrue(bootstrap.is_file())
        self.assertTrue(bootstrap.stat().st_mode & 0o111)
        contents = bootstrap.read_text(encoding="utf-8")
        self.assertIn("git -C \"$repo_root\" sparse-checkout add", contents)
        self.assertIn("gh_version=\"2.96.0\"", contents)
        self.assertIn("sha256sum --check", contents)
        self.assertIn("tar --no-same-owner -xzf", contents)
        self.assertLess(
            contents.index('elif [[ -x "/tmp/fortune-gh/'),
            contents.index('if [[ "${1:-}" == "--check" ]]'),
        )

    def test_retired_rule_is_valid_but_not_exposed_to_prediction(self):
        ledger = load_learning_ledger(PROJECT_ROOT)
        retired_rule = "RULE-HEALTH-SEVERITY-ENDPOINT-COMPARISON"
        self.assertEqual(ledger["rule_evidence"][retired_rule]["status"], "RETIRED")
        state = json.loads(
            (PROJECT_ROOT / "training/state.json").read_text(encoding="utf-8")
        )
        release = json.loads(
            (
                PROJECT_ROOT
                / "model-learning/releases"
                / f"{state['current_model_release']}.json"
            ).read_text(encoding="utf-8")
        )
        validate_learning_ledger(PROJECT_ROOT, ledger, release)
        self.assertNotIn(
            retired_rule,
            {rule["rule_id"] for rule in safe_active_rules(PROJECT_ROOT, release)},
        )

    def test_training_relay_commits_learning_ledger(self):
        workflow = (
            PROJECT_ROOT / ".github/workflows/training-issue-relay.yml"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "git add training/state.json training/learning-ledger.json",
            workflow,
        )

    def test_handoff_gate_runs_preflight_on_github_and_fails_closed(self):
        workflow = (
            PROJECT_ROOT
            / ".github/workflows/prediction-handoff-gate.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("types: [opened, reopened]", workflow)
        self.assertIn("fortune-handoff-preflight", workflow)
        self.assertIn("Require the unique current-round handoff", workflow)
        self.assertIn("gh issue close", workflow)
        self.assertIn('--reason "not planned"', workflow)
        self.assertNotIn("fortune-train score", workflow)
        self.assertNotIn("fortune-train freeze", workflow)

    def test_real_repository_has_generalization_r2_training_baseline(self):
        result = verify_repository(PROJECT_ROOT)
        self.assertEqual(result["sources"], 20)
        self.assertEqual(result["cases"], 107)
        self.assertEqual(result["questions"], 511)
        self.assertEqual(result["case_bank"]["blocked_cases"], [])
        self.assertFalse(result["case_bank"]["answer_payload_present"])
        self.assertEqual(result["legacy_controller_group"]["cases"], 5)
        self.assertEqual(result["training_unit"], "FIRST_BLIND_CASE_WITH_SPACED_REPLAY")
        self.assertFalse(result["same_case_replays_count_toward_stage_gate"])
        self.assertEqual(result["required_consecutive_independent_passes"], 3)
        self.assertTrue(result["question_taxonomy_ready"])
        self.assertTrue(result["learning_ledger_ready"])
        bundle = json.loads((PROJECT_ROOT / CHAT_INPUT_RELATIVE_PATH).read_text())
        self.assertEqual(bundle["current_model"]["knowledge_cards"]["card_count"], 23)

    def test_real_chat_runtime_is_slim_without_reasoning_reduction(self):
        result = verify_repository(PROJECT_ROOT)
        runtime = result["chat_runtime"]
        self.assertLess(runtime["current_input_characters"], 80_000)
        self.assertLess(runtime["compiled_runtime_model_characters"], 80_000)
        self.assertTrue(runtime["all_prediction_themes_preserved"])
        self.assertEqual(runtime["reasoning_theme_count"], 14)
        self.assertIsNone(runtime["evidence_quota"])

        bundle = json.loads((PROJECT_ROOT / CHAT_INPUT_RELATIVE_PATH).read_text())
        self.assertNotIn(
            "prediction_row_template",
            bundle["chat_work_handoff_contract"],
        )
        performance = bundle["runtime_performance_contract"]
        self.assertGreaterEqual(
            performance["interruption_recovery"][
                "visible_checkpoint_interval_seconds"
            ],
            15,
        )
        self.assertLessEqual(
            performance["interruption_recovery"][
                "visible_checkpoint_interval_seconds"
            ],
            20,
        )
        self.assertTrue(
            performance["comparison_representation"]["all_pairs_required"]
        )
        self.assertFalse(
            performance["comparison_representation"][
                "may_omit_reasoning_step"
            ]
        )
        self.assertTrue(
            performance["shared_case_work"]["reuse_by_reference"]
        )
        self.assertEqual(
            performance["retrieval"]["mode"],
            "ANCHOR_FIRST_PROGRESSIVE_EXPANSION",
        )

        runtime_model = json.loads(
            (PROJECT_ROOT / CHAT_RUNTIME_MODEL_RELATIVE_PATH).read_text()
        )
        self.assertFalse(runtime_model["predictive_content_omitted"])
        self.assertEqual(
            runtime_model["release_id"],
            bundle["state_summary"]["current_model_release"],
        )
        self.assertTrue(runtime_model["active_rules"])
        self.assertTrue(runtime_model["active_process_corrections"])
        self.assertEqual(len(runtime_model["knowledge_cards"]), 23)
        self.assertNotIn("expected_effect", runtime_model["active_process_corrections"][-1])
        self.assertNotIn("reasoning", runtime_model["active_process_corrections"][-1])
        self.assertFalse(
            runtime_model["knowledge_workbench_chat_read_allowed"]
        )
        self.assertEqual(
            runtime_model["knowledge_card_runtime_authority"],
            "chat-input/runtime-model.json#knowledge_cards",
        )

        question_ids = {
            row["question_id"]
            for row in bundle["current_case"]["questions"]["parsed"]
        }
        execution_routes = bundle["current_model"]["question_execution_routes"]
        self.assertEqual(
            {row["question_id"] for row in execution_routes},
            question_ids,
        )
        self.assertTrue(
            all(row["knowledge_card_ids"] for row in execution_routes)
        )

    def test_model_runtime_rejects_project_source_dependency(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            policy = json.loads(
                (
                    PROJECT_ROOT / "config" / "model-runtime.json"
                ).read_text()
            )
            write_json(root / "config" / "model-runtime.json", policy)
            self.assertIsNotNone(_validate_model_runtime_policy(root))
            policy["chat_source_access"][
                "fail_closed_when_project_sources_unavailable"
            ] = True
            write_json(root / "config" / "model-runtime.json", policy)
            with self.assertRaisesRegex(TrainingError, "project-source"):
                _validate_model_runtime_policy(root)

    def test_canonical_sources_cannot_be_silently_rebaselined(self):
        parser = build_parser()
        subparsers = next(action for action in parser._actions if action.dest == "command")
        verify_parser = subparsers.choices["verify"]
        option_strings = {option for action in verify_parser._actions for option in action.option_strings}
        self.assertNotIn("--write-manifest", option_strings)

    def test_all_large_canonical_sources_have_lossless_fetchable_parent_segments(self):
        manifest = validate_canonical_runtime(PROJECT_ROOT)
        self.assertEqual(
            {source["source_id"] for source in manifest["sources"]},
            {f"S{index:02d}" for index in range(20)},
        )
        self.assertLess(
            (PROJECT_ROOT / RUNTIME_MANIFEST_PATH).stat().st_size,
            1024 * 1024,
        )
        self.assertTrue(
            any(source["canonical_bytes"] > 1024 * 1024 for source in manifest["sources"])
        )
        contract = json.loads(
            (PROJECT_ROOT / PREDICTION_ACCESS_CONTRACT_PATH).read_text()
        )
        state = json.loads((PROJECT_ROOT / "training/state.json").read_text())
        for source in manifest["sources"]:
            index_path = PROJECT_ROOT / source["runtime_index_path"]
            self.assertLess(index_path.stat().st_size, 1024 * 1024)
            source_index = json.loads(index_path.read_text())
            self.assertTrue(source_index["heading_routes"])
            segment_paths = {
                segment["path"] for segment in source_index["segments"]
            }
            self.assertTrue(segment_paths)
            self.assertTrue(
                all(
                    segment["bytes"] <= MAX_SEGMENT_BYTES
                    for segment in source_index["segments"]
                )
            )
            self.assertTrue(
                all(
                    set(route["segment_paths"]).issubset(segment_paths)
                    for route in source_index["heading_routes"]
                )
            )
            assert_prediction_access(
                PROJECT_ROOT,
                state,
                tool_class="GITHUB_FETCH_FILE",
                context_source="GITHUB_MAIN",
                repository="chinaneedM/ziwei-bazi-model",
                ref="main",
                path=source_index["segments"][0]["path"],
            )
        self.assertEqual(
            contract["canonical_runtime_access"]["runtime_segment_manifest_path"],
            RUNTIME_MANIFEST_PATH.as_posix(),
        )

    def test_canonical_source_mutation_fails_verification(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            source = fixture.root / "sources" / "canonical" / "S03_test.txt"
            source.write_text("tampered\n", encoding="utf-8")
            with self.assertRaises(TrainingError):
                verify_repository(fixture.root)

    def test_learning_ledger_tampering_fails_verification(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            ledger = load_learning_ledger(fixture.root)
            ledger["first_blind_totals"]["questions"] = -1
            write_json(fixture.root / LEDGER_RELATIVE_PATH, ledger)
            with self.assertRaises(TrainingError):
                verify_repository(fixture.root)

    def test_answer_source_readiness_is_explicit(self):
        result = verify_repository(PROJECT_ROOT)
        self.assertEqual(
            result["preloaded_encrypted_answers_ready"],
            result["answer_envelopes"] == result["answer_envelopes_required"],
        )
        self.assertTrue(result["external_post_freeze_answer_supported"])


class FormalActivationTests(unittest.TestCase):
    def test_five_option_cases_are_not_merged_and_unscored_rows_are_strict(self):
        five_option_questions = []
        for case_path in sorted((PROJECT_ROOT / "case-bank/cases").glob("CASE-*.json")):
            case = json.loads(case_path.read_text(encoding="utf-8"))
            for question in case["questions"]["parsed"]:
                option_ids = [row["option_id"] for row in question["options"]]
                self.assertIn(option_ids, [list("ABCD"), list("ABCDE")])
                if option_ids == list("ABCDE"):
                    five_option_questions.append(
                        (case["case_id"], question["question_id"])
                    )
        self.assertEqual(len(five_option_questions), 29)
        case = json.loads(
            (PROJECT_ROOT / "case-bank/cases/CASE-077.json").read_text(
                encoding="utf-8"
            )
        )
        payload = {
            "case_id": "CASE-077",
            "answers": [
                (
                    {
                        "question_id": question["question_id"],
                        "scoring_status": "UNSCORED",
                        "reason_code": "NO_VALID_OPTION",
                    }
                    if question["question_id"] == "Q3"
                    else {
                        "question_id": question["question_id"],
                        "correct_option": "A",
                    }
                )
                for question in case["questions"]["parsed"]
            ],
        }
        normalized = _validate_answers(case, payload)
        self.assertEqual(normalized["Q3"]["scoring_status"], "UNSCORED")
        self.assertEqual(
            sum(row["scoring_status"] == "SCORED" for row in normalized.values()),
            4,
        )

    def test_atomic_107_answer_import_activation_and_no_reveal_rehearsal(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "repo"
            shutil.copytree(
                PROJECT_ROOT,
                root,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
            )
            formal_vault = root / FORMAL_ANSWER_DIR
            if formal_vault.exists():
                shutil.rmtree(formal_vault)
            transport_dir = root / "answer-vault/import-transport"
            if transport_dir.exists():
                shutil.rmtree(transport_dir)
            archived_state = root / PRE_FORMAL_STATE_ARCHIVE
            if archived_state.is_file():
                archived_ledger = root / PRE_FORMAL_LEDGER_ARCHIVE
                if not archived_ledger.is_file():
                    self.fail("formal test fixture is missing the pre-formal ledger archive")
                shutil.copyfile(archived_state, root / "training/state.json")
                shutil.copyfile(
                    archived_ledger,
                    root / LEDGER_RELATIVE_PATH,
                )
                (root / FORMAL_GROUP_PATH).unlink(missing_ok=True)
                archived_state.unlink()
                archived_ledger.unlink()
                write_chat_input(root)

            manifest = json.loads((root / "case-bank/manifest.json").read_text())
            case_ids = [
                case_id
                for partition_id in ("DEVELOPMENT", "STAGE_VALIDATION", "FINAL_HOLDOUT")
                for case_id in manifest["partitions"][partition_id]
            ]
            rows = []
            for case_id in case_ids:
                case = json.loads(
                    (root / "case-bank/cases" / f"{case_id}.json").read_text()
                )
                rows.append(
                    {
                        "case_id": case_id,
                        "answers": [
                            (
                                {
                                    "question_id": question["question_id"],
                                    "scoring_status": "UNSCORED",
                                    "reason_code": "NO_VALID_OPTION",
                                }
                                if case_id == "CASE-077"
                                and question["question_id"] == "Q3"
                                else {
                                    "question_id": question["question_id"],
                                    "correct_option": "A",
                                }
                            )
                            for question in case["questions"]["parsed"]
                        ],
                    }
                )
            batch = {
                "schema": "FORTUNE-ANSWER-BATCH-V2",
                "corpus_id": manifest["corpus_id"],
                "cases": rows,
            }
            batch_path = base / "trusted-answers.json"
            write_json(batch_path, {**batch, "cases": rows[:-1]})
            key = Fernet.generate_key()
            with self.assertRaises(TrainingError):
                import_answer_batch(root, batch_path, key)
            self.assertFalse(formal_vault.exists())

            write_json(batch_path, batch)
            transport = bootstrap_answer_transport(root, key)
            self.assertTrue(transport["private_key_encrypted"])
            sealed_output = base / "answer-batch.sealed.json"
            seal_answer_batch(
                root,
                root / PUBLIC_KEY_PATH,
                batch_path,
                sealed_output,
            )
            shutil.copyfile(sealed_output, root / SEALED_BATCH_PATH)
            finalized = finalize_answer_transport(root, key)
            self.assertEqual(finalized["answer_envelopes"], 107)
            self.assertEqual(finalized["scoreable_questions"], 510)
            self.assertEqual(finalized["unscored_questions"], 1)
            self.assertEqual(finalized["current_case_id"], "CASE-002")
            self.assertEqual(finalized["recommended_round_id"], "FORMAL-ROUND-001")
            self.assertEqual(finalized["no_reveal_rehearsal"], "NO_REVEAL_REHEARSAL_PASS")
            self.assertTrue(finalized["transport_material_removed"])
            result = verify_repository(root, require_answers=True)
            self.assertEqual(result["answer_envelopes"], 107)
            self.assertEqual(result["active_controller_group"]["cases"], 61)
            self.assertEqual(result["active_controller_group"]["mode"], "FORMAL_CASE_BANK")


class PredictionContaminationQuarantineTests(unittest.TestCase):
    def _copy_runtime_files(self, root: Path) -> None:
        for relative in (
            "case-bank/partitions/development.json",
            "training/formal-development-group.json",
            "training/state.json",
            "chat-input/current.json",
        ):
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(PROJECT_ROOT / relative, destination)

    def test_quarantine_is_non_scoring_and_advances_to_next_clean_case(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._copy_runtime_files(root)
            old_state = json.loads((root / "training/state.json").read_text())
            old_group = json.loads(
                (root / "training/formal-development-group.json").read_text()
            )
            current_index = old_state["current_case_index"]
            current_case_id = old_group["case_order"][current_index]
            next_case_id = old_group["case_order"][current_index + 1]
            round_id = f"FORMAL-ROUND-{old_state['round_sequence'] + 1:03d}"

            with (
                patch("fortune_training.formal.write_chat_input"),
                patch(
                    "fortune_training.formal.verify_repository",
                    return_value={"status": "VERIFIED"},
                ),
            ):
                result = quarantine_current_case(
                    root, round_id, current_case_id
                )

            partition = json.loads(
                (root / "case-bank/partitions/development.json").read_text()
            )
            group = json.loads(
                (root / "training/formal-development-group.json").read_text()
            )
            state = json.loads((root / "training/state.json").read_text())
            self.assertNotIn(current_case_id, partition["first_blind_schedule"])
            self.assertIn(
                current_case_id,
                partition["contaminated_development_reference_case_ids"],
            )
            self.assertEqual(group["case_order"][current_index], next_case_id)
            self.assertNotIn(current_case_id, state["cases"])
            self.assertEqual(state["cases"][next_case_id]["status"], "ACTIVE")
            self.assertEqual(state["current_case_index"], current_index)
            self.assertEqual(
                state["first_blind_cases_closed"],
                old_state["first_blind_cases_closed"],
            )
            self.assertEqual(state["round_count"], old_state["round_count"])
            self.assertEqual(state["round_sequence"], old_state["round_sequence"] + 1)
            self.assertEqual(result["next_case_id"], next_case_id)
            self.assertEqual(
                result["next_round_id"],
                f"FORMAL-ROUND-{old_state['round_sequence'] + 2:03d}",
            )
            self.assertFalse(result["prediction_frozen"])
            self.assertFalse(result["scored"])
            self.assertFalse(result["answers_accessed"])

    def test_startup_order_violation_preserves_same_case_for_clean_round(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._copy_runtime_files(root)
            state_path = root / "training/state.json"
            old_state = json.loads(state_path.read_text())
            group = json.loads(
                (root / "training/formal-development-group.json").read_text()
            )
            current_case_id = group["case_order"][old_state["current_case_index"]]
            round_id = f"FORMAL-ROUND-{old_state['round_sequence'] + 1:03d}"

            with (
                patch("fortune_training.formal.write_chat_input"),
                patch(
                    "fortune_training.formal.verify_repository",
                    return_value={"status": "VERIFIED"},
                ),
            ):
                result = invalidate_current_pre_freeze_round(
                    root,
                    round_id,
                    current_case_id,
                )

            state = json.loads(state_path.read_text())
            self.assertEqual(
                state["cases"][current_case_id],
                old_state["cases"][current_case_id],
            )
            self.assertEqual(
                state["first_blind_cases_closed"],
                old_state["first_blind_cases_closed"],
            )
            self.assertEqual(state["round_count"], old_state["round_count"])
            self.assertEqual(
                state["round_sequence"],
                old_state["round_sequence"] + 1,
            )
            self.assertEqual(
                state["non_executed_rounds"][-1]["reason"],
                "PREDICTION_ACCESS_CONTRACT_NOT_EXECUTED_BEFORE_REPOSITORY_READ",
            )
            self.assertEqual(result["next_case_id"], current_case_id)
            self.assertEqual(
                result["next_round_id"],
                f"FORMAL-ROUND-{old_state['round_sequence'] + 2:03d}",
            )
            self.assertTrue(result["case_first_blind_eligibility_preserved"])
            self.assertFalse(result["prediction_frozen"])
            self.assertFalse(result["scored"])
            self.assertFalse(result["answers_accessed"])

    def test_runtime_gate_failure_preserves_same_case_for_clean_round(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._copy_runtime_files(root)
            state_path = root / "training/state.json"
            old_state = json.loads(state_path.read_text())
            group = json.loads(
                (root / "training/formal-development-group.json").read_text()
            )
            current_case_id = group["case_order"][old_state["current_case_index"]]
            round_id = f"FORMAL-ROUND-{old_state['round_sequence'] + 1:03d}"

            with (
                patch("fortune_training.formal.write_chat_input"),
                patch(
                    "fortune_training.formal.verify_repository",
                    return_value={"status": "VERIFIED"},
                ),
            ):
                result = invalidate_current_pre_freeze_round(
                    root,
                    round_id,
                    current_case_id,
                    reason=PREDICTION_CANONICAL_RUNTIME_READ_GATE_FAILURE,
                )

            state = json.loads(state_path.read_text())
            record = state["non_executed_rounds"][-1]
            self.assertEqual(
                record["status"],
                PRE_FREEZE_RUNTIME_GATE_FAILED_NOT_EXECUTED,
            )
            self.assertEqual(
                record["reason"],
                PREDICTION_CANONICAL_RUNTIME_READ_GATE_FAILURE,
            )
            self.assertEqual(
                state["cases"][current_case_id],
                old_state["cases"][current_case_id],
            )
            self.assertEqual(result["next_case_id"], current_case_id)
            self.assertTrue(result["case_first_blind_eligibility_preserved"])
            self.assertFalse(result["prediction_frozen"])
            self.assertFalse(result["scored"])
            self.assertFalse(result["answers_accessed"])

    def test_quarantine_rolls_back_every_file_when_verification_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._copy_runtime_files(root)
            paths = (
                root / "case-bank/partitions/development.json",
                root / "training/formal-development-group.json",
                root / "training/state.json",
                root / "chat-input/current.json",
            )
            before = [json.loads(path.read_text()) for path in paths]
            state = before[2]
            group = before[1]
            current_case_id = group["case_order"][state["current_case_index"]]
            round_id = f"FORMAL-ROUND-{state['round_sequence'] + 1:03d}"
            with (
                patch("fortune_training.formal.write_chat_input"),
                patch(
                    "fortune_training.formal.verify_repository",
                    side_effect=TrainingError("verification failed"),
                ),
                self.assertRaises(TrainingError),
            ):
                quarantine_current_case(root, round_id, current_case_id)
            after = [json.loads(path.read_text()) for path in paths]
            self.assertEqual(after, before)

    def test_contamination_report_rejects_prediction_or_answer_fields(self):
        valid = {
            "schema": "PREDICTION-CONTAMINATION-REPORT-V1",
            "round_id": "FORMAL-ROUND-022",
            "case_id": "CASE-102",
            "reason": "PREDICTION_CONTEXT_ALLOWLIST_VIOLATION",
        }
        self.assertEqual(validate_contamination_report(valid), valid)
        with self.assertRaises(TrainingError):
            validate_contamination_report({**valid, "correct_option": "A"})

    def test_cli_exposes_strongly_bound_quarantine_command(self):
        args = build_parser().parse_args(
            ["quarantine-current", "FORMAL-ROUND-022", "CASE-102"]
        )
        self.assertEqual(args.round_id, "FORMAL-ROUND-022")
        self.assertEqual(args.case_id, "CASE-102")
        invalidate_args = build_parser().parse_args(
            ["invalidate-current-round", "FORMAL-ROUND-025", "CASE-006"]
        )
        self.assertEqual(invalidate_args.round_id, "FORMAL-ROUND-025")
        self.assertEqual(invalidate_args.case_id, "CASE-006")


if __name__ == "__main__":
    unittest.main()
