import copy
import importlib.util
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"scripts/verify-tianwen-13fr-gk3467-day16-day30.py"
spec=importlib.util.spec_from_file_location("fr13",P)
v=importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
class Day16Day30OriginalSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=json.loads(v.E.read_text(encoding="utf-8"))
    def reject(self,mutate):
        d=copy.deepcopy(self.e)
        mutate(d)
        with self.assertRaises(AssertionError):
            v.check(d)
    def test_source_scoped_replay_metadata(self):
        self.assertTrue(v.check(self.e))
    def test_reject_day16_glyph_mutation(self):
        self.reject(lambda d:d["readings"][0].update(numeric_glyph_literal="六九五三"))
    def test_reject_day30_glyph_mutation(self):
        self.reject(lambda d:d["readings"][1].update(numeric_glyph_literal="九二二一四二"))
    def test_reject_historic_winner(self):
        self.reject(lambda d:d["adjudication"].update(day30_historical_winner="九二二一四三"))
    def test_reject_unit_bridge_inference(self):
        self.reject(lambda d:d["adjudication"].update(original_column_labels_to_modern_unit_bridge="PROVEN"))
    def test_reject_unverified_ancient_folio(self):
        self.reject(lambda d:d["readings"][0].update(ancient_folio_number=12))
    def test_reject_pdf_source_swap(self):
        self.reject(lambda d:d["original_pdf"].update(pdf_sha256="0"*64))
if __name__=="__main__":
    unittest.main()
