from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PolicySelection:
    bazi_day_boundary_policy: str
    bazi_late_zi_hour_stem_policy: str
    bazi_year_boundary_policy: str
    ziwei_calendar_date_policy: str
    ziwei_day_boundary_policy: str
    ziwei_life_body_leap_month_policy: str
    civil_ambiguous_time_policy: str


class PolicyRegistry:
    """Single, versioned registry for disputed or operational conventions."""

    def __init__(self, payload: dict[str, Any]) -> None:
        if payload.get("schema") != "TIME-CALENDAR-POLICY-REGISTRY-V1":
            raise ValueError("wrong time/calendar policy registry schema")
        if not isinstance(payload.get("registry_version"), str):
            raise ValueError("policy registry needs registry_version")
        if not isinstance(payload.get("policies"), dict):
            raise ValueError("policy registry needs policies")
        self.payload = payload

    @classmethod
    def from_file(cls, path: Path) -> "PolicyRegistry":
        with path.open("r", encoding="utf-8") as handle:
            return cls(json.load(handle))

    @property
    def version(self) -> str:
        return self.payload["registry_version"]

    def policy(self, policy_id: str) -> dict[str, Any]:
        try:
            return self.payload["policies"][policy_id]
        except KeyError as exc:
            raise ValueError(f"unknown policy id: {policy_id}") from exc

    def validate_value(self, policy_id: str, value: str) -> str:
        policy = self.policy(policy_id)
        if value not in policy["values"]:
            raise ValueError(f"invalid {policy_id}: {value}")
        return value

    def default_selection(self) -> PolicySelection:
        values = {
            policy_id: item["default"]
            for policy_id, item in self.payload["policies"].items()
        }
        return PolicySelection(
            bazi_day_boundary_policy=values["bazi.day_boundary_policy"],
            bazi_late_zi_hour_stem_policy=values["bazi.late_zi_hour_stem_policy"],
            bazi_year_boundary_policy=values["bazi.year_boundary_policy"],
            ziwei_calendar_date_policy=values["ziwei.calendar_date_policy"],
            ziwei_day_boundary_policy=values["ziwei.day_boundary_policy"],
            ziwei_life_body_leap_month_policy=values["ziwei.life_body_leap_month_policy"],
            civil_ambiguous_time_policy=values["civil.ambiguous_time_policy"],
        )

    def validate_selection(self, selection: PolicySelection) -> PolicySelection:
        mapping = {
            "bazi.day_boundary_policy": selection.bazi_day_boundary_policy,
            "bazi.late_zi_hour_stem_policy": selection.bazi_late_zi_hour_stem_policy,
            "bazi.year_boundary_policy": selection.bazi_year_boundary_policy,
            "ziwei.calendar_date_policy": selection.ziwei_calendar_date_policy,
            "ziwei.day_boundary_policy": selection.ziwei_day_boundary_policy,
            "ziwei.life_body_leap_month_policy": selection.ziwei_life_body_leap_month_policy,
            "civil.ambiguous_time_policy": selection.civil_ambiguous_time_policy,
        }
        for policy_id, value in mapping.items():
            self.validate_value(policy_id, value)
        if (
            selection.bazi_late_zi_hour_stem_policy == "ZI_START_ROLLOVER"
            and selection.bazi_day_boundary_policy != "ZI_START_23"
        ):
            raise ValueError("ZI_START_ROLLOVER requires bazi.day_boundary_policy=ZI_START_23")
        if (
            selection.ziwei_day_boundary_policy == "ZI_START_23"
            and selection.ziwei_calendar_date_policy != "LOCAL_SOLAR_DATE_INDEXED"
        ):
            raise ValueError("Ziwei ZI_START_23 currently requires LOCAL_SOLAR_DATE_INDEXED")
        return selection
