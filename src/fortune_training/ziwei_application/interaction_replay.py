from __future__ import annotations

from typing import Protocol

from .interaction_models import (
    SanheInteractionIntegrityReport,
    SanheInteractionRequest,
    SanheInteractionResolution,
)
from .models import ApplicationChartBundle


class _SanheInteractionResolver(Protocol):
    def resolve_with_bundle(
        self,
        request: SanheInteractionRequest,
    ) -> tuple[ApplicationChartBundle, SanheInteractionResolution]: ...


def validate_sanhe_interaction_full_replay(
    service: _SanheInteractionResolver,
    request: SanheInteractionRequest,
    application_bundle: ApplicationChartBundle,
    resolution: SanheInteractionResolution,
) -> SanheInteractionIntegrityReport:
    """Re-run the released Application V1 plus the exact origin selection."""

    try:
        replayed_bundle, replayed_resolution = service.resolve_with_bundle(request)
    except ValueError as exc:
        return SanheInteractionIntegrityReport(
            status="FAIL",
            diagnostics=(f"FULL_REPLAY_RESOLUTION_FAILED:{exc}",),
        )

    diagnostics: list[str] = []
    if replayed_bundle != application_bundle:
        diagnostics.append("SOURCE_APPLICATION_FULL_REPLAY_MISMATCH")
    if replayed_resolution != resolution:
        diagnostics.append("SANHE_INTERACTION_FULL_REPLAY_MISMATCH")
    return SanheInteractionIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )
