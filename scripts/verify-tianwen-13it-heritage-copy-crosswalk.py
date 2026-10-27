#!/usr/bin/env python3
"""13IT source-level comparison without ancient-original or book-to-juan promotion."""
import copy
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-13IT-GK5553-5554-HERITAGE-COPY-CROSSWALK-R1.json"
def load(path=DOC):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(e, *, state=None, ledger=None):
    assert e["schema"]=="TIANWEN-13IT-GK5553-5554-HERITAGE-COPY-CROSSWALK-R1"
    assert e["issue_id"]=="TW-OPEN-0005"
    t=e["evidence_tiers"]
    sn=t["kyujanggak_firstparty_catalog"]
    assert sn["shelfmark"]=="GK05553_00" and sn["handwritten_supplement_book_numbers"]==[8,26,29]
    assert sn["explicit_book29_to_juan81_83_binding"] is False
    gov=t["korean_heritage_firstparty_index"]
    assert gov["described_juan_count"]==98 and gov["described_book_count"]==32
    assert gov["official_long_description_directly_retrieved"] is False
    assert gov["shelfmark_in_search_snippet"] is None
    q=t["copied_heritage_description"]
    assert q["kind"].startswith("SECONDARY_REPUBLICATION")
    assert q["reported_first_holding_supplementation"]==[
       {"book":8,"juan":[19,20,21]},{"book":12,"juan":[31,32,33]},{"book":26,"juan":[73,74]}]
    assert q["reported_second_supplies_first_juan"]==[81,82]
    assert q["independent_ancient_physical_witness"] is False
    assert q["official_paragraph_verified_against_firstparty"] is False
    c=e["source_conflicts"]
    assert c["supplement_book_number_sets"]=={"firstparty_snu":[8,26,29],"secondary_republication":[8,12,26],"resolved":False}
    assert c["historical_13IN_book29_to_juan81_83_status"]=="RETRACTED_UNBOUND"
    assert c["physical_original_juan81_82_seen"] is False and c["exact_insertion_order_or_volume_to_juan_map_proven"] is False
    assert c["neither_secondary_copy_nor_official_index_authorizes_a_winner"] is True
    keep=e["controls"]
    assert keep=={"source_registry_count_unchanged":761,"matrix":[222,222],"genealogy":[252,238],"risk_issues":11,"chart":"CLOSED","algorithm_reopens":0,"candidate_collapses":0,"new_original_images":0,"new_source_registry_entries":0,"new_genealogy_nodes":0,"new_genealogy_edges":0,"gk3467_d1_d7_decided":False,"g893_six_decided":False,"nlc03130_solar_d30":None,"nlc03130_summer_d14":None}
    assert e["transmission_impact"]["edges_supported"]==[]
    s=state if state is not None else load("docs/PROJECT-CURRENT-STATE-R1.json")
    l=ledger if ledger is not None else load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
    assert tuple(map(int,s["schema_version"].split("."))) >= (1,899,0)
    assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    f=s["historical_audit"]["current_focus"]
    assert any(x.startswith("13IT ") for x in f)
    assert l["binding"]["source_focus_count"]==len(f)
    assert l["binding"]["latest_research_focus_prefix"]==f[-1].split(" ",1)[0]
    iss=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
    assert iss["status"]=="OPEN" and iss["priority"]=="P0"
    assert DOC in iss["source_refs"]
    assert "13IO" in iss["next_action"] and "RETRACTED" in iss["next_action"]
    assert any(h.get("revision_id","").startswith("TW-OPEN-0005-13IT-") and DOC in h.get("evidence_refs",[]) for h in iss["history"])
    assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
    return True
if __name__=="__main__":
    assert check(load())
    print("TIANWEN_13IT_HERITAGE_COPY_CROSSWALK_PASS")
