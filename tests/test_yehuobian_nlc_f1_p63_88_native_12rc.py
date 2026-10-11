"""12RC archive page-hash, old3/4 leaf, and non-absence proof regressions."""
import copy, importlib.util, json, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("tw12rc",ROOT/"scripts/verify_yehuobian_nlc_f1_p63_88_native_12rc.py")
MOD=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)
class Test12RC(unittest.TestCase):
    def mutate(self,fn):
        data=copy.deepcopy(MOD.read(MOD.RECORD))
        fn(data)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"mutation.json"
            p.write_text(json.dumps(data,ensure_ascii=False),encoding="utf-8")
            with self.assertRaises(ValueError):
                MOD.verify(record_path=p)
    def test_26_new_native_pages_and_no_fulltext_credit(self):
        result=MOD.verify()
        self.assertEqual(result["native_source_target_screens"],115)
        self.assertEqual(result["native_body_backlog"],913)
        self.assertEqual(result["body_full_text_collation_backlog"],1027)
        self.assertFalse(result["global_target_absence_proven"])
    def test_page_hash_tamper_rejected(self):
        self.mutate(lambda x:x["review"]["original_jpeg_sha256_by_pdf_page"].__setitem__(12,"0"*64))
    def test_mixed_juan_right_leaf_cannot_reassign(self):
        self.mutate(lambda x:x["review"]["mixed_boundary_page_88"].__setitem__("right_leaf_continues_original_juan",4))
    def test_boundary_source_page_sha_tamper_rejected(self):
        self.mutate(lambda x:x["review"]["mixed_boundary_page_88"].__setitem__("page_jpeg_sha256","0"*64))
    def test_no_negative_page_proof(self):
        self.mutate(lambda x:x["review"].__setitem__("proof_target_absent_on_any_page",True))
    def test_no_whole_manuscript_negative(self):
        self.mutate(lambda x:x["queue"].__setitem__("global_target_absence_proven",True))
    def test_no_second_physical_witness(self):
        self.mutate(lambda x:x["queue"].__setitem__("independent_physical_copy_increment",1))
    def test_no_claim_original_pdf_rehashed(self):
        self.mutate(lambda x:x["source"].__setitem__("source_pdf_binary_rehashed",True))
    def test_unearned_fulltext_queue_reduction_rejected(self):
        self.mutate(lambda x:x["queue"].__setitem__("full_text_body_collation_backlog",1001))
if __name__=="__main__": unittest.main()
