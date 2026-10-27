from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from fortune_training.bazi_target_temporal import (
    TargetTemporalCoordinateFoundation,
    TargetTemporalCoordinateResolution,
    TargetTemporalInput,
    validate_target_temporal_resolution,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .flow_models import CombinedTargetFlowRequest
from .flow_service import CombinedTargetFlowResolutionError, CombinedTargetFlowService
from .shared_time_integrity import validate_shared_ziwei_selector_projection
from .shared_time_models import SharedZiweiSelectorProjectionResolution
from .shared_time_replay import validate_shared_ziwei_selector_full_replay
from .shared_time_service import SharedZiweiSelectorProjectionService


COMBINED_TARGET_FLOW_FUSION_R2_SCHEMA = (
    "ZIWEI-BAZI-COMBINED-TARGET-FLOW-FUSION-RESOLUTION-R2"
)
COMBINED_TARGET_FLOW_FUSION_R2_ALGORITHM_ID = (
    "ZIWEI-BAZI-COMBINED-TARGET-FLOW-FUSION-COMPOSER-R2"
)
COMBINED_TARGET_FLOW_FUSION_R2_ALGORITHM_VERSION = "1.0.0"
COMBINED_TARGET_FLOW_FUSION_R2_INTEGRITY_ALGORITHM_ID = (
    "ZIWEI-BAZI-COMBINED-TARGET-FLOW-FUSION-INTEGRITY-R2"
)
COMBINED_TARGET_FLOW_FUSION_R2_INTEGRITY_ALGORITHM_VERSION = "1.0.0"


@dataclass(frozen=True)
class CombinedTargetFlowFusionR2IntegrityReport:
    status: str
    diagnostics: tuple[str, ...]
    algorithm_id: str = COMBINED_TARGET_FLOW_FUSION_R2_INTEGRITY_ALGORITHM_ID
    algorithm_version: str = COMBINED_TARGET_FLOW_FUSION_R2_INTEGRITY_ALGORITHM_VERSION


@dataclass(frozen=True)
class CombinedTargetFlowFusionR2Resolution:
    schema: str
    status: str
    composition_semantics: str
    base_combined_manifest_hash: str
    r1_target_flow_bundle_hash: str
    target_coordinate_status: str
    target_coordinate_fact_hash: str
    target_coordinate_computation_hash: str
    target_coordinate_profile_id: str
    target_coordinate_profile_version: str
    target_input: TargetTemporalInput
    bazi_target_flow_status: str
    bazi_target_flow_source_fact_hash: str
    bazi_target_flow_view_hash: str
    bazi_target_flow_bundle_hash: str
    ziwei_selector_status: str
    ziwei_selector_candidate_count: int
    ziwei_selector_fact_hash: str
    ziwei_selector_computation_hash: str
    source_fact_hash: str
    view_hash: str
    bundle_hash: str
    integrity: CombinedTargetFlowFusionR2IntegrityReport


class CombinedTargetFlowFusionR2ResolutionError(ValueError):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


def combined_target_flow_fusion_r2_source_fact_hash(
    resolution: CombinedTargetFlowFusionR2Resolution,
) -> str:
    return object_sha256(
        {
            "base_combined_manifest_hash": resolution.base_combined_manifest_hash,
            "r1_target_flow_bundle_hash": resolution.r1_target_flow_bundle_hash,
            "target_coordinate_fact_hash": resolution.target_coordinate_fact_hash,
            "bazi_target_flow_source_fact_hash": resolution.bazi_target_flow_source_fact_hash,
            "ziwei_selector_fact_hash": resolution.ziwei_selector_fact_hash,
        }
    )


def combined_target_flow_fusion_r2_view_hash(
    resolution: CombinedTargetFlowFusionR2Resolution,
) -> str:
    return object_sha256(
        {
            "composition_semantics": resolution.composition_semantics,
            "target_input": json_value(resolution.target_input),
            "target_coordinate_status": resolution.target_coordinate_status,
            "bazi_target_flow_status": resolution.bazi_target_flow_status,
            "bazi_target_flow_view_hash": resolution.bazi_target_flow_view_hash,
            "ziwei_selector_status": resolution.ziwei_selector_status,
            "ziwei_selector_candidate_count": resolution.ziwei_selector_candidate_count,
        }
    )


def combined_target_flow_fusion_r2_bundle_hash(
    resolution: CombinedTargetFlowFusionR2Resolution,
) -> str:
    return object_sha256(
        {
            "schema": resolution.schema,
            "status": resolution.status,
            "source_fact_hash": resolution.source_fact_hash,
            "view_hash": resolution.view_hash,
            "target_coordinate_computation_hash": resolution.target_coordinate_computation_hash,
            "target_coordinate_profile": [
                resolution.target_coordinate_profile_id,
                resolution.target_coordinate_profile_version,
            ],
            "bazi_target_flow_bundle_hash": resolution.bazi_target_flow_bundle_hash,
            "ziwei_selector_computation_hash": resolution.ziwei_selector_computation_hash,
            "algorithm_id": COMBINED_TARGET_FLOW_FUSION_R2_ALGORITHM_ID,
            "algorithm_version": COMBINED_TARGET_FLOW_FUSION_R2_ALGORITHM_VERSION,
        }
    )


def _expected_status(resolution: CombinedTargetFlowFusionR2Resolution) -> str:
    if (
        resolution.target_coordinate_status == "RESOLVED"
        and resolution.bazi_target_flow_status == "RESOLVED"
        and resolution.ziwei_selector_status == "RESOLVED"
        and resolution.ziwei_selector_candidate_count == 1
    ):
        return "RESOLVED"
    return "UNCERTAINTY_PRESENT"


def validate_combined_target_flow_fusion_r2_resolution(
    resolution: CombinedTargetFlowFusionR2Resolution,
) -> CombinedTargetFlowFusionR2IntegrityReport:
    diagnostics: list[str] = []

    if resolution.schema != COMBINED_TARGET_FLOW_FUSION_R2_SCHEMA:
        diagnostics.append("RESOLUTION_SCHEMA_MISMATCH")
    if resolution.composition_semantics != "INDEPENDENT_BUNDLE_IDENTITY_COMPOSITION_ONLY":
        diagnostics.append("COMPOSITION_SEMANTICS_MISMATCH")
    if resolution.target_coordinate_status not in {
        "RESOLVED",
        "MULTI_CANDIDATE_OR_BOUNDARY_UNCERTAINTY",
    }:
        diagnostics.append("TARGET_COORDINATE_STATUS_INVALID")
    if resolution.bazi_target_flow_status not in {"RESOLVED", "MULTI_CANDIDATE"}:
        diagnostics.append("BAZI_TARGET_FLOW_STATUS_INVALID")
    if resolution.ziwei_selector_status != "RESOLVED":
        diagnostics.append("ZIWEI_SELECTOR_STATUS_INVALID")
    if resolution.ziwei_selector_candidate_count < 1:
        diagnostics.append("ZIWEI_SELECTOR_CANDIDATE_COUNT_INVALID")
    if resolution.status != _expected_status(resolution):
        diagnostics.append("RESOLUTION_STATUS_MISMATCH")

    hash_fields = {
        "BASE_COMBINED_MANIFEST_HASH_MISSING": resolution.base_combined_manifest_hash,
        "R1_TARGET_FLOW_BUNDLE_HASH_MISSING": resolution.r1_target_flow_bundle_hash,
        "TARGET_COORDINATE_FACT_HASH_MISSING": resolution.target_coordinate_fact_hash,
        "TARGET_COORDINATE_COMPUTATION_HASH_MISSING": (
            resolution.target_coordinate_computation_hash
        ),
        "BAZI_TARGET_FLOW_SOURCE_FACT_HASH_MISSING": (
            resolution.bazi_target_flow_source_fact_hash
        ),
        "BAZI_TARGET_FLOW_VIEW_HASH_MISSING": resolution.bazi_target_flow_view_hash,
        "BAZI_TARGET_FLOW_BUNDLE_HASH_MISSING": resolution.bazi_target_flow_bundle_hash,
        "ZIWEI_SELECTOR_FACT_HASH_MISSING": resolution.ziwei_selector_fact_hash,
        "ZIWEI_SELECTOR_COMPUTATION_HASH_MISSING": (
            resolution.ziwei_selector_computation_hash
        ),
    }
    for code, value in hash_fields.items():
        if not value:
            diagnostics.append(code)

    if (
        resolution.source_fact_hash
        != combined_target_flow_fusion_r2_source_fact_hash(resolution)
    ):
        diagnostics.append("SOURCE_FACT_HASH_MISMATCH")
    if resolution.view_hash != combined_target_flow_fusion_r2_view_hash(resolution):
        diagnostics.append("VIEW_HASH_MISMATCH")
    if resolution.bundle_hash != combined_target_flow_fusion_r2_bundle_hash(resolution):
        diagnostics.append("BUNDLE_HASH_MISMATCH")

    return CombinedTargetFlowFusionR2IntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )


