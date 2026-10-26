import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/"scripts/verify-tianwen-13hy-source-erratum.py"
S=importlib.util.spec_from_file_location("hy",P);M=importlib.util.module_from_spec(S);S.loader.exec_module(M)
class D18ForwardErratum(unittest.TestCase):
 def setUp(self):self.e=json.loads(M.E.read_text(encoding="utf8"))
 def test_state(self):self.assertTrue(M.check(self.e))
 def test_cannot_silently_delete_three(self):
  x=copy.deepcopy(self.e);x["modern_editorial_variant"]["nikh_d18_C"]="八千四百二十四六四〇八"
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_cannot_replace_attested_one_with_two(self):
  x=copy.deepcopy(self.e);x["clean_window"]["days"][3]["A_literal"]="五分二三六二"
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_no_new_original_witness_vote(self):
  x=copy.deepcopy(self.e);x["firewall"]["no_new_physical_witnesses"]=False
  with self.assertRaises(AssertionError):M.check(x,False)
if __name__=="__main__":unittest.main()
