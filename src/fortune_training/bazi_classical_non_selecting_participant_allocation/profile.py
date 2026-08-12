from __future__ import annotations

from dataclasses import dataclass


PROFILE_ID = "BAZI-CLASSICAL-NON-SELECTING-PARTICIPANT-ALLOCATION-R1"
PROFILE_VERSION = "1.0.0"
ALGORITHM_ID = PROFILE_ID
ALGORITHM_VERSION = "1.0.0"

ALLOCATION_SEMANTIC_CANDIDATE_KIND = "SOURCE_GROUNDED_PARTICIPANT_ALLOCATION_CANDIDATE"
ALLOCATION_MECHANISM_PROPOSAL_KIND = "PARTICIPANT_ALLOCATION_MECHANISM_PROPOSAL"

ALLOCATION_DOMAIN_CLASSIFICATIONS = (
    "EXACT_INSTANCE_SET_CARDINALITY_MATCH",
    "EXACT_INSTANCE_POOL_REQUIRES_COMPATIBILITY_RELATION",
    "INSUFFICIENT_EXACT_INSTANCE_CARDINALITY",
)
PATH_CANDIDATE_KIND = "UNORDERED_EXACT_INSTANCE_SET_PATH_CANDIDATE"
DOMAIN_BLOCKER_IDS = (
    "SLOT_INSTANCE_COMPATIBILITY_RELATION_NOT_RELEASED",
    "SYNTHETIC_COMBINATORIAL_ENUMERATION_FORBIDDEN",
    "INSUFFICIENT_EXACT_RUNTIME_INSTANCE_CARDINALITY",
)
SLOT_EQUIVALENCE_VALUES = ("EXCHANGEABLE_SOURCE_EQUIVALENT",)
ALTERNATIVE_PATH_REQUIREMENT = "PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS"

EXPECTED_ALLOCATION_CLOSURE_ROWS = {
    "CLASSICAL_PARTICIPANT_ALLOCATION": "MISSING_PRIMITIVE",
    "COMPATIBLE_EXACT_INSTANCE_PATH_ENUMERATION": "PARTIALLY_AVAILABLE",
}

FRAGMENT_ALLOCATION_STATUSES = (
    "ALLOCATION_DOMAIN_ELABORATION_PROJECTED",
    "PRESERVED_NO_ALLOCATION_DOMAINS",
    "PRESERVED_ZERO_PROPOSALS_NO_ALLOCATION_DOMAINS",
)


@dataclass(frozen=True)
class ClassicalNonSelectingParticipantAllocationProfile:
    profile_id: str = PROFILE_ID
    profile_version: str = PROFILE_VERSION
    algorithm_id: str = ALGORITHM_ID
    algorithm_version: str = ALGORITHM_VERSION
    path_candidate_semantics: str = "UPSTREAM_IDENTITY_CARDINALITY_ELABORATION_ONLY"
    slot_assignment_semantics: str = "NOT_RELEASED"
    path_ordering_semantics: str = "NOT_RELEASED"
    compatibility_semantics: str = "NOT_RELEASED_BEYOND_UPSTREAM_IDENTITY"
    participant_path_selection_semantics: str = "NOT_RELEASED"
    allocation_truth_semantics: str = "NOT_RELEASED"
    allocation_operability_semantics: str = "NOT_RELEASED"
    coexistence_semantics: str = "NOT_RELEASED"
    exclusivity_semantics: str = "NOT_RELEASED"
    precedence_semantics: str = "NOT_RELEASED"
    priority_semantics: str = "NOT_RELEASED"
    winner_loser_semantics: str = "NOT_RELEASED"
    relation_effect_state_semantics: str = "NOT_RELEASED"
    rewrite_application_semantics: str = "NOT_RELEASED"
    synthetic_permutation_generation: str = "FORBIDDEN"
    synthetic_combination_generation: str = "FORBIDDEN"
    inferred_slot_instance_compatibility: str = "FORBIDDEN"
    source_narrative_policy: str = "PROVENANCE_ONLY"
    source_unresolved_graph_requirement_policy: str = "PROVENANCE_ONLY"
    fragment_selection_semantics: str = "NOT_RELEASED"
    cross_outer_composition: str = "NOT_RELEASED"
    cartesian_expansion: str = "NOT_RELEASED"
    cross_source_composition: str = "NOT_RELEASED"
    raw_relation_immutability_contract: str = "IMMUTABLE_EXACT_REFERENCE_ONLY"

    def validate(self) -> "ClassicalNonSelectingParticipantAllocationProfile":
        if self != ClassicalNonSelectingParticipantAllocationProfile():
            raise ValueError(f"unsupported Unit 6 allocation profile: {self!r}")
        return self


def bazi_classical_non_selecting_participant_allocation_r1_profile(
) -> ClassicalNonSelectingParticipantAllocationProfile:
    return ClassicalNonSelectingParticipantAllocationProfile()
