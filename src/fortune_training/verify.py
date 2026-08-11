from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .chat_input import (
    CHAT_INPUT_RELATIVE_PATH,
    CHAT_RUNTIME_MODEL_RELATIVE_PATH,
    PREDICTION_ROW_TEMPLATE_RELATIVE_PATH,
    compact_reasoning_core,
    compose_chat_input,
)
from .case_bank import validate_case_bank
from .calendar_foundation.policies import PolicyRegistry
from .canonical_runtime import (
    RUNTIME_MANIFEST_PATH,
    validate_canonical_runtime,
)
from .source_access import DERIVED_ACCESS_ROOT
from .source_access_validator import validate_source_access
from .classical_relation_evidence import (
    MATRIX_PATH as CLASSICAL_RELATION_EVIDENCE_MATRIX_PATH,
    validate_classical_relation_evidence,
)
from .bazi_five_combination_evidence_binding import (
    BINDINGS_PATH as FIVE_COMBINATION_EVIDENCE_BINDINGS_PATH,
    validate_five_combination_evidence_bindings,
)
from .bazi_classical_relation_interaction_assertion import (
    MATRIX_PATH as CLASSICAL_RELATION_INTERACTION_ASSERTION_MATRIX_PATH,
    validate_classical_relation_interaction_assertion_matrix,
)
from .learning import (
    LEDGER_RELATIVE_PATH,
    load_rule_catalog,
    load_taxonomy,
    validate_learning_patch_v3,
    validate_learning_ledger,
    validate_rule,
)
from .maintenance import validate_maintenance
from .policy import (
    REQUIRED_CONSECUTIVE_INDEPENDENT_PASSES,
    load_and_validate_policy,
)
from .prediction_access import (
    PREDICTION_ACCESS_CONTRACT_PATH,
    build_prediction_access_contract,
    load_post_prediction_handoff_policy,
    load_prediction_tool_policy,
    validate_prediction_access_contract,
)
from .util import TrainingError, is_within, load_json, object_sha256, sha256_file


SOURCE_ID = re.compile(r"^(S(?:0[0-9]|1[0-9]))_")
ALLOWED_ANSWER_KEYS = {
    "answer_isolation",
    "answer_payload_present",
    "answer_reference_disclosed",
}
FORBIDDEN_CASE_KEYS = {
    "answer",
    "answers",
    "answer_key",
    "correct_answer",
    "correct_option",
    "gold",
    "label",
    "revealed_answer",
}


def _validate_time_calendar_foundation(root: Path) -> dict[str, Any]:
    registry_path = root / "config" / "time-calendar-policies.json"
    schema_path = root / "schemas" / "time-calendar-foundation-v1.schema.json"
    try:
        registry = PolicyRegistry.from_file(registry_path)
        defaults = registry.validate_selection(registry.default_selection())
    except (OSError, ValueError) as exc:
        raise TrainingError(f"invalid time/calendar policy registry: {exc}") from exc
    expected_policy_ids = {
        "civil.ambiguous_time_policy",
        "bazi.year_boundary_policy",
        "bazi.day_boundary_policy",
        "bazi.late_zi_hour_stem_policy",
        "ziwei.calendar_date_policy",
        "ziwei.life_body_leap_month_policy",
    }
    if set(registry.payload["policies"]) != expected_policy_ids:
        raise TrainingError("time/calendar policy registry has an incomplete policy set")
    leap_policy = registry.policy("ziwei.life_body_leap_month_policy")
    if leap_policy.get("allowed_scope") != ["ZIWEI_LIFE_BODY_PLACEMENT"]:
        raise TrainingError("Ziwei leap-month policy escaped its proven R1 scope")
    schema = load_json(schema_path)
    if (
        schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema"
        or schema.get("properties", {}).get("schema", {}).get("const")
        != "TIME-CALENDAR-FOUNDATION-RESULT-V1"
        or schema.get("properties", {})
        .get("metadata", {})
        .get("properties", {})
        .get("canonical_sources_modified", {})
        .get("const")
        is not False
    ):
        raise TrainingError("invalid Time/Calendar Foundation schema")
    return {
        "schema": schema["properties"]["schema"]["const"],
        "policy_registry_version": registry.version,
        "policy_count": len(expected_policy_ids),
        "default_selection": defaults.__dict__,
        "canonical_sources_modified": False,
    }
