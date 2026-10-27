from __future__ import annotations

from datetime import timezone
from typing import Any

from fortune_training.bazi_chart import BaziChartCandidate, ResolvedBaziCalculationProfile
from fortune_training.bazi_temporal import BaziTemporalCandidate, DayunFrame
from fortune_training.calendar_foundation import BaziTimeResolver
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .models import (
    BaziFlowContext,
    FlowHashBundle,
    FlowIntegrityDiagnostic,
    FlowIntegrityReport,
)
from .profile import (
    ACTIVE_DAYUN_RULE_SET_VERSION,
    ANNUAL_RULE_SET_VERSION,
    FLOW_ALGORITHM_VERSION,
    INTERVAL_SEMANTICS,
    MONTHLY_RULE_SET_VERSION,
)


INTEGRITY_ALGORITHM_ID = "BAZI-FLOW-INTEGRITY-V1"
INTEGRITY_ALGORITHM_VERSION = "1.0.0"
HASH_ALGORITHM_ID = "BAZI-FLOW-HASH-V1"
HASH_ALGORITHM_VERSION = "1.0.0"


def _diag(rows: list[FlowIntegrityDiagnostic], code: str, path: str, detail: str) -> None:
    rows.append(FlowIntegrityDiagnostic(code=code, path=path, detail=detail))


def _instant_fact(value) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("flow fact instant must be timezone-aware")
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds")


def _frame_fact(frame) -> dict[str, Any]:
    payload = {
        "start_utc": _instant_fact(frame.start_utc),
        "end_utc": _instant_fact(frame.end_utc),
        "interval_semantics": frame.interval_semantics,
    }
    if isinstance(frame, DayunFrame):
        payload.update(
            {
                "index": frame.index,
                "ganzhi": frame.ganzhi,
                "sexagenary_index": frame.sexagenary_index,
            }
        )
    return payload


