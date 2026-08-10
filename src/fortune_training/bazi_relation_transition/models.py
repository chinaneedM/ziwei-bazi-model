from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping


@dataclass(frozen=True)
class RelationSnapshotReference:
    snapshot_id: str
    snapshot_role: str
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
class RelationParticipantReference:
    instance_id: str
    participant_kind: str
    value: str
    participant_layer: str
    source_frame_id: str | None
    source_upstream_fact_hash: str
    source_ganzhi: str | None


@dataclass(frozen=True)
class FrameChangeEvidence:
    evidence_id: str
    evidence_type: str
    participant_layer: str
    before_source_frame_id: str
    after_source_frame_id: str
    exited_participant_instance_ids: tuple[str, ...]
    entered_participant_instance_ids: tuple[str, ...]
    before_flow_fact_hash: str
    after_flow_fact_hash: str
    rule_set_id: str
    rule_set_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class RawRelationTransitionFact:
    transition_fact_id: str
    relation_id: str
    semantic_relation_id: str
    relation_type: str
    relation_family: str
    participant_instance_ids: tuple[str, ...]
    participant_layers: tuple[str, ...]
    occurrence_scope: str
    orientation: str
    arity: int
    nominal_transformation_element: str | None
    transition_state: str
    before_snapshot_id: str
    before_snapshot_fact_hash: str
    after_snapshot_id: str
    after_snapshot_fact_hash: str
    before_participant_provenance: tuple[RelationParticipantReference, ...]
    after_participant_provenance: tuple[RelationParticipantReference, ...]
    bound_frame_change_evidence_ids: tuple[str, ...]
    source_relation_rule_set_id: str
    source_relation_rule_set_version: str
    transition_rule_set_id: str
    transition_rule_set_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class BaziRelationTransitionContext:
    before_snapshot: RelationSnapshotReference
    after_snapshot: RelationSnapshotReference
    frame_change_evidence: tuple[FrameChangeEvidence, ...]
    transition_facts: tuple[RawRelationTransitionFact, ...]
    profile_id: str
    profile_version: str
    algorithm_versions: Mapping[str, str]


@dataclass(frozen=True)
class TransitionIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class TransitionIntegrityReport:
    status: str
    diagnostics: tuple[TransitionIntegrityDiagnostic, ...]
    algorithm_id: str = "BAZI-RELATION-TRANSITION-INTEGRITY-V1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class TransitionHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-RELATION-TRANSITION-HASH-V1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class BaziRelationTransitionCandidate:
    source_before_flow_candidate_indices: tuple[int, ...]
    source_before_structural_candidate_indices: tuple[int, ...]
    source_before_support_candidate_indices: tuple[int, ...]
    source_after_flow_candidate_indices: tuple[int, ...]
    source_after_structural_candidate_indices: tuple[int, ...]
    source_after_support_candidate_indices: tuple[int, ...]
    paired_temporal_candidate_indices: tuple[int, ...]
    paired_temporal_seed_ids: tuple[str, ...]
    lineage_pairing_keys: tuple[str, ...]
    context: BaziRelationTransitionContext
    integrity: TransitionIntegrityReport
    hashes: TransitionHashBundle


@dataclass(frozen=True)
class BaziRelationTransitionResolution:
    schema: str
    status: str
    candidates: tuple[BaziRelationTransitionCandidate, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
