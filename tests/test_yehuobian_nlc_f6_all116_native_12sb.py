"""12SB F6 116/116 source JPEG page-chain and no-overclaim regression."""
import copy,importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("sb",ROOT/"scripts/verify_yehuobian_nlc_f6_all116_native_12sb.py")
SB=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(SB)
class Test12SB(unittest.TestCase):
    def mutation(self,change):
        data=copy.deepcopy(SB.read(SB.RECORD));change(data)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"mutation.json"
            path.write_text(json.dumps(data,ensure_ascii=False),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"12SB_"):
                SB.verify(record_path=path)
    def test_full_fascicle_source_pages(self):
        x=SB.verify()
        self.assertEqual(x["f6_native_source_pages"],116)
        self.assertEqual(x["global_native_source_pages"],574)
        self.assertEqual(x["global_preview_only_pages"],454)
        self.assertEqual(x["fulltext_body_pending"],1027)
    def test_jpeg_hash_flip(self):
        self.mutation(lambda x:x["review"]["source_jpeg_sha256_in_ascending_pdf_page_order"].__setitem__(16,"0"*64))
    def test_last_source_page_flip(self):
        self.mutation(lambda x:x["review"]["source_jpeg_sha256_in_ascending_pdf_page_order"].__setitem__(35,"0"*64))
    def test_pdf_page_range_drift(self):
        self.mutation(lambda x:x["review"].__setitem__("end_pdf_page",115))
    def test_archive_blob_sha_drift(self):
        self.mutation(lambda x:x["source"].__setitem__("zip_sha256","0"*64))
    def test_prior80_sha_drift(self):
        self.mutation(lambda x:x["review"].__setitem__("parent_12sa_p1_80_sha256_concatenated_source_jpeg_sha256","0"*64))
    def test_no_duplicate_witness(self):
        self.mutation(lambda x:x["grade_and_scope"].__setitem__("new_independent_witnesses",1))
    def test_no_false_glyph_attestation(self):
        self.mutation(lambda x:x["review"].__setitem__("old20_original_gaizao_louke_target_folio_or_glyph_positive_attestation",True))
    def test_not_fulltext(self):
        self.mutation(lambda x:x["review"].__setitem__("fulltext_character_by_character_collation_completed",True))
    def test_no_page_absence(self):
        self.mutation(lambda x:x["review"].__setitem__("any_page_negative_absence_proven",True))
    def test_no_book_absence(self):
        self.mutation(lambda x:x["review"].__setitem__("whole_20juan_work_target_absence_proven",True))
    def test_no_juan_equivalence(self):
        self.mutation(lambda x:x["review"].__setitem__("original_juan11_is_1827_themed_volume11_proven",True))
    def test_count_gate(self):
        self.mutation(lambda x:x["grade_and_scope"].__setitem__("whole_holding_preview_only_source_body_pages_after",453))
    def test_no_algorithm_reopen(self):
        self.mutation(lambda x:x["invariants"].__setitem__("algorithm_reopens",1))
if __name__=="__main__":
    unittest.main()
