from __future__ import annotations

import unittest

from fortune_training.combined_chart_application.ziwei_basic_info_assets import (
    ZIWEI_BASIC_INFO_JS,
)


class CombinedWorkbenchZiweiLimitFlowOverlapR1Tests(unittest.TestCase):
    def test_overlap_projection_is_bound_to_typed_life_designations(self) -> None:
        self.assertIn("function limitFlowOverlap(view)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("row.designation_id !== 'LIFE'", ZIWEI_BASIC_INFO_JS)
        self.assertIn("['DAXIAN', 'ANNUAL', 'MONTH']", ZIWEI_BASIC_INFO_JS)
        self.assertIn("DAXIAN: '大限'", ZIWEI_BASIC_INFO_JS)
        self.assertIn("ANNUAL: '流年'", ZIWEI_BASIC_INFO_JS)
        self.assertIn("MONTH: '流月'", ZIWEI_BASIC_INFO_JS)
        self.assertIn("byType.size >= 2", ZIWEI_BASIC_INFO_JS)
        self.assertIn("item('限流叠宫', limitFlowOverlap(ziweiBundle?.view_model))", ZIWEI_BASIC_INFO_JS)

    def test_overlap_projection_does_not_recompute_palace_or_calendar_rules(self) -> None:
        for forbidden in (
            "NatalStructureGenerator",
            "TemporalEngine",
            "PALACE_DESIGNATIONS",
            "TimeCalendarFoundation",
            "TransformationGenerator",
            "DaxianFrame",
            "AnnualFrame",
            "MonthlyFrame",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, ZIWEI_BASIC_INFO_JS)

    def test_overlap_label_has_deterministic_frame_and_address_order(self) -> None:
        self.assertIn("temporalFrameOrder.filter", ZIWEI_BASIC_INFO_JS)
        self.assertIn(".sort(([left], [right]) => left - right)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("`${cell.stem || ''}${cell.branch || ''}`", ZIWEI_BASIC_INFO_JS)
        self.assertIn("overlaps.length ? overlaps.join('；') : '无'", ZIWEI_BASIC_INFO_JS)


if __name__ == "__main__":
    unittest.main()
