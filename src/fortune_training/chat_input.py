from __future__ import annotations

from pathlib import Path
from typing import Any

from .learning import (
    build_rule_router,
    load_runtime_governance,
    load_taxonomy,
    safe_active_rules,
)
from .policy import (
    MAX_APPLIED_RULES_PER_QUESTION,
    MINIMUM_NEW_CASES_BETWEEN_REPLAYS,
    REQUIRED_CONSECUTIVE_INDEPENDENT_PASSES,
)
from .prediction_access import (
    PREDICTION_ACCESS_CONTRACT_PATH,
    build_prediction_access_contract,
    build_prediction_access_execution_receipt,
    load_post_prediction_handoff_policy,
)
from .util import (
    atomic_write_compact_json,
    atomic_write_json,
    load_json,
    next_round_id,
    object_sha256,
    sha256_file,
)


CHAT_INPUT_RELATIVE_PATH = Path("chat-input/current.json")
PREDICTION_ROW_TEMPLATE_RELATIVE_PATH = Path(
    "chat-input/prediction-row-template.json"
)
CHAT_RUNTIME_MODEL_RELATIVE_PATH = Path("chat-input/runtime-model.json")
CHAT_RUNTIME_POLICY_RELATIVE_PATH = Path("config/chat-runtime-performance.json")
CHAT_INPUT_RAW_URL = (
    "https://raw.githubusercontent.com/chinaneedM/ziwei-bazi-model/"
    "main/chat-input/current.json"
)
GITHUB_ISSUE_BODY_MAX_CHARACTERS = 65_536
HANDOFF_TARGET_MAX_CHARACTERS = 60_000
HANDOFF_PREFERRED_MAX_CHARACTERS = 40_000
OPENABLE_STATES = {"READY_FOR_ROUND"}
CASE_VISIBLE_STATES = {
    "READY_FOR_ROUND",
    "AWAITING_PREDICTION_FREEZE",
    "PREDICTION_FROZEN",
    "LEARNING_REQUIRED",
}


def _blind_chart_model_template() -> dict[str, Any]:
    text = "<REQUIRED_NON_EMPTY_STRING>"
    return {
        "schema": "BLIND-CHART-MODEL-V2",
        "input_reliability": {
            "gender": text,
            "calendar": text,
            "birth_time": text,
            "birth_place": text,
            "four_pillars": text,
            "ziwei_coordinates": text,
            "major_periods": text,
            "missing_fields": [],
            "conflicting_fields": [],
            "unreliable_fields": [],
            "forbidden_inferences": [],
        },
        "ziwei_static_model": {
            "chart_facts": [text],
            "palace_and_star_structures": [text],
            "transformations_and_lines": [text],
            "advanced_method_applicability": [text],
            "structural_conflicts": [],
            "limitations": [text],
        },
        "bazi_static_model": {
            "immutable_atomic_fact_ledger": {
                "schema": "BAZI-ATOMIC-FACT-LEDGER-V1",
                "convention": "ZIPING_ATOMIC_RELATIONS_V1",
                "scope": "NATAL_ONLY",
                "four_pillars": {
                    "YEAR": "<STEM_BRANCH>",
                    "MONTH": "<STEM_BRANCH>",
                    "DAY": "<STEM_BRANCH>",
                    "HOUR": "<STEM_BRANCH>",
                },
                "day_master": "<HEAVENLY_STEM>",
                "hidden_stems": {"<PILLAR_POSITION>": ["<HIDDEN_STEM>"]},
                "five_elements": {"<FACT_ID>": "<ELEMENT>"},
                "element_roles": {"<FACT_ID>": "<ELEMENT_ROLE>"},
                "ten_gods": {"<STEM_FACT_ID>": "<TEN_GOD>"},
                "visible_stem_roots": {"<STEM_FACT_ID>": ["<ROOT_FACT_ID>"]},
                "heavenly_stem_combinations": [],
                "earthly_branch_relations": [],
                "verification_status": "MECHANICALLY_DERIVED",
            },
            "strength_structure_favorability_chain": {
                "schema": "BAZI-STRENGTH-STRUCTURE-FAVORABILITY-CHAIN-V1",
                "ledger_sha256": "<OBJECT_SHA256_OF_IMMUTABLE_ATOMIC_FACT_LEDGER>",
                "seasonal_command_fact_id": "MONTH_BRANCH",
                "root_fact_ids": [],
                "supporting_fact_ids": ["<ALL_PEER_AND_RESOURCE_FACT_IDS>"],
                "draining_fact_ids": ["<ALL_OUTPUT_AND_WEALTH_FACT_IDS>"],
                "controlling_fact_ids": ["<ALL_OFFICER_FACT_IDS>"],
                "relation_fact_ids": [],
                "strength_candidates": [text],
                "selected_strength_candidate": text,
                "pattern_candidates": [text],
                "selected_pattern_candidate": text,
                "favorability_candidates": [text],
                "selected_favorability_candidate": text,
                "method_competition": [text],
                "unresolved_conflicts": [],
                "reasoning_summary": text,
                "option_blind_frozen": True,
            },
            "chart_facts": [text],
            "seasonal_strength_candidates": [text],
            "pattern_candidates": [text],
            "method_competition": [text],
            "relations_and_structural_changes": [text],
            "useful_harmful_candidates": [text],
            "unresolved_disputes": [],
            "limitations": [text],
        },
        "shared_life_structure": {
            "personality_and_behavior": [text],
            "family_roles": [text],
            "marriage_capacity": [text],
            "children_axis": [text],
            "career_and_wealth": [text],
            "health_capacity": [text],
            "migration_assets_social": [text],
            "period_themes": [text],
            "major_conflicts": [],
            "unknowns": [],
        },
    }


