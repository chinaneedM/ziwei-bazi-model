import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13lc-siku-chronology.py"
s=importlib.util.spec_from_file_location("tw13lc",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Chronology(unittest.TestCase):
 def setUp(self):self.a=copy.deepcopy(list(v.load()))
 def fails(self):
  with self.assertRaises(ValueError):v.verify(*self.a)
 def test_valid(self):self.assertEqual(v.verify(*self.a)["siku_first_copy"],1782)
 def test_fake_siku_1739(self):self.a[0]["institutional_witnesses"][2]["year"]=1739;self.fails()
 def test_fabricated_copy_binding(self):self.a[0]["chronological_firewall"]["cadal_physical_copy_linked_to_wuying_1739"]=True;self.fails()
 def test_wrong_original_numeric(self):self.a[0]["source_native_preservation"]["cadal_original_13month"]="238977.09";self.fails()
 def test_fake_catalog_glyph_vote(self):self.a[0]["institutional_witnesses"][0]["target_juan35_glyph_observed"]=True;self.fails()
 def test_scope_chart_reopen(self):self.a[0]["scope"]["algorithm_reopens"]=1;self.fails()
 def test_rolling_focus_forward(self):
  self.a[2]["historical_audit"]["current_focus"].append("13LD later independent source")
  self.a[3]["binding"]["source_focus_count"]+=1
  self.a[3]["binding"]["latest_research_focus_prefix"]="13LD"
  self.a[3]["issues"][4]["next_action"]="13LD CURRENT ACTION: retain earlier evidence"
  self.assertEqual(v.verify(*self.a)["status"],"PASS")
if __name__=="__main__":unittest.main()
