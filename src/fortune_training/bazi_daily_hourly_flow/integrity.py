from __future__ import annotations

from datetime import datetime, time, timedelta, timezone
from typing import Any

from fortune_training.bazi_chart import ResolvedBaziCalculationProfile
from fortune_training.bazi_chart.registries import sexagenary_index
from fortune_training.bazi_flow import BaziFlowCandidate
from fortune_training.bazi_target_temporal import (
    ResolvedTargetTemporalCoordinateProfile,
    TargetTemporalCoordinateResolution,
)
from fortune_training.calendar_foundation import BaziTimeResolver
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .models import (
    BaziDailyHourlyFlowContext,
    DailyHourlyHashBundle,
    DailyHourlyIntegrityDiagnostic,
    DailyHourlyIntegrityReport,
)
from .profile import (
    DAILY_HOURLY_ALGORITHM_VERSION,
    DAILY_RULE_SET_VERSION,
    HOURLY_RULE_SET_VERSION,
    INTERVAL_SEMANTICS,
)


INTEGRITY_ALGORITHM_ID = "BAZI-DAILY-HOURLY-FLOW-INTEGRITY-R1"
INTEGRITY_ALGORITHM_VERSION = "1.0.0"
HASH_ALGORITHM_ID = "BAZI-DAILY-HOURLY-FLOW-HASH-R1"
HASH_ALGORITHM_VERSION = "1.0.0"


def _diag(rows: list[DailyHourlyIntegrityDiagnostic], code: str, path: str, detail: str) -> None:
    rows.append(DailyHourlyIntegrityDiagnostic(code=code, path=path, detail=detail))


