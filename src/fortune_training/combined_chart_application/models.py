from __future__ import annotations

from dataclasses import dataclass

from fortune_training.bazi_application import (
    BaziApplicationProfile,
    BaziApplicationResolution,
)
from fortune_training.bazi_chart import ResolvedBaziCalculationProfile
from fortune_training.bazi_temporal import ResolvedBaziTemporalProfile
from fortune_training.calendar_foundation import BirthInput
from fortune_training.ziwei_application import (
    ApplicationChartBundle,
    ZiweiApplicationProfile,
)
from fortune_training.ziwei_chart import PresentationProfile, ResolvedZiweiCalculationProfile

from .profile import CombinedChartApplicationProfile


@dataclass(frozen=True)
class CombinedSubsystemError:
    code: str
    detail: str


@dataclass(frozen=True)
class CombinedChartApplicationRequest:
    birth: BirthInput
    sex: str
    ziwei_calculation_profile: ResolvedZiweiCalculationProfile
    ziwei_application_profile: ZiweiApplicationProfile
    ziwei_presentation_profile: PresentationProfile
    bazi_natal_profile: ResolvedBaziCalculationProfile
    bazi_temporal_profile: ResolvedBaziTemporalProfile
    bazi_application_profile: BaziApplicationProfile
    combined_profile: CombinedChartApplicationProfile
    ziwei_daxian_frame_id: str | None = None
    ziwei_annual_year: int | None = None
    ziwei_minor_limit_age: int | None = None
    ziwei_daxian_count: int = 12
    bazi_dayun_count: int = 12


@dataclass(frozen=True)
class CombinedApplicationIntegrityReport:
    status: str
    diagnostics: tuple[str, ...]
    algorithm_id: str = "ZIWEI-BAZI-COMBINED-APPLICATION-INTEGRITY-V1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class CombinedChartApplicationResolution:
    schema: str
    status: str
    birth: BirthInput
    sex: str
    combined_profile: CombinedChartApplicationProfile
    ziwei_calculation_profile: ResolvedZiweiCalculationProfile
    ziwei_application_profile: ZiweiApplicationProfile
    ziwei_presentation_profile: PresentationProfile
    bazi_natal_profile: ResolvedBaziCalculationProfile
    bazi_temporal_profile: ResolvedBaziTemporalProfile
    bazi_application_profile: BaziApplicationProfile
    ziwei_bundle: ApplicationChartBundle | None
    bazi_bundle: BaziApplicationResolution | None
    ziwei_error: CombinedSubsystemError | None
    bazi_error: CombinedSubsystemError | None
    manifest_hash: str
    integrity: CombinedApplicationIntegrityReport
