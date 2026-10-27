#!/usr/bin/env python3
"""12ZV Yonsei 33-book indexed heritage copy without illicit original-glyph elevation."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12ZV-GORYEOSA-YONSEI-33BOOK-LATER-IMPRESSION-BOUNDARY-R1.json"
PRIOR="docs/research/TIANWEN-12ZU-GORYEOSA-HERITAGE-GK-ID-AND-SHARED-MICROFILM-R1.json"
SOURCE="docs/research/TIANWEN-12ZV-GORYEOSA-YONSEI-HERITAGE-SOURCE-SHARD-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
MANIFEST="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
def load(p):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))
def require(cond,msg):
    if not cond: raise ValueError(msg)
def verify():
    d,p,s,l,m,src=map(load,(DOC,PRIOR,STATE,LEDGER,MANIFEST,SOURCE))
    require(d["schema"]=="TIANWEN-12ZV-GORYEOSA-YONSEI-33BOOK-LATER-IMPRESSION-CANDIDATE-R1" and d["prior"]==PRIOR,"schema/prior")
    x=d["new_physical_copy_candidate"]
    require(x["physical_books"]==33 and x["work_volumes"]==139 and x["woodblock_cut_year"]==1613,"catalog counts")
    require(x["impression_classification"]=="LATER_IMPRESSION_CENTURY_17_TO_18" and x["heritage_record"]=="고려사(2021-5)","later-print identity")
    for field in ("specific_library_call_number","work52_physical_book_number","work52_original_folio_reference","work52_original_image_url","work52_original_image_sha256","d16_original_glyph","d18_original_glyph"):
        require(x[field] is None,"unproven copy-level glyph: "+field)
    require(d["source_review"]["original_page_open_result"]=="403_OR_TOOL_ACCESS_FAILURE" and not d["source_review"]["original_source_folio_seen"],"access grade")
    require([z["physical_books"] for z in p["items"]]==[85,85],"preserve 12ZU")
    require([z["books"] for z in d["existing_physical_copy_controls"]]==[85,85,75],"physical comparison")
    require(all(d["scope_firewall"].values()),"anti conflation")
    u=d["unresolved"]
    require(u["new_original_folios"]==u["new_cross_physical_d16_d18_votes"]==u["algorithm_reopens"]==0,"no false ancient source")
    require(u["g893_principal_original_controls"]=="5/6" and u["g893_cross_original_controls"]=="0/6" and u["omission_open_issues"]==11,"P0 still open")
    require(len(src["sources"])==1 and src["sources"][0]["verification_status"]=="ACCESS_BOUNDARY_UNVERIFIED" and src["sources"][0]["physical_glyph_authority"] is False,"source grade")
    require(s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"state sync")
    require(s["historical_audit"]["external_source_registry_total_unique_count"]>=717 and m["combined_source_count"]==s["historical_audit"]["external_source_registry_total_unique_count"],"source count")
    require(any(e["path"]==SOURCE and e["source_count"]==1 for e in m["shards"]),"source shard")
    require(any(x.startswith("12ZV ") for x in s["historical_audit"]["current_focus"]) and l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0],"focus forward")
    require(l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"]),"focus count")
    issue=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
    require(issue["status"]=="OPEN" and all(z in issue["source_refs"] for z in (DOC,DOC.replace(".json",".md"),SOURCE)),"P0 preservation")
    require(all(i["status"]!="RESOLVED_WITH_EVIDENCE" for i in l["issues"]) and len(l["issues"])==11,"no issue removed")
    require(l["checkpoint_log"][-1]["state_version"]==s["schema_version"] and set(l["checkpoint_log"][-1]["reviewed_issue_ids"])=={i["id"] for i in l["issues"]},"checkpoint")
    require(s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0,"R1 invariant")
    return {"status":"PASS","yonsei_new_physical_catalog_leads":1,"ancient_target_original_pages":0}
if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False))
