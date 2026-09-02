from __future__ import annotations

from dataclasses import dataclass, replace

from fortune_training.util import object_sha256
from fortune_training.ziwei_structural.r6 import (
    QiShuPositionState,
    ZiweiQiShuPositionRuntime,
    validate_qishu_state,
    ziwei_structural_v2_r6_profile,
)
from fortune_training.ziwei_structural.r7 import (
    OneSixCommonRootState,
    ZiweiOneSixCommonRootRuntime,
    validate_one_six_state,
    ziwei_structural_v2_r7_profile,
)
from fortune_training.ziwei_structural.r8 import (
    AdjacentPalacePairState,
    ZiweiAdjacentPalaceRuntime,
    validate_adjacent_palace_state,
    ziwei_structural_v2_r8_profile,
)

from .models import ApplicationChartBundle
from .service import ApplicationResolutionError, validate_application_bundle


STRUCTURAL_RELATION_PROJECTIONS_SCHEMA = (
    "ZIWEI-STRUCTURAL-RELATION-PROJECTIONS-SIDECAR-R1"
)
STRUCTURAL_RELATION_PROJECTIONS_PROFILE_ID = (
    "ZIWEI-STRUCTURAL-RELATION-PROJECTIONS-R1"
)
STRUCTURAL_RELATION_PROJECTIONS_PROFILE_VERSION = "1.0.0"
STRUCTURAL_RELATION_PROJECTIONS_ALGORITHM_ID = (
    "ZIWEI-STRUCTURAL-RELATION-PROJECTIONS-COMPOSER-R1"
)
STRUCTURAL_RELATION_PROJECTIONS_ALGORITHM_VERSION = "1.0.0"
STRUCTURAL_RELATION_PROJECTIONS_INTEGRITY_ID = (
    "ZIWEI-STRUCTURAL-RELATION-PROJECTIONS-INTEGRITY-R1"
)
STRUCTURAL_RELATION_PROJECTIONS_INTEGRITY_VERSION = "1.0.0"
STRUCTURAL_RELATION_PROJECTIONS_SEMANTIC_SCOPE = (
    "R6_R7_R8_READ_ONLY_NATAL_RELATION_PROJECTIONS_"
    "NO_EVENT_ENDPOINT_SCORE_OR_FLANK_JUDGMENT"
)


class ZiweiStructuralRelationProjectionResolutionError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code
        self.detail = detail


@dataclass(frozen=True)
class ZiweiStructuralRelationProjectionIntegrityReport:
    status: str
    diagnostics: tuple[str, ...]
    algorithm_id: str = STRUCTURAL_RELATION_PROJECTIONS_INTEGRITY_ID
    algorithm_version: str = STRUCTURAL_RELATION_PROJECTIONS_INTEGRITY_VERSION


@dataclass(frozen=True)
class ZiweiStructuralRelationProjectionResolution:
    schema: str
    status: str
    source_application_bundle_hash: str
    source_r2_fact_hash: str
    source_r2_computation_hash: str
    profile_id: str
    profile_version: str
    semantic_scope: str
    qishu: QiShuPositionState
    one_six: OneSixCommonRootState
    adjacent_palace: AdjacentPalacePairState
    bundle_hash: str
    integrity: ZiweiStructuralRelationProjectionIntegrityReport


def _component_ref(state) -> dict[str, str]:
    return {
        "schema": state.schema,
        "fact_hash": state.hashes.fact_hash,
        "computation_hash": state.hashes.computation_hash,
    }


