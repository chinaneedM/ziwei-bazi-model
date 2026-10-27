#!/usr/bin/env python3
"""12YA tests for D16 bounded original source and sealed external-only arithmetic."""
import importlib.util
from pathlib import Path
import unittest
S=Path(__file__).resolve().parents[1]/"scripts/verify-g893-d16-solar-scope-12ya.py"
spec=importlib.util.spec_from_file_location("g893_12ya",S)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestBoundedSolarD16(unittest.TestCase):
    def setUp(self):self.p=list(m.load())
    def test_guard_passes(self):self.assertEqual(m.verify(*self.p)["status"],"PASS")
    def test_source_jpg_tamper(self):
        self.p[0]["direct_original_page_evidence"][2]["jpeg_sha256"]="0"*64
        with self.assertRaises(ValueError):m.verify(*self.p)
    def test_original_roi_tamper(self):
        self.p[0]["original_rgb_roi"]["regions"][2]["sha256"]="0"*64
        with self.assertRaises(ValueError):m.verify(*self.p)
    def test_import_received_value_as_g893_d16(self):
        self.p[0]["visual_interpretation"]["candidate_full_d16_original_target_literal"]="五分一三六二"
        with self.assertRaises(ValueError):m.verify(*self.p)
    def test_false_whole_book_negative_proof(self):
        self.p[0]["visual_interpretation"]["negative_evidence_whole_manuscript"]=True
        with self.assertRaises(ValueError):m.verify(*self.p)
    def test_wrong_decimal_result(self):
        self.p[0]["external_edition_arithmetic"]["derived_strings"]["symmetric_neighbor_midpoint"]="5.1362"
        with self.assertRaises(ValueError):m.verify(*self.p)
    def test_invent_g893_transmission_cause(self):
        self.p[0]["external_edition_arithmetic"]["does_not_identify_transmission_cause"]=False
        with self.assertRaises(ValueError):m.verify(*self.p)
    def test_force_numeric_variant_closure(self):
        self.p[0]["safeguards"]["all_six_cross_edition_mechanical_variant_final_decisions"]=1
        with self.assertRaises(ValueError):m.verify(*self.p)
    def test_prior_12xy_negative_grade_rewritten(self):
        self.p[3]["original_manual_visual"]["solar"]["original_second_difference_numeric_literal"]="5.2362"
        with self.assertRaises(ValueError):m.verify(*self.p)
if __name__=="__main__":unittest.main()
