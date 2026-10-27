import importlib.util
import unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-5554-enumeration-12zh.py"
spec=importlib.util.spec_from_file_location("tw12zh",P)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class Check(unittest.TestCase):
 def setUp(self):
  self.data=list(v.load())
 def bad(self):
  with self.assertRaises(ValueError):v.verify(*self.data)
 def test_pass(self):
  self.assertEqual(v.verify(*self.data)["status"],"PASS")
 def test_source_count_inflation(self):
  self.data[0]["received_enumerations"]["secondary_scholarly"]["computed_distinct_numbered_work_volumes"]=105;self.bad()
 def test_29_35_silent_fill(self):
  self.data[0]["received_enumerations"]["republished_heritage"]["numbered_work_volume_ranges"].append([30,34]);self.bad()
 def test_d16_invented(self):
  self.data[0]["scope"]["original_5554_v52_d16_printed_glyph"]="五分一三六二";self.bad()
 def test_stemmatic_phantom(self):
  self.data[0]["scope"]["physical_witness_votes_added"]=1;self.bad()
 def test_exaggerated_fascicle(self):
  self.data[0]["scope"]["exact_v52_physical_book"]=10;self.bad()
 def test_survives_future_batches(self):
  self.data[2]["historical_audit"]["current_focus"].append("12ZI future research")
  self.data[3]["binding"]["source_focus_count"]+=1
  self.data[3]["binding"]["latest_research_focus_prefix"]="12ZI"
  self.assertEqual(v.verify(*self.data)["status"],"PASS")
if __name__=="__main__":unittest.main()
