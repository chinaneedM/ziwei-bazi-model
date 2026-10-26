import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"scripts/verify-tianwen-13hz-nikh-d18.py"
S=importlib.util.spec_from_file_location("hz",P);M=importlib.util.module_from_spec(S);S.loader.exec_module(M)
class D18NIKH(unittest.TestCase):
 def setUp(self):self.x=json.loads(M.E.read_text(encoding="utf8"))
 def test_current_evidence(self):self.assertTrue(M.check(self.x))
 def test_do_not_delete_terminal_three(self):
  x=copy.deepcopy(self.x);x["D18"]["C"]="八千四百二十四六四〇八"
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_do_not_fill_original_from_math(self):
  x=copy.deepcopy(self.x);x["D18"]["C_int"]=84246408
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_independent_right_neighbor_constraint(self):
  x=copy.deepcopy(self.x);x["D19"]["C_int"]+=1
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_glyph_not_physical(self):
  x=copy.deepcopy(self.x);x["arithmetic"]["original_C18_print_glyph"]="八千四百二十四六四〇八"
  with self.assertRaises(AssertionError):M.check(x,False)
if __name__=="__main__":unittest.main()
