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
    shared_ziwei_temporal_layer_hashes,
    validate_shared_ziwei_selector_projection,
    validate_shared_ziwei_temporal_layer_projection,
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
from fortune_training.ziwei_chart.temporal_auxiliary import (
    temporal_auxiliary_candidate_set_hashes,
    temporal_auxiliary_method_candidate_hashes,
)


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
        self.assertIsNotNone(row.daxian_layer_projection)
        self.assertEqual("DAXIAN", row.daxian_layer_projection.source_layer)
        self.assertEqual(row.daxian_frame_id, row.daxian_layer_projection.frame_id)
        self.assertIsNone(row.daxian_layer_projection.parent_frame_id)
        self.assertEqual("ANNUAL", row.annual_layer_projection.source_layer)
        self.assertEqual(annual.frame_id, row.annual_layer_projection.frame_id)
        self.assertEqual(row.daxian_frame_id, row.annual_layer_projection.parent_frame_id)
        self.assertEqual(annual.year_stem, row.annual_layer_projection.source_stem)
        self.assertEqual("LOCAL_SOLAR_DATE_INDEXED", row.ziwei_calendar_date_policy)
        self.assertEqual("ZI_START_23", row.ziwei_day_boundary_policy)
        self.assertEqual("REGULAR_LUNAR_MONTH_RESOLVED", row.monthly_projection_status)
        self.assertEqual(f"MONTH:2026:{row.effective_lunar_month}", row.monthly_frame_id)
        self.assertIsNotNone(row.monthly_layer_projection)
        self.assertEqual("MONTH", row.monthly_layer_projection.source_layer)
        self.assertEqual(row.monthly_frame_id, row.monthly_layer_projection.frame_id)
        self.assertEqual(row.source_annual_frame_id, row.monthly_layer_projection.parent_frame_id)
        for layer in (
            row.daxian_layer_projection,
            row.annual_layer_projection,
            row.monthly_layer_projection,
        ):
            self.assertEqual("S10_CURRENT_TEMPORAL_R1", layer.frame_rule_set_id)
            self.assertEqual("ZIWEI-TEMPORAL-FRAMES-V1", layer.frame_algorithm_id)
            self.assertEqual(4, len(layer.transformations))
            self.assertEqual(5, len(layer.auxiliary_activations))
            self.assertEqual(1, len(layer.auxiliary_candidate_sets))
            kui_yue = layer.auxiliary_candidate_sets[0]
            self.assertEqual("CANDIDATES_PRESERVED_NO_SELECTION", kui_yue.selection_status)
            self.assertEqual(2, len(kui_yue.method_candidates))
            self.assertEqual(
                {"S01-QS-STRICT-KUI-YUE-R1", "COMPAT-WENMO-KUI-YUE-R1"},
                {candidate.method_id for candidate in kui_yue.method_candidates},
            )
            self.assertTrue(all(len(candidate.activations) == 2 for candidate in kui_yue.method_candidates))
            self.assertEqual(64, len(kui_yue.fact_hash))
            self.assertEqual(64, len(kui_yue.computation_hash))
            self.assertTrue(layer.source_refs)
            self.assertEqual({layer.source_layer}, {item.source_layer for item in layer.transformations})
            self.assertEqual({layer.source_stem}, {item.source_stem for item in layer.transformations})
            self.assertEqual({layer.source_layer}, {item.source_layer for item in layer.auxiliary_activations})
            self.assertEqual({layer.source_stem}, {item.source_stem for item in layer.auxiliary_activations})
            self.assertEqual(64, len(layer.fact_hash))
            self.assertEqual(64, len(layer.computation_hash))
        self.assertEqual(
            12,
            len({
                item.activation_id
                for layer in (
                    row.daxian_layer_projection,
                    row.annual_layer_projection,
                    row.monthly_layer_projection,
                )
                for item in layer.transformations
            }),
        )
        self.assertEqual(
            15,
            len({
                item.activation_id
                for layer in (
                    row.daxian_layer_projection,
                    row.annual_layer_projection,
                    row.monthly_layer_projection,
                )
                for item in layer.auxiliary_activations
            }),
        )
        self.assertEqual(2, len(row.monthly_ganzhi))
        self.assertIn(row.monthly_active_address_branch, "子丑寅卯辰巳午未申酉戌亥")
        self.assertEqual("REGULAR_LUNAR_DAY_RESOLVED", row.daily_projection_status)
        self.assertEqual(f"DAY:{row.daily_effective_gregorian_date}", row.daily_frame_id)
        self.assertEqual(2, len(row.daily_ganzhi))
        self.assertIn(row.daily_active_address_branch, "子丑寅卯辰巳午未申酉戌亥")
        self.assertEqual(12, len(row.daily_designation_overlay))
        self.assertEqual("LIFE", row.daily_designation_overlay[0].designation_id)
        self.assertEqual(row.daily_active_address_branch, row.daily_designation_overlay[0].address.branch)
        self.assertEqual(12, len({item.address.branch for item in row.daily_designation_overlay}))
        self.assertEqual("SOURCE_RULE_RESOLVED", row.daily_auxiliary_status)
        self.assertEqual(["禄存", "擎羊", "陀罗", "文昌", "文曲"], [item.display_name for item in row.daily_auxiliary_activations])
        self.assertEqual({row.daily_ganzhi[0]}, {item.source_stem for item in row.daily_auxiliary_activations})
        self.assertTrue(all(item.source_layer == "DAY" for item in row.daily_auxiliary_activations))
        self.assertEqual(1, len(row.daily_auxiliary_candidate_sets))
        self.assertEqual(
            "DAY",
            row.daily_auxiliary_candidate_sets[0].source_layer,
        )
        self.assertIn("S10:ZZTERM-P-0278", row.daily_auxiliary_source_refs)
        self.assertEqual("S10-FLOW-MONTH-FIRST-DAY-FORWARD-R1", row.daily_rule_id)
        self.assertIn("S10:ZZTERM-P-0274", row.daily_source_refs)
        self.assertEqual("PROFILE_RULE_SET_RESOLVED", row.daily_transformation_status)
        self.assertEqual("S08_CURRENT_40_ASSIGNMENT_R1", row.daily_transformation_rule_set_id)
        self.assertEqual(4, len(row.daily_transformations))
        self.assertEqual(
            ["化禄", "化权", "化科", "化忌"],
            [activation.transformation_type for activation in row.daily_transformations],
        )
        self.assertEqual(
            {row.daily_ganzhi[0]},
            {activation.source_stem for activation in row.daily_transformations},
        )
        self.assertTrue(all(activation.source_layer == "DAY" for activation in row.daily_transformations))
        self.assertIn("S01:ZZZA-CF-008", row.daily_transformation_source_refs)
        self.assertEqual(
            "CANDIDATES_PRESERVED_NO_SELECTED_FRAME",
            row.hourly_projection_status,
        )
        self.assertEqual(
            ["ZHONGZHOU_LUOYANG_MEAN_SOLAR_TIME", "LOCAL_APPARENT_SOLAR_TIME"],
            [candidate.time_standard for candidate in row.hourly_method_candidates],
        )
        self.assertTrue(all(candidate.active_address_branch == candidate.hour_branch for candidate in row.hourly_method_candidates))
        self.assertTrue(all(len(candidate.designation_overlay) == 12 for candidate in row.hourly_method_candidates))
        self.assertTrue(all(candidate.designation_overlay[0].address.branch == candidate.active_address_branch for candidate in row.hourly_method_candidates))
        self.assertTrue(all(candidate.active_address_rule_id == "S10-CASE-HOUR-BRANCH-ACTIVE-ADDRESS-CANDIDATE-R1" for candidate in row.hourly_method_candidates))
        self.assertTrue(all(candidate.auxiliary_status == "CASE_METHOD_SOURCE_RULE_RESOLVED" for candidate in row.hourly_method_candidates))
        self.assertTrue(all(len(candidate.auxiliary_activations) == 5 for candidate in row.hourly_method_candidates))
        self.assertTrue(all(len(candidate.auxiliary_candidate_sets) == 1 for candidate in row.hourly_method_candidates))
        self.assertTrue(all(
            candidate.auxiliary_candidate_sets[0].source_layer == "HOUR_CANDIDATE"
            for candidate in row.hourly_method_candidates
        ))
        self.assertTrue(all(
            {item.source_stem for item in candidate.auxiliary_activations} == {candidate.hour_ganzhi[0]}
            for candidate in row.hourly_method_candidates
        ))
        self.assertTrue(all(candidate.authority_status == "CASE_METHOD_ONLY_NOT_GLOBAL_RULE" for candidate in row.hourly_method_candidates))
        self.assertTrue(all("S01:ZZZA-CF-002" in candidate.source_refs for candidate in row.hourly_method_candidates))
        self.assertTrue(all(candidate.transformation_status == "CASE_METHOD_PROFILE_RULE_SET_RESOLVED" for candidate in row.hourly_method_candidates))
        self.assertTrue(all(len(candidate.transformations) == 4 for candidate in row.hourly_method_candidates))
        self.assertTrue(all("S01:ZZZA-CF-008" in candidate.transformation_source_refs for candidate in row.hourly_method_candidates))
        Draft202012Validator(self.schema).validate(json_value(first))

        injected = copy.deepcopy(json_value(first))
        injected["prediction"] = "FORBIDDEN"
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.schema).validate(injected)

    def test_leap_month_is_preserved_without_fabricating_a_regular_month_frame(self) -> None:
        target = self._target(datetime(2025, 8, 1, 12, 0))
        row = self._project(target).candidates[0]
        self.assertTrue(row.effective_lunar_is_leap_month)
        self.assertEqual("LEAP_MONTH_UNRESOLVED_NO_FRAME", row.monthly_projection_status)
        self.assertIsNone(row.monthly_frame_id)
        self.assertIsNone(row.monthly_ganzhi)
        self.assertIsNone(row.monthly_active_address_branch)
        self.assertIsNone(row.monthly_layer_projection)
        self.assertEqual("PARENT_LEAP_MONTH_UNRESOLVED_NO_FRAME", row.daily_projection_status)
        self.assertIsNone(row.daily_frame_id)
        self.assertIsNone(row.daily_effective_gregorian_date)
        self.assertIsNone(row.daily_ganzhi)
        self.assertIsNone(row.daily_active_address_branch)
        self.assertEqual((), row.daily_designation_overlay)
        self.assertEqual("PARENT_DAILY_FRAME_UNRESOLVED", row.daily_auxiliary_status)
        self.assertEqual((), row.daily_auxiliary_activations)
        self.assertEqual((), row.daily_auxiliary_source_refs)
        self.assertIsNone(row.daily_rule_id)
        self.assertEqual((), row.daily_source_refs)
        self.assertEqual("PARENT_DAILY_FRAME_UNRESOLVED", row.daily_transformation_status)
        self.assertIsNone(row.daily_transformation_rule_set_id)
        self.assertEqual((), row.daily_transformations)
        self.assertEqual((), row.daily_transformation_source_refs)
        self.assertEqual(2, len(row.hourly_method_candidates))

    def test_daily_active_address_counts_forward_from_month_first_day(self) -> None:
        row = self._project(self._target(datetime(2026, 8, 18, 12, 0))).candidates[0]
        branches = "子丑寅卯辰巳午未申酉戌亥"
        expected_index = (
            branches.index(row.monthly_active_address_branch)
            + row.effective_lunar_day
            - 1
        ) % 12
        self.assertEqual(branches[expected_index], row.daily_active_address_branch)

    def test_hourly_time_standard_conflict_remains_two_named_candidates(self) -> None:
        row = self._project(self._target(datetime(2026, 11, 15, 13, 15))).candidates[0]
        mean, apparent = row.hourly_method_candidates
        self.assertEqual("ZHONGZHOU_LUOYANG_MEAN_SOLAR_TIME", mean.time_standard)
        self.assertEqual("LOCAL_APPARENT_SOLAR_TIME", apparent.time_standard)
        self.assertNotEqual(mean.source_local_datetime, apparent.source_local_datetime)
        self.assertNotEqual(mean.hour_branch, apparent.hour_branch)
        self.assertEqual("CASE_METHOD_ACTIVE_ADDRESS_CANDIDATE_NO_COMPLETE_CHART", mean.frame_status)
        self.assertEqual("CASE_METHOD_ACTIVE_ADDRESS_CANDIDATE_NO_COMPLETE_CHART", apparent.frame_status)
        self.assertEqual(mean.hour_branch, mean.active_address_branch)
        self.assertEqual(apparent.hour_branch, apparent.active_address_branch)
        self.assertIn("S01:ZZZA-PR-004", mean.source_refs)

    def test_ziwei_late_zi_daily_date_uses_ziwei_policy_not_bazi_flow(self) -> None:
        row = self._project(self._target(datetime(2026, 8, 18, 23, 30))).candidates[0]
        self.assertEqual("2026-08-19", row.daily_effective_gregorian_date)
        self.assertEqual("ZI_START_23", row.ziwei_day_boundary_policy)
        self.assertNotIn("bazi", row.daily_rule_id.lower())

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
        self.assertIsNone(row.daxian_layer_projection)
        self.assertIsNone(row.annual_layer_projection.parent_frame_id)

    def test_layer_projection_replay_rejects_rehashed_lineage_and_fact_tamper(self) -> None:
        target = self._target(datetime(2026, 8, 18, 12, 0))
        result = self._project(target)
        original = result.candidates[0]
        annual_layer = original.annual_layer_projection
        changed_layer = replace(
            annual_layer,
            parent_frame_id="DAXIAN:index=999",
            source_stem="癸" if annual_layer.source_stem != "癸" else "甲",
            frame_rule_set_id="TAMPERED-RULE-SET",
            source_refs=("S10:TAMPERED",),
            transformations=(
                replace(
                    annual_layer.transformations[0],
                    source_stem="癸" if annual_layer.source_stem != "癸" else "甲",
                ),
                *annual_layer.transformations[1:],
            ),
            auxiliary_activations=(
                *annual_layer.auxiliary_activations[:3],
                replace(
                    annual_layer.auxiliary_activations[3],
                    source_stem="癸" if annual_layer.source_stem != "癸" else "甲",
                ),
                *annual_layer.auxiliary_activations[4:],
            ),
            fact_hash="",
            computation_hash="",
        )
        fact_hash, computation_hash = shared_ziwei_temporal_layer_hashes(changed_layer)
        changed_layer = replace(
            changed_layer,
            fact_hash=fact_hash,
            computation_hash=computation_hash,
        )
        changed_candidate = replace(
            original,
            annual_layer_projection=changed_layer,
            candidate_hash="",
        )
        changed_candidate = replace(
            changed_candidate,
            candidate_hash=shared_selector_candidate_hash(changed_candidate),
        )
        tampered = replace(
            result,
            candidates=(changed_candidate,),
            hashes=replace(result.hashes, fact_hash="", computation_hash=""),
        )
        tampered = replace(tampered, hashes=shared_selector_hash_bundle(tampered))

        report = validate_shared_ziwei_selector_projection(
            self.ziwei_bundle,
            target,
            self.target_profile,
            tampered,
        )
        self.assertEqual("FAIL", report.status)
        self.assertIn(
            "CANDIDATE_0_ANNUAL_LAYER_PROJECTION_MISMATCH",
            report.diagnostics,
        )

        annual_frame = next(
            frame
            for frame in self.ziwei_bundle.temporal_state.annual_frames
            if frame.frame_id == original.source_annual_frame_id
        )
        replay = validate_shared_ziwei_temporal_layer_projection(
            changed_layer,
            source_layer="ANNUAL",
            source_frame=annual_frame,
            temporal_state=self.ziwei_bundle.temporal_state,
        )
        self.assertEqual("FAIL", replay.status)
        self.assertIn("TEMPORAL_LAYER_PARENT_FRAME_ID_REPLAY_MISMATCH", replay.diagnostics)
        self.assertIn("TEMPORAL_LAYER_SOURCE_STEM_REPLAY_MISMATCH", replay.diagnostics)
        self.assertIn("TEMPORAL_LAYER_FRAME_RULE_SET_ID_REPLAY_MISMATCH", replay.diagnostics)
        self.assertIn("TEMPORAL_LAYER_SOURCE_REFS_REPLAY_MISMATCH", replay.diagnostics)

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

    def test_layer_projection_rejects_rehashed_kui_yue_candidate_tamper(self) -> None:
        target = self._target(datetime(2026, 8, 18, 12, 0))
        result = self._project(target)
        original = result.candidates[0]
        layer = original.annual_layer_projection
        candidate_set = layer.auxiliary_candidate_sets[0]
        strict, compat = candidate_set.method_candidates
        changed_compat = replace(
            compat,
            activations=(
                replace(
                    compat.activations[0],
                    target_address=compat.activations[1].target_address,
                ),
                compat.activations[1],
            ),
            fact_hash="",
            computation_hash="",
        )
        fact_hash, computation_hash = temporal_auxiliary_method_candidate_hashes(
            changed_compat
        )
        changed_compat = replace(
            changed_compat,
            fact_hash=fact_hash,
            computation_hash=computation_hash,
        )
        changed_set = replace(
            candidate_set,
            method_candidates=(strict, changed_compat),
            fact_hash="",
            computation_hash="",
        )
        fact_hash, computation_hash = temporal_auxiliary_candidate_set_hashes(changed_set)
        changed_set = replace(
            changed_set,
            fact_hash=fact_hash,
            computation_hash=computation_hash,
        )
        changed_layer = replace(
            layer,
            auxiliary_candidate_sets=(changed_set,),
            fact_hash="",
            computation_hash="",
        )
        fact_hash, computation_hash = shared_ziwei_temporal_layer_hashes(changed_layer)
        changed_layer = replace(
            changed_layer,
            fact_hash=fact_hash,
            computation_hash=computation_hash,
        )
        changed_candidate = replace(
            original,
            annual_layer_projection=changed_layer,
            candidate_hash="",
        )
        changed_candidate = replace(
            changed_candidate,
            candidate_hash=shared_selector_candidate_hash(changed_candidate),
        )
        tampered = replace(
            result,
            candidates=(changed_candidate,),
            hashes=replace(result.hashes, fact_hash="", computation_hash=""),
        )
        tampered = replace(tampered, hashes=shared_selector_hash_bundle(tampered))
        report = validate_shared_ziwei_selector_projection(
            self.ziwei_bundle,
            target,
            self.target_profile,
            tampered,
        )
        self.assertEqual("FAIL", report.status)
        self.assertIn("CANDIDATE_0_ANNUAL_LAYER_PROJECTION_MISMATCH", report.diagnostics)

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

    def test_recomputed_hashes_cannot_hide_daily_or_hourly_transformation_tamper(self) -> None:
        target = self._target(datetime(2026, 8, 18, 12, 0))
        result = self._project(target)
        original = result.candidates[0]

        changed_daily_activation = replace(
            original.daily_transformations[0],
            source_stem="癸" if original.daily_transformations[0].source_stem != "癸" else "甲",
        )
        changed_hour_activation = replace(
            original.hourly_method_candidates[0].transformations[0],
            source_stem=(
                "癸"
                if original.hourly_method_candidates[0].transformations[0].source_stem != "癸"
                else "甲"
            ),
        )
        changed_hour = replace(
            original.hourly_method_candidates[0],
            designation_overlay=(
                replace(
                    original.hourly_method_candidates[0].designation_overlay[0],
                    address=original.hourly_method_candidates[0].designation_overlay[1].address,
                ),
                *original.hourly_method_candidates[0].designation_overlay[1:],
            ),
            auxiliary_activations=(
                replace(
                    original.hourly_method_candidates[0].auxiliary_activations[0],
                    source_stem="癸" if original.hourly_method_candidates[0].auxiliary_activations[0].source_stem != "癸" else "甲",
                ),
                *original.hourly_method_candidates[0].auxiliary_activations[1:],
            ),
            transformations=(
                changed_hour_activation,
                *original.hourly_method_candidates[0].transformations[1:],
            ),
        )
        changed_candidate = replace(
            original,
            daily_designation_overlay=(
                replace(
                    original.daily_designation_overlay[0],
                    address=original.daily_designation_overlay[1].address,
                ),
                *original.daily_designation_overlay[1:],
            ),
            daily_auxiliary_activations=(
                replace(
                    original.daily_auxiliary_activations[0],
                    source_stem="癸" if original.daily_auxiliary_activations[0].source_stem != "癸" else "甲",
                ),
                *original.daily_auxiliary_activations[1:],
            ),
            daily_transformations=(changed_daily_activation, *original.daily_transformations[1:]),
            hourly_method_candidates=(changed_hour, original.hourly_method_candidates[1]),
            candidate_hash="",
        )
        changed_candidate = replace(
            changed_candidate,
            candidate_hash=shared_selector_candidate_hash(changed_candidate),
        )
        tampered = replace(
            result,
            candidates=(changed_candidate,),
            hashes=replace(result.hashes, fact_hash="", computation_hash=""),
        )
        tampered = replace(tampered, hashes=shared_selector_hash_bundle(tampered))

        report = validate_shared_ziwei_selector_projection(
            self.ziwei_bundle,
            target,
            self.target_profile,
            tampered,
        )
        self.assertEqual("FAIL", report.status)
        self.assertTrue(any("DAILY_TRANSFORMATIONS_MISMATCH" in row for row in report.diagnostics))
        self.assertTrue(any("DAILY_DESIGNATION_OVERLAY_MISMATCH" in row for row in report.diagnostics))
        self.assertTrue(any("DAILY_AUXILIARY_ACTIVATIONS_MISMATCH" in row for row in report.diagnostics))
        self.assertTrue(any("HOURLY_0_TRANSFORMATIONS_MISMATCH" in row for row in report.diagnostics))
        self.assertTrue(any("HOURLY_0_DESIGNATION_OVERLAY_MISMATCH" in row for row in report.diagnostics))
        self.assertTrue(any("HOURLY_0_AUXILIARY_ACTIVATIONS_MISMATCH" in row for row in report.diagnostics))

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
