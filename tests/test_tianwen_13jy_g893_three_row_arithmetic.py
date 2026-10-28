import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13jy-g893-three-row-arithmetic.py"
spec=importlib.util.spec_from_file_location("tw13jy",p)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class ExactDecimalSourceFence(unittest.TestCase):
 def setUp(self):self.data=copy.deepcopy(list(v.load()))
 def fails(self):
  with self.assertRaises(AssertionError):v.verify(*self.data)
 def test_exact(self):self.assertEqual(v.verify(*self.data)["status"],"PASS")
 def test_received_raw_change(self):self.data[0]["cases"][1]["received_candidate"]="1.0281";self.fails()
 def test_arithmetic_change(self):self.data[0]["cases"][1]["received_second_differences"][1]="0.0000000";self.fails()
 def test_l132_promotion(self):self.data[0]["cases"][2]["received_candidate_grade"]="CERTIFIED";self.fails()
 def test_false_original_award(self):self.data[0]["result"]["original_g893_six_cross_witness_variant_winners_awarded"]=1;self.fails()
 def test_cross_witness_scope(self):self.data[0]["method"]="same witness true";self.fails()
 def test_future_append_only(self):
  self.data[1]["historical_audit"]["current_focus"].append("13JZ future work")
  self.data[2]["binding"]["source_focus_count"]+=1
  self.data[2]["binding"]["latest_research_focus_prefix"]="13JZ"
  self.assertEqual(v.verify(*self.data)["status"],"PASS")
if __name__=="__main__":unittest.main()
