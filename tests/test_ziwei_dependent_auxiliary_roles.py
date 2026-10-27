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
from fortune_training.ziwei_chart.derived_auxiliary import DerivedAuxiliaryGenerator
from fortune_training.ziwei_chart.models import Placement
from fortune_training.ziwei_chart.registries import address
from fortune_training.ziwei_chart.roles import (
    MINGZHU_BY_LIFE_BRANCH,
    QSRoleGenerator,
    RoleGenerationError,
    ROLE_ALGORITHM_ID,
    ROLE_ALGORITHM_VERSION,
    WENMO_DEFAULT_ROLE_RULE_SET_ID,
    WENMO_DEFAULT_ROLE_RULE_SET_VERSION,
    WenmoDefaultRoleGenerator,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / "tests" / "fixtures" / "wenmo-profile-discriminators-r1.json").read_text(encoding="utf-8"))


def _anchor(entity_id: str, display_name: str, index: int) -> Placement:
    return Placement(entity_id, display_name, address(index), "TEST", "1", ("TEST:ANCHOR",))


class DerivedAuxiliaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = DerivedAuxiliaryGenerator()

    def test_fullbook_santai_bazuo_examples(self):
        anchors = {
            "STAR.ZUOFU": address(10).index,  # 戌
            "STAR.YOUBI": address(4).index,   # 辰
        }
        santai, bazuo = self.generator.san_tai_ba_zuo(anchors, 18)
        self.assertEqual("卯", santai.address.branch)
        self.assertEqual("亥", bazuo.address.branch)
        self.assertTrue(santai.source_refs)
        self.assertTrue(bazuo.source_refs)

    def test_enguang_tiangui_examples(self):
        anchors = {
            "STAR.WENCHANG": address(2).index,  # 寅
            "STAR.WENQU": address(0).index,     # 子
        }
        enguang, tiangui = self.generator.en_guang_tian_gui(anchors, 18)
        self.assertEqual("午", enguang.address.branch)
        self.assertEqual("辰", tiangui.address.branch)

    def test_day_one_anchor_semantics(self):
        placements = [
            _anchor("STAR.ZUOFU", "左辅", 2),
            _anchor("STAR.YOUBI", "右弼", 0),
            _anchor("STAR.WENCHANG", "文昌", 4),
            _anchor("STAR.WENQU", "文曲", 10),
        ]
        actual = {row.entity_id: row.address.branch for row in self.generator.generate(placements, 1)}
        self.assertEqual(
            {
                "STAR.SANTAI": "寅",
                "STAR.BAZUO": "子",
                "STAR.ENGUANG": "卯",
                "STAR.TIANGUI": "酉",
            },
            actual,
        )


class RoleBindingTests(unittest.TestCase):
    def test_mingzhu_table_covers_all_twelve_life_branches(self):
        generator = QSRoleGenerator()
        self.assertEqual(12, len(MINGZHU_BY_LIFE_BRANCH))
        for branch, (entity_id, name) in MINGZHU_BY_LIFE_BRANCH.items():
            row = generator.mingzhu(branch)
            self.assertEqual(entity_id, row.entity_id)
            self.assertEqual(name, row.entity_display_name)
            self.assertEqual("LIFE_PALACE_BRANCH", row.basis_type)
            self.assertEqual(branch, row.basis_value)

    def test_strict_qs_preserves_zi_wu_shenzhu_textual_ambiguity(self):
        generator = QSRoleGenerator()
        for branch in ("子", "午"):
            with self.assertRaisesRegex(RoleGenerationError, "QS_SHENZHU_ZI_WU_TEXTUAL_AMBIGUITY"):
                generator.shenzhu(branch)

    def test_wenmo_operational_shenzhu_uses_birth_year_branch(self):
        generator = WenmoDefaultRoleGenerator()
        shenzhu = generator.shenzhu("巳")
        self.assertEqual("STAR.TIANJI", shenzhu.entity_id)
        self.assertEqual("天机", shenzhu.entity_display_name)
        self.assertEqual("ZIWEI_BIRTH_YEAR_BRANCH", shenzhu.basis_type)
        self.assertEqual("巳", shenzhu.basis_value)

    def test_wenmo_resolves_zi_wu_to_fire_without_mutating_qs(self):
        generator = WenmoDefaultRoleGenerator()
        for branch in ("子", "午"):
            shenzhu = generator.shenzhu(branch)
            self.assertEqual("STAR.HUOXING", shenzhu.entity_id)
            self.assertEqual("火星", shenzhu.entity_display_name)


class WenmoDependentAndRoleIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.case = next(row for row in FIXTURE["cases"] if row["id"] == "WENMO-CHARTDIFF-006")
        cls.registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.profile = ResolvedZiweiCalculationProfile(
            profile_id="WENMO-DEPENDENT-ROLE-COMPAT-R1",
            profile_version="1.0.0",
            time_calendar_policy_registry_version=cls.registry.version,
            time_calendar_policies=cls.registry.default_selection(),
            auxiliary_rule_set_id=WENMO_DEFAULT_CORE_AUX_RULE_SET_ID,
            auxiliary_rule_set_version=WENMO_DEFAULT_CORE_AUX_RULE_SET_VERSION,
            auxiliary_algorithm_id=AUXILIARY_ALGORITHM_ID,
            auxiliary_algorithm_version=AUXILIARY_ALGORITHM_VERSION,
            role_rule_set_id=WENMO_DEFAULT_ROLE_RULE_SET_ID,
            role_rule_set_version=WENMO_DEFAULT_ROLE_RULE_SET_VERSION,
            role_algorithm_id=ROLE_ALGORITHM_ID,
            role_algorithm_version=ROLE_ALGORITHM_VERSION,
        )
        cls.result = ZiweiChartFoundation(TimeCalendarFoundation(cls.registry)).resolve(
            ZiweiChartRequest(
                birth=BirthInput(
                    reported_local_datetime=datetime.fromisoformat(cls.case["input"]),
                    birth_place="Beijing",
                    latitude=39.9042,
                    longitude=116.4,
                    timezone_id="Asia/Shanghai",
                ),
                sex=Sex.MALE,
                profile=cls.profile,
            )
        )

    def test_wenmo_2001_fixture_closes_all_four_dependent_stars(self):
        self.assertEqual("RESOLVED", self.result["status"])
        chart = self.result["charts"][0]
        actual = {row["entity_id"]: row["address"]["branch"] for row in chart["placements"]}
        for entity_id, branch in self.case["observed_dependent_auxiliary"].items():
            self.assertEqual(branch, actual[entity_id], entity_id)
        self.assertEqual(32, len(actual))

    def test_wenmo_2001_fixture_closes_mingzhu_and_shenzhu_as_roles(self):
        chart = self.result["charts"][0]
        actual = {row["role_id"]: row for row in chart["role_bindings"]}
        self.assertEqual(2, len(actual))
        for role_id, expected in self.case["observed_roles"].items():
            row = actual[role_id]
            for field, value in expected.items():
                self.assertEqual(value, row[field], f"{role_id}:{field}")
        self.assertEqual(ROLE_ALGORITHM_VERSION, chart["algorithm_versions"]["roles"])
        self.assertTrue(all(row["source_refs"] for row in chart["role_bindings"]))


if __name__ == "__main__":
    unittest.main()
