from __future__ import annotations

import json
import unittest
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimeCalendarFoundation
from fortune_training.ziwei_chart import ResolvedZiweiCalculationProfile, Sex, ZiweiChartFoundation, ZiweiChartRequest
from fortune_training.ziwei_chart.auxiliary import (
    AUXILIARY_ALGORITHM_ID,
    AUXILIARY_ALGORITHM_VERSION,
    WENMO_DEFAULT_CORE_AUX_RULE_SET_ID,
    WENMO_DEFAULT_CORE_AUX_RULE_SET_VERSION,
)
from fortune_training.ziwei_chart.minor_stars import (
    MINOR_STAR_ALGORITHM_ID,
    MINOR_STAR_ALGORITHM_VERSION,
    MinorStarContext,
    WENMO_DEFAULT_MINOR_RULE_SET_ID,
    WENMO_DEFAULT_MINOR_RULE_SET_VERSION,
    WenmoDefaultMinorStarGenerator,
)
from fortune_training.ziwei_chart.registries import EARTHLY_BRANCHES, HEAVENLY_STEMS, address
from fortune_training.ziwei_chart.roles import (
    ROLE_ALGORITHM_ID,
    ROLE_ALGORITHM_VERSION,
    WENMO_DEFAULT_ROLE_RULE_SET_ID,
    WENMO_DEFAULT_ROLE_RULE_SET_VERSION,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads(
    (ROOT / "tests" / "fixtures" / "wenmo-chartdiff-006-minor-stars-r1.json").read_text(encoding="utf-8")
)


class WenmoOperationalMinorStarUnitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = WenmoDefaultMinorStarGenerator()

    def test_all_ten_stems_produce_five_stem_bound_facts(self):
        for stem in HEAVENLY_STEMS:
            rows = self.generator.stem_stars(stem)
            self.assertEqual(5, len(rows), stem)
            self.assertEqual(5, len({row.entity_id for row in rows}), stem)
            self.assertTrue(all(row.source_refs for row in rows))
        xin = {row.entity_id: row.address.branch for row in self.generator.stem_stars("辛")}
        self.assertEqual("酉", xin["STAR.TIANGUAN"])
        self.assertEqual("巳", xin["STAR.TIANFU_BLESSING"])
        self.assertEqual("午", xin["STAR.TIANCHU"])
        self.assertEqual("巳", xin["STAR.JIEKONG"])
        self.assertEqual("辰", xin["STAR.FU_JIEKONG"])

    def test_xunkong_all_sixty_valid_ganzhi_pairs(self):
        checked = 0
        for index in range(60):
            stem = HEAVENLY_STEMS[index % 10]
            branch = EARTHLY_BRANCHES[index % 12]
            xun, secondary = self.generator.xunkong(stem, branch)
            self.assertNotEqual(xun.address, secondary.address)
            self.assertTrue(xun.source_refs)
            self.assertTrue(secondary.source_refs)
            checked += 1
        self.assertEqual(60, checked)
        xin_si = {row.entity_id: row.address.branch for row in self.generator.xunkong("辛", "巳")}
        self.assertEqual("酉", xin_si["STAR.XUNKONG"])
        self.assertEqual("申", xin_si["STAR.FU_XUNKONG"])

    def test_year_branch_families_cover_all_twelve_branches(self):
        for branch in EARTHLY_BRANCHES:
            rows = self.generator.year_branch_stars(branch, "甲", life_index=3)
            self.assertEqual(20, len(rows), branch)
            self.assertEqual(20, len({row.entity_id for row in rows}), branch)
            self.assertTrue(all(0 <= row.address.index < 12 for row in rows))

    def test_hour_and_month_domains_are_exhaustive(self):
        for hour_index in range(12):
            rows = self.generator.hour_stars(hour_index)
            self.assertEqual(2, len(rows))
            self.assertTrue(all(0 <= row.address.index < 12 for row in rows))
        for month in range(1, 13):
            rows = self.generator.month_stars(month)
            self.assertEqual(6, len(rows))
            self.assertTrue(all(0 <= row.address.index < 12 for row in rows))

    def test_leap_month_policy_is_independent_and_explicit(self):
        common = dict(
            ziwei_birth_year_stem="庚",
            ziwei_birth_year_branch="子",
            raw_lunar_month=4,
            is_leap_month=True,
            birth_hour_branch=address(6),
            life_address=address(11),
            body_address=address(11),
        )
        first = MinorStarContext(**common, lunar_day=15)
        second = MinorStarContext(**common, lunar_day=16)
        self.assertEqual(4, self.generator._month_coordinate(first))
        self.assertEqual(5, self.generator._month_coordinate(second))


class WenmoOperationalMinorStarIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.profile = ResolvedZiweiCalculationProfile(
            profile_id="WENMO-OPERATIONAL-MINOR-COMPAT-R1",
            profile_version="1.0.0",
            time_calendar_policy_registry_version=cls.registry.version,
            time_calendar_policies=cls.registry.default_selection(),
            auxiliary_rule_set_id=WENMO_DEFAULT_CORE_AUX_RULE_SET_ID,
            auxiliary_rule_set_version=WENMO_DEFAULT_CORE_AUX_RULE_SET_VERSION,
            auxiliary_algorithm_id=AUXILIARY_ALGORITHM_ID,
            auxiliary_algorithm_version=AUXILIARY_ALGORITHM_VERSION,
            minor_rule_set_id=WENMO_DEFAULT_MINOR_RULE_SET_ID,
            minor_rule_set_version=WENMO_DEFAULT_MINOR_RULE_SET_VERSION,
            minor_algorithm_id=MINOR_STAR_ALGORITHM_ID,
            minor_algorithm_version=MINOR_STAR_ALGORITHM_VERSION,
            role_rule_set_id=WENMO_DEFAULT_ROLE_RULE_SET_ID,
            role_rule_set_version=WENMO_DEFAULT_ROLE_RULE_SET_VERSION,
            role_algorithm_id=ROLE_ALGORITHM_ID,
            role_algorithm_version=ROLE_ALGORITHM_VERSION,
        )
        cls.result = ZiweiChartFoundation(TimeCalendarFoundation(cls.registry)).resolve(
            ZiweiChartRequest(
                birth=BirthInput(
                    reported_local_datetime=datetime.fromisoformat(FIXTURE["input"]),
                    birth_place="Beijing",
                    latitude=39.9042,
                    longitude=116.4,
                    timezone_id="Asia/Shanghai",
                ),
                sex=Sex.MALE,
                profile=cls.profile,
            )
        )

    def test_2001_fixture_closes_all_thirty_five_operational_minor_stars(self):
        self.assertEqual("RESOLVED", self.result["status"])
        actual = {
            row["entity_id"]: row["address"]["branch"]
            for row in self.result["charts"][0]["placements"]
        }
        expected = FIXTURE["expected_operational_minor_placements"]
        self.assertEqual(35, len(expected))
        for entity_id, branch in expected.items():
            self.assertEqual(branch, actual[entity_id], entity_id)

    def test_full_current_wenmo_operational_slice_has_unique_entity_ids(self):
        chart = self.result["charts"][0]
        ids = [row["entity_id"] for row in chart["placements"]]
        self.assertEqual(67, len(ids))
        self.assertEqual(67, len(set(ids)))
        self.assertEqual(MINOR_STAR_ALGORITHM_VERSION, chart["algorithm_versions"]["minor_stars"])
        self.assertEqual(2, len(chart["role_bindings"]))

    def test_unknown_minor_rule_set_is_rejected_before_generation(self):
        broken = ResolvedZiweiCalculationProfile(
            profile_id="BROKEN-MINOR",
            profile_version="1.0.0",
            time_calendar_policy_registry_version=self.registry.version,
            time_calendar_policies=self.registry.default_selection(),
            minor_rule_set_id="UNNAMED-MODERN-MINOR",
            minor_rule_set_version="1.0.0",
            minor_algorithm_id=MINOR_STAR_ALGORITHM_ID,
            minor_algorithm_version=MINOR_STAR_ALGORITHM_VERSION,
        )
        with self.assertRaisesRegex(ValueError, "unsupported minor-star rule set"):
            broken.validate(self.registry)


if __name__ == "__main__":
    unittest.main()
