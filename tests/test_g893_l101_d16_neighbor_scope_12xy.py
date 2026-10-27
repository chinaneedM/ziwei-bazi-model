#!/usr/bin/env python3
"""12XY anti-overclaim regression: original pixel evidence is not original numerical adjudication."""
import importlib.util
import pathlib
import unittest

PATH=pathlib.Path(__file__).resolve().parents[1]/"scripts/verify-g893-l101-d16-neighbor-scope-12xy.py"
spec=importlib.util.spec_from_file_location("g893_12xy",PATH)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class TestL101D16NativeGeometry(unittest.TestCase):
    def setUp(self):
        self.records=list(mod.load())

    def test_original_geometry_document_passes(self):
        self.assertEqual(mod.verify(*self.records)["status"],"PASS")

    def test_source_jpeg_digest_swap_fails(self):
        self.records[0]["source_pages"][0]["jpeg_sha256"]="0"*64
        with self.assertRaises(ValueError):mod.verify(*self.records)

    def test_l101_external_value_not_original_glyph(self):
        self.records[0]["original_manual_visual"]["lunar"]["original_complete_target_accumulated_degree_literal"]="五度二十四八一一二五"
        with self.assertRaises(ValueError):mod.verify(*self.records)

    def test_d16_foreign_second_difference_cannot_be_filled(self):
        self.records[0]["original_manual_visual"]["solar"]["original_second_difference_numeric_literal"]="5.2362"
        with self.assertRaises(ValueError):mod.verify(*self.records)

    def test_target_glyph_count_not_raised_without_source_field(self):
        self.records[0]["research_grade"]["complete_source_literal_fields_prior_and_now"]=5
        with self.assertRaises(ValueError):mod.verify(*self.records)

    def test_original_header_not_swapped(self):
        self.records[0]["replayed_original_rgb_regions"][0]["page_id"]="018b"
        with self.assertRaises(ValueError):mod.verify(*self.records)

    def test_no_independent_witness_from_same_copy_five_pages(self):
        self.records[0]["research_grade"]["new_independent_print_votes"]=1
        with self.assertRaises(ValueError):mod.verify(*self.records)

    def test_no_false_cross_edition_numeric_decision(self):
        self.records[0]["research_grade"]["final_cross_witness_numeric_or_mechanical_decisions"]=1
        with self.assertRaises(ValueError):mod.verify(*self.records)

if __name__=="__main__":
    unittest.main()
