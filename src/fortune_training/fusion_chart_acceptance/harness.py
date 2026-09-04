from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from fortune_training.bazi_application import (
    BaziApplicationRequest,
    BaziChartService,
    bazi_local_application_v1_profile,
)
from fortune_training.bazi_chart import bazi_foundation_v1_profile
from fortune_training.bazi_target_temporal import (
    TargetTemporalInput,
    bazi_target_temporal_coordinate_r1_profile,
)
from fortune_training.bazi_temporal import BaziSex, bazi_temporal_v1_continuous_profile
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry
from fortune_training.combined_chart_application import (
    CombinedChartApplicationRequest,
    CombinedChartService,
    CombinedTargetFlowRequest,
    CombinedTargetFlowService,
    combined_chart_application_v1_profile,
)
from fortune_training.combined_chart_application.flow_fusion_r2 import (
    CombinedTargetFlowFusionR2Service,
)
from fortune_training.ziwei_application import (
    ApplicationBirthRequest,
    ZiweiChartService,
    ziwei_application_default_presentation_profile,
    ziwei_application_v1_profile,
)
from fortune_training.ziwei_chart import Sex, ziwei_chart_engine_v1_profile


@dataclass(frozen=True)
class AcceptanceLocation:
    place: str
    latitude: float
    longitude: float
    timezone_id: str


DEFAULT_ACCEPTANCE_LOCATIONS = (
    AcceptanceLocation("Beijing", 39.9042, 116.4074, "Asia/Shanghai"),
    AcceptanceLocation("Kashgar", 39.4704, 75.9898, "Asia/Shanghai"),
    AcceptanceLocation("New York", 40.7128, -74.0060, "America/New_York"),
    AcceptanceLocation("Greenwich", 51.4769, 0.0, "Etc/UTC"),
    AcceptanceLocation("Singapore", 1.3521, 103.8198, "Asia/Singapore"),
)


class AcceptanceHarness:
    """Build released services/profiles without changing any canonical rule."""

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = Path(repository_root).resolve()
        self.registry = PolicyRegistry.from_file(
            self.repository_root / "config" / "time-calendar-policies.json"
        )
        self.ziwei_calculation_profile = ziwei_chart_engine_v1_profile(self.registry)
        self.ziwei_application_profile = ziwei_application_v1_profile()
        self.ziwei_presentation_profile = ziwei_application_default_presentation_profile()
        self.bazi_natal_profile = bazi_foundation_v1_profile(self.registry)
        self.bazi_temporal_profile = bazi_temporal_v1_continuous_profile()
        self.bazi_application_profile = bazi_local_application_v1_profile()
        self.combined_profile = combined_chart_application_v1_profile()
        self.target_profile = bazi_target_temporal_coordinate_r1_profile()

        self.ziwei_service = ZiweiChartService.from_repository(self.repository_root)
        self.bazi_service = BaziChartService.from_repository(self.repository_root)
        self.combined_service = CombinedChartService.from_repository(self.repository_root)
        self.target_flow_service = CombinedTargetFlowService.from_repository(
            self.repository_root
        )
        self.fusion_r2_service = CombinedTargetFlowFusionR2Service.from_repository(
            self.repository_root
        )

    @staticmethod
    def birth(
        local: datetime,
        location: AcceptanceLocation,
        *,
        uncertainty_seconds: int = 0,
    ) -> BirthInput:
        return BirthInput(
            reported_local_datetime=local,
            birth_place=location.place,
            latitude=location.latitude,
            longitude=location.longitude,
            timezone_id=location.timezone_id,
            uncertainty_seconds=uncertainty_seconds,
        )

    def combined_request(
        self,
        birth: BirthInput,
        *,
        sex: str = "MALE",
        ziwei_annual_year: int | None = None,
        ziwei_lunar_month: int | None = None,
        ziwei_minor_limit_age: int | None = None,
        ziwei_daxian_count: int = 12,
        bazi_dayun_count: int = 12,
    ) -> CombinedChartApplicationRequest:
        return CombinedChartApplicationRequest(
            birth=birth,
            sex=sex,
            ziwei_calculation_profile=self.ziwei_calculation_profile,
            ziwei_application_profile=self.ziwei_application_profile,
            ziwei_presentation_profile=self.ziwei_presentation_profile,
            bazi_natal_profile=self.bazi_natal_profile,
            bazi_temporal_profile=self.bazi_temporal_profile,
            bazi_application_profile=self.bazi_application_profile,
            combined_profile=self.combined_profile,
            ziwei_annual_year=ziwei_annual_year,
            ziwei_lunar_month=ziwei_lunar_month,
            ziwei_minor_limit_age=ziwei_minor_limit_age,
            ziwei_daxian_count=ziwei_daxian_count,
            bazi_dayun_count=bazi_dayun_count,
        )

    @staticmethod
    def target(
        local: datetime,
        location: AcceptanceLocation,
        *,
        uncertainty_seconds: int = 0,
    ) -> TargetTemporalInput:
        return TargetTemporalInput(
            reported_local_datetime=local,
            target_place=location.place,
            latitude=location.latitude,
            longitude=location.longitude,
            timezone_id=location.timezone_id,
            uncertainty_seconds=uncertainty_seconds,
        )

    def target_flow_request(
        self,
        birth: BirthInput,
        target: TargetTemporalInput,
        *,
        sex: str = "MALE",
        ziwei_annual_year: int | None = None,
    ) -> CombinedTargetFlowRequest:
        return CombinedTargetFlowRequest(
            combined_request=self.combined_request(
                birth,
                sex=sex,
                ziwei_annual_year=ziwei_annual_year,
            ),
            target_input=target,
            target_coordinate_profile=self.target_profile,
        )

    def resolve_ziwei(self, birth: BirthInput, *, sex: str = "MALE"):
        return self.ziwei_service.resolve(
            ApplicationBirthRequest(
                birth=birth,
                sex=Sex(sex),
                calculation_profile=self.ziwei_calculation_profile,
                presentation_profile=self.ziwei_presentation_profile,
                daxian_count=12,
            )
        )

    def resolve_bazi(self, birth: BirthInput, *, sex: str = "MALE"):
        return self.bazi_service.resolve(
            BaziApplicationRequest(
                birth=birth,
                sex=BaziSex(sex),
                natal_profile=self.bazi_natal_profile,
                temporal_profile=self.bazi_temporal_profile,
                application_profile=self.bazi_application_profile,
                dayun_count=12,
            )
        )

    def resolve_combined(self, birth: BirthInput, *, sex: str = "MALE"):
        return self.combined_service.resolve(self.combined_request(birth, sex=sex))

    def resolve_target_flow(
        self,
        birth: BirthInput,
        target: TargetTemporalInput,
        *,
        sex: str = "MALE",
    ):
        return self.target_flow_service.resolve(
            self.target_flow_request(birth, target, sex=sex)
        )

    def resolve_fusion_r2(
        self,
        birth: BirthInput,
        target: TargetTemporalInput,
        *,
        sex: str = "MALE",
    ):
        return self.fusion_r2_service.resolve(
            self.target_flow_request(birth, target, sex=sex)
        )
