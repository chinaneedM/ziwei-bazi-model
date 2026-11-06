import json
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs/research/TIANWEN-13SK-G893-ORIGINAL-SOLAR-POST-TABLE-TOTALS-R1.json"


class TestSolarPostTableTotals(unittest.TestCase):
    def setUp(self):
        self.evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_prose_pairs_and_models(self):
        replay = self.evidence["same_copy_replay"]
        for season, model in replay["seasons"].items():
            with self.subTest(season=season):
                full, skip = [
                    row["total_microdegrees"]
                    for row in self.evidence["post_table_original_totals"]
                    if row["season"] == season
                ]
                self.assertEqual(full - skip, model["J_initial_microdegrees"] - 1_000_000)
                self.assertEqual(full - skip, model["printed_full_minus_skip"])
                sign = model["sign"]
                end = model["end_day"]
                base = 1_000_000 * (end + 1)
                days = range(end + 1)
                day_pairs = [day * (day - 1) // 2 for day in days]
                magnitudes = [
                    model["M4_initial"] - day * model["S4_initial"] - pairs * model["step4"]
                    for day, pairs in zip(days, day_pairs)
                ]
                self.assertEqual(sum(magnitudes), model["marked_C4"])
                for start, observed in enumerate((full, skip)):
                    window = magnitudes[start:]
                    daily = base + sign * sum(value // 100 for value in window)
                    nearest = base + sign * sum((value + 50) // 100 for value in window)
                    aggregate = base + sign * Decimal(sum(window)) / 100
                    quarter_tail = aggregate - sign * Decimal(sum(day_pairs[start:])) / 400

                    self.assertEqual(daily, model["daily_truncation"][start])
                    self.assertEqual(nearest, model["daily_nearest_magnitude"][start])
                    self.assertEqual(aggregate, Decimal(model["unrounded_aggregate"][start]))
                    self.assertEqual(quarter_tail, Decimal(model["unrounded_quarter_tail_aggregate"][start]))
                    self.assertEqual(observed - daily, model["daily_truncation_residual"][start])
                    self.assertTrue(all(abs(observed - value) > 1 for value in (daily, nearest, aggregate, quarter_tail)))

    def test_prose_agreement_does_not_normalize_terminal_c(self):
        comparison = self.evidence["cross_copy"]
        self.assertEqual(
            comparison["prose_totals_microdegrees_in_same_order"],
            [row["total_microdegrees"] for row in self.evidence["post_table_original_totals"]],
        )
        erratum = comparison["terminal_C4_erratum"]
        self.assertEqual(erratum["observed_Waseda_C4"], 240135022)
        self.assertEqual(erratum["observed_G893_C4"], 240135032)
        self.assertEqual(
            erratum["observed_Waseda_C4"] - erratum["Waseda_ordinary_D93_C4"]
            - erratum["Waseda_ordinary_D93_M4"],
            -10,
        )
        self.assertEqual(comparison["repeat_capture"]["physical_vote_increment"], 0)
        self.assertEqual(self.evidence["adjudication"]["historical_G893_finals"], "0/6")


if __name__ == "__main__":
    unittest.main()
