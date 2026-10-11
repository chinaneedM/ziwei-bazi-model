"""12RS direct fascicle4 original-source image ledger regressions."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("tw12rs", ROOT/"scripts/verify_yehuobian_nlc_f4_p1_20_native_12rs.py")
GATE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)

class TestFascicle4NativeFirstTwenty12RS(unittest.TestCase):
    def tamper(self,fn):
        rec=copy.deepcopy(GATE.read(GATE.DATA))
        fn(rec)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"tampered.json"
            p.write_text(json.dumps(rec,ensure_ascii=False),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"12RS_"):
                GATE.verify(record_path=p)
    def test_direct_bounded_first_twenty(self):
        result=GATE.verify()
        self.assertEqual(result["original_individual_pages_reviewed"],20)
        self.assertTrue(result["archive_jpeg_sha_and_size_56_checked"])
        self.assertFalse(result["whole_book_global_unique_page_recounted"])
        self.assertEqual(result["full_text_body_pages_still_pending"],1027)
    def test_source_page_pin_mutation(self):
        self.tamper(lambda d:d["review"]["source_jpeg_sha256_in_pdf_order"].__setitem__(6,"0"*64))
    def test_wrong_original_volume(self):
        self.tamper(lambda d:d["review"].__setitem__("source_p1_direct_volume_heading","卷九"))
    def test_wrong_zip_sha(self):
        self.tamper(lambda d:d["source"].__setitem__("archive_zip_sha256","0"*64))
    def test_false_pdf_binary_rehash(self):
        self.tamper(lambda d:d["source"].__setitem__("source_pdf_binary_rehashed_in_12rs",True))
    def test_negative_text_claim_forbidden(self):
        self.tamper(lambda d:d["review"].__setitem__("whole_old20_work_target_absence_proven",True))
    def test_1827_identity_not_promoted(self):
        self.tamper(lambda d:d["review"].__setitem__("same_as_1827_fulishanfang_original_juan_or_direct_copy_proven",True))
    def test_fulltext_not_collated(self):
        self.tamper(lambda d:d["review"].__setitem__("full_text_linewise_collation_completed",True))
    def test_global_coverage_not_double_counted(self):
        self.tamper(lambda d:d["queue"].__setitem__("new_whole_holding_native_bounded_pages_reported",359))
    def test_parent_batch_stage_distinct(self):
        self.tamper(lambda d:d.__setitem__("parent_open_batch","12QE_OPEN"))

if __name__=="__main__":
    unittest.main()
