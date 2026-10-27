from __future__ import annotations

from dataclasses import dataclass

from fortune_training.ziwei_chart.models import Address
from fortune_training.ziwei_structural.r2 import RelativePalaceRoleFact
from fortune_training.ziwei_structural.r5 import ResolvedSanfangSizhengFrameFact

from .models import ApplicationBirthRequest


SANHE_INTERACTION_SCHEMA = "ZIWEI-SANHE-INTERACTION-RESOLUTION-R1"
SANHE_INTERACTION_MODE = "SANHE"
SANHE_INTERACTION_ALGORITHM_ID = "ZIWEI-SANHE-INTERACTION-CONTROLLER-R1"
SANHE_INTERACTION_ALGORITHM_VERSION = "1.0.0"
SANHE_INTERACTION_INTEGRITY_ALGORITHM_ID = "ZIWEI-SANHE-INTERACTION-INTEGRITY-R1"
SANHE_INTERACTION_INTEGRITY_ALGORITHM_VERSION = "1.0.0"


@dataclass(frozen=True)
class SanheInteractionRequest:
    application_request: ApplicationBirthRequest
    origin_designation_id: str

    def __post_init__(self) -> None:
        if not self.origin_designation_id.strip():
            raise ValueError("origin_designation_id must not be empty")


@dataclass(frozen=True)
class SanheInteractionIntegrityReport:
    status: str
    diagnostics: tuple[str, ...]
    algorithm_id: str = SANHE_INTERACTION_INTEGRITY_ALGORITHM_ID
    algorithm_version: str = SANHE_INTERACTION_INTEGRITY_ALGORITHM_VERSION


@dataclass(frozen=True)
class SanheInteractionResolution:
    schema: str
    status: str
    interaction_mode: str
    source_application_bundle_hash: str
    source_application_resolution_status: str
    selected_daxian_frame_id: str | None
    selected_annual_year: int | None
    selected_minor_limit_age: int | None
    selected_origin_designation_id: str
    selected_origin_address: Address
    relative_roles: tuple[RelativePalaceRoleFact, ...]
    sanfang_sizheng_frame: ResolvedSanfangSizhengFrameFact
    r2_fact_hash: str
    r2_computation_hash: str
    r3_fact_hash: str
    r3_computation_hash: str
    r4_fact_hash: str
    r4_computation_hash: str
    r5_fact_hash: str
    r5_computation_hash: str
    source_fact_hash: str
    view_hash: str
    bundle_hash: str
    integrity: SanheInteractionIntegrityReport
