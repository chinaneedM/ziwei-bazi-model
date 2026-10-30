"""13LN source-native acquisition audit and anti-authority-promotion mutation checks."""
import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13ln-naaj-p7-native-source.py"
spec=importlib.util.spec_from_file_location("verify13ln",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=m.load()
 def test_baseline(self):self.assertEqual(m.check(*self.data)["source_native_jpeg_regions"],6)
 def test_corrupt_jpeg_sha(self):
  e,m0,s,l=copy.deepcopy(self.data);e["controls"][0]["jpeg_sha256"]="bad"
  with self.assertRaises(AssertionError):m.check(e,m0,s,l)
 def test_resampled_source(self):
  e,m0,s,l=copy.deepcopy(self.data);e["controls"][0]["pixels"]=[100,100]
  with self.assertRaises(AssertionError):m.check(e,m0,s,l)
 def test_fake_woodblock(self):
  e,m0,s,l=copy.deepcopy(self.data);e["adjudication"]["identical_physical_woodblock_proven"]=True
  with self.assertRaises(AssertionError):m.check(e,m0,s,l)
 def test_fake_original_jp2(self):
  e,m0,s,l=copy.deepcopy(self.data);e["adjudication"]["original_jp2_acquired"]=True
  with self.assertRaises(AssertionError):m.check(e,m0,s,l)
 def test_artifact_sha_mismatch(self):
  e,m0,s,l=copy.deepcopy(self.data);e["acquisition"]["artifact_zip_sha256"]="0"*64
  with self.assertRaises(AssertionError):m.check(e,m0,s,l)
 def test_fake_historical_winner(self):
  e,m0,s,l=copy.deepcopy(self.data);e["adjudication"]["g893_six_numeric_winners"]=1
  with self.assertRaises(AssertionError):m.check(e,m0,s,l)
if __name__=="__main__":unittest.main()
