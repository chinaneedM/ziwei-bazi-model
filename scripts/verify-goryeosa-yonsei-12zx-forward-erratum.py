#!/usr/bin/env python3
"""12ZX: forward-only erratum for unresolved Yonsei paper book to work volume mapping."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12ZX-YONSEI-139V-BOOK30-UNBOUND-WORK52-ERRATUM-R1.json"
PRIOR="docs/research/TIANWEN-12ZW-YONSEI-CHOI-SEAL-BOOK30-MANUSCRIPT-PRINT-GRADE-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def read(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def ck(condition,message):
    if not condition: raise ValueError(message)
def verify():
    x=read(DOC);p=read(PRIOR);s=read(STATE);l=read(LEDGER)
    ck(x["schema"]=="TIANWEN-12ZX-YONSEI-FORWARD-ERRATUM-WORK52-UNKNOWN-R1" and x["historical_snapshot_preserved"] and x["prior"]==PRIOR,"forward-only identity")
    a,b=x["prior_field_overclaims"]
    ck(a["field"]=="physical.printed_work_volume_total" and a["old_value"]==p["physical"]["printed_work_volume_total"]==139,"old 139 assertion preserved")
    ck(a["new_field"]=="catalog_work_volume_total" and a["new_value"]==139 and a["original_woodblock_printed_work_volume_total"] is None,"139 not counted as original woodblock")
    ck(b["field"]=="explicit_book_level_composite.work52_same_book_30" and b["old_value"] is p["explicit_book_level_composite"]["work52_same_book_30"] is False and b["effective_new_value"] is None,"book30 prior false and effective unknown")
    o=x["effective_copy_reading"]
    ck(o["catalog_work_volume_count"]==139 and o["physical_book_count"]==33 and o["book30_includes_work_volumes"]==[122,123] and o["book30_work122_123_later_manuscript"] is True,"known catalog facts")
    for key in ("work52_physical_book_number","work52_in_physical_book30","work52_material_type","work52_d16_d18_original_folio_url","work52_d16_d18_original_image_sha256"):
        ck(o[key] is None,"do not guess: "+key)
    sc=x["scope"]
    ck(sc["disproved_claims_in_prior_fields_are_not_kept_as_current_fact"] and sc["new_original_work52_pages"]==sc["new_D16_D18_numeric_votes"]==sc["chart_reopen_count"]==0,"no fabricated new fact")
    ck(sc["source_registry_total"]==s["historical_audit"]["external_source_registry_total_unique_count"]==717,"no double-counted web source")
    ck(sc["omission_issues_open"]==len(l["issues"])==11 and sc["g893_original_direct"]=="5/6" and sc["g893_cross_original"]=="0/6","risks kept open")
    ck(s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"version sync")
    ck(s["historical_audit"]["current_focus"][-1].startswith("12ZX ") and l["binding"]["latest_research_focus_prefix"]=="12ZX" and l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"]),"focus sync")
    issue=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
    ck(issue["status"]=="OPEN" and DOC in issue["source_refs"] and DOC.replace(".json",".md") in issue["source_refs"],"unresolved issue preserving erratum")
    ck(l["checkpoint_log"][-1]["state_version"]==s["schema_version"] and set(l["checkpoint_log"][-1]["reviewed_issue_ids"])=={i["id"] for i in l["issues"]},"checkpoint")
    ck(s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0,"product invariant")
    return {"status":"PASS","corrected_field_overclaims":2,"original_glyph_votes":0}
if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False))
