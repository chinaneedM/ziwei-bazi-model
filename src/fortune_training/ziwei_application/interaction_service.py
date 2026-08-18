from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from .interaction_integrity import (
    sanhe_interaction_bundle_hash,
    sanhe_interaction_source_fact_hash,
    sanhe_interaction_view_hash,
    validate_sanhe_interaction_resolution,
)
from .interaction_models import (
    SANHE_INTERACTION_MODE,
    SANHE_INTERACTION_SCHEMA,
    SanheInteractionIntegrityReport,
    SanheInteractionRequest,
    SanheInteractionResolution,
)
from .models import ApplicationChartBundle
from .service import ZiweiChartService, validate_application_bundle


class SanheInteractionResolutionError(ValueError):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


class ZiweiSanheInteractionService:
    schema = SANHE_INTERACTION_SCHEMA

    def __init__(self, base_service: ZiweiChartService) -> None:
        self.base_service = base_service

    @classmethod
    def from_repository(cls, repository_root: Path) -> "ZiweiSanheInteractionService":
        return cls(ZiweiChartService.from_repository(repository_root))

    @staticmethod
    def _select_origin(bundle: ApplicationChartBundle, origin_designation_id: str):
        r2_rows = tuple(
            row
            for row in bundle.r2_state.frame_facts
            if row.origin_designation_id == origin_designation_id
        )
        if len(r2_rows) != 12:
            raise SanheInteractionResolutionError(
                "SANHE_INTERACTION_R2_ORIGIN_NOT_UNIQUE",
                f"origin={origin_designation_id};rows={len(r2_rows)}",
            )
        origin_addresses = {row.origin_address for row in r2_rows}
        if len(origin_addresses) != 1:
            raise SanheInteractionResolutionError(
                "SANHE_INTERACTION_R2_ORIGIN_ADDRESS_NOT_UNIQUE",
                f"origin={origin_designation_id};addresses={len(origin_addresses)}",
            )
        origin_address = next(iter(origin_addresses))

        r4_frames = tuple(
            row
            for row in bundle.r4_state.sanfang_sizheng_frames
            if row.origin_designation_id == origin_designation_id
        )
        if len(r4_frames) != 1:
            raise SanheInteractionResolutionError(
                "SANHE_INTERACTION_R4_ORIGIN_NOT_UNIQUE",
                f"origin={origin_designation_id};frames={len(r4_frames)}",
            )
        if r4_frames[0].origin_address != origin_address:
            raise SanheInteractionResolutionError(
                "SANHE_INTERACTION_R2_R4_ORIGIN_ADDRESS_MISMATCH",
                origin_designation_id,
            )

        r5_frames = tuple(
            row
            for row in bundle.r5_state.frames
            if row.origin_designation_id == origin_designation_id
        )
        if len(r5_frames) != 1:
            raise SanheInteractionResolutionError(
                "SANHE_INTERACTION_R5_ORIGIN_NOT_UNIQUE",
                f"origin={origin_designation_id};frames={len(r5_frames)}",
            )
        if r5_frames[0].origin_address != origin_address:
            raise SanheInteractionResolutionError(
                "SANHE_INTERACTION_R2_R5_ORIGIN_ADDRESS_MISMATCH",
                origin_designation_id,
            )
        return origin_address, r2_rows, r5_frames[0]

    def _resolve_pair(
        self,
        request: SanheInteractionRequest,
    ) -> tuple[ApplicationChartBundle, SanheInteractionResolution]:
        try:
            bundle = self.base_service.resolve(request.application_request)
            validate_application_bundle(bundle)
        except ValueError as exc:
            code = getattr(exc, "diagnostic_code", None) or "SANHE_INTERACTION_APPLICATION_FAILED"
            raise SanheInteractionResolutionError(str(code), str(exc)) from exc

        origin_address, r2_rows, r5_frame = self._select_origin(
            bundle,
            request.origin_designation_id,
        )
        provisional = SanheInteractionResolution(
            schema=self.schema,
            status="RESOLVED",
            interaction_mode=SANHE_INTERACTION_MODE,
            source_application_bundle_hash=bundle.bundle_hash,
            source_application_resolution_status=bundle.resolution_status,
            selected_daxian_frame_id=bundle.selected_daxian_frame_id,
            selected_annual_year=bundle.selected_annual_year,
            selected_minor_limit_age=bundle.selected_minor_limit_age,
            selected_origin_designation_id=request.origin_designation_id,
            selected_origin_address=origin_address,
            relative_roles=r2_rows,
            sanfang_sizheng_frame=r5_frame,
            r2_fact_hash=bundle.r2_state.hashes.fact_hash,
            r2_computation_hash=bundle.r2_state.hashes.computation_hash,
            r3_fact_hash=bundle.r3_state.hashes.fact_hash,
            r3_computation_hash=bundle.r3_state.hashes.computation_hash,
            r4_fact_hash=bundle.r4_state.hashes.fact_hash,
            r4_computation_hash=bundle.r4_state.hashes.computation_hash,
            r5_fact_hash=bundle.r5_state.hashes.fact_hash,
            r5_computation_hash=bundle.r5_state.hashes.computation_hash,
            source_fact_hash="",
            view_hash="",
            bundle_hash="",
            integrity=SanheInteractionIntegrityReport(status="PENDING", diagnostics=()),
        )
        provisional = replace(
            provisional,
            source_fact_hash=sanhe_interaction_source_fact_hash(provisional),
        )
        provisional = replace(
            provisional,
            view_hash=sanhe_interaction_view_hash(provisional),
        )
        provisional = replace(
            provisional,
            bundle_hash=sanhe_interaction_bundle_hash(provisional),
        )
        report = validate_sanhe_interaction_resolution(bundle, provisional)
        if report.status != "PASS":
            raise SanheInteractionResolutionError(
                "SANHE_INTERACTION_INTEGRITY_FAILED",
                ";".join(report.diagnostics),
            )
        return bundle, replace(provisional, integrity=report)

    def resolve(self, request: SanheInteractionRequest) -> SanheInteractionResolution:
        return self._resolve_pair(request)[1]

    def resolve_with_bundle(
        self,
        request: SanheInteractionRequest,
    ) -> tuple[ApplicationChartBundle, SanheInteractionResolution]:
        return self._resolve_pair(request)
