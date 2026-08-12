from __future__ import annotations

from dataclasses import dataclass


PROFILE_ID = "BAZI-CLASSICAL-EFFECT-SEMANTIC-CANDIDATE-PROJECTION-R1"
PROFILE_VERSION = "1.0.0"
ALGORITHM_ID = "BAZI-CLASSICAL-EFFECT-SEMANTIC-CANDIDATE-PROJECTION-R1"
ALGORITHM_VERSION = "1.0.0"

SOURCE_CLAIM_TO_SEMANTIC_CANDIDATE = {
    "SOURCE_ASSERTED_RESOLUTION": (
        "RELATION_EFFECT_DISPOSITION",
        "SOURCE_GROUNDED_RESOLUTION_CANDIDATE",
    ),
    "SOURCE_ASSERTED_RESOLUTION_FAILURE": (
        "RELATION_EFFECT_DISPOSITION",
        "SOURCE_GROUNDED_RESOLUTION_FAILURE_CANDIDATE",
    ),
    "SOURCE_ASSERTED_REVERSAL_OR_REAPPEARANCE": (
        "RELATION_EFFECT_DISPOSITION",
        "SOURCE_GROUNDED_REVERSAL_OR_REAPPEARANCE_CANDIDATE",
    ),
    "SOURCE_ASSERTED_ATTENUATION": (
        "RELATION_EFFECT_GRADE",
        "SOURCE_GROUNDED_ATTENUATION_CANDIDATE",
    ),
    "SOURCE_ASSERTED_PARTICIPANT_ALLOCATION": (
        "RELATION_PARTICIPANT_ALLOCATION",
        "SOURCE_GROUNDED_PARTICIPANT_ALLOCATION_CANDIDATE",
    ),
}

SEMANTIC_CANDIDATE_KINDS = tuple(
    row[1] for row in SOURCE_CLAIM_TO_SEMANTIC_CANDIDATE.values()
)
FRAGMENT_PROJECTION_STATUSES = (
    "SEMANTIC_CANDIDATES_PROJECTED",
    "PRESERVED_NO_SEMANTIC_CANDIDATES",
    "PRESERVED_OUTSIDE_PROFILE_NO_SEMANTIC_CANDIDATES",
)


@dataclass(frozen=True)
class ClassicalEffectSemanticCandidateProjectionProfile:
    profile_id: str = PROFILE_ID
    profile_version: str = PROFILE_VERSION
    algorithm_id: str = ALGORITHM_ID
    algorithm_version: str = ALGORITHM_VERSION
    candidate_truth_semantics: str = "NOT_RELEASED"
    candidate_applicability_semantics: str = "NOT_RELEASED_BEYOND_UNIT3_ADMISSION"
    candidate_coexistence_semantics: str = "NOT_RELEASED"
    candidate_exclusivity_semantics: str = "NOT_RELEASED"
    candidate_priority_semantics: str = "NOT_RELEASED"
    candidate_conflict_semantics: str = "NOT_RELEASED"
    candidate_rewrite_semantics: str = "NOT_RELEASED"
    candidate_state_transition_semantics: str = "NOT_RELEASED"
    candidate_winner_loser_semantics: str = "NOT_RELEASED"
    raw_relation_immutability_contract: str = "IMMUTABLE_EXACT_REFERENCE_ONLY"
    source_narrative_semantics: str = "PROVENANCE_ORDER_ONLY"
    source_unresolved_graph_requirement_policy: str = "PROVENANCE_ONLY_NEVER_DIRECT_PREDICATE"
    unresolved_classical_requirement_policy: str = "PASS_THROUGH_UNSOLVED"
    participant_allocation_policy: str = "PRESERVE_UPSTREAM_MULTIPLICITY_NO_SELECTION"
    attenuation_grade_policy: str = "CANDIDATE_ONLY_NO_NUMERIC_GRADE"
    fragment_selection_semantics: str = "NOT_RELEASED"
    cross_outer_composition: str = "NOT_RELEASED"
    cartesian_expansion: str = "NOT_RELEASED"
    cross_source_composition: str = "NOT_RELEASED"

    def validate(self) -> "ClassicalEffectSemanticCandidateProjectionProfile":
        if self != ClassicalEffectSemanticCandidateProjectionProfile():
            raise ValueError(f"unsupported Unit 4 semantic candidate profile: {self!r}")
        return self


def bazi_classical_effect_semantic_candidate_projection_r1_profile(
) -> ClassicalEffectSemanticCandidateProjectionProfile:
    return ClassicalEffectSemanticCandidateProjectionProfile()
