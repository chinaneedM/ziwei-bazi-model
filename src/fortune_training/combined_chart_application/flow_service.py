from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from fortune_training.bazi_application import (
    BaziApplicationFlowRequest,
    BaziApplicationFlowResolution,
    BaziApplicationFlowService,
    BaziApplicationRequest,
    validate_application_flow_full_replay,
    validate_application_flow_resolution,
)
from fortune_training.bazi_temporal import BaziSex

from .flow_integrity import (
    combined_target_flow_bundle_hash,
    combined_target_flow_source_fact_hash,
    combined_target_flow_view_hash,
    validate_combined_target_flow_resolution,
)
from .flow_models import (
    COMBINED_TARGET_FLOW_SCHEMA,
    CombinedTargetFlowIntegrityReport,
    CombinedTargetFlowRequest,
    CombinedTargetFlowResolution,
)
from .models import CombinedChartApplicationResolution
from .service import CombinedChartService, validate_combined_resolution


class CombinedTargetFlowResolutionError(ValueError):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


class CombinedTargetFlowService:
    schema = COMBINED_TARGET_FLOW_SCHEMA

    def __init__(
        self,
        base_service: CombinedChartService,
        bazi_flow_service: BaziApplicationFlowService | None = None,
    ) -> None:
        self.base_service = base_service
        self.bazi_flow_service = bazi_flow_service or BaziApplicationFlowService(
            base_service.bazi_service
        )

    @classmethod
    def from_repository(cls, repository_root: Path) -> "CombinedTargetFlowService":
        return cls(CombinedChartService.from_repository(repository_root))

    def _resolve_triplet(
        self,
        request: CombinedTargetFlowRequest,
    ) -> tuple[
        CombinedChartApplicationResolution,
        BaziApplicationFlowResolution,
        CombinedTargetFlowResolution,
    ]:
        target_profile = request.target_coordinate_profile.validate()
        base = self.base_service.resolve(request.combined_request)
        base_report = validate_combined_resolution(base)
        if base_report.status != "PASS" or base_report != base.integrity:
            raise CombinedTargetFlowResolutionError(
                "COMBINED_TARGET_FLOW_BASE_REPLAY_FAILED",
                ";".join(base_report.diagnostics) or base_report.status,
            )
        if base.ziwei_bundle is None or base.bazi_bundle is None:
            detail = ":".join(
                (
                    base.status,
                    base.ziwei_error.code if base.ziwei_error is not None else "ZIWEI_OK",
                    base.bazi_error.code if base.bazi_error is not None else "BAZI_OK",
                )
            )
            raise CombinedTargetFlowResolutionError(
                "COMBINED_TARGET_FLOW_REQUIRES_BOTH_BASE_BUNDLES",
                detail,
            )

        bazi_request = BaziApplicationRequest(
            birth=base.birth,
            sex=BaziSex(base.sex),
            natal_profile=base.bazi_natal_profile,
            temporal_profile=base.bazi_temporal_profile,
            application_profile=base.bazi_application_profile,
            dayun_count=base.bazi_bundle.dayun_count,
        )
        bazi_flow_request = BaziApplicationFlowRequest(
            application_request=bazi_request,
            target_input=request.target_input,
            target_coordinate_profile=target_profile,
        )
        bazi_base, bazi_flow = self.bazi_flow_service.resolve_with_base(
            bazi_flow_request
        )

        if bazi_base != base.bazi_bundle:
            raise CombinedTargetFlowResolutionError(
                "COMBINED_TARGET_FLOW_BAZI_BASE_OBJECT_MISMATCH",
                f"combined={base.bazi_bundle.bundle_hash};flow={bazi_base.bundle_hash}",
            )
        if bazi_flow.base_application_bundle_hash != base.bazi_bundle.bundle_hash:
            raise CombinedTargetFlowResolutionError(
                "COMBINED_TARGET_FLOW_BAZI_BASE_HASH_MISMATCH",
                (
                    f"combined={base.bazi_bundle.bundle_hash};"
                    f"flow={bazi_flow.base_application_bundle_hash}"
                ),
            )

        structural = validate_application_flow_resolution(bazi_flow)
        if structural.status != "PASS" or structural != bazi_flow.integrity:
            raise CombinedTargetFlowResolutionError(
                "COMBINED_TARGET_FLOW_BAZI_FLOW_INTEGRITY_FAILED",
                ";".join(structural.diagnostics) or structural.status,
            )
        full_replay = validate_application_flow_full_replay(
            self.bazi_flow_service,
            bazi_flow_request,
            bazi_flow,
        )
        if full_replay.status != "PASS":
            raise CombinedTargetFlowResolutionError(
                "COMBINED_TARGET_FLOW_BAZI_FLOW_FULL_REPLAY_FAILED",
                ";".join(full_replay.diagnostics),
            )
        if bazi_flow.target_input != request.target_input:
            raise CombinedTargetFlowResolutionError(
                "COMBINED_TARGET_FLOW_TARGET_INPUT_MISMATCH",
                "released Bazi target-flow target input differs from combined request",
            )
        if (
            bazi_flow.target_coordinate_profile_id != target_profile.profile_id
            or bazi_flow.target_coordinate_profile_version != target_profile.profile_version
        ):
            raise CombinedTargetFlowResolutionError(
                "COMBINED_TARGET_FLOW_TARGET_PROFILE_MISMATCH",
                (
                    f"{bazi_flow.target_coordinate_profile_id}:"
                    f"{bazi_flow.target_coordinate_profile_version}"
                ),
            )

        ziwei = base.ziwei_bundle
        expected_status = (
            "RESOLVED"
            if base.status == "RESOLVED_BOTH"
            and ziwei.resolution_status == "RESOLVED"
            and bazi_flow.status == "RESOLVED"
            else "UNCERTAINTY_PRESENT"
        )
        provisional = CombinedTargetFlowResolution(
            schema=self.schema,
            status=expected_status,
            combined_profile_id=base.combined_profile.profile_id,
            combined_profile_version=base.combined_profile.profile_version,
            composition_semantics=base.combined_profile.composition_semantics,
            base_combined_status=base.status,
            base_combined_manifest_hash=base.manifest_hash,
            ziwei_bundle_hash=ziwei.bundle_hash,
            ziwei_resolution_status=ziwei.resolution_status,
            ziwei_selected_daxian_frame_id=ziwei.selected_daxian_frame_id,
            ziwei_selected_annual_year=ziwei.selected_annual_year,
            ziwei_selected_minor_limit_age=ziwei.selected_minor_limit_age,
            bazi_base_bundle_hash=base.bazi_bundle.bundle_hash,
            bazi_dayun_count=base.bazi_bundle.dayun_count,
            bazi_target_flow_status=bazi_flow.status,
            bazi_target_flow_source_fact_hash=bazi_flow.source_fact_hash,
            bazi_target_flow_view_hash=bazi_flow.view_hash,
            bazi_target_flow_bundle_hash=bazi_flow.bundle_hash,
            target_coordinate_fact_hash=bazi_flow.target_coordinate_fact_hash,
            target_coordinate_computation_hash=(
                bazi_flow.target_coordinate_computation_hash
            ),
            target_coordinate_profile_id=target_profile.profile_id,
            target_coordinate_profile_version=target_profile.profile_version,
            target_input=request.target_input,
            source_fact_hash="",
            view_hash="",
            bundle_hash="",
            integrity=CombinedTargetFlowIntegrityReport(
                status="PENDING", diagnostics=()
            ),
        )
        provisional = replace(
            provisional,
            source_fact_hash=combined_target_flow_source_fact_hash(provisional),
        )
        provisional = replace(
            provisional,
            view_hash=combined_target_flow_view_hash(provisional),
        )
        provisional = replace(
            provisional,
            bundle_hash=combined_target_flow_bundle_hash(provisional),
        )
        report = validate_combined_target_flow_resolution(provisional)
        if report.status != "PASS":
            raise CombinedTargetFlowResolutionError(
                "COMBINED_TARGET_FLOW_BINDING_INTEGRITY_FAILED",
                ";".join(report.diagnostics),
            )
        return base, bazi_flow, replace(provisional, integrity=report)

    def resolve(self, request: CombinedTargetFlowRequest) -> CombinedTargetFlowResolution:
        return self._resolve_triplet(request)[2]

    def resolve_with_bundles(
        self,
        request: CombinedTargetFlowRequest,
    ) -> tuple[
        CombinedChartApplicationResolution,
        BaziApplicationFlowResolution,
        CombinedTargetFlowResolution,
    ]:
        return self._resolve_triplet(request)
