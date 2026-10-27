import copy
import importlib.util
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
path=ROOT / "scripts/verify-tianwen-13ft-nlc-gk3467-counterparts.py"
spec=importlib.util.spec_from_file_location("check13ft",path)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
class Test13FT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=json.loads(mod.E.read_text(encoding="utf-8"))
        cls.fr=json.loads(mod.FR.read_text(encoding="utf-8"))
    def test_valid_record(self):
        self.assertTrue(mod.check(self.e,self.fr))
    def test_no_invented_nlc_numeric(self):
        x=copy.deepcopy(self.e);x["targets"][0]["nlc_fourfen_full_glyph_literal"]="六九五四"
        with self.assertRaises(AssertionError):mod.check(x,self.fr)
    def test_no_counterfeit_extra_copy(self):
        x=copy.deepcopy(self.e);x["decisions"]["new_ancient_copy_votes"]=2
        with self.assertRaises(AssertionError):mod.check(x,self.fr)
    def test_no_fake_roi_sha(self):
        x=copy.deepcopy(self.e);x["targets"][1]["roi_rgb_sha256"]="0"*64
        with self.assertRaises(AssertionError):mod.check(x,self.fr)
    def test_no_historic_winner(self):
        x=copy.deepcopy(self.e);x["decisions"]["day30_final_historical_winner"]="九二二一四三"
        with self.assertRaises(AssertionError):mod.check(x,self.fr)
if __name__=="__main__":unittest.main()