def _utc_fact(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Daily/Hourly target UTC must be timezone-aware")
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds")


def _las_fact(value: datetime) -> str:
    if value.tzinfo is not None and value.utcoffset() is not None:
        raise ValueError("Daily/Hourly LAS must be a naive local solar datetime")
    return value.isoformat(timespec="microseconds")


def _expected_daily_interval(effective_day_date, day_boundary_policy: str) -> tuple[datetime, datetime]:
    if day_boundary_policy == "MIDNIGHT":
        start = datetime.combine(effective_day_date, time.min)
    elif day_boundary_policy == "ZI_START_23":
        start = datetime.combine(effective_day_date - timedelta(days=1), time(hour=23))
    else:
        raise ValueError(f"unsupported day boundary policy: {day_boundary_policy}")
    return start, start + timedelta(days=1)


def _expected_hourly_interval(las: datetime) -> tuple[datetime, datetime]:
    clock_date = las.date()
    if las.hour == 23:
        start = datetime.combine(clock_date, time(hour=23))
    elif las.hour == 0:
        start = datetime.combine(clock_date - timedelta(days=1), time(hour=23))
    else:
        start_hour = las.hour if las.hour % 2 == 1 else las.hour - 1
        start = datetime.combine(clock_date, time(hour=start_hour))
    return start, start + timedelta(hours=2)


def _daily_frame_id_payload(context: BaziDailyHourlyFlowContext, resolved) -> dict[str, object]:
    return {
        "ganzhi": resolved.day_pillar,
        "effective_day_date": resolved.effective_day_date.isoformat(),
        "start_las": context.daily_frame.start_las.isoformat(timespec="microseconds"),
        "end_las": context.daily_frame.end_las.isoformat(timespec="microseconds"),
        "day_boundary_policy": context.day_boundary_policy,
        "source_flow_fact_hash": context.source_flow_fact_hash,
        "source_target_coordinate_fact_hash": context.source_target_coordinate_fact_hash,
        "source_target_coordinate_candidate_id": context.source_target_coordinate_candidate_id,
        "natal_profile_id": context.natal_profile_id,
        "natal_profile_version": context.natal_profile_version,
    }


def _hourly_frame_id_payload(context: BaziDailyHourlyFlowContext, resolved) -> dict[str, object]:
    return {
        "ganzhi": resolved.hour_pillar,
        "start_las": context.hourly_frame.start_las.isoformat(timespec="microseconds"),
        "end_las": context.hourly_frame.end_las.isoformat(timespec="microseconds"),
        "hour_stem_source_date": resolved.hour_stem_source_date.isoformat(),
        "late_zi_hour_stem_policy": context.late_zi_hour_stem_policy,
        "daily_frame_id": context.daily_frame.frame_id,
        "source_flow_fact_hash": context.source_flow_fact_hash,
        "source_target_coordinate_fact_hash": context.source_target_coordinate_fact_hash,
        "source_target_coordinate_candidate_id": context.source_target_coordinate_candidate_id,
        "natal_profile_id": context.natal_profile_id,
        "natal_profile_version": context.natal_profile_version,
    }


def daily_hourly_fact_projection(context: BaziDailyHourlyFlowContext) -> dict[str, Any]:
    daily = context.daily_frame
    hourly = context.hourly_frame
    return {
        "upstream_natal_fact_hash": context.upstream_natal_fact_hash,
        "upstream_temporal_fact_hash": context.upstream_temporal_fact_hash,
        "source_flow_fact_hash": context.source_flow_fact_hash,
        "source_target_coordinate_fact_hash": context.source_target_coordinate_fact_hash,
        "source_target_coordinate_candidate_id": context.source_target_coordinate_candidate_id,
        "target_utc": _utc_fact(context.target_utc),
        "target_local_apparent_solar_datetime": _las_fact(context.target_local_apparent_solar_datetime),
        "target_longitude": context.target_longitude,
        "daily_frame": {
            "frame_id": daily.frame_id,
            "ganzhi": daily.ganzhi,
            "sexagenary_index": daily.sexagenary_index,
            "effective_day_date": daily.effective_day_date.isoformat(),
            "start_las": _las_fact(daily.start_las),
            "end_las": _las_fact(daily.end_las),
            "interval_semantics": daily.interval_semantics,
            "day_boundary_policy": daily.day_boundary_policy,
            "source_flow_fact_hash": daily.source_flow_fact_hash,
            "source_target_coordinate_fact_hash": daily.source_target_coordinate_fact_hash,
            "source_target_coordinate_candidate_id": daily.source_target_coordinate_candidate_id,
            "natal_profile_id": daily.natal_profile_id,
            "natal_profile_version": daily.natal_profile_version,
        },
        "hourly_frame": {
            "frame_id": hourly.frame_id,
            "ganzhi": hourly.ganzhi,
            "sexagenary_index": hourly.sexagenary_index,
            "branch": hourly.branch,
            "start_las": _las_fact(hourly.start_las),
            "end_las": _las_fact(hourly.end_las),
            "interval_semantics": hourly.interval_semantics,
            "hour_stem_source_date": hourly.hour_stem_source_date.isoformat(),
            "late_zi_hour_stem_policy": hourly.late_zi_hour_stem_policy,
            "daily_frame_id": hourly.daily_frame_id,
            "source_flow_fact_hash": hourly.source_flow_fact_hash,
            "source_target_coordinate_fact_hash": hourly.source_target_coordinate_fact_hash,
            "source_target_coordinate_candidate_id": hourly.source_target_coordinate_candidate_id,
            "natal_profile_id": hourly.natal_profile_id,
            "natal_profile_version": hourly.natal_profile_version,
        },
        "natal_profile_id": context.natal_profile_id,
        "natal_profile_version": context.natal_profile_version,
        "day_boundary_policy": context.day_boundary_policy,
        "late_zi_hour_stem_policy": context.late_zi_hour_stem_policy,
        "year_boundary_policy": context.year_boundary_policy,
    }


def daily_hourly_hash_bundle(
    context: BaziDailyHourlyFlowContext,
    calculation_profile: ResolvedBaziCalculationProfile,
) -> DailyHourlyHashBundle:
    fact_hash = object_sha256(daily_hourly_fact_projection(context))
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "source_flow_computation_hash": context.source_flow_computation_hash,
            "source_flow_candidate_index": context.source_flow_candidate_index,
            "source_target_coordinate_computation_hash": context.source_target_coordinate_computation_hash,
            "source_target_coordinate_candidate_index": context.source_target_coordinate_candidate_index,
            "resolved_calculation_profile": json_value(calculation_profile),
            "algorithm_versions": dict(sorted(context.algorithm_versions.items())),
            "hash_algorithm": f"{HASH_ALGORITHM_ID}@{HASH_ALGORITHM_VERSION}",
        }
    )
    return DailyHourlyHashBundle(
        fact_hash=fact_hash,
        computation_hash=computation_hash,
        algorithm_id=HASH_ALGORITHM_ID,
        algorithm_version=HASH_ALGORITHM_VERSION,
    )


