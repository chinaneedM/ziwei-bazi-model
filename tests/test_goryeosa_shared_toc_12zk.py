import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-shared-toc-12zk.py"
s=importlib.util.spec_from_file_location("tw12zk",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Test(unittest.TestCase):
 def setUp(self): self.x=list(v.load())
 def bad(self):
  with self.assertRaises(ValueError):v.verify(*self.x)
 def test_ok(self):self.assertEqual(v.verify(*self.x)["status"],"PASS")
 def test_toc_is_not_holdings(self):self.x[0]["boundaries"]["work_level_toc_is_copy_specific_fascicle_census"]=True;self.bad()
 def test_5553_film_cannot_attest_5554(self):self.x[0]["boundaries"]["gk05553_microfilm_licenses_gk05554_original_read"]=True;self.bad()
 def test_no_5554_work52_book(self):self.x[0]["boundaries"]["gk05554_work52_physical_book"]=8;self.bad()
 def test_no_new_physical_witness(self):self.x[0]["boundaries"]["new_physical_witnesses"]=1;self.bad()
 def test_no_1482_print_impression(self):self.x[0]["items"][1]["impression"]="1482";self.bad()
 def test_future_focus_works(self):
  self.x[2]["historical_audit"]["current_focus"].append("12ZL next")
  self.x[3]["binding"]["source_focus_count"]+=1
  self.x[3]["binding"]["latest_research_focus_prefix"]="12ZL"
  self.assertEqual(v.verify(*self.x)["status"],"PASS")
if __name__=="__main__":unittest.main()
