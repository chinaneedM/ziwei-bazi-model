"""Ensure bounded NLC old20 volume20 result does not become a whole-work negative."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QE-NLC-OLD20-V20-NINE-PAGE-BOUNDED-REVIEW-R1.json"
class NLC12QEOld20V20Boundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.o=json.loads(E.read_text(encoding="utf-8"))
    def test_only_source_bound_nine_pages_reviewed(self):
        d=self.o["direct_page_review"]
        self.assertEqual([x["pdf_page"] for x in d["reviewed_pages"]],list(range(137,146)))
        self.assertEqual(len({x["derived_jpeg_sha256"] for x in d["reviewed_pages"]}),9)
        self.assertEqual(d["heading_start_exact"],"萬曆肆拾伍丁巳卷二十")
        self.assertEqual(d["normalized_bibliographic_volume_label"],"萬曆野獲編卷二十")
        self.assertTrue(d["heading_text_is_not_bibliographic_label"])
        self.assertEqual(d["end_exact"],"萬曆野獲編二十卷紀事畢")
        self.assertFalse(d["target_heading_seen_within_nine_pages"])
    def test_no_false_global_absence_or_edition_identity(self):
        d=self.o["direct_page_review"]
        c=self.o["comparison"]
        self.assertFalse(d["entire_original_20_volume_work_negatively_searched"])
        self.assertFalse(d["other_original_volume_positions_checked_for_target"])
        self.assertEqual(d["target_not_in_any_other_old20_volume"],"UNRESOLVED")
        self.assertTrue(c["same_volume_number_no_equivalent_locator"])
        self.assertTrue(c["do_not_mark_original_work_absent"])
        self.assertEqual(c["same_text_other_volume_or_recension"],"UNRESOLVED")
        self.assertEqual(self.o["source"]["duplicate_witness_count_delta"],0)
    def test_product_closed(self):
        self.assertEqual(self.o["invariants"]["chart_defects"],0)
        self.assertEqual(self.o["invariants"]["algorithm_reopen"],0)
        self.assertEqual(self.o["invariants"]["product"],"CLOSED")
if __name__=="__main__":unittest.main()
