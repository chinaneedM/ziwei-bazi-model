import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "docs" / "research"
EVIDENCE = RESEARCH / "TIANWEN-13SN-G893-SOLAR-PER-DAY-ROUNDING-ENVELOPE-R1.json"
ORIGINAL = RESEARCH / "TIANWEN-13SM-G893-COMPLETE-SOLAR-DAILY-DIFFERENCE-AND-DEGREE-R1.json"
PROSE = RESEARCH / "TIANWEN-13SK-G893-ORIGINAL-SOLAR-POST-TABLE-TOTALS-R1.json"


class TestG893SolarRoundingEnvelope(unittest.TestCase):
    def test_all_daily_bounds_and_original_rows(self):
        report = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        original = json.loads(ORIGINAL.read_text(encoding="utf-8"))
        prose = json.loads(PROSE.read_text(encoding="utf-8"))
        for season_name in ("winter", "summer"):
            with self.subTest(season=season_name):
                season = original["seasons"][season_name]
                expected = report["bounds"][season_name]
                low, high, nonintegral = [], [], 0
                M4 = season["M4_initial"]
                for day, _, _, _, observed_J in season["J"]:
                    floor = M4 // 100
                    ceil = (M4 + 99) // 100
                    if M4 % 100:
                        nonintegral += 1
                    self.assertEqual(observed_J, 1_000_000 + season["sign"] * floor)
                    if season["sign"] > 0:
                        low.append(1_000_000 + floor)
                        high.append(1_000_000 + ceil)
                    else:
                        low.append(1_000_000 - ceil)
                        high.append(1_000_000 - floor)
                    M4 -= season["S4_initial"] + day * season["step4"]
                self.assertEqual(len(low), expected["day_count"])
                self.assertEqual(nonintegral, expected["M4_mod_100_nonzero_count"])
                self.assertEqual([sum(low), sum(high)], expected["full_allowable_microdegrees"])
                self.assertEqual(
                    [1_000_000 + sum(low[1:]), 1_000_000 + sum(high[1:])],
                    expected["skip_allowable_microdegrees"],
                )
                targets = [x["total_microdegrees"] for x in prose["post_table_original_totals"] if x["season"] == season_name]
                self.assertEqual(targets, [expected["original_full_microdegrees"], expected["original_skip_microdegrees"]])
                for position, field in enumerate(("full", "skip")):
                    a, b = expected[field + "_allowable_microdegrees"]
                    target = targets[position]
                    self.assertEqual(a <= target <= b, expected[field + "_inside"])
        self.assertFalse(report["bounds"]["summer"]["full_inside"])
        self.assertFalse(report["bounds"]["summer"]["skip_inside"])
        self.assertEqual(report["bounds"]["summer"]["original_full_microdegrees"] - report["bounds"]["summer"]["full_allowable_microdegrees"][1], 20)
        self.assertEqual(report["bounds"]["summer"]["original_skip_microdegrees"] - report["bounds"]["summer"]["skip_allowable_microdegrees"][1], 20)

    def test_no_unjustified_historical_closure(self):
        report = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        adjudication = report["adjudication"]
        self.assertEqual(adjudication["original_g893_shao_wei_carry"], "OPEN")
        self.assertEqual(adjudication["historical_numeric_finals"], "0/6")
        self.assertEqual(adjudication["algorithm_reopens"], 0)
        self.assertEqual(adjudication["deterministic_chart_product"], "CLOSED")
        self.assertEqual(adjudication["source_registry_delta"], 0)
        self.assertEqual(adjudication["genealogy_delta"], 0)


if __name__ == "__main__":
    unittest.main()
