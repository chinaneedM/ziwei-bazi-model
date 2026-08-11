from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping


@dataclass(frozen=True)
class SourceGraphBindabilityPlan:
    graph_record_id: str
    source_occurrence_id: str
    graph_record_sha256: str
    source_unresolved_graph_requirements: tuple[str, ...]
    bindability_class: str
    exact_relation_pattern_node_ids: tuple[str, ...]
    exact_position_constraint_ids: tuple[str, ...]
    unresolved_structural_constraint_ids: tuple[str, ...]
    structural_reason_ids: tuple[str, ...]


@dataclass(frozen=True)
class SourceParticipantExactBinding:
    participant_pattern_node_ids: tuple[str, ...]
    participant_kind: str
    literal_value: str
    runtime_instance_ids: tuple[str, ...]
    position_reference_ids: tuple[str, ...]
    participant_layers: tuple[str, ...]
    source_frame_ids: tuple[str | None, ...]
    raw_position_tokens: tuple[str, ...]
    source_evidence_mode: str


@dataclass(frozen=True)
class SourceRelationExactBinding:
    relation_pattern_node_id: str
    source_relation_reference_id: str
    source_relation_id: str
    source_semantic_relation_id: str
    positional_fact_id: str
    source_relation_type: str
    source_relation_family: str
    source_orientation: str
    source_arity: int
    source_participant_pattern_path: tuple[str, ...]
    runtime_participant_instance_ids: tuple[str, ...]
    participant_position_reference_ids: tuple[str, ...]
    source_evidence_mode: str


@dataclass(frozen=True)
class SourcePositionConstraintExactBinding:
    position_constraint_id: str
    constraint_status: str
    evidence_mode: str
    natal_pillar: str | None
    participant_pattern_node_ids: tuple[str, ...]
    runtime_instance_ids: tuple[str, ...]
    position_reference_ids: tuple[str, ...]
    raw_position_tokens: tuple[str, ...]
    replay_status: str


@dataclass(frozen=True)
class SourceMultiplicityExactBinding:
    multiplicity_constraint_id: str
    exchangeable_symbolic_slot_node_ids: tuple[str, ...]
    exact_runtime_instance_ids: tuple[str, ...]
    required_symbolic_cardinality: int
    slot_equivalence: str
    alternative_path_requirement: str


@dataclass(frozen=True)
class ChartSpecificExactBindingCandidate:
    binding_candidate_id: str
    normalized_assignment_signature: str
    graph_record_id: str
    source_occurrence_id: str
    relation_bindings: tuple[SourceRelationExactBinding, ...]
    participant_bindings: tuple[SourceParticipantExactBinding, ...]
    position_constraint_bindings: tuple[SourcePositionConstraintExactBinding, ...]
    multiplicity_bindings: tuple[SourceMultiplicityExactBinding, ...]
    residual_unresolved_structural_constraint_ids: tuple[str, ...]
    source_interaction_claim_edge_ids: tuple[str, ...]
    source_interaction_chain_pattern_ids: tuple[str, ...]


@dataclass(frozen=True)
class SourceGraphBindingInventory:
    graph_record_id: str
    source_occurrence_id: str
    bindability_class: str
    inventory_status: str
    source_unresolved_graph_requirements: tuple[str, ...]
    structural_reason_ids: tuple[str, ...]
    unresolved_structural_constraint_ids: tuple[str, ...]
    binding_candidates: tuple[ChartSpecificExactBindingCandidate, ...]


@dataclass(frozen=True)
class ChartSourcePatternBindingSnapshot:
    snapshot_id: str
    snapshot_fact_hash: str
    target_utc: datetime
    source_graph_artifact_semantics_sha256: str
    source_graph_record_hash_chain_sha256: str
    source_natal_fact_hash: str
    source_natal_computation_hash: str
    source_incidence_snapshot_id: str
    source_incidence_snapshot_fact_hash: str
    source_incidence_fact_hash: str
    source_incidence_computation_hash: str
    source_branch_positional_snapshot_id: str
    source_branch_positional_fact_hash: str
    source_branch_positional_computation_hash: str
    source_stem_positional_snapshot_id: str
    source_stem_positional_fact_hash: str
    source_stem_positional_computation_hash: str
    profile_id: str
    profile_version: str
    rule_set_id: str
    rule_set_version: str


@dataclass(frozen=True)
class BindingIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class BindingIntegrityReport:
    status: str
    diagnostics: tuple[BindingIntegrityDiagnostic, ...]
    algorithm_id: str = "BAZI-CHART-SOURCE-PATTERN-BINDING-INTEGRITY-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class BindingHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-CHART-SOURCE-PATTERN-BINDING-HASH-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class ChartSourcePatternBindingOuterCandidate:
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
    snapshot: ChartSourcePatternBindingSnapshot
    graph_binding_inventory: tuple[SourceGraphBindingInventory, ...]
    algorithm_versions: Mapping[str, str]
    integrity: BindingIntegrityReport
    hashes: BindingHashBundle


@dataclass(frozen=True)
class BaziChartSourcePatternBindingResolution:
    schema: str
    status: str
    bindability_plan: tuple[SourceGraphBindabilityPlan, ...]
    candidates: tuple[ChartSourcePatternBindingOuterCandidate, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
