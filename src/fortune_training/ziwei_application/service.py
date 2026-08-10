from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256
from fortune_training.ziwei_chart import (
    PlainTextZiweiRenderer,
    ZiweiChartFoundation,
    ZiweiChartRequest,
    ZiweiTemporalEngine,
    ZiweiViewProjectionCompiler,
    temporal_hash_bundle,
    validate_temporal_state,
)
from fortune_training.ziwei_structural import (
    ZiweiStructuralRuntime,
    validate_structural_state,
    ziwei_structural_v2_r1_profile,
)
from fortune_training.ziwei_structural.r2 import (
    ZiweiRelativePalaceFrameRuntime,
    validate_relative_frame_state,
    ziwei_structural_v2_r2_profile,
)
from fortune_training.ziwei_structural.r3 import (
    ZiweiBorrowProjectionRuntime,
    validate_borrow_projection_state,
    ziwei_structural_v2_r3_profile,
)
from fortune_training.ziwei_structural.r4 import (
    ZiweiNamedStructuralSemanticRuntime,
    validate_named_semantic_state,
    ziwei_structural_v2_r4_profile,
)
from fortune_training.ziwei_structural.r5 import (
    ZiweiResolvedStructuralRuntime,
    validate_resolved_structural_state,
    ziwei_structural_v2_r5_profile,
)

from .models import (
    APPLICATION_CHART_BUNDLE_SCHEMA,
    ApplicationBirthRequest,
    ApplicationChartBundle,
)
from .profile import ZiweiApplicationProfile, ziwei_application_v1_profile


APPLICATION_EXPORT_SCHEMA = "ZIWEI-APPLICATION-CHART-EXPORT-V1"


class ApplicationResolutionError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


def _hash_ref(hashes) -> dict[str, str]:
    return {
        "fact_hash": hashes.fact_hash,
        "computation_hash": hashes.computation_hash,
    }


def _state_refs(
    candidate,
    temporal_hashes,
    r1_state,
    r2_state,
    r3_state,
    r4_state,
    r5_state,
) -> dict[str, dict[str, str]]:
    return {
        "natal": _hash_ref(candidate.hashes),
        "temporal": _hash_ref(temporal_hashes),
        "r1": _hash_ref(r1_state.hashes),
        "r2": _hash_ref(r2_state.hashes),
        "r3": _hash_ref(r3_state.hashes),
        "r4": _hash_ref(r4_state.hashes),
        "r5": _hash_ref(r5_state.hashes),
    }


def application_bundle_hash(
    application_profile: ZiweiApplicationProfile,
    resolution_status: str,
    candidate,
    temporal_hashes,
    r1_state,
    r2_state,
    r3_state,
    r4_state,
    r5_state,
    view_model,
    *,
    selected_daxian_frame_id: str | None,
    selected_annual_year: int | None,
    selected_minor_limit_age: int | None,
) -> str:
    return object_sha256(
        {
            "application_profile": json_value(application_profile),
            "bundle_schema": APPLICATION_CHART_BUNDLE_SCHEMA,
            "resolution_status": resolution_status,
            "candidate_branch_indices": list(candidate.branch_indices),
            "state_refs": _state_refs(
                candidate,
                temporal_hashes,
                r1_state,
                r2_state,
                r3_state,
                r4_state,
                r5_state,
            ),
            "selection": {
                "daxian_frame_id": selected_daxian_frame_id,
                "annual_year": selected_annual_year,
                "minor_limit_age": selected_minor_limit_age,
            },
            "view_hash": view_model.view_hash,
            "hash_algorithm": (
                f"{application_profile.bundle_hash_algorithm_id}@"
                f"{application_profile.bundle_hash_algorithm_version}"
            ),
        }
    )


