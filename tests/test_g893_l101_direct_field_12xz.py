#!/usr/bin/env python3
"""12XZ mutation tests: zero glyph, source/neighbor/header SHA and numeric firewall."""
import importlib.util
from pathlib import Path
import unittest
SCRIPT=Path(__file__).resolve().parents[1]/"scripts/verify-g893-l101-direct-field-12xz.py"
spec=importlib.util.spec_from_file_location("g893_l101_12xz",SCRIPT)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
class TestG893L101DirectOriginal(unittest.TestCase):
    def setUp(self): self.a=list(mod.load())
    def test_valid_source(self): self.assertEqual(mod.verify(*self.a)["result"],"PASS")
    def test_swapped_zero_place(self):
        self.a[0]["target"]["original_literal_full_field"]="五度二十四八一一二五"
        with self.assertRaises(ValueError): mod.verify(*self.a)
    def test_swapped_source_original_page_sha(self):
        self.a[0]["source_page"]["source_original_sha256"]="0"*64
        with self.assertRaises(ValueError): mod.verify(*self.a)
    def test_wrong_header_field(self):
        self.a[0]["structural_header"]["observed_column_label"]="遲疾曆日率"
        with self.assertRaises(ValueError): mod.verify(*self.a)
    def test_swapped_roi_pixels(self):
        self.a[0]["original_rgb_pixel_regions"]["regions"][0]["rgb_pixel_sha256"]="0"*64
        with self.assertRaises(ValueError): mod.verify(*self.a)
    def test_numeric_mechanics_not_proven_by_glyph(self):
        self.a[0]["target"]["cross_witness_numeric_variant_final_decision"]="SAME"
        with self.assertRaises(ValueError): mod.verify(*self.a)
    def test_historical_geometry_not_overwritten(self):
        self.a[3]["original_manual_visual"]["lunar"]["original_complete_target_accumulated_degree_literal"]="五度二十〇分四八一一二五"
        with self.assertRaises(ValueError): mod.verify(*self.a)
    def test_false_source_witness_voting(self):
        self.a[0]["safeguards"]["new_source_registry_records"]=1
        with self.assertRaises(ValueError): mod.verify(*self.a)
if __name__=="__main__": unittest.main()
