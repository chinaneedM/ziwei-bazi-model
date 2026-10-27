import copy,importlib.util,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=importlib.util.spec_from_file_location("batch13id",R/"scripts/verify-tianwen-13id-original-source-table-start.py")
M=importlib.util.module_from_spec(S);S.loader.exec_module(M)
class Test(unittest.TestCase):
 def setUp(self):self.d=M.load(M.E)
 def test_real(self):self.assertTrue(M.check(self.d))
 def test_old_C18_8000_rejected(self):
  d=copy.deepcopy(self.d);d["local_values"][1][2]=80002697
  with self.assertRaises(AssertionError):M.check(d,False)
 def test_wrong_original_original_offset_rejected(self):
  d=copy.deepcopy(self.d);d["holder_comparison"]["W_D17_C8000_NAJ_D18_C8000"]=0
  with self.assertRaises(AssertionError):M.check(d,False)
 def test_column_to_right_rejected(self):
  d=copy.deepcopy(self.d);d["roi"][5][2]=[1150,685,1184,1400]
  with self.assertRaises(AssertionError):M.check(d,False)
 def test_edited_terminal_three_preserved(self):
  d=copy.deepcopy(self.d);d["firewalls"]["NIKH_edited_D18_C_literal"]="八千四百二十四六四〇八"
  with self.assertRaises(AssertionError):M.check(d,False)
 def test_prior_sha_frozen(self):
  d=copy.deepcopy(self.d);d["dependencies"][1]["sha"]="0"*40
  with self.assertRaises(AssertionError):M.check(d,False)
if __name__=="__main__":unittest.main()
