from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from fortune_training.calendar_foundation import BirthInput, TimeCalendarFoundation
from fortune_training.calendar_foundation.models import json_value

from .auxiliary import AuxiliaryContext, QSCoreAuxiliaryGenerator
from .main_stars import MainStarGenerator
from .models import NatalChartState, Sex
from .natal import NatalStructureGenerator, NatalStructureInput
from .profile import ResolvedZiweiCalculationProfile


@dataclass(frozen=True)
class ZiweiChartRequest:
    birth: BirthInput
    sex: Sex
    profile: ResolvedZiweiCalculationProfile


class ZiweiChartFoundation:
    schema = "ZIWEI-CHART-FOUNDATION-RESULT-V1"

    def __init__(self, time_calendar: TimeCalendarFoundation) -> None:
        self.time_calendar = time_calendar
        self.natal = NatalStructureGenerator()
        self.main_stars = MainStarGenerator()
        self.qs_core_aux = QSCoreAuxiliaryGenerator()

    @classmethod
    def from_repository(cls, repository_root: Path) -> "ZiweiChartFoundation":
        return cls(TimeCalendarFoundation.from_repository(repository_root))

    def _generate_chart(self, branch: dict[str, Any], request: ZiweiChartRequest) -> NatalChartState:
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
                life_body_leap_month_policy=request.profile.time_calendar_policies.ziwei_life_body_leap_month_policy,
            )
        )
        placements = list(self.main_stars.generate(structure.lunar_birth_day, structure.bureau.number))
        algorithm_versions = {
            "natal_structure": request.profile.natal_structure_algorithm_version,
            "main_stars": request.profile.main_star_algorithm_version,
        }
        if request.profile.auxiliary_rule_set_id is not None:
            placements.extend(
                self.qs_core_aux.generate(
                    AuxiliaryContext(
                        ziwei_birth_year_stem=structure.ziwei_birth_year_stem,
                        ziwei_birth_year_branch=structure.ziwei_birth_year_branch,
                        raw_lunar_month=structure.raw_lunar_month,
                        birth_hour_branch=structure.birth_hour_branch,
                    )
                )
            )
            algorithm_versions["core_auxiliary"] = request.profile.auxiliary_algorithm_version or ""

        return NatalChartState(
            structure=structure,
            placements=tuple(placements),
            profile_id=request.profile.profile_id,
            profile_version=request.profile.profile_version,
            algorithm_versions=algorithm_versions,
        )

    @staticmethod
    def _chart_key(chart: dict[str, Any]) -> str:
        """Stable equality key for canonical chart candidates in this foundation slice."""
        return json.dumps(chart, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

    def resolve(self, request: ZiweiChartRequest) -> dict[str, Any]:
        profile = request.profile.validate(self.time_calendar.policy_registry)
        time_result = self.time_calendar.resolve(request.birth, profile.time_calendar_policies)
        if not time_result["branches"]:
            return {
                "schema": self.schema,
                "status": "FAILED",
                "diagnostics": ["TIME_CALENDAR_UNRESOLVED"],
                "events": [],
                "calculation_profile": json_value(profile),
                "time_calendar": time_result,
                "charts": [],
                "chart_branch_indices": [],
            }

        unique: dict[str, dict[str, Any]] = {}
        for branch_index, branch in enumerate(time_result["branches"]):
            chart = json_value(self._generate_chart(branch, request))
            key = self._chart_key(chart)
            if key not in unique:
                unique[key] = {"chart": chart, "branch_indices": []}
            unique[key]["branch_indices"].append(branch_index)

        candidates = list(unique.values())
        charts = [row["chart"] for row in candidates]
        chart_branch_indices = [row["branch_indices"] for row in candidates]
        if len(charts) > 1:
            status = "MULTI_CANDIDATE"
            events = ["TIME_UNCERTAINTY_CHANGED_ZIWEI_CHART"]
        elif time_result["status"] == "RESOLVED":
            status = "RESOLVED"
            events = []
        else:
            status = "RESOLVED_SINGLE_CHART_WITH_TIME_UNCERTAINTY"
            events = ["TIME_UNCERTAINTY_DID_NOT_CHANGE_ZIWEI_CHART"]

        return {
            "schema": self.schema,
            "status": status,
            "calculation_profile": json_value(profile),
            "time_calendar": time_result,
            "charts": charts,
            "chart_branch_indices": chart_branch_indices,
            "events": events,
            "diagnostics": [],
        }