def structural_relation_projections_bundle_hash(
    *,
    source_application_bundle_hash: str,
    source_r2_fact_hash: str,
    source_r2_computation_hash: str,
    qishu: QiShuPositionState,
    one_six: OneSixCommonRootState,
    adjacent_palace: AdjacentPalacePairState,
) -> str:
    return object_sha256(
        {
            "schema": STRUCTURAL_RELATION_PROJECTIONS_SCHEMA,
            "status": "COMPLETE",
            "source_application_bundle_hash": source_application_bundle_hash,
            "source_r2_fact_hash": source_r2_fact_hash,
            "source_r2_computation_hash": source_r2_computation_hash,
            "profile_id": STRUCTURAL_RELATION_PROJECTIONS_PROFILE_ID,
            "profile_version": STRUCTURAL_RELATION_PROJECTIONS_PROFILE_VERSION,
            "semantic_scope": STRUCTURAL_RELATION_PROJECTIONS_SEMANTIC_SCOPE,
            "components": {
                "qishu": _component_ref(qishu),
                "one_six": _component_ref(one_six),
                "adjacent_palace": _component_ref(adjacent_palace),
            },
            "algorithm": (
                f"{STRUCTURAL_RELATION_PROJECTIONS_ALGORITHM_ID}@"
                f"{STRUCTURAL_RELATION_PROJECTIONS_ALGORITHM_VERSION}"
            ),
        }
    )


def validate_structural_relation_projections(
    base_application: ApplicationChartBundle,
    resolution: ZiweiStructuralRelationProjectionResolution,
) -> ZiweiStructuralRelationProjectionIntegrityReport:
    diagnostics: list[str] = []
    try:
        validate_application_bundle(base_application)
    except ApplicationResolutionError as exc:
        diagnostics.append(f"SOURCE_APPLICATION_INVALID:{exc.diagnostic_code}")
        return ZiweiStructuralRelationProjectionIntegrityReport(
            status="FAIL",
            diagnostics=tuple(diagnostics),
        )

    if resolution.schema != STRUCTURAL_RELATION_PROJECTIONS_SCHEMA:
        diagnostics.append("SCHEMA_MISMATCH")
    if resolution.status != "COMPLETE":
        diagnostics.append("STATUS_NOT_COMPLETE")
    if (
        resolution.profile_id != STRUCTURAL_RELATION_PROJECTIONS_PROFILE_ID
        or resolution.profile_version != STRUCTURAL_RELATION_PROJECTIONS_PROFILE_VERSION
    ):
        diagnostics.append("PROFILE_MISMATCH")
    if resolution.semantic_scope != STRUCTURAL_RELATION_PROJECTIONS_SEMANTIC_SCOPE:
        diagnostics.append("SEMANTIC_SCOPE_MISMATCH")
    if resolution.source_application_bundle_hash != base_application.bundle_hash:
        diagnostics.append("SOURCE_APPLICATION_BUNDLE_HASH_MISMATCH")
    if resolution.source_r2_fact_hash != base_application.r2_state.hashes.fact_hash:
        diagnostics.append("SOURCE_R2_FACT_HASH_MISMATCH")
    if (
        resolution.source_r2_computation_hash
        != base_application.r2_state.hashes.computation_hash
    ):
        diagnostics.append("SOURCE_R2_COMPUTATION_HASH_MISMATCH")

    components = (
        ("R6", resolution.qishu, validate_qishu_state),
        ("R7", resolution.one_six, validate_one_six_state),
        ("R8", resolution.adjacent_palace, validate_adjacent_palace_state),
    )
    for label, state, validator in components:
        report = validator(base_application.r2_state, state)
        if report.status != "PASS":
            first = report.diagnostics[0] if report.diagnostics else None
            detail = first.code if first is not None else "UNKNOWN"
            diagnostics.append(f"{label}_INTEGRITY_FAILED:{detail}")
        if state.upstream_r2_fact_hash != base_application.r2_state.hashes.fact_hash:
            diagnostics.append(f"{label}_UPSTREAM_R2_FACT_HASH_MISMATCH")
        if (
            state.upstream_r2_computation_hash
            != base_application.r2_state.hashes.computation_hash
        ):
            diagnostics.append(f"{label}_UPSTREAM_R2_COMPUTATION_HASH_MISMATCH")
        if state.time_layer != "NATAL":
            diagnostics.append(f"{label}_TIME_LAYER_MISMATCH")

    expected_bundle_hash = structural_relation_projections_bundle_hash(
        source_application_bundle_hash=resolution.source_application_bundle_hash,
        source_r2_fact_hash=resolution.source_r2_fact_hash,
        source_r2_computation_hash=resolution.source_r2_computation_hash,
        qishu=resolution.qishu,
        one_six=resolution.one_six,
        adjacent_palace=resolution.adjacent_palace,
    )
    if resolution.bundle_hash != expected_bundle_hash:
        diagnostics.append("BUNDLE_HASH_MISMATCH")

    return ZiweiStructuralRelationProjectionIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )


