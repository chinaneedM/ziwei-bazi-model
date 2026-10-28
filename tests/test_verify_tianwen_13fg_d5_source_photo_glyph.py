import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-tianwen-13fg-d5-source-photo-glyph.py"
s=importlib.util.spec_from_file_location("v13fg",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Test13FG(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=v.read(v.P);cls.s=v.read(v.S);cls.l=v.read(v.L)
 def test_positive_source_evidence(self):self.assertTrue(v.check(self.e,self.s,self.l))
 def test_live_source_growth_does_not_rewrite_13fg_snapshot(self):
  self.assertGreater(self.s["historical_audit"]["external_source_registry_total_unique_count"],self.e["impact"]["source_registry_total_unique_count"])
 def test_reject_tampering_with_frozen_13fg_source_count(self):
  self.deny(lambda x:x["impact"].update(source_registry_total_unique_count=763))
 def test_live_source_count_cannot_go_below_13fg_snapshot(self):
  s=copy.deepcopy(self.s);s["historical_audit"]["external_source_registry_total_unique_count"]=760
  with self.assertRaises(AssertionError):v.check(self.e,s,self.l)

 def deny(self,fn):
  x=copy.deepcopy(self.e);fn(x)
  with self.assertRaises(AssertionError):v.check(x,self.s,self.l)
 def test_forged_photo_five(self):self.deny(lambda x:x["D5_direct_visual_image_evidence"].update(directly_read_literal="四分〇一七二"))
 def test_forged_crop_sha(self):self.deny(lambda x:x["D5_direct_visual_image_evidence"].update(original_RGB_fourfen_lane_sha256="0"*64))
 def test_forged_original_book(self):self.deny(lambda x:x["D5_direct_visual_image_evidence"].update(physical_original_book_number=22))
 def test_fake_numeric_winner(self):self.deny(lambda x:x["opposing_prior_source"].update(historic_true_winner="FIVE"))
 def test_ncl_retraction(self):self.deny(lambda x:x["opposing_prior_source"].update(NCL_O_original_reading_withdrawn=True))
 def test_fake_independent_edition(self):self.deny(lambda x:x["impact"].update(separately_authenticated_independent_ancient_editions_added=1))
 def test_forged_missing_folios(self):self.deny(lambda x:x["source_image_recovery"].update(outstanding_transport_error_indices=[]))
 def test_fake_algorithm_reopen(self):self.deny(lambda x:x["impact"].update(chart_algorithm_reopens=1))
if __name__=="__main__":unittest.main()
