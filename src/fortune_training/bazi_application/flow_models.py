from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from fortune_training.bazi_target_temporal import (
    ResolvedTargetTemporalCoordinateProfile,
    TargetTemporalInput,
)

from .models import BaziApplicationRequest


FLOW_APPLICATION_SCHEMA = "BAZI-APPLICATION-FLOW-RESOLUTION-R1"
FLOW_APPLICATION_VIEW_SCHEMA = "BAZI-APPLICATION-FLOW-VIEW-R1"
FLOW_APPLICATION_ALGORITHM_ID = "BAZI-APPLICATION-FLOW-COMPOSER-R1"
FLOW_APPLICATION_ALGORITHM_VERSION = "1.0.0"
FLOW_APPLICATION_INTEGRITY_ALGORITHM_ID = "BAZI-APPLICATION-FLOW-INTEGRITY-R1"
FLOW_APPLICATION_INTEGRITY_ALGORITHM_VERSION = "1.0.0"


@dataclass(frozen=True)
class BaziApplicationFlowRequest:
    application_request: BaziApplicationRequest
    target_input: TargetTemporalInput
    target_coordinate_profile: ResolvedTargetTemporalCoordinateProfile


@dataclass(frozen=True)
class BaziApplicationFlowCandidate:
    candidate_id: str
    natal_candidate_index: int
    source_temporal_candidate_indices: tuple[int, ...]
    source_application_candidate_ids: tuple[str, ...]
    source_flow_candidate_index: int
    source_target_coordinate_candidate_index: int
    target_coordinate_candidate_id: str
    natal_fact_hash: str
    temporal_fact_hash: str
    flow_fact_hash: str
    flow_computation_hash: str
    daily_hourly_fact_hash: str
    daily_hourly_computation_hash: str
    view_schema: str
    view: Mapping[str, Any]
    view_hash: str


@dataclass(frozen=True)
class BaziApplicationFlowIntegrityReport:
    status: str
    diagnostics: tuple[str, ...]
    algorithm_id: str = FLOW_APPLICATION_INTEGRITY_ALGORITHM_ID
    algorithm_version: str = FLOW_APPLICATION_INTEGRITY_ALGORITHM_VERSION


@dataclass(frozen=True)
class BaziApplicationFlowResolution:
    schema: str
    status: str
    base_application_bundle_hash: str
    base_application_source_fact_hash: str
    application_profile_id: str
    application_profile_version: str
    natal_profile_id: str
    natal_profile_version: str
    temporal_profile_id: str
    temporal_profile_version: str
    target_coordinate_profile_id: str
    target_coordinate_profile_version: str
    dayun_count: int
    target_input: TargetTemporalInput
    target_coordinate_status: str
    target_coordinate_effective_uncertainty_seconds_each_side: int
    target_coordinate_sample_count: int
    target_coordinate_ambiguous_sample_count: int
    target_coordinate_unresolved_samples: tuple[Mapping[str, Any], ...]
    target_coordinate_fact_hash: str
    target_coordinate_computation_hash: str
    candidates: tuple[BaziApplicationFlowCandidate, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
    source_fact_hash: str
    view_hash: str
    bundle_hash: str
    integrity: BaziApplicationFlowIntegrityReport
