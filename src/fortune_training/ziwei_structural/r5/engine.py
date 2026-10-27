from __future__ import annotations

from fortune_training.ziwei_structural.r3.models import BorrowProjectionState
from fortune_training.ziwei_structural.r4.models import NamedStructuralSemanticState

from .composition import ResolvedStructuralComposer, ResolvedStructuralCompositionError
from .integrity import (
    resolved_structural_hash_bundle,
    validate_resolved_structural_components,
    validate_resolved_structural_state,
)
from .models import ResolvedSanfangSizhengViewState, ResolvedStructuralIntegrityReport
from .profile import ResolvedStructuralCompositionProfile


class ResolvedStructuralGenerationError(ValueError):
    def __init__(
        self,
        diagnostic_code: str,
        detail: str,
        *,
        report: ResolvedStructuralIntegrityReport | None = None,
    ) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code
        self.report = report


class ZiweiResolvedStructuralRuntime:
    """V2-R5 composition of validated R3 borrow resolution and R4 named semantics."""

    def __init__(self) -> None:
        self.composer = ResolvedStructuralComposer()

    @staticmethod
    def _raise_report(report: ResolvedStructuralIntegrityReport) -> None:
        first = report.diagnostics[0]
        raise ResolvedStructuralGenerationError(first.code, first.detail, report=report)

    def generate(
        self,
        r3_state: BorrowProjectionState,
        r4_state: NamedStructuralSemanticState,
        profile: ResolvedStructuralCompositionProfile,
        *,
        time_layer: str = "NATAL",
    ) -> ResolvedSanfangSizhengViewState:
        try:
            profile.validate()
        except ValueError as exc:
            raise ResolvedStructuralGenerationError("INVALID_R5_PROFILE", str(exc)) from exc

        if time_layer != "NATAL" or time_layer != profile.supported_time_layer:
            raise ResolvedStructuralGenerationError(
                "UNSUPPORTED_R5_TIME_LAYER",
                f"R5 currently supports NATAL only, got {time_layer}",
            )
        if r3_state.time_layer != time_layer:
            raise ResolvedStructuralGenerationError(
                "R3_R5_TIME_LAYER_MISMATCH",
                "R5 time layer must equal the supplied R3 time layer",
            )

        preflight = validate_resolved_structural_components(
            r3_state,
            r4_state,
            profile,
            time_layer,
            (),
        )
        preflight_codes = {row.code for row in preflight.diagnostics}
        ignorable_preflight_codes = {
            "INVALID_RESOLVED_FRAME_COUNT",
            "NONCANONICAL_RESOLVED_FRAME_ORDER",
        }
        blocking = tuple(
            row for row in preflight.diagnostics if row.code not in ignorable_preflight_codes
        )
        if blocking:
            report = ResolvedStructuralIntegrityReport(
                status="FAIL",
                diagnostics=blocking,
                algorithm_id=preflight.algorithm_id,
                algorithm_version=preflight.algorithm_version,
            )
            self._raise_report(report)
        if preflight_codes - ignorable_preflight_codes:
            self._raise_report(preflight)

        try:
            frames = self.composer.compose(r3_state, r4_state)
        except ResolvedStructuralCompositionError as exc:
            raise ResolvedStructuralGenerationError(exc.diagnostic_code, str(exc)) from exc

        report = validate_resolved_structural_components(
            r3_state,
            r4_state,
            profile,
            time_layer,
            frames,
        )
        if report.status != "PASS":
            self._raise_report(report)

        hashes = resolved_structural_hash_bundle(
            r3_state.hashes.fact_hash,
            r3_state.hashes.computation_hash,
            r4_state.hashes.fact_hash,
            r4_state.hashes.computation_hash,
            profile,
            time_layer,
            frames,
        )
        state = ResolvedSanfangSizhengViewState(
            upstream_r3_fact_hash=r3_state.hashes.fact_hash,
            upstream_r3_computation_hash=r3_state.hashes.computation_hash,
            upstream_r4_fact_hash=r4_state.hashes.fact_hash,
            upstream_r4_computation_hash=r4_state.hashes.computation_hash,
            profile=profile,
            time_layer=time_layer,
            frames=frames,
            integrity=report,
            hashes=hashes,
        )
        final_report = validate_resolved_structural_state(r3_state, r4_state, state)
        if final_report.status != "PASS":
            self._raise_report(final_report)
        return state
