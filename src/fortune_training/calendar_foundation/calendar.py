from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from functools import lru_cache
from importlib.metadata import version

import astronomy

from .astronomy import SolarTermEngine
from .models import LunarDate


@dataclass(frozen=True)
class _LunarMonth:
    start_instant_utc: datetime
    start_date: date
    next_start_date: date
    next_start_instant_utc: datetime
    number: int
    is_leap: bool
    lunar_year: int
    contains_principal_term: bool


class ChineseCalendarEngine:
    """Astronomically derive the modern Chinese calendar for 1901..2100.

    R1 applies the modern national-calendar day boundary in Beijing Standard
    Time: fixed UTC+08:00 (the standard time of 120 degrees east longitude).
    This is deliberately not the historical Asia/Shanghai civil-time zone,
    because historical DST must not move an official Chinese-calendar day
    boundary. Month starts are civil dates containing geocentric new moons;
    month 11 contains winter solstice; in a 13-month sui the first subsequent
    month without a principal term is leap. Historical calendar regimes are
    intentionally outside this adapter.
    """

    algorithm_id = "MODERN-CHINESE-CALENDAR-ASTRONOMICAL-V1"
    calendar_zone = "UTC+08:00"
    calendar_time_standard = "BEIJING_STANDARD_TIME"
    supported_years = (1901, 2100)

    def __init__(self, solar_terms: SolarTermEngine | None = None) -> None:
        self.solar_terms = solar_terms or SolarTermEngine()
        self.zone = timezone(timedelta(hours=8), name="Beijing Standard Time")

    @staticmethod
    def _atime(instant: datetime) -> astronomy.Time:
        utc = instant.astimezone(timezone.utc)
        seconds = utc.second + utc.microsecond / 1_000_000
        return astronomy.Time.Make(utc.year, utc.month, utc.day, utc.hour, utc.minute, seconds)

    @staticmethod
    def _utc(time: astronomy.Time) -> datetime:
        return time.Utc().replace(tzinfo=timezone.utc)

    def _new_moons(self, start_utc: datetime, end_utc: datetime) -> tuple[datetime, ...]:
        cursor = start_utc - timedelta(days=35)
        rows: list[datetime] = []
        while True:
            found = astronomy.SearchMoonPhase(0.0, self._atime(cursor), 40.0)
            if found is None:
                raise RuntimeError("new-moon search failed")
            instant = self._utc(found)
            if instant > end_utc + timedelta(days=35):
                break
            if not rows or abs((instant - rows[-1]).total_seconds()) > 1.0:
                rows.append(instant)
            cursor = instant + timedelta(seconds=1)
        return tuple(rows)

    def _local_date(self, instant: datetime) -> date:
        return instant.astimezone(self.zone).date()

    @lru_cache(maxsize=64)
    def _cycle(self, winter_solstice_year: int) -> tuple[_LunarMonth, ...]:
        first_ws = self.solar_terms.term(winter_solstice_year, 270).utc_instant
        next_ws = self.solar_terms.term(winter_solstice_year + 1, 270).utc_instant
        moons = self._new_moons(first_ws - timedelta(days=40), next_ws + timedelta(days=40))
        first_ws_date = self._local_date(first_ws)
        next_ws_date = self._local_date(next_ws)
        first_index = max(
            index for index, instant in enumerate(moons) if self._local_date(instant) <= first_ws_date
        )
        next_index = max(
            index for index, instant in enumerate(moons) if self._local_date(instant) <= next_ws_date
        )
        count = next_index - first_index
        if count not in (12, 13):
            raise RuntimeError(f"unexpected lunar-month count between solstices: {count}")
        starts = moons[first_index : next_index + 1]

        principal_terms = []
        for year in (winter_solstice_year, winter_solstice_year + 1):
            principal_terms.extend(
                term
                for term in self.solar_terms.terms_for_gregorian_year(year)
                if term.kind == "ZHONGQI"
            )
        has_principal: list[bool] = []
        for index in range(count):
            start_date = self._local_date(starts[index])
            end_date = self._local_date(starts[index + 1])
            has_principal.append(
                any(start_date <= self._local_date(term.utc_instant) < end_date for term in principal_terms)
            )

        leap_index = None
        if count == 13:
            leap_index = next((index for index in range(1, count) if not has_principal[index]), None)
            if leap_index is None:
                raise RuntimeError("13-month lunar year has no leap-month candidate")

        numbers = [11]
        for index in range(1, count):
            previous = numbers[-1]
            numbers.append(previous if index == leap_index else (previous % 12) + 1)
        month_one_index = numbers.index(1)
        month_one_year = self._local_date(starts[month_one_index]).year

        rows: list[_LunarMonth] = []
        for index in range(count):
            rows.append(
                _LunarMonth(
                    start_instant_utc=starts[index],
                    start_date=self._local_date(starts[index]),
                    next_start_date=self._local_date(starts[index + 1]),
                    next_start_instant_utc=starts[index + 1],
                    number=numbers[index],
                    is_leap=index == leap_index,
                    lunar_year=month_one_year if index >= month_one_index else month_one_year - 1,
                    contains_principal_term=has_principal[index],
                )
            )
        return tuple(rows)

    def from_gregorian_date(self, gregorian_date: date) -> LunarDate:
        low, high = self.supported_years
        if not low <= gregorian_date.year <= high:
            raise ValueError(f"R1 modern Chinese-calendar support is limited to {low}..{high}")
        matching: _LunarMonth | None = None
        for solstice_year in (gregorian_date.year - 1, gregorian_date.year):
            for month in self._cycle(solstice_year):
                if month.start_date <= gregorian_date < month.next_start_date:
                    matching = month
                    break
            if matching is not None:
                break
        if matching is None:
            raise RuntimeError(f"failed to map Chinese-calendar date: {gregorian_date}")
        day = (gregorian_date - matching.start_date).days + 1
        length = (matching.next_start_date - matching.start_date).days
        if length not in (29, 30):
            raise RuntimeError(f"invalid lunar month length: {length}")
        return LunarDate(
            year=matching.lunar_year,
            month=matching.number,
            day=day,
            is_leap_month=matching.is_leap,
            month_length_days=length,
            source_gregorian_date=gregorian_date,
            calendar_zone=self.calendar_zone,
            algorithm_id=self.algorithm_id,
            algorithm_version=version("astronomy-engine"),
            month_start_utc=matching.start_instant_utc,
            next_month_start_utc=matching.next_start_instant_utc,
            contains_principal_term=matching.contains_principal_term,
        )
