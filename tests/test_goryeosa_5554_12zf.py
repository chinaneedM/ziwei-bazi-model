import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-5554-12zf.py"
spec=importlib.util.spec_from_file_location("tw12zf",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class Tests(unittest.TestCase):
 def setUp(self):self.d=list(v.load())
 def bad(self):
  with self.assertRaises(ValueError):v.verify(*self.d)
 def test_pass(self):self.assertEqual(v.verify(*self.d)["status"],"PASS")
 def test_no_phantom_source(self):self.d[0]["official"]["k5554_work52_image"]="001a";self.bad()
 def test_no_rebound_mf(self):self.d[0]["official"]["k5554_film_physically_bound"]=True;self.bad()
 def test_source_tension(self):self.d[0]["scholarship"]["claimed_5553_third_manuscript_book"]=29;self.bad()
 def test_reprint_not_original(self):self.d[0]["modern_reprint"]["vol52_print_origin"]="GK05554_00";self.bad()
 def test_no_stemma_vote(self):self.d[0]["outcome"]["new_independent_historical_source_votes"]=5;self.bad()
 def test_future_focus(self):
  self.d[1]["historical_audit"]["current_focus"].append("12ZG future")
  self.d[2]["binding"]["source_focus_count"]+=1
  self.d[2]["binding"]["latest_research_focus_prefix"]="12ZG"
  self.assertEqual(v.verify(*self.d)["status"],"PASS")
if __name__=="__main__":unittest.main()
