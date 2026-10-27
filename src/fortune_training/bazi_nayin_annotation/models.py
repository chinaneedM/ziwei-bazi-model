from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NayinPillarAnnotation:
    annotation_id: str
    source_pillar_position: str
    source_pillar_ganzhi: str
    source_pillar_sexagenary_index: int
    source_stem_instance_id: str
    source_branch_instance_id: str
    nayin_semantic_id: str
    display_name: str
    element: str
    registry_id: str
    registry_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class NayinIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class NayinIntegrityReport:
    status: str
    diagnostics: tuple[NayinIntegrityDiagnostic, ...]
    algorithm_id: str = "BAZI-NAYIN-INTEGRITY-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class BaziNayinAnnotationResolution:
    schema: str
    annotation_profile_id: str
    annotation_profile_version: str
    registry_id: str
    registry_version: str
    registry_origin: str
    registry_hash: str
    source_natal_fact_hash: str
    source_natal_computation_hash: str
    annotations: tuple[NayinPillarAnnotation, ...]
    fact_hash: str
    computation_hash: str
    integrity: NayinIntegrityReport
