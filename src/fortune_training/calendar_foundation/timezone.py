from __future__ import annotations

from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .models import (
    BirthInput,
    CivilCandidate,
    CivilResolution,
    CivilTimeStatus,
    HistoricalTimezoneConfidence,
    InputTimeType,
)


AMBIGUOUS_TIME_POLICIES = {"REJECT", "EARLIER_OFFSET", "LATER_OFFSET"}


class CivilTimeResolver:
    """Resolve a local civil wall time through the IANA timezone database."""

    algorithm_id = "PYTHON-ZONEINFO-IANA-V1"

    @staticmethod
    def _tzdb_version() -> str:
        try:
            return version("tzdata")
        except PackageNotFoundError:
            return "SYSTEM-TZDB-UNVERSIONED"

    @staticmethod
    def _confidence(local_datetime: datetime) -> HistoricalTimezoneConfidence:
        # IANA defines post-1970 timestamps as the design scope of location zones.
        if local_datetime.year >= 1970:
            return HistoricalTimezoneConfidence.TZDB_POST_1970
        return HistoricalTimezoneConfidence.TZDB_PRE_1970_REDUCED

    @staticmethod
    def _candidate(local: datetime, zone: ZoneInfo, fold: int) -> CivilCandidate | None:
        aware = local.replace(tzinfo=zone, fold=fold)
        utc = aware.astimezone(timezone.utc)
        round_trip = utc.astimezone(zone).replace(tzinfo=None)
        if round_trip != local:
            return None
        offset = aware.utcoffset()
        dst = aware.dst()
        if offset is None or dst is None:
            return None
        return CivilCandidate(
            fold=fold,
            utc_instant=utc,
            utc_offset_seconds=int(offset.total_seconds()),
            daylight_saving_seconds=int(dst.total_seconds()),
            timezone_abbreviation=aware.tzname() or "",
        )

    def resolve(
        self,
        birth: BirthInput,
        ambiguous_time_policy: str = "REJECT",
    ) -> CivilResolution:
        if ambiguous_time_policy not in AMBIGUOUS_TIME_POLICIES:
            raise ValueError(f"unknown ambiguous_time_policy: {ambiguous_time_policy}")
        if birth.input_time_type is not InputTimeType.CIVIL:
            return CivilResolution(
                status=CivilTimeStatus.NOT_APPLICABLE,
                candidates=(),
                selected_candidate=None,
                timezone_id=birth.timezone_id,
                tzdb_version=self._tzdb_version(),
                historical_confidence=HistoricalTimezoneConfidence.NOT_RESOLVED,
                warnings=("UTC cannot be derived unless input_time_type is CIVIL",),
            )
        try:
            zone = ZoneInfo(birth.timezone_id)
        except ZoneInfoNotFoundError as exc:
            raise ValueError(f"unknown IANA timezone id: {birth.timezone_id}") from exc

        candidates_by_utc: dict[datetime, CivilCandidate] = {}
        for fold in (0, 1):
            candidate = self._candidate(birth.reported_local_datetime, zone, fold)
            if candidate is not None:
                candidates_by_utc.setdefault(candidate.utc_instant, candidate)
        candidates = tuple(sorted(candidates_by_utc.values(), key=lambda item: item.utc_instant))
        confidence = self._confidence(birth.reported_local_datetime)
        warnings: list[str] = []
        if confidence is HistoricalTimezoneConfidence.TZDB_PRE_1970_REDUCED:
            warnings.append("IANA tzdb does not guarantee complete pre-1970 historical coverage")

        if not candidates:
            return CivilResolution(
                status=CivilTimeStatus.NONEXISTENT,
                candidates=(),
                selected_candidate=None,
                timezone_id=birth.timezone_id,
                tzdb_version=self._tzdb_version(),
                historical_confidence=confidence,
                warnings=tuple(warnings + ["reported wall time falls in a timezone gap"]),
            )
        if len(candidates) == 1:
            return CivilResolution(
                status=CivilTimeStatus.UNIQUE,
                candidates=candidates,
                selected_candidate=candidates[0],
                timezone_id=birth.timezone_id,
                tzdb_version=self._tzdb_version(),
                historical_confidence=confidence,
                warnings=tuple(warnings),
            )

        selected = None
        if ambiguous_time_policy == "EARLIER_OFFSET":
            selected = candidates[0]
        elif ambiguous_time_policy == "LATER_OFFSET":
            selected = candidates[-1]
        return CivilResolution(
            status=CivilTimeStatus.AMBIGUOUS,
            candidates=candidates,
            selected_candidate=selected,
            timezone_id=birth.timezone_id,
            tzdb_version=self._tzdb_version(),
            historical_confidence=confidence,
            warnings=tuple(warnings + (["ambiguous wall time requires an explicit fold policy"] if selected is None else [])),
        )
