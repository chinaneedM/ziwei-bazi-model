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
 def test_guard_reviewed_version_cannot_lag(self):
  self.state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.599.0"
  self.invalid("state guard synchronization")
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
 def test_nlc_bounded_review_must_not_claim_fulltext(self):
  record=next(x for x in self.d["issues"] if x["id"]=="TW-OPEN-0009")
  record["source_page_coverage"]["fulltext_linewise_collated_body_pages"]=1027
  self.invalid("fulltext completed replay mismatch")
 def test_nlc_bounded_review_does_not_prove_absence(self):
  record=next(x for x in self.d["issues"] if x["id"]=="TW-OPEN-0009")
  record["source_page_coverage"]["all_body_passage_absence_proven"]=True
  self.invalid("unproven whole-work absence")
 def test_nlc_bounded_review_has_one_physical_copy(self):
  record=next(x for x in self.d["issues"] if x["id"]=="TW-OPEN-0009")
  record["source_page_coverage"]["copy_identity_unified_not_multiple_independent_physical_witnesses"]=False
  self.invalid("source copy multiplication")
 def test_nlc_seam_does_not_prove_new_print_identity(self):
  record=next(x for x in self.d["issues"] if x["id"]=="TW-OPEN-0009")
  record["source_page_coverage"]["distinct_1827_thematic_juan20_binding_proven"]=True
  self.invalid("false old/new juan equivalence")
 def test_nlc_page_evidence_cannot_disappear(self):
  latest=copy.deepcopy(self.d)
  next(x for x in latest["issues"] if x["id"]=="TW-OPEN-0009").pop("source_page_coverage")
  with self.assertRaisesRegex(ValueError,"prior source-page coverage missing"):m.check_forward_only(self.d,latest)
 def test_no_bounded_snapshot_mutation_even_with_reason(self):
  latest=copy.deepcopy(self.d);i=next(x for x in latest["issues"] if x["id"]=="TW-OPEN-0009")
  i["source_page_coverage"]["fulltext_linewise_collated_body_pages"]=1027
  i["history"].append({"event":"ISSUE_REVISION","reason":"unsupported alleged reread","evidence_refs":["docs/PROJECT-CURRENT-STATE-R1.json"]})
  with self.assertRaisesRegex(ValueError,"historical source-page snapshot rewritten"):m.check_forward_only(self.d,latest)
 def test_later_revision_requires_append_only_history(self):
  latest=copy.deepcopy(self.d);i=next(x for x in latest["issues"] if x["id"]=="TW-OPEN-0009")
  i["source_page_coverage_revisions"]=[{"revision_id":"SIMULATED_TEST_ONLY"}]
  with self.assertRaisesRegex(ValueError,"new source-page revision without history"):m.check_forward_only(self.d,latest)
 def test_fake_revision_cannot_pass_current_live_validation(self):
  i=next(x for x in self.d["issues"] if x["id"]=="TW-OPEN-0009")
  i["source_page_coverage_revisions"]=[{"revision_id":"SIMULATED_TEST_ONLY","review_kind":"DIRECT_ORIGINAL_TARGET_FOLIO"}]
  self.invalid("source-page revision field missing")
 def test_bounded_old_snapshot_alone_not_sufficient_to_close(self):
  i=next(x for x in self.d["issues"] if x["id"]=="TW-OPEN-0009")
  i["status"]="RESOLVED_WITH_EVIDENCE"
  i["resolution_evidence"]=["docs/PROJECT-CURRENT-STATE-R1.json"]
  i["history"].append({"event":"RESOLVED_WITH_EVIDENCE","evidence_refs":["docs/PROJECT-CURRENT-STATE-R1.json"]})
  self.invalid("old bounded page snapshot cannot by itself resolve target")
 def test_append_only_revisions_cannot_disappear(self):
  before=copy.deepcopy(self.d);after=copy.deepcopy(self.d)
  ib=next(x for x in before["issues"] if x["id"]=="TW-OPEN-0009")
  ib["source_page_coverage_revisions"]=[{"revision_id":"SIMULATED_TEST_ONLY"}]
  with self.assertRaisesRegex(ValueError,"source-page revisions rewritten or removed"):m.check_forward_only(before,after)
 def test_grade_scope_is_immutably_interpreted(self):
  latest=copy.deepcopy(self.d);i=next(x for x in latest["issues"] if x["id"]=="TW-OPEN-0009")
  i["source_page_coverage_interpretation"]["positive_target_evidence_from_12xk"]=True
  with self.assertRaisesRegex(ValueError,"prior source-grade interpretation silently rewritten"):m.check_forward_only(self.d,latest)
 def test_g893_six_controls_are_not_solar_initial_pages(self):
  x=next(x for x in self.d["issues"] if x["id"]=="TW-OPEN-0005")
  x["g893_six_control_snapshot"]["six_original_target_controls"][0]["status"]="SOURCE_DECIDED"
  self.invalid("G893 six targets falsely adjudicated")
 def test_g893_six_target_missing(self):
  x=next(x for x in self.d["issues"] if x["id"]=="TW-OPEN-0005")
  x["g893_six_control_snapshot"]["six_original_target_controls"].pop()
  self.invalid("G893 one of six control IDs")
 def test_g893_archived_book_page_count_not_six_number_decisions(self):
  x=next(x for x in self.d["issues"] if x["id"]=="TW-OPEN-0005")
  x["g893_six_control_snapshot"]["independent_original_target_numeric_decisions"]=6
  self.invalid("G893 whole book access vs six target separation lost")
 def test_g893_legacy_access_blocker_must_be_open(self):
  x=next(x for x in self.d["issues"] if x["id"]=="TW-OPEN-0005")
  x["status"]="BLOCKED_SOURCE_ACCESS"
  self.invalid("G893 complete source mistakenly access-blocked")
 def test_g893_legacy_six_witnesses_cannot_be_implicitly_closed(self):
  x=next(x for x in self.d["issues"] if x["id"]=="TW-OPEN-0005")
  x["status"]="RESOLVED_WITH_EVIDENCE"
  self.invalid("G893 6 original number controls still uncollated")
 def test_g893_source_archive_hash_integrity(self):
  x=next(x for x in self.d["issues"] if x["id"]=="TW-OPEN-0005")
  x["g893_six_control_snapshot"]["source_doc_git_blob_sha"]="0"*40
  self.invalid("G893 existing source blob drift")
 def test_g893_append_only_history_preserves_source_snapshot(self):
  new=copy.deepcopy(self.d)
  x=next(x for x in new["issues"] if x["id"]=="TW-OPEN-0005")
  x["g893_six_control_snapshot"]["six_original_target_controls"][1]["original_page_id"]="synthetic-unverified"
  x["history"].append({"event":"ISSUE_REVISION","reason":"pretend data","evidence_refs":["docs/PROJECT-CURRENT-STATE-R1.json"]})
  with self.assertRaisesRegex(ValueError,"historical G893 six-control source snapshot overwritten"):m.check_forward_only(self.d,new)
 def test_forward_only_ordinary_noop(self):
  self.assertEqual(m.check_forward_only(self.d,copy.deepcopy(self.d))["status"],"PASS")
if __name__=="__main__":unittest.main()