REQUIRED_METHOD_GATES = {
    "CALENDAR_SOLAR_TERM_MONTH_MAPPING",
    "ZIWEI_COORDINATE_INTEGRITY",
    "ZIWEI_COORDINATE_TRUTH_TABLE",
    "PERIOD_NAMESPACE_YEAR_ALIGNMENT",
    "BAZI_IMMUTABLE_ATOMIC_FACT_LEDGER",
    "BAZI_STRENGTH_STRUCTURE_FAVORABILITY_CHAIN",
    "BAZI_DYNAMIC_RELATION_SCOPE",
    "RESULT_QUESTION_DYNAMIC_CLOSURE",
    "QUESTION_SCOPE_MINIMUM_SUFFICIENT_RETRIEVAL",
    "EVENT_CAUSE_SENSITIVE_REALITY_ATOM_BOUNDARY",
    "ENTITY_NONEXISTENCE_NONBINARY",
    "EVENT_SPECIFICITY_WEIGHT_DOMINANCE",
    "PRIMARY_AUXILIARY_QI_DYNAMIC_ROUTING",
    "CROSS_QUESTION_JOINT_CANDIDATE_MATRIX",
    "STATUS_TRANSITION_STATE_MACHINE",
    "COLLABORATIVE_HYPOTHESIS_REVALIDATION",
    "CROSS_CASE_HYPOTHESIS_QUARANTINE",
    "COMPOSITE_REQUIRED_ATOM_CLOSURE",
    "UPSTREAM_FACT_DEPENDENCY_INVALIDATION",
    "TIME_BOUNDARY_PARALLEL_CHART_BRANCHES",
}
REQUIRED_ROUTE_GATES = {
    "calendar_and_month_mapping",
    "ziwei_coordinate_integrity",
    "ziwei_coordinate_truth_table",
    "period_namespace_alignment",
    "bazi_atomic_fact_ledger",
    "bazi_strength_structure_favorability",
    "bazi_dynamic_relation_scope",
    "result_dynamic_closure",
    "question_scope_minimum_sufficient_retrieval",
    "event_cause_sensitive_reality_atom_boundary",
    "entity_nonexistence",
    "event_specificity",
    "topic_palace_chain",
    "cross_question_joint_candidates",
    "status_transition_state_machine",
    "collaborative_hypothesis_revalidation",
    "cross_case_hypothesis_quarantine",
    "composite_required_atom_closure",
    "upstream_fact_dependency_invalidation",
    "time_boundary_parallel_branches",
}
REQUIRED_METHOD_GATE_CHECKS = {
    "ZIWEI_COORDINATE_INTEGRITY": {
        "transformations_bind_origin_layer_heavenly_stem_transformed_star_and_destination_palace",
    },
    "ZIWEI_COORDINATE_TRUTH_TABLE": {
        "materialize_one_immutable_coordinate_truth_table",
        "include_natal_major_period_year_and_each_subject_taiji_namespace",
        "require_exactly_twelve_unique_palace_rows_per_namespace",
        "assign_stable_coordinate_ids",
        "freeze_one_natal_physical_star_inventory",
        "bind_every_dynamic_coordinate_to_its_natal_physical_coordinate",
        "mechanically_verify_opposites_and_trines",
        "keep_qi_and_one_six_as_distinct_typed_links",
        "allow_empty_palace_borrowing_only_from_the_verified_opposite",
        "require_all_downstream_ziwei_claims_to_reference_coordinate_ids",
        "materialize_all_twelve_subject_taiji_palaces_before_topic_reasoning",
        "bind_each_transformation_to_source_kind_origin_layer_heavenly_stem_transformation_type_star_origin_and_semantic_destination",
        "forbid_transformations_from_moving_physical_star_coordinates",
    },
    "PERIOD_NAMESPACE_YEAR_ALIGNMENT": {
        "name_ziwei_periods_under_ziwei_major_period_namespace",
        "name_bazi_periods_under_bazi_luck_cycle_namespace",
        "forbid_unqualified_major_period_or_luck_cycle_labels",
        "bind_each_period_to_explicit_start_and_end_years",
        "validate_reference_year_membership_independently_in_each_track",
        "record_age_convention_and_boundary_handling",
    },
    "BAZI_IMMUTABLE_ATOMIC_FACT_LEDGER": {
        "freeze_exact_year_month_day_and_hour_pillars",
        "derive_hidden_stems_under_one_declared_convention",
        "derive_all_visible_and_hidden_stem_ten_gods_from_the_day_master",
        "derive_five_elements_and_element_roles_for_every_atomic_fact",
        "derive_visible_stem_root_presence_and_qi_grade",
        "enumerate_all_natal_heavenly_stem_five_combinations",
        "enumerate_all_natal_earthly_branch_combinations_clashes_punishments_harms_and_breaks",
        "bind_one_mechanical_verification_receipt",
        "forbid_downstream_mutation_or_option_driven_recalculation",
    },
    "BAZI_STRENGTH_STRUCTURE_FAVORABILITY_CHAIN": {
        "bind_the_chain_to_the_atomic_ledger_hash",
        "identify_month_command_and_seasonal_qi",
        "enumerate_all_peer_resource_output_wealth_and_officer_facts",
        "enumerate_day_master_root_facts",
        "enumerate_all_declared_relation_facts",
        "compare_competing_strength_candidates",
        "compare_competing_pattern_candidates",
        "compare_competing_favorability_candidates",
        "freeze_selected_candidates_before_option_ranking",
        "preserve_unresolved_method_conflicts",
    },
    "BAZI_DYNAMIC_RELATION_SCOPE": {
        "assign_each_natal_period_year_and_month_object_to_one_scope_id",
        "separate_active_query_objects_from_historical_validation_anchors",
        "enumerate_relations_only_among_objects_active_in_the_declared_scope",
        "treat_historical_event_years_as_inactive_by_default",
        "require_named_method_source_route_and_bounded_objects_for_any_cross_time_reactivation",
        "prevent_one_historical_anchor_from_becoming_reusable_future_dynamic_evidence",
    },
    "EVENT_SPECIFICITY_WEIGHT_DOMINANCE": {
        "label_each_evidence_row_as_direct_same_axis_one_hop_or_multi_hop",
        "materialize_every_intermediate_link_for_transmitted_evidence",
        "discount_longer_transmission_distance_before_general_counts",
    },
    "QUESTION_SCOPE_MINIMUM_SUFFICIENT_RETRIEVAL": {
        "classify_each_question_as_static_current_result_or_time_comparison",
        "resolve_the_target_time_for_every_nonstatic_question",
        "declare_required_and_actually_inspected_layers",
        "require_natal_ziwei_major_period_bazi_luck_cycle_and_year_for_current_or_dynamic_questions",
        "justify_every_extra_layer_or_advanced_module_by_a_live_competition_gap",
        "preserve_all_question_required_core_layers",
    },
    "EVENT_CAUSE_SENSITIVE_REALITY_ATOM_BOUNDARY": {
        "classify_cause_atoms_separately_from_event_atoms",
        "require_an_independent_same_option_event_to_cause_bridge_before_cause_completion",
        "classify_reality_identity_and_primary_cashflow_atoms",
        "require_independent_reality_endpoint_evidence_for_identity_or_primary_cashflow_completion",
        "mark_sensitive_noninferable_atoms",
        "keep_sensitive_noninferable_atoms_unknown_and_out_of_chart_evidence",
    },
    "CROSS_QUESTION_JOINT_CANDIDATE_MATRIX": {
        "identify_related_questions_without_assuming_shared_answers",
        "build_joint_candidates_on_explicit_dimensions_such_as_year_by_cause",
        "preserve_each_questions_independent_evidence_ledger",
        "allow_only_independent_direct_same_axis_counterevidence_edges_between_questions",
        "forbid_cyclic_cross_question_dependencies",
        "zero_story_coherence_and_repeated_evidence_as_decision_weight",
        "rerun_pairwise_ranking_after_valid_cross_question_counterevidence",
    },
    "STATUS_TRANSITION_STATE_MACHINE": {
        "declare_state_domain_for_marriage_career_asset_and_other_status_questions",
        "separate_entry_maintenance_impairment_and_exit_transitions",
        "require_observable_transition_evidence_for_each_state_change",
        "treat_damage_pressure_or_interruption_as_nonterminal_by_default",
        "test_recovery_continuation_and_substitute_states",
        "bind_terminal_exit_to_independent_dynamic_endpoint_evidence",
    },
    "COLLABORATIVE_HYPOTHESIS_REVALIDATION": {
        "label_every_user_or_model_proposed_derivation_as_unverified_hypothesis",
        "return_to_the_frozen_chart_before_acceptance",
        "recompute_coordinates_and_time_mappings_from_the_truth_table",
        "seek_independent_support_and_same_axis_counterevidence",
        "record_accept_revise_or_reject_status_with_basis",
        "forbid_authority_fluency_or_agreement_as_evidence",
    },
    "CROSS_CASE_HYPOTHESIS_QUARANTINE": {
        "register_new_recurrence_patterns_as_generic_hypotheses_only",
        "strip_case_answers_options_years_and_prediction_directions",
        "predeclare_scope_mechanism_and_falsification_conditions",
        "require_independent_cross_case_support_and_counterexamples",
        "keep_runtime_decision_weight_at_zero_while_pending",
        "forbid_promotion_by_single_case_discussion_or_replay",
        "promote_only_through_the_existing_governance_and_validation_process",
    },
    "COMPOSITE_REQUIRED_ATOM_CLOSURE": {
        "partition_every_required_atom_as_independently_supported_directly_refuted_or_unknown",
        "require_exact_atom_evidence_bindings",
        "forbid_half_match_whole_option_acceptance",
        "reduce_top1_confidence_when_any_required_atom_is_not_independently_closed",
        "preserve_existing_independent_evidence_fail_closed_for_severe_irreversible_and_high_precision_atoms",
    },
    "UPSTREAM_FACT_DEPENDENCY_INVALIDATION": {
        "register_ziwei_coordinate_transformation_bazi_atomic_and_period_facts_by_stable_id",
        "bind_every_evidence_row_to_branch_scoped_upstream_fact_ids",
        "hash_each_dependency_set_independently_of_evidence_wording",
        "recompute_upstream_facts_before_ranking",
        "invalidate_all_evidence_with_any_failed_dependency",
        "remove_invalidated_evidence_from_tracks_matrices_reversal_tests_and_branch_rankings",
        "rerun_ranking_after_invalidation",
    },
    "TIME_BOUNDARY_PARALLEL_CHART_BRANCHES": {
        "detect_true_solar_time_late_zi_day_change_and_other_hour_boundary_ambiguity",
        "materialize_every_legal_branch_before_option_reading",
        "build_a_complete_ziwei_coordinate_truth_table_per_branch",
        "build_and_mechanically_verify_a_complete_bazi_atomic_ledger_per_branch",
        "label_every_evidence_row_with_exactly_one_branch",
        "rank_every_branch_independently",
        "forbid_option_atoms_from_time_calibration",
        "preserve_uncertainty_when_branch_top1_differs",
        "allow_branch_selection_only_from_independent_external_facts",
    },
}
REQUIRED_ROUTE_GATE_ORDERS = {
    "ziwei_coordinate_truth_table": [
        "natal_twelve_palaces_and_physical_star_inventory",
        "ziwei_major_period_twelve_palaces",
        "ziwei_year_twelve_palaces",
        "each_rotated_subject_taiji_twelve_palaces",
        "same_branch_natal_coordinate_bindings",
        "mechanical_opposite_and_trine_topology",
        "separate_qi_and_one_six_links",
        "opposite_only_empty_palace_borrowing",
        "source_kind_type_star_origin_and_semantic_destination_for_transformations",
        "downstream_read_only_coordinate_references",
    ],
    "period_namespace_alignment": [
        "ziwei_major_period_namespace",
        "bazi_luck_cycle_namespace",
        "explicit_start_and_end_years",
        "age_and_boundary_conventions",
        "independent_reference_year_membership",
        "preserved_cross_track_conflicts",
    ],
    "bazi_atomic_fact_ledger": [
        "four_pillars",
        "hidden_stems",
        "ten_gods",
        "five_elements_and_element_roles",
        "visible_stem_roots",
        "heavenly_stem_five_combinations",
        "earthly_branch_combinations_clashes_punishments_harms_and_breaks",
        "mechanical_verification_receipt",
        "immutable_downstream_reference",
    ],
    "bazi_strength_structure_favorability": [
        "atomic_ledger_hash_binding",
        "month_command_and_seasonal_qi",
        "complete_support_drain_and_control_fact_classes",
        "day_master_roots",
        "relation_facts",
        "strength_candidate_comparison",
        "pattern_candidate_comparison",
        "favorability_candidate_comparison",
        "option_blind_freeze",
        "unresolved_method_conflicts",
    ],
    "bazi_dynamic_relation_scope": [
        "natal_objects",
        "bazi_luck_cycle_objects",
        "active_query_year_and_month_objects",
        "historical_validation_anchors",
        "within_scope_relations",
        "declared_cross_time_method_if_any",
        "source_route_and_bounded_reactivated_objects",
    ],
    "event_specificity": [
        "same_axis_counterevidence",
        "direct_same_axis_event_evidence",
        "completed_event_specific_chain",
        "one_hop_transmission_with_complete_path",
        "time_bound_distinguishing_mechanism",
        "multi_hop_transmission_with_complete_path",
        "topic_specific_structure",
        "general_tendency",
    ],
    "cross_question_joint_candidates": [
        "related_question_detection",
        "explicit_joint_dimensions",
        "per_question_independent_evidence",
        "direct_same_axis_counterevidence_edges_only",
        "acyclic_dependency_check",
        "story_coherence_and_duplicate_evidence_zeroing",
        "affected_pairwise_ranking_recheck",
    ],
    "question_scope_minimum_sufficient_retrieval": [
        "question_mode",
        "target_time_resolution",
        "required_layers",
        "actually_inspected_layers",
        "advanced_module_justification",
        "core_layer_preservation",
    ],
    "event_cause_sensitive_reality_atom_boundary": [
        "event_atoms",
        "cause_atoms",
        "same_option_event_to_cause_bridge",
        "reality_identity_atoms",
        "primary_cashflow_atoms",
        "sensitive_noninferable_atoms",
        "closure_or_unknown",
    ],
    "status_transition_state_machine": [
        "state_domain",
        "entry_transition",
        "maintenance_evidence",
        "impairment_or_interruption",
        "recovery_or_substitute_state",
        "terminal_exit_endpoint",
    ],
    "collaborative_hypothesis_revalidation": [
        "unverified_hypothesis_label",
        "frozen_chart_return",
        "coordinate_and_time_recalculation",
        "independent_support_and_counterevidence",
        "accept_revise_or_reject_status",
        "ranking_eligibility",
    ],
    "cross_case_hypothesis_quarantine": [
        "generic_hypothesis_registration",
        "case_detail_stripping",
        "scope_mechanism_and_falsification_predeclaration",
        "independent_cross_case_support",
        "counterexample_review",
        "pending_zero_decision_weight",
        "governed_promotion_or_rejection",
    ],
    "composite_required_atom_closure": [
        "required_atom_inventory",
        "independent_exact_support",
        "direct_same_axis_refutation",
        "explicit_unknowns",
        "disjoint_complete_partition",
        "top1_unclosed_atom_confidence_reduction",
        "existing_severe_precision_fail_closed",
    ],
    "upstream_fact_dependency_invalidation": [
        "stable_upstream_fact_ids",
        "branch_scoped_source_resolution",
        "evidence_dependency_hashes",
        "upstream_recomputation",
        "transitive_evidence_invalidation",
        "downstream_contribution_removal",
        "ranking_recomputation",
    ],
    "time_boundary_parallel_branches": [
        "boundary_detection",
        "all_legal_branch_materialization",
        "complete_ziwei_truth_table_per_branch",
        "complete_bazi_atomic_ledger_per_branch",
        "branch_labeled_evidence",
        "independent_branch_rankings",
        "option_blind_time_calibration",
        "divergence_preservation",
        "external_fact_only_resolution",
    ],
}
REQUIRED_REASONING_THEMES = {
    "INPUT_AND_CHART_COORDINATE_FREEZE",
    "CALENDAR_SOLAR_TERM_MONTH_MAPPING_GATE",
    "ZIWEI_COORDINATE_INTEGRITY_GATE",
    "ZIWEI_COORDINATE_TRUTH_TABLE_GATE",
    "PERIOD_NAMESPACE_YEAR_ALIGNMENT_GATE",
    "BAZI_IMMUTABLE_ATOMIC_FACT_LEDGER_GATE",
    "BAZI_STRENGTH_STRUCTURE_FAVORABILITY_CHAIN_GATE",
    "BAZI_DYNAMIC_RELATION_SCOPE_GATE",
    "OPTION_BLIND_SHARED_CHART_MODEL",
    "ZIWEI_STATIC_STRUCTURE",
    "ZIWEI_DYNAMIC_ACTIVATION_WHEN_APPLICABLE",
    "BAZI_STATIC_STRUCTURE_INDEPENDENTLY",
    "BAZI_DYNAMIC_ACTIVATION_WHEN_APPLICABLE",
    "RESULT_QUESTION_MAJOR_PERIOD_YEAR_MONTH_CLOSURE",
    "QUESTION_SCOPE_MINIMUM_SUFFICIENT_RETRIEVAL_GATE",
    "EVENT_CAUSE_SENSITIVE_REALITY_ATOM_BOUNDARY_GATE",
    "PRIMARY_AUXILIARY_QI_DYNAMIC_ROUTING",
    "ACTOR_ACTION_OBJECT_TIME_ENDPOINT_CLOSURE",
    "ENTITY_NONEXISTENCE_NONBINARY_GATE",
    "EVENT_SPECIFICITY_WEIGHT_DOMINANCE",
    "REALITY_SEMANTICS_AND_MAGNITUDE",
    "ALL_OPTION_ATOM_COVERAGE",
    "ALL_OPTION_PAIR_COMPARISON",
    "TOP1_TOP2_STRONGEST_REVERSAL",
    "CROSS_TRACK_CONFLICT_PRESERVATION",
    "CROSS_QUESTION_CONSISTENCY",
    "CROSS_QUESTION_JOINT_CANDIDATE_MATRIX",
    "STATUS_TRANSITION_STATE_MACHINE",
    "COLLABORATIVE_HYPOTHESIS_REVALIDATION",
    "CROSS_CASE_HYPOTHESIS_QUARANTINE",
    "COMPOSITE_REQUIRED_ATOM_CLOSURE_GATE",
    "UPSTREAM_FACT_DEPENDENCY_INVALIDATION_GATE",
    "TIME_BOUNDARY_PARALLEL_CHART_BRANCHES_GATE",
    "CAPABILITY_LIMIT_AND_CONFIDENCE_CALIBRATION",
}


