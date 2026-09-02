from __future__ import annotations

from typing import TYPE_CHECKING

from fortune_training.ziwei_chart.models import NatalChartState
from fortune_training.ziwei_structural import StructuralState
from fortune_training.ziwei_structural.r2 import RelativePalaceFrameState, validate_relative_frame_state

from .integrity import qishu_hash_bundle, validate_qishu_components, validate_qishu_state
from .models import QiShuIntegrityReport, QiShuPositionState
from .profile import ResolvedQiShuPositionProfile
from .projection import QiShuProjectionError, project_qishu_positions

if TYPE_CHECKING:
    from fortune_training.ziwei_chart.engine import ZiweiChartCandidate


class QiShuGenerationError(ValueError):
    def __init__(
        self,
        diagnostic_code: str,
        detail: str,
        *,
        report: QiShuIntegrityReport | None = None,
    ) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code
        self.report = report


class ZiweiQiShuPositionRuntime:
    """V2-R6 source-backed QiShu position projection over the frozen R2 frame."""

    @staticmethod
    def _raise_report(report: QiShuIntegrityReport) -> None:
        first = report.diagnostics[0]
        raise QiShuGenerationError(first.code, first.detail, report=report)

    def generate(
        self,
        natal_chart: NatalChartState,
        structural_state: StructuralState,
        r2_state: RelativePalaceFrameState,
        profile: ResolvedQiShuPositionProfile,
        *,
        time_layer: str = "NATAL",
    ) -> QiShuPositionState:
        try:
            profile.validate()
        except ValueError as exc:
            raise QiShuGenerationError("INVALID_QISHU_PROFILE", str(exc)) from exc

        r2_report = validate_relative_frame_state(natal_chart, structural_state, r2_state)
        if r2_report.status != "PASS":
            first = r2_report.diagnostics[0]
            raise QiShuGenerationError(
                "UPSTREAM_R2_INTEGRITY_FAILED",
                f"{first.code}:{first.path}:{first.detail}",
            )
        if (
            r2_state.profile.profile_id != profile.upstream_r2_profile_id
            or r2_state.profile.profile_version != profile.upstream_r2_profile_version
        ):
            raise QiShuGenerationError(
                "UPSTREAM_R2_PROFILE_MISMATCH",
                "R2 state profile does not match the R6 profile binding",
            )
        if time_layer != profile.supported_time_layer:
            raise QiShuGenerationError(
                "UNSUPPORTED_QISHU_TIME_LAYER",
                f"expected {profile.supported_time_layer}, got {time_layer}",
            )
        try:
            facts = project_qishu_positions(r2_state)
        except QiShuProjectionError as exc:
            raise QiShuGenerationError(exc.diagnostic_code, str(exc)) from exc
        report = validate_qishu_components(r2_state, profile, time_layer, facts)
        if report.status != "PASS":
            self._raise_report(report)
        hashes = qishu_hash_bundle(
            r2_state.hashes.fact_hash,
            r2_state.hashes.computation_hash,
            profile,
            time_layer,
            facts,
        )
        state = QiShuPositionState(
            upstream_r2_fact_hash=r2_state.hashes.fact_hash,
            upstream_r2_computation_hash=r2_state.hashes.computation_hash,
            profile=profile,
            time_layer=time_layer,
            qishu_facts=facts,
            integrity=report,
            hashes=hashes,
        )
        final_report = validate_qishu_state(r2_state, state)
        if final_report.status != "PASS":
            self._raise_report(final_report)
        return state

    def generate_from_candidate(
        self,
        candidate: "ZiweiChartCandidate",
        structural_state: StructuralState,
        r2_state: RelativePalaceFrameState,
        profile: ResolvedQiShuPositionProfile,
        *,
        time_layer: str = "NATAL",
    ) -> QiShuPositionState:
        if candidate.integrity.status != "PASS":
            raise QiShuGenerationError(
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
