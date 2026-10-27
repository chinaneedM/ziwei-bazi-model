from __future__ import annotations

from dataclasses import dataclass

from fortune_training.bazi_classical_semantic_closure_governance.profile import (
    SEMANTIC_CANDIDATE_TO_MECHANISM_PROPOSAL,
)


PROFILE_ID = "BAZI-CLASSICAL-FINAL-EFFECT-CANDIDATE-ENVELOPE-ASSEMBLY-R1"
PROFILE_VERSION = "1.0.0"
ALGORITHM_ID = PROFILE_ID
ALGORITHM_VERSION = "1.0.0"

FINAL_CANDIDATE_SEMANTICS = "SOURCE_GROUNDED_PRE_RESOLVER_ENVELOPE_ASSEMBLY_ONLY"
INDEX_SEMANTICS = "IDENTITY_ONLY_NO_MERGE_RANK_ARBITRATION_OR_SELECTION"
FRAGMENT_FINAL_STATUSES = (
    "FINAL_EFFECT_CANDIDATES_ASSEMBLED",
    "PRESERVED_ZERO_FINAL_EFFECT_CANDIDATES",
)

SEMANTIC_TO_MECHANISM = dict(SEMANTIC_CANDIDATE_TO_MECHANISM_PROPOSAL)


@dataclass(frozen=True)
class ClassicalFinalEffectCandidateEnvelopeProfile:
    profile_id: str = PROFILE_ID
    profile_version: str = PROFILE_VERSION
    algorithm_id: str = ALGORITHM_ID
    algorithm_version: str = ALGORITHM_VERSION
    final_candidate_semantics: str = FINAL_CANDIDATE_SEMANTICS
    candidate_truth_semantics: str = "NOT_RELEASED"
    candidate_operability_semantics: str = "NOT_RELEASED"
    candidate_applicability_semantics: str = "NOT_RELEASED_BEYOND_UNIT3_ADMISSION"
    mechanism_execution_semantics: str = "NOT_RELEASED"
    rewrite_application_semantics: str = "NOT_RELEASED"
    lifecycle_truth_gate: str = "NOT_RELEASED"
    candidate_coexistence_semantics: str = "NOT_RELEASED"
    candidate_exclusivity_semantics: str = "NOT_RELEASED"
    candidate_conflict_semantics: str = "NOT_RELEASED"
    precedence_semantics: str = "NOT_RELEASED"
    priority_semantics: str = "NOT_RELEASED"
    winner_loser_semantics: str = "NOT_RELEASED"
    participant_path_selection_semantics: str = "NOT_RELEASED"
    relation_effect_state_semantics: str = "NOT_RELEASED"
    graph_mutation_fixpoint_semantics: str = "NOT_RELEASED"
    execution_readiness_semantics: str = "NOT_RELEASED"
    synthetic_permutation_generation: str = "FORBIDDEN"
    synthetic_combination_generation: str = "FORBIDDEN"
    inferred_slot_instance_compatibility: str = "FORBIDDEN"
    source_narrative_policy: str = "PROVENANCE_ONLY"
    source_unresolved_graph_requirement_policy: str = "PROVENANCE_ONLY"
    fragment_selection_semantics: str = "NOT_RELEASED"
    cross_outer_composition: str = "NOT_RELEASED"
    cross_source_composition: str = "NOT_RELEASED"
    cartesian_expansion: str = "NOT_RELEASED"
    raw_relation_immutability_contract: str = "IMMUTABLE_EXACT_REFERENCE_ONLY"

    def validate(self) -> "ClassicalFinalEffectCandidateEnvelopeProfile":
        if self != ClassicalFinalEffectCandidateEnvelopeProfile():
            raise ValueError(f"unsupported Unit 7 final effect envelope profile: {self!r}")
        return self


def bazi_classical_final_effect_candidate_envelope_r1_profile(
) -> ClassicalFinalEffectCandidateEnvelopeProfile:
    return ClassicalFinalEffectCandidateEnvelopeProfile()
