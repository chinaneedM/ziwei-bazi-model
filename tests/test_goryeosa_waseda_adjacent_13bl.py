import copy,importlib.util,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("research13bl",Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-waseda-adjacent-13bl.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Original13BL(unittest.TestCase):
 def setUp(self):
  self.e=m.load(m.P);self.l=m.load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json");self.s=m.load("docs/PROJECT-CURRENT-STATE-R1.json")
 def go(self,e=None,l=None,s=None):
  return m.check(self.e if e is None else e,self.l if l is None else l,self.s if s is None else s)
 def test_positive(self):self.assertTrue(self.go())
 def test_fabricated_waseda_original_cumulative(self):
  e=copy.deepcopy(self.e);e["bounded_interpretation"]["original_day21_cumulative_value"]="9257.6000"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_falsely_collated_native_roi(self):
  e=copy.deepcopy(self.e);e["bounded_interpretation"]["day21_original_cumulative_numeric_direct_native_collation"]="PERFORMED"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_falsely_proved_global_table_law(self):
  e=copy.deepcopy(self.e);e["bounded_interpretation"]["global_day_index_and_table_start_end"]="PROVEN"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_inflated_physical_vote(self):
  e=copy.deepcopy(self.e);e["scope_counters"]["independent_numerical_votes"]=1
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_pdf_sha(self):
  e=copy.deepcopy(self.e);e["source"]["provider_pdf_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_original_jpeg_sha(self):
  e=copy.deepcopy(self.e);e["original_embedded_images"][0]["original_jpeg_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_xref_or_page(self):
  e=copy.deepcopy(self.e);e["original_embedded_images"][0]["embedded_xref"]=70
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_old_action_resurrection_rejected(self):
  l=copy.deepcopy(self.l);next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")["next_action"]="13BK CURRENT ACTION (STALE)"
  with self.assertRaises(AssertionError):self.go(l=l)
 def test_unregistered_same_focus_action_rejected(self):
  l=copy.deepcopy(self.l)
  next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")["next_action"]="13BL UNREGISTERED ACTION"
  with self.assertRaises(AssertionError):self.go(l=l)
 def test_issue_action_remains_stable_when_unrelated_new_research_focus_is_added(self):
  l=copy.deepcopy(self.l);s=copy.deepcopy(self.s)
  prior_action=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")["next_action"]
  active_family=prior_action.split(" ",1)[0]
  last_action_revision=[h for h in next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")["history"] if "next_action" in h.get("changed_fields",[])][-1]
  self.assertTrue(prior_action.startswith(active_family+" CURRENT ACTION"))
  self.assertTrue(last_action_revision.get("revision_id","").startswith("TW-OPEN-0005-"+active_family+"-"))
  s["schema_version"]="NEXT_UNRELATED";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="NEXT_UNRELATED"
  s["historical_audit"]["current_focus"].append("13DN UNRELATED PHYSICAL COPY ACCESS")
  l["binding"].update(reviewed_state_version="NEXT_UNRELATED",
    source_focus_count=len(s["historical_audit"]["current_focus"]),
    latest_research_focus_prefix="13DN")
  l["checkpoint_log"].append({"state_version":"NEXT_UNRELATED","reviewed_issue_ids":[x["id"] for x in l["issues"]]})
  self.assertTrue(self.go(l=l,s=s))
 def test_future_append_only_valid(self):
  l=copy.deepcopy(self.l);s=copy.deepcopy(self.s)
  issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  issue["next_action"]="13BM CURRENT ACTION source-specific future verified work"
  issue["history"].append({"event":"ISSUE_REVISION","changed_fields":["next_action"],"evidence_refs":[m.P]})
  s["schema_version"]="NEXT";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="NEXT"
  s["historical_audit"]["current_focus"].append("13BM future scoped work")
  l["binding"]["reviewed_state_version"]="NEXT";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13BM"
  l["checkpoint_log"].append({"state_version":"NEXT","reviewed_issue_ids":[x["id"] for x in l["issues"]]})
  self.assertTrue(self.go(l=l,s=s))
if __name__=="__main__":unittest.main()
