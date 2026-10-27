from __future__ import annotations

from datetime import datetime, timezone
from functools import lru_cache
from importlib.metadata import version

import astronomy

from .models import SolarTerm


# Longitudes follow the true equinox-of-date convention used by HKO and the
# apparent geocentric longitude search implemented by Astronomy Engine.
_TERM_DATA = {
    0: ("VERNAL_EQUINOX", "春分", "ZHONGQI"),
    15: ("CLEAR_AND_BRIGHT", "清明", "JIE"),
    30: ("GRAIN_RAIN", "谷雨", "ZHONGQI"),
    45: ("START_OF_SUMMER", "立夏", "JIE"),
    60: ("GRAIN_FULL", "小满", "ZHONGQI"),
    75: ("GRAIN_IN_EAR", "芒种", "JIE"),
    90: ("SUMMER_SOLSTICE", "夏至", "ZHONGQI"),
    105: ("MINOR_HEAT", "小暑", "JIE"),
    120: ("MAJOR_HEAT", "大暑", "ZHONGQI"),
    135: ("START_OF_AUTUMN", "立秋", "JIE"),
    150: ("END_OF_HEAT", "处暑", "ZHONGQI"),
    165: ("WHITE_DEW", "白露", "JIE"),
    180: ("AUTUMNAL_EQUINOX", "秋分", "ZHONGQI"),
    195: ("COLD_DEW", "寒露", "JIE"),
    210: ("FROST_DESCENT", "霜降", "ZHONGQI"),
    225: ("START_OF_WINTER", "立冬", "JIE"),
    240: ("MINOR_SNOW", "小雪", "ZHONGQI"),
    255: ("MAJOR_SNOW", "大雪", "JIE"),
    270: ("WINTER_SOLSTICE", "冬至", "ZHONGQI"),
    285: ("MINOR_COLD", "小寒", "JIE"),
    300: ("MAJOR_COLD", "大寒", "ZHONGQI"),
    315: ("START_OF_SPRING", "立春", "JIE"),
    330: ("RAIN_WATER", "雨水", "ZHONGQI"),
    345: ("AWAKENING_OF_INSECTS", "惊蛰", "JIE"),
}


def _astronomy_time(instant: datetime) -> astronomy.Time:
    utc = instant.astimezone(timezone.utc)
    seconds = utc.second + utc.microsecond / 1_000_000
    return astronomy.Time.Make(utc.year, utc.month, utc.day, utc.hour, utc.minute, seconds)


def _utc_datetime(time: astronomy.Time) -> datetime:
    value = time.Utc()
    return value.replace(tzinfo=timezone.utc)


class SolarTermEngine:
    """Find global instants at which apparent solar longitude reaches 15° steps."""

    algorithm_id = "ASTRONOMY-ENGINE-APPARENT-GEOCENTRIC-SOLAR-LONGITUDE-V1"
    advertised_angular_accuracy_arcminutes = 1.0

    @lru_cache(maxsize=64)
    def terms_for_gregorian_year(self, year: int) -> tuple[SolarTerm, ...]:
        if not 1600 <= year <= 2400:
            raise ValueError("R1 solar-term support is limited to Gregorian years 1600..2400")
        start = astronomy.Time.Make(year, 1, 1, 0, 0, 0)
        rows: list[SolarTerm] = []
        engine_version = version("astronomy-engine")
        for longitude, (name, chinese_name, kind) in _TERM_DATA.items():
            found = astronomy.SearchSunLongitude(float(longitude), start, 370.0)
            if found is None:
                raise RuntimeError(f"solar term search failed: {year} longitude={longitude}")
            instant = _utc_datetime(found)
            if instant.year != year:
                raise RuntimeError(f"solar term search escaped target year: {year} longitude={longitude}")
            rows.append(
                SolarTerm(
                    name=name,
                    chinese_name=chinese_name,
                    longitude_degrees=longitude,
                    kind=kind,
                    utc_instant=instant,
                    algorithm_id=self.algorithm_id,
                    algorithm_version=engine_version,
                    advertised_angular_accuracy_arcminutes=self.advertised_angular_accuracy_arcminutes,
                    time_scale_assumption=(
                        "ASTRONOMY_ENGINE_APPROXIMATES_UT1_AS_UTC_WITHIN_0_9_SECONDS"
                    ),
                )
            )
        return tuple(sorted(rows, key=lambda item: item.utc_instant))

    def term(self, year: int, longitude_degrees: int) -> SolarTerm:
        normalized = longitude_degrees % 360
        for term in self.terms_for_gregorian_year(year):
            if term.longitude_degrees == normalized:
                return term
        raise ValueError(f"not a 24-term longitude: {longitude_degrees}")

    def adjacent_terms(self, utc_instant: datetime, *, jie_only: bool = False) -> tuple[SolarTerm, SolarTerm]:
        if utc_instant.tzinfo is None:
            raise ValueError("utc_instant must be timezone-aware")
        utc = utc_instant.astimezone(timezone.utc)
        pool: list[SolarTerm] = []
        for year in (utc.year - 1, utc.year, utc.year + 1):
            pool.extend(self.terms_for_gregorian_year(year))
        if jie_only:
            pool = [term for term in pool if term.kind == "JIE"]
        pool.sort(key=lambda item: item.utc_instant)
        previous = max(
            (term for term in pool if term.utc_instant <= utc),
            key=lambda item: item.utc_instant,
        )
        following = min(
            (term for term in pool if term.utc_instant > utc),
            key=lambda item: item.utc_instant,
        )
        return previous, following

    def principal_terms_between(self, start_utc: datetime, end_utc: datetime) -> tuple[SolarTerm, ...]:
        if start_utc >= end_utc:
            return ()
        rows: list[SolarTerm] = []
        for year in range(start_utc.year - 1, end_utc.year + 2):
            rows.extend(
                term
                for term in self.terms_for_gregorian_year(year)
                if term.kind == "ZHONGQI" and start_utc <= term.utc_instant < end_utc
            )
        return tuple(sorted(rows, key=lambda item: item.utc_instant))
