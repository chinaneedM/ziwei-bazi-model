"""13SD: discriminate *which variable* is quantized daily in G893 solar short-lane hypotheses.
Only reads already hash-bound original G893 13RS row transcriptions; does not invent
an ancient rounding prescription or a fresh physical witness.
"""
import json
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/research/TIANWEN-13RS-G893-ORIGINAL-TWO-SEASON-SOLAR-DEGREE-PRECISION-R1.json"
BATCH = ROOT / "docs/research/TIANWEN-13SD-G893-PER-DAY-M-QUANTIZATION-STAGE-FIREWALL-R1.json"

SEASON = {
    "winter": {"m4": 5108569, "s4": 49386, "delta_micro": 18625,
               "expected": {"FLOOR": (2, 9, 2), "HALF_UP": (3, 8, 14)}},
    "summer": {"m4": 4848473, "s4": 44362, "delta_micro": 16225,
               "expected": {"FLOOR": (2, 15, 2), "HALF_UP": (4, 13, 4)}},
}


def run_model(rows, params, rounding):
    original = {int(row["day"]): int(Decimal(row["original_M_fen"]) * 10000)
                for row in rows}
    m_micro = params["m4"] * 100
    s_micro = params["s4"] * 100
    matched = []
    mismatched = []
    for day in range(max(original) + 1):
        if day in original:
            (matched if m_micro // 100 == original[day] else mismatched).append(day)
        raw = m_micro - s_micro
        m_micro = ((raw + (50 if rounding == "HALF_UP" else 0)) // 100) * 100
        s_micro += params["delta_micro"]
    return len(matched), len(mismatched), mismatched[0]


class TestG893PerDayMQuantization(unittest.TestCase):
    def test_28_source_original_pairs_and_discrimination(self):
        src = json.loads(SOURCE.read_text(encoding="utf-8"))
        doc = json.loads(BATCH.read_text(encoding="utf-8"))
        self.assertEqual(len(src["paired_rows"]), 28)
        for season, params in SEASON.items():
            rows = [r for r in src["paired_rows"] if r["season"] == season]
            self.assertEqual(len(rows), doc["results"][season]["FLOOR"]["sample_count"])
            for rounding, expected in params["expected"].items():
                got = run_model(rows, params, rounding)
                self.assertEqual(got, expected, (season, rounding))
                published = doc["results"][season][rounding]
                self.assertEqual(got[:2], (published["match_count"], published["mismatch_count"]))
                self.assertEqual(got[2], published["first_mismatch"]["day"])

    def test_no_numeric_adjudication(self):
        doc = json.loads(BATCH.read_text(encoding="utf-8"))
        self.assertEqual(doc["firewall"]["historic_numeric_finals"], 0)
        self.assertFalse(doc["firewall"]["G893_original_native_shao_wei_radix_or_carry_instruction"])
        self.assertEqual(doc["firewall"]["TW_OPEN_0005"], "OPEN")
        self.assertEqual(doc["firewall"]["algorithm_reopens"], 0)


if __name__ == "__main__":
    unittest.main()
