import unittest,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-institutional-d16-12yy.py"
spec=importlib.util.spec_from_file_location("tianwen12yy",p)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class InstitutionalDigitalTextVsOriginal(unittest.TestCase):
 def setUp(self):self.x=list(v.read())
 def bad(self):
  with self.assertRaises(ValueError):v.verify(*self.x)
 def test_valid(self):self.assertEqual(v.verify(*self.x)["gap"],"0.1000")
 def test_no_d16_silent_editorial_correction(self):self.x[0]["direct_reading"]["days"][1]["official_goryeosa"]="五分二三六二";self.bad()
 def test_source_original_tamper(self):self.x[0]["direct_reading"]["days"][1]["g893_original"]="五分一三六二";self.bad()
 def test_false_paper_original(self):self.x[0]["scope_firewall"]["distinct_goryeosa_historical_paper_page_verified"]=True;self.bad()
 def test_false_uncertain_cause_closure(self):self.x[0]["scope_firewall"]["attribution_as_original_printing_or_ocr_error"]="EDITORIAL_TYPO_PROVEN";self.bad()
 def test_fake_sixth_g893_win(self):self.x[0]["scope_firewall"]["g893_principal_six"]="6/6";self.bad()
 def test_false_independent_physical_vote(self):self.x[0]["scope_firewall"]["new_ancient_physical_source_votes"]=1;self.bad()
 def test_future_focus_growth_accepted(self):
  self.x[2]["historical_audit"]["current_focus"].append("12YZ later")
  self.x[1]["binding"]["source_focus_count"]+=1
  self.x[1]["binding"]["latest_research_focus_prefix"]="12YZ"
  self.assertEqual(v.verify(*self.x)["status"],"PASS")
if __name__=="__main__":unittest.main()
