#!/usr/bin/env python3
"""12XW regression: source page, evidence grade, and mechanical decision boundaries."""
import importlib.util
import pathlib
import unittest

SCRIPT=pathlib.Path(__file__).resolve().parents[1]/"scripts/verify-g893-cross-ledger-live-stage-12xw.py"
spec=importlib.util.spec_from_file_location("g893_12xw",SCRIPT)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class TestSourceStageReconciliation(unittest.TestCase):
    def setUp(self):
        self.parts=list(module.read_inputs())
    def test_exact_stage_passes(self):
        self.assertEqual(module.verify(*self.parts)["status"],"PASS")
    def test_swapped_source_page_hash_fails(self):
        self.parts[0]["original_day_page_locators"][0]["page_sha256"]="0"*64
        with self.assertRaises(ValueError): module.verify(*self.parts)
    def test_pixel_only_region_cannot_claim_historical_number(self):
        self.parts[6]["reviews"][0]["numeric_value"]="5.2362"
        with self.assertRaises(ValueError): module.verify(*self.parts)
    def test_old_stage_cannot_be_silently_edited(self):
        self.parts[0]["historic_g893_witness_stage"]="SIX_PAGES_LOCATED"
        with self.assertRaises(ValueError): module.verify(*self.parts)
    def test_original_full_glyph_not_numeric_adjudication(self):
        self.parts[0]["final_cross_edition_mechanical_variant_decisions"]=1
        with self.assertRaises(ValueError): module.verify(*self.parts)
    def test_remaining_three_source_columns_cannot_disappear(self):
        self.parts[0]["unresolved_source_full_field_controls"]=[]
        with self.assertRaises(ValueError): module.verify(*self.parts)

if __name__=="__main__":
    unittest.main()
