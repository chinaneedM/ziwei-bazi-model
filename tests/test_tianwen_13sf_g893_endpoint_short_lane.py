from decimal import Decimal
import json
from pathlib import Path
import unittest


EVIDENCE = (
    Path(__file__).resolve().parents[1] / "docs" / "research"
    / "TIANWEN-13SF-G893-SOLAR-ENDPOINT-SHORT-LANE-AND-GORYEOSA-PRINT-VARIANTS-R1.json"
)


class G893EndpointShortLaneTests(unittest.TestCase):
    def setUp(self):
        self.evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        self.rows = {
            (row["copy"], row["season"]): row for row in self.evidence["original_rows"]
        }

    def test_short_lane_variants_do_not_fill_original_blanks(self):
        for season, marker in (("winter", "九一"), ("summer", "七一")):
            with self.subTest(season=season):
                source = self.rows["G893", season]
                comparator = self.rows["Waseda", season]
                self.assertEqual(source["terminal"]["header_small_glyphs"], marker)
                self.assertEqual(comparator["terminal"]["header_small_glyphs"], marker)
                for section in ("regular", "terminal"):
                    self.assertEqual(source[section]["S_literal"], "空")
                    self.assertIsNone(source[section]["S4"])
                self.assertIsNone(source["terminal"]["M4"])
                replay = self.evidence["exact_replay"][season]
                previous = replay["G893_D87_S4" if season == "winter" else "G893_D92_S4"]
                displayed_step = replay["displayed_step4"]
                self.assertEqual(comparator["regular"]["S4"], previous + displayed_step)
                if season == "winter":
                    self.assertEqual(comparator["terminal"]["S4"], previous + 2 * displayed_step)
                else:
                    self.assertIsNone(comparator["terminal"]["S4"])

    def test_cumulative_step_is_full_last_addend_in_g893(self):
        for season, candidate_fraction in (("winter", "0.91"), ("summer", "0.71")):
            with self.subTest(season=season):
                source = self.rows["G893", season]
                comparator = self.rows["Waseda", season]
                increment = source["terminal"]["C4"] - source["regular"]["C4"]
                self.assertEqual(increment, source["regular"]["M4"])
                self.assertNotEqual(increment, source["regular"]["M4"] * Decimal(candidate_fraction))
                comparator_increment = comparator["terminal"]["C4"] - comparator["regular"]["C4"]
                self.assertEqual(comparator_increment - comparator["regular"]["M4"], int(season == "winter"))
