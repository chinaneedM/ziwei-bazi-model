"""12RB source scope and non-absence proof regression."""
import copy,importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("tw12rb",ROOT/"scripts/verify_yehuobian_nlc_f1_p43_62_native_12rb.py")
M=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(M)
class Test12RB(unittest.TestCase):
    def mutate(self,fn):
        j=copy.deepcopy(M.read(M.RECORD));fn(j)
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"mutation.json";p.write_text(json.dumps(j,ensure_ascii=False),encoding="utf-8")
            with self.assertRaises(ValueError):M.verify(record_path=p)
    def test_queue_and_scope(self):
        r=M.verify();self.assertEqual(r["native_body_backlog"],939)
        self.assertEqual(r["fulltext_body_backlog"],1027)
        self.assertFalse(r["target_absence_proven"])
    def test_source_hash_tamper(self):
        self.mutate(lambda j:j["review"]["source_image_sha256_by_pdf_page"].__setitem__(1,"0"*64))
    def test_no_copy_inflation(self):
        self.mutate(lambda j:j["queue"].__setitem__("new_physical_copy_count",1))
    def test_juan3_leaf_not_mixed(self):
        self.mutate(lambda j:j["review"]["year_1600_original_juan3_start"].__setitem__("right_leaf_previous_volume",True))
    def test_no_false_negative_proof(self):
        self.mutate(lambda j:j["review"].__setitem__("negative_page_text_proven",True))
    def test_no_fake_pdf_rehash(self):
        self.mutate(lambda j:j["source"].__setitem__("source_pdf_binary_rehashed",True))
if __name__=="__main__": unittest.main()
