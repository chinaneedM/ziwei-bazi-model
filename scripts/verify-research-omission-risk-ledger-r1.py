#!/usr/bin/env python3
"""Evidence-scoped, forward-only research omission ledger verifier."""
import argparse
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LEDGER=Path("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
STATE=Path("docs/PROJECT-CURRENT-STATE-R1.json")
PROTOCOL=Path("docs/PROJECT-CONTINUITY-PROTOCOL-R1.md")
MATRIX=Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
MANIFEST=Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
ALLOWED={"OPEN","BLOCKED_SOURCE_ACCESS","RESOLVED_WITH_EVIDENCE"}
REQUIRED_AXES={
 "primary_editions_and_physical_copies","region_and_location","school_specific_methods",
 "philology_and_word_sense","historical_time_and_calendar_coordinate",
 "mathematical_replay","contrary_and_negative_evidence","transmission_lineage_and_non_edges"
}
BASELINE_IDS={f"TW-OPEN-{i:04d}" for i in range(1,10)}
def require(p,msg):
 if not p:raise ValueError(msg)
def read(path):
 return json.loads((ROOT/path).read_text(encoding="utf-8"))
def record_statuses(data):
 return {x["id"]:x for x in data["issues"]}
def validate(data,state,protocol,exists_fn=None):
 require(data["schema"]=="TIANWEN-RESEARCH-OMISSION-RISK-LEDGER-R1","schema")
 for issue in data["issues"]:
  if "source_page_coverage" not in issue:
   continue
  ev=issue["source_page_coverage"]
  p=Path(ev["source_doc"])
  require(p.as_posix().startswith("docs/research/") and ".." not in p.parts,"evidence replay path must be stable")
  original=(ROOT/p).read_bytes()
  import hashlib
  blob_hash=hashlib.sha1(b"blob "+str(len(original)).encode("ascii")+b"\0"+original).hexdigest()
  require(blob_hash==ev["source_blob_sha"],"research image-grade source blob mismatch")
  src=json.loads(original)
  g=src["grade_union"];r=src["review"]
  require(ev["total_source_pdf_pages"]==g["whole_holding_source_pdf_pages"],"page-count replay mismatch")
  require(ev["body_source_pages"]==g["whole_body_pages"],"body page replay mismatch")
  require(ev["bounded_native_body_jpeg_pages"]==g["global_native_body_source_pages_after"],"native grade replay mismatch")
  require(ev["linewise_fulltext_pending_body_pages"]==g["whole_body_fulltext_collation_pending"],"full-text pending replay mismatch")
  require(ev["fulltext_linewise_collated_body_pages"]==g["whole_body_pages"]-g["whole_body_fulltext_collation_pending"],"fulltext completed replay mismatch")
  require(ev["non_target_preliminary_pages"]==g["non_target_first_fascicle_preliminary_pages"],"preliminary non-body page replay mismatch")
  require(ev["nonbody_colophon_pages"]==g["f10_colophon_native_nonbody_pages"],"colophon non-body page replay mismatch")
  require(ev["any_page_target_absence_proven"]==r["any_page_target_absence_proven"]==False,"unproven page-level text absence")
  require(ev["all_body_passage_absence_proven"]==r["whole_old20_work_target_absence_proven"]==False,"unproven whole-work absence")
  require(ev["original_old20_target_folio_attested"]==r["any_original_old20_gaizao_louke_target_folio_positive_attestation"]==False,"unproven original target folio")
  require(ev["source_pdf_rehashed_in_this_batch"]==src["source"]["source_pdf_rehashed_this_batch"]==False,"false source PDF binary rehash")
  require(ev["copy_identity_unified_not_multiple_independent_physical_witnesses"]==True and ev["physical_holding"]==src["source"]["physical_holding"],"source copy multiplication")
  require(ev["distinct_1827_thematic_juan20_binding_proven"]==False and r["old20_juan_equivalent_to_1827_reorganized_thematic_juan"]==False,"false old/new juan equivalence")
  seam=Path(ev["direct_juan_seam_doc"])
  seam_bytes=(ROOT/seam).read_bytes()
  require(hashlib.sha1(b"blob "+str(len(seam_bytes)).encode("ascii")+b"\0"+seam_bytes).hexdigest()==ev["direct_juan_seam_blob_sha"],"chronological seam source drift")
  sm=json.loads(seam_bytes)
  require({(x["from_juan"],x["to_juan"],x["shared_pdf_page"]) for x in sm["seams"]}>={(18,19,81),(19,20,137)},"old20 mixed-leaf seam evidence missing")
  revisions=issue.get("source_page_coverage_revisions",[])
  require(isinstance(revisions,list),"source-page revisions must be a list")
  require(len({x.get("revision_id") for x in revisions})==len(revisions),"duplicate page-review revision id")
  for rev in revisions:
   require(rev.get("review_kind") in ("DIRECT_ORIGINAL_TARGET_FOLIO","FULL_SOURCE_HIGH_RES_LINEWISE_NEGATIVE"),"source-page revision kind unsupported")
   for key in ("revision_id","source_doc","source_blob_sha","physical_holding","original_folio_ref","original_image_sha256","reviewed_by","review_date","review_kind"):
    require(isinstance(rev.get(key),str) and bool(rev[key]),"source-page revision field missing: "+key)
   import re
   require(bool(re.fullmatch(r"[0-9a-f]{40}",rev["source_blob_sha"])),"revision Git blob SHA format")
   require(bool(re.fullmatch(r"[0-9a-f]{64}",rev["original_image_sha256"])),"revision image SHA256 format")
   new_path=Path(rev["source_doc"])
   require(new_path.parts[:2]==("docs","research") and ".." not in new_path.parts,"revision evidence doc path")
   newbytes=(ROOT/new_path).read_bytes()
   require(hashlib.sha1(b"blob "+str(len(newbytes)).encode("ascii")+b"\0"+newbytes).hexdigest()==rev["source_blob_sha"],"revision source blob integrity")
   doc=json.loads(newbytes)
   match=doc.get("source_page_review_revision",{})
   for key in ("revision_id","physical_holding","original_folio_ref","original_image_sha256","reviewed_by","review_date","review_kind"):
    require(match.get(key)==rev[key],"revision original page source binding mismatch: "+key)
   require(match.get("original_image_source_url") and match.get("human_direct_glyph_or_linewise_review") is True,"revision original image and human review required")
   if rev["review_kind"]=="FULL_SOURCE_HIGH_RES_LINEWISE_NEGATIVE":
    require(match.get("whole_body_pages_linewise_reviewed")==ev["body_source_pages"],"full manuscript negative lacks source-scoped complete linewise pages")
    require(match.get("complete_original_page_image_manifest_sha256") and not match.get("source_coverage_gaps"),"negative source completeness unproved")
   else:
    require(match.get("target_passage")=="改造漏刻" and match.get("target_passage_original_glyph_directly_visible") is True,"positive target original glyph not proven")
  if issue["status"]=="RESOLVED_WITH_EVIDENCE":
   require(bool(revisions),"old bounded page snapshot cannot by itself resolve target")
   require(bool(issue.get("resolution_evidence")),"resolution evidence must be explicit")


 require(data["definition"].startswith("NON_EXHAUSTIVE"),"not falsely exhaustive")
 require(len(data["explicit_limits"])>=3 and any("not be recovered" in x for x in data["explicit_limits"]),"unsaved research limitation")
 require(data["binding"]["reviewed_state_version"]==state["schema_version"],"state review missing")
 require(data["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"]),"research focus changed without ledger review")
 require(data["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ")[0],"latest research family review missing")
 require(data["binding"]["branch"]==state["development_branch"] and data["binding"]["repository"]==state["repository"],"repository scope")
 require(set(data["coverage_axes"])==REQUIRED_AXES and len(data["coverage_axes"])==len(REQUIRED_AXES),"coverage axes not exhaustive as method")
 require(data["resolution_policy"]["allowed_statuses"]==["OPEN","BLOCKED_SOURCE_ACCESS","RESOLVED_WITH_EVIDENCE"],"allowed statuses")
 ids=[x.get("id") for x in data["issues"]]
 require(len(ids)==len(set(ids)),"duplicate issue IDs")
 require(BASELINE_IDS.issubset(set(ids)),"baseline research issue silently removed")
 require(len(data["issues"])>=len(BASELINE_IDS),"missing baseline issues")
 matrix=read(MATRIX)
 matrix_ids={x["rule_id"] for x in matrix["rows"]}
 missing_ids={x["rule_id"] for x in matrix["rows"] if x["audit_status"]=="MISSING_FROM_PRODUCT"}
 tracked_ids={rid for x in data["issues"] for rid in x.get("matrix_rule_ids",[])}
 require(tracked_ids.issubset(matrix_ids),"unrecognized Matrix rule coverage reference")
 require(missing_ids.issubset(tracked_ids),"missing product candidate coverage: "+", ".join(sorted(missing_ids-tracked_ids)))
 for x in data["issues"]:
  for key in ("id","title","priority","scope","origin","source_refs","evidence_boundary","missing_evidence","next_action","closure_criteria","history","resolution_evidence"):
   require(x.get(key),"missing issue field: "+x["id"]+" "+key) if key not in ("resolution_evidence",) else require(isinstance(x.get(key),list),"resolution evidence list")
  require(x["status"] in ALLOWED,"issue status "+x["id"])
  require(x["priority"] in ("P0","P1","P2"),"priority "+x["id"])
  if "matrix_rule_ids" in x:
   require(isinstance(x["matrix_rule_ids"],list) and len(x["matrix_rule_ids"])==len(set(x["matrix_rule_ids"])),"duplicate matrix rule IDs "+x["id"])
  require(x["history"][0]["event"]=="REGISTERED_UNRESOLVED","registration lost")
  if x["status"]=="RESOLVED_WITH_EVIDENCE":
   require(x["resolution_evidence"],"closed issue without evidence "+x["id"])
   require(x["history"][-1]["event"]=="RESOLVED_WITH_EVIDENCE" and x["history"][-1].get("evidence_refs"),"resolution event missing "+x["id"])
  else:
   require(not x["resolution_evidence"],"open issue cannot have asserted resolution "+x["id"])
  for s in x["source_refs"]:
   require(isinstance(s,str) and s.startswith("docs/") and ".." not in Path(s).parts,"path escape/unstable evidence ref "+x["id"])
   if exists_fn is not None:
    require(exists_fn(s),"missing primary reference "+x["id"]+": "+s)
 checks=data["checkpoint_log"]
 require(len(checks)>0,"checkpoint log empty")
 require(checks[-1]["state_version"]==state["schema_version"],"checkpoint not latest state")
 require(set(checks[-1]["reviewed_issue_ids"])==set(ids),"unreviewed open items")
 require("Research omission and interruption recovery gate" in protocol and str(LEDGER) in protocol,"protocol missing recovery requirement")
 guard=state["historical_audit"]["research_omission_guard"]
 require(guard["ledger"]==str(LEDGER) and guard["verifier"]=="scripts/verify-research-omission-risk-ledger-r1.py","state guard paths")
 require(guard["version"]==data["version"] and guard["reviewed_state_version"]==state["schema_version"],"state guard synchronization")
 open_count=sum(x["status"]!="RESOLVED_WITH_EVIDENCE" for x in data["issues"])
 require(guard["open_issues"]==open_count and guard["coverage_status"]=="INCREMENTAL_NOT_EXHAUSTIVE","state open count cannot masquerade as exhaustiveness")
 h=state["historical_audit"];i=state["invariants"]
 require(h["row_count"]==h["audited_row_count"]==len(matrix["rows"]) and h["repaired_provenance_metadata_defect_count"]==matrix["audit_summary"]["repaired_provenance_metadata_defect_count"],"historical matrix snapshot")
 manifest=read(MANIFEST)
 require(h["external_source_registry_root_count"]==manifest["root_source_count"] and h["external_source_registry_extension_count"]==manifest["extension_source_count"] and h["external_source_registry_total_unique_count"]==manifest["combined_source_count"],"source registry snapshot")
 require(i["deterministic_fusion_chart_product_r1"]=="CLOSED" and i["algorithm_reopen_count"]==0,"product and algorithm freeze")
 return {"result":"PASS","tracked_issues":len(ids),"open_issues":open_count,"coverage":"NON_EXHAUSTIVE","state_version":state["schema_version"]}
