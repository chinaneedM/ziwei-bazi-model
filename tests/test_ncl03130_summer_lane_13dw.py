import copy
import importlib.util
import unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-summer-lane-13dw.py"
spec=importlib.util.spec_from_file_location("check13dw",p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class TestNCL03130Lane13DW(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L)
    def go(self,e=None):
        return m.check(self.e if e is None else e,self.s,self.l)
    def bad(self,fn):
        e=copy.deepcopy(self.e);fn(e)
        with self.assertRaises(AssertionError):
            self.go(e)
    def test_positive(self): self.assertTrue(self.go())
    def test_false_decimal_fails_closed(self): self.bad(lambda e:e["source_native_d28_unit_band"].update(exact_xingdu_decimal="0.994549"))
    def test_false_original_value_fails_closed(self): self.bad(lambda e:e["cross_original_scope"].update(ncl03130_day28_printed_xingdu="0.994549"))
    def test_fake_field_scope_fails_closed(self): self.bad(lambda e:e["source_native_d28_unit_band"].update(exact_xingdu_locus="RESOLVED"))
    def test_fake_independent_witness_fails_closed(self): self.bad(lambda e:e["resolution"].update(new_stemmatic_votes=1))
    def test_wrong_day_roi_fails_closed(self): self.bad(lambda e:e["p86_native_roi_provenance"]["rois"][1].update(png_sha256="0"*64))
    def test_wrong_unit_head_fails_closed(self): self.bad(lambda e:e["source_native_d28_unit_band"].update(header_glyphs_right_to_left=["行","度"]))
if __name__=="__main__": unittest.main()
