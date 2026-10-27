import copy,importlib.util,unittest
from pathlib import Path
f=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-waseda-d17-d18-tight-13bo.py"
spec=importlib.util.spec_from_file_location("waseda13bo",f)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Source13BO(unittest.TestCase):
 def setUp(self):
  self.e=m.load(m.P);self.p=m.load(m.PREV);self.l=m.load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json");self.s=m.load("docs/PROJECT-CURRENT-STATE-R1.json")
 def go(self,e=None,l=None,s=None):return m.check(self.e if e is None else e,self.p,self.l if l is None else l,self.s if s is None else s)
 def test_positive(self):self.assertTrue(self.go())
 def test_false_day17_heading(self):
  e=copy.deepcopy(self.e);e["original_header_rois"][0]["literal"]="十六日"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_real_pixel_digest(self):
  e=copy.deepcopy(self.e);e["original_numeric_rois"][3]["pixel_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wide_mixed_lanes_not_allowed(self):
  e=copy.deepcopy(self.e);e["original_numeric_rois"][0]["bbox"]=[920,685,1015,1400]
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_decimal_relation(self):
  e=copy.deepcopy(self.e);e["same_copy_consecutive_arithmetic"][0]["exact_delta"]="424.3712"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_fake_global_law(self):
  e=copy.deepcopy(self.e);e["now_verified_source_local_chain"]["full_table_global_law_proven"]=True
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_fake_stemma(self):
  e=copy.deepcopy(self.e);e["cross_holding_scope"]["Waseda_NAJ_same_impression_proven"]=True
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_old_action_reintroduced(self):
  l=copy.deepcopy(self.l);next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")["next_action"]="13BN CURRENT ACTION stale"
  with self.assertRaises(AssertionError):self.go(l=l)
 def test_future_append_only(self):
  l=copy.deepcopy(self.l);s=copy.deepcopy(self.s);i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  i["next_action"]="13BP CURRENT ACTION source-bound next"
  i["history"].append({"event":"ISSUE_REVISION","changed_fields":["next_action"],"evidence_refs":[m.P]})
  s["schema_version"]="NEXT";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="NEXT"
  s["historical_audit"]["current_focus"].append("13BP future evidence")
  l["binding"]["reviewed_state_version"]="NEXT";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13BP"
  l["checkpoint_log"].append({"state_version":"NEXT","reviewed_issue_ids":[x["id"] for x in l["issues"]]})
  self.assertTrue(self.go(l=l,s=s))
if __name__=="__main__":unittest.main()
