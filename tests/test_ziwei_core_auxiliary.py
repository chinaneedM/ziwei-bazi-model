from __future__ import annotations

import unittest
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimeCalendarFoundation
from fortune_training.ziwei_chart import ResolvedZiweiCalculationProfile, Sex, ZiweiChartFoundation, ZiweiChartRequest
from fortune_training.ziwei_chart.auxiliary import (
    AUXILIARY_ALGORITHM_ID,
    AUXILIARY_ALGORITHM_VERSION,
    AuxiliaryContext,
    AuxiliaryGenerationError,
    KUI_YUE_BY_STEM,
    LUCUN_BY_STEM,
    QS_CORE_AUX_RULE_SET_ID,
    QS_CORE_AUX_RULE_SET_VERSION,
    TIANMA_BY_BRANCH,
    QSCoreAuxiliaryGenerator,
)
from fortune_training.ziwei_chart.registries import address


ROOT = Path(__file__).resolve().parents[1]


class QSCoreAuxiliaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = QSCoreAuxiliaryGenerator()

    def test_chang_qu_all_twelve_hours(self):
        for hour_index in range(12):
            chang, qu = self.generator.chang_qu(hour_index)
            self.assertEqual((10 - hour_index) % 12, chang.address.index)
            self.assertEqual((4 + hour_index) % 12, qu.address.index)
            self.assertTrue(chang.source_refs)
            self.assertTrue(qu.source_refs)

    def test_fu_bi_all_twelve_raw_lunar_months(self):
        for month in range(1, 13):
            fu, bi = self.generator.fu_bi(month)
            offset = month - 1
            self.assertEqual((4 + offset) % 12, fu.address.index)
            self.assertEqual((10 - offset) % 12, bi.address.index)

    def test_kui_yue_all_ten_stems(self):
        for stem, expected in KUI_YUE_BY_STEM.items():
            kui, yue = self.generator.kui_yue(stem)
            self.assertEqual(expected[0], kui.address.branch)
            self.assertEqual(expected[1], yue.address.branch)
        self.assertEqual(10, len(KUI_YUE_BY_STEM))

    def test_tianma_all_twelve_birth_year_branches(self):
        for branch, expected in TIANMA_BY_BRANCH.items():
            (tianma,) = self.generator.tianma(branch)
            self.assertEqual(expected, tianma.address.branch)
        self.assertEqual(12, len(TIANMA_BY_BRANCH))

    def test_lucun_yang_tuo_all_ten_stems(self):
        for stem, expected_lucun in LUCUN_BY_STEM.items():
            lucun, yang, tuo = self.generator.lucun_yang_tuo(stem)
            self.assertEqual(expected_lucun, lucun.address.branch)
            self.assertEqual((lucun.address.index + 1) % 12, yang.address.index)
            self.assertEqual((lucun.address.index - 1) % 12, tuo.address.index)
        self.assertEqual(10, len(LUCUN_BY_STEM))

    def test_hour_void_and_dijie_all_twelve_hours(self):
        for hour_index in range(12):
            void, dijie = self.generator.hour_void_robbery(hour_index)
            self.assertEqual((11 - hour_index) % 12, void.address.index)
            self.assertEqual((11 + hour_index) % 12, dijie.address.index)
        void, dijie = self.generator.hour_void_robbery(0)
        self.assertEqual("亥", void.address.branch)
        self.assertEqual("亥", dijie.address.branch)

    def test_reference_examples_are_preserved(self):
        chang, qu = self.generator.chang_qu(1)
        self.assertEqual("酉", chang.address.branch)
        self.assertEqual("巳", qu.address.branch)
        fu, bi = self.generator.fu_bi(2)
        self.assertEqual("巳", fu.address.branch)
        self.assertEqual("酉", bi.address.branch)
        lucun, yang, tuo = self.generator.lucun_yang_tuo("癸")
        self.assertEqual(("子", "丑", "亥"), (lucun.address.branch, yang.address.branch, tuo.address.branch))

    def test_strict_qs_rule_set_does_not_guess_month_based_auxiliaries_in_leap_month(self):
        with self.assertRaisesRegex(AuxiliaryGenerationError, "QS_CORE_AUX_LEAP_MONTH_POLICY_UNRESOLVED"):
            self.generator.generate(
                AuxiliaryContext(
                    ziwei_birth_year_stem="庚",
                    ziwei_birth_year_branch="子",
                    raw_lunar_month=4,
                    is_leap_month=True,
                    birth_hour_branch=address(6),
                )
            )


