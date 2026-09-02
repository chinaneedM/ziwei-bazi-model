from __future__ import annotations

import unittest

from fortune_training.bazi_application.shensha import (
    FEIREN_BRANCH_BY_STEM,
    SOURCE_REFS,
    YANGREN_BY_STEM,
    classical_shensha_for_pillars,
)
from fortune_training.bazi_application.temporal_shensha import (
    temporal_shensha_target_projection,
)


EXPECTED_FEIREN = {
    "甲": ("酉",), "乙": ("戌",), "丙": ("子",), "丁": ("丑",),
    "戊": ("子",), "己": ("丑",), "庚": ("卯",), "辛": ("辰",),
    "壬": ("午",), "癸": ("未",),
}
EXPECTED_REFS = [f"S11:YHZP-USR-S{number:05d}" for number in range(378, 389)]


class BaziFeirenShenshaR1Tests(unittest.TestCase):
    @staticmethod
    def source() -> dict:
        return classical_shensha_for_pillars(
            {
                "YEAR": "甲子",
                "MONTH": "辛酉",
                "DAY": "癸未",
                "HOUR": "乙丑",
            }
        )

    @staticmethod
    def candidate(source: dict, basis: str) -> dict:
        return next(
            row for row in source["candidates"]
            if row["shensha_id"] == "FEIREN" and row["anchor_basis"] == basis
        )

    def test_all_ten_source_explicit_mappings_and_refs_are_frozen(self) -> None:
        self.assertEqual(EXPECTED_FEIREN, FEIREN_BRANCH_BY_STEM)
        self.assertEqual(EXPECTED_REFS, list(SOURCE_REFS["FEIREN"]))

    def test_year_and_day_stem_candidates_remain_separate_without_winner(self) -> None:
        source = self.source()
        year = self.candidate(source, "YEAR_STEM")
        day = self.candidate(source, "DAY_STEM")

        self.assertEqual("甲", year["anchor_value"])
        self.assertEqual(["酉"], year["target_values"])
        self.assertEqual(["MONTH"], [row["pillar_position"] for row in year["occurrences"]])
        self.assertEqual("癸", day["anchor_value"])
        self.assertEqual(["未"], day["target_values"])
        self.assertEqual(["DAY"], [row["pillar_position"] for row in day["occurrences"]])

        for row in (year, day):
            self.assertEqual("BRANCH", row["target_kind"])
            self.assertEqual("ALL_PILLARS", row["match_scope"])
            self.assertEqual("CANDIDATE_NOT_ARBITRATED", row["selection_status"])
            self.assertEqual(EXPECTED_REFS, row["source_refs"])
        self.assertNotEqual(year["candidate_id"], day["candidate_id"])
        self.assertEqual("NO_WINNER_NO_IMPLICIT_MERGE", source["selection_semantics"])
        self.assertEqual("FACTS_ONLY_NO_INTERPRETATION", source["semantic_scope"])

    def test_feiren_is_independent_from_yangren_runtime_and_provenance(self) -> None:
        self.assertEqual(
            {
                "甲": ("卯",), "丙": ("午",), "戊": ("午",),
                "庚": ("酉",), "壬": ("子",),
            },
            YANGREN_BY_STEM,
        )
        self.assertNotEqual(SOURCE_REFS["YANGREN"], SOURCE_REFS["FEIREN"])
        source = self.source()
        yangren_year = next(
            row for row in source["candidates"]
            if row["shensha_id"] == "YANGREN" and row["anchor_basis"] == "YEAR_STEM"
        )
        self.assertEqual(["卯"], yangren_year["target_values"])
        self.assertEqual(
            ["S11:YHZP-USR-S00282", "S11:YHZP-USR-S02740", "S11:YHZP-CH-224"],
            yangren_year["source_refs"],
        )

    def test_generic_temporal_branch_projection_automatically_carries_feiren(self) -> None:
        source = self.source()
        projection = temporal_shensha_target_projection(
            source,
            dayun_kind="DAYUN",
            dayun_frame={"frame_id": "DU:1", "ganzhi": "辛酉"},
            xiaoyun_candidates=[],
            annual_frame={"frame_id": "Y:1", "ganzhi": "辛酉"},
            monthly_frame={"frame_id": "M:1", "ganzhi": "乙未"},
            daily_frame={"frame_id": "D:1", "ganzhi": "癸未"},
            hourly_frame={"frame_id": "H:1", "ganzhi": "辛酉"},
        )
        year = self.candidate(source, "YEAR_STEM")
        day = self.candidate(source, "DAY_STEM")

        def match_ids(slot: dict) -> set[str]:
            return {row["source_candidate_id"] for row in slot["matches"]}

        self.assertIn(year["candidate_id"], match_ids(projection["dayun"]))
        self.assertIn(year["candidate_id"], match_ids(projection["annual"]))
        self.assertIn(year["candidate_id"], match_ids(projection["hourly"]))
        self.assertIn(day["candidate_id"], match_ids(projection["monthly"]))
        self.assertIn(day["candidate_id"], match_ids(projection["daily"]))

        projected = next(
            row for row in projection["annual"]["matches"]
            if row["source_candidate_id"] == year["candidate_id"]
        )
        self.assertEqual("BRANCH", projected["target_kind"])
        self.assertEqual("酉", projected["matched_value"])
        self.assertEqual("CANDIDATE_NOT_ARBITRATED", projected["source_selection_status"])
        self.assertEqual("NOT_CLASSICALLY_ARBITRATED", projected["temporal_applicability_status"])
        self.assertEqual(EXPECTED_REFS, projected["source_refs"])


if __name__ == "__main__":
    unittest.main()