class CombinedTargetFlowFusionR2Service:
    """Compose the already-released Bazi and Ziwei target-time projections.

    R2 deliberately does not change R1. The same target coordinate resolution
    is replayed into both subsystems while their calendar/day-boundary policies
    remain independent.
    """

    schema = COMBINED_TARGET_FLOW_FUSION_R2_SCHEMA

    def __init__(
        self,
        r1_service: CombinedTargetFlowService,
        *,
        target_foundation: TargetTemporalCoordinateFoundation | None = None,
        ziwei_selector_service: SharedZiweiSelectorProjectionService | None = None,
    ) -> None:
        self.r1_service = r1_service
        self.target_foundation = target_foundation or TargetTemporalCoordinateFoundation()
        self.ziwei_selector_service = (
            ziwei_selector_service or SharedZiweiSelectorProjectionService()
        )

    @classmethod
    def from_repository(cls, repository_root: Path) -> "CombinedTargetFlowFusionR2Service":
        return cls(CombinedTargetFlowService.from_repository(repository_root))

    def _resolve_all(
        self,
        request: CombinedTargetFlowRequest,
    ) -> tuple[
        Any,
        Any,
        Any,
        TargetTemporalCoordinateResolution,
        SharedZiweiSelectorProjectionResolution,
        CombinedTargetFlowFusionR2Resolution,
    ]:
        target_profile = request.target_coordinate_profile.validate()
        base, bazi_flow, r1 = self.r1_service.resolve_with_bundles(request)

        target = self.target_foundation.resolve(request.target_input, target_profile)
        target_report = validate_target_temporal_resolution(
            target,
            target_profile,
            self.target_foundation.civil,
            self.target_foundation.solar,
        )
        if target_report.status != "PASS" or target.integrity != target_report:
            raise CombinedTargetFlowFusionR2ResolutionError(
                "COMBINED_TARGET_FLOW_FUSION_R2_TARGET_INTEGRITY_FAILED",
                ";".join(row.code for row in target_report.diagnostics)
                or "embedded target integrity mismatch",
            )
        if not target.candidates:
            raise CombinedTargetFlowFusionR2ResolutionError(
                "COMBINED_TARGET_FLOW_FUSION_R2_TARGET_CANDIDATE_REQUIRED",
                target.status,
            )

        expected_target_binding = (
            target.hashes.fact_hash,
            target.hashes.computation_hash,
            target.profile_id,
            target.profile_version,
        )
        r1_target_binding = (
            r1.target_coordinate_fact_hash,
            r1.target_coordinate_computation_hash,
            r1.target_coordinate_profile_id,
            r1.target_coordinate_profile_version,
        )
        if r1_target_binding != expected_target_binding:
            raise CombinedTargetFlowFusionR2ResolutionError(
                "COMBINED_TARGET_FLOW_FUSION_R2_R1_TARGET_BINDING_MISMATCH",
                f"r1={r1_target_binding};target={expected_target_binding}",
            )
        bazi_target_binding = (
            bazi_flow.target_coordinate_fact_hash,
            bazi_flow.target_coordinate_computation_hash,
            bazi_flow.target_coordinate_profile_id,
            bazi_flow.target_coordinate_profile_version,
        )
        if bazi_target_binding != expected_target_binding:
            raise CombinedTargetFlowFusionR2ResolutionError(
                "COMBINED_TARGET_FLOW_FUSION_R2_BAZI_TARGET_BINDING_MISMATCH",
                f"bazi={bazi_target_binding};target={expected_target_binding}",
            )
        if bazi_flow.target_input != request.target_input:
            raise CombinedTargetFlowFusionR2ResolutionError(
                "COMBINED_TARGET_FLOW_FUSION_R2_BAZI_TARGET_INPUT_MISMATCH",
                "Bazi target input differs from combined target input",
            )

        if base.ziwei_bundle is None:
            raise CombinedTargetFlowFusionR2ResolutionError(
                "COMBINED_TARGET_FLOW_FUSION_R2_ZIWEI_BASE_REQUIRED",
                base.status,
            )
        ziwei_selector = self.ziwei_selector_service.project(
            base.ziwei_bundle,
            target,
            target_profile,
        )
        ziwei_report = validate_shared_ziwei_selector_projection(
            base.ziwei_bundle,
            target,
            target_profile,
            ziwei_selector,
        )
        if ziwei_report.status != "PASS" or ziwei_selector.integrity != ziwei_report:
            raise CombinedTargetFlowFusionR2ResolutionError(
                "COMBINED_TARGET_FLOW_FUSION_R2_ZIWEI_SELECTOR_INTEGRITY_FAILED",
                ";".join(ziwei_report.diagnostics)
                or "embedded Ziwei selector integrity mismatch",
            )
        ziwei_replay = validate_shared_ziwei_selector_full_replay(
            self.ziwei_selector_service,
            base.ziwei_bundle,
            target,
            target_profile,
            ziwei_selector,
        )
        if ziwei_replay.status != "PASS":
            raise CombinedTargetFlowFusionR2ResolutionError(
                "COMBINED_TARGET_FLOW_FUSION_R2_ZIWEI_SELECTOR_REPLAY_FAILED",
                ";".join(ziwei_replay.diagnostics),
            )

        if (
            ziwei_selector.source_target_coordinate_fact_hash
            != target.hashes.fact_hash
            or ziwei_selector.source_target_coordinate_computation_hash
            != target.hashes.computation_hash
        ):
            raise CombinedTargetFlowFusionR2ResolutionError(
                "COMBINED_TARGET_FLOW_FUSION_R2_ZIWEI_TARGET_BINDING_MISMATCH",
                ziwei_selector.source_target_coordinate_fact_hash,
            )

        provisional = CombinedTargetFlowFusionR2Resolution(
            schema=self.schema,
            status="PENDING",
            composition_semantics=r1.composition_semantics,
            base_combined_manifest_hash=base.manifest_hash,
            r1_target_flow_bundle_hash=r1.bundle_hash,
            target_coordinate_status=target.status,
            target_coordinate_fact_hash=target.hashes.fact_hash,
            target_coordinate_computation_hash=target.hashes.computation_hash,
            target_coordinate_profile_id=target.profile_id,
            target_coordinate_profile_version=target.profile_version,
            target_input=request.target_input,
            bazi_target_flow_status=bazi_flow.status,
            bazi_target_flow_source_fact_hash=bazi_flow.source_fact_hash,
            bazi_target_flow_view_hash=bazi_flow.view_hash,
            bazi_target_flow_bundle_hash=bazi_flow.bundle_hash,
            ziwei_selector_status=ziwei_selector.status,
            ziwei_selector_candidate_count=len(ziwei_selector.candidates),
            ziwei_selector_fact_hash=ziwei_selector.hashes.fact_hash,
            ziwei_selector_computation_hash=ziwei_selector.hashes.computation_hash,
            source_fact_hash="",
            view_hash="",
            bundle_hash="",
            integrity=CombinedTargetFlowFusionR2IntegrityReport(
                status="PENDING", diagnostics=()
            ),
        )
        provisional = replace(provisional, status=_expected_status(provisional))
        provisional = replace(
            provisional,
            source_fact_hash=combined_target_flow_fusion_r2_source_fact_hash(
                provisional
            ),
        )
        provisional = replace(
            provisional,
            view_hash=combined_target_flow_fusion_r2_view_hash(provisional),
        )
        provisional = replace(
            provisional,
            bundle_hash=combined_target_flow_fusion_r2_bundle_hash(provisional),
        )
        report = validate_combined_target_flow_fusion_r2_resolution(provisional)
        if report.status != "PASS":
            raise CombinedTargetFlowFusionR2ResolutionError(
                "COMBINED_TARGET_FLOW_FUSION_R2_INTEGRITY_FAILED",
                ";".join(report.diagnostics),
            )
        return (
            base,
            bazi_flow,
            r1,
            target,
            ziwei_selector,
            replace(provisional, integrity=report),
        )

    def resolve(
        self,
        request: CombinedTargetFlowRequest,
    ) -> CombinedTargetFlowFusionR2Resolution:
        return self._resolve_all(request)[5]

    def resolve_with_bundles(
        self,
        request: CombinedTargetFlowRequest,
    ) -> tuple[
        Any,
        Any,
        Any,
        TargetTemporalCoordinateResolution,
        SharedZiweiSelectorProjectionResolution,
        CombinedTargetFlowFusionR2Resolution,
    ]:
        return self._resolve_all(request)


