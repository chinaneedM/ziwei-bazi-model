from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from fortune_training.bazi_chart import (
    BranchInstance,
    HiddenStemExposureLink,
    HiddenStemMembership,
    StemBranchAffinityFact,
    StemInstance,
    TenGodBinding,
)


@dataclass(frozen=True)
class TemporalParticipantProvenance:
    instance_id: str
    layer: str
    source_frame_id: str
    source_flow_fact_hash: str
    source_ganzhi: str


@dataclass(frozen=True)
class DynamicRelationOccurrence:
    relation_id: str
    semantic_relation_id: str
    relation_family: str
    participant_instance_ids: tuple[str, ...]
    participant_layers: tuple[str, ...]
    relation_scope: str
    orientation: str
    arity: int
    nominal_transformation_element: str | None
    rule_set_id: str
    rule_set_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class BaziStructuralContext:
    upstream_natal_fact_hash: str
    upstream_temporal_fact_hash: str
    upstream_flow_fact_hash: str
    natal_day_master_stem: str
    natal_stem_instance_ids: tuple[str, ...]
    natal_branch_instance_ids: tuple[str, ...]
    active_temporal_stems: tuple[StemInstance, ...]
    active_temporal_branches: tuple[BranchInstance, ...]
    temporal_participant_provenance: tuple[TemporalParticipantProvenance, ...]
    temporal_hidden_stems: tuple[HiddenStemMembership, ...]
    temporal_ten_gods: tuple[TenGodBinding, ...]
    upstream_natal_exposure_link_ids: tuple[str, ...]
    dynamic_exposures: tuple[HiddenStemExposureLink, ...]
    upstream_natal_affinity_fact_ids: tuple[str, ...]
    dynamic_affinities: tuple[StemBranchAffinityFact, ...]
    upstream_natal_raw_relation_ids: tuple[str, ...]
    dynamic_raw_relations: tuple[DynamicRelationOccurrence, ...]
    profile_id: str
    profile_version: str
    algorithm_versions: Mapping[str, str]


@dataclass(frozen=True)
class StructuralIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class StructuralIntegrityReport:
    status: str
    diagnostics: tuple[StructuralIntegrityDiagnostic, ...]
    algorithm_id: str = "BAZI-STRUCTURAL-INTEGRITY-V1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class StructuralHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-STRUCTURAL-HASH-V1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class BaziStructuralCandidate:
    source_flow_candidate_indices: tuple[int, ...]
    source_temporal_candidate_indices: tuple[int, ...]
    source_temporal_seed_ids: tuple[str, ...]
    context: BaziStructuralContext
    integrity: StructuralIntegrityReport
    hashes: StructuralHashBundle


@dataclass(frozen=True)
class BaziStructuralResolution:
    schema: str
    status: str
    candidates: tuple[BaziStructuralCandidate, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
