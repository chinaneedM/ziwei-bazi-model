import copy
import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('embedded_grade',ROOT/'scripts/verify-tianwen-13gn-embedded-image-grade.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class EmbeddedGradeTest(unittest.TestCase):
 def setUp(self):self.e=json.loads(m.E.read_text(encoding='utf-8'))
 def test_sealed_source_rois(self):self.assertTrue(m.check(self.e))
 def test_render_grid_is_not_embedded_grid(self):
  self.e['pages'][0]['embedded']['size']=[1305,873]
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_old_coordinates_must_not_be_reused(self):
  self.e['pages'][0]['review_rois'][0]['coordinate_grid']='PRIOR_RENDER_PIXELS'
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_interpolation_is_not_source_reading(self):
  self.e['pages'][2]['review_rois'][0]['complete_original_literal']='四分九二二二'
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_same_pdf_is_not_new_witness(self):
  self.e['new_physical_witnesses']=1
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_old_snapshot_cannot_be_rehashed(self):
  self.e['pages'][0]['previous_render']['rgb_sha256']='0'*64
  with self.assertRaises(AssertionError):m.check(self.e)
if __name__=='__main__':unittest.main()
