from __future__ import annotations

from typing import TYPE_CHECKING

from fortune_training.ziwei_chart.integrity import HashBundle, validate_natal_chart
from fortune_training.ziwei_chart.models import NatalChartState
from fortune_training.ziwei_structural import StructuralState, validate_structural_state
from fortune_training.ziwei_structural.r2 import (
    RelativePalaceFrameState,
    validate_relative_frame_state,
)

from .integrity import (
    borrow_projection_hash_bundle,
    validate_borrow_projection_components,
    validate_borrow_projection_state,
)
from .models import BorrowProjectionIntegrityReport, BorrowProjectionState
from .profile import ResolvedBorrowProjectionProfile
from .projection import BorrowProjectionGenerator

if TYPE_CHECKING:
    from fortune_training.ziwei_chart.engine import ZiweiChartCandidate


class BorrowProjectionGenerationError(ValueError):
    def __init__(
        self,
        diagnostic_code: str,
        detail: str,
        *,
        report: BorrowProjectionIntegrityReport | None = None,
    ) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code
        self.report = report


class ZiweiBorrowProjectionRuntime:
    """V2-R3 structural borrow view over validated V1 + R1 + R2 state."""

    def __init__(self) -> None:
        self.generator = BorrowProjectionGenerator()

    @staticmethod
    def _raise_report(report: BorrowProjectionIntegrityReport) -> None:
        first = report.diagnostics[0]
        raise BorrowProjectionGenerationError(first.code, first.detail, report=report)

    def generate(
        self,
        natal_chart: NatalChartState,
        natal_hashes: HashBundle,
        structural_state: StructuralState,
        relative_state: RelativePalaceFrameState,
        profile: ResolvedBorrowProjectionProfile,
        *,
        time_layer: str = "NATAL",
    ) -> BorrowProjectionState:
        try:
            profile.validate()
        except ValueError as exc:
            raise BorrowProjectionGenerationError(
                "INVALID_BORROW_PROJECTION_PROFILE", str(exc)
            ) from exc

        natal_report = validate_natal_chart(natal_chart)
        if natal_report.status != "PASS":
            first = natal_report.diagnostics[0]
            raise BorrowProjectionGenerationError(
                "UPSTREAM_NATAL_INTEGRITY_FAILED",
                f"{first.code}:{first.path}:{first.detail}",
            )
        structural_report = validate_structural_state(structural_state)
        if structural_report.status != "PASS":
            first = structural_report.diagnostics[0]
            raise BorrowProjectionGenerationError(
                "UPSTREAM_STRUCTURAL_INTEGRITY_FAILED",
                f"{first.code}:{first.path}:{first.detail}",
            )
        relative_report = validate_relative_frame_state(
            natal_chart,
            structural_state,
            relative_state,
        )
        if relative_report.status != "PASS":
            first = relative_report.diagnostics[0]
            raise BorrowProjectionGenerationError(
                "UPSTREAM_RELATIVE_FRAME_INTEGRITY_FAILED",
                f"{first.code}:{first.path}:{first.detail}",
            )

        if (
            structural_state.upstream_natal_fact_hash != natal_hashes.fact_hash
            or structural_state.upstream_natal_computation_hash != natal_hashes.computation_hash
        ):
            raise BorrowProjectionGenerationError(
                "CROSS_CHART_V1_R1_BINDING_MISMATCH",
                "R1 state is not bound to the supplied Natal computation",
            )
        if (
            relative_state.upstream_structural_fact_hash != structural_state.hashes.fact_hash
            or relative_state.upstream_structural_computation_hash
            != structural_state.hashes.computation_hash
        ):
            raise BorrowProjectionGenerationError(
                "CROSS_STATE_R1_R2_BINDING_MISMATCH",
                "R2 state is not bound to the supplied R1 computation",
            )

        try:
            facts = self.generator.generate(
                natal_chart,
                relative_state,
                time_layer=time_layer,
            )
        except ValueError as exc:
            raise BorrowProjectionGenerationError(
                "BORROW_PROJECTION_GENERATION_FAILED", str(exc)
            ) from exc

        report = validate_borrow_projection_components(
            natal_chart,
            structural_state,
            relative_state,
            profile,
            time_layer,
            facts,
        )
        if report.status != "PASS":
            self._raise_report(report)

        hashes = borrow_projection_hash_bundle(
            relative_state.hashes.fact_hash,
            relative_state.hashes.computation_hash,
            profile,
            time_layer,
            facts,
        )
        state = BorrowProjectionState(
            upstream_relative_frame_fact_hash=relative_state.hashes.fact_hash,
            upstream_relative_frame_computation_hash=relative_state.hashes.computation_hash,
            profile=profile,
            time_layer=time_layer,
            member_facts=facts,
            integrity=report,
            hashes=hashes,
        )
        final_report = validate_borrow_projection_state(
            natal_chart,
            structural_state,
            relative_state,
            state,
        )
        if final_report.status != "PASS":
            self._raise_report(final_report)
        return state

    def generate_from_candidate(
        self,
        candidate: "ZiweiChartCandidate",
        structural_state: StructuralState,
        relative_state: RelativePalaceFrameState,
        profile: ResolvedBorrowProjectionProfile,
        *,
        time_layer: str = "NATAL",
    ) -> BorrowProjectionState:
        if candidate.integrity.status != "PASS":
            raise BorrowProjectionGenerationError(
                "UPSTREAM_NATAL_INTEGRITY_FAILED",
                "ZiweiChartCandidate must carry a PASS natal integrity report",
            )
        return self.generate(
            candidate.chart,
            candidate.hashes,
            structural_state,
            relative_state,
            profile,
            time_layer=time_layer,
        )
