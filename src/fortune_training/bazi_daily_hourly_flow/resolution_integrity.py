from __future__ import annotations

from datetime import timezone

from fortune_training.bazi_chart import ResolvedBaziCalculationProfile
from fortune_training.bazi_flow import BaziFlowCandidate
from fortune_training.bazi_target_temporal import (
    ResolvedTargetTemporalCoordinateProfile,
    TargetTemporalCoordinateResolution,
)
from fortune_training.calendar_foundation import BaziTimeResolver

from .integrity import daily_hourly_hash_bundle, validate_daily_hourly_context
from .models import (
    BaziDailyHourlyFlowResolution,
    DailyHourlyIntegrityDiagnostic,
    DailyHourlyIntegrityReport,
)


RESOLUTION_INTEGRITY_ALGORITHM_ID = "BAZI-DAILY-HOURLY-FLOW-RESOLUTION-INTEGRITY-R1"
RESOLUTION_INTEGRITY_ALGORITHM_VERSION = "1.0.0"


def _diag(rows: list[DailyHourlyIntegrityDiagnostic], code: str, path: str, detail: str) -> None:
    rows.append(DailyHourlyIntegrityDiagnostic(code=code, path=path, detail=detail))


def validate_daily_hourly_resolution(
    resolution: BaziDailyHourlyFlowResolution,
    flow_candidates: tuple[BaziFlowCandidate, ...],
    target_resolution: TargetTemporalCoordinateResolution,
    target_profile: ResolvedTargetTemporalCoordinateProfile,
    calculation_profile: ResolvedBaziCalculationProfile,
    bazi_time: BaziTimeResolver,
) -> DailyHourlyIntegrityReport:
    diagnostics: list[DailyHourlyIntegrityDiagnostic] = []

    if resolution.schema != "BAZI-DAILY-HOURLY-FLOW-RESOLUTION-R1":
        _diag(diagnostics, "RESOLUTION_SCHEMA_MISMATCH", "schema", resolution.schema)

    expected_status = "FAILED" if not resolution.candidates else (
        "RESOLVED" if len(resolution.candidates) == 1 else "MULTI_CANDIDATE"
    )
    if resolution.status != expected_status:
        _diag(diagnostics, "RESOLUTION_STATUS_MISMATCH", "status", expected_status)
    if resolution.status == "FAILED" and not resolution.diagnostics:
        _diag(diagnostics, "FAILED_RESOLUTION_WITHOUT_DIAGNOSTIC", "diagnostics", "at least one diagnostic required")
    if resolution.status != "FAILED" and resolution.diagnostics:
        _diag(diagnostics, "RESOLVED_WITH_DIAGNOSTICS", "diagnostics", str(resolution.diagnostics))

    seen_pairs: set[tuple[int, int]] = set()
    for index, candidate in enumerate(resolution.candidates):
        path = f"candidates[{index}]"
        flow_index = candidate.source_flow_candidate_index
        target_index = candidate.source_target_coordinate_candidate_index
        pair = (flow_index, target_index)
        if pair in seen_pairs:
            _diag(diagnostics, "DUPLICATE_SOURCE_INDEX_PAIR", path, str(pair))
        seen_pairs.add(pair)

        if candidate.context.source_flow_candidate_index != flow_index:
            _diag(
                diagnostics,
                "OUTER_FLOW_INDEX_LINEAGE_MISMATCH",
                f"{path}.source_flow_candidate_index",
                f"context={candidate.context.source_flow_candidate_index}",
            )
        if candidate.context.source_target_coordinate_candidate_index != target_index:
            _diag(
                diagnostics,
                "OUTER_TARGET_INDEX_LINEAGE_MISMATCH",
                f"{path}.source_target_coordinate_candidate_index",
                f"context={candidate.context.source_target_coordinate_candidate_index}",
            )

        if not 0 <= flow_index < len(flow_candidates):
            _diag(diagnostics, "SOURCE_FLOW_CANDIDATE_INDEX_INVALID", f"{path}.source_flow_candidate_index", str(flow_index))
            continue
        if not 0 <= target_index < len(target_resolution.candidates):
            _diag(diagnostics, "SOURCE_TARGET_CANDIDATE_INDEX_INVALID", f"{path}.source_target_coordinate_candidate_index", str(target_index))
            continue

        flow = flow_candidates[flow_index]
        target = target_resolution.candidates[target_index]
        if flow.context.target_utc.astimezone(timezone.utc) != target.target_utc.astimezone(timezone.utc):
            _diag(diagnostics, "SOURCE_PAIR_UTC_MISMATCH", path, target.target_utc.isoformat())

        replay = validate_daily_hourly_context(
            candidate.context,
            flow,
            target_resolution,
            target_profile,
            calculation_profile,
            bazi_time,
        )
        if replay.status != "PASS":
            for item in replay.diagnostics:
                _diag(diagnostics, f"CONTEXT_{item.code}", f"{path}.{item.path}", item.detail)
        if candidate.integrity != replay:
            _diag(diagnostics, "STORED_INTEGRITY_REPLAY_MISMATCH", f"{path}.integrity", replay.status)

        expected_hashes = daily_hourly_hash_bundle(candidate.context, calculation_profile)
        if candidate.hashes != expected_hashes:
            _diag(
                diagnostics,
                "STORED_HASH_REPLAY_MISMATCH",
                f"{path}.hashes",
                f"expected={expected_hashes.fact_hash}/{expected_hashes.computation_hash}",
            )

    if resolution.status != "FAILED":
        expected_pairs = {
            (flow_index, target_index)
            for target_index, target in enumerate(target_resolution.candidates)
            for flow_index, flow in enumerate(flow_candidates)
            if flow.context.target_utc.astimezone(timezone.utc) == target.target_utc.astimezone(timezone.utc)
        }
        if seen_pairs != expected_pairs:
            _diag(
                diagnostics,
                "COMPATIBLE_SOURCE_PAIR_COVERAGE_MISMATCH",
                "candidates",
                f"expected={sorted(expected_pairs)} actual={sorted(seen_pairs)}",
            )

    return DailyHourlyIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=RESOLUTION_INTEGRITY_ALGORITHM_ID,
        algorithm_version=RESOLUTION_INTEGRITY_ALGORITHM_VERSION,
    )
