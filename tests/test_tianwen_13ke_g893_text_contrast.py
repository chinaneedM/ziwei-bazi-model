"""G893 13KE source scope and opposed action verb regression."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
modpath=ROOT/"scripts/verify-tianwen-13ke-g893-text-contrast.py"
spec=importlib.util.spec_from_file_location("thirteen_ke",modpath)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class HistoricalSourceGradeTest(unittest.TestCase):
    def setUp(self):
        self.record=json.loads((ROOT/mod.DOC).read_text(encoding="utf-8"))
    def test_sources_are_received_not_original(self):
        self.assertEqual(mod.verify(self.record)["source_original_pages_added"],0)
    def test_huang_g893_167_has_no_original_leaf(self):
        bad=copy.deepcopy(self.record);bad["explicit_conflicts"][1]["independently_attested_original_printed_leaf"]=True
        with self.assertRaises(ValueError):mod.verify(bad)
    def test_ocr_opposite_polarity_preserved(self):
        bad=copy.deepcopy(self.record);bad["received_loci"]["huang"]["gain_loss_direction"]="GAIN_DECREASE_LOSS_INCREASE"
        with self.assertRaises(ValueError):mod.verify(bad)
    def test_no_scribal_error_from_receipt(self):
        bad=copy.deepcopy(self.record);bad["explicit_conflicts"][0]["historical_ocr_or_print_error_finalized"]=True
        with self.assertRaises(ValueError):mod.verify(bad)
    def test_original_g893_copy_not_multiplied(self):
        bad=copy.deepcopy(self.record);bad["comparator_identity"]["physical_independent_copy_delta"]=1
        with self.assertRaises(ValueError):mod.verify(bad)
    def test_mingshi_tiny_step_cannot_be_erased(self):
        bad=copy.deepcopy(self.record);bad["explicit_conflicts"][2]["huang_ocr"]="五秒八十一微"
        with self.assertRaises(ValueError):mod.verify(bad)
    def test_no_lineage_award_from_catalogs(self):
        bad=copy.deepcopy(self.record);bad["received_text_transmission_edges_awarded"]=1
        with self.assertRaises(ValueError):mod.verify(bad)

if __name__=="__main__":
    unittest.main()
