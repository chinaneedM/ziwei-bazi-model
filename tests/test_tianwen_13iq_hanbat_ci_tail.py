import copy,unittest,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("verify13iq",ROOT/"scripts/verify-tianwen-13iq-hanbat-ci-tail.py")
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class Checks(unittest.TestCase):
 def test_base(self):self.assertTrue(m.check(m.load()))
 def test_no_false_original_leaf(self):
  d=copy.deepcopy(m.load());d["adjudication"]["NLC03130_solar_D30_complete_original_numeric_value"]=42
  with self.assertRaises(AssertionError):m.check(d,False)
 def test_no_fake_item_image(self):
  d=copy.deepcopy(m.load());d["first_party_hanbat"]["list_results"][0]["photographed_original"]=True
  with self.assertRaises(AssertionError):m.check(d,False)
if __name__=="__main__":unittest.main()
