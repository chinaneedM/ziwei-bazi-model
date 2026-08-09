from __future__ import annotations

import json
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimeCalendarFoundation
from fortune_training.ziwei_chart import ResolvedZiweiCalculationProfile, Sex, ZiweiChartFoundation, ZiweiChartRequest
from fortune_training.ziwei_chart.auxiliary import (
    AUXILIARY_ALGORITHM_ID,
    AUXILIARY_ALGORITHM_VERSION,
    QS_CORE_AUX_RULE_SET_ID,
    QS_CORE_AUX_RULE_SET_VERSION,
    WENMO_DEFAULT_CORE_AUX_RULE_SET_ID,
    WENMO_DEFAULT_CORE_AUX_RULE_SET_VERSION,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / "tests" / "fixtures" / "wenmo-profile-discriminators-r1.json").read_text(encoding="utf-8"))


class WenmoProfileDiscriminatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.engine = ZiweiChartFoundation(TimeCalendarFoundation(cls.registry))
        defaults = cls.registry.default_selection()
        cls.wenmo_policies = replace(
            defaults,
            bazi_day_boundary_policy="ZI_START_23",
            bazi_late_zi_hour_stem_policy="ZI_START_ROLLOVER",
            ziwei_life_body_leap_month_policy="ZHONGZHOU_FIXED_15",
        )
        cls.wenmo_profile = ResolvedZiweiCalculationProfile(
            profile_id="WENMO-DEFAULT-COMPAT-R1",
            profile_version="1.0.0",
            time_calendar_policy_registry_version=cls.registry.version,
            time_calendar_policies=cls.wenmo_policies,
            ziwei_day_boundary_policy="ZI_START_23",
            auxiliary_rule_set_id=WENMO_DEFAULT_CORE_AUX_RULE_SET_ID,
            auxiliary_rule_set_version=WENMO_DEFAULT_CORE_AUX_RULE_SET_VERSION,
            auxiliary_algorithm_id=AUXILIARY_ALGORITHM_ID,
            auxiliary_algorithm_version=AUXILIARY_ALGORITHM_VERSION,
        )

    def _case(self, case_id: str):
        return next(row for row in FIXTURE["cases"] if row["id"] == case_id)

    def _resolve(self, case: dict, profile=None):
        return self.engine.resolve(
            ZiweiChartRequest(
                birth=BirthInput(
                    reported_local_datetime=datetime.fromisoformat(case["input"]),
                    birth_place="Beijing",
                    latitude=39.9042,
                    longitude=116.4,
                    timezone_id="Asia/Shanghai",
                ),
                sex=Sex.MALE,
                profile=profile or self.wenmo_profile,
            )
        )

    def _assert_common_chart(self, case: dict, result: dict):
        self.assertEqual("RESOLVED", result["status"], case["id"])
        branch = result["time_calendar"]["branches"][0]
        self.assertTrue(branch["solar_time"]["local_apparent_solar_datetime"].startswith(case["displayed_true_solar_minute"]))
        chart = result["charts"][0]
        structure = chart["structure"]
        self.assertEqual(case["life_branch"], structure["life_address"]["branch"])
        self.assertEqual(case["body_branch"], structure["body_address"]["branch"])
        self.assertEqual(tuple(case["bureau"]), (structure["bureau"]["element"], structure["bureau"]["number"], structure["bureau"]["life_palace_ganzhi"]))
        actual = {row["entity_id"]: row["address"]["branch"] for row in chart["placements"]}
        self.assertEqual(case["placements"], actual)
        self.assertEqual(26, len(actual))

    def test_leap_month_first_half_preserves_raw_lunar_identity_but_uses_month_4_coordinate(self):
        case = self._case("WENMO-CHARTDIFF-002")
        result = self._resolve(case)
        self._assert_common_chart(case, result)
        branch = result["time_calendar"]["branches"][0]
        raw = branch["ziwei_calendar"]["local_solar_lunar_date"]
        expected = case["gui_raw_lunar"]
        self.assertEqual((expected["year"], expected["month"], expected["day"], expected["is_leap_month"]), (raw["year"], raw["month"], raw["day"], raw["is_leap_month"]))
        self.assertEqual(4, result["charts"][0]["structure"]["natal_month_coordinate"])
        self.assertEqual("未", case["placements"]["STAR.ZUOFU"])
        self.assertEqual("未", case["placements"]["STAR.YOUBI"])

    def test_leap_month_second_half_preserves_raw_lunar_identity_but_uses_month_5_coordinate(self):
        case = self._case("WENMO-CHARTDIFF-003")
        result = self._resolve(case)
        self._assert_common_chart(case, result)
        branch = result["time_calendar"]["branches"][0]
        raw = branch["ziwei_calendar"]["local_solar_lunar_date"]
        expected = case["gui_raw_lunar"]
        self.assertEqual((expected["year"], expected["month"], expected["day"], expected["is_leap_month"]), (raw["year"], raw["month"], raw["day"], raw["is_leap_month"]))
        self.assertEqual(5, result["charts"][0]["structure"]["natal_month_coordinate"])
        self.assertEqual("申", case["placements"]["STAR.ZUOFU"])
        self.assertEqual("午", case["placements"]["STAR.YOUBI"])

    def test_late_zi_rollover_keeps_time_calendar_raw_and_advances_chart_coordinate(self):
        case = self._case("WENMO-CHARTDIFF-004")
        result = self._resolve(case)
        self._assert_common_chart(case, result)
        branch = result["time_calendar"]["branches"][0]
        raw = branch["ziwei_calendar"]["local_solar_lunar_date"]
        time_calendar_effective = branch["ziwei_calendar"]["effective_ziwei_lunar_date"]
        raw_expected = case["raw_local_solar_lunar"]
        effective_expected = case["effective_ziwei_lunar"]
        self.assertEqual((raw_expected["month"], raw_expected["day"]), (raw["month"], raw["day"]))
        self.assertEqual((raw_expected["month"], raw_expected["day"]), (time_calendar_effective["month"], time_calendar_effective["day"]))
        structure = result["charts"][0]["structure"]
        self.assertEqual((effective_expected["month"], effective_expected["day"]), (structure["raw_lunar_month"], structure["lunar_birth_day"]))
        self.assertEqual("ZI_START_23", result["calculation_profile"]["ziwei_day_boundary_policy"])
        self.assertEqual(case["expected_bazi_day_pillar"], branch["bazi_time"]["day_pillar"])

    def test_xin_year_kui_yue_is_profile_discriminating_not_a_global_override(self):
        case = self._case("WENMO-CHARTDIFF-005")
        wenmo = self._resolve(case)
        self._assert_common_chart(case, wenmo)
        wenmo_actual = {row["entity_id"]: row["address"]["branch"] for row in wenmo["charts"][0]["placements"]}
        self.assertEqual("寅", wenmo_actual["STAR.TIANKUI"])
        self.assertEqual("午", wenmo_actual["STAR.TIANYUE"])

        qs_profile = ResolvedZiweiCalculationProfile(
            profile_id="QS-XIN-COUNTERFACTUAL-R1",
            profile_version="1.0.0",
            time_calendar_policy_registry_version=self.registry.version,
            time_calendar_policies=self.wenmo_policies,
            ziwei_day_boundary_policy="ZI_START_23",
            auxiliary_rule_set_id=QS_CORE_AUX_RULE_SET_ID,
            auxiliary_rule_set_version=QS_CORE_AUX_RULE_SET_VERSION,
            auxiliary_algorithm_id=AUXILIARY_ALGORITHM_ID,
            auxiliary_algorithm_version=AUXILIARY_ALGORITHM_VERSION,
        )
        qs = self._resolve(case, qs_profile)
        qs_actual = {row["entity_id"]: row["address"]["branch"] for row in qs["charts"][0]["placements"]}
        expected_qs = case["strict_qs_kui_yue_counterfactual"]
        self.assertEqual(expected_qs["STAR.TIANKUI"], qs_actual["STAR.TIANKUI"])
        self.assertEqual(expected_qs["STAR.TIANYUE"], qs_actual["STAR.TIANYUE"])
        self.assertNotEqual((wenmo_actual["STAR.TIANKUI"], wenmo_actual["STAR.TIANYUE"]), (qs_actual["STAR.TIANKUI"], qs_actual["STAR.TIANYUE"]))

    def test_external_exports_do_not_redefine_raw_lunar_identity(self):
        first = self._case("WENMO-CHARTDIFF-002")
        second = self._case("WENMO-CHARTDIFF-003")
        self.assertTrue(first["gui_raw_lunar"]["is_leap_month"])
        self.assertTrue(second["gui_raw_lunar"]["is_leap_month"])
        self.assertIn("四月初一", first["text_export_lunar_label"])
        self.assertIn("五月十六", second["text_export_lunar_label"])


if __name__ == "__main__":
    unittest.main()
