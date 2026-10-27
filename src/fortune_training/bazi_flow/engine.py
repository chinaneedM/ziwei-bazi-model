from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from fortune_training.bazi_chart import BaziChartCandidate, ResolvedBaziCalculationProfile
from fortune_training.bazi_temporal import BaziTemporalCandidate, DayunFrame, PreDayunFrame
from fortune_training.calendar_foundation import BaziTimeResolver
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .models import (
    AnnualFrame,
    BaziFlowCandidate,
    BaziFlowContext,
    BaziFlowResolution,
    MonthlyFrame,
)
from .profile import (
    ACTIVE_DAYUN_RULE_SET_VERSION,
    ANNUAL_RULE_SET_ID,
    ANNUAL_RULE_SET_VERSION,
    FLOW_ALGORITHM_VERSION,
    INTERVAL_SEMANTICS,
    MONTHLY_RULE_SET_ID,
    MONTHLY_RULE_SET_VERSION,
)


class BaziFlowGenerationError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class BaziFlowRequest:
    natal_candidate: BaziChartCandidate
    temporal_candidates: tuple[BaziTemporalCandidate, ...]
    target_utc: datetime
    calculation_profile: ResolvedBaziCalculationProfile


def _utc_fact(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds")


def _stable_frame_id(kind: str, payload: dict[str, Any]) -> str:
    return f"{kind}:{object_sha256(payload)}"


def _select_active_dayun(
    temporal: BaziTemporalCandidate,
    target_utc: datetime,
) -> tuple[str, PreDayunFrame | DayunFrame]:
    state = temporal.state
    birth = state.pre_dayun.start_utc.astimezone(timezone.utc)
    target = target_utc.astimezone(timezone.utc)
    if target < birth:
        raise BaziFlowGenerationError(
            "TARGET_BEFORE_BIRTH",
            f"{target.isoformat()} < {birth.isoformat()}",
        )
    pre = state.pre_dayun
    if pre.start_utc <= target < pre.end_utc:
        return "PRE_DAYUN", pre
    for frame in state.dayun_frames:
        if frame.start_utc <= target < frame.end_utc:
            return "DAYUN", frame
    last_end = state.dayun_frames[-1].end_utc if state.dayun_frames else pre.end_utc
    if target >= last_end:
        raise BaziFlowGenerationError(
            "TARGET_OUT_OF_MATERIALIZED_DAYUN_RANGE",
            f"{target.isoformat()} >= {last_end.isoformat()}",
        )
    raise BaziFlowGenerationError(
        "TARGET_NOT_CONTAINED_IN_DAYUN_SCHEDULE",
        target.isoformat(),
    )


class BaziFlowEngine:
    schema = "BAZI-FLOW-CONTEXT-RESULT-V1"
    typed_schema = "BAZI-FLOW-CONTEXT-TYPED-RESOLUTION-V1"

    def __init__(self, bazi_time: BaziTimeResolver | None = None) -> None:
        self.bazi_time = bazi_time or BaziTimeResolver()

    def _frames(self, target_utc: datetime, year_boundary_policy: str) -> tuple[AnnualFrame, MonthlyFrame]:
        resolved = self.bazi_time.resolve_year_month(
            target_utc,
            year_boundary_policy=year_boundary_policy,
        )
        annual_payload = {
            "pillar_year": resolved.pillar_year,
            "ganzhi": resolved.year_pillar,
            "start_utc": _utc_fact(resolved.annual_start_boundary.utc_instant),
            "end_utc": _utc_fact(resolved.annual_end_boundary.utc_instant),
            "year_boundary_policy": year_boundary_policy,
        }
        annual = AnnualFrame(
            frame_id=_stable_frame_id("ANNUAL", annual_payload),
            pillar_year=resolved.pillar_year,
            ganzhi=resolved.year_pillar,
            sexagenary_index=resolved.year_sexagenary_index,
            start_term_name=resolved.annual_start_boundary.name,
            start_term_chinese_name=resolved.annual_start_boundary.chinese_name,
            start_utc=resolved.annual_start_boundary.utc_instant,
            end_term_name=resolved.annual_end_boundary.name,
            end_term_chinese_name=resolved.annual_end_boundary.chinese_name,
            end_utc=resolved.annual_end_boundary.utc_instant,
            interval_semantics=resolved.interval_semantics,
            year_boundary_policy=resolved.year_boundary_policy,
            solar_term_algorithm_id=resolved.annual_start_boundary.algorithm_id,
            solar_term_algorithm_version=resolved.annual_start_boundary.algorithm_version,
            source_refs=("TIME-CALENDAR-FOUNDATION-R1", ANNUAL_RULE_SET_ID),
        )
        monthly_payload = {
            "ganzhi": resolved.month_pillar,
            "start_jie": resolved.active_month_boundary.name,
            "start_utc": _utc_fact(resolved.active_month_boundary.utc_instant),
            "end_jie": resolved.next_month_boundary.name,
            "end_utc": _utc_fact(resolved.next_month_boundary.utc_instant),
        }
        monthly = MonthlyFrame(
            frame_id=_stable_frame_id("MONTHLY", monthly_payload),
            ganzhi=resolved.month_pillar,
            sexagenary_index=resolved.month_sexagenary_index,
            start_jie_name=resolved.active_month_boundary.name,
            start_jie_chinese_name=resolved.active_month_boundary.chinese_name,
            start_jie_longitude_degrees=resolved.active_month_boundary.longitude_degrees,
            start_utc=resolved.active_month_boundary.utc_instant,
            end_jie_name=resolved.next_month_boundary.name,
            end_jie_chinese_name=resolved.next_month_boundary.chinese_name,
            end_jie_longitude_degrees=resolved.next_month_boundary.longitude_degrees,
            end_utc=resolved.next_month_boundary.utc_instant,
            interval_semantics=resolved.interval_semantics,
            solar_term_algorithm_id=resolved.active_month_boundary.algorithm_id,
            solar_term_algorithm_version=resolved.active_month_boundary.algorithm_version,
            source_refs=("TIME-CALENDAR-FOUNDATION-R1", MONTHLY_RULE_SET_ID),
        )
        return annual, monthly

    def _context(
        self,
        request: BaziFlowRequest,
        temporal: BaziTemporalCandidate,
        target_utc: datetime,
    ) -> BaziFlowContext:
        if temporal.state.upstream_natal_fact_hash != request.natal_candidate.hashes.fact_hash:
            raise BaziFlowGenerationError(
                "UPSTREAM_NATAL_HASH_MISMATCH",
                temporal.state.upstream_natal_fact_hash,
            )
        chart = request.natal_candidate.chart
        profile = request.calculation_profile
        if (chart.profile_id, chart.profile_version) != (profile.profile_id, profile.profile_version):
            raise BaziFlowGenerationError(
                "NATAL_PROFILE_BINDING_MISMATCH",
                f"{chart.profile_id}@{chart.profile_version}",
            )
        year_policy = profile.time_calendar_policies.bazi_year_boundary_policy
        active_kind, active_frame = _select_active_dayun(temporal, target_utc)
        annual, monthly = self._frames(target_utc, year_policy)
        return BaziFlowContext(
            upstream_natal_fact_hash=request.natal_candidate.hashes.fact_hash,
            upstream_temporal_fact_hash=temporal.hashes.fact_hash,
            target_utc=target_utc,
            active_dayun_kind=active_kind,
            active_dayun_frame=active_frame,
            annual_frame=annual,
            monthly_frame=monthly,
            natal_profile_id=profile.profile_id,
            natal_profile_version=profile.profile_version,
            temporal_profile_id=temporal.state.profile_id,
            temporal_profile_version=temporal.state.profile_version,
            time_calendar_policy_registry_version=profile.time_calendar_policy_registry_version,
            year_boundary_policy=year_policy,
            algorithm_versions={
                "flow": FLOW_ALGORITHM_VERSION,
                "annual": ANNUAL_RULE_SET_VERSION,
                "monthly": MONTHLY_RULE_SET_VERSION,
                "active_dayun": ACTIVE_DAYUN_RULE_SET_VERSION,
                "bazi_year_month": "1.0.0",
            },
        )

    def resolve_typed(self, request: BaziFlowRequest) -> BaziFlowResolution:
        if request.target_utc.tzinfo is None or request.target_utc.utcoffset() is None:
            return BaziFlowResolution(
                schema=self.typed_schema,
                status="FAILED",
                candidates=(),
                events=(),
                diagnostics=("INVALID_TARGET_INSTANT:timezone-aware UTC instant required",),
            )
        target = request.target_utc.astimezone(timezone.utc)
        if not request.temporal_candidates:
            return BaziFlowResolution(
                schema=self.typed_schema,
                status="FAILED",
                candidates=(),
                events=(),
                diagnostics=("NO_TEMPORAL_CANDIDATES",),
            )

        from .integrity import flow_hash_bundle, validate_flow_context

        unique: dict[str, dict[str, Any]] = {}
        try:
            for index, temporal in enumerate(request.temporal_candidates):
                context = self._context(request, temporal, target)
                report = validate_flow_context(
                    context,
                    request.natal_candidate,
                    temporal,
                    request.calculation_profile,
                    self.bazi_time,
                )
                if report.status != "PASS":
                    return BaziFlowResolution(
                        schema=self.typed_schema,
                        status="FAILED",
                        candidates=(),
                        events=(),
                        diagnostics=tuple(
                            f"INTEGRITY:{row.code}:{row.path}" for row in report.diagnostics
                        ),
                    )
                hashes = flow_hash_bundle(
                    context,
                    request.natal_candidate,
                    temporal,
                    request.calculation_profile,
                )
                row = unique.get(hashes.fact_hash)
                if row is None:
                    unique[hashes.fact_hash] = {
                        "indices": [index],
                        "seed_ids": list(temporal.source_temporal_seed_ids),
                        "context": context,
                        "integrity": report,
                        "hashes": hashes,
                    }
                else:
                    if row["hashes"].computation_hash != hashes.computation_hash:
                        return BaziFlowResolution(
                            schema=self.typed_schema,
                            status="FAILED",
                            candidates=(),
                            events=(),
                            diagnostics=(
                                "INTEGRITY:SAME_FLOW_FACT_DIFFERENT_COMPUTATION_LINEAGE",
                            ),
                        )
                    row["indices"].append(index)
                    row["seed_ids"].extend(temporal.source_temporal_seed_ids)
        except (BaziFlowGenerationError, ValueError) as exc:
            code = getattr(exc, "diagnostic_code", "FLOW_GENERATION_FAILED")
            return BaziFlowResolution(
                schema=self.typed_schema,
                status="FAILED",
                candidates=(),
                events=(),
                diagnostics=(f"{code}:{exc}",),
            )

        candidates = tuple(
            BaziFlowCandidate(
                source_temporal_candidate_indices=tuple(row["indices"]),
                source_temporal_seed_ids=tuple(dict.fromkeys(row["seed_ids"])),
                context=row["context"],
                integrity=row["integrity"],
                hashes=row["hashes"],
            )
            for row in unique.values()
        )
        return BaziFlowResolution(
            schema=self.typed_schema,
            status="RESOLVED" if len(candidates) == 1 else "MULTI_CANDIDATE",
            candidates=candidates,
            events=("TEMPORAL_CANDIDATES_PRESERVED",) if len(candidates) > 1 else (),
            diagnostics=(),
        )

    def resolve(self, request: BaziFlowRequest) -> dict[str, Any]:
        typed = self.resolve_typed(request)
        return {
            "schema": self.schema,
            "typed_schema": typed.schema,
            "status": typed.status,
            "target_utc": json_value(
                request.target_utc.astimezone(timezone.utc)
                if request.target_utc.tzinfo is not None and request.target_utc.utcoffset() is not None
                else request.target_utc
            ),
            "upstream_natal_fact_hash": request.natal_candidate.hashes.fact_hash,
            "calculation_profile": json_value(request.calculation_profile),
            "temporal_candidate_count": len(request.temporal_candidates),
            "candidates": [json_value(row) for row in typed.candidates],
            "events": list(typed.events),
            "diagnostics": list(typed.diagnostics),
        }
