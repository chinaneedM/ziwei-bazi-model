"""13MW bibliographic-source quarantine regression."""
import copy,importlib.util,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("v13mw",R/"scripts/verify-tianwen-13mw-naaj-catalog.py")
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class Catalogue(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.d=[json.loads(f.read_text(encoding="utf-8")) for f in (v.E,v.S,v.L)]
 def test_pass(self):self.assertEqual(v.check(*self.d)["status"],"PASS")
 def reject(self,path,value):
  a=copy.deepcopy(self.d);z=a[0]
  for k in path[:-1]:z=z[k]
  z[path[-1]]=value
  with self.assertRaises(AssertionError):v.check(*a)
 def test_fake_original_impression(self):self.reject(["date_separation","impression_year"],1569)
 def test_fake_another_original(self):self.reject(["guards","new_physical_copies"],1)
 def test_fake_historical_winner(self):self.reject(["guards","new_historical_g893_winners"],1)
 def test_fake_naj_sixth_book_proof(self):self.reject(["catalogues",0,"sixth_book_datong_item_proven"],True)
 def test_wrong_catalogue_title(self):self.reject(["catalogues",1,"ncid"],"BC18449469")
if __name__=="__main__":unittest.main()
