import unittest,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-siku-zongmu-juan-mu-12yw.py"
s=importlib.util.spec_from_file_location("tianwen12yw",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class SikuCatalogSourceScope(unittest.TestCase):
 def setUp(self):self.d=v.read()
 def fail_gate(self):
  with self.assertRaises(ValueError):v.verify(*self.d)
 def test_valid(self):self.assertEqual(v.verify(*self.d)["original_page_loci"],2)
 def test_append_only_future_12yx_focus(self):
  self.d[2]["historical_audit"]["current_focus"].append("12YX future independent source review")
  self.d[1]["binding"]["source_focus_count"]+=1
  self.d[1]["binding"]["latest_research_focus_prefix"]="12YX"
  self.assertEqual(v.verify(*self.d)["result"],"PASS")
 def test_fabricated_source_hash(self):self.d[0]["original_source"]["sha1_self_verified"]=True;self.fail_gate()
 def test_unproven_17_juan_as_copy(self):self.d[0]["textual_result"]["separate_seventeen_juan_physical_edition_proven"]=True;self.fail_gate()
 def test_wrong_fascicle(self):self.d[0]["nlc_locator"]["correct_nlc_item"]="NLC892-001945406-317562";self.fail_gate()
 def test_false_g893(self):self.d[0]["scope"]["g893_cross_source"]="6/6";self.fail_gate()
 def test_bad_physical_vote(self):self.d[0]["scope"]["new_historical_physical_copy_votes"]=1;self.fail_gate()
 def test_fake_printing_date(self):self.d[0]["original_source"]["impression_year"]="1782";self.fail_gate()
if __name__=="__main__":unittest.main()
