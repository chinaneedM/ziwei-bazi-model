from __future__ import annotations

import json
import unittest
from dataclasses import replace
from pathlib import Path

from fortune_training.calendar_foundation import PolicyRegistry
from fortune_training.ziwei_chart import ResolvedZiweiCalculationProfile, Sex
from fortune_training.ziwei_chart.models import AddressAttribute, Placement
from fortune_training.ziwei_chart.registries import address
from fortune_training.ziwei_chart.temporal import (
    S10_CURRENT_TEMPORAL_RULE_SET_ID,
    S10_CURRENT_TEMPORAL_RULE_SET_VERSION,
    TEMPORAL_ALGORITHM_ID,
    TEMPORAL_ALGORITHM_VERSION,
    TemporalNatalContext,
    ZiweiTemporalEngine,
)
from fortune_training.ziwei_chart.transformations import (
    S08_TRANSFORMATION_RULE_SET_ID,
    S08_TRANSFORMATION_RULE_SET_VERSION,
    TRANSFORMATION_ALGORITHM_ID,
    TRANSFORMATION_ALGORITHM_VERSION,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads(
    (ROOT / "tests" / "fixtures" / "wenmo-chartdiff-006-temporal-r1.json").read_text(encoding="utf-8")
)


def _placement(entity_id: str, display_name: str, branch_index: int) -> Placement:
    return Placement(
        entity_id=entity_id,
        display_name=display_name,
        address=address(branch_index),
        generator_id="TEST-NATAL-PHYSICAL",
        algorithm_version="1.0.0",
        source_refs=("TEST:WENMO-006-PHYSICAL",),
    )


WENMO_2001_TRANSFORMATION_TARGETS = (
    _placement("STAR.LIANZHEN", "廉贞", 3),
    _placement("STAR.POJUN", "破军", 3),
    _placement("STAR.WUQU", "武曲", 7),
    _placement("STAR.TAIYANG", "太阳", 8),
    _placement("STAR.TIANJI", "天机", 10),
    _placement("STAR.TIANLIANG", "天梁", 10),
    _placement("STAR.ZIWEI", "紫微", 11),
    _placement("STAR.TAIYIN", "太阴", 6),
    _placement("STAR.TIANTONG", "天同", 6),
    _placement("STAR.WENCHANG", "文昌", 4),
    _placement("STAR.JUMEN", "巨门", 8),
    _placement("STAR.TANLANG", "贪狼", 7),
    _placement("STAR.YOUBI", "右弼", 0),
    _placement("STAR.WENQU", "文曲", 10),
    _placement("STAR.ZUOFU", "左辅", 2),
)

WENMO_2001_ADDRESS_STEMS = tuple(
    AddressAttribute(address(index), stem)
    for index, stem in enumerate(("庚", "辛", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己"))
)


def _context(**changes) -> TemporalNatalContext:
    base = TemporalNatalContext(
        ziwei_birth_year=2001,
        ziwei_birth_year_stem="辛",
        ziwei_birth_year_branch="巳",
        bureau_number=4,
        bureau_element="金",
        life_address=address(6),
        address_attributes=WENMO_2001_ADDRESS_STEMS,
        placements=WENMO_2001_TRANSFORMATION_TARGETS,
        sex=Sex.MALE,
        natal_month_coordinate=11,
        birth_hour_branch=address(5),
    )
    return replace(base, **changes)


class TemporalRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.profile = ResolvedZiweiCalculationProfile(
            profile_id="S10-TEMPORAL-WENMO-006-R1",
            profile_version="1.0.0",
            time_calendar_policy_registry_version=cls.registry.version,
            time_calendar_policies=cls.registry.default_selection(),
            transformation_rule_set_id=S08_TRANSFORMATION_RULE_SET_ID,
            transformation_rule_set_version=S08_TRANSFORMATION_RULE_SET_VERSION,
            transformation_algorithm_id=TRANSFORMATION_ALGORITHM_ID,
            transformation_algorithm_version=TRANSFORMATION_ALGORITHM_VERSION,
            temporal_rule_set_id=S10_CURRENT_TEMPORAL_RULE_SET_ID,
            temporal_rule_set_version=S10_CURRENT_TEMPORAL_RULE_SET_VERSION,
            temporal_algorithm_id=TEMPORAL_ALGORITHM_ID,
            temporal_algorithm_version=TEMPORAL_ALGORITHM_VERSION,
        ).validate(cls.registry)
        cls.engine = ZiweiTemporalEngine()
        cls.state = cls.engine.generate(_context(), cls.profile)

    def test_wenmo_2001_all_twelve_daxian_frames_match(self):
        self.assertEqual(FIXTURE["expected_daxian_direction"], self.state.daxian_direction)
        self.assertEqual(4, self.state.first_daxian_nominal_age)
        self.assertEqual(12, len(self.state.daxian_frames))
        for expected, actual in zip(FIXTURE["expected_daxian"], self.state.daxian_frames, strict=True):
            self.assertEqual(expected["index"], actual.index)
            self.assertEqual(tuple(expected["age"]), (actual.nominal_age_start, actual.nominal_age_end))
            self.assertEqual(tuple(expected["years"]), (actual.absolute_year_start, actual.absolute_year_end))
            self.assertEqual(expected["active_ganzhi"], actual.active_palace_ganzhi)
            self.assertEqual(expected["active_ganzhi"][1], actual.active_address.branch)
            self.assertEqual(expected["active_ganzhi"][0], actual.source_stem)
            self.assertEqual(actual.active_address, actual.designation_overlay[0].address)
            self.assertEqual(12, len({row.address.index for row in actual.designation_overlay}))
            self.assertEqual(4, len(actual.transformations))
            self.assertTrue(all(row.source_layer == "DAXIAN" for row in actual.transformations))
            self.assertTrue(all(row.source_stem == actual.source_stem for row in actual.transformations))

    def test_daxian_direction_matrix_is_year_yinyang_by_sex(self):
        cases = (
            ("甲", Sex.MALE, "FORWARD"),
            ("甲", Sex.FEMALE, "REVERSE"),
            ("辛", Sex.MALE, "REVERSE"),
            ("辛", Sex.FEMALE, "FORWARD"),
        )
        for stem, sex, expected in cases:
            context = _context(ziwei_birth_year_stem=stem, sex=sex)
            frames = self.engine.daxian_frames(context, self.profile, count=2)
            delta = (frames[1].active_address.index - frames[0].active_address.index) % 12
            self.assertEqual(expected, self.engine._direction_name(self.engine._daxian_direction(stem, sex)))
            self.assertEqual(1 if expected == "FORWARD" else 11, delta)

    def test_five_bureau_numbers_are_first_daxian_nominal_ages(self):
        for number in (2, 3, 4, 5, 6):
            context = _context(bureau_number=number)
            frame = self.engine.daxian_frames(context, self.profile, count=1)[0]
            self.assertEqual(number, frame.nominal_age_start)
            self.assertEqual(2001 + number - 1, frame.absolute_year_start)

    def test_annual_samples_keep_taisui_branch_and_natal_palace_ganzhi_separate(self):
        frames = {row.absolute_year: row for row in self.state.annual_frames}
        for expected in FIXTURE["expected_annual_samples"]:
            actual = frames[expected["year"]]
            self.assertEqual(expected["age"], actual.nominal_age)
            self.assertEqual(expected["year_ganzhi"], f"{actual.year_stem}{actual.year_branch}")
            self.assertEqual(expected["year_ganzhi"][1], actual.active_address.branch)
            self.assertEqual(expected["active_palace_ganzhi"], actual.active_palace_ganzhi)
            self.assertEqual(expected["parent_daxian"], actual.parent_daxian_frame_id)
            self.assertEqual(actual.active_address, actual.designation_overlay[0].address)
            self.assertEqual(4, len(actual.transformations))
            self.assertTrue(all(row.source_layer == "ANNUAL" for row in actual.transformations))
            self.assertTrue(all(row.source_stem == actual.year_stem for row in actual.transformations))

    def test_2004_proves_annual_transform_stem_is_not_annual_life_palace_stem(self):
        frame = next(row for row in self.state.annual_frames if row.absolute_year == 2004)
        self.assertEqual("甲", frame.year_stem)
        self.assertEqual("丙申", frame.active_palace_ganzhi)
        self.assertTrue(all(row.source_stem == "甲" for row in frame.transformations))
        self.assertNotEqual(frame.year_stem, frame.active_palace_ganzhi[0])

    def test_classical_doujun_source_example_replays_exactly(self):
        context = _context(
            natal_month_coordinate=3,
            birth_hour_branch=address(4),
        )
        self.assertEqual("辰", self.engine.doujun_address(context, "寅").branch)

    def test_wenmo_1994_zi_year_doujun_replays_exactly(self):
        context = _context(
            natal_month_coordinate=4,
            birth_hour_branch=address(7),
        )
        self.assertEqual("辰", self.engine.doujun_address(context, "子").branch)

    def test_all_annual_frames_carry_hashed_doujun_identity(self):
        for frame in self.state.annual_frames:
            expected = self.engine.doujun_address(_context(), frame.year_branch)
            self.assertEqual(expected, frame.doujun_address)
            self.assertTrue(frame.doujun_rule_id)

    def test_minor_limit_age_one_to_twelve_matches_wenmo_and_male_forward_rule(self):
        frames = {row.nominal_age: row for row in self.state.minor_limit_frames}
        for age_text, expected_branch in FIXTURE["expected_minor_age_1_to_12"].items():
            self.assertEqual(expected_branch, frames[int(age_text)].active_address.branch)
        for age in range(2, 13):
            self.assertEqual(
                (frames[age - 1].active_address.index + 1) % 12,
                frames[age].active_address.index,
            )

    def test_minor_limit_female_reverses_independent_of_year_stem_yinyang(self):
        male = _context(ziwei_birth_year_stem="甲", sex=Sex.MALE)
        female = _context(ziwei_birth_year_stem="甲", sex=Sex.FEMALE)
        self.assertEqual("未", self.engine.minor_limit_frame(male, 1).active_address.branch)
        self.assertEqual("未", self.engine.minor_limit_frame(female, 1).active_address.branch)
        self.assertEqual("申", self.engine.minor_limit_frame(male, 2).active_address.branch)
        self.assertEqual("午", self.engine.minor_limit_frame(female, 2).active_address.branch)

    def test_generated_schedule_keeps_predaxian_annual_years_without_inventing_parent(self):
        self.assertEqual(123, len(self.state.annual_frames))
        self.assertEqual(123, len(self.state.minor_limit_frames))
        age1 = self.state.annual_frames[0]
        age3 = self.state.annual_frames[2]
        age4 = self.state.annual_frames[3]
        self.assertIsNone(age1.parent_daxian_frame_id)
        self.assertIsNone(age3.parent_daxian_frame_id)
        self.assertEqual("DAXIAN:index=1", age4.parent_daxian_frame_id)

    def test_temporal_profile_without_transformation_binding_generates_geometry_only(self):
        profile = ResolvedZiweiCalculationProfile(
            profile_id="S10-TEMPORAL-GEOMETRY-ONLY-R1",
            profile_version="1.0.0",
            time_calendar_policy_registry_version=self.registry.version,
            time_calendar_policies=self.registry.default_selection(),
            temporal_rule_set_id=S10_CURRENT_TEMPORAL_RULE_SET_ID,
            temporal_rule_set_version=S10_CURRENT_TEMPORAL_RULE_SET_VERSION,
            temporal_algorithm_id=TEMPORAL_ALGORITHM_ID,
            temporal_algorithm_version=TEMPORAL_ALGORITHM_VERSION,
        ).validate(self.registry)
        state = self.engine.generate(_context(placements=()), profile, daxian_count=1, max_nominal_age=5)
        self.assertEqual(1, len(state.daxian_frames))
        self.assertEqual(5, len(state.annual_frames))
        self.assertEqual((), state.daxian_frames[0].transformations)
        self.assertTrue(all(frame.transformations == () for frame in state.annual_frames))

    def test_unknown_temporal_rule_set_rejected_at_profile_validation(self):
        broken = ResolvedZiweiCalculationProfile(
            profile_id="BROKEN-TEMPORAL",
            profile_version="1.0.0",
            time_calendar_policy_registry_version=self.registry.version,
            time_calendar_policies=self.registry.default_selection(),
            temporal_rule_set_id="UNNAMED-TEMPORAL",
            temporal_rule_set_version="1.0.0",
            temporal_algorithm_id=TEMPORAL_ALGORITHM_ID,
            temporal_algorithm_version=TEMPORAL_ALGORITHM_VERSION,
        )
        with self.assertRaisesRegex(ValueError, "unsupported temporal rule set"):
            broken.validate(self.registry)


if __name__ == "__main__":
    unittest.main()
