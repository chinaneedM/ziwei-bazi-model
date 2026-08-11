from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class SourceScopeSpecification:
    source_occurrence_id: str
    graph_record_id: str
    scope_specification_status: str
    source_scope_evidence_mode: str | None
    source_chart_domain: str | None
    runtime_scope_subject: str | None
    required_runtime_participant_layer: str | None
    cross_layer_extension_policy: str | None
    context_inheritance_edge_ids: tuple[str, ...]


@dataclass(frozen=True)
class SourceScopeCompatibilityProjection:
    source_occurrence_id: str
    binding_candidate_id: str
    source_scope_compatibility: str
    observed_participant_layers: tuple[str, ...]
    cross_layer_participant_instance_ids: tuple[str, ...]


@dataclass(frozen=True)
class BoundRelationIdentityObservation:
    observation_id: str
    relation_pattern_node_id: str
    exact_relation_id: str
    exact_semantic_relation_id: str
    relation_type: str
    relation_family: str
    participant_instance_ids: tuple[str, ...]
    source_relation_reference_id: str
    positional_fact_id: str


@dataclass(frozen=True)
class BoundParticipantIdentityObservation:
    observation_id: str
    participant_pattern_node_ids: tuple[str, ...]
    participant_kind: str
    literal_value: str
    exact_participant_instance_ids: tuple[str, ...]


@dataclass(frozen=True)
class BoundRelationPairTopologyObservation:
    observation_id: str
    pair_fact_id: str
    exact_relation_ids: tuple[str, str]
    topology_kind: str
    shared_participant_instance_ids: tuple[str, ...]
    left_only_participant_instance_ids: tuple[str, ...]
    right_only_participant_instance_ids: tuple[str, ...]
    referencing_claim_edge_ids: tuple[str, ...]


@dataclass(frozen=True)
class BoundParticipantIncidenceObservation:
    observation_id: str
    incidence_fact_id: str
    participant_instance_id: str
    relation_ids: tuple[str, ...]
    relation_count: int


@dataclass(frozen=True)
class BoundTemporalLayerFrameObservation:
    observation_id: str
    participant_instance_id: str
    participant_layer: str
    source_frame_id: str | None
    position_reference_id: str


@dataclass(frozen=True)
class BindingScopedNeutralObservationBundle:
    observation_bundle_id: str
    binding_candidate_id: str
    source_occurrence_id: str
    required_neutral_primitives: tuple[str, ...]
    relation_identity_observations: tuple[BoundRelationIdentityObservation, ...]
    participant_identity_observations: tuple[BoundParticipantIdentityObservation, ...]
    relation_pair_topology_observations: tuple[BoundRelationPairTopologyObservation, ...]
    participant_incidence_observations: tuple[BoundParticipantIncidenceObservation, ...]
    temporal_layer_frame_observations: tuple[BoundTemporalLayerFrameObservation, ...]


@dataclass(frozen=True)
class ChartBoundSourceInteractionClaim:
    chart_bound_claim_id: str
    binding_candidate_id: str
    source_occurrence_id: str
    graph_record_id: str
    source_claim_edge_id: str
    source_claim_edge_class: str
    source_assertion_class: str
    source_evidence_mode: str
    exact_source_fragments: tuple[str, ...]
    actor_reference_kind: str
    actor_exact_relation_ids: tuple[str, ...]
    actor_exact_participant_ids: tuple[str, ...]
    context_exact_participant_ids: tuple[str, ...]
    target_reference_kind: str
    target_exact_relation_ids: tuple[str, ...]
    target_exact_participant_ids: tuple[str, ...]
    unresolved_classical_semantic_requirements: tuple[str, ...]
    residual_unresolved_structural_constraint_ids: tuple[str, ...]
    source_unresolved_graph_requirements: tuple[str, ...]
    source_interaction_chain_pattern_ids: tuple[str, ...]


@dataclass(frozen=True)
class ChartBoundClassicalInteractionBundle:
    bundle_id: str
    binding_candidate_id: str
    source_occurrence_id: str
    graph_record_id: str
    structural_binding_class: str
    source_scope_specification: SourceScopeSpecification
    source_scope_compatibility: SourceScopeCompatibilityProjection
    neutral_observation_bundle: BindingScopedNeutralObservationBundle
    chart_bound_claims: tuple[ChartBoundSourceInteractionClaim, ...]
    residual_unresolved_structural_constraint_ids: tuple[str, ...]
    source_unresolved_graph_requirements: tuple[str, ...]
    source_interaction_chain_pattern_ids: tuple[str, ...]


@dataclass(frozen=True)
class ProjectionIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class ProjectionIntegrityReport:
    status: str
    diagnostics: tuple[ProjectionIntegrityDiagnostic, ...]
    algorithm_id: str = "BAZI-CHART-BOUND-CLASSICAL-INTERACTION-PROJECTION-INTEGRITY-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class ProjectionHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-CHART-BOUND-CLASSICAL-INTERACTION-PROJECTION-HASH-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class ChartBoundClassicalInteractionOuterCandidate:
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
    bundles: tuple[ChartBoundClassicalInteractionBundle, ...]
    algorithm_versions: Mapping[str, str]
    integrity: ProjectionIntegrityReport
    hashes: ProjectionHashBundle


@dataclass(frozen=True)
class BaziChartBoundClassicalInteractionProjectionResolution:
    schema: str
    status: str
    candidates: tuple[ChartBoundClassicalInteractionOuterCandidate, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
