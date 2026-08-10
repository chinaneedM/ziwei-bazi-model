from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping


@dataclass(frozen=True)
class StemRelationPositionalSnapshot:
    snapshot_id: str
    snapshot_fact_hash: str
    source_incidence_snapshot_id: str
    source_incidence_snapshot_fact_hash: str
    source_incidence_fact_hash: str
    source_incidence_computation_hash: str
    source_natal_fact_hash: str
    source_natal_computation_hash: str
    source_temporal_fact_hash: str
    source_flow_fact_hash: str
    source_flow_computation_hash: str
    source_structural_fact_hash: str
    source_structural_computation_hash: str
    source_support_fact_hash: str
    source_support_computation_hash: str
    target_utc: datetime
    profile_id: str
    profile_version: str
    rule_set_id: str
    rule_set_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class StemParticipantPositionReference:
    reference_id: str
    participant_instance_id: str
    stem: str
    element: str
    polarity: str
    participant_layer: str
    source_frame_id: str | None
    raw_position_token: str
    position_domain: str
    natal_pillar_ordinal: int | None
    is_natal_day_master_participant: bool
    source_upstream_fact_hash: str
    source_incidence_reference_ids: tuple[str, ...]
    rule_set_id: str
    rule_set_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class StemPairPositionalFact:
    positional_fact_id: str
    source_relation_reference_id: str
    source_relation_id: str
    source_semantic_relation_id: str
    source_relation_type: str
    source_relation_family: str
    participant_instance_ids: tuple[str, str]
    participant_position_reference_ids: tuple[str, str]
    position_domain_pair: tuple[str, str]
    natal_linear_order_comparable: bool
    natal_pillar_ordinals: tuple[int, ...]
    natal_ordinal_distance: int | None
    intervening_natal_visible_stem_instance_ids: tuple[str, ...]
    contains_natal_day_master_participant: bool
    natal_day_master_participant_instance_ids: tuple[str, ...]
    source_incidence_snapshot_id: str
    source_incidence_snapshot_fact_hash: str
    source_incidence_fact_hash: str
    rule_set_id: str
    rule_set_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class BaziStemRelationPositionalContext:
    snapshot: StemRelationPositionalSnapshot
    participant_position_references: tuple[StemParticipantPositionReference, ...]
    stem_pair_positional_facts: tuple[StemPairPositionalFact, ...]
    profile_id: str
    profile_version: str
    algorithm_versions: Mapping[str, str]


@dataclass(frozen=True)
class PositionalIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class PositionalIntegrityReport:
    status: str
    diagnostics: tuple[PositionalIntegrityDiagnostic, ...]
    algorithm_id: str = "BAZI-STEM-RELATION-POSITIONAL-INTEGRITY-V1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class PositionalHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-STEM-RELATION-POSITIONAL-HASH-V1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class BaziStemRelationPositionalCandidate:
    source_incidence_candidate_indices: tuple[int, ...]
    source_flow_candidate_indices: tuple[int, ...]
    source_structural_candidate_indices: tuple[int, ...]
    source_support_candidate_indices: tuple[int, ...]
    source_temporal_candidate_indices: tuple[int, ...]
    source_temporal_seed_ids: tuple[str, ...]
    source_incidence_lineage_binding_keys: tuple[str, ...]
    lineage_binding_keys: tuple[str, ...]
    context: BaziStemRelationPositionalContext
    integrity: PositionalIntegrityReport
    hashes: PositionalHashBundle


@dataclass(frozen=True)
class BaziStemRelationPositionalResolution:
    schema: str
    status: str
    candidates: tuple[BaziStemRelationPositionalCandidate, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
