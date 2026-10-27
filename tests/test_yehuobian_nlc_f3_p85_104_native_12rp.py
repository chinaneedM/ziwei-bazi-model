"""12RP F3 p85–104 exact source SHA chain with counter and false glyph grade regressions."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("tw12rp",ROOT/"scripts/verify_yehuobian_nlc_f3_p85_104_native_12rp.py")
GATE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)

class TestF3Native85To104_12RP(unittest.TestCase):
    def fake(self,operation):
        record=copy.deepcopy(GATE.read(GATE.RECORD))
        operation(record)
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"fake.json"
            path.write_text(json.dumps(record,ensure_ascii=False),encoding="utf-8")
            with self.assertRaises(ValueError):
                GATE.verify(record_path=path)
    def test_native_source_104_first_pages(self):
        r=GATE.verify()
        self.assertEqual((r["fascicle3_contiguous_native_bounded_reviewed"],
                          r["fascicle3_remaining_native_review_pages"]),(104,17))
        self.assertEqual((r["whole_holding_native_bounded"],r["whole_holding_preview_only"]),(322,706))
        self.assertEqual(r["whole_holding_fulltext_body_untranscribed"],1027)
        self.assertFalse(r["target_old20_gaizao_louke_glyph_or_absence_proof"])
    def test_image_source_sha_mutation(self):
        self.fake(lambda x:x["review"]["original_source_jpeg_sha256_in_order"].__setitem__(9,"0"*64))
    def test_old_juan7_heading_mutation(self):
        self.fake(lambda x:x["review"].__setitem__("direct_original_juan7_heading_in_source_pdf_p83_left_leaf","卷六"))
    def test_false_new_juan8_title(self):
        self.fake(lambda x:x["review"].__setitem__("new_original_juan8_title_directly_seen",True))
    def test_pdf_rehash_invention(self):
        self.fake(lambda x:x["source"].__setitem__("source_pdf_binary_rehashed_in_12rp",True))
    def test_false_target_absence(self):
        self.fake(lambda x:x["review"].__setitem__("whole_old20_work_target_absence_proven",True))
    def test_false_fulltext_completion(self):
        self.fake(lambda x:x["review"].__setitem__("complete_text_collation_performed",True))
    def test_1827_original_juan_equivalence_invention(self):
        self.fake(lambda x:x["review"].__setitem__("print1827_30juan_copy_equated",True))
    def test_unread_pages_not_closed(self):
        self.fake(lambda x:x["queue"].__setitem__("fascicle3_pending_native_target_screen_pages",0))
    def test_unread_total_body_not_closed(self):
        self.fake(lambda x:x["queue"].__setitem__("whole_holding_full_text_body_collation_pending",0))
    def test_new_physical_witness_inflation(self):
        self.fake(lambda x:x["queue"].__setitem__("independent_physical_copy_increment",1))

if __name__=="__main__":
    unittest.main()
