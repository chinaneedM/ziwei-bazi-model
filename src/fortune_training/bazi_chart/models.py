from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping


@dataclass(frozen=True)
class GenerationTrace:
    operation: str
    algorithm_id: str
    algorithm_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class PillarState:
    position: str
    ganzhi: str
    sexagenary_index: int
    stem_instance_id: str
    branch_instance_id: str


@dataclass(frozen=True)
class StemInstance:
    instance_id: str
    position: str
    stem: str
    element: str
    polarity: str


@dataclass(frozen=True)
class BranchInstance:
    instance_id: str
    position: str
    branch: str
    element_affiliation: str


@dataclass(frozen=True)
class HiddenStemMembership:
    instance_id: str
    branch_instance_id: str
    branch_position: str
    stem: str
    element: str
    registry_ordinal: int
    rule_set_id: str
    rule_set_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class TenGodBinding:
    binding_id: str
    target_instance_id: str
    target_stem: str
    day_master_stem: str
    semantic_role_id: str
    display_name: str
    rule_set_id: str
    rule_set_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class HiddenStemExposureLink:
    link_id: str
    hidden_stem_instance_id: str
    visible_stem_instance_id: str
    stem: str
    match_kind: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class StemBranchAffinityFact:
    fact_id: str
    visible_stem_instance_id: str
    branch_instance_id: str
    exact_hidden_stem_instance_ids: tuple[str, ...]
    same_element_hidden_stem_instance_ids: tuple[str, ...]
    rule_set_id: str
    rule_set_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class RelationCandidate:
    relation_id: str
    semantic_relation_id: str
    relation_family: str
    participant_instance_ids: tuple[str, ...]
    orientation: str
    arity: int
    nominal_transformation_element: str | None
    rule_set_id: str
    rule_set_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class BaziNatalState:
    pillars: tuple[PillarState, ...]
    stems: tuple[StemInstance, ...]
    branches: tuple[BranchInstance, ...]
    hidden_stems: tuple[HiddenStemMembership, ...]
    ten_gods: tuple[TenGodBinding, ...]
    exposures: tuple[HiddenStemExposureLink, ...]
    affinities: tuple[StemBranchAffinityFact, ...]
    raw_relations: tuple[RelationCandidate, ...]
    day_master_stem: str
    profile_id: str
    profile_version: str
    algorithm_versions: Mapping[str, str]
    trace: tuple[GenerationTrace, ...]


@dataclass(frozen=True)
class BaziTemporalSeed:
    seed_id: str
    source_time_branch_index: int
    sample_reported_local_datetime: datetime
    birth_utc: datetime
    local_apparent_solar_datetime: datetime
    previous_jie_name: str
    previous_jie_utc: datetime
    next_jie_name: str
    next_jie_utc: datetime
    input_uncertainty_seconds_each_side: int
    time_calendar_policy_registry_version: str


@dataclass(frozen=True)
class IntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class IntegrityReport:
    status: str
    diagnostics: tuple[IntegrityDiagnostic, ...]
    algorithm_id: str = "BAZI-NATAL-INTEGRITY-V1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class HashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-NATAL-HASH-V1"
    algorithm_version: str = "1.0.0"
