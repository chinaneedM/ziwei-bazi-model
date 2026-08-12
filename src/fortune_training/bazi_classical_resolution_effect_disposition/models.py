from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from fortune_training.bazi_classical_final_effect_candidate_envelope.models import (
    FinalClassicalEffectCandidate,
)


@dataclass(frozen=True)
class CandidateLocalResolutionEffectDisposition:
    resolution_effect_disposition_id: str
    source_final_candidate_id: str
    source_occurrence_id: str
    graph_record_id: str
    interaction_assertion_id: str
    source_claim_edge_id: str
    source_claim_edge_class: str
    exact_source_fragments: tuple[str, ...]
    target_effect_channel_id: str
    target_exact_relation_id: str
    effect_facet: str
    disposition_kind: str
    semantic_scope: str
    raw_relation_action: str
    raw_relation_presence_semantics: str
    source_narrative_chain_ids_provenance: tuple[str, ...]
    source_unresolved_graph_requirements_provenance: tuple[str, ...]


@dataclass(frozen=True)
class ResolutionClosureResolutionRow:
    closure_requirement_id: str
    upstream_runtime_dependency_status: str
    unit8_local_closure_result: str
    semantic_scope: str


@dataclass(frozen=True)
class ResolutionEffectCandidateProjection:
    candidate_projection_id: str
    source_final_candidate_id: str
    source_final_candidate: FinalClassicalEffectCandidate
    projection_status: str
    resolution_closure_rows: tuple[ResolutionClosureResolutionRow, ...]
    resolution_effect_dispositions: tuple[CandidateLocalResolutionEffectDisposition, ...]
    resolution_effect_disposition_ids: tuple[str, ...]


@dataclass(frozen=True)
class ResolutionEffectFragmentProjection:
    fragment_projection_id: str
    source_final_fragment_id: str
    source_fragment_id: str
    source_occurrence_id: str
    binding_candidate_id: str
    source_final_fragment_status: str
    projection_status: str
    source_final_candidate_ids: tuple[str, ...]
    candidate_projections: tuple[ResolutionEffectCandidateProjection, ...]
    candidate_projection_ids: tuple[str, ...]
    resolution_effect_disposition_ids: tuple[str, ...]


@dataclass(frozen=True)
class SourceRecordResolutionEffectCandidateSet:
    source_record_candidate_set_id: str
    source_final_candidate_set_id: str
    source_layer: str
    source_occurrence_id: str
    source_final_fragment_ids: tuple[str, ...]
    fragment_projection_ids: tuple[str, ...]
    candidate_projection_ids: tuple[str, ...]
    resolution_effect_disposition_ids: tuple[str, ...]
    member_selection_semantics: str = "NOT_RELEASED"
    member_coexistence_semantics: str = "NOT_RELEASED"
    member_exclusivity_semantics: str = "NOT_RELEASED"
    member_priority_semantics: str = "NOT_RELEASED"
    member_conflict_semantics: str = "NOT_RELEASED"


@dataclass(frozen=True)
class EffectChannelResolutionDispositionIndexEntry:
    target_exact_relation_id: str
    effect_facet: str
    candidate_projection_ids: tuple[str, ...]
    resolution_effect_disposition_ids: tuple[str, ...]
    index_semantics: str


@dataclass(frozen=True)
class SourceOccurrenceResolutionDispositionIndexEntry:
    source_occurrence_id: str
    candidate_projection_ids: tuple[str, ...]
    resolution_effect_disposition_ids: tuple[str, ...]
    index_semantics: str


@dataclass(frozen=True)
class LocalClosureResolutionIndexEntry:
    closure_requirement_id: str
    unit8_local_closure_result: str
    candidate_projection_ids: tuple[str, ...]
    index_semantics: str


@dataclass(frozen=True)
class ResolutionEffectDispositionIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class ResolutionEffectDispositionIntegrityReport:
    status: str
    diagnostics: tuple[ResolutionEffectDispositionIntegrityDiagnostic, ...]
    algorithm_id: str = "BAZI-CLASSICAL-RESOLUTION-EFFECT-DISPOSITION-INTEGRITY-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class ResolutionEffectDispositionHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-CLASSICAL-RESOLUTION-EFFECT-DISPOSITION-HASH-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class ClassicalResolutionEffectDispositionEnvelope:
    resolution_effect_envelope_id: str
    source_final_effect_envelope_id: str
    source_final_effect_fact_hash: str
    source_final_effect_computation_hash: str
    source_allocation_envelope_id: str
    source_mechanism_closure_envelope_id: str
    source_semantic_projection_envelope_id: str
    source_admission_envelope_id: str
    source_effect_envelope_id: str
    lineage_binding_keys: tuple[str, ...]
    fragment_projections: tuple[ResolutionEffectFragmentProjection, ...]
    source_record_candidate_sets: tuple[SourceRecordResolutionEffectCandidateSet, ...]
    effect_channel_index: tuple[EffectChannelResolutionDispositionIndexEntry, ...]
    source_occurrence_index: tuple[SourceOccurrenceResolutionDispositionIndexEntry, ...]
    local_closure_index: tuple[LocalClosureResolutionIndexEntry, ...]
    projected_candidate_projection_ids: tuple[str, ...]
    projected_resolution_effect_disposition_ids: tuple[str, ...]
    disposition_semantic_scope: str
    candidate_global_truth_semantics: str
    global_operability_semantics: str
    candidate_selection_semantics: str
    candidate_coexistence_semantics: str
    candidate_exclusivity_semantics: str
    candidate_conflict_semantics: str
    precedence_semantics: str
    priority_semantics: str
    winner_loser_semantics: str
    global_relation_effect_state_semantics: str
    execution_readiness_semantics: str
    resolution_failure_semantics: str
    reversal_reappearance_semantics: str
    attenuation_grade_semantics: str
    participant_allocation_semantics: str
    participant_path_selection_semantics: str
    inferred_slot_instance_compatibility: str
    source_narrative_execution: str
    graph_mutation_fixpoint_semantics: str
    fragment_selection_semantics: str
    cross_outer_composition: str
    cross_source_composition: str
    cartesian_expansion: str
    final_classical_verdict_semantics: str
    raw_relation_immutability_contract: str
    algorithm_versions: Mapping[str, str]
    integrity: ResolutionEffectDispositionIntegrityReport
    hashes: ResolutionEffectDispositionHashBundle


@dataclass(frozen=True)
class BaziClassicalResolutionEffectDispositionResolution:
    schema: str
    status: str
    candidates: tuple[ClassicalResolutionEffectDispositionEnvelope, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