def validate_flow_context(
    context: BaziFlowContext,
    natal: BaziChartCandidate,
    temporal: BaziTemporalCandidate,
    profile: ResolvedBaziCalculationProfile,
    bazi_time: BaziTimeResolver,
) -> FlowIntegrityReport:
    diagnostics: list[FlowIntegrityDiagnostic] = []
    target = context.target_utc.astimezone(timezone.utc)

    if context.upstream_natal_fact_hash != natal.hashes.fact_hash:
        _diag(diagnostics, "UPSTREAM_NATAL_HASH_MISMATCH", "upstream_natal_fact_hash", context.upstream_natal_fact_hash)
    if context.upstream_temporal_fact_hash != temporal.hashes.fact_hash:
        _diag(diagnostics, "UPSTREAM_TEMPORAL_HASH_MISMATCH", "upstream_temporal_fact_hash", context.upstream_temporal_fact_hash)
    if temporal.state.upstream_natal_fact_hash != natal.hashes.fact_hash:
        _diag(diagnostics, "TEMPORAL_NATAL_HASH_MISMATCH", "upstream", temporal.state.upstream_natal_fact_hash)
    if (context.natal_profile_id, context.natal_profile_version) != (profile.profile_id, profile.profile_version):
        _diag(diagnostics, "NATAL_PROFILE_LINEAGE_MISMATCH", "natal_profile_id", context.natal_profile_id)
    if (context.temporal_profile_id, context.temporal_profile_version) != (
        temporal.state.profile_id,
        temporal.state.profile_version,
    ):
        _diag(diagnostics, "TEMPORAL_PROFILE_LINEAGE_MISMATCH", "temporal_profile_id", context.temporal_profile_id)
    if context.time_calendar_policy_registry_version != profile.time_calendar_policy_registry_version:
        _diag(diagnostics, "POLICY_REGISTRY_LINEAGE_MISMATCH", "time_calendar_policy_registry_version", context.time_calendar_policy_registry_version)
    expected_policy = profile.time_calendar_policies.bazi_year_boundary_policy
    if context.year_boundary_policy != expected_policy:
        _diag(diagnostics, "YEAR_BOUNDARY_POLICY_MISMATCH", "year_boundary_policy", context.year_boundary_policy)
    expected_algorithms = {
        "flow": FLOW_ALGORITHM_VERSION,
        "annual": ANNUAL_RULE_SET_VERSION,
        "monthly": MONTHLY_RULE_SET_VERSION,
        "active_dayun": ACTIVE_DAYUN_RULE_SET_VERSION,
        "bazi_year_month": "1.0.0",
    }
    for name, version in expected_algorithms.items():
        if context.algorithm_versions.get(name) != version:
            _diag(
                diagnostics,
                "FLOW_ALGORITHM_VERSION_MISMATCH",
                f"algorithm_versions.{name}",
                str(context.algorithm_versions.get(name)),
            )

    active = context.active_dayun_frame
    if active.interval_semantics != INTERVAL_SEMANTICS:
        _diag(diagnostics, "ACTIVE_DAYUN_INTERVAL_SEMANTICS_MISMATCH", "active_dayun_frame.interval_semantics", active.interval_semantics)
    if not active.start_utc <= target < active.end_utc:
        _diag(diagnostics, "TARGET_OUTSIDE_ACTIVE_DAYUN", "active_dayun_frame", target.isoformat())
    expected_kind = "DAYUN" if isinstance(active, DayunFrame) else "PRE_DAYUN"
    if context.active_dayun_kind != expected_kind:
        _diag(diagnostics, "ACTIVE_DAYUN_KIND_MISMATCH", "active_dayun_kind", expected_kind)
    all_frames = (temporal.state.pre_dayun,) + temporal.state.dayun_frames
    containing = [frame for frame in all_frames if frame.start_utc <= target < frame.end_utc]
    if len(containing) != 1 or containing[0] != active:
        _diag(diagnostics, "ACTIVE_DAYUN_REPLAY_MISMATCH", "active_dayun_frame", str(len(containing)))

    resolved = bazi_time.resolve_year_month(target, year_boundary_policy=expected_policy)
    annual = context.annual_frame
    expected_annual_id = "ANNUAL:" + object_sha256(
        {
            "pillar_year": resolved.pillar_year,
            "ganzhi": resolved.year_pillar,
            "start_utc": _instant_fact(resolved.annual_start_boundary.utc_instant),
            "end_utc": _instant_fact(resolved.annual_end_boundary.utc_instant),
            "year_boundary_policy": expected_policy,
        }
    )
    if annual.frame_id != expected_annual_id:
        _diag(diagnostics, "ANNUAL_FRAME_ID_MISMATCH", "annual_frame.frame_id", expected_annual_id)
    if not annual.start_utc <= target < annual.end_utc:
        _diag(diagnostics, "TARGET_OUTSIDE_ANNUAL_FRAME", "annual_frame", target.isoformat())
    if (
        annual.ganzhi != resolved.year_pillar
        or annual.sexagenary_index != resolved.year_sexagenary_index
        or annual.pillar_year != resolved.pillar_year
    ):
        _diag(diagnostics, "ANNUAL_GANZHI_REPLAY_MISMATCH", "annual_frame.ganzhi", resolved.year_pillar)
    if (
        annual.start_utc != resolved.annual_start_boundary.utc_instant
        or annual.end_utc != resolved.annual_end_boundary.utc_instant
        or annual.start_term_name != resolved.annual_start_boundary.name
        or annual.end_term_name != resolved.annual_end_boundary.name
        or annual.start_term_chinese_name != resolved.annual_start_boundary.chinese_name
        or annual.end_term_chinese_name != resolved.annual_end_boundary.chinese_name
        or annual.solar_term_algorithm_id != resolved.annual_start_boundary.algorithm_id
        or annual.solar_term_algorithm_version != resolved.annual_start_boundary.algorithm_version
    ):
        _diag(diagnostics, "ANNUAL_BOUNDARY_REPLAY_MISMATCH", "annual_frame", str(resolved.pillar_year))
    if annual.interval_semantics != INTERVAL_SEMANTICS or annual.year_boundary_policy != expected_policy:
        _diag(diagnostics, "ANNUAL_POLICY_OR_INTERVAL_MISMATCH", "annual_frame.interval_semantics", annual.interval_semantics)

    monthly = context.monthly_frame
    expected_monthly_id = "MONTHLY:" + object_sha256(
        {
            "ganzhi": resolved.month_pillar,
            "start_jie": resolved.active_month_boundary.name,
            "start_utc": _instant_fact(resolved.active_month_boundary.utc_instant),
            "end_jie": resolved.next_month_boundary.name,
            "end_utc": _instant_fact(resolved.next_month_boundary.utc_instant),
        }
    )
    if monthly.frame_id != expected_monthly_id:
        _diag(diagnostics, "MONTHLY_FRAME_ID_MISMATCH", "monthly_frame.frame_id", expected_monthly_id)
    if not monthly.start_utc <= target < monthly.end_utc:
        _diag(diagnostics, "TARGET_OUTSIDE_MONTHLY_FRAME", "monthly_frame", target.isoformat())
    if monthly.ganzhi != resolved.month_pillar or monthly.sexagenary_index != resolved.month_sexagenary_index:
        _diag(diagnostics, "MONTHLY_GANZHI_REPLAY_MISMATCH", "monthly_frame.ganzhi", resolved.month_pillar)
    if (
        monthly.start_utc != resolved.active_month_boundary.utc_instant
        or monthly.end_utc != resolved.next_month_boundary.utc_instant
        or monthly.start_jie_name != resolved.active_month_boundary.name
        or monthly.end_jie_name != resolved.next_month_boundary.name
        or monthly.start_jie_chinese_name != resolved.active_month_boundary.chinese_name
        or monthly.end_jie_chinese_name != resolved.next_month_boundary.chinese_name
        or monthly.start_jie_longitude_degrees != resolved.active_month_boundary.longitude_degrees
        or monthly.end_jie_longitude_degrees != resolved.next_month_boundary.longitude_degrees
        or monthly.solar_term_algorithm_id != resolved.active_month_boundary.algorithm_id
        or monthly.solar_term_algorithm_version != resolved.active_month_boundary.algorithm_version
    ):
        _diag(diagnostics, "MONTHLY_BOUNDARY_REPLAY_MISMATCH", "monthly_frame", resolved.month_pillar)
    if monthly.interval_semantics != INTERVAL_SEMANTICS:
        _diag(diagnostics, "MONTHLY_INTERVAL_SEMANTICS_MISMATCH", "monthly_frame.interval_semantics", monthly.interval_semantics)
    if not annual.source_refs or not monthly.source_refs:
        _diag(diagnostics, "MISSING_FLOW_PROVENANCE", "annual_monthly", "source_refs required")

    return FlowIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=INTEGRITY_ALGORITHM_ID,
        algorithm_version=INTEGRITY_ALGORITHM_VERSION,
    )


