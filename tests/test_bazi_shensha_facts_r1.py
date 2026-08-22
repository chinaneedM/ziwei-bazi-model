from __future__ import annotations

import unittest

from fortune_training.bazi_application import (
    classical_shensha_for_pillars,
    validate_shensha_registries,
)


class BaziShenshaFactsR1Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.pillars = {
            "YEAR": "甲戌",
            "MONTH": "己巳",
            "DAY": "癸卯",
            "HOUR": "己未",
        }
        self.result = classical_shensha_for_pillars(self.pillars)

    def candidate(self, shensha_id: str, anchor_basis: str) -> dict:
        return next(
            row
            for row in self.result["candidates"]
            if row["shensha_id"] == shensha_id and row["anchor_basis"] == anchor_basis
        )

    def test_four_source_definitions_preserve_two_anchor_candidates_each(self) -> None:
        self.assertEqual(8, len(self.result["candidates"]))
        self.assertEqual("UNRESOLVED_CLASSICAL_ANCHOR_ALTERNATIVES", self.result["resolution_status"])
        self.assertEqual("NO_WINNER_NO_IMPLICIT_MERGE", self.result["selection_semantics"])

    def test_tianyi_and_lu_use_exact_yuanhai_tables(self) -> None:
        tianyi = self.candidate("TIANYI", "DAY_STEM")
        self.assertEqual("癸", tianyi["anchor_value"])
        self.assertEqual(["卯", "巳"], tianyi["target_branches"])
        self.assertEqual(["MONTH", "DAY"], [row["pillar_position"] for row in tianyi["occurrences"]])
        lu = self.candidate("LU", "DAY_STEM")
        self.assertEqual(["子"], lu["target_branches"])
        self.assertFalse(lu["present"])

    def test_yima_and_huagai_keep_day_and_year_branch_candidates_separate(self) -> None:
        day_yima = self.candidate("YIMA", "DAY_BRANCH")
        year_yima = self.candidate("YIMA", "YEAR_BRANCH")
        self.assertEqual(["巳"], day_yima["target_branches"])
        self.assertEqual(["申"], year_yima["target_branches"])
        self.assertTrue(day_yima["present"])
        self.assertFalse(year_yima["present"])
        day_huagai = self.candidate("HUAGAI", "DAY_BRANCH")
        year_huagai = self.candidate("HUAGAI", "YEAR_BRANCH")
        self.assertEqual(["未"], day_huagai["target_branches"])
        self.assertEqual(["戌"], year_huagai["target_branches"])
        self.assertTrue(day_huagai["present"])
        self.assertTrue(year_huagai["present"])

    def test_results_are_identity_only_and_invalid_inputs_fail_closed(self) -> None:
        validate_shensha_registries()
        self.assertTrue(
            all(row["semantic_scope"] == "IDENTITY_MATCH_ONLY_NO_AUSPICIOUSNESS" for row in self.result["candidates"])
        )
        with self.assertRaises(ValueError):
            classical_shensha_for_pillars({"YEAR": "甲戌"})


if __name__ == "__main__":
    unittest.main()
