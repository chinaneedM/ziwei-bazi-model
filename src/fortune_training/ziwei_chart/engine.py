from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from fortune_training.calendar_foundation import BirthInput, TimeCalendarFoundation
from fortune_training.calendar_foundation.models import json_value
from fortune_training.calendar_foundation.policies import PolicySelection

from .main_stars import MAIN_STAR_ALGORITHM_VERSION, MainStarGenerator
from .models import NatalChartState, Sex
from .natal import NATAL_STRUCTURE_ALGORITHM_VERSION, NatalStructureGenerator, NatalStructureInput


@dataclass(frozen=True)
class ZiweiChartRequest:
    birth: BirthInput
    sex: Sex
    calculation_profile_id: str
    calculation_profile_version: str


class ZiweiChartFoundation:
    schema = "ZIWEI-CHART-FOUNDATION-RESULT-V1"

    def __init__(self, time_calendar: TimeCalendarFoundation) -> None:
        self.time_calendar = time_calendar
        self.natal = NatalStructureGenerator()
        self.main_stars = MainStarGenerator()

    @classmethod
    def from_repository(cls, repository_root: Path) -> "ZiweiChartFoundation":
        return cls(TimeCalendarFoundation.from_repository(repository_root))

    def _generate_chart(self, branch: dict[str, Any], request: ZiweiChartRequest, selection: PolicySelection) -> NatalChartState:
        lunar = branch["ziwei_calendar"]["effective_ziwei_lunar_date"]
        local_solar = datetime.fromisoformat(branch["solar_time"]["local_apparent_solar_datetime"])
        structure = self.natal.generate(
            NatalStructureInput(
                lunar_year=lunar["year"],
                lunar_month=lunar["month"],
                lunar_day=lunar["day"],
                is_leap_month=lunar["is_leap_month"],
                lunar_month_length_days=lunar["month_length_days"],
                local_apparent_solar_datetime=local_solar,
                life_body_leap_month_policy=selection.ziwei_life_body_leap_month_policy,
            )
        )
        placements = self.main_stars.generate(structure.lunar_birth_day, structure.bureau.number)
        return NatalChartState(
            structure=structure,
            placements=placements,
            profile_id=request.calculation_profile_id,
            profile_version=request.calculation_profile_version,
            algorithm_versions={
                "natal_structure": NATAL_STRUCTURE_ALGORITHM_VERSION,
                "main_stars": MAIN_STAR_ALGORITHM_VERSION,
            },
        )

    def resolve(self, request: ZiweiChartRequest, *, time_policy_selection: PolicySelection) -> dict[str, Any]:
        selection = self.time_calendar.policy_registry.validate_selection(time_policy_selection)
        time_result = self.time_calendar.resolve(request.birth, selection)
        if not time_result["branches"]:
            return {
                "schema": self.schema,
                "status": "FAILED",
                "diagnostics": ["TIME_CALENDAR_UNRESOLVED"],
                "time_calendar": time_result,
                "charts": [],
            }

        charts = [json_value(self._generate_chart(branch, request, selection)) for branch in time_result["branches"]]
        status = "RESOLVED" if time_result["status"] == "RESOLVED" else "MULTI_CANDIDATE"
        return {
            "schema": self.schema,
            "status": status,
            "calculation_profile": {
                "id": request.calculation_profile_id,
                "version": request.calculation_profile_version,
            },
            "time_calendar": time_result,
            "charts": charts,
            "diagnostics": [],
        }
