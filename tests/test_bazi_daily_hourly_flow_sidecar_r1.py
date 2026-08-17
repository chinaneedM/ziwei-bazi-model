from __future__ import annotations

import json
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jsonschema

from fortune_training.bazi_chart import (
    BaziChartFoundation,
    BaziChartRequest,
    bazi_foundation_v1_profile,
    bazi_foundation_zi_start_23_r1_profile,
)
from fortune_training.bazi_daily_hourly_flow import (
    BaziDailyHourlyFlowEngine,
    BaziDailyHourlyFlowRequest,
    validate_daily_hourly_context,
    validate_daily_hourly_resolution,
)
from fortune_training.bazi_daily_hourly_flow.engine import _daily_interval, _hourly_interval
from fortune_training.bazi_flow import BaziFlowEngine, BaziFlowRequest
from fortune_training.bazi_target_temporal import (
    TargetTemporalCoordinateFoundation,
    TargetTemporalInput,
    bazi_target_temporal_coordinate_r1_profile,
)
from fortune_training.bazi_temporal import (
    BaziSex,
    BaziTemporalEngine,
    BaziTemporalRequest,
    bazi_temporal_v1_continuous_profile,
)
from fortune_training.calendar_foundation import BirthInput
from fortune_training.calendar_foundation.models import json_value


ROOT = Path(__file__).resolve().parents[1]


