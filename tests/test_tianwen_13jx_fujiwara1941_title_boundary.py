import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13jx-fujiwara1941-title-boundary.py"
spec=importlib.util.spec_from_file_location("tw13jx",p)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class Fujiwara1941(unittest.TestCase):
 def setUp(self):self.x=copy.deepcopy(list(v.load()))
 def denied(self):
  with self.assertRaises(AssertionError):v.verify(*self.x)
 def test_baseline(self):self.assertEqual(v.verify(*self.x)["status"],"PASS")
 def test_no_same_title(self):self.x[0]["g893_object"]["title_identity_proven_with_1941_subject"]=True;self.denied()
 def test_no_1298_original(self):self.x[0]["distinct_object_1941_claim"]["narrative_is_not_direct_ancient_original"]=False;self.denied()
 def test_no_fabricated_pdf_hash(self):self.x[0]["modern_publication"]["original_1941_pdf_sha256"]="0"*64;self.denied()
 def test_no_g893_numeric_award(self):self.x[0]["scope_guard"]["g893_six_original_decisions"]=1;self.denied()
 def test_future_batch_append(self):
  self.x[1]["historical_audit"]["current_focus"].append("13JY future")
  self.x[2]["binding"]["source_focus_count"]+=1
  self.x[2]["binding"]["latest_research_focus_prefix"]="13JY"
  self.assertEqual(v.verify(*self.x)["status"],"PASS")
if __name__=="__main__":unittest.main()
