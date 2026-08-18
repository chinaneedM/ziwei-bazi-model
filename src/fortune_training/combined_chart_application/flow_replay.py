from __future__ import annotations

from typing import Protocol

from fortune_training.bazi_application import BaziApplicationFlowResolution

from .flow_models import (
    CombinedTargetFlowIntegrityReport,
    CombinedTargetFlowRequest,
    CombinedTargetFlowResolution,
)
from .models import CombinedChartApplicationResolution


class _CombinedTargetFlowResolver(Protocol):
    def resolve_with_bundles(
        self,
        request: CombinedTargetFlowRequest,
    ) -> tuple[
        CombinedChartApplicationResolution,
        BaziApplicationFlowResolution,
        CombinedTargetFlowResolution,
    ]: ...


def validate_combined_target_flow_full_replay(
    service: _CombinedTargetFlowResolver,
    request: CombinedTargetFlowRequest,
    base_resolution: CombinedChartApplicationResolution,
    bazi_flow_resolution: BaziApplicationFlowResolution,
    resolution: CombinedTargetFlowResolution,
) -> CombinedTargetFlowIntegrityReport:
    """Re-run the complete combined target-flow composition and compare outputs."""

    try:
        replayed_base, replayed_bazi_flow, replayed = service.resolve_with_bundles(
            request
        )
    except (ValueError, RuntimeError) as exc:
        return CombinedTargetFlowIntegrityReport(
            status="FAIL",
            diagnostics=(f"FULL_REPLAY_RESOLUTION_FAILED:{exc}",),
        )

    diagnostics: list[str] = []
    if replayed_base != base_resolution:
        diagnostics.append("BASE_COMBINED_FULL_REPLAY_MISMATCH")
    if replayed_bazi_flow != bazi_flow_resolution:
        diagnostics.append("BAZI_TARGET_FLOW_FULL_REPLAY_MISMATCH")
    if replayed != resolution:
        diagnostics.append("COMBINED_TARGET_FLOW_FULL_REPLAY_MISMATCH")
    return CombinedTargetFlowIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )
