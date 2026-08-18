from __future__ import annotations

from dataclasses import dataclass

from fortune_training.bazi_target_temporal import (
    ResolvedTargetTemporalCoordinateProfile,
    TargetTemporalInput,
)

from .models import CombinedChartApplicationRequest


COMBINED_TARGET_FLOW_SCHEMA = "ZIWEI-BAZI-COMBINED-TARGET-FLOW-RESOLUTION-R1"
COMBINED_TARGET_FLOW_ALGORITHM_ID = "ZIWEI-BAZI-COMBINED-TARGET-FLOW-COMPOSER-R1"
COMBINED_TARGET_FLOW_ALGORITHM_VERSION = "1.0.0"
COMBINED_TARGET_FLOW_INTEGRITY_ALGORITHM_ID = (
    "ZIWEI-BAZI-COMBINED-TARGET-FLOW-INTEGRITY-R1"
)
COMBINED_TARGET_FLOW_INTEGRITY_ALGORITHM_VERSION = "1.0.0"


@dataclass(frozen=True)
class CombinedTargetFlowRequest:
    combined_request: CombinedChartApplicationRequest
    target_input: TargetTemporalInput
    target_coordinate_profile: ResolvedTargetTemporalCoordinateProfile


@dataclass(frozen=True)
class CombinedTargetFlowIntegrityReport:
    status: str
    diagnostics: tuple[str, ...]
    algorithm_id: str = COMBINED_TARGET_FLOW_INTEGRITY_ALGORITHM_ID
    algorithm_version: str = COMBINED_TARGET_FLOW_INTEGRITY_ALGORITHM_VERSION


@dataclass(frozen=True)
class CombinedTargetFlowResolution:
    schema: str
    status: str
    combined_profile_id: str
    combined_profile_version: str
    composition_semantics: str
    base_combined_status: str
    base_combined_manifest_hash: str
    ziwei_bundle_hash: str
    ziwei_resolution_status: str
    ziwei_selected_daxian_frame_id: str | None
    ziwei_selected_annual_year: int | None
    ziwei_selected_minor_limit_age: int | None
    bazi_base_bundle_hash: str
    bazi_dayun_count: int
    bazi_target_flow_status: str
    bazi_target_flow_source_fact_hash: str
    bazi_target_flow_view_hash: str
    bazi_target_flow_bundle_hash: str
    target_coordinate_fact_hash: str
    target_coordinate_computation_hash: str
    target_coordinate_profile_id: str
    target_coordinate_profile_version: str
    target_input: TargetTemporalInput
    source_fact_hash: str
    view_hash: str
    bundle_hash: str
    integrity: CombinedTargetFlowIntegrityReport
