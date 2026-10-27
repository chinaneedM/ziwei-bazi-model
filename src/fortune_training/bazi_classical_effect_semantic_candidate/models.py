from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from fortune_training.bazi_classical_effect_constraint_graph.models import (
    EffectConstraintMultiplicityReference,
)


@dataclass(frozen=True)
class ClassicalEffectSemanticCandidate:
    semantic_candidate_id: str
    source_admission_projection_id: str
    source_effect_envelope_id: str
    source_effect_envelope_fact_hash: str
    source_effect_envelope_computation_hash: str
    source_fragment_id: str
    source_fragment_fact_hash: str
    source_fragment_computation_hash: str
    source_effect_constraint_id: str
    binding_candidate_id: str
    source_occurrence_id: str
    graph_record_id: str
    interaction_assertion_id: str
    source_claim_edge_id: str
    source_claim_edge_class: str
    source_assertion_class: str
    source_evidence_mode: str
    exact_source_fragments: tuple[str, ...]
    target_effect_channel_id: str
    target_exact_relation_id: str
    actor_exact_relation_ids: tuple[str, ...]
    actor_exact_participant_ids: tuple[str, ...]
    context_exact_participant_ids: tuple[str, ...]
    effect_facet: str
    semantic_candidate_kind: str
    multiplicity_references: tuple[EffectConstraintMultiplicityReference, ...]
    source_narrative_chain_ids: tuple[str, ...]
    unresolved_classical_semantic_requirements: tuple[str, ...]
    source_unresolved_graph_requirements_provenance: tuple[str, ...]
    source_semantic_profile_id: str
    source_semantic_partition_id: str
    candidate_truth_semantics: str = "NOT_RELEASED"
    candidate_applicability_semantics: str = "NOT_RELEASED_BEYOND_UNIT3_ADMISSION"


@dataclass(frozen=True)
class ClassicalFragmentSemanticCandidateProjection:
    fragment_semantic_projection_id: str
    source_admission_projection_id: str
    source_fragment_id: str
    source_fragment_fact_hash: str
    source_fragment_computation_hash: str
    source_occurrence_id: str
    binding_candidate_id: str
    admission_status: str
    admission_blocker_ids: tuple[str, ...]
    source_semantic_profile_id: str
    source_semantic_partition_id: str
    projection_status: str
    semantic_candidates: tuple[ClassicalEffectSemanticCandidate, ...]
    source_unresolved_graph_requirements_provenance: tuple[str, ...]
    unresolved_classical_semantic_requirements: tuple[str, ...]


@dataclass(frozen=True)
class SourceRecordSemanticCandidateSet:
    source_record_candidate_set_id: str
    source_layer: str
    source_occurrence_id: str
    source_fragment_ids: tuple[str, ...]
    fragment_semantic_projection_ids: tuple[str, ...]
    semantic_candidate_ids: tuple[str, ...]
    member_selection_semantics: str = "NOT_RELEASED"
    member_coexistence_semantics: str = "NOT_RELEASED"
    member_exclusivity_semantics: str = "NOT_RELEASED"
    semantic_candidate_priority_semantics: str = "NOT_RELEASED"
    semantic_candidate_conflict_semantics: str = "NOT_RELEASED"


@dataclass(frozen=True)
class ExactEffectChannelSemanticCandidateIndexEntry:
    target_exact_relation_id: str
    effect_facet: str
    source_fragment_ids: tuple[str, ...]
    semantic_candidate_ids: tuple[str, ...]
    index_semantics: str = "IDENTITY_ONLY_NO_MERGE_OR_ARBITRATION"


@dataclass(frozen=True)
class SemanticCandidateIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class SemanticCandidateIntegrityReport:
    status: str
    diagnostics: tuple[SemanticCandidateIntegrityDiagnostic, ...]
    algorithm_id: str = "BAZI-CLASSICAL-EFFECT-SEMANTIC-CANDIDATE-INTEGRITY-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class SemanticCandidateHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-CLASSICAL-EFFECT-SEMANTIC-CANDIDATE-HASH-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class ClassicalEffectSemanticCandidateProjectionEnvelope:
    semantic_projection_envelope_id: str
    source_admission_envelope_id: str
    source_admission_fact_hash: str
    source_admission_computation_hash: str
    source_effect_envelope_id: str
    source_effect_fact_hash: str
    source_effect_computation_hash: str
    lineage_binding_keys: tuple[str, ...]
    fragment_projections: tuple[ClassicalFragmentSemanticCandidateProjection, ...]
    source_record_candidate_sets: tuple[SourceRecordSemanticCandidateSet, ...]
    effect_channel_candidate_index: tuple[ExactEffectChannelSemanticCandidateIndexEntry, ...]
    projected_semantic_candidate_ids: tuple[str, ...]
    fragment_selection_semantics: str
    cross_outer_composition: str
    cartesian_expansion: str
    raw_relation_immutability_contract: str
    candidate_truth_semantics: str
    candidate_coexistence_semantics: str
    candidate_exclusivity_semantics: str
    candidate_priority_semantics: str
    candidate_conflict_semantics: str
    candidate_rewrite_semantics: str
    candidate_state_transition_semantics: str
    candidate_winner_loser_semantics: str
    algorithm_versions: Mapping[str, str]
    integrity: SemanticCandidateIntegrityReport
    hashes: SemanticCandidateHashBundle


@dataclass(frozen=True)
class BaziClassicalEffectSemanticCandidateProjectionResolution:
    schema: str
    status: str
    candidates: tuple[ClassicalEffectSemanticCandidateProjectionEnvelope, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
