import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-royal-annals-publication-12zp.py"
spec=importlib.util.spec_from_file_location("tw12zp",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test(unittest.TestCase):
    def setUp(self):self.d=list(m.load())
    def fails(self):
        with self.assertRaises(ValueError):m.verify(*self.d)
    def test_baseline(self):self.assertEqual(m.verify(*self.d)["status"],"PASS")
    def test_old_draft_not_final(self):self.d[0]["conclusions"]["1482_memorial_predecessor_state"]="SAME_FINAL_TEXT";self.fails()
    def test_print_order_not_completion(self):self.d[0]["conclusions"]["1452_nov_goryeosa_state"]="COMPLETE";self.fails()
    def test_1454_print_vs_grant(self):self.d[0]["conclusions"]["1454_oct_full_goryeosa_state"]="ALREADY_DISTRIBUTED";self.fails()
    def test_no_direct_glyph_votes(self):self.d[0]["witness_delta"]["new_work52_d16_d18_glyph_votes"]=1;self.fails()
    def test_no_original_promotion(self):self.d[1]["sources"][0]["physical_glyph_authority"]=True;self.fails()
    def test_keep_1452_1453_open(self):self.d[0]["conclusions"]["chronology_dispute_1452_vs_1453"]="RESOLVED";self.fails()
    def test_manifest_growth(self):self.d[2]["combined_source_count"]=706;self.fails()
    def test_forward_compatible_focus(self):
        self.d[3]["historical_audit"]["current_focus"].append("12ZQ next")
        self.d[4]["binding"]["source_focus_count"]+=1
        self.d[4]["binding"]["latest_research_focus_prefix"]="12ZQ"
        self.assertEqual(m.verify(*self.d)["status"],"PASS")
if __name__=="__main__":unittest.main()
