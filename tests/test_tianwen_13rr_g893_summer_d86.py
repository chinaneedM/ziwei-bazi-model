"""Source-scoped fixed-point evidence gate for 13RR; never auto-emend a historical glyph."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/research/TIANWEN-13RR-G893-017A-SUMMER-D86-ORIGINAL-CUMULATIVE-CROSSCOPY-R1.json"

class G893SummerD86CrossCopy(unittest.TestCase):
    def test_physical_source_and_exact_integer_replay(self):
        report = json.loads(DOC.read_text(encoding="utf-8"))
        self.assertEqual(report["physical_copy"]["holding"], "奎貴893 / GK00893_00")
        self.assertEqual(report["image_acquisition"]["original_017a_jpeg"]["jpeg_sha256"],
                         "2f151dc678e277e935f947b36744fb6be4e0f99f901a868dacc14d3aa3b303e7")
        a = report["exact_integer_replay"]
        self.assertEqual(a["G893_C85_scaled"] + a["G893_M85_scaled"], a["G893_C86_scaled"])
        self.assertEqual(a["G893_C86_scaled"] - a["other_C86_scaled"], 10_000_000)
        self.assertEqual(a["difference_normalized"], "1000.0000")
        self.assertEqual(report["native_rgb_rois"][0]["correct_physical_column"], "SUMMER_DAY86_YINGSUO_CUMULATIVE")
        self.assertEqual(report["native_rgb_rois"][1]["correct_physical_column"], "SUMMER_DAY85_YINGSUO_CUMULATIVE")
        self.assertEqual(report["epistemic_scope"]["specific_six_legacy_original_historical_numeric_finals"], "0/6")
        self.assertEqual(report["epistemic_scope"]["algorithm_reopens"], 0)
        self.assertTrue(report["cross_copy"]["Waseda_and_Taiwan_not_proven_stemmatically_independent"])

if __name__ == "__main__":
    unittest.main()
