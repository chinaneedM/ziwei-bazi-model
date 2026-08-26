from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping, Sequence

from fortune_training.bazi_application.flow_integrity import validate_application_flow_resolution
from fortune_training.bazi_application.flow_models import BaziApplicationFlowResolution
from fortune_training.bazi_application.integrity import validate_application_resolution
from fortune_training.bazi_application.models import BaziApplicationCandidate, BaziApplicationResolution
from fortune_training.bazi_application.temporal_shensha import temporal_shensha_target_projection
from fortune_training.util import object_sha256

from .integrity import (
    temporal_shensha_sidecar_bundle_hash,
    temporal_shensha_sidecar_candidate_computation_hash,
    temporal_shensha_sidecar_candidate_fact_hash,
    temporal_shensha_sidecar_candidate_id,
    temporal_shensha_sidecar_computation_hash,
    temporal_shensha_sidecar_fact_hash,
    validate_temporal_shensha_sidecar_resolution,
)
from .models import (
    TEMPORAL_SHENSHA_SIDECAR_PROFILE_ID,
    TEMPORAL_SHENSHA_SIDECAR_PROFILE_VERSION,
    TEMPORAL_SHENSHA_SIDECAR_SCHEMA,
    TemporalShenshaSidecarCandidate,
    TemporalShenshaSidecarIntegrityReport,
    TemporalShenshaSidecarResolution,
)


class TemporalShenshaSidecarResolutionError(ValueError):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


def coherent_source_shensha_for_candidates(
    candidates: Sequence[BaziApplicationCandidate],
) -> tuple[Mapping[str, Any], str]:
    if not candidates:
        raise TemporalShenshaSidecarResolutionError(
            "BAZI_TEMPORAL_SHENSHA_SOURCE_LINEAGE_EMPTY", "0"
        )
    rows: list[Mapping[str, Any]] = []
    for candidate in candidates:
        shensha = candidate.view.get("shensha")
        if not isinstance(shensha, Mapping):
            raise TemporalShenshaSidecarResolutionError(
                "BAZI_TEMPORAL_SHENSHA_SOURCE_VIEW_MISSING",
                candidate.candidate_id,
            )
        rows.append(shensha)
    first = rows[0]
    first_hash = object_sha256(first)
    for index, row in enumerate(rows[1:], start=1):
        if row != first or object_sha256(row) != first_hash:
            raise TemporalShenshaSidecarResolutionError(
                "BAZI_TEMPORAL_SHENSHA_SOURCE_LINEAGE_MISMATCH",
                f"candidate0={candidates[0].candidate_id};candidate{index}={candidates[index].candidate_id}",
            )
    return first, first_hash


