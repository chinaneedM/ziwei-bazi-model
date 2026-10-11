"""12RW F1–F5 original-page hash-source identity and evidence firewall."""
import copy,importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("rwgate",ROOT/"scripts/verify_yehuobian_nlc_f1_f5_union_12rw.py")
G=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(G)
class Test12RW(unittest.TestCase):
    def mutate(self,fn):
        x=copy.deepcopy(G.read(G.RECORD));fn(x)
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"bad.json";p.write_text(json.dumps(x,ensure_ascii=False),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"12RW_"):G.verify(record_path=p)
    def test_live_union(self):
        d=G.verify()
        self.assertEqual(d["native_source_identity_pages_f1_f5"],429)
        self.assertEqual(d["outside_f1_f5"],599)
        self.assertFalse(d["whole_1030_page_union_claimed"])
    def test_wrong_parent(self):self.mutate(lambda d:d.__setitem__("parent_open_batch","12QE_OPEN"))
    def test_missing_window(self):self.mutate(lambda d:d["windows"].pop())
    def test_duplicate_page_range(self):self.mutate(lambda d:d["windows"][14].__setitem__("first",83))
    def test_hash_drift(self):self.mutate(lambda d:d["windows"][-1].__setitem__("chain","0"*64))
    def test_false_global_count(self):self.mutate(lambda d:d["accounting"].__setitem__("global_1030_native_source_union_computed",True))
    def test_false_text_claim(self):self.mutate(lambda d:d["scope_guards"].__setitem__("no_target_absence_proof",False))
    def test_imprint_not_verified(self):self.mutate(lambda d:d["transmission_impact"]["edges_supported"].append("COPYING"))
    def test_source_identity(self):self.mutate(lambda d:d["source"]["fascicles"][2].__setitem__("source_pdf_sha256","0"*64))
if __name__=="__main__":unittest.main()
