import unittest,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-g893-solar-seven-day-original-12yg.py"
spec=importlib.util.spec_from_file_location("g893_12yg",p)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class OriginalSevenDays(unittest.TestCase):
 def setUp(self):self.d=list(module.load())
 def fail_case(self):
  with self.assertRaises(ValueError):module.verify(*self.d)
 def test_pass(self):self.assertEqual(module.verify(*self.d)["exact_subtraction_edges"],6)
 def test_wrong_long_digit(self):self.d[0]["readings"][3]["long_decimal"]="434.3711";self.fail_case()
 def test_false_ascending_recurrence(self):self.d[0]["local_arithmetic"]["long_differences"][0]="4.8010";self.fail_case()
 def test_false_history(self):self.d[0]["forward_only_erratum"]["prior_12yf_status"]="VERIFIED";self.fail_case()
 def test_false_source_sha(self):self.d[0]["rois"][4]["sha256"]="0"*64;self.fail_case()
 def test_overlap_rois(self):self.d[0]["rois"][1]["rect"][0]=1020;self.fail_case()
 def test_wrong_day20_source(self):self.d[0]["readings"][6]["page"]="002b";self.fail_case()
 def test_wrong_headers(self):self.d[0]["heading"]["unit_to_long_short_lane_mapping"]="PROVEN";self.fail_case()
 def test_false_witness(self):self.d[0]["same_copy"]["new_physical_witnesses"]=1;self.fail_case()
 def test_false_mechanical_winner(self):self.d[0]["boundaries"]["cross_witness_final_mechanical_decisions"]="6/6";self.fail_case()
 def test_false_issue_closure(self):next(z for z in self.d[1]["issues"] if z["id"]=="TW-OPEN-0005")["status"]="RESOLVED_WITH_EVIDENCE";self.fail_case()
 def test_wrong_version(self):self.d[2]["schema_version"]="1.619.0";self.fail_case()
if __name__=="__main__":unittest.main()
