import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("gz",ROOT/"scripts/verify-tianwen-13gz-native-segmentation.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class SourcePixelTiling(unittest.TestCase):
    def setUp(self):
        self.e=json.loads(mod.E.read_text(encoding="utf8"))
    def test_source_blob_and_exact_reassembly(self):
        result=mod.check(self.e)
        self.assertTrue(result["reconstruction_exact"])
        self.assertEqual(len(result["tiles"]),7)
    def test_header_lower_boundary(self):
        self.e["tiles"][0]["source_xyxy"][3]=679
        with self.assertRaises(AssertionError): mod.check(self.e)
    def test_mid_to_tail_boundary(self):
        self.e["tiles"][2]["source_xyxy"][1]=821
        with self.assertRaises(AssertionError): mod.check(self.e)
    def test_unsupported_numeric_claim(self):
        self.e["adjudication"]["historical_original_d14_complete_numeric"]="四分六六三〇"
        with self.assertRaises(AssertionError): mod.check(self.e)
    def test_false_terminal(self):
        self.e["adjudication"]["historical_original_d14_terminal_glyph"]="〇"
        with self.assertRaises(AssertionError): mod.check(self.e)
    def test_false_ancient_unit(self):
        self.e["adjudication"]["ancient_unit"]="分"
        with self.assertRaises(AssertionError): mod.check(self.e)
    def test_false_independent_source(self):
        self.e["provenance"]["new_independent_source_witnesses"]=1
        with self.assertRaises(AssertionError): mod.check(self.e)
    def test_pixel_copy_identity(self):
        self.e["provenance"]["png_git_blob_sha"]="0"*40
        with self.assertRaises(AssertionError): mod.check(self.e)
    def test_gutter_not_same_column(self):
        self.e["tiles"][5]["source_xyxy"][2]=181
        with self.assertRaises(AssertionError): mod.check(self.e)

if __name__=="__main__": unittest.main()
