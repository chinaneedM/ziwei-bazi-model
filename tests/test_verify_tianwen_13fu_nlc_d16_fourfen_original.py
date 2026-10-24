import copy
import importlib.util
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"scripts/verify-tianwen-13fu-nlc-d16-fourfen-original.py"
spec=importlib.util.spec_from_file_location("check13fu",P)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class Test13FU(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=json.loads(mod.E.read_text("utf-8"))
        cls.fr=json.loads(mod.FR.read_text("utf-8"))
        cls.ft=json.loads(mod.FT.read_text("utf-8"))
    def test_source_literal_record(self):
        self.assertTrue(mod.check(self.e,self.fr,self.ft))
    def test_reject_invented_day30(self):
        e=copy.deepcopy(self.e);e["limits"]["nlc_day30_full_fourfen_literal"]="九二二一四三"
        with self.assertRaises(AssertionError):mod.check(e,self.fr,self.ft)
    def test_reject_rewritten_earlier_13ft(self):
        x=copy.deepcopy(self.ft);x["targets"][0]["nlc_fourfen_full_glyph_literal"]="六九五四"
        with self.assertRaises(AssertionError):mod.check(self.e,self.fr,x)
    def test_reject_wrong_original_sha(self):
        e=copy.deepcopy(self.e);e["original_field"]["roi_rgb_sha256"]="0"*64
        with self.assertRaises(AssertionError):mod.check(e,self.fr,self.ft)
    def test_reject_unit_inference(self):
        e=copy.deepcopy(self.e);e["original_field"]["machine_unit_value"]=0.6954
        with self.assertRaises(AssertionError):mod.check(e,self.fr,self.ft)
    def test_reject_copy_votes(self):
        e=copy.deepcopy(self.e);e["cross_original"]["new_physically_authenticated_witnesses"]=1
        with self.assertRaises(AssertionError):mod.check(e,self.fr,self.ft)
    def test_reject_day5_variant_winner(self):
        e=copy.deepcopy(self.e);e["limits"]["day5_opposing_origins"]["winner"]="五一七二"
        with self.assertRaises(AssertionError):mod.check(e,self.fr,self.ft)
if __name__=="__main__":unittest.main()
