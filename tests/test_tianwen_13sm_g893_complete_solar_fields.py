import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "docs" / "research"
EVIDENCE = RESEARCH / "TIANWEN-13SM-G893-COMPLETE-SOLAR-DAILY-DIFFERENCE-AND-DEGREE-R1.json"
PROSE = RESEARCH / "TIANWEN-13SK-G893-ORIGINAL-SOLAR-POST-TABLE-TOTALS-R1.json"


class TestCompleteG893SolarFields(unittest.TestCase):
    def test_source_rows_and_recurrence(self):
        data = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        images = data["source"]["images"]
        self.assertEqual(len(images), 35)
        for name, end in (("winter", 88), ("summer", 93)):
            with self.subTest(season=name):
                season = data["seasons"][name]
                for field in ("S", "J"):
                    rows = season[field]
                    self.assertEqual([row[0] for row in rows], list(range(end + 1)))
                    for _, folio, (left, top, right, bottom), digest, _ in rows:
                        self.assertIn(folio, images)
                        self.assertTrue(0 <= left < right <= 1150)
                        self.assertTrue(0 <= top < bottom <= 2000)
                        self.assertRegex(digest, r"^[0-9a-f]{64}$")

                initial = season["S4_initial"]
                step = season["step4"]
                self.assertEqual(
                    [row[-1] for row in season["S"]],
                    [initial + day * step for day in range(end)] + [None],
                )

                addend = season["M4_initial"]
                for day, _, _, _, observed in season["J"]:
                    expected = 1_000_000 + season["sign"] * (addend // 100)
                    self.assertEqual(observed, expected, (name, day))
                    addend -= initial + day * step

    def test_sum_of_printed_degrees_differs_from_printed_prose(self):
        data = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        prose = json.loads(PROSE.read_text(encoding="utf-8"))
        for name, residual in (("winter", 27), ("summer", 20)):
            with self.subTest(season=name):
                season = data["seasons"][name]
                daily = [row[-1] for row in season["J"]]
                direct_sums = [sum(daily), 1_000_000 + sum(daily[1:])]
                original_totals = [
                    row["total_microdegrees"] for row in prose["post_table_original_totals"]
                    if row["season"] == name
                ]
                self.assertEqual(direct_sums, season["printed_J_sums_microdegrees"])
                self.assertEqual(original_totals, season["printed_prose_totals_microdegrees"])
                self.assertEqual(
                    [original - daily_sum for original, daily_sum in zip(original_totals, direct_sums)],
                    [residual, residual],
                )
                self.assertEqual(season["prose_minus_printed_J_sum_microdegrees"], [residual, residual])

        self.assertEqual(data["adjudication"]["g893_native_shao_wei_carry"], "OPEN")
        self.assertEqual(data["adjudication"]["historical_numeric_finals"], "0/6")
