"""12RN: preserve direct p83 left folio heading and prevent whole-page misattribution."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("tw12rn",ROOT/"scripts/verify_yehuobian_nlc_f3_mixed_juan7_12rn.py")
GATE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)
class TestF3DirectOriginalJuan7MixedBoundary12RN(unittest.TestCase):
    def mutate(self,fn):
        r=copy.deepcopy(GATE.read(GATE.RECORD))
        fn(r)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"mutated.json"
            p.write_text(json.dumps(r,ensure_ascii=False),encoding="utf-8")
            with self.assertRaises(ValueError):
                GATE.verify(record_path=p)
    def test_real_p83_left_leaf_direct_heading(self):
        result=GATE.verify()
        self.assertEqual(result["mixed_pdf_page"],83)
        self.assertEqual(result["original_juan7_heading"],"萬曆三十二年甲辰卷七")
        self.assertEqual((result["whole_native_bounded_pages"],result["preview_only_backlog"]),(282,746))
        self.assertEqual(result["fascicle3_native_remaining"],57)
        self.assertEqual(result["whole_body_fulltext_collation_pending"],1027)
        self.assertFalse(result["target_old20_gaizao_louke_attested"])
    def test_mutate_p83_source_jpeg_sha(self):
        self.mutate(lambda x:x["review"]["source_page_sha256_in_order"].__setitem__(2,"0"*64))
    def test_false_whole_page83_exclusive_juan7(self):
        self.mutate(lambda x:x["review"].__setitem__("full_pdf_page83_assigned_exclusively_to_juan7",True))
    def test_false_right_leaf_juan6_heading(self):
        self.mutate(lambda x:x["review"].__setitem__("pdf_p83_right_leaf_original_juan6_direct_heading_visible",True))
    def test_juan7_original_heading_glyph_tampered(self):
        self.mutate(lambda x:x["review"].__setitem__("source_direct_juan7_heading_text","萬曆三十年甲辰卷七"))
    def test_p83_left_to_right_swap(self):
        self.mutate(lambda x:x["review"].__setitem__("heading_directly_seen_on","F3 PDF P83 RIGHT ORIGINAL LEAF"))
    def test_falsely_locate_gaizao_louke(self):
        self.mutate(lambda x:x["review"].__setitem__("old20_gaizao_louke_target_heading_or_folio_attested",True))
    def test_false_work_absence(self):
        self.mutate(lambda x:x["review"].__setitem__("whole_work_target_absence_proven",True))
    def test_pdf_not_newly_hashed(self):
        self.mutate(lambda x:x["source"].__setitem__("source_pdf_binary_rehashed_in_batch",True))
    def test_noncontiguous_native_regions_not_collapsed(self):
        self.mutate(lambda x:x["queue"].__setitem__("fascicle3_native_bounded_regions",[[1,64]]))
    def test_wrong_remaining_count(self):
        self.mutate(lambda x:x["queue"].__setitem__("fascicle3_native_bounded_pending_pages",0))
if __name__=="__main__":
    unittest.main()
