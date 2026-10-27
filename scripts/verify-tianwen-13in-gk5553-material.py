#!/usr/bin/env python3
"""Catalog material exception and secondary journal contradiction (13IN)."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-13IN-GK5553-BOOK29-MATERIAL-CONFLICT-R1.json"
def read(p=DOC):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check(x,check_state=True):
    assert x["schema"]=="TIANWEN-13IN-GK5553-BOOK29-MATERIAL-CONFLICT-R1"
    assert x["issue_id"]=="TW-OPEN-0005"
    a=x["snu_firstparty"];j=x["journal_2020"];c=x["conflict"];scope=x["evidence_scope"]
    assert a["item"]=="奎貴5553-v.1-46" and a["whole_set_type"]=="乙亥字"
    assert a["supplemental_manuscript_book_numbers"]==[8,26,29] and a["book29_juan"]==[81,82,83]  # Historical 13IN assertion retained; 13IO retracts catalog attribution
    assert a["book29_original_folio_images_obtained"] is False and a["exact_impression_year"] is None
    assert j["printed_page"]==100 and j["footnote"]==6 and j["facsimile_base"]=="奎5554" and j["alternate"]=="奎5553"
    assert j["claims_alternate_eulhae_juan"]==[31,77,78,79,81,82] and j["source_pdf_raw_sha256"] is None
    assert c["juan"]==[81,82] and c["status"]=="UNRESOLVED_BOOK_MATERIAL_VS_SECONDARY_PAPER"
    for key in ("paper_proven_wrong","catalog_proven_wrong","physical_book29_juan81_82_verified","full_set_eulhae_label_proves_each_leaf","original_1972_page_seen"):
        assert c[key] is False
    for key in ("is_direct_ancient_original","confirms_gk3467_juan52_leaf_loss","confirms_gk3467_d1_to_d7","confirms_g893_six_numerals"):
        assert scope[key] is False
    for key in ("new_source_registry_entries","new_genealogy_nodes","new_genealogy_edges","algorithm_reopen_count"):
        assert scope[key]==0
    assert x["invariants"]=={"matrix":[222,222],"sources":761,"graph":[252,238],"issues":11,"product":"CLOSED","algorithm_reopens":0}
    if check_state:
        s=read("docs/PROJECT-CURRENT-STATE-R1.json");l=read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
        assert tuple(map(int,s["schema_version"].split("."))) >= (1,893,0)
        assert s["schema_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]==l["binding"]["reviewed_state_version"]
        assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
        assert any(f.startswith("13IN ") for f in s["historical_audit"]["current_focus"])
        issue=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
        assert issue["status"]=="OPEN" and DOC in issue["source_refs"]
        assert any(h.get("new_action_prefix")=="13IN" for h in issue["history"])
    return True
if __name__=="__main__":
    assert check(read())
    print("TIANWEN_13IN_GK5553_BOOK29_MATERIAL_CONFLICT_SCOPE_PASS")
