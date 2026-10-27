from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from fortune_training.bazi_classical_semantic_closure_governance.models import (
    ClassicalSemanticClosureGovernanceRow,
)


@dataclass(frozen=True)
class UnorderedExactInstanceSetPathCandidate:
    path_candidate_id: str
    path_candidate_kind: str
    source_semantic_candidate_id: str
    source_mechanism_proposal_id: str
    multiplicity_constraint_id: str
    exchangeable_symbolic_slot_node_ids: tuple[str, ...]
    exact_runtime_instance_ids: tuple[str, ...]
    required_symbolic_cardinality: int
    slot_equivalence: str
    path_candidate_semantics: str = "UPSTREAM_IDENTITY_CARDINALITY_ELABORATION_ONLY"
    slot_assignment_semantics: str = "NOT_RELEASED"
    path_ordering_semantics: str = "NOT_RELEASED"
    compatibility_semantics: str = "NOT_RELEASED_BEYOND_UPSTREAM_IDENTITY"
    selection_semantics: str = "NOT_RELEASED"


@dataclass(frozen=True)
class AllocationDomainObservation:
    allocation_domain_observation_id: str
    source_semantic_candidate_id: str
    source_mechanism_proposal_id: str
    source_occurrence_id: str
    binding_candidate_id: str
    graph_record_id: str
    interaction_assertion_id: str
    source_claim_edge_id: str
    target_exact_relation_id: str
    effect_facet: str
    multiplicity_constraint_id: str
    exchangeable_symbolic_slot_node_ids: tuple[str, ...]
    exact_runtime_instance_ids: tuple[str, ...]
    required_symbolic_cardinality: int
    slot_equivalence: str
    alternative_path_requirement: str
    allocation_domain_classification: str
    domain_blocker_ids: tuple[str, ...]
    path_candidates: tuple[UnorderedExactInstanceSetPathCandidate, ...]
    unit5_allocation_closure_rows: tuple[ClassicalSemanticClosureGovernanceRow, ...]
    source_unresolved_graph_requirements_provenance: tuple[str, ...]
    source_narrative_chain_ids_provenance: tuple[str, ...]


@dataclass(frozen=True)
class ProposalAllocationElaboration:
    proposal_allocation_elaboration_id: str
    source_mechanism_proposal_id: str
    source_semantic_candidate_id: str
    source_fragment_governance_projection_id: str
    source_fragment_semantic_projection_id: str
    source_fragment_id: str
    source_occurrence_id: str
    binding_candidate_id: str
    semantic_candidate_kind: str
    mechanism_proposal_kind: str
    allocation_domain_observations: tuple[AllocationDomainObservation, ...]
    allocation_elaboration_semantics: str


@dataclass(frozen=True)
class FragmentAllocationElaborationProjection:
    fragment_allocation_projection_id: str
    source_fragment_governance_projection_id: str
    source_fragment_semantic_projection_id: str
    source_fragment_id: str
    source_occurrence_id: str
    binding_candidate_id: str
    source_governance_status: str
    allocation_status: str
    source_mechanism_proposal_ids: tuple[str, ...]
    proposal_elaborations: tuple[ProposalAllocationElaboration, ...]
    allocation_domain_observation_ids: tuple[str, ...]


@dataclass(frozen=True)
class SourceRecordAllocationElaborationSet:
    source_record_candidate_set_id: str
    source_layer: str
    source_occurrence_id: str
    source_fragment_ids: tuple[str, ...]
    fragment_allocation_projection_ids: tuple[str, ...]
    source_mechanism_proposal_ids: tuple[str, ...]
    allocation_domain_observation_ids: tuple[str, ...]
    path_candidate_ids: tuple[str, ...]
    member_selection_semantics: str = "NOT_RELEASED"
    member_coexistence_semantics: str = "NOT_RELEASED"
    member_exclusivity_semantics: str = "NOT_RELEASED"
    allocation_priority_semantics: str = "NOT_RELEASED"
    allocation_conflict_semantics: str = "NOT_RELEASED"


@dataclass(frozen=True)
class MultiplicityAllocationDomainIndexEntry:
    multiplicity_constraint_id: str
    source_semantic_candidate_ids: tuple[str, ...]
    source_mechanism_proposal_ids: tuple[str, ...]
    allocation_domain_observation_ids: tuple[str, ...]
    path_candidate_ids: tuple[str, ...]
    index_semantics: str = "IDENTITY_ONLY_NO_SYNTHESIS_OR_SELECTION"


@dataclass(frozen=True)
class AllocationIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class AllocationIntegrityReport:
    status: str
    diagnostics: tuple[AllocationIntegrityDiagnostic, ...]
    algorithm_id: str = "BAZI-CLASSICAL-NON-SELECTING-ALLOCATION-INTEGRITY-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class AllocationHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-CLASSICAL-NON-SELECTING-ALLOCATION-HASH-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class ClassicalNonSelectingParticipantAllocationEnvelope:
    allocation_envelope_id: str
    source_mechanism_closure_envelope_id: str
    source_mechanism_closure_fact_hash: str
    source_mechanism_closure_computation_hash: str
    source_semantic_projection_envelope_id: str
    source_admission_envelope_id: str
    source_effect_envelope_id: str
    lineage_binding_keys: tuple[str, ...]
    fragment_allocation_projections: tuple[FragmentAllocationElaborationProjection, ...]
    source_record_candidate_sets: tuple[SourceRecordAllocationElaborationSet, ...]
    multiplicity_domain_index: tuple[MultiplicityAllocationDomainIndexEntry, ...]
    projected_allocation_domain_observation_ids: tuple[str, ...]
    projected_path_candidate_ids: tuple[str, ...]
    synthetic_permutation_generation: str
    synthetic_combination_generation: str
    inferred_slot_instance_compatibility: str
    participant_path_selection_semantics: str
    allocation_truth_semantics: str
    allocation_operability_semantics: str
    coexistence_semantics: str
    exclusivity_semantics: str
    precedence_semantics: str
    priority_semantics: str
    winner_loser_semantics: str
    relation_effect_state_semantics: str
    rewrite_application_semantics: str
    fragment_selection_semantics: str
    cross_outer_composition: str
    cartesian_expansion: str
    raw_relation_immutability_contract: str
    algorithm_versions: Mapping[str, str]
    integrity: AllocationIntegrityReport
    hashes: AllocationHashBundle


@dataclass(frozen=True)
class BaziClassicalNonSelectingParticipantAllocationResolution:
    schema: str
    status: str
    candidates: tuple[ClassicalNonSelectingParticipantAllocationEnvelope, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