def flow_fact_projection(context: BaziFlowContext) -> dict[str, Any]:
    annual = context.annual_frame
    monthly = context.monthly_frame
    return {
        "upstream_natal_fact_hash": context.upstream_natal_fact_hash,
        "upstream_temporal_fact_hash": context.upstream_temporal_fact_hash,
        "target_utc": _instant_fact(context.target_utc),
        "active_dayun_kind": context.active_dayun_kind,
        "active_dayun_frame": _frame_fact(context.active_dayun_frame),
        "annual_frame": {
            "frame_id": annual.frame_id,
            "pillar_year": annual.pillar_year,
            "ganzhi": annual.ganzhi,
            "sexagenary_index": annual.sexagenary_index,
            "start_term_name": annual.start_term_name,
            "start_utc": _instant_fact(annual.start_utc),
            "end_term_name": annual.end_term_name,
            "end_utc": _instant_fact(annual.end_utc),
            "interval_semantics": annual.interval_semantics,
            "year_boundary_policy": annual.year_boundary_policy,
        },
        "monthly_frame": {
            "frame_id": monthly.frame_id,
            "ganzhi": monthly.ganzhi,
            "sexagenary_index": monthly.sexagenary_index,
            "start_jie_name": monthly.start_jie_name,
            "start_jie_longitude_degrees": monthly.start_jie_longitude_degrees,
            "start_utc": _instant_fact(monthly.start_utc),
            "end_jie_name": monthly.end_jie_name,
            "end_jie_longitude_degrees": monthly.end_jie_longitude_degrees,
            "end_utc": _instant_fact(monthly.end_utc),
            "interval_semantics": monthly.interval_semantics,
        },
        "year_boundary_policy": context.year_boundary_policy,
    }


def flow_hash_bundle(
    context: BaziFlowContext,
    natal: BaziChartCandidate,
    temporal: BaziTemporalCandidate,
    profile: ResolvedBaziCalculationProfile,
) -> FlowHashBundle:
    fact_hash = object_sha256(flow_fact_projection(context))
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "upstream_natal_computation_hash": natal.hashes.computation_hash,
            "upstream_temporal_computation_hash": temporal.hashes.computation_hash,
            "resolved_calculation_profile": json_value(profile),
            "flow_lineage": {
                "natal_profile": f"{context.natal_profile_id}@{context.natal_profile_version}",
                "temporal_profile": f"{context.temporal_profile_id}@{context.temporal_profile_version}",
                "policy_registry_version": context.time_calendar_policy_registry_version,
                "algorithm_versions": dict(sorted(context.algorithm_versions.items())),
                "annual_source_refs": sorted(context.annual_frame.source_refs),
                "monthly_source_refs": sorted(context.monthly_frame.source_refs),
            },
            "hash_algorithm": f"{HASH_ALGORITHM_ID}@{HASH_ALGORITHM_VERSION}",
        }
    )
    return FlowHashBundle(
        fact_hash=fact_hash,
        computation_hash=computation_hash,
        algorithm_id=HASH_ALGORITHM_ID,
        algorithm_version=HASH_ALGORITHM_VERSION,
    )
