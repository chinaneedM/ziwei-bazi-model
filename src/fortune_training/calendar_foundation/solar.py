from __future__ import annotations

from datetime import datetime, timedelta, timezone
from importlib.metadata import version

import astronomy

from .models import SolarTimeResult


class SolarTimeEngine:
    """Calculate local mean and apparent solar clock readings as full datetimes."""

    algorithm_id = "ASTRONOMY-ENGINE-GAST-GEOCENTRIC-APPARENT-SUN-EOT-V2"

    @staticmethod
    def _astronomy_time(utc_instant: datetime) -> astronomy.Time:
        utc = utc_instant.astimezone(timezone.utc)
        seconds = utc.second + utc.microsecond / 1_000_000
        return astronomy.Time.Make(utc.year, utc.month, utc.day, utc.hour, utc.minute, seconds)

    @classmethod
    def equation_of_time_seconds(cls, utc_instant: datetime) -> float:
        """Return apparent solar time minus local mean solar time at Greenwich.

        USNO defines apparent solar time as 12h plus the local hour angle of the
        apparent Sun. The equation of time is a longitude-independent clock
        correction, so use the apparent *geocentric* solar right ascension in
        the true-equator-of-date frame. Astronomy Engine's Equator() API is
        topocentric and therefore is intentionally not used here.
        """
        utc = utc_instant.astimezone(timezone.utc)
        time = cls._astronomy_time(utc)
        sun_eqj = astronomy.GeoVector(astronomy.Body.Sun, time, aberration=True)
        sun_eqd = astronomy.RotateVector(astronomy.Rotation_EQJ_EQD(time), sun_eqj)
        sun = astronomy.EquatorFromVector(sun_eqd)
        apparent_hours = (astronomy.SiderealTime(time) - sun.ra + 12.0) % 24.0
        utc_hours = (
            utc.hour
            + utc.minute / 60.0
            + utc.second / 3600.0
            + utc.microsecond / 3_600_000_000.0
        )
        equation_hours = ((apparent_hours - utc_hours + 12.0) % 24.0) - 12.0
        return equation_hours * 3600.0

    def resolve(
        self,
        utc_instant: datetime,
        longitude: float,
        civil_offset_seconds: int,
    ) -> SolarTimeResult:
        if utc_instant.tzinfo is None or utc_instant.utcoffset() is None:
            raise ValueError("utc_instant must be timezone-aware")
        if not -180.0 <= longitude <= 180.0:
            raise ValueError("longitude must be in [-180, 180]")
        utc = utc_instant.astimezone(timezone.utc)
        longitude_seconds = longitude * 240.0  # 360 degrees / 24 hours.
        equation_seconds = self.equation_of_time_seconds(utc)
        lmt = (utc + timedelta(seconds=longitude_seconds)).replace(tzinfo=None)
        apparent = lmt + timedelta(seconds=equation_seconds)
        return SolarTimeResult(
            utc_instant=utc,
            local_mean_solar_datetime=lmt,
            local_apparent_solar_datetime=apparent,
            longitude_correction_seconds_from_civil=longitude_seconds - civil_offset_seconds,
            equation_of_time_seconds=equation_seconds,
            apparent_solar_offset_from_utc_seconds=longitude_seconds + equation_seconds,
            algorithm_id=self.algorithm_id,
            algorithm_version=version("astronomy-engine"),
            time_scale_assumption="ASTRONOMY_ENGINE_APPROXIMATES_UT1_AS_UTC_WITHIN_0_9_SECONDS",
        )
