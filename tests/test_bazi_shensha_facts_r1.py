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

    def test_source_definitions_and_alternatives_are_all_materialized(self) -> None:
        self.assertEqual("1.4.0", self.result["profile_version"])
        self.assertEqual(32, len(self.result["candidates"]))
        self.assertEqual(
            {
                "TIANYI", "TIANGUAN", "LU", "YIMA", "HUAGAI", "YUEDE", "YUEDEHE",
                "TIANDE", "TIANCHU", "FUXING", "TAIJI", "SANQI",
                "TIANSHE", "XUETANG", "JINYU", "JIALU", "GONGLU", "YANGREN",
            },
            {row["shensha_id"] for row in self.result["candidates"]},
        )
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

    def test_tianguan_uses_source_explicit_birth_year_stem_anchor(self) -> None:
        tianguan = self.candidate("TIANGUAN", "YEAR_STEM")
        self.assertEqual("甲", tianguan["anchor_value"])
        self.assertEqual(["未"], tianguan["target_branches"])
        self.assertEqual(["HOUR"], [row["pillar_position"] for row in tianguan["occurrences"]])
        self.assertEqual("SOURCE_EXPLICIT", tianguan["selection_status"])
        self.assertEqual(
            ["S11:YHZP-USR-S00240", "S11:YHZP-CH-025"],
            tianguan["source_refs"],
        )

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

    def test_month_commanded_rules_keep_source_match_scope(self) -> None:
        yuede = self.candidate("YUEDE", "MONTH_BRANCH")
        self.assertEqual("巳", yuede["anchor_value"])
        self.assertEqual("STEM", yuede["target_kind"])
        self.assertEqual(["庚"], yuede["target_values"])
        self.assertEqual("ONLY_DAY", yuede["match_scope"])

        yuedehe = [
            row for row in self.result["candidates"]
            if row["shensha_id"] == "YUEDEHE"
        ]
        self.assertEqual({"ONLY_DAY", "ALL_PILLARS"}, {row["match_scope"] for row in yuedehe})
        self.assertTrue(all(row["selection_status"] == "CANDIDATE_NOT_ARBITRATED" for row in yuedehe))

        tiande = self.candidate("TIANDE", "MONTH_BRANCH")
        self.assertEqual("STEM", tiande["target_kind"])
        self.assertEqual(["辛"], tiande["target_values"])

    def test_stem_anchor_alternatives_never_merge(self) -> None:
        day_kitchen = self.candidate("TIANCHU", "DAY_STEM")
        year_kitchen = self.candidate("TIANCHU", "YEAR_STEM")
        self.assertEqual(["卯"], day_kitchen["target_branches"])
        self.assertEqual(["巳"], year_kitchen["target_branches"])
        self.assertNotEqual(day_kitchen["candidate_id"], year_kitchen["candidate_id"])

        day_jinyu = self.candidate("JINYU", "DAY_STEM")
        self.assertEqual(["寅"], day_jinyu["target_branches"])
        self.assertFalse(day_jinyu["present"])

    def test_jialu_requires_both_lu_neighbours_and_preserves_anchor_ambiguity(self) -> None:
        result = classical_shensha_for_pillars({
            "YEAR": "甲子", "MONTH": "乙丑", "DAY": "丁卯", "HOUR": "戊辰",
        })
        year_jialu = next(
            row for row in result["candidates"]
            if row["shensha_id"] == "JIALU" and row["anchor_basis"] == "YEAR_STEM"
        )
        day_jialu = next(
            row for row in result["candidates"]
            if row["shensha_id"] == "JIALU" and row["anchor_basis"] == "DAY_STEM"
        )
        self.assertEqual("甲", year_jialu["anchor_value"])
        self.assertEqual("BRANCH_PAIR", year_jialu["target_kind"])
        self.assertEqual(["丑", "卯"], year_jialu["target_branches"])
        self.assertEqual("BOTH_TARGET_BRANCHES_REQUIRED", year_jialu["qualification_status"])
        self.assertTrue(year_jialu["present"])
        self.assertEqual(["MONTH", "DAY"], year_jialu["occurrences"][0]["pillar_positions"])
        self.assertEqual(["丑", "卯"], year_jialu["occurrences"][0]["matched_branches"])
        self.assertEqual("CANDIDATE_NOT_ARBITRATED", year_jialu["selection_status"])
        self.assertEqual("丁", day_jialu["anchor_value"])
        self.assertEqual(["巳", "未"], day_jialu["target_branches"])
        self.assertFalse(day_jialu["present"])

        one_sided = classical_shensha_for_pillars({
            "YEAR": "甲子", "MONTH": "乙丑", "DAY": "丙寅", "HOUR": "戊辰",
        })
        one_sided_year = next(
            row for row in one_sided["candidates"]
            if row["shensha_id"] == "JIALU" and row["anchor_basis"] == "YEAR_STEM"
        )
        self.assertEqual(["丑", "卯"], one_sided_year["target_branches"])
        self.assertFalse(one_sided_year["present"])
        self.assertEqual([], one_sided_year["occurrences"])
        self.assertEqual(
            [
                "S11:YHZP-USR-S00327", "S11:YHZP-USR-S00278",
                "S11:YHZP-CH-044", "S11:YHZP-CH-034",
            ],
            one_sided_year["source_refs"],
        )

    def test_gonglu_preserves_exact_four_cases_and_anchor_ambiguity(self) -> None:
        result = classical_shensha_for_pillars({
            "YEAR": "戊辰", "MONTH": "丙午", "DAY": "甲子", "HOUR": "己巳",
        })
        year_gonglu = next(
            row for row in result["candidates"]
            if row["shensha_id"] == "GONGLU" and row["anchor_basis"] == "YEAR_GANZHI"
        )
        day_gonglu = next(
            row for row in result["candidates"]
            if row["shensha_id"] == "GONGLU" and row["anchor_basis"] == "DAY_GANZHI"
        )
        self.assertEqual("戊辰", year_gonglu["anchor_value"])
        self.assertEqual("GANZHI", year_gonglu["target_kind"])
        self.assertEqual(["丙午"], year_gonglu["target_values"])
        self.assertEqual(["MONTH"], [row["pillar_position"] for row in year_gonglu["occurrences"]])
        self.assertTrue(year_gonglu["present"])
        self.assertEqual("CANDIDATE_NOT_ARBITRATED", year_gonglu["selection_status"])
        self.assertEqual([], day_gonglu["target_values"])
        self.assertFalse(day_gonglu["present"])

        reciprocal = classical_shensha_for_pillars({
            "YEAR": "甲子", "MONTH": "丁巳", "DAY": "己未", "HOUR": "丙寅",
        })
        day_reciprocal = next(
            row for row in reciprocal["candidates"]
            if row["shensha_id"] == "GONGLU" and row["anchor_basis"] == "DAY_GANZHI"
        )
        self.assertEqual(["丁巳"], day_reciprocal["target_values"])
        self.assertEqual(["MONTH"], [row["pillar_position"] for row in day_reciprocal["occurrences"]])
        self.assertEqual(
            [
                "S11:YHZP-USR-S00315", "S11:YHZP-USR-S00316",
                "S11:YHZP-USR-S00317", "S11:YHZP-CH-041",
            ],
            day_reciprocal["source_refs"],
        )

    def test_taiji_tianshe_and_xuetang_preserve_distinct_anchor_types(self) -> None:
        taiji = self.candidate("TAIJI", "YEAR_STEM")
        self.assertEqual(["子", "午"], taiji["target_branches"])
        self.assertEqual("SOURCE_EXPLICIT", taiji["selection_status"])

        tianshe = self.candidate("TIANSHE", "MONTH_BRANCH_SEASON")
        self.assertEqual("GANZHI", tianshe["target_kind"])
        self.assertEqual(["甲午"], tianshe["target_values"])
        self.assertEqual("ONLY_DAY", tianshe["match_scope"])

        xuetang = [row for row in self.result["candidates"] if row["shensha_id"] == "XUETANG"]
        self.assertEqual(
            {"YEAR_NAYIN_ELEMENT", "DAY_NAYIN_ELEMENT"},
            {row["anchor_basis"] for row in xuetang},
        )
        self.assertTrue(all(row["qualification_status"].startswith("ORTHODOX_GANZHI:") for row in xuetang))

    def test_sanqi_requires_ordered_consecutive_stems_and_keeps_qualifier_open(self) -> None:
        result = classical_shensha_for_pillars({
            "YEAR": "甲子", "MONTH": "戊辰", "DAY": "庚申", "HOUR": "壬午",
        })
        heaven = next(
            row for row in result["candidates"]
            if row["shensha_id"] == "SANQI" and row["anchor_value"] == "HEAVEN"
        )
        self.assertTrue(heaven["present"])
        self.assertEqual(["YEAR", "MONTH", "DAY"], heaven["occurrences"][0]["pillar_positions"])
        self.assertEqual(
            "BASE_SEQUENCE_ONLY_AUXILIARY_CONDITIONS_NOT_ARBITRATED",
            heaven["qualification_status"],
        )
        reversed_result = classical_shensha_for_pillars({
            "YEAR": "庚子", "MONTH": "戊辰", "DAY": "甲申", "HOUR": "壬午",
        })
        reversed_heaven = next(
            row for row in reversed_result["candidates"]
            if row["shensha_id"] == "SANQI" and row["anchor_value"] == "HEAVEN"
        )
        self.assertFalse(reversed_heaven["present"])


if __name__ == "__main__":
    unittest.main()
