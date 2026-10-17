#!/usr/bin/env python3
"""12YV bibliographical juan/mu collision: received citations are not originals."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
D="docs/research/TIANWEN-12YV-MEI-DATONG-LIZHI-EIGHT-JUAN-SEVENTEEN-MU-BIBLIOGRAPHIC-CONFLICT-R1.json"
def load():
 return [json.loads((R/p).read_text(encoding="utf-8")) for p in (D,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json")]
def check(d,l,s):
 def req(cond,msg):
  if not cond: raise ValueError(msg)
 req(d["schema"]=="TIANWEN-12YV-MEI-DATONG-LIZHI-BIBLIOGRAPHIC-JUAN-MU-CONFLICT-R1","schema")
 req(d["grade"].startswith("RECEIVED_BIBLIOGRAPHIC_TEXT"),"not native original")
 src=d["controls"]
 req(len(src)==5 and len(set(z["source"] for z in src))==5,"five scoped witnesses")
 req(all(z["url"].startswith("https://") and z["independence"] for z in src),"untraceable scope")
 req(d["philology"]["three_parts_mu_counts"]==[7,4,6] and d["philology"]["mu_total"]==17,"mu arithmetic")
 req(d["philology"]["mu_total_is_not_automatically_historical_juan_count"] is True,"juan/mu collapsed")
 c=d["comparison_result"]
 req(c["same_original_physical_catalog_folio_disagreement"]=="UNADJUDICATED" and c["seventeen_juan_historical_edition_or_repagination"]=="UNPROVEN","unwarranted edition winner")
 req(c["treat_siku_catalogue_double_rendering_as_two_independent_qing_originals"] is False,"double-counted library transcripts")
 e=d["evidence_impact"]
 req(all(e[k]==0 for k in ("new_numeric_original_page_loci","new_distinct_historical_physical_witnesses","new_genealogy_nodes","new_genealogy_edges","new_source_registry_entries","algorithm_reopens")),"false physical/genealogy vote")
 req(e["g893_original_principal"]=="5/6" and e["g893_cross_witness_final"]=="0/6" and e["open_research_issues"]==11 and e["product"]=="CLOSED" and e["closure_for_juan_conflict"].startswith("OPEN"),"mechanics falsely closed")
 x=next(q for q in l["issues"] if q["id"]=="TW-OPEN-0005")
 req(x["status"]=="OPEN" and D in x["source_refs"] and D.replace(".json",".md") in x["source_refs"],"issue provenance")
 req(x["mei_12yv_bibliographic_juan_mu_conflict_reviews"][0]["original_catalog_leaf_verified"] is False,"fabricated original")
 req(l["binding"]["reviewed_state_version"]==s["schema_version"] and l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"]),"state drift")
 req(l["checkpoint_log"][-1]["state_version"]==s["schema_version"] and len(l["checkpoint_log"][-1]["reviewed_issue_ids"])==len(l["issues"]),"omission gate")
 req(s["historical_audit"]["current_focus"][-1].startswith("12YV ") and s["invariants"]["algorithm_reopen_count"]==0,"handoff and frozen algorithm")
 return {"result":"PASS","grade":"RECEIVED_AND_SECONDARY_ONLY","original_catalog_leaf_verified":False,"source_count":5,"unresolved":11}
if __name__=="__main__":print(json.dumps(check(*load()),ensure_ascii=False))
