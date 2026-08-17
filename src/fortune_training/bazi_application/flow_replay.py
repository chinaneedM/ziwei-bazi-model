from __future__ import annotations

from typing import Protocol

from .flow_models import (
    BaziApplicationFlowIntegrityReport,
    BaziApplicationFlowRequest,
    BaziApplicationFlowResolution,
)
from .service import BaziApplicationResolutionError


class _FlowResolver(Protocol):
    def resolve(
        self, request: BaziApplicationFlowRequest
    ) -> BaziApplicationFlowResolution: ...


def validate_application_flow_full_replay(
    service: _FlowResolver,
    request: BaziApplicationFlowRequest,
    resolution: BaziApplicationFlowResolution,
) -> BaziApplicationFlowIntegrityReport:
    """Re-run the complete target-flow composition and compare exact output.

    This deliberately sits above the structural/hash validator.  The service
    replay re-executes the released Application V1, Natal/Temporal, target
    coordinate, Flow, and Daily/Hourly integrity paths before producing the
    comparison object, so a locally self-consistent rewritten payload cannot
    substitute for the deterministic upstream computation.
    """

    try:
        replayed = service.resolve(request)
    except BaziApplicationResolutionError as exc:
        return BaziApplicationFlowIntegrityReport(
            status="FAIL",
            diagnostics=(f"FULL_REPLAY_RESOLUTION_FAILED:{exc.code}:{exc.detail}",),
        )
    except ValueError as exc:
        return BaziApplicationFlowIntegrityReport(
            status="FAIL",
            diagnostics=(f"FULL_REPLAY_VALUE_ERROR:{exc}",),
        )

    if replayed != resolution:
        return BaziApplicationFlowIntegrityReport(
            status="FAIL",
            diagnostics=("FULL_REPLAY_MISMATCH",),
        )
    return BaziApplicationFlowIntegrityReport(status="PASS", diagnostics=())