def validate_daily_hourly_context(
    context: BaziDailyHourlyFlowContext,
    flow: BaziFlowCandidate,
    target_resolution: TargetTemporalCoordinateResolution,
    target_profile: ResolvedTargetTemporalCoordinateProfile,
    calculation_profile: ResolvedBaziCalculationProfile,
    bazi_time: BaziTimeResolver,
) -> DailyHourlyIntegrityReport:
    diagnostics: list[DailyHourlyIntegrityDiagnostic] = []

    if flow.integrity.status != "PASS":
        _diag(diagnostics, "FLOW_INTEGRITY_NOT_PASS", "flow.integrity.status", flow.integrity.status)
    if target_resolution.integrity.status != "PASS":
        _diag(
            diagnostics,
            "TARGET_COORDINATE_INTEGRITY_NOT_PASS",
            "target_coordinate_resolution.integrity.status",
            target_resolution.integrity.status,
        )

    if context.source_flow_fact_hash != flow.hashes.fact_hash:
        _diag(diagnostics, "SOURCE_FLOW_FACT_HASH_MISMATCH", "source_flow_fact_hash", context.source_flow_fact_hash)
    if context.source_flow_computation_hash != flow.hashes.computation_hash:
        _diag(
            diagnostics,
            "SOURCE_FLOW_COMPUTATION_HASH_MISMATCH",
            "source_flow_computation_hash",
            context.source_flow_computation_hash,
        )
    if context.upstream_natal_fact_hash != flow.context.upstream_natal_fact_hash:
        _diag(
            diagnostics,
            "UPSTREAM_NATAL_HASH_MISMATCH",
            "upstream_natal_fact_hash",
            context.upstream_natal_fact_hash,
        )
    if context.upstream_temporal_fact_hash != flow.context.upstream_temporal_fact_hash:
        _diag(
            diagnostics,
            "UPSTREAM_TEMPORAL_HASH_MISMATCH",
            "upstream_temporal_fact_hash",
            context.upstream_temporal_fact_hash,
        )
    if context.source_target_coordinate_fact_hash != target_resolution.hashes.fact_hash:
        _diag(
            diagnostics,
            "SOURCE_TARGET_FACT_HASH_MISMATCH",
            "source_target_coordinate_fact_hash",
            context.source_target_coordinate_fact_hash,
        )
    if context.source_target_coordinate_computation_hash != target_resolution.hashes.computation_hash:
        _diag(
            diagnostics,
            "SOURCE_TARGET_COMPUTATION_HASH_MISMATCH",
            "source_target_coordinate_computation_hash",
            context.source_target_coordinate_computation_hash,
        )

    if context.source_flow_candidate_index < 0:
        _diag(
            diagnostics,
            "SOURCE_FLOW_CANDIDATE_INDEX_INVALID",
            "source_flow_candidate_index",
            str(context.source_flow_candidate_index),
        )
    if not 0 <= context.source_target_coordinate_candidate_index < len(target_resolution.candidates):
        _diag(
            diagnostics,
            "SOURCE_TARGET_CANDIDATE_INDEX_INVALID",
            "source_target_coordinate_candidate_index",
            str(context.source_target_coordinate_candidate_index),
        )
        target = None
    else:
        target = target_resolution.candidates[context.source_target_coordinate_candidate_index]
        if context.source_target_coordinate_candidate_id != target.candidate_id:
            _diag(
                diagnostics,
                "SOURCE_TARGET_CANDIDATE_ID_MISMATCH",
                "source_target_coordinate_candidate_id",
                context.source_target_coordinate_candidate_id,
            )

    if (target_resolution.profile_id, target_resolution.profile_version) != (
        target_profile.profile_id,
        target_profile.profile_version,
    ):
        _diag(
            diagnostics,
            "TARGET_PROFILE_LINEAGE_MISMATCH",
            "target_coordinate_resolution.profile_id",
            f"{target_resolution.profile_id}@{target_resolution.profile_version}",
        )

    if (context.natal_profile_id, context.natal_profile_version) != (
        calculation_profile.profile_id,
        calculation_profile.profile_version,
    ):
        _diag(
            diagnostics,
            "CALCULATION_PROFILE_LINEAGE_MISMATCH",
            "natal_profile_id",
            f"{context.natal_profile_id}@{context.natal_profile_version}",
        )
    if (flow.context.natal_profile_id, flow.context.natal_profile_version) != (
        calculation_profile.profile_id,
        calculation_profile.profile_version,
    ):
        _diag(
            diagnostics,
            "FLOW_CALCULATION_PROFILE_LINEAGE_MISMATCH",
            "flow.context.natal_profile_id",
            f"{flow.context.natal_profile_id}@{flow.context.natal_profile_version}",
        )

    policies = calculation_profile.time_calendar_policies
    expected_policies = {
        "day_boundary_policy": policies.bazi_day_boundary_policy,
        "late_zi_hour_stem_policy": policies.bazi_late_zi_hour_stem_policy,
        "year_boundary_policy": policies.bazi_year_boundary_policy,
    }
    for name, expected in expected_policies.items():
        if getattr(context, name) != expected:
            _diag(diagnostics, "CALCULATION_POLICY_MISMATCH", name, f"expected={expected}")

    expected_algorithms = {
        "daily_hourly": DAILY_HOURLY_ALGORITHM_VERSION,
        "daily": DAILY_RULE_SET_VERSION,
        "hourly": HOURLY_RULE_SET_VERSION,
        "bazi_time": "PHASE-01-R1",
    }
    for name, expected in expected_algorithms.items():
        if context.algorithm_versions.get(name) != expected:
            _diag(
                diagnostics,
                "DAILY_HOURLY_ALGORITHM_VERSION_MISMATCH",
                f"algorithm_versions.{name}",
                str(context.algorithm_versions.get(name)),
            )

    try:
        target_utc = context.target_utc.astimezone(timezone.utc)
    except (AttributeError, ValueError):
        target_utc = None
        _diag(diagnostics, "TARGET_UTC_NOT_AWARE", "target_utc", str(context.target_utc))
    else:
        if context.target_utc.tzinfo is None or context.target_utc.utcoffset() is None:
            _diag(diagnostics, "TARGET_UTC_NOT_AWARE", "target_utc", str(context.target_utc))
            target_utc = None

    if context.target_local_apparent_solar_datetime.tzinfo is not None:
        _diag(
            diagnostics,
            "TARGET_LAS_NOT_NAIVE",
            "target_local_apparent_solar_datetime",
            context.target_local_apparent_solar_datetime.isoformat(),
        )

    if target is not None and target_utc is not None:
        if target_utc != target.target_utc.astimezone(timezone.utc):
            _diag(diagnostics, "TARGET_UTC_REPLAY_MISMATCH", "target_utc", target.target_utc.isoformat())
        if target_utc != flow.context.target_utc.astimezone(timezone.utc):
            _diag(
                diagnostics,
                "FLOW_TARGET_UTC_MISMATCH",
                "target_utc",
                flow.context.target_utc.isoformat(),
            )
        if context.target_local_apparent_solar_datetime != target.local_apparent_solar_datetime:
            _diag(
                diagnostics,
                "TARGET_LAS_REPLAY_MISMATCH",
                "target_local_apparent_solar_datetime",
                target.local_apparent_solar_datetime.isoformat(),
            )
        if context.target_longitude != target_resolution.target_input.longitude:
            _diag(
                diagnostics,
                "TARGET_LONGITUDE_LINEAGE_MISMATCH",
                "target_longitude",
                str(target_resolution.target_input.longitude),
            )

        resolved = bazi_time.resolve(
            target.target_utc,
            target.local_apparent_solar_datetime,
            year_boundary_policy=policies.bazi_year_boundary_policy,
            day_boundary_policy=policies.bazi_day_boundary_policy,
            late_zi_hour_stem_policy=policies.bazi_late_zi_hour_stem_policy,
        )

        if resolved.year_pillar != flow.context.annual_frame.ganzhi:
            _diag(
                diagnostics,
                "AUTHORITATIVE_ANNUAL_FRAME_MISMATCH",
                "flow.context.annual_frame.ganzhi",
                resolved.year_pillar,
            )
        if resolved.month_pillar != flow.context.monthly_frame.ganzhi:
            _diag(
                diagnostics,
                "AUTHORITATIVE_MONTHLY_FRAME_MISMATCH",
                "flow.context.monthly_frame.ganzhi",
                resolved.month_pillar,
            )

        daily = context.daily_frame
        expected_daily_start, expected_daily_end = _expected_daily_interval(
            resolved.effective_day_date,
            policies.bazi_day_boundary_policy,
        )
        expected_daily_id = "DAILY:" + object_sha256(_daily_frame_id_payload(context, resolved))
        if daily.frame_id != expected_daily_id:
            _diag(diagnostics, "DAILY_FRAME_ID_MISMATCH", "daily_frame.frame_id", expected_daily_id)
        if daily.ganzhi != resolved.day_pillar or daily.sexagenary_index != sexagenary_index(resolved.day_pillar):
            _diag(diagnostics, "DAILY_GANZHI_REPLAY_MISMATCH", "daily_frame.ganzhi", resolved.day_pillar)
        if daily.effective_day_date != resolved.effective_day_date:
            _diag(
                diagnostics,
                "DAILY_EFFECTIVE_DATE_REPLAY_MISMATCH",
                "daily_frame.effective_day_date",
                resolved.effective_day_date.isoformat(),
            )
        if daily.start_las != expected_daily_start or daily.end_las != expected_daily_end:
            _diag(
                diagnostics,
                "DAILY_INTERVAL_REPLAY_MISMATCH",
                "daily_frame",
                f"{expected_daily_start.isoformat()}/{expected_daily_end.isoformat()}",
            )
        if not daily.start_las <= target.local_apparent_solar_datetime < daily.end_las:
            _diag(
                diagnostics,
                "TARGET_OUTSIDE_DAILY_FRAME",
                "daily_frame",
                target.local_apparent_solar_datetime.isoformat(),
            )
        if daily.interval_semantics != INTERVAL_SEMANTICS:
            _diag(
                diagnostics,
                "DAILY_INTERVAL_SEMANTICS_MISMATCH",
                "daily_frame.interval_semantics",
                daily.interval_semantics,
            )
        if daily.day_boundary_policy != policies.bazi_day_boundary_policy:
            _diag(
                diagnostics,
                "DAILY_POLICY_MISMATCH",
                "daily_frame.day_boundary_policy",
                daily.day_boundary_policy,
            )

        hourly = context.hourly_frame
        expected_hourly_start, expected_hourly_end = _expected_hourly_interval(target.local_apparent_solar_datetime)
        expected_hourly_id = "HOURLY:" + object_sha256(_hourly_frame_id_payload(context, resolved))
        if hourly.frame_id != expected_hourly_id:
            _diag(diagnostics, "HOURLY_FRAME_ID_MISMATCH", "hourly_frame.frame_id", expected_hourly_id)
        if hourly.ganzhi != resolved.hour_pillar or hourly.sexagenary_index != sexagenary_index(resolved.hour_pillar):
            _diag(diagnostics, "HOURLY_GANZHI_REPLAY_MISMATCH", "hourly_frame.ganzhi", resolved.hour_pillar)
        if hourly.branch != resolved.hour_pillar[1]:
            _diag(diagnostics, "HOURLY_BRANCH_REPLAY_MISMATCH", "hourly_frame.branch", resolved.hour_pillar[1])
        if hourly.hour_stem_source_date != resolved.hour_stem_source_date:
            _diag(
                diagnostics,
                "HOURLY_STEM_SOURCE_DATE_REPLAY_MISMATCH",
                "hourly_frame.hour_stem_source_date",
                resolved.hour_stem_source_date.isoformat(),
            )
        if hourly.start_las != expected_hourly_start or hourly.end_las != expected_hourly_end:
            _diag(
                diagnostics,
                "HOURLY_INTERVAL_REPLAY_MISMATCH",
                "hourly_frame",
                f"{expected_hourly_start.isoformat()}/{expected_hourly_end.isoformat()}",
            )
        if not hourly.start_las <= target.local_apparent_solar_datetime < hourly.end_las:
            _diag(
                diagnostics,
                "TARGET_OUTSIDE_HOURLY_FRAME",
                "hourly_frame",
                target.local_apparent_solar_datetime.isoformat(),
            )
        if hourly.interval_semantics != INTERVAL_SEMANTICS:
            _diag(
                diagnostics,
                "HOURLY_INTERVAL_SEMANTICS_MISMATCH",
                "hourly_frame.interval_semantics",
                hourly.interval_semantics,
            )
        if hourly.late_zi_hour_stem_policy != policies.bazi_late_zi_hour_stem_policy:
            _diag(
                diagnostics,
                "HOURLY_POLICY_MISMATCH",
                "hourly_frame.late_zi_hour_stem_policy",
                hourly.late_zi_hour_stem_policy,
            )
        if hourly.daily_frame_id != daily.frame_id:
            _diag(
                diagnostics,
                "HOURLY_DAILY_BINDING_MISMATCH",
                "hourly_frame.daily_frame_id",
                hourly.daily_frame_id,
            )

        for frame_name, frame in (("daily_frame", daily), ("hourly_frame", hourly)):
            if frame.source_flow_fact_hash != context.source_flow_fact_hash:
                _diag(
                    diagnostics,
                    "FRAME_FLOW_HASH_BINDING_MISMATCH",
                    f"{frame_name}.source_flow_fact_hash",
                    frame.source_flow_fact_hash,
                )
            if frame.source_target_coordinate_fact_hash != context.source_target_coordinate_fact_hash:
                _diag(
                    diagnostics,
                    "FRAME_TARGET_HASH_BINDING_MISMATCH",
                    f"{frame_name}.source_target_coordinate_fact_hash",
                    frame.source_target_coordinate_fact_hash,
                )
            if frame.source_target_coordinate_candidate_id != context.source_target_coordinate_candidate_id:
                _diag(
                    diagnostics,
                    "FRAME_TARGET_CANDIDATE_BINDING_MISMATCH",
                    f"{frame_name}.source_target_coordinate_candidate_id",
                    frame.source_target_coordinate_candidate_id,
                )
            if (frame.natal_profile_id, frame.natal_profile_version) != (
                context.natal_profile_id,
                context.natal_profile_version,
            ):
                _diag(
                    diagnostics,
                    "FRAME_PROFILE_BINDING_MISMATCH",
                    f"{frame_name}.natal_profile_id",
                    f"{frame.natal_profile_id}@{frame.natal_profile_version}",
                )

    return DailyHourlyIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=INTEGRITY_ALGORITHM_ID,
        algorithm_version=INTEGRITY_ALGORITHM_VERSION,
    )
