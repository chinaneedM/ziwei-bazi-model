from __future__ import annotations

import unittest

from fortune_training.ziwei_chart.four_transformation_historical_candidates import (
    FOUR_TRANSFORMATION_HISTORICAL_SELECTION_STATUS,
    FULLBOOK_SHIDIAN_CANDIDATE_ID,
    FULLBOOK_SHIDIAN_TABLE,
    ZHONGZHOU_WANGTINGZHI_CANDIDATE_ID,
    ZHONGZHOU_WANGTINGZHI_TABLE,
    historical_four_transformation_candidate_payload,
    resolve_historical_four_transformation_candidate,
)
from fortune_training.ziwei_chart.transformations import TransformationGenerator


class FourTransformationHistoricalCandidatesTest(unittest.TestCase):
    stems = tuple("甲乙丙丁戊己庚辛壬癸")
    types = ("化禄", "化权", "化科", "化忌")

    @staticmethod
    def current_table() -> dict[str, tuple[str, ...]]:
        return {
            stem: tuple(row.target_display_name for row in TransformationGenerator.assignments(stem))
            for stem in FourTransformationHistoricalCandidatesTest.stems
        }

    def test_registry_is_whole_table_only_and_unselected(self) -> None:
        payload = historical_four_transformation_candidate_payload()
        self.assertTrue(payload["whole_table_only"])
        self.assertFalse(payload["cell_level_hybridization_allowed"])
        self.assertEqual(
            "PRESERVED_NOT_SELECTED",
            FOUR_TRANSFORMATION_HISTORICAL_SELECTION_STATUS,
        )
        self.assertEqual(
            {FULLBOOK_SHIDIAN_CANDIDATE_ID, ZHONGZHOU_WANGTINGZHI_CANDIDATE_ID},
            set(payload["candidate_ids"]),
        )

    def test_fullbook_shidian_table_is_complete_and_differs_only_at_three_cells(self) -> None:
        current = self.current_table()
        mismatches = {
            (stem, self.types[index], current[stem][index], FULLBOOK_SHIDIAN_TABLE[stem][index])
            for stem in self.stems
            for index in range(4)
            if current[stem][index] != FULLBOOK_SHIDIAN_TABLE[stem][index]
        }
        self.assertEqual(
            {
                ("庚", "化科", "太阴", "天同"),
                ("庚", "化忌", "天同", "天相"),
                ("壬", "化科", "左辅", "天府"),
            },
            mismatches,
        )

    def test_zhongzhou_table_is_complete_and_differs_only_at_three_cells(self) -> None:
        current = self.current_table()
        mismatches = {
            (stem, self.types[index], current[stem][index], ZHONGZHOU_WANGTINGZHI_TABLE[stem][index])
            for stem in self.stems
            for index in range(4)
            if current[stem][index] != ZHONGZHOU_WANGTINGZHI_TABLE[stem][index]
        }
        self.assertEqual(
            {
                ("戊", "化科", "右弼", "太阳"),
                ("庚", "化科", "太阴", "天府"),
                ("壬", "化科", "左辅", "天府"),
            },
            mismatches,
        )

    def test_source_scoped_resolver_returns_one_candidate_family_at_a_time(self) -> None:
        for candidate_id in (FULLBOOK_SHIDIAN_CANDIDATE_ID, ZHONGZHOU_WANGTINGZHI_CANDIDATE_ID):
            for stem in self.stems:
                payload = resolve_historical_four_transformation_candidate(
                    candidate_id=candidate_id,
                    source_stem=stem,
                )
                self.assertEqual("PRESERVED_NOT_SELECTED", payload["selection_status"])
                self.assertTrue(payload["whole_table_only"])
                self.assertEqual(candidate_id, payload["candidate_id"])
                self.assertEqual(4, len(payload["assignments"]))
                self.assertTrue(payload["registry_hash"])
                self.assertTrue(payload["runtime_hash"])

    def test_invalid_candidate_and_stem_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported Four-Transformation historical candidate"):
            resolve_historical_four_transformation_candidate(candidate_id="HYBRID", source_stem="甲")
        with self.assertRaisesRegex(ValueError, "unsupported Four-Transformation source stem"):
            resolve_historical_four_transformation_candidate(
                candidate_id=FULLBOOK_SHIDIAN_CANDIDATE_ID,
                source_stem="X",
            )


if __name__ == "__main__":
    unittest.main()
