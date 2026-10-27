from __future__ import annotations

from dataclasses import dataclass


PROFILE_ID = "BAZI-CLASSICAL-CANDIDATE-PRESERVING-RESOLUTION-EFFECT-DISPOSITION-R1"
PROFILE_VERSION = "1.0.0"
ALGORITHM_ID = PROFILE_ID
ALGORITHM_VERSION = "1.0.0"

HANDLED_SEMANTIC_CANDIDATE_KIND = "SOURCE_GROUNDED_RESOLUTION_CANDIDATE"
HANDLED_MECHANISM_PROPOSAL_KIND = "RESOLUTION_MECHANISM_PROPOSAL"
HANDLED_SOURCE_CLAIM_EDGE_CLASS = "SOURCE_ASSERTED_RESOLUTION"
HANDLED_EFFECT_FACET = "RELATION_EFFECT_DISPOSITION"
RESOLUTION_CLOSURE_REQUIREMENT_ID = "CLASSICAL_RESOLUTION_SEMANTICS"
EXPECTED_UPSTREAM_CLOSURE_STATUS = "MISSING_PRIMITIVE"
LOCAL_CLOSURE_RESULT = (
    "AVAILABLE_EXACTLY_AS_CANDIDATE_LOCAL_SOURCE_ASSERTED_EFFECT_DISPOSITION"
)
DISPOSITION_KIND = "SOURCE_ASSERTED_RESOLVED_EFFECT_DISPOSITION"
DISPOSITION_SEMANTIC_SCOPE = "CANDIDATE_LOCAL_SOURCE_ASSERTED_EFFECT_BRANCH_ONLY"
INDEX_SEMANTICS = "IDENTITY_ONLY_NO_MERGE_RANK_ARBITRATION_SELECTION_OR_GLOBAL_STATE"
FRAGMENT_PROJECTION_STATUSES = (
    "RESOLUTION_EFFECT_DISPOSITIONS_PROJECTED",
    "PRESERVED_NO_RESOLUTION_EFFECT_DISPOSITIONS",
    "PRESERVED_ZERO_CANDIDATES",
)
CANDIDATE_PROJECTION_STATUSES = (
    "RESOLUTION_EFFECT_DISPOSITION_PROJECTED",
    "PRESERVED_NON_RESOLUTION_CANDIDATE",
)


@dataclass(frozen=True)
class ClassicalResolutionEffectDispositionProfile:
    profile_id: str = PROFILE_ID
    profile_version: str = PROFILE_VERSION
    algorithm_id: str = ALGORITHM_ID
    algorithm_version: str = ALGORITHM_VERSION
    disposition_kind: str = DISPOSITION_KIND
    disposition_semantic_scope: str = DISPOSITION_SEMANTIC_SCOPE
    raw_relation_action: str = "NO_MUTATION"
    raw_relation_presence_semantics: str = "UNCHANGED"
    handled_semantic_candidate_kind: str = HANDLED_SEMANTIC_CANDIDATE_KIND
    handled_mechanism_proposal_kind: str = HANDLED_MECHANISM_PROPOSAL_KIND
    handled_source_claim_edge_class: str = HANDLED_SOURCE_CLAIM_EDGE_CLASS
    handled_effect_facet: str = HANDLED_EFFECT_FACET
    resolution_closure_requirement_id: str = RESOLUTION_CLOSURE_REQUIREMENT_ID
    expected_upstream_closure_status: str = EXPECTED_UPSTREAM_CLOSURE_STATUS
    local_closure_result: str = LOCAL_CLOSURE_RESULT
    candidate_global_truth_semantics: str = "NOT_RELEASED"
    global_operability_semantics: str = "NOT_RELEASED"
    candidate_selection_semantics: str = "NOT_RELEASED"
    candidate_coexistence_semantics: str = "NOT_RELEASED"
    candidate_exclusivity_semantics: str = "NOT_RELEASED"
    candidate_conflict_semantics: str = "NOT_RELEASED"
    precedence_semantics: str = "NOT_RELEASED"
    priority_semantics: str = "NOT_RELEASED"
    winner_loser_semantics: str = "NOT_RELEASED"
    global_relation_effect_state_semantics: str = "NOT_RELEASED"
    execution_readiness_semantics: str = "NOT_RELEASED"
    resolution_failure_semantics: str = "NOT_RELEASED"
    reversal_reappearance_semantics: str = "NOT_RELEASED"
    attenuation_grade_semantics: str = "NOT_RELEASED"
    participant_allocation_semantics: str = "NOT_RELEASED"
    participant_path_selection_semantics: str = "NOT_RELEASED"
    inferred_slot_instance_compatibility: str = "FORBIDDEN"
    source_narrative_execution: str = "FORBIDDEN"
    source_narrative_policy: str = "PROVENANCE_ONLY"
    source_unresolved_graph_requirement_policy: str = "PROVENANCE_ONLY"
    graph_mutation_fixpoint_semantics: str = "NOT_RELEASED"
    fragment_selection_semantics: str = "NOT_RELEASED"
    cross_outer_composition: str = "NOT_RELEASED"
    cross_source_composition: str = "NOT_RELEASED"
    cartesian_expansion: str = "NOT_RELEASED"
    final_classical_verdict_semantics: str = "NOT_RELEASED"
    raw_relation_immutability_contract: str = "IMMUTABLE_EXACT_REFERENCE_ONLY"

    def validate(self) -> "ClassicalResolutionEffectDispositionProfile":
        if self != ClassicalResolutionEffectDispositionProfile():
            raise ValueError(f"unsupported Unit 8 resolution effect disposition profile: {self!r}")
        return self


def bazi_classical_resolution_effect_disposition_r1_profile(
) -> ClassicalResolutionEffectDispositionProfile:
    return ClassicalResolutionEffectDispositionProfile()
