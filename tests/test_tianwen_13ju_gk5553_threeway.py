import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13ju-gk5553-threeway.py"
s=importlib.util.spec_from_file_location("tw13ju",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class ThreeWay(unittest.TestCase):
 def setUp(self):self.x=list(v.load())
 def deny(self):
  with self.assertRaises(AssertionError):v.verify(*self.x)
 def test_ok(self):self.assertEqual(v.verify(*self.x)["status"],"PASS")
 def test_no_28_to_29_merge(self):self.x[0]["sources"][2]["fascicles"]=[8,26,29];self.deny()
 def test_material_not_conflated(self):self.x[0]["sources"][2]["material"]="일부 필사본";self.deny()
 def test_no_printed_page_promotion(self):self.x[0]["sources"][2]["source_2021_print_page_examined"]=True;self.deny()
 def test_no_copy_vote(self):self.x[0]["comparison"]["ancient_copy_votes"]=1;self.deny()
 def test_future_append(self):
  self.x[1]["historical_audit"]["current_focus"].append("13JV follow-up")
  self.x[2]["binding"]["source_focus_count"]+=1
  self.x[2]["binding"]["latest_research_focus_prefix"]="13JV"
  self.assertEqual(v.verify(*self.x)["status"],"PASS")
if __name__=="__main__":unittest.main()
