"""13MV fail-closed arithmetic and source-scoped time origin."""
import copy,importlib.util,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("v13mv",R/"scripts/verify-tianwen-13mv-dayzero-recurrence.py")
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class DayZeroRecurrence(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.inputs=[json.loads(p.read_text(encoding="utf8")) for p in (v.E,v.MU,v.MR,v.S,v.L)]
 def test_positive(self):
  self.assertEqual(v.check(*self.inputs)["status"],"PASS")
 def mutate_and_fail(self,route,value):
  a=copy.deepcopy(self.inputs)
  d=a[0]
  for k in route[:-1]:d=d[k]
  d[route[-1]]=value
  with self.assertRaises(AssertionError):v.check(*a)
 def test_false_zero_day_value(self):
  self.mutate_and_fail(["original_source_local_day_anchor","day0_short"],"4.9387")
 def test_false_day_fifteen(self):
  self.mutate_and_fail(["original_source_local_day_anchor","day15_short"],"5.2177")
 def test_false_middle_lane(self):
  self.mutate_and_fail(["original_source_local_lane_recurrence","d16_middle"],"429.6074")
 def test_false_cumulative_lane(self):
  self.mutate_and_fail(["original_source_local_lane_recurrence","d16_lower_cumulative"],"7570.6625")
 def test_absolute_epoch_overclaim_rejected(self):
  self.mutate_and_fail(["bounds","day0_is_absolute_calendar_epoch"],True)
 def test_fake_cross_original_winner_rejected(self):
  self.mutate_and_fail(["bounds","g893_final_historical_winners"],1)
 def test_false_new_pixel_hash_rejected(self):
  self.mutate_and_fail(["original_source_local_day_anchor","page14_firstday_glyph_pixels_newly_rehashed"],True)
if __name__=="__main__":unittest.main()
