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
    WENMO_DEFAULT_MINOR_RULE_SET_ID,
    WENMO_DEFAULT_MINOR_RULE_SET_VERSION,
)
from fortune_training.ziwei_chart.registries import EARTHLY_BRANCHES, address
from fortune_training.ziwei_chart.rings import (
    CHANGSHENG_ANCHOR_BY_ELEMENT,
    JIANGQIAN_ANCHOR_BY_YEAR_BRANCH,
    RING_ALGORITHM_ID,
    RING_ALGORITHM_VERSION,
    RingGenerationError,
    WENMO_DEFAULT_RING_RULE_SET_ID,
    WENMO_DEFAULT_RING_RULE_SET_VERSION,
    WenmoDefaultRingGenerator,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / "tests" / "fixtures" / "wenmo-chartdiff-006-rings-r1.json").read_text(encoding="utf-8"))


class RingGeneratorUnitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = WenmoDefaultRingGenerator()

    def test_changsheng_anchor_elements_and_yinyang_sex_direction(self):
        for element, expected_anchor in CHANGSHENG_ANCHOR_BY_ELEMENT.items():
            forward = self.generator.changsheng(element, "甲", Sex.MALE)
            reverse = self.generator.changsheng(element, "辛", Sex.MALE)
            self.assertEqual(expected_anchor, forward.anchor_address.branch)
            self.assertEqual(expected_anchor, reverse.anchor_address.branch)
            self.assertEqual("FORWARD", forward.direction)
            self.assertEqual("REVERSE", reverse.direction)
            self.assertEqual(12, len(forward.members))
            self.assertEqual(12, len({row.address.branch for row in forward.members}))
        self.assertEqual("REVERSE", self.generator.changsheng("金", "甲", Sex.FEMALE).direction)
        self.assertEqual("FORWARD", self.generator.changsheng("金", "辛", Sex.FEMALE).direction)

    def test_taisui_all_year_branches_anchor_at_birth_branch(self):
        for branch in EARTHLY_BRANCHES:
            ring = self.generator.taisui(branch)
            self.assertEqual(branch, ring.anchor_address.branch)
            self.assertEqual("FORWARD", ring.direction)
            self.assertEqual(branch, ring.members[0].address.branch)

    def test_jiangqian_trine_anchor_mapping_covers_all_year_branches(self):
        self.assertEqual(12, len(JIANGQIAN_ANCHOR_BY_YEAR_BRANCH))
        for branch, anchor_branch in JIANGQIAN_ANCHOR_BY_YEAR_BRANCH.items():
            ring = self.generator.jiangqian(branch)
            self.assertEqual(anchor_branch, ring.anchor_address.branch)
            self.assertEqual("将星", ring.members[0].display_name)

    def test_boshi_uses_lucun_dependency_and_direction(self):
        ring = self.generator.boshi(address(9), "辛", Sex.MALE)
        self.assertEqual("酉", ring.anchor_address.branch)
        self.assertEqual("REVERSE", ring.direction)
        self.assertEqual("博士", ring.members[0].display_name)
        self.assertEqual("申", ring.members[1].address.branch)

    def test_ring_generation_fails_closed_without_lucun(self):
        with self.assertRaisesRegex(RingGenerationError, "BOSHI_RING_REQUIRES_LUCUN_PLACEMENT"):
            self.generator.generate("金", "辛", "巳", Sex.MALE, None)


class RingIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")

    def _profile(self, *, with_minor: bool = False, with_aux: bool = True) -> ResolvedZiweiCalculationProfile:
        kwargs = {}
        if with_aux:
            kwargs.update(
                auxiliary_rule_set_id=WENMO_DEFAULT_CORE_AUX_RULE_SET_ID,
                auxiliary_rule_set_version=WENMO_DEFAULT_CORE_AUX_RULE_SET_VERSION,
                auxiliary_algorithm_id=AUXILIARY_ALGORITHM_ID,
                auxiliary_algorithm_version=AUXILIARY_ALGORITHM_VERSION,
            )
        if with_minor:
            kwargs.update(
                minor_rule_set_id=WENMO_DEFAULT_MINOR_RULE_SET_ID,
                minor_rule_set_version=WENMO_DEFAULT_MINOR_RULE_SET_VERSION,
                minor_algorithm_id=MINOR_STAR_ALGORITHM_ID,
                minor_algorithm_version=MINOR_STAR_ALGORITHM_VERSION,
            )
        return ResolvedZiweiCalculationProfile(
            profile_id="WENMO-RING-COMPAT-R1",
            profile_version="1.0.0",
            time_calendar_policy_registry_version=self.registry.version,
            time_calendar_policies=self.registry.default_selection(),
            ring_rule_set_id=WENMO_DEFAULT_RING_RULE_SET_ID,
            ring_rule_set_version=WENMO_DEFAULT_RING_RULE_SET_VERSION,
            ring_algorithm_id=RING_ALGORITHM_ID,
            ring_algorithm_version=RING_ALGORITHM_VERSION,
            **kwargs,
        )

    def _resolve(self, profile: ResolvedZiweiCalculationProfile):
        return ZiweiChartFoundation(TimeCalendarFoundation(self.registry)).resolve(
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

    def test_wenmo_2001_fixture_closes_all_four_rings_and_48_members(self):
        result = self._resolve(self._profile())
        self.assertEqual("RESOLVED", result["status"])
        rings = {row["ring_id"]: row for row in result["charts"][0]["rings"]}
        self.assertEqual(4, len(rings))
        checked = 0
        for ring_id, expected in FIXTURE["expected"].items():
            ring = rings[ring_id]
            self.assertEqual(expected["anchor"], ring["anchor_address"]["branch"])
            self.assertEqual(expected["direction"], ring["direction"])
            actual_members = {row["display_name"]: row["address"]["branch"] for row in ring["members"]}
            self.assertEqual(expected["members"], actual_members)
            self.assertTrue(ring["source_refs"])
            self.assertTrue(all(row["source_refs"] for row in ring["members"]))
            checked += len(actual_members)
        self.assertEqual(48, checked)
        self.assertEqual(RING_ALGORITHM_VERSION, result["charts"][0]["algorithm_versions"]["rings"])

    def test_same_label_physical_star_and_ring_member_remain_distinct_fact_types(self):
        result = self._resolve(self._profile(with_minor=True))
        chart = result["charts"][0]
        physical = {row["display_name"]: row for row in chart["placements"]}
        self.assertIn("华盖", physical)
        self.assertEqual("STAR.HUAGAI", physical["华盖"]["entity_id"])
        jiangqian = next(row for row in chart["rings"] if row["ring_id"] == "RING.JIANGQIAN12")
        ring_huagai = next(row for row in jiangqian["members"] if row["display_name"] == "华盖")
        self.assertTrue(ring_huagai["member_id"].startswith("RING.JIANGQIAN12."))
        self.assertNotIn("entity_id", ring_huagai)

    def test_ring_profile_without_lucun_dependency_fails_closed(self):
        result = self._resolve(self._profile(with_aux=False))
        self.assertEqual("FAILED", result["status"])
        self.assertIn("BOSHI_RING_REQUIRES_LUCUN_PLACEMENT", result["diagnostics"])

    def test_unknown_ring_rule_set_rejected_at_profile_validation(self):
        broken = ResolvedZiweiCalculationProfile(
            profile_id="BROKEN-RING",
            profile_version="1.0.0",
            time_calendar_policy_registry_version=self.registry.version,
            time_calendar_policies=self.registry.default_selection(),
            ring_rule_set_id="UNNAMED-RING",
            ring_rule_set_version="1.0.0",
            ring_algorithm_id=RING_ALGORITHM_ID,
            ring_algorithm_version=RING_ALGORITHM_VERSION,
        )
        with self.assertRaisesRegex(ValueError, "unsupported ring rule set"):
            broken.validate(self.registry)


if __name__ == "__main__":
    unittest.main()
