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
    QS_CORE_AUX_RULE_SET_ID,
    QS_CORE_AUX_RULE_SET_VERSION,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "wenmo-chartdiff-001.json"

WENMO_PALACE_LABEL_TO_ID = {
    "命宫": "LIFE",
    "兄弟宫": "SIBLINGS",
    "夫妻宫": "SPOUSE",
    "子女宫": "CHILDREN",
    "财帛宫": "WEALTH",
    "疾厄宫": "HEALTH",
    "迁移宫": "TRAVEL",
    "交友宫": "SERVANTS_FRIENDS",
    "官禄宫": "CAREER",
    "田宅宫": "PROPERTY",
    "福德宫": "FORTUNE",
    "父母宫": "PARENTS",
}


class WenmoChartDiff001Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.profile = ResolvedZiweiCalculationProfile(
            profile_id="WENMO-CHARTDIFF-001-COMMON-SCOPE",
            profile_version="1.0.0",
            time_calendar_policy_registry_version=cls.registry.version,
            time_calendar_policies=cls.registry.default_selection(),
            auxiliary_rule_set_id=QS_CORE_AUX_RULE_SET_ID,
            auxiliary_rule_set_version=QS_CORE_AUX_RULE_SET_VERSION,
            auxiliary_algorithm_id=AUXILIARY_ALGORITHM_ID,
            auxiliary_algorithm_version=AUXILIARY_ALGORITHM_VERSION,
        )
        birth = cls.fixture["input"]
        cls.result = ZiweiChartFoundation(TimeCalendarFoundation(cls.registry)).resolve(
            ZiweiChartRequest(
                birth=BirthInput(
                    reported_local_datetime=datetime.fromisoformat(birth["reported_local_datetime"]),
                    birth_place=birth["birth_place"],
                    latitude=birth["latitude"],
                    longitude=birth["longitude"],
                    timezone_id=birth["timezone_id"],
                ),
                sex=Sex.MALE,
                profile=cls.profile,
            )
        )

    def test_fixture_is_explicitly_compatibility_not_canonical_authority(self):
        self.assertEqual(
            "EXTERNAL_COMPATIBILITY_ORACLE_NOT_CANONICAL_AUTHORITY",
            self.fixture["authority"],
        )

    def test_time_and_calendar_match_wenmo_displayed_coordinates(self):
        self.assertEqual("RESOLVED", self.result["status"])
        branch = self.result["time_calendar"]["branches"][0]
        expected = self.fixture["wenmo_time_calendar"]
        self.assertTrue(
            branch["solar_time"]["local_apparent_solar_datetime"].startswith(
                expected["displayed_true_solar_minute"]
            )
        )
        lunar = branch["ziwei_calendar"]["effective_ziwei_lunar_date"]
        self.assertEqual(
            (expected["lunar_year"], expected["lunar_month"], expected["lunar_day"], expected["is_leap_month"]),
            (lunar["year"], lunar["month"], lunar["day"], lunar["is_leap_month"]),
        )

    def test_natal_structure_and_all_twelve_palace_ganzhi_match_wenmo(self):
        chart = self.result["charts"][0]
        structure = chart["structure"]
        expected = self.fixture["expected_current_common_scope"]
        self.assertEqual(expected["life_branch"], structure["life_address"]["branch"])
        self.assertEqual(expected["body_branch"], structure["body_address"]["branch"])
        self.assertEqual(expected["bureau"], {
            "element": structure["bureau"]["element"],
            "number": structure["bureau"]["number"],
            "life_palace_ganzhi": structure["bureau"]["life_palace_ganzhi"],
        })

        address_stem = {
            row["address"]["branch"]: row["stem"]
            for row in structure["address_attributes"]
        }
        designation_branch = {
            row["designation_id"]: row["address"]["branch"]
            for row in structure["designation_bindings"]
        }
        for wenmo_label, ganzhi in expected["palace_ganzhi_by_designation"].items():
            designation_id = WENMO_PALACE_LABEL_TO_ID[wenmo_label]
            branch = designation_branch[designation_id]
            self.assertEqual(ganzhi[1], branch, wenmo_label)
            self.assertEqual(ganzhi[0], address_stem[branch], wenmo_label)

    def test_original_twenty_six_common_scope_placements_remain_exact(self):
        chart = self.result["charts"][0]
        actual = {
            row["entity_id"]: row["address"]["branch"]
            for row in chart["placements"]
        }
        expected = self.fixture["expected_current_common_scope"]["placements"]
        for entity_id, branch in expected.items():
            self.assertEqual(branch, actual[entity_id], entity_id)
        self.assertEqual(30, len(actual))
        self.assertTrue({"STAR.SANTAI", "STAR.BAZUO", "STAR.ENGUANG", "STAR.TIANGUI"}.issubset(actual))

    def test_dikong_and_separate_tiankong_are_not_collapsed(self):
        chart = self.result["charts"][0]
        placements = {row["entity_id"]: row for row in chart["placements"]}
        self.assertEqual("地空", placements["STAR.DIKONG"]["display_name"])
        observed_future = self.fixture["observed_beyond_current_engine_scope"]
        self.assertEqual("亥", observed_future["separate_tiankong_small_star"])
        self.assertNotIn("STAR.TIANKONG", placements)


if __name__ == "__main__":
    unittest.main()
