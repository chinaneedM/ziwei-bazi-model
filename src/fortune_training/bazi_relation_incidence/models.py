from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping


@dataclass(frozen=True)
class RelationIncidenceSnapshot:
    snapshot_id: str
    snapshot_fact_hash: str
    target_utc: datetime
    upstream_natal_fact_hash: str
    upstream_natal_computation_hash: str
    upstream_temporal_fact_hash: str
    source_temporal_candidate_indices: tuple[int, ...]
    source_temporal_seed_ids: tuple[str, ...]
    upstream_flow_fact_hash: str
    upstream_flow_computation_hash: str
    upstream_structural_fact_hash: str
    upstream_structural_computation_hash: str
    upstream_support_fact_hash: str
    upstream_support_computation_hash: str
    active_dayun_kind: str
    active_dayun_source_frame_id: str
    annual_frame_id: str
    monthly_frame_id: str
    raw_relation_ids: tuple[str, ...]
    rule_set_id: str
    rule_set_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class IncidenceParticipantReference:
    instance_id: str
    participant_kind: str
    value: str
    participant_layer: str
    source_frame_id: str | None
    source_upstream_fact_hash: str
    source_ganzhi: str | None


@dataclass(frozen=True)
class RelationOccurrenceReference:
    reference_id: str
    relation_id: str
    semantic_relation_id: str
    relation_type: str
    relation_family: str
    participant_instance_ids: tuple[str, ...]
    participant_layers: tuple[str, ...]
    participant_provenance: tuple[IncidenceParticipantReference, ...]
    relation_scope: str
    orientation: str
    arity: int
    nominal_transformation_element: str | None
    nominal_transformation_semantics: str | None
    source_occurrence_kind: str
    source_upstream_fact_hash: str
    source_relation_rule_set_id: str
    source_relation_rule_set_version: str
    reference_rule_set_id: str
    reference_rule_set_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class ParticipantRelationIncidenceFact:
    incidence_fact_id: str
    participant_instance_id: str
    participant_kind: str
    value: str
    participant_layer: str
    source_frame_id: str | None
    source_ganzhi: str | None
    relation_ids: tuple[str, ...]
    relation_count: int
    support_evidence_candidate_ids: tuple[str, ...]
    seasonal_role_ids: tuple[str, ...]
    seasonal_role_reference_ids: tuple[str, ...]
    source_participant_fact_hash: str
    source_relation_fact_hashes: tuple[str, ...]
    source_support_fact_hash: str
    snapshot_id: str
    snapshot_fact_hash: str
    rule_set_id: str
    rule_set_version: str
    support_touch_rule_set_id: str
    support_touch_rule_set_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class RelationPairTopologyFact:
    pair_fact_id: str
    relation_ids: tuple[str, str]
    topology_kind: str
    shared_participant_instance_ids: tuple[str, ...]
    left_only_participant_instance_ids: tuple[str, ...]
    right_only_participant_instance_ids: tuple[str, ...]
    participant_layer_provenance: tuple[IncidenceParticipantReference, ...]
    source_snapshot_id: str
    source_snapshot_fact_hash: str
    profile_id: str
    profile_version: str
    rule_set_id: str
    rule_set_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class BaziRelationIncidenceContext:
    snapshot: RelationIncidenceSnapshot
    relation_occurrences: tuple[RelationOccurrenceReference, ...]
    participant_incidence_facts: tuple[ParticipantRelationIncidenceFact, ...]
    relation_pair_topology_facts: tuple[RelationPairTopologyFact, ...]
    profile_id: str
    profile_version: str
    algorithm_versions: Mapping[str, str]


@dataclass(frozen=True)
class IncidenceIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class IncidenceIntegrityReport:
    status: str
    diagnostics: tuple[IncidenceIntegrityDiagnostic, ...]
    algorithm_id: str = "BAZI-RELATION-INCIDENCE-INTEGRITY-V1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class IncidenceHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-RELATION-INCIDENCE-HASH-V1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class BaziRelationIncidenceCandidate:
    source_flow_candidate_indices: tuple[int, ...]
    source_structural_candidate_indices: tuple[int, ...]
    source_support_candidate_indices: tuple[int, ...]
    source_temporal_candidate_indices: tuple[int, ...]
    source_temporal_seed_ids: tuple[str, ...]
    lineage_binding_keys: tuple[str, ...]
    context: BaziRelationIncidenceContext
    integrity: IncidenceIntegrityReport
    hashes: IncidenceHashBundle


@dataclass(frozen=True)
class BaziRelationIncidenceResolution:
    schema: str
    status: str
    candidates: tuple[BaziRelationIncidenceCandidate, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
