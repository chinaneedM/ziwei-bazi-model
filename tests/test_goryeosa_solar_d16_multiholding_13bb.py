import copy,importlib.util,unittest
from pathlib import Path
path=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-solar-d16-multiholding-13bb.py"
spec=importlib.util.spec_from_file_location("check13bb",path)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13BB(unittest.TestCase):
 def setUp(self):
  self.c=m.load(m.PC);self.a=m.load(m.PA);self.b=m.load(m.PB)
 def test_live_original_bindings(self):
  self.assertTrue(m.check(self.c,self.a,self.b))
 def test_wrong_original_digit_rejected(self):
  c=copy.deepcopy(self.c);c["controls"][0]["short_d16"]="五分二三六二"
  with self.assertRaises(AssertionError):m.check(c,self.a,self.b)
 def test_forged_independence_rejected(self):
  c=copy.deepcopy(self.c);c["independent_stemmatic_votes"]=3
  with self.assertRaises(AssertionError):m.check(c,self.a,self.b)
 def test_fake_nlc_item_binding_rejected(self):
  a=copy.deepcopy(self.a);a["source_nlc"]["firstparty_nlc_item_crosswalk_verified"]=True
  with self.assertRaises(AssertionError):m.check(self.c,a,self.b)
 def test_false_cross_work_equivalence_rejected(self):
  c=copy.deepcopy(self.c);c["cross_work_same_locus_does_not_prove_same_original_table"]=False
  with self.assertRaises(AssertionError):m.check(c,self.a,self.b)
if __name__=="__main__":unittest.main()
