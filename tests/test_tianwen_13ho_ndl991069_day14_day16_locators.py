import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("tianwen13ho",ROOT/"scripts/verify-tianwen-13ho-ndl991069-day14-day16-locators.py")
M=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(M)
class Ndl1909DayHeadingScope(unittest.TestCase):
 def setUp(self):self.e=json.loads(M.E.read_text(encoding="utf8"))
 def test_source_scope_and_handoff(self):self.assertTrue(M.check(self.e))
 def test_no_promotion_into_ancient_numeric(self):
  x=copy.deepcopy(self.e);x["evidence_effect"]["new_numeric_glyph_decisions"]=1
  with self.assertRaises(AssertionError):M.check(x)
 def test_no_false_original_fullres(self):
  x=copy.deepcopy(self.e);x["immutable_artifact"]["original_unscaled_full_resolution_obtained"]=True
  with self.assertRaises(AssertionError):M.check(x)
 def test_no_transfer_from_nikh(self):
  x=copy.deepcopy(self.e);x["limits"]["Taiwan_NCL03130_original_day14_complete"]="四分六六三〇"
  with self.assertRaises(AssertionError):M.check(x)
 def test_bbox_source_bounds(self):
  x=copy.deepcopy(self.e);x["observations"][0]["native_preview_heading_bbox_xyxy"]=[1020,590,1800,682]
  with self.assertRaises(AssertionError):M.check(x)
