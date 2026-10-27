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
from fortune_training.ziwei_chart.models import Placement
from fortune_training.ziwei_chart.registries import HEAVENLY_STEMS, address
from fortune_training.ziwei_chart.transformations import (
    ASSIGNMENTS_BY_STEM,
    S08_TRANSFORMATION_RULE_SET_ID,
    S08_TRANSFORMATION_RULE_SET_VERSION,
    TRANSFORMATION_ALGORITHM_ID,
    TRANSFORMATION_ALGORITHM_VERSION,
    TransformationGenerationError,
    TransformationGenerator,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads(
    (ROOT / "tests" / "fixtures" / "wenmo-chartdiff-006-transformations-r1.json").read_text(encoding="utf-8")
)


def _placement(entity_id: str, display_name: str, index: int) -> Placement:
    return Placement(
        entity_id=entity_id,
        display_name=display_name,
        address=address(index),
        generator_id="TEST-PHYSICAL-PLACEMENT",
        algorithm_version="1.0.0",
        source_refs=("TEST:PHYSICAL",),
    )


ALL_TARGET_PLACEMENTS = (
    _placement("STAR.LIANZHEN", "廉贞", 0),
    _placement("STAR.POJUN", "破军", 1),
    _placement("STAR.WUQU", "武曲", 2),
    _placement("STAR.TAIYANG", "太阳", 3),
    _placement("STAR.TIANJI", "天机", 4),
    _placement("STAR.TIANLIANG", "天梁", 5),
    _placement("STAR.ZIWEI", "紫微", 6),
    _placement("STAR.TAIYIN", "太阴", 7),
    _placement("STAR.TIANTONG", "天同", 8),
    _placement("STAR.WENCHANG", "文昌", 9),
    _placement("STAR.JUMEN", "巨门", 10),
    _placement("STAR.TANLANG", "贪狼", 11),
    _placement("STAR.YOUBI", "右弼", 0),
    _placement("STAR.WENQU", "文曲", 1),
    _placement("STAR.ZUOFU", "左辅", 2),
)


class TransformationRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = TransformationGenerator()

    def test_all_ten_stems_have_four_ordered_transformations(self):
        self.assertEqual(set(HEAVENLY_STEMS), set(ASSIGNMENTS_BY_STEM))
        for stem in HEAVENLY_STEMS:
            rows = self.generator.assignments(stem)
            self.assertEqual(4, len(rows), stem)
            self.assertEqual(["化禄", "化权", "化科", "化忌"], [row.transformation_type for row in rows])
            self.assertTrue(all(row.source_stem == stem for row in rows))

    def test_s08_has_exactly_40_assignments_and_39_mechanism_nodes(self):
        rows = [row for stem in HEAVENLY_STEMS for row in self.generator.assignments(stem)]
        self.assertEqual(40, len(rows))
        self.assertEqual(40, len({row.assignment_id for row in rows}))
        self.assertEqual(39, len({row.mechanism_id for row in rows}))
        shared = [row for row in rows if row.mechanism_id == "S08-TN-27"]
        self.assertEqual(
            [("庚", "化科", "STAR.TAIYIN"), ("癸", "化科", "STAR.TAIYIN")],
            [(row.source_stem, row.transformation_type, row.target_entity_id) for row in shared],
        )

    def test_activation_targets_existing_physical_addresses_without_mutation(self):
        before = tuple((row.entity_id, row.address.index) for row in ALL_TARGET_PLACEMENTS)
        rows = self.generator.activate(
            "辛",
            ALL_TARGET_PLACEMENTS,
            source_layer="NATAL_BIRTH_YEAR",
            context_id="NATAL",
        )
        after = tuple((row.entity_id, row.address.index) for row in ALL_TARGET_PLACEMENTS)
        self.assertEqual(before, after)
        physical = {row.entity_id: row.address for row in ALL_TARGET_PLACEMENTS}
        self.assertEqual(4, len(rows))
        for row in rows:
            self.assertEqual(physical[row.target_entity_id], row.target_address)
            self.assertEqual("辛", row.source_stem)
            self.assertEqual("NATAL_BIRTH_YEAR", row.source_layer)
            self.assertEqual("NATAL", row.context_id)
            self.assertTrue(row.source_refs)

    def test_same_generator_reuses_physical_facts_for_annual_context(self):
        natal = self.generator.activate(
            "辛", ALL_TARGET_PLACEMENTS, source_layer="NATAL_BIRTH_YEAR", context_id="NATAL"
        )
        annual = self.generator.activate(
            "辛", ALL_TARGET_PLACEMENTS, source_layer="ANNUAL", context_id="ANNUAL:2021"
        )
        self.assertEqual(
            [(row.transformation_type, row.target_entity_id, row.target_address) for row in natal],
            [(row.transformation_type, row.target_entity_id, row.target_address) for row in annual],
        )
        self.assertTrue(all(row.activation_id.startswith("ANNUAL:2021:") for row in annual))
        self.assertTrue(all(row.source_layer == "ANNUAL" for row in annual))

    def test_missing_required_target_fails_closed(self):
        rows = [row for row in ALL_TARGET_PLACEMENTS if row.entity_id != "STAR.WENCHANG"]
        with self.assertRaisesRegex(
            TransformationGenerationError,
            "TRANSFORMATION_TARGET_PLACEMENT_MISSING:STAR.WENCHANG",
        ):
            self.generator.activate("辛", rows, source_layer="NATAL_BIRTH_YEAR", context_id="NATAL")

    def test_duplicate_physical_target_fails_closed(self):
        rows = list(ALL_TARGET_PLACEMENTS) + [_placement("STAR.JUMEN", "巨门", 4)]
        with self.assertRaisesRegex(
            TransformationGenerationError,
            "TRANSFORMATION_DUPLICATE_TARGET_ENTITY_PLACEMENT",
        ):
            self.generator.activate("辛", rows, source_layer="NATAL_BIRTH_YEAR", context_id="NATAL")


class NatalTransformationIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.profile = ResolvedZiweiCalculationProfile(
            profile_id="S08-NATAL-TRANSFORMATION-COMPAT-R1",
            profile_version="1.0.0",
            time_calendar_policy_registry_version=cls.registry.version,
            time_calendar_policies=cls.registry.default_selection(),
            auxiliary_rule_set_id=WENMO_DEFAULT_CORE_AUX_RULE_SET_ID,
            auxiliary_rule_set_version=WENMO_DEFAULT_CORE_AUX_RULE_SET_VERSION,
            auxiliary_algorithm_id=AUXILIARY_ALGORITHM_ID,
            auxiliary_algorithm_version=AUXILIARY_ALGORITHM_VERSION,
            transformation_rule_set_id=S08_TRANSFORMATION_RULE_SET_ID,
            transformation_rule_set_version=S08_TRANSFORMATION_RULE_SET_VERSION,
            transformation_algorithm_id=TRANSFORMATION_ALGORITHM_ID,
            transformation_algorithm_version=TRANSFORMATION_ALGORITHM_VERSION,
        )
        cls.engine = ZiweiChartFoundation(TimeCalendarFoundation(cls.registry))
        cls.result = cls.engine.resolve(
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

    def test_wenmo_2001_birth_year_transformations_close_exactly(self):
        self.assertEqual("RESOLVED", self.result["status"])
        chart = self.result["charts"][0]
        rows = chart["transformations"]
        self.assertEqual(4, len(rows))
        actual = {
            row["transformation_type"]: {
                "target_entity_id": row["target_entity_id"],
                "target_display_name": row["target_display_name"],
                "target_branch": row["target_address"]["branch"],
                "assignment_id": row["assignment_id"],
                "mechanism_id": row["mechanism_id"],
            }
            for row in rows
        }
        expected = {row["transformation_type"]: {key: value for key, value in row.items() if key != "transformation_type"} for row in FIXTURE["expected"]}
        self.assertEqual(expected, actual)
        self.assertTrue(all(row["source_layer"] == "NATAL_BIRTH_YEAR" for row in rows))
        self.assertTrue(all(row["source_stem"] == "辛" for row in rows))
        self.assertTrue(all(row["context_id"] == "NATAL" for row in rows))
        self.assertEqual(TRANSFORMATION_ALGORITHM_VERSION, chart["algorithm_versions"]["transformations"])

    def test_transformation_targets_are_same_objects_as_physical_star_addresses(self):
        chart = self.result["charts"][0]
        physical = {row["entity_id"]: row["address"] for row in chart["placements"]}
        for row in chart["transformations"]:
            self.assertEqual(physical[row["target_entity_id"]], row["target_address"])

    def test_profile_without_transformation_binding_keeps_empty_overlay(self):
        profile = ResolvedZiweiCalculationProfile(
            profile_id="NO-TRANSFORMATION",
            profile_version="1.0.0",
            time_calendar_policy_registry_version=self.registry.version,
            time_calendar_policies=self.registry.default_selection(),
        )
        result = self.engine.resolve(
            ZiweiChartRequest(
                birth=BirthInput(
                    reported_local_datetime=datetime.fromisoformat(FIXTURE["input"]),
                    birth_place="Beijing",
                    latitude=39.9042,
                    longitude=116.4,
                    timezone_id="Asia/Shanghai",
                ),
                sex=Sex.MALE,
                profile=profile,
            )
        )
        self.assertEqual("RESOLVED", result["status"])
        self.assertEqual([], result["charts"][0]["transformations"])

    def test_unknown_transformation_rule_set_is_rejected_before_generation(self):
        broken = ResolvedZiweiCalculationProfile(
            profile_id="BROKEN-TRANSFORMATION",
            profile_version="1.0.0",
            time_calendar_policy_registry_version=self.registry.version,
            time_calendar_policies=self.registry.default_selection(),
            transformation_rule_set_id="UNNAMED-TRANSFORMATION-TABLE",
            transformation_rule_set_version="1.0.0",
            transformation_algorithm_id=TRANSFORMATION_ALGORITHM_ID,
            transformation_algorithm_version=TRANSFORMATION_ALGORITHM_VERSION,
        )
        with self.assertRaisesRegex(ValueError, "unsupported transformation rule set"):
            broken.validate(self.registry)


if __name__ == "__main__":
    unittest.main()