def _cross_question_consistency_template() -> dict[str, Any]:
    return {
        "checks": [
            {
                "question_id": "<QUESTION_ID>",
                "consistent": True,
                "conflicts": [],
                "resolution": "<REQUIRED_NON_EMPTY_STRING>",
            }
        ],
        "unresolved_conflicts": [],
    }


def _replay_remediation_template() -> dict[str, Any]:
    return {
        "original_root_causes": ["<ROOT_CAUSE>"],
        "remediation_type": "<REMEDIATION_TYPE>",
        "new_idea_executed": "<REQUIRED_NON_EMPTY_STRING>",
        "changed_steps": ["<REQUIRED_NON_EMPTY_STRING>"],
        "predicted_mechanism_of_improvement": "<REQUIRED_NON_EMPTY_STRING>",
        "new_error_risks": [],
    }


def _prediction_row_template() -> dict[str, Any]:
    text = "<REQUIRED_NON_EMPTY_STRING>"
    option_id = "<OPTION_ID>"
    evidence_id = "<EVIDENCE_ID>"
    supporting_evidence_id = (
        "<SUPPORTING_EVIDENCE_ID_EXCLUSIVE_FROM_CONTRADICTING_SET>"
    )
    confidence = "<INTEGER_PERCENT_0_TO_100>"
    overall_confidence = (
        "<INTEGER_PERCENT_0_TO_WEAKEST_NON_OVERALL_COMPONENT>"
    )
    ranking = ["<ALL_OPTION_IDS_IN_FINAL_ORDER>"]
    return {
        "question_id": "<QUESTION_ID>",
        "top1": "<OPTION_ID>",
        "top2": "<OPTION_ID>",
        "public_summary": text,
        "question_profile": {
            "topic_tags": ["<TAXONOMY_VALUE>"],
            "subject_tags": ["<TAXONOMY_VALUE>"],
            "time_scope_tags": ["<TAXONOMY_VALUE>"],
            "endpoint_tags": ["<TAXONOMY_VALUE>"],
            "reasoning_skill_tags": ["<TAXONOMY_VALUE>"],
            "source_routes": ["<S00_TO_S19>"],
            "applied_rule_ids": [],
        },
        "rule_attribution": {
            "decisive_rule_ids": [],
            "supporting_rule_ids": [],
            "counterevidence_rule_ids": [],
            "decision_changed": False,
        },
        "question_semantic_model": {
            "target": text,
            "subject": text,
            "time_range": text,
            "action_subject": text,
            "reality_object": text,
            "event_process": text,
            "completion_endpoint": text,
            "magnitude": text,
            "is_composite_narrative": False,
            "option_atoms": {
                option_id: {
                    "required_atoms": [text],
                    "distinctive_atoms": [text],
                    "severe_irreversible_or_high_precision_atoms": [],
                }
            },
            "shared_non_discriminating_atoms": [],
            "ambiguities": [],
        },
        "ziwei_track_seal": {
            "top1": "<OPTION_ID>",
            "top2": "<OPTION_ID>",
            "ranking": ranking,
            "core_structure": text,
            "dynamic_trigger": text,
            "endpoint_chain": {
                "subject": text,
                "action": text,
                "object": text,
                "endpoint": text,
            },
            "supporting_evidence_ids": [supporting_evidence_id],
            "contradicting_evidence_ids": [],
            "alternative_explanations": [text],
            "unresolved_links": [],
            "capability_ceiling": text,
            "confidence": confidence,
        },
        "bazi_track_seal": {
            "top1": "<OPTION_ID>",
            "top2": "<OPTION_ID>",
            "ranking": ranking,
            "strength_and_pattern": text,
            "method_competition": text,
            "luck_timing": text,
            "dynamic_relation_scope": {
                "query_scope_id": "<QUESTION_BOUND_SCOPE_ID>",
                "active_dynamic_object_ids": [],
                "historical_anchor_ids": [],
                "cross_time_reactivation": {
                    "status": "NOT_USED",
                    "method": "NOT_APPLICABLE",
                    "source_route": "NOT_APPLICABLE",
                    "bounded_object_ids": [],
                },
            },
            "endpoint_chain": {
                "subject": text,
                "action": text,
                "object": text,
                "endpoint": text,
            },
            "supporting_evidence_ids": [supporting_evidence_id],
            "contradicting_evidence_ids": [],
            "alternative_explanations": [text],
            "unresolved_links": [],
            "capability_ceiling": text,
            "confidence": confidence,
        },
        "cross_track_arbitration": {
            "agreement_layers": [],
            "conflict_layers": [],
            "conflict_origin": text,
            "shared_reality_assumption_risk": text,
            "stronger_track_for_topic": "UNRESOLVED",
            "decision": text,
            "confidence_reduction_required": True,
        },
        "evidence_ledger": [
            {
                "evidence_id": evidence_id,
                "track": "<ZIWEI_OR_BAZI_OR_REALITY>",
                "layer": "<NATAL_PERIOD_YEAR_MONTH_OR_REALITY>",
                "chart_fact": text,
                "source_route": "<DECLARED_S00_TO_S19>",
                "knowledge_point": text,
                "applicability_conditions": [text],
                "conditions_satisfied": [text],
                "supports_option_atoms": [f"{option_id}:<EXACT_ATOM_TEXT>"],
                "contradicts_option_atoms": [],
                "alternative_explanation": text,
                "evidence_family_id": "<EVIDENCE_FAMILY_ID>",
                "independence_status": "<INDEPENDENT|SAME_FAMILY|NEUTRAL_BACKGROUND>",
                "reliability": "<HIGH_MEDIUM_LOW_OR_UNKNOWN>",
                "capability_ceiling": text,
                "decision_impact": "<DECISIVE_SUPPORTING_COUNTEREVIDENCE_OR_NEUTRAL>",
                "limitations": text,
                "axis_distance": "<DIRECT_SAME_AXIS_ONE_HOP_OR_MULTI_HOP>",
                "transmission_path": [],
                "temporal_role": "<NATAL_STATIC_PERIOD_CONTEXT_ACTIVE_QUERY_OBJECT_HISTORICAL_VALIDATION_ANCHOR_OR_REALITY_ENDPOINT>",
                "scope_id": "<DECLARED_TEMPORAL_SCOPE_ID>",
            }
        ],
        "final_ranking": ranking,
        "option_comparison_matrix": {
            "options": {
                option_id: {
                    "required_atom_completion": [],
                    "distinctive_atom_completion": [],
                    "severe_atoms_have_independent_evidence": False,
                    "ziwei_support_evidence_ids": [],
                    "bazi_support_evidence_ids": [],
                    "reality_closure": text,
                    "timing_closure": text,
                    "direct_counterevidence_ids": [],
                    "unknown_atoms": [],
                    "shared_background_zeroed": True,
                    "final_rank": 1,
                    "final_rank_reason": text,
                }
            },
            "pairwise": [
                {
                    "left": "<OPTION_ID>",
                    "right": "<OPTION_ID>",
                    "winner": "<OPTION_ID>",
                    "reason": text,
                }
            ],
        },
        "adversarial_review": {
            "top1_weakest_required_atom": text,
            "strongest_competitor": "<TOP2_OPTION_ID>",
            "strongest_reversal_evidence_ids": [evidence_id],
            "ignored_alternative_explanations": [text],
            "option_wording_inducement": text,
            "annual_signal_overweighting": text,
            "bazi_posthoc_agreement": text,
            "duplicate_evidence_stacking": text,
            "background_as_endpoint": text,
            "participation_as_action": text,
            "valence_as_mechanism": text,
            "known_rule_execution_omissions": text,
            "precision_beyond_capability": text,
            "reversal_test": {
                "removed_evidence_ids": [evidence_id],
                "ranking_before": ranking,
                "ranking_after_removal": ranking,
                "top2_best_explanation": text,
                "top1_survives": (
                    "<BOOLEAN_DERIVED_FROM_RANKING_BEFORE_AND_AFTER_REMOVAL>"
                ),
                "reason": text,
            },
        },
        "confidence_components": {
            "input_confidence": confidence,
            "natal_structure_confidence": confidence,
            "subject_confidence": confidence,
            "mechanism_confidence": confidence,
            "timing_confidence": confidence,
            "reality_endpoint_confidence": confidence,
            "cross_track_agreement": confidence,
            "top1_top2_separation": confidence,
            "overall_confidence": overall_confidence,
        },
        "counterfactual_analysis": {
            "full_model_ranking": ranking,
            "canonical_only_ranking": ranking,
            "ziwei_only_ranking": ranking,
            "bazi_only_ranking": ranking,
            "fused_ranking": ranking,
            "decisive_rule_ablations": [
                {
                    "rule_id": "<ONE_ROW_FOR_EACH_DECISIVE_RULE_ID>",
                    "ranking_without_rule": [
                        "<ALL_OPTION_IDS_IN_FINAL_ORDER_WITHOUT_THIS_RULE>"
                    ],
                    "changes_top1": (
                        "<BOOLEAN_DERIVED_FROM_RANKING_WITHOUT_RULE>"
                    ),
                    "reason": text,
                }
            ],
        },
    }


