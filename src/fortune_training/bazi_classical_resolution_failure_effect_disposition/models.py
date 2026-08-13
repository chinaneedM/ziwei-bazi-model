from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from fortune_training.bazi_classical_final_effect_candidate_envelope.models import (
    FinalClassicalEffectCandidate,
)


@dataclass(frozen=True)
class CandidateLocalResolutionFailureEffectDisposition:
    resolution_failure_effect_disposition_id: str
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
    resolution_mechanism_disposition: str
    raw_relation_action: str
    raw_relation_presence_semantics: str
    source_narrative_chain_ids_provenance: tuple[str, ...]
    source_unresolved_graph_requirements_provenance: tuple[str, ...]


@dataclass(frozen=True)
class ResolutionFailureClosureResolutionRow:
    closure_requirement_id: str
    upstream_runtime_dependency_status: str
    unit9_local_closure_result: str
    semantic_scope: str


@dataclass(frozen=True)
class ResolutionFailureEffectCandidateProjection:
    candidate_projection_id: str
    source_final_candidate_id: str
    source_final_candidate: FinalClassicalEffectCandidate
    projection_status: str
    resolution_failure_closure_rows: tuple[ResolutionFailureClosureResolutionRow, ...]
    resolution_failure_effect_dispositions: tuple[
        CandidateLocalResolutionFailureEffectDisposition, ...
    ]
    resolution_failure_effect_disposition_ids: tuple[str, ...]


@dataclass(frozen=True)
class ResolutionFailureEffectFragmentProjection:
    fragment_projection_id: str
    source_final_fragment_id: str
    source_fragment_id: str
    source_occurrence_id: str
    binding_candidate_id: str
    source_final_fragment_status: str
    projection_status: str
    source_final_candidate_ids: tuple[str, ...]
    candidate_projections: tuple[ResolutionFailureEffectCandidateProjection, ...]
    candidate_projection_ids: tuple[str, ...]
    resolution_failure_effect_disposition_ids: tuple[str, ...]


@dataclass(frozen=True)
class SourceRecordResolutionFailureEffectCandidateSet:
    source_record_candidate_set_id: str
    source_final_candidate_set_id: str
    source_layer: str
    source_occurrence_id: str
    source_final_fragment_ids: tuple[str, ...]
    fragment_projection_ids: tuple[str, ...]
    candidate_projection_ids: tuple[str, ...]
    resolution_failure_effect_disposition_ids: tuple[str, ...]
    member_selection_semantics: str = "NOT_RELEASED"
    member_coexistence_semantics: str = "NOT_RELEASED"
    member_exclusivity_semantics: str = "NOT_RELEASED"
    member_priority_semantics: str = "NOT_RELEASED"
    member_conflict_semantics: str = "NOT_RELEASED"


@dataclass(frozen=True)
class EffectChannelResolutionFailureDispositionIndexEntry:
    target_exact_relation_id: str
    effect_facet: str
    candidate_projection_ids: tuple[str, ...]
    resolution_failure_effect_disposition_ids: tuple[str, ...]
    index_semantics: str


@dataclass(frozen=True)
class SourceOccurrenceResolutionFailureDispositionIndexEntry:
    source_occurrence_id: str
    candidate_projection_ids: tuple[str, ...]
    resolution_failure_effect_disposition_ids: tuple[str, ...]
    index_semantics: str


@dataclass(frozen=True)
class LocalFailureClosureResolutionIndexEntry:
    closure_requirement_id: str
    unit9_local_closure_result: str
    candidate_projection_ids: tuple[str, ...]
    index_semantics: str


@dataclass(frozen=True)
class ResolutionFailureEffectDispositionIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class ResolutionFailureEffectDispositionIntegrityReport:
    status: str
    diagnostics: tuple[ResolutionFailureEffectDispositionIntegrityDiagnostic, ...]
    algorithm_id: str = (
        "BAZI-CLASSICAL-RESOLUTION-FAILURE-EFFECT-DISPOSITION-INTEGRITY-R1"
    )
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class ResolutionFailureEffectDispositionHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-CLASSICAL-RESOLUTION-FAILURE-EFFECT-DISPOSITION-HASH-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class ClassicalResolutionFailureEffectDispositionEnvelope:
    resolution_failure_effect_envelope_id: str
    source_final_effect_envelope_id: str
    source_final_effect_fact_hash: str
    source_final_effect_computation_hash: str
    source_allocation_envelope_id: str
    source_mechanism_closure_envelope_id: str
    source_semantic_projection_envelope_id: str
    source_admission_envelope_id: str
    source_effect_envelope_id: str
    lineage_binding_keys: tuple[str, ...]
    fragment_projections: tuple[ResolutionFailureEffectFragmentProjection, ...]
    source_record_candidate_sets: tuple[SourceRecordResolutionFailureEffectCandidateSet, ...]
    effect_channel_index: tuple[EffectChannelResolutionFailureDispositionIndexEntry, ...]
    source_occurrence_index: tuple[
        SourceOccurrenceResolutionFailureDispositionIndexEntry, ...
    ]
    local_closure_index: tuple[LocalFailureClosureResolutionIndexEntry, ...]
    projected_candidate_projection_ids: tuple[str, ...]
    projected_resolution_failure_effect_disposition_ids: tuple[str, ...]
    disposition_semantic_scope: str
    resolution_mechanism_disposition: str
    candidate_global_truth_semantics: str
    target_relation_restored_state_semantics: str
    reversal_reappearance_semantics: str
    interaction_chain_execution_semantics: str
    global_operability_semantics: str
    candidate_applicability_semantics: str
    execution_readiness_semantics: str
    candidate_selection_semantics: str
    candidate_coexistence_semantics: str
    candidate_exclusivity_semantics: str
    candidate_conflict_semantics: str
    precedence_semantics: str
    priority_semantics: str
    winner_loser_semantics: str
    global_relation_effect_state_semantics: str
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
    integrity: ResolutionFailureEffectDispositionIntegrityReport
    hashes: ResolutionFailureEffectDispositionHashBundle


@dataclass(frozen=True)
class BaziClassicalResolutionFailureEffectDispositionResolution:
    schema: str
    status: str
    candidates: tuple[ClassicalResolutionFailureEffectDispositionEnvelope, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
