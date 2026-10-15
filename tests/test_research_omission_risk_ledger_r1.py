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
  r=m.verify();self.assertEqual(r["open_issues"],9);self.assertEqual(r["coverage"],"NON_EXHAUSTIVE")
 def test_missing_issue(self):
  self.d["issues"].pop(0);self.invalid("baseline research issue")
 def test_bad_closed_status(self):
  self.d["issues"][0]["status"]="RESOLVED_WITH_EVIDENCE";self.invalid("closed issue without evidence")
 def test_biblio_source_removed(self):
  self.d["issues"][0]["source_refs"]=["docs/DOES-NOT-EXIST.md"]
  with self.assertRaisesRegex(ValueError,"missing primary reference"):
   m.validate(self.d,self.state,self.protocol,lambda x:(ROOT/x).is_file())
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
 def test_forward_only_ordinary_noop(self):
  self.assertEqual(m.check_forward_only(self.d,copy.deepcopy(self.d))["status"],"PASS")
if __name__=="__main__":unittest.main()
