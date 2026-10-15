import copy, importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("risk",ROOT/"scripts/verify-research-omission-risk-ledger-r1.py")
m=importlib.util.module_from_spec(sp)
sp.loader.exec_module(m)
class ResearchOmissionLedgerTests(unittest.TestCase):
 def setUp(self):
  self.d=m.read(m.LEDGER);self.state=m.read(m.STATE);self.protocol=(ROOT/m.PROTOCOL).read_text(encoding="utf-8")
 def invalid(self,match):
  with self.assertRaisesRegex(ValueError,match):m.validate(self.d,self.state,self.protocol)
 def test_live(self):
  r=m.verify();self.assertEqual(r["open_issues"],11);self.assertEqual(r["coverage"],"NON_EXHAUSTIVE")
 def test_missing_issue(self):
  self.d["issues"].pop(0);self.invalid("baseline research issue")
 def test_bad_closed_status(self):
  self.d["issues"][0]["status"]="RESOLVED_WITH_EVIDENCE";self.invalid("closed issue without evidence")
 def test_biblio_source_removed(self):
  self.d["issues"][0]["source_refs"]=["docs/DOES-NOT-EXIST.md"]
  with self.assertRaisesRegex(ValueError,"missing primary reference"):
   m.validate(self.d,self.state,self.protocol,lambda x:(ROOT/x).is_file())
 def test_latest_family_cannot_be_stale(self):
  self.d["binding"]["latest_research_focus_prefix"]="12XG";self.invalid("latest research family review missing")
 def test_stale_state_version(self):
  self.d["binding"]["reviewed_state_version"]="1.594.0";self.invalid("state review missing")
 def test_open_count_laundered(self):
  self.state["historical_audit"]["research_omission_guard"]["open_issues"]=0;self.invalid("state open count")
 def test_coverage_lane_dropped(self):
  self.d["coverage_axes"].pop();self.invalid("coverage axes")
 def test_not_exhaustive(self):
  self.d["definition"]="ALL_WITNESSES_EXHAUSTIVELY_CHECKED";self.invalid("not falsely exhaustive")
 def test_missing_recent_checkpoint(self):
  self.d["checkpoint_log"][-1]["reviewed_issue_ids"]=["TW-OPEN-0001"];self.invalid("unreviewed open items")
 def test_parent_comparison_catches_deletion(self):
  latest=copy.deepcopy(self.d);latest["issues"].pop()
  with self.assertRaisesRegex(ValueError,"old issue removed"):
   m.check_forward_only(self.d,latest)
 def test_parent_comparison_catches_history_rewrite(self):
  latest=copy.deepcopy(self.d);latest["issues"][0]["history"][0]["event"]="SILENTLY_DONE"
  with self.assertRaisesRegex(ValueError,"prior issue history overwritten"):
   m.check_forward_only(self.d,latest)
 def test_parent_comparison_catches_unproved_close(self):
  latest=copy.deepcopy(self.d);latest["issues"][0]["status"]="RESOLVED_WITH_EVIDENCE"
  with self.assertRaisesRegex(ValueError,"status silently changed"):
   m.check_forward_only(self.d,latest)
 def test_matrix_coverage_catches_loss(self):
  self.d["issues"]= [x for x in self.d["issues"] if x["id"]!="TW-OPEN-0011"]
  self.d["checkpoint_log"][-1]["reviewed_issue_ids"]=[x["id"] for x in self.d["issues"]]
  self.invalid("missing product candidate coverage")
 def test_matrix_coverage_bridge_catches_loss(self):
  x=next(x for x in self.d["issues"] if x["id"]=="TW-OPEN-0010")
  x["matrix_rule_ids"]=[]
  self.invalid("missing product candidate coverage")
 def test_manifest_growth_is_not_hardcoded(self):
  self.state["historical_audit"]["external_source_registry_total_unique_count"]=705
  self.invalid("source registry snapshot")
 def test_forward_only_catches_source_deletion(self):
  new=copy.deepcopy(self.d);new["issues"][0]["source_refs"].pop()
  with self.assertRaisesRegex(ValueError,"prior source reference removed"):m.check_forward_only(self.d,new)
 def test_forward_only_catches_matrix_rule_deletion(self):
  new=copy.deepcopy(self.d);next(x for x in new["issues"] if x["id"]=="TW-OPEN-0006")["matrix_rule_ids"]=[]
  with self.assertRaisesRegex(ValueError,"prior matrix coverage removed"):m.check_forward_only(self.d,new)
 def test_forward_only_catches_priority_downgrade(self):
  new=copy.deepcopy(self.d);new["issues"][0]["priority"]="P2"
  with self.assertRaisesRegex(ValueError,"scope silently changed"):m.check_forward_only(self.d,new)
 def test_forward_only_catches_stealth_missing_evidence_rewrite(self):
  new=copy.deepcopy(self.d);new["issues"][0]["missing_evidence"]="nothing remains"
  with self.assertRaisesRegex(ValueError,"scope silently changed"):m.check_forward_only(self.d,new)
 def test_forward_only_allows_explicit_scoped_revision(self):
  new=copy.deepcopy(self.d)
  x=new["issues"][0];x["next_action"]="New independently sourced action"
  x["history"].append({"event":"ISSUE_REVISION","date":"2026-10-15","changed_fields":["next_action"],"reason":"new evidence","evidence_refs":["docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"]})
  self.assertEqual(m.check_forward_only(self.d,new)["status"],"PASS")
 def test_forward_only_catches_silent_title_change(self):
  updated=copy.deepcopy(self.d);updated["issues"][0]["title"]="injected title"
  with self.assertRaisesRegex(ValueError,"issue title silently changed"):m.check_forward_only(self.d,updated)
 def test_forward_only_allows_evidence_backed_title_correction(self):
  updated=copy.deepcopy(self.d);x=updated["issues"][0];old=x["title"];x["title"]="corrected authenticated title"
  x["history"].append({"event":"TITLE_CORRECTION","date":"2026-10-15","previous_title":old,"new_title":x["title"],"changed_fields":["title"],"reason":"corrected evidence","evidence_refs":["docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"]})
  self.assertEqual(m.check_forward_only(self.d,updated)["status"],"PASS")
 def test_forward_only_ordinary_noop(self):
  self.assertEqual(m.check_forward_only(self.d,copy.deepcopy(self.d))["status"],"PASS")
if __name__=="__main__":unittest.main()
