#!/usr/bin/env python3
"""Prevent archival metadata and scan identifiers being promoted to historical glyph votes."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13J-NLC99-WASEDA1848-WUL47-COPY-FIREWALL-R1.json"
SH="docs/research/TIANWEN-13J-NLC99-WASEDA1848-WUL47-SOURCE-SHARD-R1.json"
def read(p):
    return json.loads((R/p).read_text(encoding="utf-8"))
def validate(e):
    w,n,m,a=e["waseda"],e["nlc"],e["wul_mirror"],e["adjudication"]
    assert e["schema"]=="TIANWEN-13J-NLC99-WASEDA1848-WUL47-COPY-FIREWALL-R1"
    assert w["shelfmark"]=="リ06 03059" and w["physical_books"]==28 and w["postscript_year"]==1848
    assert w["impression_year"] is None and w["copy_date"] is None
    assert w["identical_to_1782"] is False and w["original_work9_leaf_read"] is False
    assert n["digital_id"]=="411999022809" and n["digital_file_count"]==99
    assert n["surviving_work_volumes"]==["1-117","120-125","127-137"]
    assert n["firstparty_item_verified"] is False
    assert all(n[k] is None for k in ("physical_books_verified","vol52_digital_group","vol52_folio","d16_glyph","d18_glyph","image_sha256"))
    assert m["same_prior_physical_shelfmark"]=="リ06 02809" and m["group_number"]==47
    assert m["commons_work_year"]==1451 and m["official_imprint_year"] is None
    assert m["new_independent_copy"] is False and m["group47_contains_work52_confirmed"] is False
    assert a["new_source_routes"]==3
    assert a["new_original_glyph_votes"]==a["new_numeric_independent_witnesses"]==a["new_genealogy_edges"]==a["algorithm_reopen"]==0
    assert a["existing_direct_controls"]==5 and a["existing_target_count"]==6
    assert a["existing_cross_copy_controls"]==0 and a["open_issues"]==11
    assert a["deterministic_product"]=="CLOSED"
def verify():
    e=read(E);validate(e)
    sh=read(SH)
    m=read("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
    state=read("docs/PROJECT-CURRENT-STATE-R1.json")
    ledger=read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
    assert len(sh["sources"])==3 and sh["schema"]=="TIANWEN-13J-NLC99-WASEDA1848-WUL47-SOURCE-SHARD-R1"
    assert all(x["physical_glyph_authority"] is False and x["evidence"]==E for x in sh["sources"])
    assert len({x["source_id"] for x in sh["sources"]})==3
    assert any(x["path"]==SH and x["schema"]==sh["schema"] and x["source_count"]==3 for x in m["shards"])
    assert m["root_source_count"]==647 and m["extension_source_count"]==87 and m["combined_source_count"]==734
    assert state["schema_version"]=="1.673.0"
    assert state["historical_audit"]["external_source_registry_total_unique_count"]==734
    assert state["historical_audit"]["external_source_registry_extension_count"]==87
    assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]
    assert state["schema_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
    assert state["historical_audit"]["current_focus"][-1].startswith("13J ")
    assert ledger["binding"]["latest_research_focus_prefix"]=="13J"
    issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
    assert issue["status"]=="OPEN"
    assert all(x in issue["source_refs"] for x in (E,"docs/research/TIANWEN-13J-NLC99-WASEDA1848-WUL47-COPY-FIREWALL-R1.md",SH))
    assert len(ledger["issues"])==11
    assert ledger["checkpoint_log"][-1]["state_version"]=="1.673.0"
    assert {x["id"] for x in ledger["issues"]}==set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])
    assert state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
    assert state["invariants"]["algorithm_reopen_count"]==0
    return {"status":"PASS","source_count":734,"new_original_votes":0}
if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False))
