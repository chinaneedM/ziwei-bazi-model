from __future__ import annotations

from typing import TYPE_CHECKING

from fortune_training.ziwei_chart.models import NatalChartState
from fortune_training.ziwei_structural import StructuralState
from fortune_training.ziwei_structural.r2 import RelativePalaceFrameState, validate_relative_frame_state

from .integrity import (
    adjacent_palace_hash_bundle,
    validate_adjacent_palace_components,
    validate_adjacent_palace_state,
)
from .models import AdjacentPalaceIntegrityReport, AdjacentPalacePairState
from .profile import ResolvedAdjacentPalacePairProfile
from .projection import AdjacentPalaceProjectionError, project_adjacent_palace_pairs

if TYPE_CHECKING:
    from fortune_training.ziwei_chart.engine import ZiweiChartCandidate


class AdjacentPalaceGenerationError(ValueError):
    def __init__(
        self,
        diagnostic_code: str,
        detail: str,
        *,
        report: AdjacentPalaceIntegrityReport | None = None,
    ) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code
        self.report = report


class ZiweiAdjacentPalaceRuntime:
    """V2-R8 source-backed bilateral neighbor projection over the frozen R2 frame."""

    @staticmethod
    def _raise_report(report: AdjacentPalaceIntegrityReport) -> None:
        first = report.diagnostics[0]
        raise AdjacentPalaceGenerationError(first.code, first.detail, report=report)

    def generate(
        self,
        natal_chart: NatalChartState,
        structural_state: StructuralState,
        r2_state: RelativePalaceFrameState,
        profile: ResolvedAdjacentPalacePairProfile,
        *,
        time_layer: str = "NATAL",
    ) -> AdjacentPalacePairState:
        try:
            profile.validate()
        except ValueError as exc:
            raise AdjacentPalaceGenerationError("INVALID_ADJACENT_PALACE_PROFILE", str(exc)) from exc
        r2_report = validate_relative_frame_state(natal_chart, structural_state, r2_state)
        if r2_report.status != "PASS":
            first = r2_report.diagnostics[0]
            raise AdjacentPalaceGenerationError(
                "UPSTREAM_R2_INTEGRITY_FAILED",
                f"{first.code}:{first.path}:{first.detail}",
            )
        if (
            r2_state.profile.profile_id != profile.upstream_r2_profile_id
            or r2_state.profile.profile_version != profile.upstream_r2_profile_version
        ):
            raise AdjacentPalaceGenerationError(
                "UPSTREAM_R2_PROFILE_MISMATCH",
                "R2 state profile does not match the R8 profile binding",
            )
        if time_layer != profile.supported_time_layer:
            raise AdjacentPalaceGenerationError(
                "UNSUPPORTED_ADJACENT_PALACE_TIME_LAYER",
                f"expected {profile.supported_time_layer}, got {time_layer}",
            )
        try:
            facts = project_adjacent_palace_pairs(r2_state)
        except AdjacentPalaceProjectionError as exc:
            raise AdjacentPalaceGenerationError(exc.diagnostic_code, str(exc)) from exc
        report = validate_adjacent_palace_components(r2_state, profile, time_layer, facts)
        if report.status != "PASS":
            self._raise_report(report)
        hashes = adjacent_palace_hash_bundle(
            r2_state.hashes.fact_hash,
            r2_state.hashes.computation_hash,
            profile,
            time_layer,
            facts,
        )
        state = AdjacentPalacePairState(
            upstream_r2_fact_hash=r2_state.hashes.fact_hash,
            upstream_r2_computation_hash=r2_state.hashes.computation_hash,
            profile=profile,
            time_layer=time_layer,
            adjacent_palace_pairs=facts,
            integrity=report,
            hashes=hashes,
        )
        final_report = validate_adjacent_palace_state(r2_state, state)
        if final_report.status != "PASS":
            self._raise_report(final_report)
        return state

    def generate_from_candidate(
        self,
        candidate: "ZiweiChartCandidate",
        structural_state: StructuralState,
        r2_state: RelativePalaceFrameState,
        profile: ResolvedAdjacentPalacePairProfile,
        *,
        time_layer: str = "NATAL",
    ) -> AdjacentPalacePairState:
        if candidate.integrity.status != "PASS":
            raise AdjacentPalaceGenerationError(
                "UPSTREAM_NATAL_INTEGRITY_FAILED",
                "ZiweiChartCandidate must carry a PASS natal integrity report",
            )
        return self.generate(
            candidate.chart,
            structural_state,
            r2_state,
            profile,
            time_layer=time_layer,
        )
