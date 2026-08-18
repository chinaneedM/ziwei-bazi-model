from __future__ import annotations

import copy
import json
import unittest
from dataclasses import fields, replace
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

from fortune_training.bazi_target_temporal import (
    TargetTemporalCoordinateFoundation,
    TargetTemporalInput,
    bazi_target_temporal_coordinate_r1_profile,
)
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimePrecision
from fortune_training.calendar_foundation.models import json_value
from fortune_training.combined_chart_application.shared_time_integrity import (
    shared_selector_candidate_hash,
    shared_selector_hash_bundle,
    validate_shared_ziwei_selector_projection,
)
from fortune_training.combined_chart_application.shared_time_models import (
    SharedZiweiSelectorProjectionCandidate,
    SharedZiweiSelectorProjectionResolution,
)
from fortune_training.combined_chart_application.shared_time_replay import (
    validate_shared_ziwei_selector_full_replay,
)
from fortune_training.combined_chart_application.shared_time_service import (
    SharedZiweiSelectorProjectionError,
    SharedZiweiSelectorProjectionService,
)
from fortune_training.ziwei_application import (
    ApplicationBirthRequest,
    ZiweiChartService,
    ziwei_application_default_presentation_profile,
)
from fortune_training.ziwei_chart import Sex, ziwei_chart_engine_v1_profile


ROOT = Path(__file__).resolve().parents[1]


