import copy
import importlib.util
import unittest
from pathlib import Path

P=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-source-sidedness-13cf.py"
spec=importlib.util.spec_from_file_location("sidedness13cf",P)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class D17Sidedness13CF(unittest.TestCase):
    def setUp(self):
        self.e=m.load(m.E)
        self.src=m.bind_sources(self.e)
        self.s=m.load(m.STATE)
        self.l=m.load(m.LEDGER)
    def check(self,e=None,src=None,s=None,l=None):
        return m.check(self.e if e is None else e,
                       self.src if src is None else src,
                       self.s if s is None else s,
                       self.l if l is None else l)
    def test_positive(self):
        self.assertTrue(self.check())
    def test_reverse_source_left_right(self):
        e=copy.deepcopy(self.e)
        e["side_of_heading_controls"][1]["relationship"]="NUMERIC_TO_LEFT"
        with self.assertRaises(AssertionError):self.check(e=e)
    def test_fake_waseda_same_day_C(self):
        e=copy.deepcopy(self.e)
        e["interpretation_boundary"]["WASEDA_D16_7570_same_day_yingsuoji"]="7570.6624"
        with self.assertRaises(AssertionError):self.check(e=e)
    def test_fake_naj_C(self):
        e=copy.deepcopy(self.e)
        e["interpretation_boundary"]["NAJ_D17_7570_same_day_yingsuoji"]="7570.6624"
        with self.assertRaises(AssertionError):self.check(e=e)
    def test_fake_numeric_roi_box(self):
        e=copy.deepcopy(self.e)
        e["bounded_positions"][2]["bbox"][0]=1080
        with self.assertRaises(AssertionError):self.check(e=e)
    def test_fake_physical_copy_vote(self):
        e=copy.deepcopy(self.e)
        e["scope_firewall"]["new_physical_witnesses"]=1
        with self.assertRaises(AssertionError):self.check(e=e)
    def test_fake_prior_source_numeric(self):
        src=copy.deepcopy(self.src)
        next(x for x in src["BO"]["original_numeric_rois"] if x["key"]=="P23_D17_C")["value"]="7570.6624"
        with self.assertRaises(AssertionError):self.check(src=src)
    def test_future_batch_append(self):
        s=copy.deepcopy(self.s)
        l=copy.deepcopy(self.l)
        s["schema_version"]="1.999.0"
        s["historical_audit"]["current_focus"].append("13ZZ future source scope")
        s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.999.0"
        l["binding"]["reviewed_state_version"]="1.999.0"
        l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"])
        self.assertTrue(self.check(s=s,l=l))

if __name__=="__main__":
    unittest.main()
