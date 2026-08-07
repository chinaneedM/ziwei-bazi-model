from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from .calendar import ChineseCalendarEngine
from .models import LunarDate


@dataclass(frozen=True)
class ZiweiCalendarResult:
    actual_civil_lunar_date: LunarDate
    local_solar_lunar_date: LunarDate
    effective_ziwei_lunar_date: LunarDate
    calendar_date_policy: str
    life_body_leap_month_policy: str
    events: tuple[str, ...]
    algorithm_id: str = "ZIWEI-CALENDAR-RESOLVER-V1"


class ZiweiCalendarResolver:
    """Keep raw calendar mappings separate from Ziwei policy interpretation."""

    def __init__(self, calendar: ChineseCalendarEngine | None = None) -> None:
        self.calendar = calendar or ChineseCalendarEngine()

    def resolve(
        self,
        reported_civil_date: date,
        local_apparent_solar_datetime: datetime,
        *,
        calendar_date_policy: str,
        life_body_leap_month_policy: str,
    ) -> ZiweiCalendarResult:
        civil_lunar = self.calendar.from_gregorian_date(reported_civil_date)
        solar_lunar = self.calendar.from_gregorian_date(local_apparent_solar_datetime.date())
        if calendar_date_policy == "LOCAL_SOLAR_DATE_INDEXED":
            effective = solar_lunar
        elif calendar_date_policy == "ABSOLUTE_CALENDAR":
            effective = civil_lunar
        else:
            raise ValueError(f"unsupported Ziwei calendar date policy: {calendar_date_policy}")
        events = ()
        if reported_civil_date != local_apparent_solar_datetime.date():
            events = ("CALENDAR_DATE_DIVERGENCE",)
        # The leap-month policy is recorded but deliberately not applied here:
        # its R1 scope is life/body placement, which is a later phase.
        return ZiweiCalendarResult(
            actual_civil_lunar_date=civil_lunar,
            local_solar_lunar_date=solar_lunar,
            effective_ziwei_lunar_date=effective,
            calendar_date_policy=calendar_date_policy,
            life_body_leap_month_policy=life_body_leap_month_policy,
            events=events,
        )
