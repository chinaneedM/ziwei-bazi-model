from __future__ import annotations

from dataclasses import replace
from datetime import timezone
from pathlib import Path
from typing import Any

from fortune_training.bazi_chart import BaziChartRequest
from fortune_training.bazi_daily_hourly_flow import (
    BaziDailyHourlyFlowEngine,
    BaziDailyHourlyFlowRequest,
    validate_daily_hourly_resolution,
)
from fortune_training.bazi_flow import (
    BaziFlowEngine,
    BaziFlowRequest,
    flow_hash_bundle,
    validate_flow_context,
)
from fortune_training.bazi_structural import (
    BaziStructuralEngine,
    BaziStructuralRequest,
    bazi_structural_context_r1_profile,
)
from fortune_training.bazi_structural_support import (
    BaziStructuralSupportEngine,
    BaziStructuralSupportRequest,
    bazi_structural_support_foundation_r1_profile,
)
from fortune_training.bazi_target_temporal import (
    TargetTemporalCoordinateFoundation,
    target_hash_bundle,
    validate_target_temporal_resolution,
)
from fortune_training.bazi_temporal import BaziTemporalRequest
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .flow_integrity import (
    application_flow_bundle_hash,
    application_flow_candidate_id,
    application_flow_source_fact_hash,
    application_flow_view_hash,
    validate_application_flow_resolution,
)
from .flow_models import (
    FLOW_APPLICATION_SCHEMA,
    FLOW_APPLICATION_VIEW_SCHEMA,
    BaziApplicationFlowCandidate,
    BaziApplicationFlowIntegrityReport,
    BaziApplicationFlowRequest,
    BaziApplicationFlowResolution,
)
from .models import BaziApplicationResolution
from .service import BaziApplicationResolutionError, BaziChartService
from .temporal_annotations import temporal_classical_annotation_projection
from .structural_projection import structural_projection
from .structural_support_projection import structural_support_projection


