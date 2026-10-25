import copy
import importlib.util
import json
import unittest
from pathlib import Path

R = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("gy", R / "scripts/verify-tianwen-13gy-header-numeric-overlap.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class OverlapFirewall(unittest.TestCase):
    def setUp(self):
        self.e = json.loads(m.E.read_text(encoding="utf-8"))

    def test_forward_only_original_overlap(self):
        self.assertTrue(m.check(self.e))

    def test_erase_overlap_rejected(self):
        self.e["geometry"]["intersection_xyxy"] = [135,680,171,822]
        with self.assertRaises(AssertionError): m.check(self.e)

    def test_false_area_rejected(self):
        self.e["geometry"]["intersection_area_px2"] = 0
        with self.assertRaises(AssertionError): m.check(self.e)

    def test_false_numeric_value_rejected(self):
        self.e["interpretation"]["fully_certified_D14_numeric"] = "四分六六三〇"
        with self.assertRaises(AssertionError): m.check(self.e)

    def test_old_snapshot_hash_immutable(self):
        self.e["source_snapshots"][2]["git_blob_sha"] = "0"*40
        with self.assertRaises(AssertionError): m.check(self.e)

    def test_false_mechanical_nonidentity_rejected(self):
        self.e["interpretation"]["fourfen_chudu_mechanical_identity"] = False
        with self.assertRaises(AssertionError): m.check(self.e)

    def test_false_lower_terminal_certification_rejected(self):
        self.e["interpretation"]["lower_y822_1060_numeric_certified"] = True
        with self.assertRaises(AssertionError): m.check(self.e)

    def test_false_independent_witness_rejected(self):
        self.e["guards"]["new_physical_witnesses"] = 1
        with self.assertRaises(AssertionError): m.check(self.e)

if __name__ == "__main__":
    unittest.main()