class BaziDailyHourlyFlowSidecarR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.chart_engine = BaziChartFoundation.from_repository(ROOT)
        registry = cls.chart_engine.time_calendar.policy_registry
        cls.midnight_profile = bazi_foundation_v1_profile(registry)
        cls.zi_profile = bazi_foundation_zi_start_23_r1_profile(registry)
        cls.temporal_engine = BaziTemporalEngine()
        cls.flow_engine = BaziFlowEngine(cls.chart_engine.time_calendar.bazi)
        cls.target_foundation = TargetTemporalCoordinateFoundation()
        cls.target_profile = bazi_target_temporal_coordinate_r1_profile()
        cls.sidecar = BaziDailyHourlyFlowEngine(cls.chart_engine.time_calendar.bazi)
        cls.schema = json.loads(
            (ROOT / "schemas" / "bazi-daily-hourly-flow-sidecar-r1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        cls.midnight_natal, cls.midnight_temporal = cls._natal_temporal(
            cls.midnight_profile,
            datetime(2025, 2, 7, 10, 10),
            place="Beijing",
            latitude=39.9042,
            longitude=116.4074,
            timezone_id="Asia/Shanghai",
        )
        cls.zi_natal, cls.zi_temporal = cls._natal_temporal(
            cls.zi_profile,
            datetime(2025, 2, 7, 10, 10),
            place="Beijing",
            latitude=39.9042,
            longitude=116.4074,
            timezone_id="Asia/Shanghai",
        )

    @classmethod
    def _natal_temporal(
        cls,
        profile,
        local: datetime,
        *,
        place: str,
        latitude: float,
        longitude: float,
        timezone_id: str,
    ):
        natal_resolution = cls.chart_engine.resolve_typed(
            BaziChartRequest(
                BirthInput(
                    reported_local_datetime=local,
                    birth_place=place,
                    latitude=latitude,
                    longitude=longitude,
                    timezone_id=timezone_id,
                ),
                profile,
            )
        )
        if len(natal_resolution.candidates) != 1:
            raise RuntimeError(f"fixture requires one Natal candidate: {natal_resolution.status}")
        natal = natal_resolution.candidates[0]
        temporal = cls.temporal_engine.resolve_typed(
            BaziTemporalRequest(
                natal,
                BaziSex.MALE,
                bazi_temporal_v1_continuous_profile(),
                dayun_count=6,
            )
        )
        if not temporal.candidates:
            raise RuntimeError(f"fixture requires temporal candidates: {temporal.status}")
        return natal, temporal

    @classmethod
    def _target(
        cls,
        local: datetime,
        *,
        place: str = "Greenwich",
        latitude: float = 51.4769,
        longitude: float = 0.0,
        timezone_id: str = "Etc/UTC",
        uncertainty_seconds: int = 0,
    ):
        return cls.target_foundation.resolve(
            TargetTemporalInput(
                reported_local_datetime=local,
                target_place=place,
                latitude=latitude,
                longitude=longitude,
                timezone_id=timezone_id,
                uncertainty_seconds=uncertainty_seconds,
            ),
            cls.target_profile,
        )

    @classmethod
    def _flow_candidate(cls, target_utc, *, natal=None, temporal=None, profile=None):
        natal = natal or cls.midnight_natal
        temporal = temporal or cls.midnight_temporal
        profile = profile or cls.midnight_profile
        result = cls.flow_engine.resolve_typed(
            BaziFlowRequest(
                natal_candidate=natal,
                temporal_candidates=temporal.candidates,
                target_utc=target_utc,
                calculation_profile=profile,
            )
        )
        if not result.candidates:
            raise RuntimeError(f"fixture requires Flow candidate: {result.status} {result.diagnostics}")
        return result.candidates[0]

    @classmethod
    def _flows_for_target(cls, target_resolution, *, natal=None, temporal=None, profile=None):
        rows = []
        seen = set()
        for target in target_resolution.candidates:
            key = target.target_utc.astimezone(timezone.utc)
            if key in seen:
                continue
            seen.add(key)
            rows.append(
                cls._flow_candidate(
                    key,
                    natal=natal,
                    temporal=temporal,
                    profile=profile,
                )
            )
        return tuple(rows)

    @classmethod
    def _resolve_sidecar(cls, target_resolution, *, natal=None, temporal=None, profile=None, flows=None):
        profile = profile or cls.midnight_profile
        flows = flows or cls._flows_for_target(
            target_resolution,
            natal=natal,
            temporal=temporal,
            profile=profile,
        )
        return cls.sidecar.resolve(
            BaziDailyHourlyFlowRequest(
                flow_candidates=flows,
                target_coordinate_resolution=target_resolution,
                target_coordinate_profile=cls.target_profile,
                calculation_profile=profile,
            )
        ), flows

    def test_ordinary_target_is_deterministic_and_schema_valid(self) -> None:
        target = self._target(datetime(2026, 6, 1, 12, 0))
        first, flows = self._resolve_sidecar(target)
        second, _ = self._resolve_sidecar(target, flows=flows)
        self.assertEqual("RESOLVED", first.status)
        self.assertEqual(first, second)
        self.assertEqual("PASS", first.candidates[0].integrity.status)
        self.assertEqual(first.candidates[0].hashes, second.candidates[0].hashes)
        self.assertEqual(
            "PASS",
            validate_daily_hourly_resolution(
                first,
                flows,
                target,
                self.target_profile,
                self.midnight_profile,
                self.sidecar.bazi_time,
            ).status,
        )
        jsonschema.Draft202012Validator(self.schema).validate(json_value(first))

    def test_23_las_profile_split_preserves_released_policy_difference(self) -> None:
        target = self._target(datetime(2026, 1, 15, 23, 30))
        self.assertEqual(23, target.candidates[0].local_apparent_solar_datetime.hour)
        midnight, _ = self._resolve_sidecar(target)
        zi, _ = self._resolve_sidecar(
            target,
            natal=self.zi_natal,
            temporal=self.zi_temporal,
            profile=self.zi_profile,
        )
        m = midnight.candidates[0].context
        z = zi.candidates[0].context
        self.assertEqual("MIDNIGHT", m.day_boundary_policy)
        self.assertEqual("ZI_START_23", z.day_boundary_policy)
        self.assertEqual("CLASSICAL_CONTINUOUS", m.late_zi_hour_stem_policy)
        self.assertEqual("ZI_START_ROLLOVER", z.late_zi_hour_stem_policy)
        self.assertNotEqual(m.daily_frame.effective_day_date, z.daily_frame.effective_day_date)
        self.assertNotEqual(midnight.candidates[0].hashes, zi.candidates[0].hashes)

    def test_midnight_boundary_and_two_hour_branch_boundary_are_half_open(self) -> None:
        before_midnight = datetime(2026, 6, 1, 23, 59, 59, 999999)
        at_midnight = datetime(2026, 6, 2, 0, 0)
        before_start, before_end = _daily_interval(before_midnight, before_midnight.date(), "MIDNIGHT")
        exact_start, exact_end = _daily_interval(at_midnight, at_midnight.date(), "MIDNIGHT")
        self.assertLess(before_midnight, before_end)
        self.assertEqual(before_end, exact_start)
        self.assertLess(at_midnight, exact_end)

        before_branch = datetime(2026, 6, 1, 2, 59, 59, 999999)
        at_branch = datetime(2026, 6, 1, 3, 0)
        old_start, old_end = _hourly_interval(before_branch)
        new_start, new_end = _hourly_interval(at_branch)
        self.assertEqual(datetime(2026, 6, 1, 1, 0), old_start)
        self.assertEqual(datetime(2026, 6, 1, 3, 0), old_end)
        self.assertEqual(old_end, new_start)
        self.assertEqual(datetime(2026, 6, 1, 5, 0), new_end)

    def test_same_utc_different_target_longitude_changes_las_hourly_not_flow_annual_monthly(self) -> None:
        utc_wall = datetime(2026, 6, 1, 0, 30)
        west = self._target(
            utc_wall,
            place="UTC meridian",
            latitude=0.0,
            longitude=0.0,
            timezone_id="Etc/UTC",
        )
        east = self._target(
            utc_wall,
            place="Explicit east longitude",
            latitude=0.0,
            longitude=120.0,
            timezone_id="Etc/UTC",
        )
        self.assertEqual(west.candidates[0].target_utc, east.candidates[0].target_utc)
        self.assertNotEqual(
            west.candidates[0].local_apparent_solar_datetime,
            east.candidates[0].local_apparent_solar_datetime,
        )
        shared_flow = self._flow_candidate(west.candidates[0].target_utc)
        west_sidecar, _ = self._resolve_sidecar(west, flows=(shared_flow,))
        east_sidecar, _ = self._resolve_sidecar(east, flows=(shared_flow,))
        self.assertEqual(
            west_sidecar.candidates[0].context.source_flow_fact_hash,
            east_sidecar.candidates[0].context.source_flow_fact_hash,
        )
        self.assertNotEqual(
            west_sidecar.candidates[0].context.hourly_frame.ganzhi,
            east_sidecar.candidates[0].context.hourly_frame.ganzhi,
        )
        self.assertNotEqual(
            west_sidecar.candidates[0].hashes.fact_hash,
            east_sidecar.candidates[0].hashes.fact_hash,
        )

    def test_dst_fold_preserves_both_target_realizations_and_lineages(self) -> None:
        target = self._target(
            datetime(2026, 11, 1, 1, 30),
            place="New York",
            latitude=40.7128,
            longitude=-74.0060,
            timezone_id="America/New_York",
        )
        self.assertEqual(2, len(target.candidates))
        result, flows = self._resolve_sidecar(target)
        self.assertEqual("MULTI_CANDIDATE", result.status)
        self.assertEqual(2, len(result.candidates))
        self.assertEqual({0, 1}, {row.source_target_coordinate_candidate_index for row in result.candidates})
        self.assertEqual(2, len({row.context.target_utc for row in result.candidates}))
        self.assertEqual(
            "PASS",
            validate_daily_hourly_resolution(
                result,
                flows,
                target,
                self.target_profile,
                self.midnight_profile,
                self.sidecar.bazi_time,
            ).status,
        )

    def test_uncertainty_preserves_candidate_multiplicity_across_hourly_boundaries(self) -> None:
        target = self._target(
            datetime(2026, 6, 1, 12, 0),
            uncertainty_seconds=7200,
        )
        self.assertEqual(5, len(target.candidates))
        result, _ = self._resolve_sidecar(target)
        self.assertEqual("MULTI_CANDIDATE", result.status)
        self.assertEqual(5, len(result.candidates))
        self.assertGreater(
            len({row.context.hourly_frame.frame_id for row in result.candidates}),
            1,
        )
        self.assertEqual(
            list(range(5)),
            [row.source_target_coordinate_candidate_index for row in result.candidates],
        )

    def test_explicit_target_coordinate_not_birth_longitude_controls_visible_daily_hourly(self) -> None:
        alternate_natal, alternate_temporal = self._natal_temporal(
            self.midnight_profile,
            datetime(2025, 2, 7, 2, 10),
            place="Greenwich birth",
            latitude=51.4769,
            longitude=0.0,
            timezone_id="Etc/UTC",
        )
        target = self._target(
            datetime(2026, 6, 1, 18, 0),
            place="Explicit target",
            latitude=0.0,
            longitude=90.0,
            timezone_id="Etc/UTC",
        )
        beijing_birth, _ = self._resolve_sidecar(target)
        greenwich_birth, _ = self._resolve_sidecar(
            target,
            natal=alternate_natal,
            temporal=alternate_temporal,
            profile=self.midnight_profile,
        )
        left = beijing_birth.candidates[0].context
        right = greenwich_birth.candidates[0].context
        self.assertEqual(left.target_local_apparent_solar_datetime, right.target_local_apparent_solar_datetime)
        self.assertEqual(left.target_longitude, right.target_longitude)
        self.assertEqual(left.daily_frame.ganzhi, right.daily_frame.ganzhi)
        self.assertEqual(left.hourly_frame.ganzhi, right.hourly_frame.ganzhi)
        self.assertNotEqual(left.upstream_natal_fact_hash, right.upstream_natal_fact_hash)

    def test_flow_target_utc_mismatch_fails_closed(self) -> None:
        target = self._target(datetime(2026, 6, 1, 12, 0))
        wrong_flow = self._flow_candidate(target.candidates[0].target_utc + timedelta(hours=1))
        result, _ = self._resolve_sidecar(target, flows=(wrong_flow,))
        self.assertEqual("FAILED", result.status)
        self.assertEqual((), result.candidates)
        self.assertTrue(result.diagnostics[0].startswith("NO_COMPATIBLE_FLOW_FOR_TARGET:"))

    def test_upstream_hashes_remain_byte_stable_after_sidecar_projection(self) -> None:
        target = self._target(datetime(2026, 6, 1, 12, 0))
        flow = self._flow_candidate(target.candidates[0].target_utc)
        natal_hashes = self.midnight_natal.hashes
        temporal_hashes = tuple(row.hashes for row in self.midnight_temporal.candidates)
        flow_hashes = flow.hashes
        target_hashes = target.hashes
        result, _ = self._resolve_sidecar(target, flows=(flow,))
        self.assertEqual("RESOLVED", result.status)
        self.assertEqual(natal_hashes, self.midnight_natal.hashes)
        self.assertEqual(temporal_hashes, tuple(row.hashes for row in self.midnight_temporal.candidates))
        self.assertEqual(flow_hashes, flow.hashes)
        self.assertEqual(target_hashes, target.hashes)

    def test_same_visible_frames_under_profiles_keep_distinct_computation_lineage(self) -> None:
        target = self._target(datetime(2026, 6, 1, 12, 0))
        midnight, _ = self._resolve_sidecar(target)
        zi, _ = self._resolve_sidecar(
            target,
            natal=self.zi_natal,
            temporal=self.zi_temporal,
            profile=self.zi_profile,
        )
        m = midnight.candidates[0]
        z = zi.candidates[0]
        self.assertEqual(m.context.daily_frame.ganzhi, z.context.daily_frame.ganzhi)
        self.assertEqual(m.context.hourly_frame.ganzhi, z.context.hourly_frame.ganzhi)
        self.assertNotEqual(m.hashes.computation_hash, z.hashes.computation_hash)
        self.assertNotEqual(m.context.natal_profile_id, z.context.natal_profile_id)

    def test_tampered_frame_binding_hash_or_source_index_fails_replay(self) -> None:
        target = self._target(datetime(2026, 6, 1, 12, 0))
        result, flows = self._resolve_sidecar(target)
        row = result.candidates[0]
        tampered_context = replace(
            row.context,
            daily_frame=replace(row.context.daily_frame, ganzhi="甲子"),
        )
        report = validate_daily_hourly_context(
            tampered_context,
            flows[0],
            target,
            self.target_profile,
            self.midnight_profile,
            self.sidecar.bazi_time,
        )
        self.assertEqual("FAIL", report.status)
        self.assertIn("DAILY_GANZHI_REPLAY_MISMATCH", {item.code for item in report.diagnostics})

        tampered_row = replace(row, source_flow_candidate_index=99)
        tampered_resolution = replace(result, candidates=(tampered_row,))
        resolution_report = validate_daily_hourly_resolution(
            tampered_resolution,
            flows,
            target,
            self.target_profile,
            self.midnight_profile,
            self.sidecar.bazi_time,
        )
        self.assertEqual("FAIL", resolution_report.status)
        self.assertIn(
            "OUTER_FLOW_INDEX_LINEAGE_MISMATCH",
            {item.code for item in resolution_report.diagnostics},
        )

        wrong_hash = replace(row.hashes, fact_hash="0" * 64)
        hash_tampered = replace(result, candidates=(replace(row, hashes=wrong_hash),))
        hash_report = validate_daily_hourly_resolution(
            hash_tampered,
            flows,
            target,
            self.target_profile,
            self.midnight_profile,
            self.sidecar.bazi_time,
        )
        self.assertIn("STORED_HASH_REPLAY_MISMATCH", {item.code for item in hash_report.diagnostics})


if __name__ == "__main__":
    unittest.main()
