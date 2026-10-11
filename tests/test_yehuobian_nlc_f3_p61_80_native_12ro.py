"""12RO protects source-anchored p61-80 SHA chain and p83 mixed leaf against promotions."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("tw12ro",ROOT/"scripts/verify_yehuobian_nlc_f3_p61_80_native_12ro.py")
GATE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)

class TestOld20F3P61To80Native12RO(unittest.TestCase):
    def mutate(self,func):
        data=copy.deepcopy(GATE.read(GATE.RECORD))
        func(data)
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"altered.json"
            p.write_text(json.dumps(data,ensure_ascii=False),encoding="utf-8")
            with self.assertRaises(ValueError):
                GATE.verify(record_path=p)

    def test_valid_contiguous_first84_fascicle3_source_pages(self):
        result=GATE.verify()
        self.assertEqual((result["f3_contiguous_native_screened"],result["f3_remaining"]),(84,37))
        self.assertEqual((result["whole_holding_native_bounded"],result["whole_holding_preview_only"]),(302,726))
        self.assertEqual(result["whole_holding_fulltext_body_untranscribed"],1027)
        self.assertFalse(result["old20_target_glyph_or_negative_text_proven"])
    def test_changed_original_image_sha(self):
        self.mutate(lambda x:x["review"]["original_jpeg_sha256_in_source_page_order"].__setitem__(7,"0"*64))
    def test_changed_source_archive_sha(self):
        self.mutate(lambda x:x["source"].__setitem__("archive_zip_sha256","0"*64))
    def test_new_pdf_binary_rehash_false_claim(self):
        self.mutate(lambda x:x["source"].__setitem__("source_pdf_binary_rehashed_in_12ro",True))
    def test_changed_84_page_chain(self):
        self.mutate(lambda x:x["review"].__setitem__("third_fascicle_p1_84_hash_chain_sha256","0"*64))
    def test_exclusive_original_juan7_page83_cannot_be_asserted(self):
        self.mutate(lambda x:x["review"].__setitem__("page83_whole_page_exclusively_juan7",True))
    def test_bogus_original_juan7_at_page80(self):
        self.mutate(lambda x:x["review"].__setitem__("page80_original_juan7_heading_directly_attested",True))
    def test_false_absence_in_whole_manuscript(self):
        self.mutate(lambda x:x["review"].__setitem__("entire_old20_manuscript_target_absence_proven",True))
    def test_bogus_complete_full_text_transcription(self):
        self.mutate(lambda x:x["review"].__setitem__("complete_linewise_text_transcription",True))
    def test_no_stemmatic_independent_copy_inflation(self):
        self.mutate(lambda x:x["queue"].__setitem__("new_independent_physical_holding_count",1))
    def test_fascicle3_pending_cannot_vanish(self):
        self.mutate(lambda x:x["queue"].__setitem__("fascicle3_native_target_pending",0))
    def test_cannot_collapse_unreviewed_85_121_window(self):
        self.mutate(lambda x:x["queue"].__setitem__("fascicle3_remaining_window",[]))

if __name__=="__main__":
    unittest.main()