class ZiweiStructuralRelationProjectionService:
    """Application sidecar exposing released R6-R8 structural states unchanged."""

    def __init__(self) -> None:
        self.r6 = ZiweiQiShuPositionRuntime()
        self.r7 = ZiweiOneSixCommonRootRuntime()
        self.r8 = ZiweiAdjacentPalaceRuntime()

    def _resolve_once(
        self,
        base_application: ApplicationChartBundle,
    ) -> ZiweiStructuralRelationProjectionResolution:
        try:
            validate_application_bundle(base_application)
        except ApplicationResolutionError as exc:
            raise ZiweiStructuralRelationProjectionResolutionError(
                "ZIWEI_STRUCTURAL_RELATIONS_SOURCE_APPLICATION_INVALID",
                str(exc),
            ) from exc

        try:
            qishu = self.r6.generate_from_candidate(
                base_application.candidate,
                base_application.r1_state,
                base_application.r2_state,
                ziwei_structural_v2_r6_profile(),
            )
            one_six = self.r7.generate_from_candidate(
                base_application.candidate,
                base_application.r1_state,
                base_application.r2_state,
                ziwei_structural_v2_r7_profile(),
            )
            adjacent_palace = self.r8.generate_from_candidate(
                base_application.candidate,
                base_application.r1_state,
                base_application.r2_state,
                ziwei_structural_v2_r8_profile(),
            )
        except ValueError as exc:
            code = getattr(exc, "diagnostic_code", None)
            raise ZiweiStructuralRelationProjectionResolutionError(
                str(code or "ZIWEI_STRUCTURAL_RELATIONS_RUNTIME_FAILED"),
                str(exc),
            ) from exc

        bundle_hash = structural_relation_projections_bundle_hash(
            source_application_bundle_hash=base_application.bundle_hash,
            source_r2_fact_hash=base_application.r2_state.hashes.fact_hash,
            source_r2_computation_hash=base_application.r2_state.hashes.computation_hash,
            qishu=qishu,
            one_six=one_six,
            adjacent_palace=adjacent_palace,
        )
        provisional = ZiweiStructuralRelationProjectionResolution(
            schema=STRUCTURAL_RELATION_PROJECTIONS_SCHEMA,
            status="COMPLETE",
            source_application_bundle_hash=base_application.bundle_hash,
            source_r2_fact_hash=base_application.r2_state.hashes.fact_hash,
            source_r2_computation_hash=base_application.r2_state.hashes.computation_hash,
            profile_id=STRUCTURAL_RELATION_PROJECTIONS_PROFILE_ID,
            profile_version=STRUCTURAL_RELATION_PROJECTIONS_PROFILE_VERSION,
            semantic_scope=STRUCTURAL_RELATION_PROJECTIONS_SEMANTIC_SCOPE,
            qishu=qishu,
            one_six=one_six,
            adjacent_palace=adjacent_palace,
            bundle_hash=bundle_hash,
            integrity=ZiweiStructuralRelationProjectionIntegrityReport(
                status="PENDING",
                diagnostics=(),
            ),
        )
        integrity = validate_structural_relation_projections(
            base_application,
            provisional,
        )
        if integrity.status != "PASS":
            raise ZiweiStructuralRelationProjectionResolutionError(
                "ZIWEI_STRUCTURAL_RELATIONS_INTEGRITY_FAILED",
                ";".join(integrity.diagnostics),
            )
        return replace(provisional, integrity=integrity)

    def resolve(
        self,
        base_application: ApplicationChartBundle,
    ) -> ZiweiStructuralRelationProjectionResolution:
        first = self._resolve_once(base_application)
        replay = self._resolve_once(base_application)
        if replay != first:
            raise ZiweiStructuralRelationProjectionResolutionError(
                "ZIWEI_STRUCTURAL_RELATIONS_FULL_REPLAY_FAILED",
                "identical application bundle produced different R6-R8 sidecar state",
            )
        return first
