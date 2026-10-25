import copy
import importlib.util
import json
from pathlib import Path
import unittest
R=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('roi_13go',R/'scripts/verify-tianwen-13go-embedded-roi-coverage.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class ROI13GOTest(unittest.TestCase):
 def setUp(self):self.e=json.loads(m.E.read_text(encoding='utf8'))
 def test_original_source_links_and_estimates(self):self.assertTrue(m.check(self.e))
 def test_false_d14_coverage_is_rejected(self):
  self.e['cases'][1]['saved_roi_contains_projected']=True
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_false_d30_coverage_is_rejected(self):
  self.e['cases'][2]['saved_roi_contains_projected']=True
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_dimensions_not_pixel_registration(self):
  self.e['pixel_registration_verified']=True
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_cannot_invent_historic_digit(self):
  self.e['unresolved']['NLC_old_D30_complete_literal']='四分九二二二'
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_cannot_relabel_prior_target_strip(self):
  self.e['cases'][2]['prior_render_union_xyxy']=[551,405,592,790]
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_new_probe_is_not_clipped(self):
  self.e['cases'][1]['proposed_followup_embedded_probe_xyxy']=[130,555,159,830]
  with self.assertRaises(AssertionError):m.check(self.e)
if __name__=='__main__':unittest.main()
