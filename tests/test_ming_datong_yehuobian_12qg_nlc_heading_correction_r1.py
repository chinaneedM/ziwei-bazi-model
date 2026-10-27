"""Source-scoped forward-only correction: original old20v volume20 literal heading."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
READ=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QE-NLC-OLD20-V20-NINE-PAGE-BOUNDED-REVIEW-R1.json"
CORRECTION=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QG-NLC-OLD20-V20-HEADING-FORWARD-CORRECTION-R1.json"
EARLIER=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12PZ-OLD20-VOLUME-HEADING-CROSSWALK-R1.json"
class Old20V20SourceHeadingCorrectionGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.read=json.loads(READ.read_text(encoding="utf-8"))
        cls.c=json.loads(CORRECTION.read_text(encoding="utf-8"))
        cls.earlier=json.loads(EARLIER.read_text(encoding="utf-8"))
    def test_literal_must_not_equal_normalized_bibliography(self):
        d=self.read["direct_page_review"]
        self.assertEqual(self.c["corrected_literal_heading"],"萬曆肆拾伍丁巳卷二十")
        self.assertEqual(d["heading_start_exact"],self.c["corrected_literal_heading"])
        self.assertEqual(d["normalized_bibliographic_volume_label"],"萬曆野獲編卷二十")
        self.assertNotEqual(d["heading_start_exact"],d["normalized_bibliographic_volume_label"])
        self.assertEqual(self.earlier["revision_history"][0]["corrected_value"],d["heading_start_exact"])
    def test_exact_source_and_distinct_end_colophon(self):
        s=self.c["source_identity"]
        self.assertEqual(s["source_pdf_page"],137)
        self.assertEqual(s["source_pdf_sha256"],self.read["source"]["source_pdf_sha256"])
        self.assertEqual(s["derived_fullpage_jpeg_sha256_from_12qe_review"],next(p["derived_jpeg_sha256"] for p in self.read["direct_page_review"]["reviewed_pages"] if p["pdf_page"]==137))
        self.assertEqual(self.read["direct_page_review"]["end_exact"],"萬曆野獲編二十卷紀事畢")
        self.assertTrue(self.c["actual_lineage"]["not_same_literal_as_start"])
    def test_forward_correction_does_not_invent_new_witness_or_algorithm(self):
        h=self.read["forward_only_revision_history"][-1]
        self.assertEqual(h["previous_literal_recorded"],self.c["previous_12qe_recorded_heading"])
        self.assertEqual(h["corrected_literal"],self.c["corrected_literal_heading"])
        self.assertEqual(self.c["invariants"]["new_independent_witnesses"],0)
        self.assertEqual(self.c["invariants"]["algorithm_reopen"],0)
        self.assertFalse(self.c["invariants"]["batch_12qe_closed"])
        self.assertEqual(self.read["source"]["duplicate_witness_count_delta"],0)
        self.assertFalse(self.read["direct_page_review"]["entire_original_20_volume_work_negatively_searched"])
if __name__=="__main__": unittest.main()
