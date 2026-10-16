#!/usr/bin/env python3
"""12YC source-glyph and mechanical non-promotion integrity tests."""
import importlib.util
from pathlib import Path
import unittest
p=Path(__file__).resolve().parents[1]/"scripts/verify-g893-symmetric-original-pairs-12yc.py"
spec=importlib.util.spec_from_file_location("g893_12yc",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SameCopySourcePairs(unittest.TestCase):
    def setUp(self):self.parts=list(m.load())
    def test_pass(self):self.assertEqual(m.verify(*self.parts)["status"],"PASS")
    def test_swapped_original_page(self):
        self.parts[0]["original_page_evidence"][2]["jpeg_sha256"]="0"*64
        with self.assertRaises(ValueError):m.verify(*self.parts)
    def test_changed_source_roi(self):
        self.parts[0]["original_rgb_roi"]["regions"][4]["sha256"]="0"*64
        with self.assertRaises(ValueError):m.verify(*self.parts)
    def test_glyph_zero_elided(self):
        self.parts[0]["direct_original_collation"]["rows"][3]["numeric_glyphs"]="一十分五六一七七五"
        with self.assertRaises(ValueError):m.verify(*self.parts)
    def test_swapped_original_sign(self):
        self.parts[0]["direct_original_collation"]["rows"][1]["polarity"]="損"
        with self.assertRaises(ValueError):m.verify(*self.parts)
    def test_fake_general_table_rule(self):
        self.parts[0]["direct_original_collation"]["complete_limit_table_global_symmetry_rule"]="PROVEN"
        with self.assertRaises(ValueError):m.verify(*self.parts)
    def test_numeric_promotion(self):
        self.parts[0]["direct_original_collation"]["normalized_numeric_values"]={"8":"10.561775"}
        with self.assertRaises(ValueError):m.verify(*self.parts)
    def test_fake_d16_closure(self):
        self.parts[0]["controls"]["primary_solar_d16_field_identity"]="5.2362"
        with self.assertRaises(ValueError):m.verify(*self.parts)
    def test_fake_copy_vote(self):
        self.parts[0]["controls"]["new_independent_physical_witnesses"]=1
        with self.assertRaises(ValueError):m.verify(*self.parts)
    def test_old_12xu_rewritten(self):
        self.parts[1]["original_fields"][0]["complete_original_literal"]="益十〇分五六一七七五"
        with self.assertRaises(ValueError):m.verify(*self.parts)
    def test_unreviewed_state(self):
        self.parts[4]["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.615.0"
        with self.assertRaises(ValueError):m.verify(*self.parts)
if __name__=="__main__":unittest.main()