def build_source_manifest(root: Path) -> dict[str, Any]:
    """Build the immutable Git canonical-source manifest for comparison only."""
    source_dir = root / "sources" / "canonical"
    files = sorted(source_dir.glob("*.txt"))
    entries: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in files:
        match = SOURCE_ID.match(path.name)
        if not match:
            raise TrainingError(f"unexpected source filename: {path.name}")
        source_id = match.group(1)
        if source_id in seen:
            raise TrainingError(f"duplicate source library: {source_id}")
        seen.add(source_id)
        entries.append(
            {
                "source_id": source_id,
                "path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
                "runtime_role": (
                    "TRAINING_LOOP_GUIDANCE"
                    if source_id == "S19"
                    else "PREDICTION_KNOWLEDGE_ONLY"
                ),
            }
        )
    expected = {f"S{index:02d}" for index in range(20)}
    if seen != expected:
        missing = sorted(expected - seen)
        extra = sorted(seen - expected)
        raise TrainingError(f"source set must be exactly S00-S19; missing={missing}, extra={extra}")
    manifest = {
        "schema": "CANONICAL-SOURCE-MANIFEST-V1",
        "source_count": len(entries),
        "process_authority": "config/training-policy.json",
        "runtime_source": "GIT_REPOSITORY_ONLY",
        "mutability": "IMMUTABLE_DURING_TRAINING",
        "sources": entries,
    }
    return manifest