def check_forward_only(old,new):
 before=record_statuses(old);after=record_statuses(new)
 require(set(before).issubset(set(after)),"old issue removed instead of retaining history")
 require(old["coverage_axes"]==new["coverage_axes"],"coverage axes changed without versioned protocol")
 require(new["checkpoint_log"][:len(old["checkpoint_log"])]==old["checkpoint_log"],"prior checkpoint overwritten")
 for k,x in before.items():
  y=after[k]
  for name in ("id","origin","scope"):
   require(x[name]==y[name],"immutable issue identity changed: "+k)
  require(y["history"][:len(x["history"])]==x["history"],"prior issue history overwritten: "+k)
  if x["title"]!=y["title"]:
   require(len(y["history"])>len(x["history"]),"issue title silently changed: "+k)
   last=y["history"][-1]
   require(last.get("event")=="TITLE_CORRECTION" and last.get("previous_title")==x["title"] and last.get("new_title")==y["title"] and "title" in last.get("changed_fields",[]) and last.get("reason") and last.get("evidence_refs"),"title correction lacks original/evidence record: "+k)
  require(set(x["source_refs"]).issubset(set(y["source_refs"])),"prior source reference removed: "+k)
  require(set(x.get("matrix_rule_ids",[])).issubset(set(y.get("matrix_rule_ids",[]))),"prior matrix coverage removed: "+k)
  if x.get("source_page_coverage"):
   require(y.get("source_page_coverage"),"prior source-page coverage missing: "+k)
   require(x["source_page_coverage"]==y["source_page_coverage"],"historical source-page snapshot rewritten: "+k)
  prior_revisions=x.get("source_page_coverage_revisions",[])
  later_revisions=y.get("source_page_coverage_revisions",[])
  require(isinstance(prior_revisions,list) and isinstance(later_revisions,list),"page revisions not append-only list: "+k)
  require(later_revisions[:len(prior_revisions)]==prior_revisions,"source-page revisions rewritten or removed: "+k)
  if len(later_revisions)>len(prior_revisions):
   require(len(y["history"])>len(x["history"]),"new source-page revision without history: "+k)
   last=y["history"][-1]
   require(last.get("event")=="SOURCE_PAGE_REVIEW_REVISION" and last.get("evidence_refs") and last.get("reason"),"new source-page revision needs evidence-scoped history: "+k)
  if x.get("source_page_coverage_interpretation"):
   require(y.get("source_page_coverage_interpretation")==x["source_page_coverage_interpretation"],"prior source-grade interpretation silently rewritten: "+k)
  material=("priority","evidence_boundary","missing_evidence","next_action","closure_criteria")
  changed={name for name in material if x[name]!=y[name]}
  if changed:
   require(len(y["history"])>len(x["history"]),"scope silently changed: "+k)
   last=y["history"][-1]
   require(changed.issubset(set(last.get("changed_fields",[]))) and last.get("reason") and last.get("evidence_refs"),"scope revision missing explicit field/evidence audit: "+k)
  if y["status"]!=x["status"]:
   require(len(y["history"])>len(x["history"]),"status silently changed: "+k)
   last=y["history"][-1]
   require(last.get("from")==x["status"] and last.get("to")==y["status"],"status transition missing scope: "+k)
   require(last.get("evidence_refs") or last.get("reason"),"transition missing evidence: "+k)
   if y["status"]=="RESOLVED_WITH_EVIDENCE":
    require(last["event"]=="RESOLVED_WITH_EVIDENCE","closure without resolution event: "+k)
  if x["status"]=="RESOLVED_WITH_EVIDENCE":
   require(y["resolution_evidence"][:len(x["resolution_evidence"])]==x["resolution_evidence"],"historical resolution evidence removed: "+k)
 return {"status":"PASS","old_issues_preserved":len(before)}
def parent_revision():
 p=subprocess.run(["git","show",f"HEAD^:{LEDGER.as_posix()}"],cwd=ROOT,capture_output=True,text=True)
 if p.returncode:
  # Initial installation only: ensure it was actually added this commit.
  check=subprocess.run(["git","diff-tree","--no-commit-id","--name-status","-r","HEAD","--",LEDGER.as_posix()],cwd=ROOT,capture_output=True,text=True)
  require(check.returncode==0 and any(s.startswith("A") for s in check.stdout.splitlines()),"cannot compare parent ledger; fetch at least 2 commits")
  return None
 return json.loads(p.stdout)
def verify(check_parent=False):
 data=read(LEDGER)
 result=validate(data,read(STATE),(ROOT/PROTOCOL).read_text(encoding="utf-8"),lambda x:(ROOT/x).is_file())
 if check_parent:
  previous=parent_revision()
  result["parent_check"]=check_forward_only(previous,data) if previous is not None else {"status":"INITIAL_LEDGER_COMMIT"}
 return result
if __name__=="__main__":
 a=argparse.ArgumentParser()
 a.add_argument("--check-parent",action="store_true")
 args=a.parse_args()
 print(json.dumps(verify(args.check_parent),ensure_ascii=False))
