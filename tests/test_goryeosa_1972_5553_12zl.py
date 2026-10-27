import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-1972-5553-12zl.py"
s=importlib.util.spec_from_file_location("tw12zl",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Test(unittest.TestCase):
 def setUp(self):self.x=list(v.load())
 def bad(self):
  with self.assertRaises(ValueError):v.verify(*self.x)
 def test_ok(self):self.assertEqual(v.verify(*self.x)["status"],"PASS")
 def test_conflicting_catalog_books_not_erased(self):self.x[0]["adjudication"]["contested_books"]=[];self.bad()
 def test_secondary_not_firstparty(self):self.x[0]["source_evidence"]["heritage_reprint"]["original_heritage_full_text_directly_verified"]=True;self.bad()
 def test_no_facsimile_original(self):self.x[0]["adjudication"]["modern_1972_total_work_is_single_original_5554"]=True;self.bad()
 def test_no_glyph_promotion(self):self.x[0]["open_originals"]["gk5554_d16_image"]="sha";self.bad()
 def test_no_fake_new_witness(self):self.x[0]["open_originals"]["independent_physical_votes"]=1;self.bad()
 def test_next_batch_forward_compatible(self):
  self.x[1]["historical_audit"]["current_focus"].append("12ZM later")
  self.x[2]["binding"]["source_focus_count"]+=1
  self.x[2]["binding"]["latest_research_focus_prefix"]="12ZM"
  self.assertEqual(v.verify(*self.x)["status"],"PASS")
if __name__=="__main__":unittest.main()
