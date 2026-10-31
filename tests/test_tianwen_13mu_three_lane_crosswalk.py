"""13MU direct original source column comparison and context digit-elision gate."""
import copy,importlib.util,json,unittest,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("v13mu",R/"scripts/verify-tianwen-13mu-three-lane-crosswalk.py")
v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class ThreeLane(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.d=[json.loads(f.read_text(encoding="utf-8")) for f in (v.E,v.S,v.L,v.Q)]
 def test_original_metadata_and_arithmetic(self):self.assertEqual(v.check(*self.d)["status"],"PASS")
 def test_fake_zhou_cumulative_digit_rejected(self):
  a=copy.deepcopy(self.d);a[0]["rows"][1]["zhou_lower_normalized"]="7570.6625"
  with self.assertRaises(AssertionError):v.check(*a)
 def test_fake_same_role_mismatch_rejected(self):
  a=copy.deepcopy(self.d);a[0]["forward_only_adjudication"]["wrong_comparator_for_same_field_historical_disagreement"]=False
  with self.assertRaises(AssertionError):v.check(*a)
 def test_fake_original_digit_entirely_printed_rejected(self):
  a=copy.deepcopy(self.d);a[0]["visible_original_context"]["normalized_from_context_not_all_glyphs_printed_each_day"]=False
  with self.assertRaises(AssertionError):v.check(*a)
 def test_fake_historical_winner_rejected(self):
  a=copy.deepcopy(self.d);a[0]["forward_only_adjudication"]["G893_six_final_historical_winners"]=1
  with self.assertRaises(AssertionError):v.check(*a)
 def test_source_pixel_optional(self):
  source=os.getenv("TIANWEN_13MU_ZHOU_PDF")
  if not source:self.skipTest("Source PDF not present in CI; metadata-only")
  self.assertEqual(v.pixel_replay(self.d[0],source)["rgb_roi_hashes_verified"],5)
 def test_forward_successor(self):
  a=copy.deepcopy(self.d);a[1]["schema_version"]="1.984.0";a[1]["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.984.0";a[1]["historical_audit"]["current_focus"].append("13MV successor")
  a[2]["binding"]["reviewed_state_version"]="1.984.0";a[2]["binding"]["source_focus_count"]+=1
  self.assertEqual(v.check(*a)["status"],"PASS")
if __name__=="__main__":unittest.main()
