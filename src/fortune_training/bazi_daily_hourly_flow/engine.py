from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timedelta, timezone

from fortune_training.bazi_chart.registries import sexagenary_index
from fortune_training.bazi_target_temporal import (
    TargetTemporalCoordinateFoundation,
    validate_target_temporal_resolution,
)
from fortune_training.calendar_foundation import BaziTimeResolver
from fortune_training.util import object_sha256

from .models import (
    BaziDailyHourlyFlowContext,
    BaziDailyHourlyFlowRequest,
    BaziDailyHourlyFlowResolution,
    DailyFrame,
    HourlyFrame,
)
from .profile import (
    DAILY_HOURLY_ALGORITHM_VERSION,
    DAILY_RULE_SET_VERSION,
    HOURLY_RULE_SET_VERSION,
    INTERVAL_SEMANTICS,
)


class BaziDailyHourlyFlowGenerationError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


def _stable_frame_id(kind: str, payload: dict[str, object]) -> str:
    return f"{kind}:{object_sha256(payload)}"


def _daily_interval(las: datetime, effective_day_date, day_boundary_policy: str) -> tuple[datetime, datetime]:
    if day_boundary_policy == "MIDNIGHT":
        start = datetime.combine(effective_day_date, time.min)
        return start, start + timedelta(days=1)
    if day_boundary_policy == "ZI_START_23":
        start = datetime.combine(effective_day_date - timedelta(days=1), time(hour=23))
        return start, start + timedelta(days=1)
    raise BaziDailyHourlyFlowGenerationError(
        "UNSUPPORTED_DAY_BOUNDARY_POLICY",
        day_boundary_policy,
    )


def _hourly_interval(las: datetime) -> tuple[datetime, datetime]:
    clock_date = las.date()
    if las.hour == 23:
        start = datetime.combine(clock_date, time(hour=23))
    elif las.hour == 0:
        start = datetime.combine(clock_date - timedelta(days=1), time(hour=23))
    else:
        start_hour = las.hour if las.hour % 2 == 1 else las.hour - 1
        start = datetime.combine(clock_date, time(hour=start_hour))
    return start, start + timedelta(hours=2)