def application_export(bundle: ApplicationChartBundle) -> dict[str, Any]:
    validate_application_bundle(bundle)
    return {
        "schema": APPLICATION_EXPORT_SCHEMA,
        "bundle_schema": bundle.schema,
        "application_profile": json_value(bundle.application_profile),
        "resolution_status": bundle.resolution_status,
        "candidate_branch_indices": list(bundle.candidate.branch_indices),
        "selection": {
            "daxian_frame_id": bundle.selected_daxian_frame_id,
            "annual_year": bundle.selected_annual_year,
            "minor_limit_age": bundle.selected_minor_limit_age,
        },
        "state_refs": _state_refs(
            bundle.candidate,
            bundle.temporal_hashes,
            bundle.r1_state,
            bundle.r2_state,
            bundle.r3_state,
            bundle.r4_state,
            bundle.r5_state,
        ),
        "view_hash": bundle.view_model.view_hash,
        "bundle_hash": bundle.bundle_hash,
        "view_model": json_value(bundle.view_model),
    }


def _require_pass(report, diagnostic_code: str) -> None:
    if report.status != "PASS":
        detail = report.diagnostics[0].detail if report.diagnostics else "integrity status is not PASS"
        raise ApplicationResolutionError(diagnostic_code, detail)


def validate_application_bundle(bundle: ApplicationChartBundle) -> None:
    if bundle.schema != APPLICATION_CHART_BUNDLE_SCHEMA:
        raise ApplicationResolutionError("APPLICATION_BUNDLE_SCHEMA_MISMATCH", bundle.schema)
    try:
        bundle.application_profile.validate()
        bundle.presentation_profile.validate()
    except ValueError as exc:
        raise ApplicationResolutionError("APPLICATION_PROFILE_INVALID", str(exc)) from exc
    if bundle.candidate.integrity.status != "PASS":
        raise ApplicationResolutionError(
            "APPLICATION_NATAL_INTEGRITY_FAILED",
            "candidate must carry PASS natal integrity",
        )

    _require_pass(
        validate_temporal_state(bundle.temporal_state, bundle.temporal_context),
        "APPLICATION_TEMPORAL_INTEGRITY_FAILED",
    )
    expected_temporal_hashes = temporal_hash_bundle(
        bundle.temporal_state,
        bundle.calculation_profile,
    )
    if bundle.temporal_hashes != expected_temporal_hashes:
        raise ApplicationResolutionError(
            "APPLICATION_TEMPORAL_HASH_MISMATCH",
            "temporal state/profile do not reproduce stored temporal hashes",
        )

    _require_pass(
        validate_structural_state(bundle.r1_state),
        "APPLICATION_R1_INTEGRITY_FAILED",
    )
    if (
        bundle.r1_state.upstream_natal_fact_hash != bundle.candidate.hashes.fact_hash
        or bundle.r1_state.upstream_natal_computation_hash
        != bundle.candidate.hashes.computation_hash
    ):
        raise ApplicationResolutionError(
            "APPLICATION_NATAL_R1_BINDING_MISMATCH",
            "R1 is not bound to the application candidate",
        )

    _require_pass(
        validate_relative_frame_state(
            bundle.candidate.chart,
            bundle.r1_state,
            bundle.r2_state,
        ),
        "APPLICATION_R2_INTEGRITY_FAILED",
    )
    _require_pass(
        validate_borrow_projection_state(
            bundle.candidate.chart,
            bundle.r1_state,
            bundle.r2_state,
            bundle.r3_state,
        ),
        "APPLICATION_R3_INTEGRITY_FAILED",
    )
    _require_pass(
        validate_named_semantic_state(bundle.r2_state, bundle.r4_state),
        "APPLICATION_R4_INTEGRITY_FAILED",
    )
    _require_pass(
        validate_resolved_structural_state(
            bundle.r3_state,
            bundle.r4_state,
            bundle.r5_state,
        ),
        "APPLICATION_R5_INTEGRITY_FAILED",
    )

    if (
        bundle.view_model.source_fact_hash != bundle.candidate.hashes.fact_hash
        or bundle.view_model.source_computation_hash
        != bundle.candidate.hashes.computation_hash
    ):
        raise ApplicationResolutionError(
            "APPLICATION_VIEW_NATAL_BINDING_MISMATCH",
            "ViewModel is not bound to the application candidate",
        )

    try:
        replay_view = ZiweiViewProjectionCompiler().compile(
            bundle.candidate.chart,
            bundle.candidate.hashes,
            bundle.presentation_profile,
            temporal_state=bundle.temporal_state,
            temporal_context=bundle.temporal_context,
            daxian_frame_id=bundle.selected_daxian_frame_id,
            annual_year=bundle.selected_annual_year,
            minor_limit_age=bundle.selected_minor_limit_age,
        )
    except ValueError as exc:
        raise ApplicationResolutionError("APPLICATION_VIEW_REPLAY_FAILED", str(exc)) from exc
    if replay_view != bundle.view_model:
        raise ApplicationResolutionError(
            "APPLICATION_VIEW_REPLAY_MISMATCH",
            "stored ViewModel does not reproduce from bundle inputs",
        )

    expected_bundle_hash = application_bundle_hash(
        bundle.application_profile,
        bundle.resolution_status,
        bundle.candidate,
        bundle.temporal_hashes,
        bundle.r1_state,
        bundle.r2_state,
        bundle.r3_state,
        bundle.r4_state,
        bundle.r5_state,
        bundle.view_model,
        selected_daxian_frame_id=bundle.selected_daxian_frame_id,
        selected_annual_year=bundle.selected_annual_year,
        selected_minor_limit_age=bundle.selected_minor_limit_age,
    )
    if bundle.bundle_hash != expected_bundle_hash:
        raise ApplicationResolutionError(
            "APPLICATION_BUNDLE_HASH_MISMATCH",
            "bundle references do not reproduce stored bundle hash",
        )