def _validate_source_policy(root: Path) -> dict[str, Any]:
    policy = load_json(root / "config" / "source-policy.json")
    if policy.get("schema") != "SOURCE-AUTHORITY-POLICY-V2":
        raise TrainingError("wrong source authority policy schema")
    expected = {
        "external_project_sources_required": False,
        "project_file_library_sources_runtime_allowed": False,
        "runtime_canonical_authority": "GIT_MAIN_SOURCES_CANONICAL_ONLY",
        "runtime_source": "GIT_REPOSITORY_ONLY",
        "git_repository": "chinaneedM/ziwei-bazi-model",
        "git_ref": "main",
        "git_canonical_path": "sources/canonical",
        "git_canonical_mutable_during_training": False,
        "canonical_runtime_manifest_path": RUNTIME_MANIFEST_PATH.as_posix(),
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
    }
    for key, value in expected.items():
        if policy.get(key) != value:
            raise TrainingError(f"source policy mismatch for {key}: expected {value!r}")
    manifest_hash = policy.get("canonical_manifest_sha256")
    if not isinstance(manifest_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", manifest_hash):
        raise TrainingError("source policy needs a valid canonical_manifest_sha256 lock")
    runtime_manifest_hash = policy.get("canonical_runtime_manifest_sha256")
    if not isinstance(runtime_manifest_hash, str) or not re.fullmatch(
        r"[0-9a-f]{64}", runtime_manifest_hash
    ):
        raise TrainingError(
            "source policy needs a valid canonical_runtime_manifest_sha256 lock"
        )
    return policy


def _validate_model_runtime_policy(root: Path) -> dict[str, Any] | None:
    path = root / "config" / "model-runtime.json"
    if not path.is_file():
        return None
    policy = load_json(path)
    if policy.get("schema") != "FORTUNE-MODEL-RUNTIME-V2":
        raise TrainingError("wrong model runtime schema")
    cards = policy.get("knowledge_cards")
    if (
        not isinstance(cards, dict)
        or set(cards)
        != {
            "build_time_sources",
            "knowledge_workbench_runtime_role",
            "chat_direct_read_allowed",
            "compiled_runtime_ref",
        }
        or cards.get("knowledge_workbench_runtime_role") != "BUILD_TIME_ONLY"
        or cards.get("chat_direct_read_allowed") is not False
        or cards.get("compiled_runtime_ref")
        != "chat-input/runtime-model.json#knowledge_cards"
        or not isinstance(cards.get("build_time_sources"), list)
        or not cards["build_time_sources"]
        or any(
            not isinstance(item, str)
            or not item.startswith("knowledge-workbench/")
            for item in cards["build_time_sources"]
        )
    ):
        raise TrainingError("knowledge cards are not build-time compiled for Chat")
    access = policy.get("chat_source_access")
    if (
        not isinstance(access, dict)
        or access.get("mode") != "GITHUB_MAIN_ALLOWLIST_ONLY"
        or access.get("file_library_allowed") is not False
        or access.get("project_sources_allowed") is not False
        or access.get("external_project_sources_required") is not False
        or access.get("historical_uploads_allowed") is not False
        or access.get("cross_conversation_memory_allowed") is not False
        or access.get("fail_closed_when_git_canonical_unavailable") is not True
        or access.get("canonical_runtime_manifest")
        != RUNTIME_MANIFEST_PATH.as_posix()
        or access.get("canonical_runtime_mode")
        != "LOSSLESS_GIT_DERIVED_SEGMENTS"
        or access.get("canonical_direct_large_file_reads_allowed") is not False
        or "fail_closed_when_project_sources_unavailable" in access
    ):
        raise TrainingError("model runtime reintroduced a project-source dependency")
    if policy.get("runtime_dependency_guard") != {
        "forbid_project_source_dependency": True,
        "forbid_file_library_dependency": True,
        "forbid_knowledge_workbench_chat_reads": True,
        "require_compiled_knowledge_cards": True,
    }:
        raise TrainingError("model runtime dependency guard is incomplete")
    return policy


def _validate_method_execution_gates(
    root: Path,
    model_runtime_policy: dict[str, Any] | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if model_runtime_policy is None:
        raise TrainingError("model runtime policy is required for method gates")
    reasoning_path = model_runtime_policy.get("reasoning_core")
    route_path = model_runtime_policy.get("knowledge_route_map")
    if not isinstance(reasoning_path, str) or not isinstance(route_path, str):
        raise TrainingError("model runtime method paths are missing")
    reasoning_core = load_json(root / reasoning_path)
    route_map = load_json(root / route_path)
    gates = reasoning_core.get("method_gates")
    if not isinstance(gates, dict) or set(gates) != REQUIRED_METHOD_GATES:
        raise TrainingError("reasoning core method gates are incomplete")
    for gate_id, gate in gates.items():
        if (
            not isinstance(gate, dict)
            or set(gate) != {"required_checks", "fail_closed_when", "rule"}
            or not isinstance(gate["required_checks"], list)
            or not gate["required_checks"]
            or len(gate["required_checks"]) != len(set(gate["required_checks"]))
            or not isinstance(gate["fail_closed_when"], list)
            or not gate["fail_closed_when"]
            or len(gate["fail_closed_when"]) != len(set(gate["fail_closed_when"]))
            or not isinstance(gate["rule"], str)
            or not gate["rule"].strip()
        ):
            raise TrainingError(f"invalid reasoning method gate: {gate_id}")
        required_checks = REQUIRED_METHOD_GATE_CHECKS.get(gate_id, set())
        if not required_checks.issubset(set(gate["required_checks"])):
            raise TrainingError(
                f"reasoning method gate lacks mandatory checks: {gate_id}"
            )
    priority = reasoning_core.get("evidence_priority", [])
    try:
        specific_index = priority.index("independent_event_specific_mechanism")
        general_index = priority.index("general_scene_or_tendency")
    except ValueError as exc:
        raise TrainingError("reasoning core lacks event-specific evidence priority") from exc
    if specific_index >= general_index:
        raise TrainingError("general evidence outranks event-specific evidence")
    route_gates = route_map.get("execution_gates")
    if not isinstance(route_gates, dict) or set(route_gates) != REQUIRED_ROUTE_GATES:
        raise TrainingError("knowledge route execution gates are incomplete")
    for gate_id, gate in route_gates.items():
        if (
            not isinstance(gate, dict)
            or set(gate) != {"route", "required_order", "limit"}
            or not isinstance(gate["route"], list)
            or not gate["route"]
            or not set(gate["route"]).issubset({f"S{index:02d}" for index in range(20)})
            or not isinstance(gate["required_order"], list)
            or not gate["required_order"]
            or not isinstance(gate["limit"], str)
            or not gate["limit"].strip()
        ):
            raise TrainingError(f"invalid knowledge route execution gate: {gate_id}")
        required_order = REQUIRED_ROUTE_GATE_ORDERS.get(gate_id)
        if required_order is not None and gate["required_order"] != required_order:
            raise TrainingError(
                f"knowledge route gate order is incomplete: {gate_id}"
            )
    return reasoning_core, route_map


def _validate_answer_policy(root: Path) -> dict[str, Any]:
    policy = load_json(root / "config" / "answer-policy.json")
    if policy.get("schema") != "PUBLIC-REPOSITORY-ANSWER-POLICY-V1":
        raise TrainingError("wrong public-repository answer policy schema")
    expected = {
        "repository_visibility": "PUBLIC",
        "private_answer_repository_required": False,
        "plaintext_answers_allowed": False,
        "encrypted_answer_envelopes_allowed": True,
        "decryption_keys_allowed": False,
        "answer_read_phase": "POST_FREEZE_ONLY",
    }
    for key, value in expected.items():
        if policy.get(key) != value:
            raise TrainingError(f"answer policy mismatch for {key}: expected {value!r}")
    return policy


def _check_answer_free(value: Any, location: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = key.lower()
            if lowered in FORBIDDEN_CASE_KEYS:
                raise TrainingError(f"answer-bearing key in case input: {location}.{key}")
            if "answer" in lowered and lowered not in ALLOWED_ANSWER_KEYS:
                raise TrainingError(f"suspicious answer key in case input: {location}.{key}")
            _check_answer_free(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _check_answer_free(child, f"{location}[{index}]")


def _validate_case(root: Path, case_id: str, relative_path: str) -> int:
    case = load_json(root / relative_path)
    if case.get("case_id") != case_id:
        raise TrainingError(f"case id mismatch in {relative_path}")
    if case.get("group_id") != "DEV-GROUP-002":
        raise TrainingError(f"unexpected group id in {relative_path}")
    if case.get("answer_isolation", {}).get("answer_payload_present") is not False:
        raise TrainingError(f"case does not declare answer isolation: {relative_path}")
    binding = case.get("binding", {})
    if binding.get("source_manifest") != "sources/canonical-manifest.json":
        raise TrainingError(f"case does not bind the Git canonical source lock: {relative_path}")
    if binding.get("training_policy") != "config/training-policy.json":
        raise TrainingError(f"case does not bind the training policy: {relative_path}")
    _check_answer_free(case)
    questions = case.get("questions", {}).get("parsed")
    if not isinstance(questions, list) or not questions:
        raise TrainingError(f"case has no parsed questions: {relative_path}")
    declared = case.get("questions", {}).get("question_count")
    if declared != len(questions):
        raise TrainingError(f"question count mismatch in {relative_path}")
    seen_questions: set[str] = set()
    for question in questions:
        question_id = question.get("question_id")
        if not isinstance(question_id, str) or question_id in seen_questions:
            raise TrainingError(f"invalid or duplicate question id in {relative_path}")
        seen_questions.add(question_id)
        options = question.get("options")
        if not isinstance(options, list) or len(options) < 2:
            raise TrainingError(f"question {question_id} needs at least two options")
        option_ids = [option.get("option_id") for option in options]
        if any(not isinstance(item, str) for item in option_ids) or len(set(option_ids)) != len(option_ids):
            raise TrainingError(f"invalid option ids for {case_id}/{question_id}")
    return len(questions)


def _validate_release_chain(root: Path, release_id: str, seen: set[str] | None = None) -> dict[str, Any]:
    if seen is None:
        seen = set()
    if release_id in seen:
        raise TrainingError(f"model release cycle detected at {release_id}")
    seen.add(release_id)
    release_path = root / "model-learning" / "releases" / f"{release_id}.json"
    release = load_json(release_path)
    if release.get("release_id") != release_id:
        raise TrainingError(f"model release id mismatch: {release_id}")
    if release.get("schema") != "MODEL-RELEASE-V1":
        raise TrainingError(f"wrong model release schema: {release_id}")
    if release.get("base_source_manifest") != "sources/canonical-manifest.json":
        raise TrainingError(f"model release has the wrong base source manifest: {release_id}")
    if release.get("training_process_authority") != "config/training-policy.json":
        raise TrainingError(f"model release has the wrong process authority: {release_id}")
    if release.get("canonical_sources_mutated") is not False:
        raise TrainingError(f"model release may not mutate canonical sources: {release_id}")
    patches = release.get("patches")
    if not isinstance(patches, list) or len(set(patches)) != len(patches):
        raise TrainingError(f"invalid patch list in model release: {release_id}")
    patch_root = (root / "model-learning" / "patches").resolve()
    for relative_path in patches:
        if not isinstance(relative_path, str):
            raise TrainingError(f"invalid patch path in model release: {release_id}")
        patch_path = (root / relative_path).resolve()
        if not is_within(patch_root, patch_path) or not patch_path.is_file():
            raise TrainingError(
                f"model release patch is missing or outside model-learning/patches: {relative_path}"
            )
        patch = load_json(patch_path)
        if patch.get("schema") not in {
            "MODEL-LEARNING-PATCH-V1",
            "MODEL-LEARNING-PATCH-V2",
            "MODEL-LEARNING-PATCH-V3",
        }:
            raise TrainingError(f"wrong model learning patch schema: {relative_path}")
        if patch.get("contains_case_answer_mapping") is not False:
            raise TrainingError(f"model learning patch is not answer-isolated: {relative_path}")
        if patch.get("modifies_canonical_source_files") is not False:
            raise TrainingError(f"model learning patch attempts to mutate canonical sources: {relative_path}")
        if patch.get("schema") == "MODEL-LEARNING-PATCH-V2":
            content = patch.get("content")
            if not isinstance(content, dict) or set(content) != {"learning_type", "rules"}:
                raise TrainingError(f"invalid V2 learning patch content: {relative_path}")
            rules = content.get("rules")
            if not isinstance(rules, list) or not rules:
                raise TrainingError(f"V2 learning patch contains no rules: {relative_path}")
            normalized = [validate_rule(root, rule) for rule in rules]
            if normalized != rules:
                raise TrainingError(f"V2 learning patch rules are not normalized: {relative_path}")
        if patch.get("schema") == "MODEL-LEARNING-PATCH-V3":
            content = patch.get("content")
            normalized = validate_learning_patch_v3(
                root,
                content,
                check_catalog_collisions=False,
            )
            if normalized != content:
                raise TrainingError(f"V3 learning patch is not normalized: {relative_path}")
    parent_id = release.get("parent_release")
    if parent_id is None:
        if release_id != "MODEL-BASELINE-001" or patches:
            raise TrainingError("only an empty MODEL-BASELINE-001 may be a root release")
    else:
        if not isinstance(parent_id, str):
            raise TrainingError(f"invalid parent model release: {release_id}")
        parent = _validate_release_chain(root, parent_id, seen)
        if not patches or patches[:-1] != parent["patches"]:
            raise TrainingError(f"model release must append exactly one patch: {release_id}")
        latest_patch = load_json(root / patches[-1])
        if release.get("latest_patch_sha256") != object_sha256(latest_patch):
            raise TrainingError(f"latest patch hash mismatch: {release_id}")
    return release


def _validate_state(root: Path, state: dict[str, Any], group: dict[str, Any]) -> None:
    if state.get("schema") != "GENERALIZATION-TRAINING-STATE-R2":
        raise TrainingError("wrong generalization training state schema")
    case_order = group["case_order"]
    index = state.get("current_case_index")
    if not isinstance(index, int) or index < 0 or index > len(case_order):
        raise TrainingError("invalid current_case_index")
    if state.get("first_blind_cases_closed") != index:
        raise TrainingError("first_blind_cases_closed must match the new-case cursor")
    streak = state.get("independent_pass_streak")
    if not isinstance(streak, int) or isinstance(streak, bool) or streak < 0:
        raise TrainingError("invalid independent first-blind pass streak")
    if state.get("required_consecutive_independent_passes") != REQUIRED_CONSECUTIVE_INDEPENDENT_PASSES:
        raise TrainingError("wrong independent first-blind pass gate")
    queue = state.get("spaced_replay_queue")
    if not isinstance(queue, list):
        raise TrainingError("spaced_replay_queue must be a list")
    queue_ids: list[str] = []
    for item in queue:
        if not isinstance(item, dict) or set(item) != {
            "case_id",
            "eligible_after_first_blind_count",
        }:
            raise TrainingError("invalid spaced replay queue item")
        case_id = item["case_id"]
        eligible = item["eligible_after_first_blind_count"]
        if case_id not in group["cases"] or not isinstance(eligible, int) or eligible < 1:
            raise TrainingError("invalid spaced replay target")
        queue_ids.append(case_id)
    if len(queue_ids) != len(set(queue_ids)):
        raise TrainingError("duplicate case in spaced replay queue")
    active_replay = state.get("active_replay_case_id")
    if active_replay is not None and active_replay not in queue_ids:
        raise TrainingError("active replay case is absent from the replay queue")
    if state.get("status") == "GROUP_COMPLETE":
        if index != len(case_order) or queue:
            raise TrainingError("GROUP_COMPLETE requires all first blinds and replays to be closed")
    elif state.get("status") == "FIRST_BLIND_COMPLETE_REPLAY_PENDING":
        if index != len(case_order) or not queue or active_replay is not None:
            raise TrainingError("invalid replay-pending terminal state")
    elif index >= len(case_order) and active_replay is None:
        raise TrainingError("non-terminal state must have a new case or active replay")
    rounds: list[str] = []
    for case_position, case_id in enumerate(case_order):
        case_state = state["cases"][case_id]
        if not isinstance(case_state.get("round_ids"), list):
            raise TrainingError(f"invalid round list for {case_id}")
        first_blind = case_state.get("first_blind_round_id")
        if first_blind is not None and (
            not isinstance(first_blind, str) or first_blind not in case_state["round_ids"]
        ):
            raise TrainingError(f"invalid first-blind round for {case_id}")
        replays = case_state.get("replay_round_ids")
        if not isinstance(replays, list) or len(replays) != len(set(replays)):
            raise TrainingError(f"invalid replay list for {case_id}")
        if any(round_id not in case_state["round_ids"] or round_id == first_blind for round_id in replays):
            raise TrainingError(f"replay list does not match case rounds for {case_id}")
        if set(case_state["round_ids"]) != ({first_blind} if first_blind else set()) | set(replays):
            raise TrainingError(f"every case round must be classified as first-blind or replay: {case_id}")
        expected_status = "PENDING"
        if case_position < index:
            expected_status = "FIRST_BLIND_CLOSED"
        elif (
            case_position == index
            and index < len(case_order)
            and active_replay is None
        ):
            expected_status = "LEARNING_PENDING" if state.get("status") == "LEARNING_REQUIRED" else "ACTIVE"
        if case_id == active_replay:
            expected_status = "LEARNING_PENDING" if state.get("status") == "LEARNING_REQUIRED" else "REPLAY_ACTIVE"
        if case_state.get("status") != expected_status:
            raise TrainingError(
                f"case status mismatch for {case_id}: expected {expected_status}"
            )
        if case_position < index and first_blind is None:
            raise TrainingError(f"completed case lacks a first-blind round: {case_id}")
        if case_position > index and first_blind is not None:
            raise TrainingError(f"pending case already has a first-blind round: {case_id}")
        if case_position < index and not isinstance(case_state.get("first_blind_passed"), bool):
            raise TrainingError(f"closed case lacks a first-blind result: {case_id}")
        if case_id in queue_ids and case_state.get("remediation_status") != "QUEUED":
            raise TrainingError(f"queued case lacks remediation status: {case_id}")
        rounds.extend(case_state["round_ids"])
    if len(rounds) != len(set(rounds)):
        raise TrainingError("a round id appears more than once")
    if state.get("round_count") != len(rounds):
        raise TrainingError("round_count does not match the case round lists")
    non_executed_rounds = state.get("non_executed_rounds", [])
    if not isinstance(non_executed_rounds, list):
        raise TrainingError("non_executed_rounds must be a list")
    non_executed_ids: list[str] = []
    for record in non_executed_rounds:
        if not isinstance(record, dict) or set(record) != {
            "round_id",
            "case_id",
            "status",
            "prediction_frozen",
            "scored",
            "counts_toward_first_blind",
            "prediction_directions_retained",
            "reason",
            "recorded_at",
        }:
            raise TrainingError("invalid non-executed round record")
        if any(
            record.get(field) is not False
            for field in (
                "prediction_frozen",
                "scored",
                "counts_toward_first_blind",
                "prediction_directions_retained",
            )
        ):
            raise TrainingError("contaminated pre-freeze round retained training effects")
        reason = record.get("reason")
        if reason == "PREDICTION_CONTEXT_ALLOWLIST_VIOLATION":
            if record.get("status") != "PRE-FREEZE_CONTAMINATED_NOT_EXECUTED":
                raise TrainingError("contamination round has the wrong status")
            if record.get("case_id") in group["cases"]:
                raise TrainingError("quarantined case remains in the first-blind group")
        elif reason == (
            "PREDICTION_ACCESS_CONTRACT_NOT_EXECUTED_BEFORE_REPOSITORY_READ"
        ):
            if record.get("status") != "PRE-FREEZE_CONTAMINATED_NOT_EXECUTED":
                raise TrainingError("startup-order round has the wrong status")
            if record.get("case_id") not in group["cases"]:
                raise TrainingError("same-case invalidation removed the first-blind case")
        elif reason == "PREDICTION_CANONICAL_RUNTIME_READ_GATE_FAILURE":
            if (
                record.get("status")
                != "PRE-FREEZE_RUNTIME_GATE_FAILED_NOT_EXECUTED"
            ):
                raise TrainingError("runtime-gate round has the wrong status")
            if record.get("case_id") not in group["cases"]:
                raise TrainingError("runtime-gate failure removed the first-blind case")
        else:
            raise TrainingError("non-executed round has an unsupported reason")
        non_executed_ids.append(record.get("round_id"))
    if len(non_executed_ids) != len(set(non_executed_ids)):
        raise TrainingError("duplicate non-executed round id")
    if set(non_executed_ids) & set(rounds):
        raise TrainingError("non-executed round also appears as an executed round")
    round_sequence = state.get("round_sequence")
    if round_sequence is not None:
        if (
            not isinstance(round_sequence, int)
            or isinstance(round_sequence, bool)
            or round_sequence != len(rounds) + len(non_executed_rounds)
        ):
            raise TrainingError("round_sequence does not balance executed and non-executed rounds")
    for round_id in rounds:
        if not (root / "training" / "runs" / round_id / "round.json").is_file():
            raise TrainingError(f"state references a missing round: {round_id}")
    active_round = state.get("active_round_id")
    needs_active = state.get("status") in {"AWAITING_PREDICTION_FREEZE", "PREDICTION_FROZEN"}
    if needs_active != isinstance(active_round, str):
        raise TrainingError("active_round_id does not match the training status")
    if isinstance(active_round, str) and active_round not in rounds:
        raise TrainingError("active_round_id is absent from the round lists")


def verify_repository(root: Path, *, require_answers: bool = False) -> dict[str, Any]:
    root = root.resolve()
    time_calendar = _validate_time_calendar_foundation(root)
    policy = load_and_validate_policy(root / "config" / "training-policy.json")
    prediction_tool_policy = load_prediction_tool_policy(root)
    post_handoff_policy = load_post_prediction_handoff_policy(root)
    taxonomy = load_taxonomy(root)
    source_policy = _validate_source_policy(root)
    model_runtime_policy = _validate_model_runtime_policy(root)
    if model_runtime_policy is not None:
        reasoning_core, knowledge_route_map = _validate_method_execution_gates(
            root,
            model_runtime_policy,
        )
    else:
        reasoning_core, knowledge_route_map = None, None
    _validate_answer_policy(root)
    expected_manifest = build_source_manifest(root)
    manifest = load_json(root / "sources" / "canonical-manifest.json")
    if source_policy["canonical_manifest_sha256"] != object_sha256(manifest):
        raise TrainingError("canonical source manifest lock hash changed")
    if manifest != expected_manifest:
        raise TrainingError(
            "canonical S00-S19 changed or sources/canonical-manifest.json is not the frozen lock"
        )
    runtime_manifest = validate_canonical_runtime(root)
    if source_policy["canonical_runtime_manifest_sha256"] != object_sha256(
        runtime_manifest
    ):
        raise TrainingError("canonical runtime manifest lock hash changed")
    source_access = None
    if (root / DERIVED_ACCESS_ROOT).exists():
        source_access = validate_source_access(root, require_source_commit=False)
    classical_relation_evidence = None
    if (root / CLASSICAL_RELATION_EVIDENCE_MATRIX_PATH).exists():
        classical_relation_evidence = validate_classical_relation_evidence(root)
    five_combination_evidence_binding = None
    if (root / FIVE_COMBINATION_EVIDENCE_BINDINGS_PATH).exists():
        five_combination_evidence_binding = validate_five_combination_evidence_bindings(root)
    classical_relation_interaction_assertion = None
    if (root / CLASSICAL_RELATION_INTERACTION_ASSERTION_MATRIX_PATH).exists():
        classical_relation_interaction_assertion = (
            validate_classical_relation_interaction_assertion_matrix(root)
        )

    legacy_group = load_json(root / "examples" / "DEV-GROUP-002" / "group.json")
    legacy_case_order = legacy_group.get("case_order")
    legacy_cases = legacy_group.get("cases")
    if (
        not isinstance(legacy_case_order, list)
        or not legacy_case_order
        or len(set(legacy_case_order)) != len(legacy_case_order)
    ):
        raise TrainingError("the training group must contain one or more uniquely ordered cases")
    if not isinstance(legacy_cases, dict) or set(legacy_cases) != set(legacy_case_order):
        raise TrainingError("group case mapping does not match case order")
    legacy_question_counts = {
        case_id: _validate_case(root, case_id, legacy_cases[case_id])
        for case_id in legacy_case_order
    }

    release = load_json(root / "model-learning" / "releases" / "MODEL-BASELINE-001.json")
    if release.get("patches") != [] or release.get("parent_release") is not None:
        raise TrainingError("baseline model release must not contain learning patches")

    state = load_json(root / "training" / "state.json")
    dataset_manifest_path = state.get("dataset_manifest_path")
    if dataset_manifest_path is None:
        case_bank = {
            "status": "NOT_BOUND",
            "reason": "training state does not declare a dataset manifest",
        }
    else:
        if dataset_manifest_path != "case-bank/manifest.json":
            raise TrainingError("training state points to an unsupported dataset manifest")
        case_bank = validate_case_bank(root)
    group_path = state.get("group_path")
    if not isinstance(group_path, str):
        raise TrainingError("training state has no group path")
    group = load_json(root / group_path)
    case_order = group.get("case_order")
    cases = group.get("cases")
    if not isinstance(case_order, list) or not case_order or len(set(case_order)) != len(case_order):
        raise TrainingError("active training group must contain uniquely ordered cases")
    if not isinstance(cases, dict) or set(cases) != set(case_order):
        raise TrainingError("active group case mapping does not match case order")
    if state.get("mode") == "FORMAL_CASE_BANK":
        development = load_json(root / "case-bank" / "partitions" / "development.json")
        expected_order = development.get("first_blind_schedule")
        expected_cases = {
            case_id: development["cases"][case_id]
            for case_id in expected_order
        }
        if (
            group.get("group_id") != "FORMAL-DEVELOPMENT-001"
            or group.get("partition_id") != "DEVELOPMENT"
            or case_order != expected_order
            or cases != expected_cases
        ):
            raise TrainingError("formal controller group does not match the development first-blind schedule")
        question_counts = {
            case_id: load_json(root / cases[case_id])["questions"]["question_count"]
            for case_id in case_order
        }
    else:
        if group_path != "examples/DEV-GROUP-002/group.json" or group != legacy_group:
            raise TrainingError("pre-formal state must remain bound to the migration group")
        question_counts = legacy_question_counts
    if state.get("group_id") != group.get("group_id"):
        raise TrainingError("training state group mismatch")
    if state.get("round_limit") is not None or policy.get("round_limit") is not None:
        raise TrainingError("training rounds must be unlimited")
    if state.get("source_manifest_path") != "sources/canonical-manifest.json":
        raise TrainingError("training state must bind the frozen Git canonical manifest")
    current_release = state.get("current_model_release")
    if not isinstance(current_release, str) or not (
        root / "model-learning" / "releases" / f"{current_release}.json"
    ).is_file():
        raise TrainingError("training state points to a missing model release")
    if (
        state.get("round_count") == 0
        and state.get("mode") != "FORMAL_CASE_BANK"
        and current_release != "MODEL-BASELINE-001"
    ):
        raise TrainingError("an unused clean state must begin at MODEL-BASELINE-001")
    if set(state.get("cases", {})) != set(case_order):
        raise TrainingError("training state case set mismatch")
    _validate_state(root, state, group)
    current_release_record = _validate_release_chain(root, current_release)
    rule_catalog = load_rule_catalog(root, current_release_record)
    ledger = load_json(root / LEDGER_RELATIVE_PATH)
    validate_learning_ledger(root, ledger, current_release_record)
    maintenance = validate_maintenance(root, rule_catalog)

    chat_input_path = root / CHAT_INPUT_RELATIVE_PATH
    chat_input = load_json(chat_input_path)
    if chat_input != compose_chat_input(root):
        raise TrainingError("chat-input/current.json is stale or contains non-current material")
    if chat_input.get("prediction_access_contract") != build_prediction_access_contract(
        root, state
    ):
        raise TrainingError("chat prediction access contract is stale or not fail-closed")
    bootstrap_contract = load_json(root / PREDICTION_ACCESS_CONTRACT_PATH)
    validate_prediction_access_contract(bootstrap_contract)
    if bootstrap_contract != chat_input["prediction_access_contract"]:
        raise TrainingError(
            "standalone prediction access contract does not match Chat input"
        )
    handoff_contract = chat_input.get("chat_work_handoff_contract", {})
    serialization = handoff_contract.get("serialization_constraints", {})
    if (
        chat_input.get("post_prediction_handoff_policy")
        != post_handoff_policy
        or serialization.get("chat_local_preflight_required") is not False
        or serialization.get("chat_required_capabilities")
        != ["GITHUB_FETCH_FILE", "GITHUB_CREATE_ISSUE"]
        or serialization.get("normalization_authority")
        != "GITHUB_CONTROLLER"
        or serialization.get("controller_validation_workflow")
        != post_handoff_policy["controller_workflow"]
    ):
        raise TrainingError(
            "Chat handoff still depends on local preflight or bypasses the phase gate"
        )
    performance = chat_input.get("runtime_performance_contract")
    if (
        not isinstance(performance, dict)
        or performance.get("schema")
        != "CHAT-PREDICTION-RUNTIME-PERFORMANCE-V1"
        or set(performance.get("non_negotiable_reasoning_themes", []))
        != REQUIRED_REASONING_THEMES
        or performance.get("retrieval", {}).get("evidence_quota")
        is not None
        or performance.get("comparison_representation", {}).get(
            "all_pairs_required"
        )
        is not True
    ):
        raise TrainingError("Chat runtime performance policy weakens reasoning coverage")
    budgets = performance.get("budgets", {})
    current_input_characters = len(chat_input_path.read_text(encoding="utf-8"))
    if current_input_characters > budgets.get("current_input_max_characters", 0):
        raise TrainingError("chat-input/current.json exceeds its runtime budget")
    runtime_model_ref = chat_input.get("current_model", {}).get(
        "compiled_runtime_model_ref"
    )
    if (
        not isinstance(runtime_model_ref, dict)
        or runtime_model_ref.get("path")
        != CHAT_RUNTIME_MODEL_RELATIVE_PATH.as_posix()
    ):
        raise TrainingError("compiled Chat runtime model reference is invalid")
    runtime_model_path = root / CHAT_RUNTIME_MODEL_RELATIVE_PATH
    runtime_model = load_json(runtime_model_path)
    if (
        object_sha256(runtime_model) != runtime_model_ref.get("sha256")
        or runtime_model.get("release_id") != current_release
        or runtime_model.get("predictive_content_omitted") is not False
        or runtime_model.get("reasoning_core") != compact_reasoning_core(reasoning_core)
        or (
            knowledge_route_map is not None
            and runtime_model.get("knowledge_route_map", {}).get(
                "execution_gates"
            )
            != knowledge_route_map["execution_gates"]
        )
    ):
        raise TrainingError("compiled Chat runtime model is stale or incomplete")
    if model_runtime_policy is not None:
        cards = model_runtime_policy["knowledge_cards"]
        if (
            runtime_model.get("knowledge_card_runtime_authority")
            != cards["compiled_runtime_ref"]
            or runtime_model.get("knowledge_workbench_chat_read_allowed")
            is not False
        ):
            raise TrainingError(
                "compiled runtime model does not own Chat knowledge-card access"
            )
    if runtime_model.get("post_prediction_handoff") != {
        "phase": post_handoff_policy["phase"],
        "allowed_tool_classes": post_handoff_policy[
            "allowed_tool_classes"
        ],
        "allowed_issue_count_per_round": 1,
        "transition_requirements": post_handoff_policy[
            "transition_requirements"
        ],
        "normalization_authority": "GITHUB_CONTROLLER",
        "chat_local_preflight_required": False,
        "all_other_git_writes": "DENY",
    }:
        raise TrainingError("compiled runtime model has an invalid handoff phase")
    runtime_model_characters = len(runtime_model_path.read_text(encoding="utf-8"))
    if runtime_model_characters > budgets.get(
        "compiled_runtime_model_max_characters",
        0,
    ):
        raise TrainingError("compiled Chat runtime model exceeds its runtime budget")
    template_ref = chat_input.get("chat_work_handoff_contract", {}).get(
        "prediction_row_template_ref"
    )
    if (
        not isinstance(template_ref, dict)
        or template_ref.get("path")
        != PREDICTION_ROW_TEMPLATE_RELATIVE_PATH.as_posix()
        or object_sha256(load_json(root / PREDICTION_ROW_TEMPLATE_RELATIVE_PATH))
        != template_ref.get("sha256")
    ):
        raise TrainingError("prediction row template reference is stale")
    question_ids = {
        question["question_id"]
        for question in (chat_input.get("current_case") or {})
        .get("questions", {})
        .get("parsed", [])
    }
    execution_routes = chat_input.get("current_model", {}).get(
        "question_execution_routes",
        [],
    )
    if (
        {route.get("question_id") for route in execution_routes}
        != question_ids
        or any(
            route.get("retrieval_mode")
            != "ANCHOR_FIRST_PROGRESSIVE_EXPANSION"
            for route in execution_routes
        )
    ):
        raise TrainingError("question execution routes are incomplete")
    runtime_rule_ids = {row["rule_id"] for row in runtime_model["active_rules"]}
    runtime_card_ids = {
        row["card_id"] for row in runtime_model["knowledge_cards"]
    }
    for route in execution_routes:
        if not set(route["decisive_or_supporting_rule_ids"]).issubset(
            runtime_rule_ids
        ) or not set(route["counterevidence_rule_ids"]).issubset(
            runtime_rule_ids
        ):
            raise TrainingError("question execution route references an absent rule")
        if not set(route["knowledge_card_ids"]).issubset(runtime_card_ids):
            raise TrainingError("question execution route references an absent card")

    encrypted_dir = root / "answer-vault" / "encrypted"
    legacy_answer_count = sum(
        (encrypted_dir / f"{case_id}.json.fernet").is_file()
        for case_id in case_order
    )
    if dataset_manifest_path is None:
        answer_count = legacy_answer_count
        answer_required = len(case_order)
    else:
        dataset_manifest = load_json(root / dataset_manifest_path)
        dataset_case_ids = set().union(
            *(
                set(case_ids)
                for case_ids in dataset_manifest.get("partitions", {}).values()
            )
        )
        formal_dir = root / "answer-vault" / "formal"
        formal_manifest_path = formal_dir / "manifest.json"
        if formal_dir.exists():
            formal_manifest = load_json(formal_manifest_path)
            expected_hashes = formal_manifest.get("envelope_hashes")
            if (
                formal_manifest.get("schema") != "FORMAL-ANSWER-VAULT-MANIFEST-V1"
                or formal_manifest.get("answer_batch_schema") != "FORTUNE-ANSWER-BATCH-V2"
                or formal_manifest.get("corpus_id") != dataset_manifest.get("corpus_id")
                or formal_manifest.get("case_count") != len(dataset_case_ids)
                or formal_manifest.get("question_count")
                != dataset_manifest.get("question_count")
                or not isinstance(formal_manifest.get("scoreable_question_count"), int)
                or not isinstance(formal_manifest.get("unscored_question_count"), int)
                or formal_manifest["scoreable_question_count"]
                + formal_manifest["unscored_question_count"]
                != formal_manifest["question_count"]
                or not isinstance(expected_hashes, dict)
                or set(expected_hashes) != dataset_case_ids
                or formal_manifest.get("plaintext_stored_in_repository") is not False
                or formal_manifest.get("answer_read_phase") != "POST_FREEZE_ONLY"
            ):
                raise TrainingError("formal answer-vault manifest is invalid")
            actual_files = {
                path.name.removesuffix(".json.fernet")
                for path in formal_dir.glob("CASE-*.json.fernet")
            }
            if actual_files != dataset_case_ids:
                raise TrainingError("formal answer-vault files do not match the 107-case corpus")
            for case_id, expected_hash in expected_hashes.items():
                if sha256_file(formal_dir / f"{case_id}.json.fernet") != expected_hash:
                    raise TrainingError(f"formal answer envelope hash mismatch: {case_id}")
            answer_count = len(actual_files)
        else:
            answer_count = 0
        answer_required = len(dataset_case_ids)
    if require_answers and answer_count != answer_required:
        raise TrainingError(
            f"formal training requires {answer_required} encrypted answers; found {answer_count}"
        )

    return {
        "status": "PASS",
        "sources": expected_manifest["source_count"],
        "runtime_source": "GIT_REPOSITORY_ONLY",
        "canonical_sources_immutable": True,
        "canonical_source_access": source_access,
        "classical_relation_lifecycle_evidence": classical_relation_evidence,
        "five_combination_evidence_binding": five_combination_evidence_binding,
        "classical_relation_interaction_assertion": classical_relation_interaction_assertion,
        "model_learning_separate": True,
        "cases": case_bank.get("cases", len(case_order)),
        "questions": case_bank.get("questions", sum(question_counts.values())),
        "case_bank": case_bank,
        "legacy_controller_group": {
            "cases": len(legacy_case_order),
            "questions": sum(legacy_question_counts.values()),
            "answer_envelopes": legacy_answer_count,
            "role": "MIGRATION_HISTORY_UNTIL_CASE_BANK_ACTIVATION",
        },
        "active_controller_group": {
            "group_id": group["group_id"],
            "cases": len(case_order),
            "questions": sum(question_counts.values()),
            "mode": state.get("mode", "LEGACY_MIGRATION"),
        },
        "answer_envelopes": answer_count,
        "answer_envelopes_required": answer_required,
        "preloaded_encrypted_answers_ready": answer_count == answer_required,
        "external_post_freeze_answer_supported": True,
        "controller_ready": True,
        "chat_input_ready": True,
        "prediction_tool_policy": prediction_tool_policy["schema"],
        "question_taxonomy_ready": taxonomy["schema"] == "QUESTION-REASONING-TAXONOMY-V2",
        "knowledge_cards_ready": chat_input["current_model"]["knowledge_cards"]["card_count"] >= 23,
        "post_prediction_handoff_policy": post_handoff_policy["phase"],
        "knowledge_card_count": chat_input["current_model"]["knowledge_cards"]["card_count"],
        "chat_runtime": {
            "current_input_characters": current_input_characters,
            "compiled_runtime_model_characters": runtime_model_characters,
            "current_input_budget": budgets["current_input_max_characters"],
            "compiled_runtime_model_budget": budgets[
                "compiled_runtime_model_max_characters"
            ],
            "reasoning_theme_count": len(REQUIRED_REASONING_THEMES),
            "all_prediction_themes_preserved": True,
            "evidence_quota": None,
        },
        "learning_ledger_ready": True,
        "maintenance_ready": True,
        "maintenance": maintenance,
        "time_calendar_foundation": time_calendar,
        "training_unit": "FIRST_BLIND_CASE_WITH_SPACED_REPLAY",
        "required_consecutive_independent_passes": REQUIRED_CONSECUTIVE_INDEPENDENT_PASSES,
        "same_case_replays_count_toward_stage_gate": False,
        "round_limit": None,
        "first_blind_cases_scored": ledger["first_blind_totals"]["cases"],
        "first_blind_questions_scored": ledger["first_blind_totals"]["questions"],
    }
