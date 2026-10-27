import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"scripts/verify-tianwen-13hx-intercolumn.py"
S=importlib.util.spec_from_file_location("hx",P);M=importlib.util.module_from_spec(S);S.loader.exec_module(M)
class IntercolumnWinter(unittest.TestCase):
 def setUp(self): self.e=json.loads(M.E.read_text(encoding="utf8"))
 def test_full_state_and_preservation(self): self.assertTrue(M.check(self.e))
 def test_day16_physical_one_cannot_be_replaced_by_calculated_two(self):
  v=copy.deepcopy(self.e);v["daily_rows"][2]["differential_encoded"]=52362
  v["daily_rows"][2]["differential_literal"]="五分二三六二"
  with self.assertRaises(AssertionError):M.check(v,False)
 def test_additive_column_one_digit_mutation(self):
  v=copy.deepcopy(self.e);v["daily_rows"][2]["additive_encoded"]+=1
  with self.assertRaises(AssertionError):M.check(v,False)
 def test_cumulative_column_one_digit_mutation(self):
  v=copy.deepcopy(self.e);v["daily_rows"][3]["cumulative_encoded"]+=1
  with self.assertRaises(AssertionError):M.check(v,False)
 def test_scope_cannot_be_promoted_to_original(self):
  v=copy.deepcopy(self.e);v["source"]["grade"]="DIRECT_ORIGINAL"; 
  with self.assertRaises(AssertionError):M.check(v,False)
if __name__=="__main__":unittest.main()
