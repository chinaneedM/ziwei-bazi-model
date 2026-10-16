#!/usr/bin/env python3
"""12YD original-source and anti-overclaim regression tests."""
import importlib.util
from pathlib import Path
import unittest
sp=Path(__file__).resolve().parents[1]/"scripts/verify-g893-solar-original-short-lane-12yd.py"
spec=importlib.util.spec_from_file_location("g893_12yd",sp);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class OriginalSolarSource(unittest.TestCase):
 def setUp(self):self.p=list(m.load())
 def test_pass(self):self.assertEqual(m.verify(*self.p)["status"],"PASS")
 def test_page_tamper(self):
  self.p[0]["direct_original_pages"][1]["jpeg_sha256"]="0"*64
  with self.assertRaises(ValueError):m.verify(*self.p)
 def test_roi_tamper(self):
  self.p[0]["native_rgb_regions"]["regions"][5]["sha256"]="0"*64
  with self.assertRaises(ValueError):m.verify(*self.p)
 def test_fake_d16(self):
  self.p[0]["original_reading_scope"]["candidate_full_d16_target_second_difference_field_literal"]="五分二三六二"
  with self.assertRaises(ValueError):m.verify(*self.p)
 def test_day16_digit_changed(self):
  self.p[0]["original_reading_scope"]["source_bounded_candidate_vertical_lane"][1]["original_short_glyph_string"]="五分一三六二"
  with self.assertRaises(ValueError):m.verify(*self.p)
 def test_step_changed(self):
  self.p[0]["arithmetic_on_source_scoped_candidate_digits"]["day17_minus_day16"]="0.0286"
  with self.assertRaises(ValueError):m.verify(*self.p)
 def test_false_unit_bridge(self):
  self.p[0]["arithmetic_on_source_scoped_candidate_digits"]["solar_header_increment_unit_identity"]="CONFIRMED"
  with self.assertRaises(ValueError):m.verify(*self.p)
 def test_physical_copy_double_count(self):
  self.p[0]["scope_guard"]["new_independent_physical_copies"]=1
  with self.assertRaises(ValueError):m.verify(*self.p)
 def test_old_12ya_promoted(self):
  self.p[1]["visual_interpretation"]["candidate_full_d16_original_target_literal"]="五分二三六二"
  with self.assertRaises(ValueError):m.verify(*self.p)
 def test_state_out_of_sync(self):
  self.p[3]["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.616.0"
  with self.assertRaises(ValueError):m.verify(*self.p)
if __name__=="__main__":unittest.main()
