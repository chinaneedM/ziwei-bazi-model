from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from fortune_training.bazi_classical_effect_constraint_graph.models import (
    EffectConstraintMultiplicityReference,
)
from fortune_training.bazi_classical_non_selecting_participant_allocation.models import (
    AllocationDomainObservation,
)
from fortune_training.bazi_classical_semantic_closure_governance.models import (
    ClassicalSemanticClosureGovernanceRow,
)


@dataclass(frozen=True)
class FinalClassicalEffectCandidate:
    final_candidate_id: str
    source_semantic_candidate_id: str
    source_mechanism_proposal_id: str
    source_allocation_elaboration_id: str
    source_semantic_projection_envelope_id: str
    source_semantic_projection_fact_hash: str
    source_semantic_projection_computation_hash: str
    source_mechanism_closure_envelope_id: str
    source_mechanism_closure_fact_hash: str
    source_mechanism_closure_computation_hash: str
    source_allocation_envelope_id: str
    source_allocation_fact_hash: str
    source_allocation_computation_hash: str
    source_admission_envelope_id: str
    source_effect_envelope_id: str
    source_fragment_semantic_projection_id: str
    source_fragment_governance_projection_id: str
    source_fragment_allocation_projection_id: str
    source_fragment_id: str
    source_fragment_fact_hash: str
    source_fragment_computation_hash: str
    binding_candidate_id: str
    source_occurrence_id: str
    graph_record_id: str
    interaction_assertion_id: str
    source_claim_edge_id: str
    source_claim_edge_class: str
    source_assertion_class: str
    source_evidence_mode: str
    exact_source_fragments: tuple[str, ...]
    source_semantic_profile_id: str
    source_semantic_partition_id: str
    target_effect_channel_id: str
    target_exact_relation_id: str
    actor_exact_relation_ids: tuple[str, ...]
    actor_exact_participant_ids: tuple[str, ...]
    context_exact_participant_ids: tuple[str, ...]
    effect_facet: str
    semantic_candidate_kind: str
    mechanism_proposal_kind: str
    unresolved_classical_semantic_requirements: tuple[str, ...]
    closure_governance_rows: tuple[ClassicalSemanticClosureGovernanceRow, ...]
    multiplicity_references: tuple[EffectConstraintMultiplicityReference, ...]
    allocation_domain_observations: tuple[AllocationDomainObservation, ...]
    source_narrative_chain_ids_provenance: tuple[str, ...]
    source_unresolved_graph_requirements_provenance: tuple[str, ...]
    final_candidate_semantics: str


@dataclass(frozen=True)
class FinalEffectCandidateFragmentEnvelope:
    final_fragment_id: str
    source_fragment_semantic_projection_id: str
    source_fragment_governance_projection_id: str
    source_fragment_allocation_projection_id: str
    source_fragment_id: str
    source_occurrence_id: str
    binding_candidate_id: str
    source_projection_status: str
    source_governance_status: str
    source_allocation_status: str
    final_fragment_status: str
    source_semantic_candidate_ids: tuple[str, ...]
    source_mechanism_proposal_ids: tuple[str, ...]
    source_allocation_elaboration_ids: tuple[str, ...]
    final_candidates: tuple[FinalClassicalEffectCandidate, ...]
    final_candidate_ids: tuple[str, ...]


@dataclass(frozen=True)
class SourceRecordFinalEffectCandidateSet:
    source_record_candidate_set_id: str
    source_layer: str
    source_occurrence_id: str
    source_fragment_ids: tuple[str, ...]
    final_fragment_ids: tuple[str, ...]
    final_candidate_ids: tuple[str, ...]
    member_selection_semantics: str = "NOT_RELEASED"
    member_coexistence_semantics: str = "NOT_RELEASED"
    member_exclusivity_semantics: str = "NOT_RELEASED"
    member_priority_semantics: str = "NOT_RELEASED"
    member_conflict_semantics: str = "NOT_RELEASED"


@dataclass(frozen=True)
class ExactEffectChannelFinalCandidateIndexEntry:
    target_exact_relation_id: str
    effect_facet: str
    final_candidate_ids: tuple[str, ...]
    index_semantics: str


