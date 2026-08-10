from __future__ import annotations

from fortune_training.ziwei_structural.r2 import (
    RELATIVE_FRAME_INTEGRITY_ALGORITHM_ID,
    RELATIVE_FRAME_INTEGRITY_ALGORITHM_VERSION,
    relative_frame_hash_bundle,
)
from fortune_training.ziwei_structural.r2.models import RelativePalaceFrameState

from .integrity import (
    named_semantic_hash_bundle,
    validate_named_semantic_components,
    validate_named_semantic_state,
)
from .models import NamedSemanticIntegrityReport, NamedStructuralSemanticState
from .profile import ResolvedNamedStructuralSemanticProfile
from .semantics import NamedStructuralSemanticCompiler, NamedStructuralSemanticError


class NamedSemanticGenerationError(ValueError):
    def __init__(
        self,
        diagnostic_code: str,
        detail: str,
        *,
        report: NamedSemanticIntegrityReport | None = None,
    ) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code
        self.report = report


class ZiweiNamedStructuralSemanticRuntime:
    """Structural Runtime V2-R4 named Sanfang/Sizheng compiler over R2."""

    def __init__(self) -> None:
        self.compiler = NamedStructuralSemanticCompiler()

    @staticmethod
    def _raise_report(report: NamedSemanticIntegrityReport) -> None:
        first = report.diagnostics[0]
        raise NamedSemanticGenerationError(first.code, first.detail, report=report)

    @staticmethod
    def _validate_upstream_r2_self_consistency(frame_state: RelativePalaceFrameState) -> None:
        try:
            frame_state.profile.validate()
        except ValueError as exc:
            raise NamedSemanticGenerationError(
                "UPSTREAM_R2_PROFILE_INVALID",
                str(exc),
            ) from exc

        if frame_state.integrity.status != "PASS":
            raise NamedSemanticGenerationError(
                "UPSTREAM_R2_INTEGRITY_FAILED",
                "R2 RelativePalaceFrameState must carry PASS integrity",
            )
        if (
            frame_state.integrity.algorithm_id != RELATIVE_FRAME_INTEGRITY_ALGORITHM_ID
            or frame_state.integrity.algorithm_version != RELATIVE_FRAME_INTEGRITY_ALGORITHM_VERSION
        ):
            raise NamedSemanticGenerationError(
                "UPSTREAM_R2_INTEGRITY_LINEAGE_MISMATCH",
                "R2 integrity algorithm identity does not match the frozen R2 release",
            )

        expected_hashes = relative_frame_hash_bundle(
            frame_state.upstream_structural_fact_hash,
            frame_state.upstream_structural_computation_hash,
            frame_state.profile,
            frame_state.frame_facts,
        )
        if frame_state.hashes != expected_hashes:
            raise NamedSemanticGenerationError(
                "UPSTREAM_R2_HASH_MISMATCH",
                "R2 frame facts/profile/upstream lineage do not reproduce the stored R2 hashes",
            )

    def generate(
        self,
        frame_state: RelativePalaceFrameState,
        profile: ResolvedNamedStructuralSemanticProfile,
    ) -> NamedStructuralSemanticState:
        try:
            profile.validate()
        except ValueError as exc:
            raise NamedSemanticGenerationError("INVALID_R4_PROFILE", str(exc)) from exc

        self._validate_upstream_r2_self_consistency(frame_state)

        if (
            frame_state.profile.profile_id != profile.upstream_r2_profile_id
            or frame_state.profile.profile_version != profile.upstream_r2_profile_version
        ):
            raise NamedSemanticGenerationError(
                "UPSTREAM_R2_PROFILE_MISMATCH",
                "R2 profile does not match the R4 profile binding",
            )
        if frame_state.profile.semantic_rule_set_id is not None:
            raise NamedSemanticGenerationError(
                "R2_SEMANTIC_LAYER_MUTATED",
                "R2 must remain interpretation-free; R4 owns named semantics",
            )

        try:
            opposition_axes, trine_groups, frames = self.compiler.compile(frame_state)
        except NamedStructuralSemanticError as exc:
            raise NamedSemanticGenerationError(exc.diagnostic_code, str(exc)) from exc

        report = validate_named_semantic_components(
            frame_state,
            profile,
            opposition_axes,
            trine_groups,
            frames,
        )
        if report.status != "PASS":
            self._raise_report(report)

        hashes = named_semantic_hash_bundle(
            frame_state.hashes.fact_hash,
            frame_state.hashes.computation_hash,
            profile,
            opposition_axes,
            trine_groups,
            frames,
        )
        state = NamedStructuralSemanticState(
            upstream_r2_fact_hash=frame_state.hashes.fact_hash,
            upstream_r2_computation_hash=frame_state.hashes.computation_hash,
            profile=profile,
            opposition_axes=opposition_axes,
            trine_groups=trine_groups,
            sanfang_sizheng_frames=frames,
            integrity=report,
            hashes=hashes,
        )
        final_report = validate_named_semantic_state(frame_state, state)
        if final_report.status != "PASS":
            self._raise_report(final_report)
        return state
