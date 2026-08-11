from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class RawRelationReferenceNode:
    raw_relation_node_id: str
    binding_candidate_id: str
    exact_relation_id: str
    exact_semantic_relation_id: str
    relation_type: str
    relation_family: str
    participant_instance_ids: tuple[str, ...]


@dataclass(frozen=True)
class ClassicalRelationEffectChannelReference:
    effect_channel_id: str
    binding_candidate_id: str
    target_exact_relation_id: str
    effect_facet: str


@dataclass(frozen=True)
class EffectConstraintMultiplicityReference:
    multiplicity_constraint_id: str
    exchangeable_symbolic_slot_node_ids: tuple[str, ...]
    exact_runtime_instance_ids: tuple[str, ...]
    required_symbolic_cardinality: int
    slot_equivalence: str
    alternative_path_requirement: str


@dataclass(frozen=True)
class ClassicalInteractionEffectConstraintCandidate:
    effect_constraint_id: str
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
    constraint_kind: str
    structural_binding_class: str
    source_scope_compatibility: str
    residual_unresolved_structural_constraint_ids: tuple[str, ...]
    unresolved_classical_semantic_requirements: tuple[str, ...]
    source_unresolved_graph_requirements: tuple[str, ...]
    multiplicity_references: tuple[EffectConstraintMultiplicityReference, ...]
    source_narrative_chain_ids: tuple[str, ...]


@dataclass(frozen=True)
class ClassicalEffectConstraintNode:
    constraint_node_id: str
    constraint: ClassicalInteractionEffectConstraintCandidate


@dataclass(frozen=True)
class ClassicalEffectGraphEdge:
    edge_id: str
    edge_kind: str
    source_node_id: str
    target_node_id: str
    source_claim_edge_id: str | None
    source_chain_pattern_id: str | None


@dataclass(frozen=True)
class FragmentHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-CLASSICAL-EFFECT-CONSTRAINT-GRAPH-FRAGMENT-HASH-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class ClassicalInteractionEffectConstraintGraphFragmentCandidate:
    fragment_id: str
    binding_candidate_id: str
    source_occurrence_id: str
    graph_record_id: str
    interaction_assertion_id: str
    source_layer: str
    structural_binding_class: str
    source_scope_compatibility: str
    raw_relation_reference_nodes: tuple[RawRelationReferenceNode, ...]
    effect_channel_nodes: tuple[ClassicalRelationEffectChannelReference, ...]
    effect_constraint_nodes: tuple[ClassicalEffectConstraintNode, ...]
    graph_edges: tuple[ClassicalEffectGraphEdge, ...]
    multiplicity_references: tuple[EffectConstraintMultiplicityReference, ...]
    residual_unresolved_structural_constraint_ids: tuple[str, ...]
    source_unresolved_graph_requirements: tuple[str, ...]
    source_narrative_chain_ids: tuple[str, ...]
    hashes: FragmentHashBundle


@dataclass(frozen=True)
class SourceRecordEffectFragmentCandidateSet:
    source_record_candidate_set_id: str
    source_layer: str
    source_occurrence_id: str
    fragment_ids: tuple[str, ...]
    member_selection_semantics: str = "NOT_RELEASED"
    member_coexistence_semantics: str = "NOT_RELEASED"
    member_exclusivity_semantics: str = "NOT_RELEASED"


@dataclass(frozen=True)
class SourceLayerEffectFragmentPartition:
    source_layer_partition_id: str
    source_layer: str
    source_record_candidate_sets: tuple[SourceRecordEffectFragmentCandidateSet, ...]


@dataclass(frozen=True)
class ExactRawRelationConstraintReferenceIndexEntry:
    exact_relation_id: str
    referencing_fragment_ids: tuple[str, ...]
    actor_constraint_ids: tuple[str, ...]
    target_effect_channel_ids: tuple[str, ...]


@dataclass(frozen=True)
class ExactEffectChannelCoordinateIndexEntry:
    exact_relation_id: str
    effect_facet: str
    referencing_fragment_ids: tuple[str, ...]
    fragment_local_effect_channel_ids: tuple[str, ...]


@dataclass(frozen=True)
class EffectCompositionIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class EffectCompositionIntegrityReport:
    status: str
    diagnostics: tuple[EffectCompositionIntegrityDiagnostic, ...]
    algorithm_id: str = "BAZI-CLASSICAL-EFFECT-CONSTRAINT-COMPOSITION-INTEGRITY-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class EffectCompositionHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-CLASSICAL-EFFECT-CONSTRAINT-COMPOSITION-HASH-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class ClassicalEffectConstraintCompositionEnvelopeCandidate:
    envelope_id: str
    source_projection_fact_hash: str
    source_projection_computation_hash: str
    source_binding_snapshot_id: str
    source_binding_snapshot_fact_hash: str
    source_binding_fact_hash: str
    source_binding_computation_hash: str
    source_incidence_candidate_indices: tuple[int, ...]
    source_branch_positional_candidate_index: int
    source_stem_positional_candidate_index: int
    source_flow_candidate_indices: tuple[int, ...]
    source_structural_candidate_indices: tuple[int, ...]
    source_support_candidate_indices: tuple[int, ...]
    source_temporal_candidate_indices: tuple[int, ...]
    source_temporal_seed_ids: tuple[str, ...]
    source_incidence_lineage_binding_keys: tuple[str, ...]
    lineage_binding_keys: tuple[str, ...]
    fragments: tuple[ClassicalInteractionEffectConstraintGraphFragmentCandidate, ...]
    source_layer_partitions: tuple[SourceLayerEffectFragmentPartition, ...]
    raw_relation_reference_index: tuple[ExactRawRelationConstraintReferenceIndexEntry, ...]
    effect_channel_coordinate_index: tuple[ExactEffectChannelCoordinateIndexEntry, ...]
    cross_source_layer_composition: str
    cartesian_expansion: str
    raw_relation_immutability_contract: str
    algorithm_versions: Mapping[str, str]
    integrity: EffectCompositionIntegrityReport
    hashes: EffectCompositionHashBundle


@dataclass(frozen=True)
class BaziClassicalEffectConstraintGraphResolution:
    schema: str
    status: str
    candidates: tuple[ClassicalEffectConstraintCompositionEnvelopeCandidate, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
