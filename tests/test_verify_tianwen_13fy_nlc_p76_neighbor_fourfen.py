import copy,importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("v13fy",ROOT/"scripts/verify-tianwen-13fy-nlc-p76-neighbor-fourfen.py")
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class Test13FY(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=v.read(v.E);cls.fv=v.read(v.FV);cls.fx=v.read(v.FX);cls.ledger=v.read(v.L);cls.state=v.read(v.S)
 def validate(self,e):return v.check(e,self.fv,self.fx,self.ledger,self.state)
 def test_direct_two_original_positive_fields(self):self.assertTrue(self.validate(self.e))
 def test_refuse_fabricated_day30_nlc_glyph(self):
  e=copy.deepcopy(self.e);e["day30"]["original_complete_fourfen_digits"]="九二二二"
  with self.assertRaises(AssertionError):self.validate(e)
 def test_refuse_wrong_day31_original(self):
  e=copy.deepcopy(self.e);e["direct_original_fields"][1]["digits"]="九三八三"
  with self.assertRaises(AssertionError):self.validate(e)
 def test_refuse_wrong_original_page_hash(self):
  e=copy.deepcopy(self.e);e["source"]["source_png_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.validate(e)
 def test_refuse_copy_independence_without_proof(self):
  e=copy.deepcopy(self.e);e["cross_original"]["source_copy_independence"]=True
  with self.assertRaises(AssertionError):self.validate(e)
 def test_refuse_algorithm_reopen(self):
  e=copy.deepcopy(self.e);e["invariants"]["algorithm_reopens"]=1
  with self.assertRaises(AssertionError):self.validate(e)
if __name__=="__main__":unittest.main()
