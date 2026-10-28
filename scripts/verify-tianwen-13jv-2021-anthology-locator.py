#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EVIDENCE="docs/research/TIANWEN-13JV-2021-ANTHOLOGY-COPY-LOCATOR-AND-PAGINATION-GATE-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load():
    return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (EVIDENCE,STATE,LEDGER))
def verify(e,s,l):
    assert e["schema"]=="TIANWEN-13JV-2021-ANTHOLOGY-COPY-LOCATOR-AND-PAGINATION-GATE-R1"
    p=e["publication"]
    assert p["isbn13"]=="9787520181907"
    assert (p["toc_chapter_start_page"],p["toc_next_chapter_start_page"])==(208,236)
    assert p["inferred_chapter_print_range"]==[208,235]
    assert p["inferred_range_is_original_leaf_verified"] is False
    assert {x["grade"] for x in e["locators"]}=={
        "MODERN_COMMUNITY_BIBLIOGRAPHIC_TOC","MODERN_COMMERCIAL_BIBLIOGRAPHY",
        "FIRSTPARTY_INSTITUTIONAL_ACQUISITION_NOTICE","MODERN_EBOOK_CATALOG_ACCESS_LIMIT",
        "MODERN_REPOST_PREVIOUS_13JU"}
    a=e["exclusions"]
    assert all(a[k] is False for k in (
        "original_2021_print_leaf_examined","article_2021_wording_collated_against_repost",
        "copy_level_acquisition_or_call_number_verified","web_toc_start_page_is_original_page_photo",
        "modern_page_locator_is_ancient_original"))
    assert all(a[k]==0 for k in (
        "g893_six_original_numbers_awarded","ancient_physical_fascicle_binding_awarded",
        "new_registry_source_count","graph_growth","algorithm_reopen"))
    assert a["chart_product"]=="CLOSED" and e["transmission_impact"]=="NONE_BIBLIOGRAPHIC_ACCESS_ROUTE_ONLY"
    f=s["historical_audit"]["current_focus"]
    assert any(x.startswith("13JV ") for x in f) and any(x.startswith("13JU ") for x in f)
    assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    assert len(f)==l["binding"]["source_focus_count"]
    assert f[-1].split(" ",1)[0]==l["binding"]["latest_research_focus_prefix"]
    i=next(v for v in l["issues"] if v["id"]=="TW-OPEN-0005")
    assert i["status"]=="OPEN" and i["priority"]=="P0"
    assert EVIDENCE in i["source_refs"] and EVIDENCE.replace(".json",".md") in i["source_refs"]
    assert sum(x.get("revision_id")=="TW-OPEN-0005-13JV-2021-ANTHOLOGY-20261028" for x in i["history"])==1
    assert any(x.get("revision_id")=="TW-OPEN-0005-13JU-THREEWAY-20261028" for x in i["history"])
    assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
    return {"status":"PASS","original_2021_leaves":0,"g893_six_awards":0}
if __name__=="__main__":print(json.dumps(verify(*load())))
