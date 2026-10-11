"""12SA F6 original source JPEG p41-80 digest and no-overclaim mutation tests."""
import copy, importlib.util, json, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("sa",ROOT/"scripts/verify_yehuobian_nlc_f6_p41_80_native_12sa.py")
SA=importlib.util.module_from_spec(spec);spec.loader.exec_module(SA)
class Test12SA(unittest.TestCase):
    def mutate(self,modify):
        original=copy.deepcopy(SA.read(SA.RECORD))
        modify(original)
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"mutated.json"
            p.write_text(json.dumps(original,ensure_ascii=False),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"12SA_"):
                SA.verify(record_path=p)
    def test_real_40_pages(self):
        out=SA.verify()
        self.assertEqual(out["new_original_pages"],40)
        self.assertEqual(out["f6_native_total"],80)
        self.assertEqual(out["whole_native_source"],538)
        self.assertEqual(out["whole_preview_source"],490)
    def test_bad_archive_identity(self):
        self.mutate(lambda x:x["source"].__setitem__("archived_artifact_id",11674845913))
    def test_window1_hash_drift(self):
        self.mutate(lambda x:x["review"]["original_source_page_windows"][0]["source_original_jpeg_sha256_in_page_order"].__setitem__(5,"0"*64))
    def test_window2_hash_drift(self):
        self.mutate(lambda x:x["review"]["original_source_page_windows"][1]["source_original_jpeg_sha256_in_page_order"].__setitem__(9,"0"*64))
    def test_page_order_shift(self):
        self.mutate(lambda x:x["review"]["original_source_page_windows"][0].__setitem__("start_pdf_page",42))
    def test_gap_or_double_count(self):
        self.mutate(lambda x:x["review"]["original_source_page_windows"][1].__setitem__("end_pdf_page",79))
    def test_inherited_chain(self):
        self.mutate(lambda x:x["review"].__setitem__("inherited_p1_40_original_jpeg_ordered_sha256","0"*64))
    def test_fulltext_is_not_done(self):
        self.mutate(lambda x:x["review"].__setitem__("full_text_character_by_character_collated",True))
    def test_no_page_absence_proof(self):
        self.mutate(lambda x:x["review"].__setitem__("any_source_page_target_absence_proven",True))
    def test_no_whole_work_absence_proof(self):
        self.mutate(lambda x:x["review"].__setitem__("whole_original_work_absence_proven",True))
    def test_no_false_target_attestation(self):
        self.mutate(lambda x:x["review"].__setitem__("positive_original_old20_gaizao_louke_title_or_passage_attestation",True))
    def test_f6_preview_backlog(self):
        self.mutate(lambda x:x["grade_union"].__setitem__("remaining_f6_preview_only_source_pages",35))
    def test_no_witness_inflation(self):
        self.mutate(lambda x:x["grade_union"].__setitem__("new_independent_physical_copy_count",1))
    def test_no_1827_juan_equivalence(self):
        self.mutate(lambda x:x["review"].__setitem__("original_juan_equivalent_to_1827_reordered_30_juan_proven",True))
    def test_no_algorithm_reopen(self):
        self.mutate(lambda x:x["invariants"].__setitem__("algorithm_reopens",1))
if __name__=="__main__":
    unittest.main()