class BaziApplicationFlowService:
    schema = FLOW_APPLICATION_SCHEMA

    def __init__(
        self,
        base_service: BaziChartService,
        target_foundation: TargetTemporalCoordinateFoundation | None = None,
        flow_engine: BaziFlowEngine | None = None,
        daily_hourly_engine: BaziDailyHourlyFlowEngine | None = None,
        structural_engine: BaziStructuralEngine | None = None,
        structural_support_engine: BaziStructuralSupportEngine | None = None,
    ) -> None:
        self.base_service = base_service
        self.target_foundation = target_foundation or TargetTemporalCoordinateFoundation()
        self.flow_engine = flow_engine or BaziFlowEngine()
        self.daily_hourly_engine = daily_hourly_engine or BaziDailyHourlyFlowEngine()
        self.structural_engine = structural_engine or BaziStructuralEngine()
        self.structural_support_engine = (
            structural_support_engine or BaziStructuralSupportEngine()
        )

    @classmethod
    def from_repository(cls, repository_root: Path) -> "BaziApplicationFlowService":
        return cls(BaziChartService.from_repository(repository_root))

    @staticmethod
    def _target_view(target_resolution, target_index: int) -> dict[str, Any]:
        target = target_resolution.candidates[target_index]
        source = target_resolution.target_input
        return {
            "target_place": source.target_place,
            "reported_local_datetime": json_value(source.reported_local_datetime),
            "latitude": source.latitude,
            "longitude": source.longitude,
            "timezone_id": source.timezone_id,
            "precision": source.precision.value,
            "uncertainty_seconds": source.uncertainty_seconds,
            "target_coordinate_candidate_index": target_index,
            "target_coordinate_candidate_id": target.candidate_id,
            "source_sample_index": target.source_sample_index,
            "sample_reported_local_datetime": json_value(
                target.sample_reported_local_datetime
            ),
            "civil_status": target.civil_status,
            "fold": target.fold,
            "utc_offset_seconds": target.utc_offset_seconds,
            "target_utc": json_value(target.target_utc),
            "local_apparent_solar_datetime": json_value(
                target.local_apparent_solar_datetime
            ),
        }

    @staticmethod
    def _build_view(
        natal_index: int,
        flow,
        flow_index: int,
        daily_hourly,
        structural,
        structural_support,
        target_resolution,
        source_application_candidate_ids: tuple[str, ...],
        xiaoyun: dict[str, Any],
        birth_civil_year: int,
        day_master_stem: str,
    ) -> dict[str, Any]:
        context = daily_hourly.context
        target_index = daily_hourly.source_target_coordinate_candidate_index
        target_candidate = target_resolution.candidates[target_index]
        nominal_age = (
            target_candidate.sample_reported_local_datetime.year
            - birth_civil_year
            + 1
        )
        active_xiaoyun = []
        for candidate in xiaoyun["candidates"]:
            matches = [
                frame
                for frame in candidate["frames"]
                if frame["nominal_age"] == nominal_age
            ]
            active_xiaoyun.append(
                {
                    "profile_id": candidate["profile_id"],
                    "direction": candidate["direction"],
                    "source_refs": candidate["source_refs"],
                    "active_frame": matches[0] if len(matches) == 1 else None,
                    "activation_status": (
                        "OPERATIONAL_CIVIL_NOMINAL_AGE_MATCH"
                        if len(matches) == 1
                        else "OUTSIDE_MATERIALIZED_XIAOYUN_RANGE"
                    ),
                }
            )
        timeline = {
            "schema": "BAZI-UNIFIED-TARGET-TIMELINE-R1",
            "target_coordinate_candidate_id": target_candidate.candidate_id,
            "layer_order": [
                "NATAL",
                "DAYUN",
                "XIAOYUN",
                "ANNUAL",
                "MONTHLY",
                "DAILY",
                "HOURLY",
            ],
            "natal": {
                "source_application_candidate_ids": list(
                    source_application_candidate_ids
                ),
                "natal_fact_hash": flow.context.upstream_natal_fact_hash,
            },
            "dayun": {
                "kind": flow.context.active_dayun_kind,
                "frame": json_value(flow.context.active_dayun_frame),
            },
            "xiaoyun": {
                "selection_status": "UNRESOLVED_CLASSICAL_METHOD_ALTERNATIVES",
                "age_coordinate": {
                    "nominal_age": nominal_age,
                    "profile_id": "TARGET-CIVIL-YEAR-NOMINAL-AGE-R1",
                    "source_class": "ENGINEERING_LINKAGE_COORDINATE",
                    "formula": "target_local_civil_year-birth_local_civil_year+1",
                    "classical_age_boundary_status": "NOT_ARBITRATED",
                },
                "candidates": active_xiaoyun,
            },
            "annual": json_value(flow.context.annual_frame),
            "monthly": json_value(flow.context.monthly_frame),
            "daily": json_value(context.daily_frame),
            "hourly": json_value(context.hourly_frame),
            "semantic_scope": "TEMPORAL_COORDINATES_ONLY_NO_INTERPRETATION",
        }
        timeline["classical_annotations"] = temporal_classical_annotation_projection(
            day_master_stem,
            dayun_kind=flow.context.active_dayun_kind,
            dayun_frame=json_value(flow.context.active_dayun_frame),
            xiaoyun_candidates=active_xiaoyun,
            annual_frame=json_value(flow.context.annual_frame),
            monthly_frame=json_value(flow.context.monthly_frame),
            daily_frame=json_value(context.daily_frame),
            hourly_frame=json_value(context.hourly_frame),
        )
        return {
            "target": BaziApplicationFlowService._target_view(
                target_resolution, target_index
            ),
            "flow": {
                "active_dayun_kind": flow.context.active_dayun_kind,
                "active_dayun_frame": json_value(flow.context.active_dayun_frame),
                "annual": json_value(flow.context.annual_frame),
                "monthly": json_value(flow.context.monthly_frame),
            },
            "daily": json_value(context.daily_frame),
            "hourly": json_value(context.hourly_frame),
            "timeline": timeline,
            "structural": structural_projection(structural),
            "structural_support": structural_support_projection(
                structural_support
            ),
            "lineage": {
                "natal_candidate_index": natal_index,
                "source_temporal_candidate_indices": list(
                    flow.source_temporal_candidate_indices
                ),
                "source_application_candidate_ids": list(
                    source_application_candidate_ids
                ),
                "source_flow_candidate_index": flow_index,
                "source_target_coordinate_candidate_index": target_index,
            },
            "integrity": {
                "target_coordinate": target_resolution.integrity.status,
                "flow": flow.integrity.status,
                "daily_hourly": daily_hourly.integrity.status,
                "structural": structural.integrity.status,
                "structural_support": structural_support.integrity.status,
            },
            "source_hashes": {
                "natal_fact_hash": flow.context.upstream_natal_fact_hash,
                "temporal_fact_hash": flow.context.upstream_temporal_fact_hash,
                "flow_fact_hash": flow.hashes.fact_hash,
                "flow_computation_hash": flow.hashes.computation_hash,
                "structural_fact_hash": structural.hashes.fact_hash,
                "structural_computation_hash": structural.hashes.computation_hash,
                "structural_support_fact_hash": structural_support.hashes.fact_hash,
                "structural_support_computation_hash": (
                    structural_support.hashes.computation_hash
                ),
                "target_coordinate_fact_hash": target_resolution.hashes.fact_hash,
                "target_coordinate_computation_hash": (
                    target_resolution.hashes.computation_hash
                ),
                "daily_hourly_fact_hash": daily_hourly.hashes.fact_hash,
                "daily_hourly_computation_hash": (
                    daily_hourly.hashes.computation_hash
                ),
            },
        }

    def _validate_target_resolution(self, target_resolution, target_profile) -> None:
        replay = validate_target_temporal_resolution(
            target_resolution,
            target_profile,
            self.target_foundation.civil,
            self.target_foundation.solar,
        )
        if replay.status != "PASS" or replay != target_resolution.integrity:
            detail = ";".join(
                f"{row.code}:{row.path}" for row in replay.diagnostics
            ) or replay.status
            raise BaziApplicationResolutionError(
                "BAZI_APP_FLOW_TARGET_REPLAY_FAILED", detail
            )
        expected_hashes = target_hash_bundle(target_resolution, target_profile)
        if expected_hashes != target_resolution.hashes:
            raise BaziApplicationResolutionError(
                "BAZI_APP_FLOW_TARGET_HASH_REPLAY_MISMATCH",
                target_resolution.hashes.fact_hash,
            )
        if target_resolution.status == "FAILED" or not target_resolution.candidates:
            detail = ";".join(target_resolution.diagnostics) or target_resolution.status
            raise BaziApplicationResolutionError(
                "BAZI_APP_FLOW_TARGET_RESOLUTION_FAILED", detail
            )

    def _resolve_pair(
        self, request: BaziApplicationFlowRequest
    ) -> tuple[BaziApplicationResolution, BaziApplicationFlowResolution]:
        base_request = request.application_request
        target_profile = request.target_coordinate_profile.validate()
        base_bundle = self.base_service.resolve(base_request)

        target_resolution = self.target_foundation.resolve(
            request.target_input,
            target_profile,
        )
        self._validate_target_resolution(target_resolution, target_profile)

        base_candidate_by_lineage = {
            (row.natal_candidate_index, row.temporal_candidate_index): row
            for row in base_bundle.candidates
        }
        if len(base_candidate_by_lineage) != len(base_bundle.candidates):
            raise BaziApplicationResolutionError(
                "BAZI_APP_FLOW_BASE_APPLICATION_LINEAGE_DUPLICATE",
                str(len(base_bundle.candidates)),
            )

        natal_resolution = self.base_service.chart_foundation.resolve_typed(
            BaziChartRequest(base_request.birth, base_request.natal_profile)
        )
        if natal_resolution.status == "FAILED" or not natal_resolution.candidates:
            raise BaziApplicationResolutionError(
                "BAZI_APP_FLOW_NATAL_RESOLUTION_FAILED",
                ";".join(natal_resolution.diagnostics) or natal_resolution.status,
            )

        rows: list[BaziApplicationFlowCandidate] = []
        events: list[str] = list(base_bundle.events)
        if (
            len(target_resolution.candidates) > 1
            or target_resolution.unresolved_samples
            or target_resolution.ambiguous_sample_count
        ):
            events.append("TARGET_TEMPORAL_CANDIDATES_PRESERVED")

        for natal_index, natal in enumerate(natal_resolution.candidates):
            self.base_service._validate_natal_candidate(natal, base_request.natal_profile)
            temporal_resolution = self.base_service.temporal_engine.resolve_typed(
                BaziTemporalRequest(
                    candidate=natal,
                    sex=base_request.sex,
                    profile=base_request.temporal_profile,
                    dayun_count=base_request.dayun_count,
                )
            )
            if temporal_resolution.status == "FAILED" or not temporal_resolution.candidates:
                raise BaziApplicationResolutionError(
                    "BAZI_APP_FLOW_TEMPORAL_RESOLUTION_FAILED",
                    ";".join(temporal_resolution.diagnostics)
                    or temporal_resolution.status,
                )
            temporal_candidates = tuple(temporal_resolution.candidates)
            for temporal_index, temporal in enumerate(temporal_candidates):
                self.base_service._validate_temporal_candidate(
                    temporal, natal, base_request.temporal_profile
                )
                base_candidate = base_candidate_by_lineage.get(
                    (natal_index, temporal_index)
                )
                if base_candidate is None:
                    raise BaziApplicationResolutionError(
                        "BAZI_APP_FLOW_BASE_APPLICATION_LINEAGE_MISSING",
                        f"{natal_index}:{temporal_index}",
                    )
                if (
                    base_candidate.natal_fact_hash != natal.hashes.fact_hash
                    or base_candidate.natal_computation_hash
                    != natal.hashes.computation_hash
                    or base_candidate.temporal_fact_hash != temporal.hashes.fact_hash
                    or base_candidate.temporal_computation_hash
                    != temporal.hashes.computation_hash
                ):
                    raise BaziApplicationResolutionError(
                        "BAZI_APP_FLOW_BASE_APPLICATION_HASH_LINEAGE_MISMATCH",
                        f"{natal_index}:{temporal_index}",
                    )

            flow_candidates: list[Any] = []
            seen_target_instants: set[str] = set()
            for target in target_resolution.candidates:
                target_utc = target.target_utc.astimezone(timezone.utc)
                target_key = target_utc.isoformat(timespec="microseconds")
                if target_key in seen_target_instants:
                    continue
                seen_target_instants.add(target_key)
                flow_resolution = self.flow_engine.resolve_typed(
                    BaziFlowRequest(
                        natal_candidate=natal,
                        temporal_candidates=temporal_candidates,
                        target_utc=target_utc,
                        calculation_profile=base_request.natal_profile,
                    )
                )
                if flow_resolution.status == "FAILED" or not flow_resolution.candidates:
                    raise BaziApplicationResolutionError(
                        "BAZI_APP_FLOW_CONTEXT_RESOLUTION_FAILED",
                        ";".join(flow_resolution.diagnostics)
                        or flow_resolution.status,
                    )
                flow_candidates.extend(flow_resolution.candidates)

            flow_tuple = tuple(flow_candidates)
            for flow_index, flow in enumerate(flow_tuple):
                for source_temporal_index in flow.source_temporal_candidate_indices:
                    if not 0 <= source_temporal_index < len(temporal_candidates):
                        raise BaziApplicationResolutionError(
                            "BAZI_APP_FLOW_TEMPORAL_SOURCE_INDEX_INVALID",
                            f"{flow_index}:{source_temporal_index}",
                        )
                    temporal = temporal_candidates[source_temporal_index]
                    flow_replay = validate_flow_context(
                        flow.context,
                        natal,
                        temporal,
                        base_request.natal_profile,
                        self.flow_engine.bazi_time,
                    )
                    if flow_replay.status != "PASS" or flow_replay != flow.integrity:
                        raise BaziApplicationResolutionError(
                            "BAZI_APP_FLOW_CONTEXT_REPLAY_FAILED",
                            f"{flow_index}:{source_temporal_index}",
                        )
                    expected_flow_hashes = flow_hash_bundle(
                        flow.context,
                        natal,
                        temporal,
                        base_request.natal_profile,
                    )
                    if expected_flow_hashes != flow.hashes:
                        raise BaziApplicationResolutionError(
                            "BAZI_APP_FLOW_CONTEXT_HASH_REPLAY_MISMATCH",
                            flow.hashes.fact_hash,
                        )

            structural_resolution = self.structural_engine.resolve_typed(
                BaziStructuralRequest(
                    natal_candidate=natal,
                    flow_candidates=flow_tuple,
                    structural_profile=bazi_structural_context_r1_profile(),
                )
            )
            if (
                structural_resolution.status == "FAILED"
                or not structural_resolution.candidates
            ):
                raise BaziApplicationResolutionError(
                    "BAZI_APP_FLOW_STRUCTURAL_RESOLUTION_FAILED",
                    ";".join(structural_resolution.diagnostics)
                    or structural_resolution.status,
                )
            structural_by_flow_index = {}
            for structural in structural_resolution.candidates:
                for source_flow_index in structural.source_flow_candidate_indices:
                    if source_flow_index in structural_by_flow_index:
                        raise BaziApplicationResolutionError(
                            "BAZI_APP_FLOW_STRUCTURAL_LINEAGE_DUPLICATE",
                            str(source_flow_index),
                        )
                    structural_by_flow_index[source_flow_index] = structural
            if set(structural_by_flow_index) != set(range(len(flow_tuple))):
                raise BaziApplicationResolutionError(
                    "BAZI_APP_FLOW_STRUCTURAL_LINEAGE_INCOMPLETE",
                    str(sorted(structural_by_flow_index)),
                )

            support_resolution = self.structural_support_engine.resolve_typed(
                BaziStructuralSupportRequest(
                    natal_candidate=natal,
                    flow_candidates=flow_tuple,
                    structural_candidates=structural_resolution.candidates,
                    support_profile=bazi_structural_support_foundation_r1_profile(),
                )
            )
            if support_resolution.status == "FAILED" or not support_resolution.candidates:
                raise BaziApplicationResolutionError(
                    "BAZI_APP_FLOW_STRUCTURAL_SUPPORT_RESOLUTION_FAILED",
                    ";".join(support_resolution.diagnostics)
                    or support_resolution.status,
                )
            support_by_flow_index = {}
            for support in support_resolution.candidates:
                if support.integrity.status != "PASS":
                    raise BaziApplicationResolutionError(
                        "BAZI_APP_FLOW_STRUCTURAL_SUPPORT_INTEGRITY_FAILED",
                        support.hashes.fact_hash,
                    )
                for source_flow_index in support.source_flow_candidate_indices:
                    if source_flow_index in support_by_flow_index:
                        raise BaziApplicationResolutionError(
                            "BAZI_APP_FLOW_STRUCTURAL_SUPPORT_LINEAGE_DUPLICATE",
                            str(source_flow_index),
                        )
                    support_by_flow_index[source_flow_index] = support
            if set(support_by_flow_index) != set(range(len(flow_tuple))):
                raise BaziApplicationResolutionError(
                    "BAZI_APP_FLOW_STRUCTURAL_SUPPORT_LINEAGE_INCOMPLETE",
                    str(sorted(support_by_flow_index)),
                )
            events.extend(support_resolution.events)

            daily_hourly_resolution = self.daily_hourly_engine.resolve(
                BaziDailyHourlyFlowRequest(
                    flow_candidates=flow_tuple,
                    target_coordinate_resolution=target_resolution,
                    target_coordinate_profile=target_profile,
                    calculation_profile=base_request.natal_profile,
                )
            )
            if (
                daily_hourly_resolution.status == "FAILED"
                or not daily_hourly_resolution.candidates
            ):
                raise BaziApplicationResolutionError(
                    "BAZI_APP_FLOW_DAILY_HOURLY_RESOLUTION_FAILED",
                    ";".join(daily_hourly_resolution.diagnostics)
                    or daily_hourly_resolution.status,
                )
            daily_hourly_replay = validate_daily_hourly_resolution(
                daily_hourly_resolution,
                flow_tuple,
                target_resolution,
                target_profile,
                base_request.natal_profile,
                self.daily_hourly_engine.bazi_time,
            )
            if daily_hourly_replay.status != "PASS":
                detail = ";".join(
                    f"{row.code}:{row.path}" for row in daily_hourly_replay.diagnostics
                )
                raise BaziApplicationResolutionError(
                    "BAZI_APP_FLOW_DAILY_HOURLY_REPLAY_FAILED", detail
                )

            for daily_hourly in daily_hourly_resolution.candidates:
                flow_index = daily_hourly.source_flow_candidate_index
                if not 0 <= flow_index < len(flow_tuple):
                    raise BaziApplicationResolutionError(
                        "BAZI_APP_FLOW_DAILY_HOURLY_FLOW_INDEX_INVALID",
                        str(flow_index),
                    )
                flow = flow_tuple[flow_index]
                structural = structural_by_flow_index[flow_index]
                structural_support = support_by_flow_index[flow_index]
                source_application_candidate_ids = tuple(
                    base_candidate_by_lineage[(natal_index, temporal_index)].candidate_id
                    for temporal_index in flow.source_temporal_candidate_indices
                )
                source_application_candidates = tuple(
                    base_candidate_by_lineage[(natal_index, temporal_index)]
                    for temporal_index in flow.source_temporal_candidate_indices
                )
                xiaoyun_views = tuple(
                    candidate.view["xiaoyun"]
                    for candidate in source_application_candidates
                )
                if not xiaoyun_views or any(
                    row != xiaoyun_views[0] for row in xiaoyun_views[1:]
                ):
                    raise BaziApplicationResolutionError(
                        "BAZI_APP_FLOW_XIAOYUN_LINEAGE_MISMATCH",
                        f"natal={natal_index};flow={flow_index}",
                    )
                view = self._build_view(
                    natal_index,
                    flow,
                    flow_index,
                    daily_hourly,
                    structural,
                    structural_support,
                    target_resolution,
                    source_application_candidate_ids,
                    xiaoyun_views[0],
                    base_request.birth.reported_local_datetime.year,
                    natal.chart.day_master_stem,
                )
                view_hash = object_sha256(
                    {"view_schema": FLOW_APPLICATION_VIEW_SCHEMA, "view": view}
                )
                candidate = BaziApplicationFlowCandidate(
                    candidate_id="",
                    natal_candidate_index=natal_index,
                    source_temporal_candidate_indices=(
                        flow.source_temporal_candidate_indices
                    ),
                    source_application_candidate_ids=source_application_candidate_ids,
                    source_flow_candidate_index=flow_index,
                    source_target_coordinate_candidate_index=(
                        daily_hourly.source_target_coordinate_candidate_index
                    ),
                    target_coordinate_candidate_id=(
                        daily_hourly.context.source_target_coordinate_candidate_id
                    ),
                    natal_fact_hash=flow.context.upstream_natal_fact_hash,
                    temporal_fact_hash=flow.context.upstream_temporal_fact_hash,
                    flow_fact_hash=flow.hashes.fact_hash,
                    flow_computation_hash=flow.hashes.computation_hash,
                    structural_fact_hash=structural.hashes.fact_hash,
                    structural_computation_hash=structural.hashes.computation_hash,
                    structural_support_fact_hash=(
                        structural_support.hashes.fact_hash
                    ),
                    structural_support_computation_hash=(
                        structural_support.hashes.computation_hash
                    ),
                    daily_hourly_fact_hash=daily_hourly.hashes.fact_hash,
                    daily_hourly_computation_hash=(
                        daily_hourly.hashes.computation_hash
                    ),
                    view_schema=FLOW_APPLICATION_VIEW_SCHEMA,
                    view=view,
                    view_hash=view_hash,
                )
                rows.append(
                    replace(candidate, candidate_id=application_flow_candidate_id(candidate))
                )

        candidates = tuple(rows)
        if not candidates:
            raise BaziApplicationResolutionError(
                "BAZI_APP_FLOW_NO_COMPATIBLE_CANDIDATES", "0"
            )

        unresolved_samples = tuple(
            json_value(row) for row in target_resolution.unresolved_samples
        )
        provisional = BaziApplicationFlowResolution(
            schema=self.schema,
            status="RESOLVED" if len(candidates) == 1 else "MULTI_CANDIDATE",
            base_application_bundle_hash=base_bundle.bundle_hash,
            base_application_source_fact_hash=base_bundle.source_fact_hash,
            application_profile_id=base_request.application_profile.profile_id,
            application_profile_version=base_request.application_profile.profile_version,
            natal_profile_id=base_request.natal_profile.profile_id,
            natal_profile_version=base_request.natal_profile.profile_version,
            temporal_profile_id=base_request.temporal_profile.profile_id,
            temporal_profile_version=base_request.temporal_profile.profile_version,
            target_coordinate_profile_id=target_profile.profile_id,
            target_coordinate_profile_version=target_profile.profile_version,
            dayun_count=base_request.dayun_count,
            target_input=request.target_input,
            target_coordinate_status=target_resolution.status,
            target_coordinate_effective_uncertainty_seconds_each_side=(
                target_resolution.effective_uncertainty_seconds_each_side
            ),
            target_coordinate_sample_count=target_resolution.sample_count,
            target_coordinate_ambiguous_sample_count=(
                target_resolution.ambiguous_sample_count
            ),
            target_coordinate_unresolved_samples=unresolved_samples,
            target_coordinate_fact_hash=target_resolution.hashes.fact_hash,
            target_coordinate_computation_hash=(
                target_resolution.hashes.computation_hash
            ),
            candidates=candidates,
            events=tuple(dict.fromkeys(events)),
            diagnostics=(),
            source_fact_hash="",
            view_hash="",
            bundle_hash="",
            integrity=BaziApplicationFlowIntegrityReport(
                status="PENDING", diagnostics=()
            ),
        )
        provisional = replace(
            provisional,
            source_fact_hash=application_flow_source_fact_hash(provisional),
        )
        provisional = replace(
            provisional,
            view_hash=application_flow_view_hash(provisional),
        )
        provisional = replace(
            provisional,
            bundle_hash=application_flow_bundle_hash(provisional),
        )
        report = validate_application_flow_resolution(provisional)
        if report.status != "PASS":
            raise BaziApplicationResolutionError(
                "BAZI_APP_FLOW_APPLICATION_INTEGRITY_FAILED",
                ";".join(report.diagnostics),
            )
        return base_bundle, replace(provisional, integrity=report)

    def resolve(self, request: BaziApplicationFlowRequest) -> BaziApplicationFlowResolution:
        return self._resolve_pair(request)[1]

    def resolve_with_base(
        self, request: BaziApplicationFlowRequest
    ) -> tuple[BaziApplicationResolution, BaziApplicationFlowResolution]:
        return self._resolve_pair(request)

    def export(self, request: BaziApplicationFlowRequest) -> dict[str, Any]:
        return json_value(self.resolve(request))
