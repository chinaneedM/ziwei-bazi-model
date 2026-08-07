from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone

from .astronomy import SolarTerm, SolarTermEngine


HEAVENLY_STEMS = "甲乙丙丁戊己庚辛壬癸"
EARTHLY_BRANCHES = "子丑寅卯辰巳午未申酉戌亥"

_JIE_TO_MONTH_BRANCH = {
    315: 2,
    345: 3,
    15: 4,
    45: 5,
    75: 6,
    105: 7,
    135: 8,
    165: 9,
    195: 10,
    225: 11,
    255: 0,
    285: 1,
}


@dataclass(frozen=True)
class BaziTimeResult:
    year_pillar: str
    month_pillar: str
    day_pillar: str
    hour_pillar: str
    effective_day_date: date
    hour_stem_source_date: date
    year_boundary: SolarTerm
    active_month_boundary: SolarTerm
    next_month_boundary: SolarTerm
    year_boundary_policy: str
    day_boundary_policy: str
    late_zi_hour_stem_policy: str
    algorithm_id: str = "BAZI-TIME-RESOLVER-V1"


def _sexagenary_day_index(gregorian_date: date) -> int:
    # Proleptic-Gregorian JDN at noon; JDN 2451551 (2000-01-07) is 甲子.
    julian_day_number = gregorian_date.toordinal() + 1_721_425
    return (julian_day_number + 49) % 60


def _pillar(index: int) -> str:
    return HEAVENLY_STEMS[index % 10] + EARTHLY_BRANCHES[index % 12]


class BaziTimeResolver:
    def __init__(self, solar_terms: SolarTermEngine | None = None) -> None:
        self.solar_terms = solar_terms or SolarTermEngine()

    def resolve(
        self,
        utc_instant: datetime,
        local_apparent_solar_datetime: datetime,
        *,
        year_boundary_policy: str,
        day_boundary_policy: str,
        late_zi_hour_stem_policy: str,
    ) -> BaziTimeResult:
        if year_boundary_policy != "START_OF_SPRING":
            raise ValueError(f"unsupported year boundary policy: {year_boundary_policy}")
        if day_boundary_policy not in {"MIDNIGHT", "ZI_START_23"}:
            raise ValueError(f"unsupported day boundary policy: {day_boundary_policy}")
        if late_zi_hour_stem_policy not in {
            "CLASSICAL_CONTINUOUS",
            "CURRENT_DAY_STEM",
            "ZI_START_ROLLOVER",
        }:
            raise ValueError(f"unsupported late-Zi policy: {late_zi_hour_stem_policy}")
        if late_zi_hour_stem_policy == "ZI_START_ROLLOVER" and day_boundary_policy != "ZI_START_23":
            raise ValueError("ZI_START_ROLLOVER requires ZI_START_23")
        if utc_instant.tzinfo is None:
            raise ValueError("utc_instant must be timezone-aware")
        utc = utc_instant.astimezone(timezone.utc)

        spring = self.solar_terms.term(local_apparent_solar_datetime.year, 315)
        pillar_year = local_apparent_solar_datetime.year if utc >= spring.utc_instant else local_apparent_solar_datetime.year - 1
        year_index = (pillar_year - 4) % 60
        year_pillar = _pillar(year_index)

        active_jie, next_jie = self.solar_terms.adjacent_terms(utc, jie_only=True)
        month_branch_index = _JIE_TO_MONTH_BRANCH[active_jie.longitude_degrees]
        tiger_month_stem_index = ((year_index % 10) * 2 + 2) % 10
        month_offset = (month_branch_index - 2) % 12
        month_stem_index = (tiger_month_stem_index + month_offset) % 10
        month_pillar = HEAVENLY_STEMS[month_stem_index] + EARTHLY_BRANCHES[month_branch_index]

        clock_date = local_apparent_solar_datetime.date()
        late_zi = local_apparent_solar_datetime.hour == 23
        effective_day_date = clock_date
        if day_boundary_policy == "ZI_START_23" and late_zi:
            effective_day_date += timedelta(days=1)
        day_index = _sexagenary_day_index(effective_day_date)
        day_pillar = _pillar(day_index)

        hour_stem_source_date = effective_day_date
        if late_zi and late_zi_hour_stem_policy == "CLASSICAL_CONTINUOUS":
            hour_stem_source_date = clock_date + timedelta(days=1)
        elif late_zi and late_zi_hour_stem_policy == "CURRENT_DAY_STEM":
            hour_stem_source_date = clock_date
        hour_day_stem_index = _sexagenary_day_index(hour_stem_source_date) % 10
        hour_branch_index = ((local_apparent_solar_datetime.hour + 1) // 2) % 12
        zi_hour_stem_index = (hour_day_stem_index % 5) * 2
        hour_stem_index = (zi_hour_stem_index + hour_branch_index) % 10
        hour_pillar = HEAVENLY_STEMS[hour_stem_index] + EARTHLY_BRANCHES[hour_branch_index]

        return BaziTimeResult(
            year_pillar=year_pillar,
            month_pillar=month_pillar,
            day_pillar=day_pillar,
            hour_pillar=hour_pillar,
            effective_day_date=effective_day_date,
            hour_stem_source_date=hour_stem_source_date,
            year_boundary=spring,
            active_month_boundary=active_jie,
            next_month_boundary=next_jie,
            year_boundary_policy=year_boundary_policy,
            day_boundary_policy=day_boundary_policy,
            late_zi_hour_stem_policy=late_zi_hour_stem_policy,
        )
