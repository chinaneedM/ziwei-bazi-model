from __future__ import annotations

from fortune_training.bazi_target_temporal import (
    ResolvedTargetTemporalCoordinateProfile,
    TargetTemporalCoordinateResolution,
)
from fortune_training.ziwei_application import ApplicationChartBundle

from .shared_time_models import (
    SharedZiweiSelectorProjectionIntegrityReport,
    SharedZiweiSelectorProjectionResolution,
)
from .shared_time_service import (
    SharedZiweiSelectorProjectionError,
    SharedZiweiSelectorProjectionService,
)


def validate_shared_ziwei_selector_full_replay(
    service: SharedZiweiSelectorProjectionService,
    ziwei_bundle: ApplicationChartBundle,
    target_resolution: TargetTemporalCoordinateResolution,
    target_profile: ResolvedTargetTemporalCoordinateProfile,
    resolution: SharedZiweiSelectorProjectionResolution,
) -> SharedZiweiSelectorProjectionIntegrityReport:
    try:
        replayed = service.project(ziwei_bundle, target_resolution, target_profile)
    except SharedZiweiSelectorProjectionError as exc:
        return SharedZiweiSelectorProjectionIntegrityReport(
            status="FAIL",
            diagnostics=(f"FULL_REPLAY_RESOLUTION_FAILED:{exc.code}:{exc.detail}",),
        )

    if replayed != resolution:
        return SharedZiweiSelectorProjectionIntegrityReport(
            status="FAIL",
            diagnostics=("SHARED_ZIWEI_SELECTOR_FULL_REPLAY_MISMATCH",),
        )
    return SharedZiweiSelectorProjectionIntegrityReport(status="PASS", diagnostics=())
