import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13lh-naaj-geometry.py"
spec=importlib.util.spec_from_file_location("tw13lh",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class GeometryFirewall(unittest.TestCase):
 def setUp(self):self.a=copy.deepcopy(list(v.load()))
 def bad(self):
  with self.assertRaises(AssertionError):v.check(*self.a)
 def test_base(self):self.assertEqual(v.check(*self.a)["status"],"PASS")
 def test_false_same_plate(self):self.a[0]["adjudication"]["same_woodblocks_historically_proven"]=True;self.bad()
 def test_false_same_impression(self):self.a[0]["adjudication"]["same_historical_print_run_proven"]=True;self.bad()
 def test_false_1739(self):self.a[0]["adjudication"]["original_1739_impression_proven"]=True;self.bad()
 def test_unjustified_stemma_vote(self):self.a[0]["adjudication"]["independent_textual_recension_votes_new"]=1;self.bad()
 def test_false_number(self):self.a[0]["input_originals"][0]["original_numeral"]="288977.09";self.bad()
 def test_original_page_hash(self):self.a[0]["replay"]["page_native_rgb_sha256"]["281-0038"]["6"]="0"*64;self.bad()
 def test_legacy_action_preservation(self):self.a[2]["issues"][4]["next_action"]="13LH CURRENT ACTION: no archive";self.bad()
 def test_forward_next(self):
  self.a[1]["historical_audit"]["current_focus"].append("13LI next direct page")
  self.a[2]["binding"]["latest_research_focus_prefix"]="13LI"
  self.a[2]["binding"]["source_focus_count"]+=1
  self.a[2]["issues"][4]["next_action"]="13LI CURRENT ACTION: later study\n"+self.a[2]["issues"][4]["next_action"]
  self.assertEqual(v.check(*self.a)["status"],"PASS")
if __name__=="__main__":unittest.main()