def validate_combined_target_flow_fusion_r2_full_replay(
    service: CombinedTargetFlowFusionR2Service,
    request: CombinedTargetFlowRequest,
    resolution: CombinedTargetFlowFusionR2Resolution,
) -> CombinedTargetFlowFusionR2IntegrityReport:
    try:
        replayed = service.resolve(request)
    except (
        CombinedTargetFlowFusionR2ResolutionError,
        CombinedTargetFlowResolutionError,
        ValueError,
    ) as exc:
        return CombinedTargetFlowFusionR2IntegrityReport(
            status="FAIL",
            diagnostics=(f"FULL_REPLAY_RESOLUTION_FAILED:{exc}",),
        )
    if replayed != resolution:
        return CombinedTargetFlowFusionR2IntegrityReport(
            status="FAIL",
            diagnostics=("COMBINED_TARGET_FLOW_FUSION_R2_FULL_REPLAY_MISMATCH",),
        )
    return CombinedTargetFlowFusionR2IntegrityReport(status="PASS", diagnostics=())


def combined_target_flow_fusion_r2_export(
    resolution: CombinedTargetFlowFusionR2Resolution,
) -> dict[str, Any]:
    report = validate_combined_target_flow_fusion_r2_resolution(resolution)
    if report.status != "PASS" or report != resolution.integrity:
        raise CombinedTargetFlowFusionR2ResolutionError(
            "COMBINED_TARGET_FLOW_FUSION_R2_EXPORT_INTEGRITY_FAILED",
            ";".join(report.diagnostics) or "embedded integrity mismatch",
        )
    return json_value(resolution)
