import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-p0-original-handoff-13bi.py"
spec=importlib.util.spec_from_file_location("research13bi",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Handoff13BI(unittest.TestCase):
    def setUp(self):
        self.e=m.load(m.P);self.be=m.load(m.PBE);self.bg=m.load(m.PBG);self.bh=m.load(m.PBH)
        self.l=m.load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
        self.s=m.load("docs/PROJECT-CURRENT-STATE-R1.json")
    def go(self,e=None,ledger=None,state=None):
        return m.check(self.e if e is None else e,self.be,self.bg,self.bh,self.l if ledger is None else ledger,self.s if state is None else state)
    def test_positive(self):self.assertTrue(self.go())
    def test_stale_action_reintroduced(self):
        l=copy.deepcopy(self.l);next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")["next_action"]=self.e["prior_action_text"]
        with self.assertRaises(AssertionError):self.go(ledger=l)
    def test_source_sha_spoof(self):
        e=copy.deepcopy(self.e);e["source_positive_reconciliation"][1]["verified_sha"]="0"*64
        with self.assertRaises(AssertionError):self.go(e=e)
    def test_false_Waseda_date(self):
        e=copy.deepcopy(self.e);e["first_party_Waseda_catalog"]["imprint"]="[明代]"
        with self.assertRaises(AssertionError):self.go(e=e)
    def test_false_archetype(self):
        e=copy.deepcopy(self.e);e["D16_facts"]["historical_archetype"]="G893_WINNER"
        with self.assertRaises(AssertionError):self.go(e=e)
    def test_new_image_claim(self):
        e=copy.deepcopy(self.e);e["counters"]["new_original_images"]=1
        with self.assertRaises(AssertionError):self.go(e=e)
    def test_remove_revision(self):
        l=copy.deepcopy(self.l);i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
        i["history"]=[x for x in i["history"] if x.get("revision_id")!="TW-OPEN-0005-CURRENT-ACTION-13BI"]
        with self.assertRaises((AssertionError,StopIteration)):self.go(ledger=l)
    def test_missing_Waseda_action(self):
        e=copy.deepcopy(self.e);e["unresolved_scopes"].remove("WASEDA_P23_D18_D19_ORIGINAL_CUM_NATIVE_ROI")
        with self.assertRaises(AssertionError):self.go(e=e)
    def test_future_scoped_revisions(self):
        l=copy.deepcopy(self.l);s=copy.deepcopy(self.s)
        i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
        i["next_action"]="Future separately source-scoped verification"
        i["history"].append({"event":"ISSUE_REVISION","changed_fields":["next_action"],"reason":"FUTURE TEST","evidence_refs":[m.P]})
        s["schema_version"]="FUTURE";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="FUTURE"
        s["historical_audit"]["current_focus"].append("13BJ FUTURE")
        l["binding"]["reviewed_state_version"]="FUTURE"
        l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"])
        l["binding"]["latest_research_focus_prefix"]="13BJ"
        l["checkpoint_log"].append({"state_version":"FUTURE","reviewed_issue_ids":[x["id"] for x in l["issues"]]})
        self.assertTrue(self.go(ledger=l,state=s))
if __name__=="__main__":unittest.main()