class QSCoreAuxiliaryIntegrationTests(unittest.TestCase):
    @staticmethod
    def _profile(registry: PolicyRegistry) -> ResolvedZiweiCalculationProfile:
        return ResolvedZiweiCalculationProfile(
            profile_id="QS-EWITNESS-CORE-AUX-SMOKE-R1",
            profile_version="1.0.0",
            time_calendar_policy_registry_version=registry.version,
            time_calendar_policies=registry.default_selection(),
            auxiliary_rule_set_id=QS_CORE_AUX_RULE_SET_ID,
            auxiliary_rule_set_version=QS_CORE_AUX_RULE_SET_VERSION,
            auxiliary_algorithm_id=AUXILIARY_ALGORITHM_ID,
            auxiliary_algorithm_version=AUXILIARY_ALGORITHM_VERSION,
        )

    def test_qs_auxiliary_profile_adds_twelve_typed_placements(self):
        registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        result = ZiweiChartFoundation(TimeCalendarFoundation(registry)).resolve(
            ZiweiChartRequest(
                birth=BirthInput(
                    reported_local_datetime=datetime(1994, 5, 17, 14, 30),
                    birth_place="Beijing",
                    latitude=39.9042,
                    longitude=116.4074,
                    timezone_id="Asia/Shanghai",
                ),
                sex=Sex.MALE,
                profile=self._profile(registry),
            )
        )
        self.assertEqual("RESOLVED", result["status"])
        chart = result["charts"][0]
        self.assertEqual(26, len(chart["placements"]))
        entity_ids = {row["entity_id"] for row in chart["placements"]}
        self.assertTrue(
            {
                "STAR.WENCHANG",
                "STAR.WENQU",
                "STAR.ZUOFU",
                "STAR.YOUBI",
                "STAR.TIANKUI",
                "STAR.TIANYUE",
                "STAR.TIANMA",
                "STAR.LUCUN",
                "STAR.QINGYANG",
                "STAR.TUOLUO",
                "AUX.HOUR_VOID",
                "STAR.DIJIE",
            }.issubset(entity_ids)
        )
        self.assertEqual(AUXILIARY_ALGORITHM_VERSION, chart["algorithm_versions"]["core_auxiliary"])
        self.assertTrue(all(row["source_refs"] for row in chart["placements"]))

    def test_leap_month_qs_auxiliary_profile_fails_closed_with_machine_diagnostic(self):
        registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        result = ZiweiChartFoundation(TimeCalendarFoundation(registry)).resolve(
            ZiweiChartRequest(
                birth=BirthInput(
                    reported_local_datetime=datetime(2020, 5, 23, 12, 0),
                    birth_place="Beijing",
                    latitude=39.9042,
                    longitude=116.4074,
                    timezone_id="Asia/Shanghai",
                ),
                sex=Sex.MALE,
                profile=self._profile(registry),
            )
        )
        self.assertEqual("FAILED", result["status"])
        self.assertIn("QS_CORE_AUX_LEAP_MONTH_POLICY_UNRESOLVED", result["diagnostics"])
        self.assertEqual([], result["charts"])

    def test_unsupported_auxiliary_rule_set_fails_closed_at_profile_validation(self):
        registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        profile = ResolvedZiweiCalculationProfile(
            profile_id="BROKEN-AUX",
            profile_version="1.0.0",
            time_calendar_policy_registry_version=registry.version,
            time_calendar_policies=registry.default_selection(),
            auxiliary_rule_set_id="IMPLICIT-MODERN-DEFAULT",
            auxiliary_rule_set_version="1.0.0",
            auxiliary_algorithm_id=AUXILIARY_ALGORITHM_ID,
            auxiliary_algorithm_version=AUXILIARY_ALGORITHM_VERSION,
        )
        with self.assertRaisesRegex(ValueError, "unsupported auxiliary rule set"):
            profile.validate(registry)


if __name__ == "__main__":
    unittest.main()