def _mapping_or_none(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


class BaziTemporalShenshaSidecarService:
    schema = TEMPORAL_SHENSHA_SIDECAR_SCHEMA

    def resolve(
        self,
        base_application: BaziApplicationResolution,
        bazi_target_flow: BaziApplicationFlowResolution,
    ) -> TemporalShenshaSidecarResolution:
        base_report = validate_application_resolution(base_application)
        if base_report.status != "PASS" or base_report != base_application.integrity:
            raise TemporalShenshaSidecarResolutionError(
                "BAZI_TEMPORAL_SHENSHA_BASE_REPLAY_FAILED",
                ";".join(base_report.diagnostics) or base_report.status,
            )
        flow_report = validate_application_flow_resolution(bazi_target_flow)
        if flow_report.status != "PASS" or flow_report != bazi_target_flow.integrity:
            raise TemporalShenshaSidecarResolutionError(
                "BAZI_TEMPORAL_SHENSHA_FLOW_REPLAY_FAILED",
                ";".join(flow_report.diagnostics) or flow_report.status,
            )
        if bazi_target_flow.base_application_bundle_hash != base_application.bundle_hash:
            raise TemporalShenshaSidecarResolutionError(
                "BAZI_TEMPORAL_SHENSHA_BASE_BUNDLE_HASH_MISMATCH",
                f"base={base_application.bundle_hash};flow={bazi_target_flow.base_application_bundle_hash}",
            )

        source_by_id = {row.candidate_id: row for row in base_application.candidates}
        if len(source_by_id) != len(base_application.candidates):
            raise TemporalShenshaSidecarResolutionError(
                "BAZI_TEMPORAL_SHENSHA_SOURCE_CANDIDATE_ID_DUPLICATE",
                str(len(base_application.candidates)),
            )

        candidates: list[TemporalShenshaSidecarCandidate] = []
        for flow_candidate_index, flow_candidate in enumerate(bazi_target_flow.candidates):
            source_candidates: list[BaziApplicationCandidate] = []
            for source_id in flow_candidate.source_application_candidate_ids:
                source = source_by_id.get(source_id)
                if source is None:
                    raise TemporalShenshaSidecarResolutionError(
                        "BAZI_TEMPORAL_SHENSHA_SOURCE_LINEAGE_MISSING",
                        f"flow={flow_candidate.candidate_id};source={source_id}",
                    )
                source_candidates.append(source)
            source_shensha, source_shensha_hash = coherent_source_shensha_for_candidates(
                source_candidates
            )

            timeline = flow_candidate.view.get("timeline")
            if not isinstance(timeline, Mapping):
                raise TemporalShenshaSidecarResolutionError(
                    "BAZI_TEMPORAL_SHENSHA_TIMELINE_MISSING",
                    flow_candidate.candidate_id,
                )
            dayun = timeline.get("dayun")
            xiaoyun = timeline.get("xiaoyun")
            if not isinstance(dayun, Mapping) or not isinstance(xiaoyun, Mapping):
                raise TemporalShenshaSidecarResolutionError(
                    "BAZI_TEMPORAL_SHENSHA_TIMELINE_STRUCTURE_INVALID",
                    flow_candidate.candidate_id,
                )
            xiaoyun_candidates = xiaoyun.get("candidates")
            if not isinstance(xiaoyun_candidates, list):
                raise TemporalShenshaSidecarResolutionError(
                    "BAZI_TEMPORAL_SHENSHA_XIAOYUN_CANDIDATES_INVALID",
                    flow_candidate.candidate_id,
                )

            projection = temporal_shensha_target_projection(
                source_shensha,
                dayun_kind=str(dayun.get("kind", "")),
                dayun_frame=_mapping_or_none(dayun.get("frame")),
                xiaoyun_candidates=xiaoyun_candidates,
                annual_frame=_mapping_or_none(timeline.get("annual")),
                monthly_frame=_mapping_or_none(timeline.get("monthly")),
                daily_frame=_mapping_or_none(timeline.get("daily")),
                hourly_frame=_mapping_or_none(timeline.get("hourly")),
            )
            provisional = TemporalShenshaSidecarCandidate(
                candidate_id="",
                source_bazi_target_flow_candidate_id=flow_candidate.candidate_id,
                source_bazi_target_flow_candidate_index=flow_candidate_index,
                source_flow_candidate_index=flow_candidate.source_flow_candidate_index,
                source_target_coordinate_candidate_index=flow_candidate.source_target_coordinate_candidate_index,
                target_coordinate_candidate_id=flow_candidate.target_coordinate_candidate_id,
                source_application_candidate_ids=flow_candidate.source_application_candidate_ids,
                source_application_view_hashes=tuple(row.view_hash for row in source_candidates),
                source_shensha_hash=source_shensha_hash,
                projection=projection,
                fact_hash="",
                computation_hash="",
            )
            provisional = replace(
                provisional,
                fact_hash=temporal_shensha_sidecar_candidate_fact_hash(provisional),
            )
            provisional = replace(
                provisional,
                computation_hash=temporal_shensha_sidecar_candidate_computation_hash(provisional),
            )
            candidates.append(
                replace(
                    provisional,
                    candidate_id=temporal_shensha_sidecar_candidate_id(provisional),
                )
            )

        candidate_tuple = tuple(candidates)
        if not candidate_tuple:
            raise TemporalShenshaSidecarResolutionError(
                "BAZI_TEMPORAL_SHENSHA_NO_FLOW_CANDIDATES", "0"
            )
        provisional_resolution = TemporalShenshaSidecarResolution(
            schema=self.schema,
            status="RESOLVED" if len(candidate_tuple) == 1 else "MULTI_CANDIDATE",
            base_application_bundle_hash=base_application.bundle_hash,
            base_application_source_fact_hash=base_application.source_fact_hash,
            bazi_target_flow_bundle_hash=bazi_target_flow.bundle_hash,
            bazi_target_flow_source_fact_hash=bazi_target_flow.source_fact_hash,
            projection_profile_id=TEMPORAL_SHENSHA_SIDECAR_PROFILE_ID,
            projection_profile_version=TEMPORAL_SHENSHA_SIDECAR_PROFILE_VERSION,
            candidates=candidate_tuple,
            diagnostics=(),
            fact_hash="",
            computation_hash="",
            bundle_hash="",
            integrity=TemporalShenshaSidecarIntegrityReport(status="PENDING", diagnostics=()),
        )
        provisional_resolution = replace(
            provisional_resolution,
            fact_hash=temporal_shensha_sidecar_fact_hash(provisional_resolution),
        )
        provisional_resolution = replace(
            provisional_resolution,
            computation_hash=temporal_shensha_sidecar_computation_hash(provisional_resolution),
        )
        provisional_resolution = replace(
            provisional_resolution,
            bundle_hash=temporal_shensha_sidecar_bundle_hash(provisional_resolution),
        )
        report = validate_temporal_shensha_sidecar_resolution(provisional_resolution)
        if report.status != "PASS":
            raise TemporalShenshaSidecarResolutionError(
                "BAZI_TEMPORAL_SHENSHA_SIDECAR_INTEGRITY_FAILED",
                ";".join(report.diagnostics),
            )
        return replace(provisional_resolution, integrity=report)


def validate_temporal_shensha_sidecar_full_replay(
    service: BaziTemporalShenshaSidecarService,
    base_application: BaziApplicationResolution,
    bazi_target_flow: BaziApplicationFlowResolution,
    resolution: TemporalShenshaSidecarResolution,
) -> TemporalShenshaSidecarIntegrityReport:
    diagnostics: list[str] = []
    structural = validate_temporal_shensha_sidecar_resolution(resolution)
    if structural.status != "PASS":
        diagnostics.extend(f"STRUCTURAL:{row}" for row in structural.diagnostics)
    try:
        expected = service.resolve(base_application, bazi_target_flow)
    except TemporalShenshaSidecarResolutionError as exc:
        diagnostics.append(f"FULL_REPLAY_RESOLUTION_FAILED:{exc.code}:{exc.detail}")
    else:
        if expected != resolution:
            diagnostics.append("FULL_REPLAY_MISMATCH")
    return TemporalShenshaSidecarIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )
