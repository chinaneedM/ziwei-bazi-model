from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from fortune_training.bazi_chart import (
    BaziChartFoundation,
    BaziChartRequest,
    BranchInstance,
    SEXAGENARY_CYCLE,
    bazi_foundation_v1_profile,
    natal_hash_bundle,
    sexagenary_index,
    validate_natal_state,
)
from fortune_training.bazi_chart.registries import (
    BRANCH_ELEMENTS,
    EARTHLY_BRANCHES,
    HEAVENLY_STEMS,
)
from fortune_training.bazi_chart.relations import generate_raw_relations
from fortune_training.bazi_chart.ten_gods import TEN_GOD_DISPLAY, ten_god
from fortune_training.calendar_foundation import BirthInput


ROOT = Path(__file__).resolve().parents[1]


class BaziChartFoundationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.foundation = BaziChartFoundation.from_repository(ROOT)
        cls.profile = bazi_foundation_v1_profile(cls.foundation.time_calendar.policy_registry)

    @staticmethod
    def beijing(local: datetime, **kwargs) -> BirthInput:
        return BirthInput(
            reported_local_datetime=local,
            birth_place="Beijing",
            latitude=39.9042,
            longitude=116.4074,
            timezone_id="Asia/Shanghai",
            **kwargs,
        )

    def resolve_a1(self):
        return self.foundation.resolve_typed(
            BaziChartRequest(
                birth=self.beijing(datetime(1990, 6, 15, 12, 0)),
                profile=self.profile,
            )
        )

    def test_sexagenary_registry_accepts_exactly_sixty_of_120_pairs(self):
        legal = []
        illegal = []
        for stem in HEAVENLY_STEMS:
            for branch in EARTHLY_BRANCHES:
                ganzhi = stem + branch
                try:
                    sexagenary_index(ganzhi)
                    legal.append(ganzhi)
                except ValueError:
                    illegal.append(ganzhi)
        self.assertEqual(60, len(legal))
        self.assertEqual(60, len(illegal))
        self.assertEqual(set(SEXAGENARY_CYCLE), set(legal))
        with self.assertRaises(ValueError):
            sexagenary_index("甲丑")

    def test_ten_god_matrix_is_complete_for_all_100_stem_pairs(self):
        seen = set()
        for day_master in HEAVENLY_STEMS:
            roles = []
            for target in HEAVENLY_STEMS:
                semantic, display = ten_god(day_master, target)
                self.assertIn(semantic, TEN_GOD_DISPLAY)
                self.assertEqual(TEN_GOD_DISPLAY[semantic], display)
                roles.append(semantic)
                seen.add(semantic)
            self.assertEqual(10, len(set(roles)))
        self.assertEqual(set(TEN_GOD_DISPLAY), seen)

    def test_a1_authoritative_historical_timezone_natal_core(self):
        result = self.resolve_a1()
        self.assertEqual("RESOLVED", result.status)
        self.assertEqual(1, len(result.candidates))
        candidate = result.candidates[0]
        chart = candidate.chart
        self.assertEqual("PASS", candidate.integrity.status)
        self.assertEqual("PASS", validate_natal_state(chart).status)
        self.assertEqual(
            ("庚午", "壬午", "辛亥", "癸巳"),
            tuple(row.ganzhi for row in chart.pillars),
        )
        self.assertEqual("辛", chart.day_master_stem)

        hidden = {}
        for row in chart.hidden_stems:
            hidden.setdefault(row.branch_position, []).append(row.stem)
        self.assertEqual(["丁", "己"], hidden["YEAR"])
        self.assertEqual(["丁", "己"], hidden["MONTH"])
        self.assertEqual(["壬", "甲"], hidden["DAY"])
        self.assertEqual(["丙", "戊", "庚"], hidden["HOUR"])

        visible_ten_gods = {
            row.target_instance_id: row.display_name
            for row in chart.ten_gods
            if ".HIDDEN:" not in row.target_instance_id
        }
        self.assertEqual("劫财", visible_ten_gods["YEAR.STEM"])
        self.assertEqual("伤官", visible_ten_gods["MONTH.STEM"])
        self.assertEqual("比肩", visible_ten_gods["DAY.STEM"])
        self.assertEqual("食神", visible_ten_gods["HOUR.STEM"])
        self.assertEqual(16, len(chart.affinities))

    def test_a1_exposure_links_are_explicit_and_not_root_claims(self):
        chart = self.resolve_a1().candidates[0].chart
        exposure_pairs = {
            (row.hidden_stem_instance_id, row.visible_stem_instance_id)
            for row in chart.exposures
        }
        self.assertEqual(
            {
                ("DAY.BRANCH.HIDDEN:壬", "MONTH.STEM"),
                ("HOUR.BRANCH.HIDDEN:庚", "YEAR.STEM"),
            },
            exposure_pairs,
        )
        self.assertFalse(hasattr(chart, "root_strength"))
        self.assertFalse(hasattr(chart, "strength"))
        self.assertFalse(hasattr(chart, "pattern"))
        self.assertFalse(hasattr(chart, "useful_god"))

    def test_repeated_branch_instances_remain_distinct(self):
        chart = self.resolve_a1().candidates[0].chart
        noon = [row for row in chart.branches if row.branch == "午"]
        self.assertEqual(2, len(noon))
        self.assertEqual(2, len({row.instance_id for row in noon}))
        self_punishments = [
            row for row in chart.raw_relations
            if row.semantic_relation_id == "BRANCH.PUNISHMENT.SELF.午"
        ]
        self.assertEqual(1, len(self_punishments))
        self.assertEqual(
            {"YEAR.BRANCH", "MONTH.BRANCH"},
            set(self_punishments[0].participant_instance_ids),
        )

    def test_directed_punishment_preserves_orientation(self):
        branches = (
            BranchInstance("YEAR.BRANCH", "YEAR", "寅", BRANCH_ELEMENTS["寅"]),
            BranchInstance("MONTH.BRANCH", "MONTH", "巳", BRANCH_ELEMENTS["巳"]),
        )
        relations = generate_raw_relations((), branches)
        directed = [row for row in relations if row.relation_family == "BRANCH_PUNISHMENT"]
        self.assertEqual(1, len(directed))
        self.assertEqual("DIRECTED", directed[0].orientation)
        self.assertEqual(("YEAR.BRANCH", "MONTH.BRANCH"), directed[0].participant_instance_ids)
        self.assertEqual("BRANCH.PUNISHMENT.YIN_TO_SI", directed[0].semantic_relation_id)

    def test_full_trine_is_generated_but_partial_trine_is_not(self):
        partial = (
            BranchInstance("YEAR.BRANCH", "YEAR", "申", BRANCH_ELEMENTS["申"]),
            BranchInstance("MONTH.BRANCH", "MONTH", "子", BRANCH_ELEMENTS["子"]),
        )
        self.assertFalse(
            any(row.relation_family == "BRANCH_TRINE" for row in generate_raw_relations((), partial))
        )
        full = partial + (
            BranchInstance("DAY.BRANCH", "DAY", "辰", BRANCH_ELEMENTS["辰"]),
        )
        trines = [row for row in generate_raw_relations((), full) if row.relation_family == "BRANCH_TRINE"]
        self.assertEqual(1, len(trines))
        self.assertEqual("BRANCH.TRINE.WATER", trines[0].semantic_relation_id)
        self.assertEqual("水", trines[0].nominal_transformation_element)

    def test_same_natal_with_time_uncertainty_keeps_multiple_temporal_seeds(self):
        result = self.foundation.resolve_typed(
            BaziChartRequest(
                birth=self.beijing(datetime(1990, 6, 15, 12, 0), uncertainty_seconds=120),
                profile=self.profile,
            )
        )
        self.assertEqual("RESOLVED_SINGLE_NATAL_WITH_TIME_UNCERTAINTY", result.status)
        self.assertEqual(1, len(result.candidates))
        candidate = result.candidates[0]
        self.assertGreater(len(candidate.temporal_seeds), 1)
        self.assertEqual(len(candidate.temporal_seeds), len(candidate.branch_indices))
        self.assertEqual(len(candidate.temporal_seeds), len({seed.seed_id for seed in candidate.temporal_seeds}))

    def test_natal_hashes_are_deterministic(self):
        first = self.resolve_a1().candidates[0]
        second = self.resolve_a1().candidates[0]
        self.assertEqual(first.hashes, second.hashes)
        self.assertEqual(first.chart, second.chart)

    def test_hidden_stem_registry_order_is_not_natal_fact_identity(self):
        candidate = self.resolve_a1().candidates[0]
        reordered = replace(candidate.chart, hidden_stems=tuple(reversed(candidate.chart.hidden_stems)))
        original_hashes = natal_hash_bundle(candidate.chart, self.profile)
        reordered_hashes = natal_hash_bundle(reordered, self.profile)
        self.assertEqual(original_hashes.fact_hash, reordered_hashes.fact_hash)
        self.assertNotEqual(original_hashes.computation_hash, reordered_hashes.computation_hash)


if __name__ == "__main__":
    unittest.main()
