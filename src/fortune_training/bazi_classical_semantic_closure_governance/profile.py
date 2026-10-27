from __future__ import annotations

from dataclasses import dataclass


PROFILE_ID = "BAZI-CLASSICAL-SEMANTIC-MECHANISM-CLOSURE-GOVERNANCE-R1"
PROFILE_VERSION = "1.0.0"
ALGORITHM_ID = "BAZI-CLASSICAL-SEMANTIC-MECHANISM-CLOSURE-GOVERNANCE-R1"
ALGORITHM_VERSION = "1.0.0"

RUNTIME_DEPENDENCY_STATUSES = (
    "AVAILABLE_EXACTLY",
    "AVAILABLE_AS_NEUTRAL_EVIDENCE_ONLY",
    "PARTIALLY_AVAILABLE",
    "MISSING_PRIMITIVE",
    "OUTSIDE_CURRENT_RELATION_REGISTRY",
    "SOURCE_SEMANTICS_AMBIGUOUS",
)

SEMANTIC_CANDIDATE_TO_MECHANISM_PROPOSAL = {
    "SOURCE_GROUNDED_RESOLUTION_CANDIDATE": "RESOLUTION_MECHANISM_PROPOSAL",
    "SOURCE_GROUNDED_RESOLUTION_FAILURE_CANDIDATE": "RESOLUTION_FAILURE_MECHANISM_PROPOSAL",
    "SOURCE_GROUNDED_REVERSAL_OR_REAPPEARANCE_CANDIDATE": "REVERSAL_OR_REAPPEARANCE_MECHANISM_PROPOSAL",
    "SOURCE_GROUNDED_ATTENUATION_CANDIDATE": "ATTENUATION_MECHANISM_PROPOSAL",
    "SOURCE_GROUNDED_PARTICIPANT_ALLOCATION_CANDIDATE": "PARTICIPANT_ALLOCATION_MECHANISM_PROPOSAL",
}

CLOSURE_REQUIREMENT_REGISTRY = {
    "CLASSICAL_RESOLUTION_SEMANTICS": {
        "runtime_dependency_status": "MISSING_PRIMITIVE",
        "governance_class": "SEMANTIC_EFFECT_DISPOSITION_CLOSURE",
        "future_owner": "FUTURE_EXECUTION_CAPABLE_SEMANTIC_REWRITE_OR_RESOLVER",
    },
    "CLASSICAL_RESOLUTION_FAILURE_SEMANTICS": {
        "runtime_dependency_status": "MISSING_PRIMITIVE",
        "governance_class": "SEMANTIC_EFFECT_DISPOSITION_CLOSURE",
        "future_owner": "FUTURE_EXECUTION_CAPABLE_SEMANTIC_REWRITE_OR_RESOLVER",
    },
    "CLASSICAL_REVERSAL_OR_REAPPEARANCE_SEMANTICS": {
        "runtime_dependency_status": "MISSING_PRIMITIVE",
        "governance_class": "SEMANTIC_EFFECT_DISPOSITION_CLOSURE",
        "future_owner": "FUTURE_EXECUTION_CAPABLE_SEMANTIC_REWRITE_OR_RESOLVER",
    },
    "CLASSICAL_INTERACTION_CHAIN_RESOLUTION": {
        "runtime_dependency_status": "MISSING_PRIMITIVE",
        "governance_class": "INTERACTION_CHAIN_SEMANTIC_CLOSURE",
        "future_owner": "FUTURE_EXECUTION_CAPABLE_SEMANTIC_REWRITE_OR_RESOLVER",
    },
    "CLASSICAL_ATTENUATION_GRADE": {
        "runtime_dependency_status": "MISSING_PRIMITIVE",
        "governance_class": "EFFECT_GRADE_SEMANTIC_CLOSURE",
        "future_owner": "FUTURE_EFFECT_GRADE_SEMANTICS",
    },
    "CLASSICAL_PARTICIPANT_ALLOCATION": {
        "runtime_dependency_status": "MISSING_PRIMITIVE",
        "governance_class": "PARTICIPANT_ALLOCATION_SEMANTIC_CLOSURE",
        "future_owner": "UNIT6_NON_SELECTING_ALLOCATION_ELABORATION",
    },
    "COMPATIBLE_EXACT_INSTANCE_PATH_ENUMERATION": {
        "runtime_dependency_status": "PARTIALLY_AVAILABLE",
        "governance_class": "PARTICIPANT_ALLOCATION_PATH_CLOSURE",
        "future_owner": "UNIT6_NON_SELECTING_ALLOCATION_ELABORATION",
    },
}

