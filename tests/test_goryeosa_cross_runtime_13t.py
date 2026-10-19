import copy,unittest,importlib.util
from pathlib import Path
f=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-cross-runtime-13t.py"
s=importlib.util.spec_from_file_location("correct13t",f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class OriginalPixelCorrection13T(unittest.TestCase):
 def test_static(self):self.assertTrue(m.check(m.load(m.E)))
 def test_no_extra_physical_votes(self):
  e=copy.deepcopy(m.load(m.E));e["safety"]["independent_physical_numeric_votes"]=1
  with self.assertRaises(AssertionError):m.check(e)
 def test_no_renaming_failed_run(self):
  e=copy.deepcopy(m.load(m.E));e["failed_workflow"]["run_id"]=39203882273
  with self.assertRaises(AssertionError):m.check(e)
 def test_still_has_original_sha(self):
  e=copy.deepcopy(m.load(m.E));e["page_checks"][1]["decoded_grayscale_pixels_sha256"]="f"*64
  with self.assertRaises(AssertionError):m.check(e)
if __name__=="__main__":unittest.main()
