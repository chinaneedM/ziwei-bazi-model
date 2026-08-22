from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone

from .astronomy import SolarTerm, SolarTermEngine
from .sexagenary import (
    EARTHLY_BRANCHES,
    HEAVENLY_STEMS,
    five_rats_hour_pillar,
    sexagenary_day_index,
    sexagenary_pillar,
)


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


@dataclass(frozen=True)
class BaziYearMonthResult:
    """Shared Bazi year/month coordinates for any UTC query instant."""

    year_pillar: str
    year_sexagenary_index: int
    pillar_year: int
    annual_start_boundary: SolarTerm
    annual_end_boundary: SolarTerm
    month_pillar: str
    month_sexagenary_index: int
    active_month_boundary: SolarTerm
    next_month_boundary: SolarTerm
    year_boundary_policy: str
    interval_semantics: str = "START_INCLUSIVE_END_EXCLUSIVE"
    algorithm_id: str = "BAZI-YEAR-MONTH-RESOLVER-V1"
    algorithm_version: str = "1.0.0"


def _pillar(index: int) -> str:
    return sexagenary_pillar(index)


class BaziTimeResolver:
    def __init__(self, solar_terms: SolarTermEngine | None = None) -> None:
        self.solar_terms = solar_terms or SolarTermEngine()

    def resolve_year_month(
        self,
        utc_instant: datetime,
        *,
        year_boundary_policy: str,
    ) -> BaziYearMonthResult:
        """Resolve the active annual and monthly half-open solar-term frames.

        This is the single shared path used by natal pillar generation and by
        downstream target-time flow queries.  It deliberately contains the
        only Five-Tiger month-stem calculation in the runtime.
        """

        if year_boundary_policy != "START_OF_SPRING":
            raise ValueError(f"unsupported year boundary policy: {year_boundary_policy}")
        if utc_instant.tzinfo is None or utc_instant.utcoffset() is None:
            raise ValueError("utc_instant must be timezone-aware")
        utc = utc_instant.astimezone(timezone.utc)

        spring_this_year = self.solar_terms.term(utc.year, 315)
        pillar_year = utc.year if utc >= spring_this_year.utc_instant else utc.year - 1
        annual_start = self.solar_terms.term(pillar_year, 315)
        annual_end = self.solar_terms.term(pillar_year + 1, 315)
        year_index = (pillar_year - 4) % 60
        year_pillar = _pillar(year_index)

        active_jie, next_jie = self.solar_terms.adjacent_terms(utc, jie_only=True)
        month_branch_index = _JIE_TO_MONTH_BRANCH[active_jie.longitude_degrees]
        tiger_month_stem_index = ((year_index % 10) * 2 + 2) % 10
        month_offset = (month_branch_index - 2) % 12
        month_stem_index = (tiger_month_stem_index + month_offset) % 10
        month_pillar = HEAVENLY_STEMS[month_stem_index] + EARTHLY_BRANCHES[month_branch_index]
        month_sexagenary_index = next(
            index
            for index in range(60)
            if index % 10 == month_stem_index and index % 12 == month_branch_index
        )

        return BaziYearMonthResult(
            year_pillar=year_pillar,
            year_sexagenary_index=year_index,
            pillar_year=pillar_year,
            annual_start_boundary=annual_start,
            annual_end_boundary=annual_end,
            month_pillar=month_pillar,
            month_sexagenary_index=month_sexagenary_index,
            active_month_boundary=active_jie,
            next_month_boundary=next_jie,
            year_boundary_policy=year_boundary_policy,
        )

    def resolve(
        self,
        utc_instant: datetime,
        local_apparent_solar_datetime: datetime,
        *,
        year_boundary_policy: str,
        day_boundary_policy: str,
        late_zi_hour_stem_policy: str,
    ) -> BaziTimeResult:
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

        year_month = self.resolve_year_month(
            utc,
            year_boundary_policy=year_boundary_policy,
        )
        # Preserve the V1 public field's original reference-year boundary.
        # Active annual start/end boundaries live on BaziYearMonthResult.
        reference_year_boundary = self.solar_terms.term(
            local_apparent_solar_datetime.year,
            315,
        )

        clock_date = local_apparent_solar_datetime.date()
        late_zi = local_apparent_solar_datetime.hour == 23
        effective_day_date = clock_date
        if day_boundary_policy == "ZI_START_23" and late_zi:
            effective_day_date += timedelta(days=1)
        day_index = sexagenary_day_index(effective_day_date)
        day_pillar = _pillar(day_index)

        hour_stem_source_date = effective_day_date
        if late_zi and late_zi_hour_stem_policy == "CLASSICAL_CONTINUOUS":
            hour_stem_source_date = clock_date + timedelta(days=1)
        elif late_zi and late_zi_hour_stem_policy == "CURRENT_DAY_STEM":
            hour_stem_source_date = clock_date
        hour_pillar = five_rats_hour_pillar(
            local_apparent_solar_datetime,
            hour_stem_source_date,
        )

        return BaziTimeResult(
            year_pillar=year_month.year_pillar,
            month_pillar=year_month.month_pillar,
            day_pillar=day_pillar,
            hour_pillar=hour_pillar,
            effective_day_date=effective_day_date,
            hour_stem_source_date=hour_stem_source_date,
            year_boundary=reference_year_boundary,
            active_month_boundary=year_month.active_month_boundary,
            next_month_boundary=year_month.next_month_boundary,
            year_boundary_policy=year_boundary_policy,
            day_boundary_policy=day_boundary_policy,
            late_zi_hour_stem_policy=late_zi_hour_stem_policy,
        )
