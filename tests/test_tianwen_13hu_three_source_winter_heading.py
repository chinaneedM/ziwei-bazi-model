import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location("hu",ROOT/"scripts/verify-tianwen-13hu-three-source-winter-heading.py")
M=importlib.util.module_from_spec(S);S.loader.exec_module(M)
class CrossSourceHeadingTest(unittest.TestCase):
 def setUp(self):self.e=json.loads(M.P.read_text(encoding="utf8"))
 def test_handoff_and_original_photo_linkage(self):self.assertTrue(M.check(self.e))
 def test_mismatching_na_j_shas_not_accepted(self):
  x=copy.deepcopy(self.e);x["source_scoped_image_objects"][0]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_mismatching_waseda_original_not_accepted(self):
  x=copy.deepcopy(self.e);x["source_scoped_image_objects"][1]["observed_heading"]="太陽冬至前後二氣盈初縮末限"
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_no_physical_copy_inflation(self):
  x=copy.deepcopy(self.e);x["physical_holdings"]["new_independent_historical_votes"]=1
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_no_numeric_winner_by_shared_title(self):
  x=copy.deepcopy(self.e);x["family_scope"]["title_same_wording_does_not_transfer_numeric_fields"]=False
  with self.assertRaises(AssertionError):M.check(x,False)
