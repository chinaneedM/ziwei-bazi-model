from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

from fortune_training.bazi_chart import (
    BaziChartFoundation,
    BaziChartRequest,
    natal_hash_bundle,
    validate_natal_state,
)
from fortune_training.bazi_temporal import (
    BaziTemporalEngine,
    BaziTemporalRequest,
    temporal_hash_bundle,
    validate_dayun_state,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .integrity import validate_application_resolution
from .models import (
    BaziApplicationCandidate,
    BaziApplicationIntegrityReport,
    BaziApplicationLegalTimeRealization,
    BaziApplicationRequest,
    BaziApplicationResolution,
    BaziApplicationTimeCalendarProvenance,
    BaziApplicationUnresolvedTimeSample,
)


class BaziApplicationResolutionError(ValueError):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


class BaziChartService:
    schema = "BAZI-LOCAL-APPLICATION-RESOLUTION-V1"

    def __init__(
        self,
        chart_foundation: BaziChartFoundation,
        temporal_engine: BaziTemporalEngine | None = None,
    ) -> None:
        self.chart_foundation = chart_foundation
        self.temporal_engine = temporal_engine or BaziTemporalEngine()

    @classmethod
    def from_repository(cls, repository_root: Path) -> "BaziChartService":
        return cls(BaziChartFoundation.from_repository(repository_root))

    @staticmethod
    def _validate_natal_candidate(candidate, profile) -> None:
        report = validate_natal_state(candidate.chart)
        if report.status != "PASS":
            detail = ";".join(f"{row.code}:{row.path}" for row in report.diagnostics)
            raise BaziApplicationResolutionError("BAZI_APP_NATAL_REPLAY_FAILED", detail)
        hashes = natal_hash_bundle(candidate.chart, profile)
        if hashes != candidate.hashes:
            raise BaziApplicationResolutionError(
                "BAZI_APP_NATAL_HASH_REPLAY_MISMATCH",
                candidate.hashes.fact_hash,
            )

    @staticmethod
    def _validate_temporal_candidate(temporal, natal, profile) -> None:
        report = validate_dayun_state(temporal.state, natal, profile)
        if report.status != "PASS":
            detail = ";".join(f"{row.code}:{row.path}" for row in report.diagnostics)
            raise BaziApplicationResolutionError("BAZI_APP_TEMPORAL_REPLAY_FAILED", detail)
        hashes = temporal_hash_bundle(temporal.state, profile)
        if hashes != temporal.hashes:
            raise BaziApplicationResolutionError(
                "BAZI_APP_TEMPORAL_HASH_REPLAY_MISMATCH",
                temporal.hashes.fact_hash,
            )

    @staticmethod
    def _build_time_calendar_provenance(
        time_result: dict[str, Any],
    ) -> BaziApplicationTimeCalendarProvenance:
        interval = time_result.get("input_interval", {})

        legal_realizations: list[BaziApplicationLegalTimeRealization] = []
        for branch_index, row in enumerate(time_result.get("branches", [])):
            civil = row.get("civil_time", {})
            selected = row.get("selected_civil_candidate", {})
            legal_realizations.append(
                BaziApplicationLegalTimeRealization(
                    source_time_branch_index=branch_index,
                    sample_reported_local_datetime=str(
                        row.get("sample_reported_local_datetime", "")
                    ),
                    civil_status=str(civil.get("status", "UNKNOWN")),
                    timezone_id=str(civil.get("timezone_id", "")),
                    tzdb_version=str(civil.get("tzdb_version", "")),
                    historical_confidence=str(
                        civil.get("historical_confidence", "")
                    ),
                    warnings=tuple(str(item) for item in civil.get("warnings", [])),
                    birth_utc=str(selected.get("utc_instant", "")),
                    fold=int(selected.get("fold", 0)),
                    utc_offset_seconds=int(selected.get("utc_offset_seconds", 0)),
                    daylight_saving_seconds=int(
                        selected.get("daylight_saving_seconds", 0)
                    ),
                    timezone_abbreviation=str(
                        selected.get("timezone_abbreviation", "")
                    ),
                )
            )

        unresolved_samples: list[BaziApplicationUnresolvedTimeSample] = []
        for row in time_result.get("unresolved_samples", []):
            civil = row.get("civil_time", {})
            unresolved_samples.append(
                BaziApplicationUnresolvedTimeSample(
                    sample_reported_local_datetime=str(
                        row.get("sample_reported_local_datetime", "")
                    ),
                    civil_status=str(civil.get("status", "UNKNOWN")),
                    timezone_id=str(civil.get("timezone_id", "")),
                    tzdb_version=str(civil.get("tzdb_version", "")),
                    historical_confidence=str(
                        civil.get("historical_confidence", "")
                    ),
                    warnings=tuple(str(item) for item in civil.get("warnings", [])),
                )
            )
        return BaziApplicationTimeCalendarProvenance(
            status=str(time_result.get("status", "UNKNOWN")),
            effective_uncertainty_seconds_each_side=int(
                interval.get("uncertainty_seconds_each_side", 0)
            ),
            sample_count=int(interval.get("sample_count", 0)),
            ambiguous_sample_count=int(interval.get("ambiguous_sample_count", 0)),
            legal_realization_count=len(legal_realizations),
            legal_realizations=tuple(legal_realizations),
            unresolved_sample_count=len(unresolved_samples),
            unresolved_samples=tuple(unresolved_samples),
        )

    @staticmethod
    def _build_view(request: BaziApplicationRequest, natal, temporal) -> dict[str, Any]:
        chart = natal.chart
        stem_by_id = {row.instance_id: row for row in chart.stems}
        branch_by_id = {row.instance_id: row for row in chart.branches}
        ten_god_by_target = {row.target_instance_id: row for row in chart.ten_gods}
        hidden_by_branch: dict[str, list[Any]] = {}
        for row in chart.hidden_stems:
            hidden_by_branch.setdefault(row.branch_instance_id, []).append(row)
        for rows in hidden_by_branch.values():
            rows.sort(key=lambda item: item.registry_ordinal)

        pillars: list[dict[str, Any]] = []
        for pillar in chart.pillars:
            stem = stem_by_id[pillar.stem_instance_id]
            branch = branch_by_id[pillar.branch_instance_id]
            visible_ten_god = ten_god_by_target[stem.instance_id]
            hidden = []
            for hidden_stem in hidden_by_branch.get(branch.instance_id, []):
                hidden_ten_god = ten_god_by_target[hidden_stem.instance_id]
                hidden.append(
                    {
                        "instance_id": hidden_stem.instance_id,
                        "stem": hidden_stem.stem,
                        "element": hidden_stem.element,
                        "registry_ordinal": hidden_stem.registry_ordinal,
                        "ten_god": hidden_ten_god.display_name,
                        "ten_god_semantic_role_id": hidden_ten_god.semantic_role_id,
                    }
                )
            pillars.append(
                {
                    "position": pillar.position,
                    "ganzhi": pillar.ganzhi,
                    "sexagenary_index": pillar.sexagenary_index,
                    "stem": stem.stem,
                    "stem_element": stem.element,
                    "stem_polarity": stem.polarity,
                    "visible_ten_god": visible_ten_god.display_name,
                    "visible_ten_god_semantic_role_id": visible_ten_god.semantic_role_id,
                    "branch": branch.branch,
                    "branch_element_affiliation": branch.element_affiliation,
                    "hidden_stems": hidden,
                }
            )

        seed_by_id = {seed.seed_id: seed for seed in natal.temporal_seeds}
        time_provenance = []
        for seed_id in temporal.source_temporal_seed_ids:
            seed = seed_by_id.get(seed_id)
            if seed is None:
                raise BaziApplicationResolutionError(
                    "BAZI_APP_TEMPORAL_SEED_LINEAGE_MISSING",
                    seed_id,
                )
            time_provenance.append(
                {
                    "seed_id": seed.seed_id,
                    "source_time_branch_index": seed.source_time_branch_index,
                    "sample_reported_local_datetime": json_value(
                        seed.sample_reported_local_datetime
                    ),
                    "birth_utc": json_value(seed.birth_utc),
                    "local_apparent_solar_datetime": json_value(
                        seed.local_apparent_solar_datetime
                    ),
                    "previous_jie_name": seed.previous_jie_name,
                    "previous_jie_utc": json_value(seed.previous_jie_utc),
                    "next_jie_name": seed.next_jie_name,
                    "next_jie_utc": json_value(seed.next_jie_utc),
                    "input_uncertainty_seconds_each_side": (
                        seed.input_uncertainty_seconds_each_side
                    ),
                }
            )

        state = temporal.state
        symbolic = state.jiaoyun.symbolic_age
        return {
            "birth": json_value(request.birth),
            "time_provenance": time_provenance,
            "pillars": pillars,
            "day_master_stem": chart.day_master_stem,
            "dayun": {
                "direction": state.direction.direction,
                "year_stem": state.direction.year_stem,
                "year_stem_polarity": state.direction.year_stem_polarity,
                "sex": state.direction.sex.value,
                "jiaoyun": {
                    "anchor_kind": state.jiaoyun.anchor_kind,
                    "anchor_jie_name": state.jiaoyun.anchor_jie_name,
                    "anchor_jie_utc": json_value(state.jiaoyun.anchor_jie_utc),
                    "birth_utc": json_value(state.jiaoyun.birth_utc),
                    "raw_interval_microseconds": state.jiaoyun.raw_interval_microseconds,
                    "symbolic_age": {
                        "years_360": symbolic.years_360,
                        "months_30": symbolic.months_30,
                        "days": symbolic.days,
                        "residual_microseconds": symbolic.residual_microseconds,
                    },
                    "first_transition_utc": json_value(
                        state.jiaoyun.first_transition_utc
                    ),
                    "interval_coordinate_policy": (
                        state.jiaoyun.interval_coordinate_policy
                    ),
                    "calendar_realization_rule_set": (
                        state.jiaoyun.calendar_realization_rule_set
                    ),
                },
                "frames": [
                    {
                        "index": frame.index,
                        "ganzhi": frame.ganzhi,
                        "sexagenary_index": frame.sexagenary_index,
                        "start_utc": json_value(frame.start_utc),
                        "end_utc": json_value(frame.end_utc),
                    }
                    for frame in state.dayun_frames
                ],
            },
            "integrity": {
                "natal": natal.integrity.status,
                "temporal": temporal.integrity.status,
            },
            "source_hashes": {
                "natal_fact_hash": natal.hashes.fact_hash,
                "natal_computation_hash": natal.hashes.computation_hash,
                "temporal_fact_hash": temporal.hashes.fact_hash,
                "temporal_computation_hash": temporal.hashes.computation_hash,
            },
        }

    def resolve(self, request: BaziApplicationRequest) -> BaziApplicationResolution:
        app_profile = request.application_profile.validate()
        if request.dayun_count < 1 or request.dayun_count > 20:
            raise BaziApplicationResolutionError(
                "BAZI_APP_INVALID_DAYUN_COUNT",
                str(request.dayun_count),
            )

        natal_resolution = self.chart_foundation.resolve_typed(
            BaziChartRequest(request.birth, request.natal_profile)
        )
        if natal_resolution.status == "FAILED" or not natal_resolution.candidates:
            raise BaziApplicationResolutionError(
                "BAZI_APP_NATAL_RESOLUTION_FAILED",
                ";".join(natal_resolution.diagnostics) or natal_resolution.status,
            )
        time_calendar_provenance = self._build_time_calendar_provenance(
            natal_resolution.time_calendar
        )

        rows: list[BaziApplicationCandidate] = []
        events: list[str] = list(natal_resolution.events)
        for natal_index, natal in enumerate(natal_resolution.candidates):
            self._validate_natal_candidate(natal, request.natal_profile)
            temporal_resolution = self.temporal_engine.resolve_typed(
                BaziTemporalRequest(
                    candidate=natal,
                    sex=request.sex,
                    profile=request.temporal_profile,
                    dayun_count=request.dayun_count,
                )
            )
            if temporal_resolution.status == "FAILED" or not temporal_resolution.candidates:
                raise BaziApplicationResolutionError(
                    "BAZI_APP_TEMPORAL_RESOLUTION_FAILED",
                    ";".join(temporal_resolution.diagnostics)
                    or temporal_resolution.status,
                )
            events.extend(temporal_resolution.events)
            for temporal_index, temporal in enumerate(temporal_resolution.candidates):
                self._validate_temporal_candidate(
                    temporal,
                    natal,
                    request.temporal_profile,
                )
                view = self._build_view(request, natal, temporal)
                view_hash = object_sha256(
                    {
                        "view_schema": app_profile.view_schema,
                        "view": view,
                    }
                )
                candidate_id = "BAZI-APPLICATION-CANDIDATE:" + object_sha256(
                    {
                        "natal_fact_hash": natal.hashes.fact_hash,
                        "natal_computation_hash": natal.hashes.computation_hash,
                        "temporal_fact_hash": temporal.hashes.fact_hash,
                        "temporal_computation_hash": temporal.hashes.computation_hash,
                        "view_hash": view_hash,
                    }
                )
                rows.append(
                    BaziApplicationCandidate(
                        candidate_id=candidate_id,
                        natal_candidate_index=natal_index,
                        temporal_candidate_index=temporal_index,
                        natal_fact_hash=natal.hashes.fact_hash,
                        natal_computation_hash=natal.hashes.computation_hash,
                        temporal_fact_hash=temporal.hashes.fact_hash,
                        temporal_computation_hash=temporal.hashes.computation_hash,
                        source_temporal_seed_ids=temporal.source_temporal_seed_ids,
                        view_schema=app_profile.view_schema,
                        view=view,
                        view_hash=view_hash,
                    )
                )

        candidates = tuple(rows)
        source_fact_hash = object_sha256(
            {
                "birth": json_value(request.birth),
                "sex": request.sex.value,
                "time_calendar_provenance": json_value(time_calendar_provenance),
                "natal_fact_hashes": [row.natal_fact_hash for row in candidates],
                "temporal_fact_hashes": [row.temporal_fact_hash for row in candidates],
            }
        )
        aggregate_view_hash = object_sha256(
            {
                "view_schema": app_profile.view_schema,
                "candidate_view_hashes": [row.view_hash for row in candidates],
            }
        )
        bundle_hash = object_sha256(
            {
                "source_fact_hash": source_fact_hash,
                "view_hash": aggregate_view_hash,
                "application_profile": json_value(app_profile),
                "natal_profile": json_value(request.natal_profile),
                "temporal_profile": json_value(request.temporal_profile),
                "dayun_count": request.dayun_count,
                "candidate_ids": [row.candidate_id for row in candidates],
            }
        )

        unique_events = tuple(dict.fromkeys(events))
        if len(candidates) > 1:
            status = "MULTI_CANDIDATE"
        elif unique_events:
            status = "RESOLVED_WITH_TIME_UNCERTAINTY"
        else:
            status = "RESOLVED"
        resolution = BaziApplicationResolution(
            schema=self.schema,
            status=status,
            birth=request.birth,
            application_profile=app_profile,
            natal_profile=request.natal_profile,
            temporal_profile=request.temporal_profile,
            sex=request.sex,
            dayun_count=request.dayun_count,
            time_calendar_provenance=time_calendar_provenance,
            candidates=candidates,
            events=unique_events,
            diagnostics=(),
            source_fact_hash=source_fact_hash,
            view_hash=aggregate_view_hash,
            bundle_hash=bundle_hash,
            integrity=BaziApplicationIntegrityReport(status="PENDING", diagnostics=()),
        )
        report = validate_application_resolution(resolution)
        if report.status != "PASS":
            raise BaziApplicationResolutionError(
                "BAZI_APP_BUNDLE_INTEGRITY_FAILED",
                ";".join(report.diagnostics),
            )
        return replace(resolution, integrity=report)

    def export(self, request: BaziApplicationRequest) -> dict[str, Any]:
        return json_value(self.resolve(request))
