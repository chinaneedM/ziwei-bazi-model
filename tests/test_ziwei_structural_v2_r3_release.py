from __future__ import annotations

import unittest

from fortune_training.ziwei_chart.main_stars import TIANFU_GROUP, ZIWEI_GROUP
from fortune_training.ziwei_structural.r3 import FOURTEEN_MAIN_STAR_ENTITY_IDS


class ZiweiStructuralV2R3ReleaseTests(unittest.TestCase):
    def test_borrow_emptiness_domain_is_exactly_the_frozen_physical_main_star_generator(self) -> None:
        expected = frozenset(row[0] for row in (*ZIWEI_GROUP, *TIANFU_GROUP))
        self.assertEqual(14, len(expected))
        self.assertEqual(expected, FOURTEEN_MAIN_STAR_ENTITY_IDS)
        self.assertEqual(6, len(ZIWEI_GROUP))
        self.assertEqual(8, len(TIANFU_GROUP))
        self.assertFalse(set(row[0] for row in ZIWEI_GROUP) & set(row[0] for row in TIANFU_GROUP))


if __name__ == "__main__":
    unittest.main()