@dataclass(frozen=True)
class SemanticKindFinalCandidateIndexEntry:
    semantic_candidate_kind: str
    final_candidate_ids: tuple[str, ...]
    index_semantics: str


@dataclass(frozen=True)
class MechanismKindFinalCandidateIndexEntry:
    mechanism_proposal_kind: str
    final_candidate_ids: tuple[str, ...]
    index_semantics: str


@dataclass(frozen=True)
class ClosureStatusFinalCandidateIndexEntry:
    closure_requirement_id: str
    runtime_dependency_status: str
    final_candidate_ids: tuple[str, ...]
    index_semantics: str


@dataclass(frozen=True)
class MultiplicityFinalCandidateIndexEntry:
    multiplicity_constraint_id: str
    final_candidate_ids: tuple[str, ...]
    allocation_domain_observation_ids: tuple[str, ...]
    path_candidate_ids: tuple[str, ...]
    index_semantics: str


@dataclass(frozen=True)
class FinalEffectEnvelopeIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class FinalEffectEnvelopeIntegrityReport:
    status: str
    diagnostics: tuple[FinalEffectEnvelopeIntegrityDiagnostic, ...]
    algorithm_id: str = "BAZI-CLASSICAL-FINAL-EFFECT-CANDIDATE-ENVELOPE-INTEGRITY-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class FinalEffectEnvelopeHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-CLASSICAL-FINAL-EFFECT-CANDIDATE-ENVELOPE-HASH-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class ClassicalFinalEffectCandidateEnvelope:
    final_effect_envelope_id: str
    source_allocation_envelope_id: str
    source_allocation_fact_hash: str
    source_allocation_computation_hash: str
    source_mechanism_closure_envelope_id: str
    source_mechanism_closure_fact_hash: str
    source_mechanism_closure_computation_hash: str
    source_semantic_projection_envelope_id: str
    source_semantic_projection_fact_hash: str
    source_semantic_projection_computation_hash: str
    source_admission_envelope_id: str
    source_effect_envelope_id: str
    lineage_binding_keys: tuple[str, ...]
    fragment_envelopes: tuple[FinalEffectCandidateFragmentEnvelope, ...]
    source_record_candidate_sets: tuple[SourceRecordFinalEffectCandidateSet, ...]
    effect_channel_index: tuple[ExactEffectChannelFinalCandidateIndexEntry, ...]
    semantic_kind_index: tuple[SemanticKindFinalCandidateIndexEntry, ...]
    mechanism_kind_index: tuple[MechanismKindFinalCandidateIndexEntry, ...]
    closure_status_index: tuple[ClosureStatusFinalCandidateIndexEntry, ...]
    multiplicity_index: tuple[MultiplicityFinalCandidateIndexEntry, ...]
    projected_final_candidate_ids: tuple[str, ...]
    final_candidate_semantics: str
    candidate_truth_semantics: str
    candidate_operability_semantics: str
    candidate_applicability_semantics: str
    mechanism_execution_semantics: str
    rewrite_application_semantics: str
    lifecycle_truth_gate: str
    candidate_coexistence_semantics: str
    candidate_exclusivity_semantics: str
    candidate_conflict_semantics: str
    precedence_semantics: str
    priority_semantics: str
    winner_loser_semantics: str
    participant_path_selection_semantics: str
    relation_effect_state_semantics: str
    graph_mutation_fixpoint_semantics: str
    execution_readiness_semantics: str
    synthetic_permutation_generation: str
    synthetic_combination_generation: str
    inferred_slot_instance_compatibility: str
    fragment_selection_semantics: str
    cross_outer_composition: str
    cross_source_composition: str
    cartesian_expansion: str
    raw_relation_immutability_contract: str
    algorithm_versions: Mapping[str, str]
    integrity: FinalEffectEnvelopeIntegrityReport
    hashes: FinalEffectEnvelopeHashBundle


@dataclass(frozen=True)
class BaziClassicalFinalEffectCandidateEnvelopeResolution:
    schema: str
    status: str
    candidates: tuple[ClassicalFinalEffectCandidateEnvelope, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
