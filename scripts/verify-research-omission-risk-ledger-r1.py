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
  for name in ("id","title","origin","scope"):
   require(x[name]==y[name],"immutable issue identity changed: "+k)
  require(y["history"][:len(x["history"])]==x["history"],"prior issue history overwritten: "+k)
  require(set(x["source_refs"]).issubset(set(y["source_refs"])),"prior source reference removed: "+k)
  require(set(x.get("matrix_rule_ids",[])).issubset(set(y.get("matrix_rule_ids",[]))),"prior matrix coverage removed: "+k)
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
