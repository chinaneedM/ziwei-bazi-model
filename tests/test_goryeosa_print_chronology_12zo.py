import importlib.util
import unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-print-chronology-12zo.py"
spec=importlib.util.spec_from_file_location("tw12zo",P)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class Test(unittest.TestCase):
    def setUp(self): self.a=list(v.load())
    def reject(self):
        with self.assertRaises(ValueError): v.verify(*self.a)
    def test_pass(self): self.assertEqual(v.verify(*self.a)["status"],"PASS")
    def test_order_not_publication(self): self.a[0]["sources"]["royal_annals_1452_order"]["completed_print_attested"]=True;self.reject()
    def test_still_conflicting(self): self.a[0]["contradiction"]["resolution"]="RESOLVED";self.reject()
    def test_no_transfer_1476_to_5554(self): self.a[0]["sources"]["snu_gk05554_catalog"]["impression_date"]="1476";self.reject()
    def test_no_original_glyph_vote(self): self.a[0]["unresolved"]["new_original_target_glyphs"]=1;self.reject()
    def test_no_fake_original_fulltext(self): self.a[0]["sources"]["kci_2014_abstract"]["original_full_text_reviewed"]=True;self.reject()
    def test_no_chronology_cross_folio(self): self.a[0]["sources"]["snu_gk03579_catalog"]["work52_d16_d18_original_folio_verified"]=True;self.reject()
    def test_future_focus_compatible(self):
        self.a[2]["historical_audit"]["current_focus"].append("12ZP next")
        self.a[3]["binding"]["source_focus_count"]+=1
        self.a[3]["binding"]["latest_research_focus_prefix"]="12ZP"
        self.assertEqual(v.verify(*self.a)["status"],"PASS")
if __name__=="__main__":unittest.main()