class SharedTargetZiweiSelectorProjectionR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.calculation_profile = ziwei_chart_engine_v1_profile(registry)
        cls.application_service = ZiweiChartService.from_repository(ROOT)
        cls.birth = BirthInput(
            reported_local_datetime=datetime(1994, 5, 17, 14, 30),
            birth_place="Beijing",
            latitude=39.9042,
            longitude=116.4074,
            timezone_id="Asia/Shanghai",
        )
        cls.application_request = ApplicationBirthRequest(
            birth=cls.birth,
            sex=Sex.MALE,
            calculation_profile=cls.calculation_profile,
            presentation_profile=ziwei_application_default_presentation_profile(),
            daxian_count=12,
            max_nominal_age=120,
        )
        cls.ziwei_bundle = cls.application_service.resolve(cls.application_request)
        cls.target_foundation = TargetTemporalCoordinateFoundation()
        cls.target_profile = bazi_target_temporal_coordinate_r1_profile()
        cls.service = SharedZiweiSelectorProjectionService()
        cls.schema = json.loads(
            (ROOT / "schemas" / "shared-ziwei-selector-projection-r1.schema.json").read_text(
                encoding="utf-8"
            )
        )

    @classmethod
    def _target(
        cls,
        wall: datetime,
        *,
        place: str = "Beijing",
        latitude: float = 39.9042,
        longitude: float = 116.4074,
        timezone_id: str = "Asia/Shanghai",
        precision: TimePrecision = TimePrecision.EXACT_SECOND,
        uncertainty_seconds: int = 0,
    ):
        target_input = TargetTemporalInput(
            reported_local_datetime=wall,
            target_place=place,
            latitude=latitude,
            longitude=longitude,
            timezone_id=timezone_id,
            precision=precision,
            uncertainty_seconds=uncertainty_seconds,
        )
        return cls.target_foundation.resolve(target_input, cls.target_profile)

    @classmethod
    def _project(cls, target_resolution):
        return cls.service.project(cls.ziwei_bundle, target_resolution, cls.target_profile)

    def test_ordinary_projection_is_exact_deterministic_and_schema_valid(self) -> None:
        target = self._target(datetime(2026, 8, 18, 12, 0))
        first = self._project(target)
        second = self._project(target)
        self.assertEqual(first, second)
        self.assertEqual("RESOLVED", first.status)
        self.assertEqual("PASS", first.integrity.status)
        self.assertEqual(1, len(first.candidates))
        row = first.candidates[0]
        annual = next(
            frame
            for frame in self.ziwei_bundle.temporal_state.annual_frames
            if frame.absolute_year == 2026
        )
        self.assertEqual(2026, row.civil_year)
        self.assertEqual(annual.absolute_year, row.annual_year)
        self.assertEqual(annual.nominal_age, row.minor_limit_age)
        self.assertEqual(annual.parent_daxian_frame_id, row.daxian_frame_id)
        self.assertEqual(annual.frame_id, row.source_annual_frame_id)
        Draft202012Validator(self.schema).validate(json_value(first))

        injected = copy.deepcopy(json_value(first))
        injected["prediction"] = "FORBIDDEN"
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.schema).validate(injected)

    def test_pre_daxian_year_preserves_none_parent(self) -> None:
        pre = next(
            frame
            for frame in self.ziwei_bundle.temporal_state.annual_frames
            if frame.parent_daxian_frame_id is None
        )
        target = self._target(datetime(pre.absolute_year, 7, 1, 12, 0))
        row = self._project(target).candidates[0]
        self.assertEqual(pre.frame_id, row.source_annual_frame_id)
        self.assertEqual(pre.nominal_age, row.minor_limit_age)
        self.assertIsNone(row.daxian_frame_id)

    def test_first_and_later_daxian_boundary_years_reuse_released_parent(self) -> None:
        daxian = self.ziwei_bundle.temporal_state.daxian_frames
        for source in (daxian[0], daxian[1]):
            with self.subTest(frame=source.frame_id):
                target = self._target(datetime(source.absolute_year_start, 7, 1, 12, 0))
                row = self._project(target).candidates[0]
                annual = next(
                    frame
                    for frame in self.ziwei_bundle.temporal_state.annual_frames
                    if frame.absolute_year == source.absolute_year_start
                )
                self.assertEqual(source.frame_id, annual.parent_daxian_frame_id)
                self.assertEqual(annual.parent_daxian_frame_id, row.daxian_frame_id)
                self.assertEqual(annual.nominal_age, row.minor_limit_age)

    def test_dst_fold_preserves_both_target_lineages_without_selector_dedup(self) -> None:
        target = self._target(
            datetime(2026, 11, 1, 1, 30),
            place="New York",
            latitude=40.7128,
            longitude=-74.0060,
            timezone_id="America/New_York",
        )
        self.assertEqual(2, len(target.candidates))
        result = self._project(target)
        self.assertEqual(2, len(result.candidates))
        self.assertEqual([0, 1], [row.source_target_candidate_index for row in result.candidates])
        self.assertEqual(
            [row.candidate_id for row in target.candidates],
            [row.source_target_candidate_id for row in result.candidates],
        )
        self.assertEqual({2026}, {row.annual_year for row in result.candidates})
        self.assertNotEqual(result.candidates[0].target_utc, result.candidates[1].target_utc)

    def test_uncertainty_within_one_year_preserves_every_upstream_candidate(self) -> None:
        target = self._target(
            datetime(2026, 6, 1, 12, 0),
            uncertainty_seconds=120,
        )
        self.assertGreater(len(target.candidates), 1)
        result = self._project(target)
        self.assertEqual(len(target.candidates), len(result.candidates))
        self.assertEqual(
            list(range(len(target.candidates))),
            [row.source_target_candidate_index for row in result.candidates],
        )
        self.assertEqual({2026}, {row.annual_year for row in result.candidates})

    def test_uncertainty_crossing_new_year_preserves_both_year_projections(self) -> None:
        target = self._target(
            datetime(2025, 12, 31, 23, 59, 30),
            uncertainty_seconds=120,
        )
        result = self._project(target)
        self.assertEqual(len(target.candidates), len(result.candidates))
        years = {row.civil_year for row in result.candidates}
        self.assertEqual({2025, 2026}, years)
        self.assertEqual(years, {row.annual_year for row in result.candidates})
        self.assertEqual(
            [row.candidate_id for row in target.candidates],
            [row.source_target_candidate_id for row in result.candidates],
        )

    def test_same_utc_can_project_different_civil_years_by_target_timezone(self) -> None:
        new_york = self._target(
            datetime(2025, 12, 31, 23, 30),
            place="New York",
            latitude=40.7128,
            longitude=-74.0060,
            timezone_id="America/New_York",
        )
        tokyo = self._target(
            datetime(2026, 1, 1, 13, 30),
            place="Tokyo",
            latitude=35.6762,
            longitude=139.6503,
            timezone_id="Asia/Tokyo",
        )
        self.assertEqual(new_york.candidates[0].target_utc, tokyo.candidates[0].target_utc)
        ny_row = self._project(new_york).candidates[0]
        tokyo_row = self._project(tokyo).candidates[0]
        self.assertEqual(2025, ny_row.annual_year)
        self.assertEqual(2026, tokyo_row.annual_year)

    def test_utc_year_does_not_override_candidate_local_civil_year(self) -> None:
        target = self._target(
            datetime(2025, 12, 31, 23, 30),
            place="New York",
            latitude=40.7128,
            longitude=-74.0060,
            timezone_id="America/New_York",
        )
        candidate = target.candidates[0]
        self.assertEqual(2026, candidate.target_utc.year)
        row = self._project(target).candidates[0]
        self.assertEqual(2025, row.civil_year)
        self.assertEqual(2025, row.annual_year)

    def test_las_year_does_not_override_candidate_local_civil_year(self) -> None:
        target = self._target(
            datetime(2026, 1, 1, 0, 10),
            place="Greenwich coordinate witness",
            latitude=0.0,
            longitude=-170.0,
            timezone_id="Europe/London",
        )
        candidate = target.candidates[0]
        self.assertEqual(2025, candidate.local_apparent_solar_datetime.year)
        row = self._project(target).candidates[0]
        self.assertEqual(2026, row.civil_year)
        self.assertEqual(2026, row.annual_year)

    def test_outside_materialized_annual_range_fails_closed_without_regeneration(self) -> None:
        short_request = replace(self.application_request, max_nominal_age=10, daxian_count=1)
        short_bundle = self.application_service.resolve(short_request)
        last_year = short_bundle.temporal_state.annual_frames[-1].absolute_year
        target = self._target(datetime(last_year + 1, 7, 1, 12, 0))
        before = short_bundle.temporal_state
        with self.assertRaises(SharedZiweiSelectorProjectionError) as caught:
            self.service.project(short_bundle, target, self.target_profile)
        self.assertEqual("SHARED_ZIWEI_ANNUAL_FRAME_NOT_EXACTLY_ONE", caught.exception.code)
        self.assertEqual(before, short_bundle.temporal_state)

    def test_upstream_hashes_are_byte_stable_after_projection(self) -> None:
        target = self._target(datetime(2026, 8, 18, 12, 0))
        ziwei_hash = self.ziwei_bundle.bundle_hash
        temporal_hashes = self.ziwei_bundle.temporal_hashes
        target_hashes = target.hashes
        self._project(target)
        self.assertEqual(ziwei_hash, self.ziwei_bundle.bundle_hash)
        self.assertEqual(temporal_hashes, self.ziwei_bundle.temporal_hashes)
        self.assertEqual(target_hashes, target.hashes)

    def test_recomputed_local_hashes_cannot_hide_selector_or_lineage_tamper(self) -> None:
        target = self._target(datetime(2026, 8, 18, 12, 0))
        result = self._project(target)
        original = result.candidates[0]
        tampered_candidate = replace(
            original,
            annual_year=original.annual_year + 1,
            source_target_candidate_index=99,
            candidate_hash="",
        )
        tampered_candidate = replace(
            tampered_candidate,
            candidate_hash=shared_selector_candidate_hash(tampered_candidate),
        )
        tampered = replace(result, candidates=(tampered_candidate,), hashes=replace(result.hashes, fact_hash="", computation_hash=""))
        tampered = replace(tampered, hashes=shared_selector_hash_bundle(tampered))

        report = validate_shared_ziwei_selector_projection(
            self.ziwei_bundle,
            target,
            self.target_profile,
            tampered,
        )
        self.assertEqual("FAIL", report.status)
        self.assertTrue(any("SOURCE_TARGET_CANDIDATE_INDEX_MISMATCH" in row for row in report.diagnostics))
        self.assertTrue(any("ANNUAL_YEAR_MISMATCH" in row for row in report.diagnostics))

        replay = validate_shared_ziwei_selector_full_replay(
            self.service,
            self.ziwei_bundle,
            target,
            self.target_profile,
            tampered,
        )
        self.assertEqual("FAIL", replay.status)
        self.assertIn("SHARED_ZIWEI_SELECTOR_FULL_REPLAY_MISMATCH", replay.diagnostics)

    def test_contract_has_no_bazi_flow_reinterpretation_or_prediction_surface(self) -> None:
        candidate_names = {field.name for field in fields(SharedZiweiSelectorProjectionCandidate)}
        resolution_names = {field.name for field in fields(SharedZiweiSelectorProjectionResolution)}
        forbidden = {
            "bazi_annual", "bazi_monthly", "bazi_daily", "bazi_hourly",
            "prediction", "interpretation", "winner", "ranking", "score",
        }
        self.assertTrue(candidate_names.isdisjoint(forbidden))
        self.assertTrue(resolution_names.isdisjoint(forbidden))

    def test_full_replay_passes_for_exact_upstream_objects(self) -> None:
        target = self._target(datetime(2026, 8, 18, 12, 0))
        result = self._project(target)
        report = validate_shared_ziwei_selector_full_replay(
            self.service,
            self.ziwei_bundle,
            target,
            self.target_profile,
            result,
        )
        self.assertEqual("PASS", report.status)
        self.assertEqual((), report.diagnostics)


if __name__ == "__main__":
    unittest.main()
