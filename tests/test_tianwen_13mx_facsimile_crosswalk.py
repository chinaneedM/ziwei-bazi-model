import copy,importlib.util,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("verify13mx",R/"scripts/verify-tianwen-13mx-facsimile-crosswalk.py")
v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class TestScope(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.args=[json.loads(p.read_text(encoding="utf-8")) for p in (v.E,v.S,v.L)]
 def test_valid(self):self.assertEqual(v.check(*self.args)["status"],"PASS")
 def test_no_source_promotion(self):
  x=copy.deepcopy(self.args);x[0]["limits"]["new_historical_physical_copy"]=True
  with self.assertRaises(AssertionError):v.check(*x)
 def test_no_2022_sixth(self):
  x=copy.deepcopy(self.args);x[0]["source_2022"]["sixth_datong_original_page_proven"]=True
  with self.assertRaises(AssertionError):v.check(*x)
 def test_no_impression(self):
  x=copy.deepcopy(self.args);x[0]["limits"]["naaj_sixth_item_impression"]="CERTIFIED"
  with self.assertRaises(AssertionError):v.check(*x)
if __name__=="__main__":unittest.main()
