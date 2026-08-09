from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .astronomy import SolarTermEngine
from .bazi import BaziTimeResolver
from .calendar import ChineseCalendarEngine
from .models import AuditTrace, BirthInput, CivilCandidate, CivilTimeStatus, json_value
from .policies import PolicyRegistry, PolicySelection
from .solar import SolarTimeEngine
from .timezone import CivilTimeResolver
from .ziwei import ZiweiCalendarResolver


class TimeCalendarFoundation:
    schema = "TIME-CALENDAR-FOUNDATION-RESULT-V1"

    def __init__(self, policy_registry: PolicyRegistry) -> None:
        self.policy_registry = policy_registry
        self.civil = CivilTimeResolver()
        self.solar = SolarTimeEngine()
        self.solar_terms = SolarTermEngine()
        self.calendar = ChineseCalendarEngine(self.solar_terms)
        self.bazi = BaziTimeResolver(self.solar_terms)
        self.ziwei = ZiweiCalendarResolver(self.calendar)

    @classmethod
    def from_repository(cls, repository_root: Path) -> "TimeCalendarFoundation":
        return cls(PolicyRegistry.from_file(repository_root / "config" / "time-calendar-policies.json"))

    @staticmethod
    def _sample_wall_times(birth: BirthInput) -> tuple[datetime, ...]:
        uncertainty = birth.effective_uncertainty_seconds
        center = birth.reported_local_datetime
        if uncertainty == 0:
            return (center,)
        start = center - timedelta(seconds=uncertainty)
        end = center + timedelta(seconds=uncertainty)
        span_seconds = (end - start).total_seconds()
        step_seconds = 60 if span_seconds <= 86_400 else max(3600, int(span_seconds / 1998))
        rows = {start, center, end}
        cursor = start.replace(second=0, microsecond=0) + timedelta(minutes=1)
        if step_seconds >= 3600:
            cursor = start.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        while cursor < end and len(rows) < 2001:
            rows.add(cursor)
            cursor += timedelta(seconds=step_seconds)
        return tuple(sorted(rows))

    def _resolve_candidate(
        self,
        birth: BirthInput,
        candidate: CivilCandidate,
        selection: PolicySelection,
        civil_resolution: Any,
    ) -> dict[str, Any]:
        trace = AuditTrace()
        trace.add(
            "capture_birth_input",
            "FACT",
            {},
            {
                "reported_civil_datetime": birth.reported_local_datetime,
                "birth_place": birth.birth_place,
                "latitude": birth.latitude,
                "longitude": birth.longitude,
                "timezone_id": birth.timezone_id,
                "precision": birth.precision,
                "input_time_type": birth.input_time_type,
            },
        )
        trace.add(
            "resolve_civil_time",
            "FACT",
            {"reported_civil_datetime": birth.reported_local_datetime, "timezone_id": birth.timezone_id},
            {
                "utc_instant": candidate.utc_instant,
                "utc_offset_seconds": candidate.utc_offset_seconds,
                "dst_seconds": candidate.daylight_saving_seconds,
                "fold": candidate.fold,
            },
            {
                "algorithm": self.civil.algorithm_id,
                "tzdb_version": civil_resolution.tzdb_version,
                "historical_confidence": civil_resolution.historical_confidence,
            },
        )
        solar = self.solar.resolve(
            candidate.utc_instant,
            birth.longitude,
            candidate.utc_offset_seconds,
        )
        trace.add(
            "calculate_local_solar_time",
            "FACT",
            {"utc_instant": candidate.utc_instant, "longitude": birth.longitude},
            {
                "local_mean_solar_datetime": solar.local_mean_solar_datetime,
                "equation_of_time_seconds": solar.equation_of_time_seconds,
                "local_apparent_solar_datetime": solar.local_apparent_solar_datetime,
            },
            {"algorithm": solar.algorithm_id, "version": solar.algorithm_version},
        )
        adjacent_jie = self.solar_terms.adjacent_terms(candidate.utc_instant, jie_only=True)
        trace.add(
            "resolve_solar_term_boundaries",
            "FACT",
            {"birth_utc": candidate.utc_instant},
            {"previous_jie": adjacent_jie[0], "next_jie": adjacent_jie[1]},
            {"comparison_coordinate": "UTC_TO_UTC"},
        )
        ziwei = self.ziwei.resolve(
            birth.reported_local_datetime.date(),
            solar.local_apparent_solar_datetime,
            calendar_date_policy=selection.ziwei_calendar_date_policy,
            day_boundary_policy=selection.ziwei_day_boundary_policy,
            life_body_leap_month_policy=selection.ziwei_life_body_leap_month_policy,
        )
        trace.add(
            "map_chinese_calendar_dates",
            "FACT",
            {
                "reported_civil_date": birth.reported_local_datetime.date(),
                "local_apparent_solar_date": solar.local_apparent_solar_datetime.date(),
            },
            {
                "actual_civil_lunar_date": ziwei.actual_civil_lunar_date,
                "local_solar_lunar_date": ziwei.local_solar_lunar_date,
                "events": ziwei.events,
            },
            {"algorithm": self.calendar.algorithm_id, "calendar_zone": self.calendar.calendar_zone},
        )
        trace.add(
            "select_ziwei_calendar_date",
            "POLICY",
            {
                "calendar_date_policy": selection.ziwei_calendar_date_policy,
                "day_boundary_policy": selection.ziwei_day_boundary_policy,
                "life_body_leap_month_policy": selection.ziwei_life_body_leap_month_policy,
            },
            {
                "effective_ziwei_gregorian_date": ziwei.effective_ziwei_gregorian_date,
                "effective_ziwei_lunar_date": ziwei.effective_ziwei_lunar_date,
            },
            {
                "registry_version": self.policy_registry.version,
                "leap_policy_applied": False,
                "leap_policy_scope": "RECORDED_FOR_LATER_ZIWEI_LIFE_BODY_PLACEMENT",
            },
        )
        bazi = self.bazi.resolve(
            candidate.utc_instant,
            solar.local_apparent_solar_datetime,
            year_boundary_policy=selection.bazi_year_boundary_policy,
            day_boundary_policy=selection.bazi_day_boundary_policy,
            late_zi_hour_stem_policy=selection.bazi_late_zi_hour_stem_policy,
        )
        trace.add(
            "resolve_bazi_time_pillars",
            "POLICY",
            {
                "birth_utc": candidate.utc_instant,
                "local_apparent_solar_datetime": solar.local_apparent_solar_datetime,
                "year_boundary_policy": selection.bazi_year_boundary_policy,
                "day_boundary_policy": selection.bazi_day_boundary_policy,
                "late_zi_hour_stem_policy": selection.bazi_late_zi_hour_stem_policy,
            },
            {"bazi_time_result": bazi},
            {"registry_version": self.policy_registry.version},
        )
        return json_value(
            {
                "sample_reported_local_datetime": birth.reported_local_datetime,
                "civil_time": civil_resolution,
                "selected_civil_candidate": candidate,
                "solar_time": solar,
                "ziwei_calendar": ziwei,
                "bazi_time": bazi,
                "audit_trace": trace,
            }
        )

    @staticmethod
    def _classification_signature(branch: dict[str, Any]) -> tuple[Any, ...]:
        bazi = branch["bazi_time"]
        ziwei = branch["ziwei_calendar"]
        solar = branch["solar_time"]
        return (
            bazi["year_pillar"],
            bazi["month_pillar"],
            bazi["day_pillar"],
            bazi["hour_pillar"],
            solar["local_apparent_solar_datetime"][:10],
            ziwei["effective_ziwei_lunar_date"]["year"],
            ziwei["effective_ziwei_lunar_date"]["month"],
            ziwei["effective_ziwei_lunar_date"]["day"],
            ziwei["effective_ziwei_lunar_date"]["is_leap_month"],
        )

    def resolve(
        self,
        birth: BirthInput,
        selection: PolicySelection | None = None,
    ) -> dict[str, Any]:
        selected = self.policy_registry.validate_selection(selection or self.policy_registry.default_selection())
        branches: list[dict[str, Any]] = []
        unresolved: list[dict[str, Any]] = []
        ambiguous_samples = 0
        for wall_time in self._sample_wall_times(birth):
            sampled_birth = replace(birth, reported_local_datetime=wall_time, uncertainty_seconds=0)
            civil = self.civil.resolve(sampled_birth, selected.civil_ambiguous_time_policy)
            if civil.status is CivilTimeStatus.AMBIGUOUS:
                ambiguous_samples += 1
            if civil.status in {CivilTimeStatus.NONEXISTENT, CivilTimeStatus.NOT_APPLICABLE}:
                unresolved.append(json_value({"sample_reported_local_datetime": wall_time, "civil_time": civil}))
                continue
            candidates = (civil.selected_candidate,) if civil.selected_candidate is not None else civil.candidates
            for candidate in candidates:
                if candidate is not None:
                    branches.append(self._resolve_candidate(sampled_birth, candidate, selected, civil))

        signatures = {self._classification_signature(branch) for branch in branches}
        if not branches:
            status = "UNRESOLVED_CIVIL_TIME"
        elif len(signatures) > 1 or unresolved or ambiguous_samples:
            status = "MULTI_CANDIDATE_OR_BOUNDARY_UNCERTAINTY"
        elif birth.effective_uncertainty_seconds:
            status = "RESOLVED_RANGE_SINGLE_CLASSIFICATION"
        else:
            status = "RESOLVED"
        return {
            "schema": self.schema,
            "status": status,
            "input": json_value(birth),
            "input_interval": {
                "uncertainty_seconds_each_side": birth.effective_uncertainty_seconds,
                "sample_count": len(self._sample_wall_times(birth)),
                "ambiguous_sample_count": ambiguous_samples,
            },
            "policy_registry_version": self.policy_registry.version,
            "selected_policies": json_value(selected),
            "classification_count": len(signatures),
            "branches": branches,
            "unresolved_samples": unresolved,
            "metadata": {
                "foundation_version": "PHASE-01-R2",
                "facts_and_policies_separated": True,
                "canonical_sources_modified": False,
            },
        }
