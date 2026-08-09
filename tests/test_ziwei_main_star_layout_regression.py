from __future__ import annotations

import unittest

from fortune_training.ziwei_chart.main_stars import MainStarGenerator


class ZiweiMainStarRelativeLayoutRegressionTests(unittest.TestCase):
    def test_ziwei_group_offsets_follow_canonical_intervening_palace_semantics(self):
        expected_offsets = {
            "STAR.ZIWEI": 0,
            "STAR.TIANJI": -1,
            "STAR.TAIYANG": -3,
            "STAR.WUQU": -4,
            "STAR.TIANTONG": -5,
            "STAR.LIANZHEN": -8,
        }
        generator = MainStarGenerator()
        for ziwei_anchor in range(12):
            actual = {
                row.entity_id: (row.address.index - ziwei_anchor) % 12
                for row in generator.generate_from_ziwei_anchor(ziwei_anchor)
                if row.entity_id in expected_offsets
            }
            expected = {
                entity_id: offset % 12
                for entity_id, offset in expected_offsets.items()
            }
            self.assertEqual(expected, actual)

    def test_wenmo_chartdiff_001_lianzhen_is_yin_when_ziwei_is_xu(self):
        rows = {
            row.entity_id: row.address.branch
            for row in MainStarGenerator().generate_from_ziwei_anchor(10)
        }
        self.assertEqual("戌", rows["STAR.ZIWEI"])
        self.assertEqual("巳", rows["STAR.TIANTONG"])
        self.assertEqual("寅", rows["STAR.LIANZHEN"])


if __name__ == "__main__":
    unittest.main()
