from __future__ import annotations

import json
import base64
import shutil
import tempfile
import unittest
from pathlib import Path

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from fortune_training.chat_input import CHAT_INPUT_RELATIVE_PATH, write_chat_input
from fortune_training.cli import build_parser
from fortune_training.formal import (
    FORMAL_ANSWER_DIR,
    FORMAL_GROUP_PATH,
    PRE_FORMAL_LEDGER_ARCHIVE,
    PRE_FORMAL_STATE_ARCHIVE,
    import_answer_batch,
)
from fortune_training.issue_relay import PACKET_END, PACKET_START, extract_packet, process_packet
from fortune_training.handoff_probe import (
    process_handoff_probe,
    unseal_private_review,
)
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
from fortune_training.verify import build_source_manifest, verify_repository


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TAXONOMY = json.loads((PROJECT_ROOT / "config" / "question-taxonomy.json").read_text())
POLICY = json.loads((PROJECT_ROOT / "config" / "training-policy.json").read_text())


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
        write_json(self.root / "config" / "question-taxonomy.json", TAXONOMY)
        source_manifest = build_source_manifest(self.root)
        write_json(
            self.root / "config" / "source-policy.json",
            {
                "schema": "SOURCE-AUTHORITY-POLICY-V1",
                "original_project_library_role": "ARCHIVAL_READ_ONLY_NOT_RUNTIME",
                "original_project_library_deletion_required": False,
                "runtime_source": "GIT_REPOSITORY_ONLY",
                "git_canonical_path": "sources/canonical",
                "git_canonical_mutable_during_training": False,
                "canonical_manifest_sha256": object_sha256(source_manifest),
                "model_learning_path": "model-learning",
                "model_learning_mutable_during_training": True,
                "conflict_resolution": "IGNORE_EXTERNAL_ORIGINAL_AND_USE_GIT_RUNTIME",
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
        write_json(self.root / "sources" / "canonical-manifest.json", source_manifest)
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
            self.assertNotIn('"top1_correct"', serialized)
            self.assertNotIn('"correct_option"', serialized)

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
        self.assert_freeze_rejected(
            lambda payload: payload["predictions"][0][
                "question_semantic_model"
            ]["option_atoms"]["D"].update(
                {
                    "severe_irreversible_or_high_precision_atoms": [
                        "exact irreversible endpoint"
                    ]
                }
            )
        )

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
                bundle["current_model"]["active_process_corrections"][-1][
                    "remediation_type"
                ],
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
    def test_probe_returns_work_private_review_without_persisting_answers(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RuntimeFixture(Path(temporary))
            bundle = json.loads((fixture.root / CHAT_INPUT_RELATIVE_PATH).read_text())
            contract = bundle["chat_work_handoff_contract"]
            prediction = json.loads(
                fixture.prediction_file(contract["binding"]["round_id"], 3).read_text()
            )
            handoff = {
                "schema": "CHAT-WORK-PREDICTION-HANDOFF-V2",
                "binding": contract["binding"],
                "blind_chart_model": prediction["blind_chart_model"],
                "cross_question_consistency": prediction[
                    "cross_question_consistency"
                ],
                "replay_remediation": prediction["replay_remediation"],
                "predictions": prediction["predictions"],
            }
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


class RepositoryIntegrityTests(unittest.TestCase):
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

    def test_canonical_sources_cannot_be_silently_rebaselined(self):
        parser = build_parser()
        subparsers = next(action for action in parser._actions if action.dest == "command")
        verify_parser = subparsers.choices["verify"]
        option_strings = {option for action in verify_parser._actions for option in action.option_strings}
        self.assertNotIn("--write-manifest", option_strings)

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
            self.assertEqual(result["active_controller_group"]["cases"], 63)
            self.assertEqual(result["active_controller_group"]["mode"], "FORMAL_CASE_BANK")


if __name__ == "__main__":
    unittest.main()
