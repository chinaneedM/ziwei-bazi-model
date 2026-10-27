from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class ClassicalSemanticClosureGovernanceRow:
    closure_requirement_id: str
    runtime_dependency_status: str
    governance_class: str
    future_owner: str
    upstream_support_class: str
    upstream_support_reference_ids: tuple[str, ...]


@dataclass(frozen=True)
class ClassicalMechanismProposalGovernance:
    mechanism_proposal_id: str
    source_semantic_candidate_id: str
    source_semantic_projection_envelope_id: str
    source_semantic_projection_fact_hash: str
    source_semantic_projection_computation_hash: str
    source_fragment_semantic_projection_id: str
    source_fragment_id: str
    source_fragment_fact_hash: str
    source_fragment_computation_hash: str
    binding_candidate_id: str
    source_occurrence_id: str
    graph_record_id: str
    interaction_assertion_id: str
    source_claim_edge_id: str
    target_exact_relation_id: str
    effect_facet: str
    semantic_candidate_kind: str
    mechanism_proposal_kind: str
    unresolved_classical_semantic_requirements: tuple[str, ...]
    closure_governance_rows: tuple[ClassicalSemanticClosureGovernanceRow, ...]
    source_unresolved_graph_requirements_provenance: tuple[str, ...]
    source_narrative_chain_ids_provenance: tuple[str, ...]
    source_semantic_profile_id: str
    source_semantic_partition_id: str
    mechanism_proposal_semantics: str = "SOURCE_GROUNDED_IDENTITY_ONLY"
    mechanism_execution_semantics: str = "NOT_RELEASED"
    rewrite_application_semantics: str = "NOT_RELEASED"


@dataclass(frozen=True)
class ClassicalFragmentMechanismClosureGovernanceProjection:
    fragment_governance_projection_id: str
    source_fragment_semantic_projection_id: str
    source_fragment_id: str
    source_occurrence_id: str
    binding_candidate_id: str
    source_projection_status: str
    governance_status: str
    source_semantic_candidate_ids: tuple[str, ...]
    mechanism_proposals: tuple[ClassicalMechanismProposalGovernance, ...]
    source_unresolved_graph_requirements_provenance: tuple[str, ...]
    unresolved_classical_semantic_requirements: tuple[str, ...]


@dataclass(frozen=True)
class SourceRecordMechanismClosureGovernanceSet:
    source_record_candidate_set_id: str
    source_layer: str
    source_occurrence_id: str
    source_fragment_ids: tuple[str, ...]
    fragment_governance_projection_ids: tuple[str, ...]
    mechanism_proposal_ids: tuple[str, ...]
    member_selection_semantics: str = "NOT_RELEASED"
    member_coexistence_semantics: str = "NOT_RELEASED"
    member_exclusivity_semantics: str = "NOT_RELEASED"
    proposal_priority_semantics: str = "NOT_RELEASED"
    proposal_conflict_semantics: str = "NOT_RELEASED"


@dataclass(frozen=True)
class ClosureRequirementGovernanceIndexEntry:
    closure_requirement_id: str
    runtime_dependency_status: str
    mechanism_proposal_ids: tuple[str, ...]
    index_semantics: str = "AUDIT_IDENTITY_ONLY_NO_INFERENCE"


@dataclass(frozen=True)
class MechanismProposalGovernanceIndexEntry:
    mechanism_proposal_kind: str
    mechanism_proposal_ids: tuple[str, ...]
    index_semantics: str = "AUDIT_IDENTITY_ONLY_NO_INFERENCE"


@dataclass(frozen=True)
class MechanismClosureIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class MechanismClosureIntegrityReport:
    status: str
    diagnostics: tuple[MechanismClosureIntegrityDiagnostic, ...]
    algorithm_id: str = "BAZI-CLASSICAL-SEMANTIC-MECHANISM-CLOSURE-INTEGRITY-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class MechanismClosureHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-CLASSICAL-SEMANTIC-MECHANISM-CLOSURE-HASH-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class ClassicalSemanticMechanismClosureGovernanceEnvelope:
    mechanism_closure_envelope_id: str
    source_semantic_projection_envelope_id: str
    source_semantic_projection_fact_hash: str
    source_semantic_projection_computation_hash: str
    source_admission_envelope_id: str
    source_effect_envelope_id: str
    lineage_binding_keys: tuple[str, ...]
    fragment_governance_projections: tuple[ClassicalFragmentMechanismClosureGovernanceProjection, ...]
    source_record_candidate_sets: tuple[SourceRecordMechanismClosureGovernanceSet, ...]
    closure_requirement_index: tuple[ClosureRequirementGovernanceIndexEntry, ...]
    mechanism_proposal_index: tuple[MechanismProposalGovernanceIndexEntry, ...]
    projected_mechanism_proposal_ids: tuple[str, ...]
    mechanism_proposal_semantics: str
    mechanism_execution_semantics: str
    rewrite_application_semantics: str
    candidate_truth_semantics: str
    candidate_applicability_semantics: str
    candidate_coexistence_semantics: str
    candidate_exclusivity_semantics: str
    candidate_conflict_semantics: str
    precedence_semantics: str
    priority_semantics: str
    winner_loser_semantics: str
    state_transition_semantics: str
    lifecycle_truth_gate: str
    fragment_selection_semantics: str
    cross_outer_composition: str
    cartesian_expansion: str
    raw_relation_immutability_contract: str
    algorithm_versions: Mapping[str, str]
    integrity: MechanismClosureIntegrityReport
    hashes: MechanismClosureHashBundle


@dataclass(frozen=True)
class BaziClassicalSemanticMechanismClosureGovernanceResolution:
    schema: str
    status: str
    candidates: tuple[ClassicalSemanticMechanismClosureGovernanceEnvelope, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
