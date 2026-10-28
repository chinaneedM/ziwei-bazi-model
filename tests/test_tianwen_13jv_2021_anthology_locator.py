import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13jv-2021-anthology-locator.py"
spec=importlib.util.spec_from_file_location("tw13jv",p)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class AnthologyLocator(unittest.TestCase):
    def setUp(self):self.data=list(v.load())
    def denied(self):
        with self.assertRaises(AssertionError):v.verify(*self.data)
    def test_baseline(self):self.assertEqual(v.verify(*self.data)["status"],"PASS")
    def test_not_original(self):self.data[0]["exclusions"]["original_2021_print_leaf_examined"]=True;self.denied()
    def test_not_original_page_range(self):self.data[0]["publication"]["inferred_range_is_original_leaf_verified"]=True;self.denied()
    def test_no_physical_fascicle_vote(self):self.data[0]["exclusions"]["ancient_physical_fascicle_binding_awarded"]=1;self.denied()
    def test_no_fake_2021_collation(self):self.data[0]["exclusions"]["article_2021_wording_collated_against_repost"]=True;self.denied()
    def test_forward_append(self):
        self.data[1]["historical_audit"]["current_focus"].append("13JW next investigation")
        self.data[2]["binding"]["source_focus_count"]+=1
        self.data[2]["binding"]["latest_research_focus_prefix"]="13JW"
        self.assertEqual(v.verify(*self.data)["status"],"PASS")
if __name__=="__main__":unittest.main()
