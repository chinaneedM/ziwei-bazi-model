#!/usr/bin/env python3
"""13G: Keep Commons proxy bibliographic leads below original-folio evidentiary grade."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13G-NCL03130-GORYEOSA-AND-NCL03136-GUKJOBOGAM-COPY-SCOPE-R1.json"
SH="docs/research/TIANWEN-13G-NCL-COMMONS-TWO-COPY-ROUTES-SOURCE-SHARD-R1.json"
def rd(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def verify():
    e=rd(E); sh=rd(SH); m=rd("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
    s=rd("docs/PROJECT-CURRENT-STATE-R1.json"); l=rd("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
    assert e["schema"]=="TIANWEN-13G-NCL03130-NCL03136-COPY-PROSPECT-FIREWALL-R1"
    x=e["goryeosa_ncl03130"]; y=e["gukjobogam_ncl03136"]; a=e["adjudication"]
    assert (x["catalog_work_volume_count"],x["catalog_physical_book_count"],x["commons_pdf_segments"])==(137,40,24)
    assert not x["catalog_identity_direct_ncl_verified"] and x["volume52_segment_index"] is None and x["volume52_leaf"] is None
    assert x["volume52_d16_original_glyph"] is None and x["volume52_d18_original_glyph"] is None and x["image_sha256"] is None
    assert (y["catalog_work_volume_count"],y["catalog_physical_book_count"],y["commons_pdf_segments"])==(68,23,2)
    assert y["snu_catalog_physical_books"]==22 and not y["same_printing_proven"] and not y["catalog_identity_direct_ncl_verified"]
    assert y["work_volume9_leaf"] is None and y["work_volume9_1454_command_image_sha256"] is None
    assert a["ncl03130_24_pdfs_independent_physical_witnesses"]==1
    assert a["verified_direct_original_numeric_target_readings_added"]==a["independent_cross_witness_numeric_votes_added"]==a["algorithm_reopens"]==0
    assert a["catalog_vol52_presence_verified"] is False and a["printing_completed_in_1454_proven"] is False
    assert a["original_1782_work9_command_leaf_verified"] is False and a["open_research_issues"]==11
    assert len(sh["sources"])==2 and all(t["physical_glyph_authority"] is False and t["verification_status"]=="ACCESS_BOUNDARY_UNVERIFIED" and t["evidence"]==E for t in sh["sources"])
    assert any(t["path"]==SH and t["source_count"]==2 for t in m["shards"])
    assert m["combined_source_count"]==s["historical_audit"]["external_source_registry_total_unique_count"]>=730
    assert m["extension_source_count"]>=83 and s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
    assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
    assert any(z.startswith("13G ") for z in s["historical_audit"]["current_focus"])
    issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
    assert issue["status"]=="OPEN" and all(z in issue["source_refs"] for z in (E,"docs/research/TIANWEN-13G-NCL03130-GORYEOSA-AND-NCL03136-GUKJOBOGAM-COPY-SCOPE-R1.md",SH))
    assert len(l["issues"])==11 and all(z["status"]!="RESOLVED_WITH_EVIDENCE" for z in l["issues"])
    assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
    assert set(l["checkpoint_log"][-1]["reviewed_issue_ids"])=={z["id"] for z in l["issues"]}
    assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0
    return {"status":"PASS","source_count":m["combined_source_count"],"physical_glyph_votes_added":0}
if __name__=="__main__": print(json.dumps(verify(),ensure_ascii=False))
