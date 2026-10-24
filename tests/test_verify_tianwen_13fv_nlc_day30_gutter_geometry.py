import copy
import importlib.util
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"scripts/verify-tianwen-13fv-nlc-day30-gutter-geometry.py"
s=importlib.util.spec_from_file_location("verify13fv",P)
v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Test13FV(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=json.loads(v.E.read_text("utf-8"))
        cls.ft=json.loads(v.FT.read_text("utf-8"))
        cls.fu=json.loads(v.FU.read_text("utf-8"))
        cls.fr=json.loads(v.FR.read_text("utf-8"))
    def check(self,x):return v.check(x,self.ft,self.fu,self.fr)
    def test_original_day_headers(self):self.assertTrue(self.check(self.e))
    def test_reject_inferred_d30_number(self):
        x=copy.deepcopy(self.e);x["geometry"]["day30_complete_fourfen_original_digits"]="九二二一四三"
        with self.assertRaises(AssertionError):self.check(x)
    def test_reject_wrong_day_31(self):
        x=copy.deepcopy(self.e);x["regions"][1]["day"]=30
        with self.assertRaises(AssertionError):self.check(x)
    def test_reject_gutter_as_fourfen(self):
        x=copy.deepcopy(self.e);x["regions"][3]["role"]="DIRECT_D30_FOURFEN"
        with self.assertRaises(AssertionError):self.check(x)
    def test_reject_wrong_roi_hash(self):
        x=copy.deepcopy(self.e);x["regions"][4]["sha256_rgb"]="0"*64
        with self.assertRaises(AssertionError):self.check(x)
    def test_reject_copy_vote(self):
        x=copy.deepcopy(self.e);x["limits"]["new_original_ancient_witnesses"]=1
        with self.assertRaises(AssertionError):self.check(x)
    def test_reject_new_unit_bridge(self):
        x=copy.deepcopy(self.e);x["comparison"]["original_numeric_unit_bridge"]="0.0001"
        with self.assertRaises(AssertionError):self.check(x)
if __name__=="__main__":unittest.main()
