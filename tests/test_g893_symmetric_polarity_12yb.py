#!/usr/bin/env python3
"""12YB anti-overclaim and integrity tests."""
import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location("g893_12yb",Path(__file__).resolve().parents[1]/"scripts/verify-g893-symmetric-polarity-12yb.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class OriginalSameCopyPolarity(unittest.TestCase):
    def setUp(self):self.p=list(m.load())
    def test_good(self):self.assertEqual(m.verify(*self.p)["status"],"PASS")
    def test_changed_original_page(self):
        self.p[0]["source_pages"][1]["jpeg_sha256"]="0"*64
        with self.assertRaises(ValueError):m.verify(*self.p)
    def test_changed_original_roi(self):
        self.p[0]["original_rgb_regions"][0]["sha256"]="0"*64
        with self.assertRaises(ValueError):m.verify(*self.p)
    def test_swapped_gain_loss(self):
        self.p[0]["direct_human_reading"]["rows"][0]["polarity_glyph"]="損"
        with self.assertRaises(ValueError):m.verify(*self.p)
    def test_invented_full_numeric(self):
        self.p[0]["direct_human_reading"]["rows"][1]["normalized_value"]="1.2345"
        with self.assertRaises(ValueError):m.verify(*self.p)
    def test_promote_symmetry(self):
        self.p[0]["epistemic_boundary"]["original_l35_l159_symmetric_numeric_relation"]="PROVED"
        with self.assertRaises(ValueError):m.verify(*self.p)
    def test_invent_d16(self):
        self.p[0]["epistemic_boundary"]["original_solar_d16_value_and_column"]="5.2362"
        with self.assertRaises(ValueError):m.verify(*self.p)
    def test_double_count_same_copy(self):
        self.p[0]["epistemic_boundary"]["added_independent_physical_witnesses"]=1
        with self.assertRaises(ValueError):m.verify(*self.p)
    def test_omission_unreviewed(self):
        self.p[2]["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.614.0"
        with self.assertRaises(ValueError):m.verify(*self.p)
if __name__=="__main__":unittest.main()
