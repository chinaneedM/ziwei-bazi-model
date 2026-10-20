import copy, importlib.util, unittest
from pathlib import Path
path=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-d16-crosslayer-13bc.py"
spec=importlib.util.spec_from_file_location("check13bc",path)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13BC(unittest.TestCase):
 def setUp(self):
  self.e=m.load(m.PC);self.a=m.load(m.PA);self.b=m.load(m.PB);self.c=m.load(m.PD)
  self.l=m.load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
  self.s=m.load("docs/PROJECT-CURRENT-STATE-R1.json")
 def run_check(self,e=None,a=None,c=None):
  return m.check(e or self.e,a or self.a,self.b,c or self.c,self.l,self.s)
 def test_positive_crosslayer(self):self.assertTrue(self.run_check())
 def test_forged_new_original(self):
  x=copy.deepcopy(self.e);x["new_historical_original_pages_acquired"]=1
  with self.assertRaises(AssertionError):self.run_check(e=x)
 def test_forged_original_crosscolumn_upgrade(self):
  x=copy.deepcopy(self.e);x["original_crosscolumn_image_collation_status"]="PROVEN"
  with self.assertRaises(AssertionError):self.run_check(e=x)
 def test_forged_12yz_long_value(self):
  x=copy.deepcopy(self.a);x["modern_received_rows"][2]["long"]="429.5073"
  with self.assertRaises(AssertionError):self.run_check(a=x)
 def test_forged_original_one_as_two(self):
  x=copy.deepcopy(self.c);x["controls"][0]["short_d16"]="五分二三六二"
  with self.assertRaises(AssertionError):self.run_check(c=x)
 def test_forged_independence_or_algorithm_reopen(self):
  x=copy.deepcopy(self.e);x["independent_numeric_votes_added"]=3
  with self.assertRaises(AssertionError):self.run_check(e=x)
  y=copy.deepcopy(self.e);y["algorithm_reopens"]=1
  with self.assertRaises(AssertionError):self.run_check(e=y)
if __name__=="__main__":unittest.main()
