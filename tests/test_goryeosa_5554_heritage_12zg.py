import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-5554-heritage-12zg.py";s=importlib.util.spec_from_file_location("tw12zg",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Test(unittest.TestCase):
 def setUp(self):self.x=list(v.load())
 def bad(self):
  with self.assertRaises(ValueError):v.verify(*self.x)
 def test_valid(self):self.assertEqual(v.verify(*self.x)["status"],"PASS")
 def test_no_1482_print(self):self.x[0]["kyudb"]["impression_year_literal"]="1482";self.bad()
 def test_heritage_no_original(self):self.x[0]["heritage"]["direct_original_printing_evidence"]=True;self.bad()
 def test_98_vs_105(self):self.x[0]["secondary"]["claimed_original_work_volumes_count"]=98;self.bad()
 def test_no_phantom_glyph(self):self.x[0]["constraints"]["confirmed_original_5554_d16"]="五分一三六二";self.bad()
 def test_future_batch(self):
  self.x[2]["historical_audit"]["current_focus"].append("12ZH future")
  self.x[3]["binding"]["source_focus_count"]+=1
  self.x[3]["binding"]["latest_research_focus_prefix"]="12ZH"
  self.assertEqual(v.verify(*self.x)["status"],"PASS")
if __name__=="__main__":unittest.main()
