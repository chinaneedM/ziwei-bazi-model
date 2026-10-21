import copy
import importlib.util
import unittest
from pathlib import Path

p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-crossfield-label-alignment-13cd.py"
spec=importlib.util.spec_from_file_location("cross13cd",p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class Cross13CD(unittest.TestCase):
    def setUp(self):
        self.e=m.load(m.E)
        self.src=m.evidence_files_and_sha(self.e)
        self.s=m.load(m.S)
        self.l=m.load(m.L)
    def go(self,e=None,src=None,s=None,l=None):
        return m.check(self.e if e is None else e,
                       self.src if src is None else src,
                       self.s if s is None else s,
                       self.l if l is None else l)
    def test_positive(self):
        self.assertTrue(self.go())
    def test_fake_uniform_two_field_day_shift(self):
        e=copy.deepcopy(self.e)
        e["positive_literal_position_matches"][0]["naj_printed_day"]=18
        with self.assertRaises(AssertionError):self.go(e=e)
    def test_fake_field_numeric(self):
        src=copy.deepcopy(self.src)
        next(x for x in src["W"]["original_numeric_rois"] if x["key"]=="P23_D17_C")["value"]="7999.2697"
        with self.assertRaises(AssertionError):self.go(src=src)
    def test_fake_same_day_naj_C17(self):
        e=copy.deepcopy(self.e)
        e["compared_observations"]["naj_D17_adjacent_numeral_field_identity"]="CUMULATIVE"
        with self.assertRaises(AssertionError):self.go(e=e)
    def test_fake_global_rule(self):
        e=copy.deepcopy(self.e)
        e["bounded_test"]["global_column_shift_convention_proven"]=True
        with self.assertRaises(AssertionError):self.go(e=e)
    def test_fake_stemmatic_vote(self):
        e=copy.deepcopy(self.e)
        e["source_independence"]["new_independent_stemmatic_votes"]=1
        with self.assertRaises(AssertionError):self.go(e=e)
    def test_fake_d16_field(self):
        e=copy.deepcopy(self.e)
        e["bounded_test"]["original_waseda_D16_isolated_yingsuoji"]="7570.6624"
        with self.assertRaises(AssertionError):self.go(e=e)
    def test_forward_only_future_focus(self):
        s=copy.deepcopy(self.s)
        l=copy.deepcopy(self.l)
        s["schema_version"]="1.800.0"
        s["historical_audit"]["current_focus"].append("13ZZ future")
        l["binding"]["reviewed_state_version"]="1.800.0"
        l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"])
        # The check here is a snapshot-specific handoff contract: explicit 13CD as latest,
        # so future stages must update the latest prefix and corresponding future verifier.
        with self.assertRaises(AssertionError):self.go(s=s,l=l)

if __name__=="__main__":unittest.main()
