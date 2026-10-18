import copy
import importlib.util
import sys
import unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-waseda-13i.py"
spec=importlib.util.spec_from_file_location("goryeosa_waseda_13i",P)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
class Waseda13IGates(unittest.TestCase):
    def test_research_gate_passes(self):self.assertEqual(mod.verify()["status"],"PASS")
    def test_invented_1454_impression_rejected(self):
        e=mod.rd(mod.E);e["waseda_first_party"]["edition_impression_year"]=1454
        with self.assertRaises(AssertionError):mod.check_evidence(e)
    def test_invented_original_glyph_rejected(self):
        e=mod.rd(mod.E);e["waseda_first_party"]["d16_original_glyph"]="五分二三六二"
        with self.assertRaises(AssertionError):mod.check_evidence(e)
    def test_upload_filename_not_proven_wrong_copy(self):
        e=mod.rd(mod.E);e["ncl_commons_proxy"]["filename_difference_proves_misidentification"]=True
        with self.assertRaises(AssertionError):mod.check_evidence(e)
if __name__=="__main__":unittest.main()
