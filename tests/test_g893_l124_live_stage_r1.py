#!/usr/bin/env python3
"""12XX negative tests for original-page, glyph, and stage evidence integrity."""
import importlib.util
import pathlib
import unittest

PATH=pathlib.Path(__file__).resolve().parents[1]/"scripts/verify-g893-l124-live-stage-r1.py"
spec=importlib.util.spec_from_file_location("g893_l124",PATH)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class TestG893L124(unittest.TestCase):
    def setUp(self):
        self.records=list(mod.load())
    def test_evidence_pass(self):
        self.assertEqual(mod.validate(*self.records)["status"],"PASS")
    def test_swap_original_page_hash_fails(self):
        self.records[0]["source_page"]["source_original_sha256"]="0"*64
        with self.assertRaises(ValueError):mod.validate(*self.records)
    def test_swap_glyph_digit_fails(self):
        self.records[0]["target"]["original_literal_full_field"]="一度〇八二一"
        with self.assertRaises(ValueError):mod.validate(*self.records)
    def test_wrong_column_semantics_fails(self):
        self.records[0]["structural_header"]["observed_column_label"]="遲疾曆日率"
        with self.assertRaises(ValueError):mod.validate(*self.records)
    def test_false_numeric_adjudication_fails(self):
        self.records[0]["target"]["historical_cross_witness_mechanical_final_decision"]="SAME"
        with self.assertRaises(ValueError):mod.validate(*self.records)
    def test_wrong_roi_original_page_fails(self):
        self.records[0]["original_rgb_pixel_regions"]["regions"][0]["page_id"]="018b"
        with self.assertRaises(ValueError):mod.validate(*self.records)
    def test_erased_historical_12xw_fails(self):
        self.records[3]["complete_source_literal_field_count"]=4
        with self.assertRaises(ValueError):mod.validate(*self.records)

if __name__=="__main__":unittest.main()
