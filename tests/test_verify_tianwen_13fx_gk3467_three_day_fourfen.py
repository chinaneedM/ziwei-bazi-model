import copy, importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("v13fx",ROOT/"scripts/verify-tianwen-13fx-gk3467-three-day-fourfen.py")
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class Test13FX(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=v.read(v.EV);cls.fr=v.read(v.FR);cls.fw=v.read(v.FW)
        cls.fv=v.read(v.FV);cls.state=v.read(v.STATE);cls.ledger=v.read(v.LEDGER)
    def validate(self,e):
        return v.check(e,self.fr,self.fw,self.fv,self.state,self.ledger)
    def test_bound_original_three_day_glyphs(self):
        self.assertTrue(self.validate(self.e))
    def test_refuse_prior_six_glyph_as_original_fourfen(self):
        e=copy.deepcopy(self.e);e["forward_only_erratum"]["revised_original_fourfen_source_specific_day30"]="九二二一四三"
        with self.assertRaises(AssertionError):self.validate(e)
    def test_refuse_unverified_original_glyph_change(self):
        e=copy.deepcopy(self.e);e["original_fourfen_rows"][1]["digits"]="九二二一"
        with self.assertRaises(AssertionError):self.validate(e)
    def test_refuse_historical_winner(self):
        e=copy.deepcopy(self.e);e["limits"]["historical_day30_winner"]="九二二二"
        with self.assertRaises(AssertionError):self.validate(e)
    def test_refuse_nlc_target_transfer(self):
        e=copy.deepcopy(self.e);e["limits"]["nlc_p76_day30_fourfen_original_digits"]="九二二二"
        with self.assertRaises(AssertionError):self.validate(e)
    def test_refuse_old_record_silent_rewrite(self):
        e=copy.deepcopy(self.e);e["forward_only_erratum"]["earlier_day30_literal"]="九二二二"
        with self.assertRaises(AssertionError):self.validate(e)
    def test_refuse_another_physical_witness(self):
        e=copy.deepcopy(self.e);e["source"]["new_ancient_physical_witnesses"]=1
        with self.assertRaises(AssertionError):self.validate(e)
if __name__=="__main__":unittest.main()
