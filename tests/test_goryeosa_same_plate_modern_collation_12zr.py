import importlib.util
import unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-same-plate-modern-collation-12zr.py"
spec=importlib.util.spec_from_file_location("tw12zr",P)
v=importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
class Test(unittest.TestCase):
    def setUp(self):
        self.a=list(v.load())
    def bad(self):
        with self.assertRaises(ValueError):
            v.verify(*self.a)
    def test_pass(self):
        self.assertEqual(v.verify(*self.a)["status"],"PASS")
    def test_same_author_not_double(self):
        self.a[0]["kci2014"]["independent_author_count_across_2012_and_2014"]=2
        self.bad()
    def test_same_plate_claim_not_our_folio_proof(self):
        self.a[0]["scope"]["author_claim_same_print_blocks_not_proven_by_this_project_original_images"]=False
        self.bad()
    def test_no_guess_kyu_item(self):
        self.a[0]["scope"]["woodblock_85book_comparator_exact_SNU_ID"]="GK03579_00"
        self.bad()
    def test_no_assumed_modern_vol52_apparatus(self):
        self.a[0]["modern2024"]["actual_vol52_apparatus_reviewed"]=True
        self.bad()
    def test_no_fake_glyph(self):
        self.a[0]["unresolved"]["ancient_glyph_votes_added"]=1
        self.bad()
    def test_no_double_ancestral_plate(self):
        self.a[0]["unresolved"]["independent_ancestral_plate_votes_added"]=2
        self.bad()
    def test_no_source_identity_drift(self):
        self.a[1]["sources"][0]["physical_glyph_authority"]=True
        self.bad()
    def test_future_registry_growth(self):
        self.a[4]["extension_source_count"]+=2
        self.a[4]["combined_source_count"]+=2
        self.a[2]["historical_audit"]["external_source_registry_extension_count"]+=2
        self.a[2]["historical_audit"]["external_source_registry_total_unique_count"]+=2
        self.assertEqual(v.verify(*self.a)["status"],"PASS")
    def test_future_focus(self):
        self.a[2]["historical_audit"]["current_focus"].append("12ZS next")
        self.a[3]["binding"]["source_focus_count"]+=1
        self.a[3]["binding"]["latest_research_focus_prefix"]="12ZS"
        self.assertEqual(v.verify(*self.a)["status"],"PASS")
if __name__=="__main__":
    unittest.main()
