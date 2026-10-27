import copy,importlib.util,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location("field",R/"scripts/verify-tianwen-13ib-field-index.py")
M=importlib.util.module_from_spec(S);S.loader.exec_module(M)
class Test(unittest.TestCase):
 def setUp(self):self.e=json.loads(M.E.read_text(encoding="utf8"))
 def test_real(self):self.assertTrue(M.check(self.e))
 def test_uniform_shift_false(self):
  x=copy.deepcopy(self.e);x["finding"]["uniform_cross_field_day_shift"]="PROVEN"
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_nikh_terminal_three_guard(self):
  x=copy.deepcopy(self.e);x["edited"]["D18"]["raw_digits"]="84246408"
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_b18_misindexed(self):
  x=copy.deepcopy(self.e);x["printed"]["D18"]["B"]=4243711
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_source_blob_frozen(self):
  x=copy.deepcopy(self.e);x["frozen"][0]["sha"]="0"*40
  with self.assertRaises(AssertionError):M.check(x,False)
if __name__=="__main__":unittest.main()
