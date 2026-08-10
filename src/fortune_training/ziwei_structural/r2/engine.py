from __future__ import annotations

from typing import TYPE_CHECKING

from fortune_training.ziwei_chart.integrity import HashBundle, validate_natal_chart
from fortune_training.ziwei_chart.models import NatalChartState
from fortune_training.ziwei_structural import StructuralState, validate_structural_state

from .frame import RelativePalaceFrameGenerator
from .integrity import (
    relative_frame_hash_bundle,
    validate_relative_frame_components,
    validate_relative_frame_state,
)
from .models import RelativeFrameIntegrityReport, RelativePalaceFrameState
from .profile import ResolvedRelativePalaceFrameProfile

if TYPE_CHECKING:
    from fortune_training.ziwei_chart.engine import ZiweiChartCandidate


class RelativeFrameGenerationError(ValueError):
    def __init__(
        self,
        diagnostic_code: str,
        detail: str,
        *,
        report: RelativeFrameIntegrityReport | None = None,
    ) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code
        self.report = report


class ZiweiRelativePalaceFrameRuntime:
    """Structural Runtime V2-R2 relative-frame compiler over V1 + R1 state."""

    def __init__(self) -> None:
        self.generator = RelativePalaceFrameGenerator()

    @staticmethod
    def _raise_report(report: RelativeFrameIntegrityReport) -> None:
        first = report.diagnostics[0]
        raise RelativeFrameGenerationError(first.code, first.detail, report=report)

    def generate(
        self,
        natal_chart: NatalChartState,
        natal_hashes: HashBundle,
        structural_state: StructuralState,
        profile: ResolvedRelativePalaceFrameProfile,
    ) -> RelativePalaceFrameState:
        try:
            profile.validate()
        except ValueError as exc:
            raise RelativeFrameGenerationError("INVALID_RELATIVE_FRAME_PROFILE", str(exc)) from exc

        natal_integrity = validate_natal_chart(natal_chart)
        if natal_integrity.status != "PASS":
            first = natal_integrity.diagnostics[0]
            raise RelativeFrameGenerationError(
                "UPSTREAM_NATAL_INTEGRITY_FAILED",
                f"{first.code}:{first.path}:{first.detail}",
            )

        structural_integrity = validate_structural_state(structural_state)
        if structural_integrity.status != "PASS":
            first = structural_integrity.diagnostics[0]
            raise RelativeFrameGenerationError(
                "UPSTREAM_STRUCTURAL_INTEGRITY_FAILED",
                f"{first.code}:{first.path}:{first.detail}",
            )

        if (
            natal_chart.profile_id != profile.natal_profile_id
            or natal_chart.profile_version != profile.natal_profile_version
        ):
            raise RelativeFrameGenerationError(
                "UPSTREAM_NATAL_PROFILE_MISMATCH",
                "Natal chart profile does not match the R2 profile binding",
            )
        if (
            structural_state.profile.profile_id != profile.structural_r1_profile_id
            or structural_state.profile.profile_version != profile.structural_r1_profile_version
        ):
            raise RelativeFrameGenerationError(
                "UPSTREAM_STRUCTURAL_PROFILE_MISMATCH",
                "R1 StructuralState profile does not match the R2 profile binding",
            )
        if (
            structural_state.upstream_natal_fact_hash != natal_hashes.fact_hash
            or structural_state.upstream_natal_computation_hash != natal_hashes.computation_hash
        ):
            raise RelativeFrameGenerationError(
                "CROSS_CHART_UPSTREAM_BINDING_MISMATCH",
                "R1 StructuralState and supplied Natal hashes do not describe the same computation",
            )

        facts = self.generator.generate(natal_chart)
        report = validate_relative_frame_components(
            natal_chart,
            structural_state,
            profile,
            facts,
        )
        if report.status != "PASS":
            self._raise_report(report)

        hashes = relative_frame_hash_bundle(
            structural_state.hashes.fact_hash,
            structural_state.hashes.computation_hash,
            profile,
            facts,
        )
        state = RelativePalaceFrameState(
            upstream_structural_fact_hash=structural_state.hashes.fact_hash,
            upstream_structural_computation_hash=structural_state.hashes.computation_hash,
            profile=profile,
            frame_facts=facts,
            integrity=report,
            hashes=hashes,
        )
        final_report = validate_relative_frame_state(natal_chart, structural_state, state)
        if final_report.status != "PASS":
            self._raise_report(final_report)
        return state

    def generate_from_candidate(
        self,
        candidate: "ZiweiChartCandidate",
        structural_state: StructuralState,
        profile: ResolvedRelativePalaceFrameProfile,
    ) -> RelativePalaceFrameState:
        if candidate.integrity.status != "PASS":
            raise RelativeFrameGenerationError(
                "UPSTREAM_NATAL_INTEGRITY_FAILED",
                "ZiweiChartCandidate must carry a PASS natal integrity report",
            )
        return self.generate(candidate.chart, candidate.hashes, structural_state, profile)
