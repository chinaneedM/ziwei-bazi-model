import copy
import importlib.util
import unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-fivepoint-original-received-offset-13bh.py"
spec=importlib.util.spec_from_file_location("research13bh",p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class FivePoint13BH(unittest.TestCase):
    def setUp(self):
        self.e=m.load(m.P); self.yz=m.load(m.PYZ); self.be=m.load(m.PBE)
        self.bf=m.load(m.PBF); self.bg=m.load(m.PBG)
        self.l=m.load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
        self.s=m.load("docs/PROJECT-CURRENT-STATE-R1.json")
    def go(self,e=None,yz=None,ledger=None,state=None):
        return m.check(self.e if e is None else e,self.yz if yz is None else yz,self.be,self.bf,self.bg,self.l if ledger is None else ledger,self.s if state is None else state)
    def test_positive(self): self.assertTrue(self.go())
    def test_false_same_day_index(self):
        e=copy.deepcopy(self.e);e["same_numbered_day_equivalence"]=True
        with self.assertRaises(AssertionError):self.go(e=e)
    def test_false_universal_header(self):
        e=copy.deepcopy(self.e);e["historical_printed_header_index_convention"]="PROVEN"
        with self.assertRaises(AssertionError):self.go(e=e)
    def test_fabricated_original_image(self):
        e=copy.deepcopy(self.e);e["scope_counters"]["new_original_pixels_acquired"]=1
        with self.assertRaises(AssertionError):self.go(e=e)
    def test_wrong_received_day(self):
        e=copy.deepcopy(self.e);e["observed_original_vs_received"][3]["received_digital_row_day"]=18
        with self.assertRaises(AssertionError):self.go(e=e)
    def test_wrong_received_digit(self):
        e=copy.deepcopy(self.e);e["observed_original_vs_received"][4]["received_digital_cumulative"]="8424.6409"
        with self.assertRaises(AssertionError):self.go(e=e)
    def test_wrong_original_delta(self):
        e=copy.deepcopy(self.e);e["original_four_local_edges"][2]["original_long"]="429.6074"
        with self.assertRaises(AssertionError):self.go(e=e)
    def test_received_text_tamper(self):
        yz=copy.deepcopy(self.yz);yz["modern_received_rows"][3]["cumulative"]="8000.3697"
        with self.assertRaises(AssertionError):self.go(yz=yz)
    def test_unproved_waseda_promotion(self):
        e=copy.deepcopy(self.e);e["Waseda_original_day18_day19_cumulative"]="PROVEN"
        with self.assertRaises(AssertionError):self.go(e=e)
    def test_false_ancestry_vote(self):
        e=copy.deepcopy(self.e);e["historical_lineage_independence"]="PROVEN"
        with self.assertRaises(AssertionError):self.go(e=e)
    def test_future_append_safe(self):
        s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
        s["schema_version"]="TEST_FUTURE"
        s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="TEST_FUTURE"
        s["historical_audit"]["current_focus"].append("13BI FUTURE_RESEARCH_NOT_13BH")
        l["binding"]["reviewed_state_version"]="TEST_FUTURE"
        l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"])
        l["binding"]["latest_research_focus_prefix"]="13BI"
        l["checkpoint_log"].append({"state_version":"TEST_FUTURE","reviewed_issue_ids":[x["id"] for x in l["issues"]]})
        self.assertTrue(self.go(ledger=l,state=s))
if __name__ == "__main__":unittest.main()
