from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta

from .calendar import ChineseCalendarEngine
from .models import LunarDate


@dataclass(frozen=True)
class ZiweiCalendarResult:
    actual_civil_lunar_date: LunarDate
    local_solar_lunar_date: LunarDate
    effective_ziwei_lunar_date: LunarDate
    effective_ziwei_gregorian_date: date
    calendar_date_policy: str
    day_boundary_policy: str
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
        life_body_leap_month_policy: str = "FULLBOOK_NEXT_MONTH",
        day_boundary_policy: str = "MIDNIGHT",
    ) -> ZiweiCalendarResult:
        civil_lunar = self.calendar.from_gregorian_date(reported_civil_date)
        local_solar_date = local_apparent_solar_datetime.date()
        solar_lunar = self.calendar.from_gregorian_date(local_solar_date)

        if calendar_date_policy == "LOCAL_SOLAR_DATE_INDEXED":
            effective_gregorian_date = local_solar_date
            if day_boundary_policy == "MIDNIGHT":
                pass
            elif day_boundary_policy == "ZI_START_23":
                if local_apparent_solar_datetime.hour == 23:
                    effective_gregorian_date += timedelta(days=1)
            else:
                raise ValueError(f"unsupported Ziwei day-boundary policy: {day_boundary_policy}")
            effective = self.calendar.from_gregorian_date(effective_gregorian_date)
        elif calendar_date_policy == "ABSOLUTE_CALENDAR":
            if day_boundary_policy != "MIDNIGHT":
                raise ValueError("ABSOLUTE_CALENDAR currently supports only MIDNIGHT Ziwei day boundary")
            effective_gregorian_date = reported_civil_date
            effective = civil_lunar
        else:
            raise ValueError(f"unsupported Ziwei calendar date policy: {calendar_date_policy}")

        events: list[str] = []
        if reported_civil_date != local_solar_date:
            events.append("CALENDAR_DATE_DIVERGENCE")
        if effective_gregorian_date != local_solar_date:
            events.append("ZIWEI_DAY_BOUNDARY_ROLLOVER")

        # The leap-month policy is recorded but deliberately not applied here:
        # its scope is Life/Body placement and raw lunar identity remains untouched.
        return ZiweiCalendarResult(
            actual_civil_lunar_date=civil_lunar,
            local_solar_lunar_date=solar_lunar,
            effective_ziwei_lunar_date=effective,
            effective_ziwei_gregorian_date=effective_gregorian_date,
            calendar_date_policy=calendar_date_policy,
            day_boundary_policy=day_boundary_policy,
            life_body_leap_month_policy=life_body_leap_month_policy,
            events=tuple(events),
        )
