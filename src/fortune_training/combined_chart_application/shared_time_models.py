from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from fortune_training.ziwei_chart.models import DesignationBinding, TransformationActivation


SHARED_ZIWEI_SELECTOR_PROJECTION_SCHEMA = "SHARED-ZIWEI-SELECTOR-PROJECTION-RESOLUTION-R1"
SHARED_ZIWEI_SELECTOR_PROJECTION_ALGORITHM_ID = "SHARED-TARGET-ZIWEI-SELECTOR-PROJECTION-R1"
SHARED_ZIWEI_SELECTOR_PROJECTION_ALGORITHM_VERSION = "1.4.0"
SHARED_ZIWEI_SELECTOR_PROJECTION_INTEGRITY_ALGORITHM_ID = (
    "SHARED-TARGET-ZIWEI-SELECTOR-PROJECTION-INTEGRITY-R1"
)
SHARED_ZIWEI_SELECTOR_PROJECTION_INTEGRITY_ALGORITHM_VERSION = "1.4.0"
SHARED_ZIWEI_SELECTOR_PROJECTION_HASH_ALGORITHM_ID = (
    "SHARED-TARGET-ZIWEI-SELECTOR-PROJECTION-HASH-R1"
)
SHARED_ZIWEI_SELECTOR_PROJECTION_HASH_ALGORITHM_VERSION = "1.4.0"


@dataclass(frozen=True)
class SharedZiweiHourlyMethodCandidate:
    candidate_id: str
    time_standard: str
    source_local_datetime: datetime
    ziwei_day_boundary_policy: str
    effective_gregorian_date: str
    day_ganzhi: str
    hour_branch: str
    hour_ganzhi: str
    frame_status: str
    active_address_branch: str | None
    designation_overlay: tuple[DesignationBinding, ...]
    active_address_rule_id: str
    active_address_source_refs: tuple[str, ...]
    transformation_status: str
    transformation_rule_set_id: str | None
    transformation_rule_set_version: str | None
    transformations: tuple[TransformationActivation, ...]
    transformation_source_refs: tuple[str, ...]
    rule_id: str
    authority_status: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class SharedZiweiSelectorProjectionCandidate:
    source_target_candidate_index: int
    source_target_candidate_id: str
    source_sample_index: int
    sample_reported_local_datetime: datetime
    target_utc: datetime
    fold: int
    civil_year: int
    source_annual_frame_id: str
    annual_year: int
    minor_limit_age: int
    daxian_frame_id: str | None
    ziwei_calendar_date_policy: str
    ziwei_day_boundary_policy: str
    effective_lunar_year: int
    effective_lunar_month: int
    effective_lunar_day: int
    effective_lunar_is_leap_month: bool
    monthly_projection_status: str
    monthly_frame_id: str | None
    monthly_ganzhi: str | None
    monthly_active_address_branch: str | None
    daily_projection_status: str
    daily_frame_id: str | None
    daily_effective_gregorian_date: str | None
    daily_ganzhi: str | None
    daily_active_address_branch: str | None
    daily_designation_overlay: tuple[DesignationBinding, ...]
    daily_rule_id: str | None
    daily_source_refs: tuple[str, ...]
    daily_transformation_status: str
    daily_transformation_rule_set_id: str | None
    daily_transformation_rule_set_version: str | None
    daily_transformations: tuple[TransformationActivation, ...]
    daily_transformation_source_refs: tuple[str, ...]
    hourly_projection_status: str
    hourly_method_candidates: tuple[SharedZiweiHourlyMethodCandidate, ...]
    candidate_hash: str


@dataclass(frozen=True)
class SharedZiweiSelectorProjectionIntegrityReport:
    status: str
    diagnostics: tuple[str, ...]
    algorithm_id: str = SHARED_ZIWEI_SELECTOR_PROJECTION_INTEGRITY_ALGORITHM_ID
    algorithm_version: str = SHARED_ZIWEI_SELECTOR_PROJECTION_INTEGRITY_ALGORITHM_VERSION


@dataclass(frozen=True)
class SharedZiweiSelectorProjectionHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = SHARED_ZIWEI_SELECTOR_PROJECTION_HASH_ALGORITHM_ID
    algorithm_version: str = SHARED_ZIWEI_SELECTOR_PROJECTION_HASH_ALGORITHM_VERSION


@dataclass(frozen=True)
class SharedZiweiSelectorProjectionResolution:
    schema: str
    status: str
    source_ziwei_application_bundle_hash: str
    source_ziwei_temporal_fact_hash: str
    source_ziwei_temporal_computation_hash: str
    source_target_coordinate_fact_hash: str
    source_target_coordinate_computation_hash: str
    source_target_coordinate_profile_id: str
    source_target_coordinate_profile_version: str
    candidates: tuple[SharedZiweiSelectorProjectionCandidate, ...]
    hashes: SharedZiweiSelectorProjectionHashBundle
    integrity: SharedZiweiSelectorProjectionIntegrityReport
