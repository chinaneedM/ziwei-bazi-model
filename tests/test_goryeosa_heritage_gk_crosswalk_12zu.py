import importlib.util,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-heritage-gk-crosswalk-12zu.py"
spec=importlib.util.spec_from_file_location("tw12zu",P)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class Test(unittest.TestCase):
    def setUp(self):self.a=list(v.load())
    def bad(self):
        with self.assertRaises(ValueError):v.verify(*self.a)
    def test_pass(self):self.assertEqual(v.verify(*self.a)["status"],"PASS")
    def test_no_swapped_items(self):
        self.a[0]["items"][1]["snu_catalog_code"]="GK03539_00";self.bad()
    def test_no_guess_from_old_snapshot(self):
        self.a[1]["heritage_items"][0]["exact_SNU_item_id"]="GK03539_00";self.bad()
    def test_treasure_number_binds(self):
        self.a[0]["items"][0]["snu_old_treasure_number"]="2115-2";self.bad()
    def test_shared_3539_mf_not_3579_source(self):
        self.a[0]["source_issued_bibliography"]["gk03579_own_independent_microfilm_source_proven"]=True;self.bad()
    def test_no_work52_image(self):
        self.a[0]["unresolved"]["gk03579_original_52_target_image_sha256"]="0"*64;self.bad()
    def test_no_glyph_vote(self):
        self.a[0]["unresolved"]["new_ancient_d16_d18_numeric_votes"]=1;self.bad()
    def test_future_focus_compatible(self):
        self.a[2]["historical_audit"]["current_focus"].append("12ZV next")
        self.a[3]["binding"]["source_focus_count"]+=1
        self.a[3]["binding"]["latest_research_focus_prefix"]="12ZV"
        self.assertEqual(v.verify(*self.a)["status"],"PASS")
if __name__=="__main__":unittest.main()