MECHANISM_PROPOSAL_KINDS = tuple(SEMANTIC_CANDIDATE_TO_MECHANISM_PROPOSAL.values())
CLOSURE_REQUIREMENT_IDS = tuple(CLOSURE_REQUIREMENT_REGISTRY)
FRAGMENT_GOVERNANCE_STATUSES = (
    "MECHANISM_CLOSURE_GOVERNANCE_PROJECTED",
    "PRESERVED_ZERO_MECHANISM_PROPOSALS",
    "PRESERVED_OUTSIDE_PROFILE_ZERO_MECHANISM_PROPOSALS",
)


@dataclass(frozen=True)
class ClassicalSemanticMechanismClosureGovernanceProfile:
    profile_id: str = PROFILE_ID
    profile_version: str = PROFILE_VERSION
    algorithm_id: str = ALGORITHM_ID
    algorithm_version: str = ALGORITHM_VERSION
    mechanism_proposal_semantics: str = "SOURCE_GROUNDED_IDENTITY_ONLY"
    mechanism_execution_semantics: str = "NOT_RELEASED"
    rewrite_application_semantics: str = "NOT_RELEASED"
    candidate_truth_semantics: str = "NOT_RELEASED"
    candidate_applicability_semantics: str = "NOT_RELEASED_BEYOND_UNIT3_ADMISSION"
    candidate_coexistence_semantics: str = "NOT_RELEASED"
    candidate_exclusivity_semantics: str = "NOT_RELEASED"
    candidate_conflict_semantics: str = "NOT_RELEASED"
    precedence_semantics: str = "NOT_RELEASED"
    priority_semantics: str = "NOT_RELEASED"
    winner_loser_semantics: str = "NOT_RELEASED"
    state_transition_semantics: str = "NOT_RELEASED"
    lifecycle_truth_gate: str = "NOT_RELEASED"
    source_unresolved_graph_requirement_policy: str = "PROVENANCE_ONLY_NEVER_CLOSURE_PREDICATE"
    source_narrative_policy: str = "PROVENANCE_ORDER_ONLY_NEVER_STATE_TRANSITION"
    candidate_specific_lifecycle_evidence_binding: str = "NOT_RELEASED"
    participant_path_selection_semantics: str = "NOT_RELEASED"
    attenuation_numeric_grade_semantics: str = "NOT_RELEASED"
    fragment_selection_semantics: str = "NOT_RELEASED"
    cross_outer_composition: str = "NOT_RELEASED"
    cartesian_expansion: str = "NOT_RELEASED"
    cross_source_composition: str = "NOT_RELEASED"
    raw_relation_immutability_contract: str = "IMMUTABLE_EXACT_REFERENCE_ONLY"

    def validate(self) -> "ClassicalSemanticMechanismClosureGovernanceProfile":
        if self != ClassicalSemanticMechanismClosureGovernanceProfile():
            raise ValueError(f"unsupported Unit 5 mechanism/closure profile: {self!r}")
        return self


def bazi_classical_semantic_mechanism_closure_governance_r1_profile(
) -> ClassicalSemanticMechanismClosureGovernanceProfile:
    return ClassicalSemanticMechanismClosureGovernanceProfile()