class ZiweiChartService:
    """Application V1 orchestration over the frozen Ziwei public runtime stack."""

    def __init__(
        self,
        chart_foundation: ZiweiChartFoundation,
        application_profile: ZiweiApplicationProfile | None = None,
    ) -> None:
        self.chart_foundation = chart_foundation
        self.application_profile = application_profile or ziwei_application_v1_profile()
        self.application_profile.validate()
        self.temporal = ZiweiTemporalEngine()
        self.r1 = ZiweiStructuralRuntime()
        self.r2 = ZiweiRelativePalaceFrameRuntime()
        self.r3 = ZiweiBorrowProjectionRuntime()
        self.r4 = ZiweiNamedStructuralSemanticRuntime()
        self.r5 = ZiweiResolvedStructuralRuntime()
        self.view = ZiweiViewProjectionCompiler()
        self.text = PlainTextZiweiRenderer()

    @classmethod
    def from_repository(cls, repository_root: Path) -> "ZiweiChartService":
        return cls(ZiweiChartFoundation.from_repository(repository_root))

    @staticmethod
    def _temporal_max_age(request: ApplicationBirthRequest, context) -> int:
        default_max = context.bureau_number + (request.daxian_count - 1) * 10 + 9
        required = 1
        if request.annual_year is not None:
            annual_age = request.annual_year - context.ziwei_birth_year + 1
            if annual_age < 1:
                raise ApplicationResolutionError(
                    "APPLICATION_ANNUAL_YEAR_PREDATES_BIRTH",
                    str(request.annual_year),
                )
            required = max(required, annual_age)
        if request.minor_limit_age is not None:
            required = max(required, request.minor_limit_age)
        if request.max_nominal_age is not None:
            if request.max_nominal_age < required:
                raise ApplicationResolutionError(
                    "APPLICATION_TEMPORAL_RANGE_TOO_SHORT",
                    f"required={required} configured={request.max_nominal_age}",
                )
            return request.max_nominal_age
        return max(default_max, required)

    @staticmethod
    def _stage_error(stage: str, exc: ValueError) -> ApplicationResolutionError:
        code = getattr(exc, "diagnostic_code", None) or f"APPLICATION_{stage}_FAILED"
        return ApplicationResolutionError(str(code), str(exc))

    def resolve(self, request: ApplicationBirthRequest) -> ApplicationChartBundle:
        try:
            typed = self.chart_foundation.resolve_typed(
                ZiweiChartRequest(
                    birth=request.birth,
                    sex=request.sex,
                    profile=request.calculation_profile,
                )
            )
        except ValueError as exc:
            raise self._stage_error("NATAL", exc) from exc

        if len(typed.candidates) != 1 or typed.status not in {
            "RESOLVED",
            "RESOLVED_SINGLE_CHART_WITH_TIME_UNCERTAINTY",
        }:
            raise ApplicationResolutionError(
                "APPLICATION_UNIQUE_NATAL_CANDIDATE_REQUIRED",
                f"status={typed.status} candidates={len(typed.candidates)} diagnostics={typed.diagnostics}",
            )
        candidate = typed.candidates[0]
        if candidate.integrity.status != "PASS":
            raise ApplicationResolutionError(
                "APPLICATION_NATAL_INTEGRITY_FAILED",
                "resolved candidate does not carry PASS integrity",
            )

        context = candidate.temporal_context()
        max_age = self._temporal_max_age(request, context)
        try:
            temporal_state = self.temporal.generate(
                context,
                typed.calculation_profile,
                daxian_count=request.daxian_count,
                max_nominal_age=max_age,
            )
            _require_pass(
                validate_temporal_state(temporal_state, context),
                "APPLICATION_TEMPORAL_INTEGRITY_FAILED",
            )
            temporal_hashes = temporal_hash_bundle(
                temporal_state,
                typed.calculation_profile,
            )

            r1_state = self.r1.generate_from_candidate(
                candidate,
                ziwei_structural_v2_r1_profile(),
            )
            r2_state = self.r2.generate_from_candidate(
                candidate,
                r1_state,
                ziwei_structural_v2_r2_profile(),
            )
            r3_state = self.r3.generate_from_candidate(
                candidate,
                r1_state,
                r2_state,
                ziwei_structural_v2_r3_profile(),
            )
            r4_state = self.r4.generate(
                r2_state,
                ziwei_structural_v2_r4_profile(),
            )
            r5_state = self.r5.generate(
                r3_state,
                r4_state,
                ziwei_structural_v2_r5_profile(),
            )
            view_model = self.view.compile(
                candidate.chart,
                candidate.hashes,
                request.presentation_profile,
                temporal_state=temporal_state,
                temporal_context=context,
                daxian_frame_id=request.daxian_frame_id,
                annual_year=request.annual_year,
                minor_limit_age=request.minor_limit_age,
            )
        except ValueError as exc:
            raise self._stage_error("ORCHESTRATION", exc) from exc

        bundle_hash = application_bundle_hash(
            self.application_profile,
            typed.status,
            candidate,
            temporal_hashes,
            r1_state,
            r2_state,
            r3_state,
            r4_state,
            r5_state,
            view_model,
            selected_daxian_frame_id=request.daxian_frame_id,
            selected_annual_year=request.annual_year,
            selected_minor_limit_age=request.minor_limit_age,
        )
        bundle = ApplicationChartBundle(
            application_profile=self.application_profile,
            resolution_status=typed.status,
            calculation_profile=typed.calculation_profile,
            presentation_profile=request.presentation_profile,
            selected_daxian_frame_id=request.daxian_frame_id,
            selected_annual_year=request.annual_year,
            selected_minor_limit_age=request.minor_limit_age,
            candidate=candidate,
            temporal_context=context,
            temporal_state=temporal_state,
            temporal_hashes=temporal_hashes,
            r1_state=r1_state,
            r2_state=r2_state,
            r3_state=r3_state,
            r4_state=r4_state,
            r5_state=r5_state,
            view_model=view_model,
            bundle_hash=bundle_hash,
        )
        validate_application_bundle(bundle)
        return bundle

    def render_plain_text(self, bundle: ApplicationChartBundle) -> str:
        validate_application_bundle(bundle)
        return self.text.render(bundle.view_model)

    def export(self, bundle: ApplicationChartBundle) -> dict[str, Any]:
        return application_export(bundle)
