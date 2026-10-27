from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


TEMPORAL_SHENSHA_SIDECAR_SCHEMA = "BAZI-TEMPORAL-SHENSHA-PROJECTION-SIDECAR-R1"
TEMPORAL_SHENSHA_SIDECAR_PROFILE_ID = "BAZI-TEMPORAL-SHENSHA-PROJECTION-SIDECAR-R1"
TEMPORAL_SHENSHA_SIDECAR_PROFILE_VERSION = "1.0.0"
TEMPORAL_SHENSHA_SIDECAR_ALGORITHM_ID = "BAZI-TEMPORAL-SHENSHA-SIDECAR-COMPOSER-R1"
TEMPORAL_SHENSHA_SIDECAR_ALGORITHM_VERSION = "1.0.0"
TEMPORAL_SHENSHA_SIDECAR_INTEGRITY_ID = "BAZI-TEMPORAL-SHENSHA-SIDECAR-INTEGRITY-R1"
TEMPORAL_SHENSHA_SIDECAR_INTEGRITY_VERSION = "1.0.0"
TEMPORAL_SHENSHA_SIDECAR_HASH_ID = "BAZI-TEMPORAL-SHENSHA-SIDECAR-HASH-R1"
TEMPORAL_SHENSHA_SIDECAR_HASH_VERSION = "1.0.0"


@dataclass(frozen=True)
class TemporalShenshaSidecarIntegrityReport:
    status: str
    diagnostics: tuple[str, ...]
    algorithm_id: str = TEMPORAL_SHENSHA_SIDECAR_INTEGRITY_ID
    algorithm_version: str = TEMPORAL_SHENSHA_SIDECAR_INTEGRITY_VERSION


@dataclass(frozen=True)
class TemporalShenshaSidecarCandidate:
    candidate_id: str
    source_bazi_target_flow_candidate_id: str
    source_bazi_target_flow_candidate_index: int
    source_flow_candidate_index: int
    source_target_coordinate_candidate_index: int
    target_coordinate_candidate_id: str
    source_application_candidate_ids: tuple[str, ...]
    source_application_view_hashes: tuple[str, ...]
    source_shensha_hash: str
    projection: Mapping[str, Any]
    fact_hash: str
    computation_hash: str


@dataclass(frozen=True)
class TemporalShenshaSidecarResolution:
    schema: str
    status: str
    base_application_bundle_hash: str
    base_application_source_fact_hash: str
    bazi_target_flow_bundle_hash: str
    bazi_target_flow_source_fact_hash: str
    projection_profile_id: str
    projection_profile_version: str
    candidates: tuple[TemporalShenshaSidecarCandidate, ...]
    diagnostics: tuple[str, ...]
    fact_hash: str
    computation_hash: str
    bundle_hash: str
    integrity: TemporalShenshaSidecarIntegrityReport
