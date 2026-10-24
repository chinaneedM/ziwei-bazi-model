import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("verify13fw", ROOT/"scripts/verify-tianwen-13fw-goryeosa-d30-received-arithmetic.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

class Test13FW(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e = json.loads(v.EV.read_text("utf-8"))
        cls.fr = json.loads(v.FR.read_text("utf-8"))
        cls.fv = json.loads(v.FV.read_text("utf-8"))
    def validate(self,e):
        return v.check(e,self.fr,self.fv)
    def test_frozen_received_fourfen_sequence_and_existing_gates(self):
        self.assertTrue(self.validate(self.e))
    def test_reject_changed_received_d30(self):
        e=copy.deepcopy(self.e)
        e["received_table"]["rows"][2]["numeric"]=9221
        with self.assertRaises(AssertionError):self.validate(e)
    def test_reject_silent_source_original_rewrite(self):
        e=copy.deepcopy(self.e)
        e["original_prior_records"]["fr_original_field_literal_reported"]="九二二二"
        with self.assertRaises(AssertionError):self.validate(e)
    def test_reject_nlc_d30_winner(self):
        e=copy.deepcopy(self.e)
        e["adjudication"]["nlc_day30_original_complete_digits"]="九二二二"
        with self.assertRaises(AssertionError):self.validate(e)
    def test_reject_historical_winner(self):
        e=copy.deepcopy(self.e)
        e["adjudication"]["historical_day30_fourfen_winner"]="四分九二二二"
        with self.assertRaises(AssertionError):self.validate(e)
    def test_reject_fabricated_original_image_review(self):
        e=copy.deepcopy(self.e)
        e["source"]["original_image_glyph_review_this_batch"]=True
        with self.assertRaises(AssertionError):self.validate(e)
    def test_reject_new_witness(self):
        e=copy.deepcopy(self.e)
        e["limits"]["new_historical_originals"]=1
        with self.assertRaises(AssertionError):self.validate(e)

if __name__ == "__main__":
    unittest.main()
