import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-5554-census-12zj.py"
s=importlib.util.spec_from_file_location("tw12zj",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Test(unittest.TestCase):
 def setUp(self):self.x=list(v.load())
 def bad(self):
  with self.assertRaises(ValueError):v.verify(*self.x)
 def test_ok(self):self.assertEqual(v.verify(*self.x)["status"],"PASS")
 def test_41_not_independent(self):self.x[0]["counts"]["claimed_missing_41_is_independent_folio_census"]=True;self.bad()
 def test_one_unit(self):self.x[0]["counts"]["one_numbered_unit_disagreement"]=0;self.bad()
 def test_no_volume52_book(self):self.x[0]["boundaries"]["exact_5554_work52_physical_book"]=10;self.bad()
 def test_no_glyph(self):self.x[0]["boundaries"]["glyph_5554_d16"]="五分";self.bad()
 def test_no_original_print_year(self):self.x[0]["source"]["kyudb"]["impression"]="1482";self.bad()
 def test_no_proven_spine_loss(self):self.x[0]["counts"]["proven_lost_11_original_books"]=True;self.bad()
 def test_later_focus(self):
  self.x[2]["historical_audit"]["current_focus"].append("12ZK next")
  self.x[3]["binding"]["source_focus_count"]+=1
  self.x[3]["binding"]["latest_research_focus_prefix"]="12ZK"
  self.assertEqual(v.verify(*self.x)["status"],"PASS")
if __name__=="__main__":unittest.main()