@dataclass(frozen=True)
class BaziDailyHourlyFlowEngine:
    bazi_time: BaziTimeResolver = BaziTimeResolver()

    schema = "BAZI-DAILY-HOURLY-FLOW-RESOLUTION-R1"

    def _context(self, request: BaziDailyHourlyFlowRequest, flow, flow_index: int, target, target_index: int):
        context = flow.context
        profile = request.calculation_profile
        target_resolution = request.target_coordinate_resolution

        if flow.integrity.status != "PASS":
            raise BaziDailyHourlyFlowGenerationError("FLOW_INTEGRITY_NOT_PASS", flow.integrity.status)
        if context.target_utc.astimezone(timezone.utc) != target.target_utc.astimezone(timezone.utc):
            raise BaziDailyHourlyFlowGenerationError(
                "FLOW_TARGET_UTC_MISMATCH",
                f"flow={context.target_utc.isoformat()} target={target.target_utc.isoformat()}",
            )
        if (context.natal_profile_id, context.natal_profile_version) != (
            profile.profile_id,
            profile.profile_version,
        ):
            raise BaziDailyHourlyFlowGenerationError(
                "CALCULATION_PROFILE_LINEAGE_MISMATCH",
                f"flow={context.natal_profile_id}@{context.natal_profile_version} "
                f"request={profile.profile_id}@{profile.profile_version}",
            )
        policies = profile.time_calendar_policies
        if context.year_boundary_policy != policies.bazi_year_boundary_policy:
            raise BaziDailyHourlyFlowGenerationError(
                "YEAR_BOUNDARY_POLICY_LINEAGE_MISMATCH",
                f"flow={context.year_boundary_policy} request={policies.bazi_year_boundary_policy}",
            )

        resolved = self.bazi_time.resolve(
            target.target_utc,
            target.local_apparent_solar_datetime,
            year_boundary_policy=policies.bazi_year_boundary_policy,
            day_boundary_policy=policies.bazi_day_boundary_policy,
            late_zi_hour_stem_policy=policies.bazi_late_zi_hour_stem_policy,
        )
        if resolved.year_pillar != context.annual_frame.ganzhi:
            raise BaziDailyHourlyFlowGenerationError(
                "AUTHORITATIVE_ANNUAL_FRAME_MISMATCH",
                f"resolver={resolved.year_pillar} flow={context.annual_frame.ganzhi}",
            )
        if resolved.month_pillar != context.monthly_frame.ganzhi:
            raise BaziDailyHourlyFlowGenerationError(
                "AUTHORITATIVE_MONTHLY_FRAME_MISMATCH",
                f"resolver={resolved.month_pillar} flow={context.monthly_frame.ganzhi}",
            )

        daily_start, daily_end = _daily_interval(
            target.local_apparent_solar_datetime,
            resolved.effective_day_date,
            policies.bazi_day_boundary_policy,
        )
        daily_payload = {
            "ganzhi": resolved.day_pillar,
            "effective_day_date": resolved.effective_day_date.isoformat(),
            "start_las": daily_start.isoformat(timespec="microseconds"),
            "end_las": daily_end.isoformat(timespec="microseconds"),
            "day_boundary_policy": policies.bazi_day_boundary_policy,
            "source_flow_fact_hash": flow.hashes.fact_hash,
            "source_target_coordinate_fact_hash": target_resolution.hashes.fact_hash,
            "source_target_coordinate_candidate_id": target.candidate_id,
            "natal_profile_id": profile.profile_id,
            "natal_profile_version": profile.profile_version,
        }
        daily = DailyFrame(
            frame_id=_stable_frame_id("DAILY", daily_payload),
            ganzhi=resolved.day_pillar,
            sexagenary_index=sexagenary_index(resolved.day_pillar),
            effective_day_date=resolved.effective_day_date,
            start_las=daily_start,
            end_las=daily_end,
            interval_semantics=INTERVAL_SEMANTICS,
            day_boundary_policy=policies.bazi_day_boundary_policy,
            source_flow_fact_hash=flow.hashes.fact_hash,
            source_target_coordinate_fact_hash=target_resolution.hashes.fact_hash,
            source_target_coordinate_candidate_id=target.candidate_id,
            natal_profile_id=profile.profile_id,
            natal_profile_version=profile.profile_version,
        )

        hourly_start, hourly_end = _hourly_interval(target.local_apparent_solar_datetime)
        hourly_payload = {
            "ganzhi": resolved.hour_pillar,
            "start_las": hourly_start.isoformat(timespec="microseconds"),
            "end_las": hourly_end.isoformat(timespec="microseconds"),
            "hour_stem_source_date": resolved.hour_stem_source_date.isoformat(),
            "late_zi_hour_stem_policy": policies.bazi_late_zi_hour_stem_policy,
            "daily_frame_id": daily.frame_id,
            "source_flow_fact_hash": flow.hashes.fact_hash,
            "source_target_coordinate_fact_hash": target_resolution.hashes.fact_hash,
            "source_target_coordinate_candidate_id": target.candidate_id,
            "natal_profile_id": profile.profile_id,
            "natal_profile_version": profile.profile_version,
        }
        hourly = HourlyFrame(
            frame_id=_stable_frame_id("HOURLY", hourly_payload),
            ganzhi=resolved.hour_pillar,
            sexagenary_index=sexagenary_index(resolved.hour_pillar),
            branch=resolved.hour_pillar[1],
            start_las=hourly_start,
            end_las=hourly_end,
            interval_semantics=INTERVAL_SEMANTICS,
            hour_stem_source_date=resolved.hour_stem_source_date,
            late_zi_hour_stem_policy=policies.bazi_late_zi_hour_stem_policy,
            daily_frame_id=daily.frame_id,
            source_flow_fact_hash=flow.hashes.fact_hash,
            source_target_coordinate_fact_hash=target_resolution.hashes.fact_hash,
            source_target_coordinate_candidate_id=target.candidate_id,
            natal_profile_id=profile.profile_id,
            natal_profile_version=profile.profile_version,
        )

        return BaziDailyHourlyFlowContext(
            upstream_natal_fact_hash=context.upstream_natal_fact_hash,
            upstream_temporal_fact_hash=context.upstream_temporal_fact_hash,
            source_flow_fact_hash=flow.hashes.fact_hash,
            source_flow_computation_hash=flow.hashes.computation_hash,
            source_flow_candidate_index=flow_index,
            source_target_coordinate_fact_hash=target_resolution.hashes.fact_hash,
            source_target_coordinate_computation_hash=target_resolution.hashes.computation_hash,
            source_target_coordinate_candidate_id=target.candidate_id,
            source_target_coordinate_candidate_index=target_index,
            target_utc=target.target_utc.astimezone(timezone.utc),
            target_local_apparent_solar_datetime=target.local_apparent_solar_datetime,
            target_longitude=target_resolution.target_input.longitude,
            daily_frame=daily,
            hourly_frame=hourly,
            natal_profile_id=profile.profile_id,
            natal_profile_version=profile.profile_version,
            day_boundary_policy=policies.bazi_day_boundary_policy,
            late_zi_hour_stem_policy=policies.bazi_late_zi_hour_stem_policy,
            year_boundary_policy=policies.bazi_year_boundary_policy,
            algorithm_versions={
                "daily_hourly": DAILY_HOURLY_ALGORITHM_VERSION,
                "daily": DAILY_RULE_SET_VERSION,
                "hourly": HOURLY_RULE_SET_VERSION,
                "bazi_time": "PHASE-01-R1",
            },
        )

    def resolve(self, request: BaziDailyHourlyFlowRequest) -> BaziDailyHourlyFlowResolution:
        from .integrity import daily_hourly_hash_bundle, validate_daily_hourly_context
        from .models import BaziDailyHourlyFlowCandidate

        target_resolution = request.target_coordinate_resolution
        target_foundation = TargetTemporalCoordinateFoundation()
        target_report = validate_target_temporal_resolution(
            target_resolution,
            request.target_coordinate_profile.validate(),
            target_foundation.civil,
            target_foundation.solar,
        )
        if target_report.status != "PASS" or target_resolution.integrity.status != "PASS":
            return BaziDailyHourlyFlowResolution(
                schema=self.schema,
                status="FAILED",
                candidates=(),
                diagnostics=("TARGET_COORDINATE_INTEGRITY_NOT_PASS",),
            )
        if not request.flow_candidates:
            return BaziDailyHourlyFlowResolution(
                schema=self.schema,
                status="FAILED",
                candidates=(),
                diagnostics=("NO_FLOW_CANDIDATES",),
            )
        if not target_resolution.candidates:
            return BaziDailyHourlyFlowResolution(
                schema=self.schema,
                status="FAILED",
                candidates=(),
                diagnostics=("NO_TARGET_COORDINATE_CANDIDATES",),
            )

        rows: list[BaziDailyHourlyFlowCandidate] = []
        diagnostics: list[str] = []
        for target_index, target in enumerate(target_resolution.candidates):
            matched = False
            for flow_index, flow in enumerate(request.flow_candidates):
                if flow.context.target_utc.astimezone(timezone.utc) != target.target_utc.astimezone(timezone.utc):
                    continue
                matched = True
                try:
                    context = self._context(request, flow, flow_index, target, target_index)
                    report = validate_daily_hourly_context(
                        context,
                        flow,
                        target_resolution,
                        request.target_coordinate_profile,
                        request.calculation_profile,
                        self.bazi_time,
                    )
                    if report.status != "PASS":
                        diagnostics.extend(
                            f"INTEGRITY:{row.code}:{row.path}:{row.detail}" for row in report.diagnostics
                        )
                        continue
                    hashes = daily_hourly_hash_bundle(
                        context,
                        request.calculation_profile,
                    )
                    rows.append(
                        BaziDailyHourlyFlowCandidate(
                            source_flow_candidate_index=flow_index,
                            source_target_coordinate_candidate_index=target_index,
                            context=context,
                            integrity=report,
                            hashes=hashes,
                        )
                    )
                except (BaziDailyHourlyFlowGenerationError, ValueError) as exc:
                    code = getattr(exc, "diagnostic_code", "DAILY_HOURLY_GENERATION_FAILED")
                    diagnostics.append(f"{code}:{exc}")
            if not matched:
                diagnostics.append(
                    f"NO_COMPATIBLE_FLOW_FOR_TARGET:{target_index}:{target.target_utc.isoformat()}"
                )

        if diagnostics:
            return BaziDailyHourlyFlowResolution(
                schema=self.schema,
                status="FAILED",
                candidates=(),
                diagnostics=tuple(diagnostics),
            )
        return BaziDailyHourlyFlowResolution(
            schema=self.schema,
            status="RESOLVED" if len(rows) == 1 else "MULTI_CANDIDATE",
            candidates=tuple(rows),
            diagnostics=(),
        )
