from __future__ import annotations

from dataclasses import dataclass, field

from fortune_training.calendar_foundation import BirthInput
from fortune_training.ziwei_chart import (
    ChartViewModel,
    HashBundle,
    PresentationProfile,
    ResolvedZiweiCalculationProfile,
    Sex,
    TemporalNatalContext,
    ZiweiChartCandidate,
    ZiweiTemporalState,
)
from fortune_training.ziwei_structural import StructuralState
from fortune_training.ziwei_structural.r2 import RelativePalaceFrameState
from fortune_training.ziwei_structural.r3 import BorrowProjectionState
from fortune_training.ziwei_structural.r4 import NamedStructuralSemanticState
from fortune_training.ziwei_structural.r5 import ResolvedSanfangSizhengViewState

from .profile import (
    ZiweiApplicationProfile,
    ziwei_application_default_presentation_profile,
)


APPLICATION_CHART_BUNDLE_SCHEMA = "ZIWEI-APPLICATION-CHART-BUNDLE-V1"


@dataclass(frozen=True)
class ApplicationBirthRequest:
    birth: BirthInput
    sex: Sex
    calculation_profile: ResolvedZiweiCalculationProfile
    presentation_profile: PresentationProfile = field(
        default_factory=ziwei_application_default_presentation_profile
    )
    daxian_frame_id: str | None = None
    annual_year: int | None = None
    lunar_month: int | None = None
    minor_limit_age: int | None = None
    daxian_count: int = 12
    max_nominal_age: int | None = None

    def __post_init__(self) -> None:
        if self.daxian_count <= 0:
            raise ValueError("daxian_count must be positive")
        if self.minor_limit_age is not None and self.minor_limit_age < 1:
            raise ValueError("minor_limit_age must be positive")
        if self.lunar_month is not None:
            if self.annual_year is None:
                raise ValueError("lunar_month requires annual_year")
            if not 1 <= self.lunar_month <= 12:
                raise ValueError("lunar_month must be in [1, 12]")
        if self.max_nominal_age is not None and self.max_nominal_age < 1:
            raise ValueError("max_nominal_age must be positive")
        if self.daxian_frame_id is not None and not self.daxian_frame_id.strip():
            raise ValueError("daxian_frame_id must not be empty")


@dataclass(frozen=True)
class ApplicationChartBundle:
    application_profile: ZiweiApplicationProfile
    resolution_status: str
    calculation_profile: ResolvedZiweiCalculationProfile
    presentation_profile: PresentationProfile
    selected_daxian_frame_id: str | None
    selected_annual_year: int | None
    selected_lunar_month: int | None
    selected_minor_limit_age: int | None
    candidate: ZiweiChartCandidate
    temporal_context: TemporalNatalContext
    temporal_state: ZiweiTemporalState
    temporal_hashes: HashBundle
    r1_state: StructuralState
    r2_state: RelativePalaceFrameState
    r3_state: BorrowProjectionState
    r4_state: NamedStructuralSemanticState
    r5_state: ResolvedSanfangSizhengViewState
    view_model: ChartViewModel
    bundle_hash: str
    schema: str = APPLICATION_CHART_BUNDLE_SCHEMA