def _compact_rule(rule: dict[str, Any]) -> dict[str, Any]:
    """Keep every runtime decision field while excluding learning-history metadata."""
    fields = (
        "rule_id",
        "validation_status",
        "runtime_role",
        "statement",
        "applicability",
        "trigger_conditions",
        "decision_procedure",
        "limits",
        "stop_conditions",
        "capability_ceiling",
        "counterexamples",
        "source_basis",
    )
    return {field: rule[field] for field in fields}


def _compact_process_correction(
    correction: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    content = correction["correction"]
    return {
        "correction_id": f"ACTIVE-PROCESS-{index:03d}",
        "remediation_type": correction["remediation_type"],
        "statement": content["statement"],
        "applicability": content["applicability"],
        "limitations": content["limitations"],
        "capability_ceiling": content["capability_ceiling"],
    }


def compact_reasoning_core(reasoning_core: dict[str, Any] | None) -> dict[str, Any] | None:
    if reasoning_core is None:
        return None
    prediction_fields = (
        "schema",
        "method_id",
        "purpose",
        "stages",
        "method_gates",
        "evidence_priority",
        "non_accumulation_rules",
        "uncertainty_rules",
    )
    return {field: reasoning_core[field] for field in prediction_fields}


def _compact_knowledge_card(card: dict[str, Any]) -> dict[str, Any]:
    fields = (
        "card_id",
        "method_family",
        "school_attribution",
        "claim_scope",
        "ordered_procedure",
        "required_inputs",
        "proof_ceiling",
        "source_anchors",
        "limitations",
        "conflicts",
        "forbidden_shortcuts",
    )
    return {field: card[field] for field in fields if field in card}


def _current_questions(current_case: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(current_case, dict):
        return []
    questions = current_case.get("questions")
    if not isinstance(questions, dict):
        return []
    parsed = questions.get("parsed")
    return parsed if isinstance(parsed, list) else []


def _build_question_execution_routes(
    current_case: dict[str, Any] | None,
    rule_router: dict[str, Any],
    knowledge_cards: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    card_sources = {
        card["card_id"]: {
            anchor["source_id"]
            for anchor in card.get("source_anchors", [])
            if isinstance(anchor, dict) and isinstance(anchor.get("source_id"), str)
        }
        for card in knowledge_cards
    }
    routes: list[dict[str, Any]] = []
    for question in _current_questions(current_case):
        profile = question.get("preblind_profile", {})
        topics = profile.get("topic_tags", [])
        source_routes = profile.get("source_routes", [])
        source_set = set(source_routes)
        decisive: list[str] = []
        counter: list[str] = []
        for topic in topics:
            topic_route = rule_router.get("topics", {}).get(topic, {})
            for rule_id in topic_route.get(
                "decisive_or_supporting_rule_ids",
                [],
            ):
                if rule_id not in decisive:
                    decisive.append(rule_id)
            for rule_id in topic_route.get("counterevidence_rule_ids", []):
                if rule_id not in counter:
                    counter.append(rule_id)
        routes.append(
            {
                "question_id": question["question_id"],
                "knowledge_card_ids": [
                    card_id
                    for card_id, sources in card_sources.items()
                    if sources and sources.issubset(source_set)
                ],
                "decisive_or_supporting_rule_ids": decisive,
                "counterevidence_rule_ids": counter,
                "retrieval_mode": "ANCHOR_FIRST_PROGRESSIVE_EXPANSION",
            }
        )
    return routes


def _compose_runtime_model(
    *,
    release_id: str,
    reasoning_core: dict[str, Any] | None,
    knowledge_route_map: dict[str, Any] | None,
    compact_knowledge_cards: list[dict[str, Any]],
    compact_rules: list[dict[str, Any]],
    compact_process_corrections: list[dict[str, Any]],
    model_runtime: dict[str, Any] | None,
    post_handoff_policy: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema": "CHAT-COMPILED-RUNTIME-MODEL-V1",
        "release_id": release_id,
        "reasoning_core": compact_reasoning_core(reasoning_core),
        "knowledge_route_map": {
            "schema": knowledge_route_map["schema"],
            "mandatory_reasoning_order": knowledge_route_map[
                "mandatory_reasoning_order"
            ],
            "execution_gates": knowledge_route_map["execution_gates"],
            "authority": knowledge_route_map["authority"],
        }
        if knowledge_route_map is not None
        else None,
        "knowledge_cards": compact_knowledge_cards,
        "active_rules": compact_rules,
        "active_process_corrections": compact_process_corrections,
        "knowledge_card_runtime_authority": (
            model_runtime["knowledge_cards"]["compiled_runtime_ref"]
            if model_runtime is not None
            else "chat-input/runtime-model.json#knowledge_cards"
        ),
        "knowledge_workbench_chat_read_allowed": False,
        "post_prediction_handoff": {
            "phase": post_handoff_policy["phase"],
            "allowed_tool_classes": post_handoff_policy[
                "allowed_tool_classes"
            ],
            "allowed_issue_count_per_round": post_handoff_policy[
                "allowed_issue_count_per_round"
            ],
            "transition_requirements": post_handoff_policy[
                "transition_requirements"
            ],
            "normalization_authority": post_handoff_policy[
                "normalization_authority"
            ],
            "chat_local_preflight_required": False,
            "all_other_git_writes": "DENY",
        },
        "compilation_rule": (
            "Only prediction-execution fields are included. Learning-history reasoning, "
            "expected-effect prose, empty validation examples, and duplicate routing metadata "
            "remain in the bound release but are not repeated in the Chat runtime."
        ),
        "predictive_content_omitted": False,
    }


def _compose_chat_input_and_runtime_model(
    root: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    root = root.resolve()
    state = load_json(root / "training" / "state.json")
    group = load_json(root / state["group_path"])
    manifest = load_json(root / state["source_manifest_path"])
    taxonomy = load_taxonomy(root)
    runtime_performance = load_json(root / CHAT_RUNTIME_POLICY_RELATIVE_PATH)

    current_case_id = None
    current_case = None
    current_case_sha256 = None
    current_case_state: dict[str, Any] = {}
    if state["status"] in CASE_VISIBLE_STATES:
        current_case_id = state.get("active_replay_case_id")
        if current_case_id is None:
            current_case_id = group["case_order"][state["current_case_index"]]
        current_case_state = state["cases"][current_case_id]
        case_path = root / group["cases"][current_case_id]
        current_case = load_json(case_path)
        current_case_sha256 = sha256_file(case_path)

    release_id = state["current_model_release"]
    release = load_json(root / "model-learning" / "releases" / f"{release_id}.json")
    active_rules = safe_active_rules(root, release)
    rule_router = build_rule_router(root, release)
    runtime_governance = load_runtime_governance(root)
    model_runtime_path = root / "config" / "model-runtime.json"
    model_runtime = load_json(model_runtime_path) if model_runtime_path.is_file() else None
    post_handoff_policy = load_post_prediction_handoff_policy(root)
    reasoning_core = (
        load_json(root / model_runtime["reasoning_core"])
        if model_runtime is not None
        else None
    )
    knowledge_route_map = (
        load_json(root / model_runtime["knowledge_route_map"])
        if model_runtime is not None
        else None
    )
    knowledge_card_payloads = (
        [
            load_json(root / relative_path)
            for relative_path in model_runtime["knowledge_cards"][
                "build_time_sources"
            ]
        ]
        if model_runtime is not None
        else []
    )
    knowledge_cards = [
        card
        for payload in knowledge_card_payloads
        for card in payload.get("cards", [])
    ]
    active_process_corrections = [
        patch["content"]
        for relative_path in release.get("patches", [])
        for patch in [load_json(root / relative_path)]
        if patch.get("schema") == "MODEL-LEARNING-PATCH-V3"
    ]
    compact_rules = [_compact_rule(rule) for rule in active_rules]
    compact_process_corrections = [
        _compact_process_correction(correction, index)
        for index, correction in enumerate(active_process_corrections, start=1)
    ]
    compact_knowledge_cards = [
        _compact_knowledge_card(card) for card in knowledge_cards
    ]
    question_execution_routes = _build_question_execution_routes(
        current_case,
        rule_router,
        compact_knowledge_cards,
    )
    runtime_model = _compose_runtime_model(
        release_id=release_id,
        reasoning_core=reasoning_core,
        knowledge_route_map=knowledge_route_map,
        compact_knowledge_cards=compact_knowledge_cards,
        compact_rules=compact_rules,
        compact_process_corrections=compact_process_corrections,
        model_runtime=model_runtime,
        post_handoff_policy=post_handoff_policy,
    )
    effective_model_input_sha256 = object_sha256(
        {
            "release": release,
            "reasoning_core": reasoning_core,
            "knowledge_route_map": knowledge_route_map,
            "knowledge_cards": knowledge_cards,
            "active_rules": active_rules,
            "active_process_corrections": active_process_corrections,
            "rule_router": rule_router,
            "runtime_governance": runtime_governance,
        }
    )
    prediction_allowed = (
        state["status"] in OPENABLE_STATES
        and state.get("active_round_id") is None
        and current_case_id is not None
    )
    recommended_round_id = next_round_id(state) if prediction_allowed else None
    prediction_access_contract = build_prediction_access_contract(root, state)
    prediction_access_execution_receipt = (
        build_prediction_access_execution_receipt(prediction_access_contract)
    )

    return {
        "schema": "CHAT-PREDICTION-INPUT-V3",
        "repository": "chinaneedM/ziwei-bazi-model",
        "branch": "main",
        "state_summary": {
            "status": state["status"],
            "current_case_id": current_case_id,
            "current_model_release": release_id,
            "round_count": state["round_count"],
            "prediction_allowed": prediction_allowed,
            "recommended_round_id": recommended_round_id,
            "training_unit": "FIRST_BLIND_CASE_WITH_SPACED_REPLAY",
            "case_attempt_policy": "ONE_FIRST_BLIND_THEN_SPACED_DIAGNOSTIC_REPLAY",
            "evaluation_kind": (
                "SPACED_REPLAY"
                if state.get("active_replay_case_id") == current_case_id
                else "FIRST_BLIND"
            ),
            "independent_pass_streak": state.get("independent_pass_streak", 0),
            "required_consecutive_independent_passes": (
                REQUIRED_CONSECUTIVE_INDEPENDENT_PASSES
            ),
            "failed_first_blind_resets_independent_passes": True,
            "same_case_replay_counts_toward_stage_gate": False,
            "minimum_new_cases_between_replays": MINIMUM_NEW_CASES_BETWEEN_REPLAYS,
            "spaced_replay_queue_size": len(state.get("spaced_replay_queue", [])),
            "dataset_manifest_path": state.get("dataset_manifest_path"),
            "dataset_runtime_status": state.get("dataset_runtime_status"),
            "mode": state.get("mode", "LEGACY_MIGRATION"),
            "formal_phase": state.get("formal_phase"),
        },
        "component_hashes": {
            "current_case_sha256": current_case_sha256,
            "current_model_release_sha256": object_sha256(release),
            "question_taxonomy_sha256": object_sha256(taxonomy),
            "canonical_source_manifest_sha256": object_sha256(manifest),
            "reasoning_core_sha256": object_sha256(reasoning_core),
            "knowledge_route_map_sha256": object_sha256(knowledge_route_map),
            "knowledge_cards_sha256": object_sha256(knowledge_cards),
            "effective_model_input_sha256": effective_model_input_sha256,
            "chat_runtime_policy_sha256": object_sha256(runtime_performance),
            "prediction_row_template_sha256": object_sha256(
                _prediction_row_template()
            ),
            "compiled_runtime_model_sha256": object_sha256(runtime_model),
        },
        "current_case": current_case,
        "question_taxonomy": {
            "schema": taxonomy["schema"],
            "path": "config/question-taxonomy.json",
            "sha256": object_sha256(taxonomy),
            "load_when": "FINAL_TAG_VALIDATION_ONLY",
        },
        "current_model": {
            "release_id": release_id,
            "compiled_runtime_model_ref": {
                "path": CHAT_RUNTIME_MODEL_RELATIVE_PATH.as_posix(),
                "sha256": object_sha256(runtime_model),
                "load_when": "AFTER_BINDING_CHECK_BEFORE_SHARED_CHART_MODEL",
            },
            "knowledge_cards": {
                "authority": "DERIVED_ROUTING_AND_PROCEDURE_ONLY",
                "card_count": len(knowledge_cards),
            },
            "active_rule_count": len(compact_rules),
            "active_process_correction_count": len(
                compact_process_corrections
            ),
            "question_execution_routes": question_execution_routes,
            "runtime_governance": {
                "schema": runtime_governance["schema"],
                "suppressed_rule_count": len(
                    runtime_governance.get("suppressed_rules", [])
                ),
                "suppressed_rule_ids": sorted(
                    row["rule_id"]
                    for row in runtime_governance.get("suppressed_rules", [])
                ),
            },
            "rule_application_policy": {
                "VALIDATED": "May be used normally within its declared scope.",
                "PROVISIONAL": "Use as a low-weight hypothesis and never as sole evidence.",
                "CANDIDATE": "Use only when scope matches; never as sole evidence.",
                "CHALLENGED": "Treat as a warning or counter-hypothesis, not a decisive rule.",
                "ATTRIBUTION": (
                    "Classify every applied rule as decisive, supporting, or "
                    "counterevidence. Removing a decisive rule must change Top1."
                ),
                "MAX_MODEL_LEARNING_RULES_PER_QUESTION": MAX_APPLIED_RULES_PER_QUESTION,
                "CANONICAL_EVIDENCE_QUOTA": None,
                "EVIDENCE_STOP_RULE": (
                    "There is no evidence quota. Stop only after every option's required "
                    "and distinctive atoms are marked supported, contradicted, or unknown; "
                    "every rival has been compared with Top1; and no unread declared source "
                    "section is reasonably capable of changing the ordering. Otherwise expand "
                    "retrieval. Unknowns remain explicit and cap confidence."
                ),
            },
        },
        "runtime_performance_contract": runtime_performance,
        "post_prediction_handoff_policy": post_handoff_policy,
        "prediction_output_contract": {
            "prediction_schema": "PREDICTION-WORKBOOK-V2",
            "frozen_schema": "FROZEN-PREDICTION-V2",
            "packet_schema_after_reveal": "TRAINING-ISSUE-PACKET-V3",
            "top_level_required": [
                "schema",
                "case_id",
                "round_id",
                "blind_chart_model",
                "cross_question_consistency",
                "replay_remediation",
                "predictions",
            ],
            "each_question_must_include": [
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
            ],
            "question_profile_fields": [
                "topic_tags",
                "subject_tags",
                "time_scope_tags",
                "endpoint_tags",
                "reasoning_skill_tags",
                "source_routes",
                "applied_rule_ids",
            ],
            "rule_attribution_fields": [
                "decisive_rule_ids",
                "supporting_rule_ids",
                "counterevidence_rule_ids",
                "decision_changed",
            ],
            "tagging_rule": (
                "Classify every question before reveal using only its stem/options and the no-answer chart. "
                "Use only taxonomy values. List a rule in applied_rule_ids only when it materially affects "
                "the frozen reasoning; unrelated questions do not validate that rule. Select no more than "
                f"{MAX_APPLIED_RULES_PER_QUESTION} scope-matched rules from question_execution_routes "
                "and the compiled runtime model. A CHALLENGED rule may appear only as counterevidence."
            ),
            "confidence_calibration_rule": (
                "If actor, exact time, mechanism, or real-world endpoint is unresolved, cap confidence "
                "at 65. Forced relative choices are not high-confidence factual claims."
            ),
            "severe_atom_binding_rule": (
                "If Top1 contains severe, irreversible, or high-precision atoms, set "
                "severe_atoms_have_independent_evidence=true only when every such atom is "
                "copied exactly into supports_option_atoms as '<OPTION_ID>:<EXACT_ATOM_TEXT>' "
                "on at least one INDEPENDENT evidence row. General option support, a different "
                "atom, or a shared scene does not qualify. Preflight never derives this flag."
            ),
            "failure_learning_rule": (
                "After reveal, classify the root cause and choose one V3 remediation type. Only "
                "NEW_GENERAL_RULE may add catalog rules; execution, measurement, calibration, weighting, "
                "scope, merge, retirement, tests, and hypotheses are valid non-rule corrections."
            ),
            "reasoning_framework_status": "WORKING_HYPOTHESIS_NOT_FIXED_DOGMA",
            "evidence_count_quota": None,
            "blind_before_options_rule": (
                "Complete blind_chart_model without option text or option-derived events before "
                "building question_semantic_model and option comparisons."
            ),
        },
        "chat_work_handoff_contract": {
            "schema": "CHAT-WORK-HANDOFF-CONTRACT-V2",
            "transport": "GITHUB_ISSUE_DURABLE_RECEIPT",
            "issue_title": (
                f"[PREDICTION HANDOFF] {recommended_round_id} {current_case_id}"
                if prediction_allowed
                else None
            ),
            "handoff_schema": "CHAT-WORK-PREDICTION-HANDOFF-V2",
            "binding": {
                "case_id": current_case_id,
                "round_id": recommended_round_id,
                "evaluation_kind": (
                    "SPACED_REPLAY"
                    if state.get("active_replay_case_id") == current_case_id
                    else "FIRST_BLIND"
                ),
                "model_release": release_id,
                "current_case_sha256": current_case_sha256,
                "current_model_release_sha256": object_sha256(release),
                "canonical_source_manifest_sha256": object_sha256(manifest),
                "effective_model_input_sha256": effective_model_input_sha256,
            },
            "handoff_required_fields": [
                "schema",
                "binding",
                "prediction_access_execution_receipt",
                "blind_chart_model",
                "cross_question_consistency",
                "replay_remediation",
                "predictions",
            ],
            "handoff_payload_template": {
                "schema": "CHAT-WORK-PREDICTION-HANDOFF-V2",
                "binding": {
                    "case_id": current_case_id,
                    "round_id": recommended_round_id,
                    "evaluation_kind": (
                        "SPACED_REPLAY"
                        if state.get("active_replay_case_id") == current_case_id
                        else "FIRST_BLIND"
                    ),
                    "model_release": release_id,
                    "current_case_sha256": current_case_sha256,
                    "current_model_release_sha256": object_sha256(release),
                    "canonical_source_manifest_sha256": object_sha256(manifest),
                    "effective_model_input_sha256": effective_model_input_sha256,
                },
                "prediction_access_execution_receipt": (
                    prediction_access_execution_receipt
                ),
                "blind_chart_model": _blind_chart_model_template(),
                "cross_question_consistency": _cross_question_consistency_template(),
                "replay_remediation": (
                    _replay_remediation_template()
                    if state.get("active_replay_case_id") == current_case_id
                    else None
                ),
                "predictions": [],
            },
            "prediction_row_template_ref": {
                "path": PREDICTION_ROW_TEMPLATE_RELATIVE_PATH.as_posix(),
                "sha256": object_sha256(_prediction_row_template()),
                "load_when": "HANDOFF_ASSEMBLY_ONLY",
            },
            "serialization_constraints": {
                "encoding": "UTF-8_JSON_WITHOUT_CODE_FENCES",
                "exact_fields_only": True,
                "confidence_unit": "INTEGER_PERCENT_0_TO_100",
                "track_evidence_partition_rule": (
                    "Within each Ziwei or Bazi track, supporting_evidence_ids and "
                    "contradicting_evidence_ids must be disjoint. Evidence that supports "
                    "Top1 by contradicting a rival remains supporting evidence for Top1."
                ),
                "overall_confidence_cap_rule": (
                    "overall_confidence must not exceed the weakest of the other eight "
                    "confidence components."
                ),
                "decisive_rule_ablation_rule": (
                    "Provide exactly one decisive_rule_ablations row for every "
                    "rule_attribution.decisive_rule_ids entry; removing that rule must "
                    "change Top1, or reclassify it as supporting before freeze."
                ),
                "reversal_test_consistency_rule": (
                    "Derive top1_survives by comparing ranking_before with "
                    "ranking_after_removal; never copy the template placeholder."
                ),
                "fractional_confidence_normalization": (
                    "A numeric float from 0.0 through 1.0 is deterministically "
                    "converted to the nearest integer percent before validation."
                ),
                "rule_status_normalization": (
                    "CHALLENGED rules are automatically moved out of decisive/supporting "
                    "roles into counterevidence. RETIRED or suppressed rules fail closed."
                ),
                "github_issue_body_hard_limit_characters": (
                    GITHUB_ISSUE_BODY_MAX_CHARACTERS
                ),
                "target_max_characters": HANDOFF_TARGET_MAX_CHARACTERS,
                "preferred_max_characters": HANDOFF_PREFERRED_MAX_CHARACTERS,
                "chat_local_preflight_required": False,
                "chat_required_capabilities": [
                    "GITHUB_FETCH_FILE",
                    "GITHUB_CREATE_ISSUE",
                ],
                "controller_validation_workflow": post_handoff_policy[
                    "controller_workflow"
                ],
                "normalization_authority": post_handoff_policy[
                    "normalization_authority"
                ],
                "preflight_rule": (
                    "CHAT applies the deterministic serialization rules embedded here, then "
                    "after complete freeze and binding/receipt verification enters "
                    "POST_PREDICTION_HANDOFF and creates exactly one Issue through the GitHub "
                    "connector. The GitHub controller performs authoritative normalization and "
                    "full validation, including fractional confidence conversion, rule-ledger "
                    "status enforcement, compact serialization, binding checks, receipt checks, "
                    "and size checks. No local gh, clone, Python, or terminal command is required. "
                    "Keep every required field and every substantive evidence row, deduplicate "
                    "repeated prose, and shorten wording toward "
                    f"{HANDOFF_PREFERRED_MAX_CHARACTERS} characters. Evidence completeness takes "
                    f"priority up to {HANDOFF_TARGET_MAX_CHARACTERS} characters. Never split one "
                    "handoff across Issues, remove ranking-changing evidence, or change Top1 or "
                    "Top2 to meet the preferred budget."
                ),
            },
            "handoff_forbidden_content": [
                "ANSWER_BEARING_FIELDS",
                "SCORING_OR_REVIEW_FIELDS",
                "EXPECTED_OUTCOME_FIELDS",
                "LEARNING_PATCH_FIELDS",
                "SECRETS_OR_KEYS",
            ],
            "chat_freeze_rule": (
                "After all predictions are frozen and the binding plus access execution receipt "
                "are verified, transition from PREDICTION to POST_PREDICTION_HANDOFF. Only then "
                "create exactly one GitHub Issue using issue_title and "
                "CHAT-WORK-PREDICTION-HANDOFF-V2. Copy binding exactly and preserve the complete "
                "prediction rows. This one GITHUB_CREATE_ISSUE call is the only Chat-side GitHub "
                "write allowed; all other Git writes remain denied."
            ),
            "work_acceptance_rule": (
                "Read the unique open handoff Issue for binding.round_id; never reconstruct predictions "
                "from conversation memory. Validate every binding value against this current bundle and "
                "stop before scoring if the receipt is missing, duplicated, stale, or mismatched."
            ),
            "training_issue_input_contract": {
                "schema": "TRAINING-ISSUE-PACKET-V3",
                "allowed_top_level_fields": [
                    "schema",
                    "round_id",
                    "case_id",
                    "blind_chart_model",
                    "cross_question_consistency",
                    "replay_remediation",
                    "predictions",
                    "expected_result",
                    "learning_release_id",
                    "learning_patch",
                ],
                "pass_required_fields": [
                    "schema",
                    "round_id",
                    "case_id",
                    "blind_chart_model",
                    "cross_question_consistency",
                    "replay_remediation",
                    "predictions",
                    "expected_result",
                ],
                "pass_forbidden_fields": [
                    "learning_release_id",
                    "learning_patch",
                ],
                "fail_required_fields": [
                    "schema",
                    "round_id",
                    "case_id",
                    "blind_chart_model",
                    "cross_question_consistency",
                    "replay_remediation",
                    "predictions",
                    "expected_result",
                    "learning_release_id",
                    "learning_patch",
                ],
                "result_only_fields_forbidden_in_input": [
                    "evaluation_kind",
                    "accuracy",
                    "correct_count",
                    "top2_coverage",
                    "learning_release",
                    "next_case_id",
                    "next_status",
                ],
            },
        },
        "canonical_source_manifest": manifest,
        "prediction_access_contract": prediction_access_contract,
        "contains_old_predictions": False,
        "contains_answers": False,
        "contains_scores_or_reviews": False,
    }, runtime_model


def compose_chat_input(root: Path) -> dict[str, Any]:
    payload, _runtime_model = _compose_chat_input_and_runtime_model(root)
    return payload


def write_chat_input(root: Path) -> dict[str, Any]:
    root = root.resolve()
    payload, runtime_model = _compose_chat_input_and_runtime_model(root)
    access_contract = payload["prediction_access_contract"]
    atomic_write_compact_json(
        root / PREDICTION_ACCESS_CONTRACT_PATH,
        access_contract,
    )
    atomic_write_compact_json(
        root / CHAT_RUNTIME_MODEL_RELATIVE_PATH,
        runtime_model,
    )
    atomic_write_json(
        root / PREDICTION_ROW_TEMPLATE_RELATIVE_PATH,
        _prediction_row_template(),
    )
    atomic_write_compact_json(root / CHAT_INPUT_RELATIVE_PATH, payload)
    return payload
