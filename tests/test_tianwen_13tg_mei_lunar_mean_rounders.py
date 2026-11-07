import json
import unittest
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/research/TIANWEN-13TG-MEI-RECEIVED-TWO-LUNAR-LIMIT-MEAN-ROUNDING-BRIDGES-R1.json"

def four_places(value, mode):
    x = value * 10000
    if mode == "CEIL":
        return -(-x.numerator // x.denominator)
    if mode == "TRUNCATE":
        return x.numerator // x.denominator
    if mode == "HALF_UP":
        return (2 * x.numerator + x.denominator) // (2 * x.denominator)
    raise AssertionError(mode)

class MeiReceivedLimitMeanRounders(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(DOC.read_text(encoding="utf-8"))
        cls.original = json.loads((ROOT / cls.doc["original_comparator"]["reference"]).read_text(encoding="utf-8"))

    def test_distinct_later_received_generators_exact(self):
        a = self.doc["exact_arithmetic"]
        daily = F(a["daily_mean"])
        self.assertEqual(daily * F(a["nominal_day_fraction"]), F(a["nominal_limit_mean_fraction"]))
        self.assertEqual(daily * F(a["half_turn_days"]), F(a["half_turn_product"]))
        self.assertEqual(daily * F(a["half_turn_days"]) / a["half_turn_limit_count"], F(a["half_turn_limit_mean_fraction"]))
        m = F(a["half_turn_limit_mean_fraction"])
        self.assertLessEqual(F(a["half_turn_mean_8dp_truncated"]), m)
        self.assertLess(m, F(a["half_turn_mean_8dp_truncated"]) + F(1, 10**8))
        self.assertNotEqual(m, F(a["nominal_limit_mean_fraction"]))

    def test_source_scoped_competing_mean_plus_rounder_fits(self):
        observed = self.original["original_rows"]
        self.assertEqual([r["limit"] for r in observed], self.doc["original_comparator"]["limits"])
        results = {}
        for model in self.doc["conditional_models"]:
            mean = F(model["mean_fraction"])
            predicted = []
            matched = 0
            for row in observed:
                q = F(row["loss_gain_magnitude_scaled_1e8_degree"], 10**8)
                ji = four_places(mean - q, model["final_four_place_rule"])
                chi = four_places(mean + q, model["final_four_place_rule"])
                predicted.append([row["limit"], ji, chi])
                matched += int(ji == row["ji_scaled_1e4_degree"])
                matched += int(chi == row["chi_scaled_1e4_degree"])
            self.assertEqual(predicted, model["predicted_limit_ji_chi"])
            self.assertEqual(matched, model["matches_out_of_10"])
            results[model["name"]] = matched
        self.assertEqual(results["NOMINAL_820_CEIL"], 10)
        self.assertEqual(results["HALF_TURN_168_TRUNCATE"], 10)
        self.assertEqual(results["NOMINAL_820_TRUNCATE_CONTROL"], 0)
        self.assertEqual(results["HALF_TURN_168_CEIL_CONTROL"], 0)
        self.assertEqual(results["HALF_TURN_168_HALF_UP_CONTROL"], 6)

    def test_source_and_algorithm_firewall(self):
        self.assertFalse(self.doc["adjudication"]["g893_native_limit_mean_proven"])
        self.assertFalse(self.doc["adjudication"]["g893_native_rounder_proven"])
        self.assertEqual(self.doc["adjudication"]["g893_six_historical_finals"], "0/6")
        self.assertEqual(self.doc["adjudication"]["new_original_physical_witnesses"], 0)
        self.assertEqual(self.doc["adjudication"]["algorithm_reopens"], 0)
        self.assertEqual(self.doc["adjudication"]["product"], "CLOSED")
        self.assertTrue(all(x["grade"].startswith("LATER_QING_RECEIVED") for x in self.doc["received_witnesses"]))

if __name__ == "__main__":
    unittest.main()
