#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH="docs/research/TIANWEN-13IL-GK3467-SNU-CURATORIAL-COPY-SCOPE-AND-2020-FACSIMILE-FIREWALL-R1.json"
def read(p=PATH):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check(x, state_check=True):
    assert x["schema"]=="TIANWEN-13IL-GK3467-SNU-CURATORIAL-COPY-SCOPE-AND-2020-FACSIMILE-FIREWALL-R1"
    assert x["issue_id"]=="TW-OPEN-0005"
    a=x["institutional_evidence"]
    assert len(a)==3 and a[0]["specifically_bound_book"]==6 and a[0]["specifically_bound_juan"]==52
    assert a[0]["book6_material_as_cataloged"]=="乙亥字"
    assert a[0]["original_book6_folio_by_folio_review_in_article"] is False
    assert a[1]["item"]=="奎3467의4" and a[1]["impression_year_literal"]=="[刊年未詳]"
    assert a[1]["physical_copy_internal_missing_leaf_count"] is None
    assert a[2]["original_per_folio_juan52_negative_proof"] is False
    j=x["journal_reconciliation"]
    assert j["facsimile_base_item"]=="奎5554" and j["target_item"]=="奎3467의4"
    for k in ("are_facsimile_base_and_target_same_item","does_received_facsimile_base_establish_original_juan52_leaf_sequence","original_article_pdf_bytes_obtained","original_article_target_page_verified","original_article_footnotes_verified"):
        assert j[k] is False
    o=x["original_scope"]
    assert o["same_copy_printed_folio_anchors"]==[[4,2],[6,10],[7,11]]
    for k in ("same_copy_first_d1_d7_direct_original_obtained","same_copy_own_winter_table_title_direct_obtained","physical_intermediate_folios_verified","exact_impression_date_verified","original_physical_leaf_loss_proven"):
        assert o[k] is False
    assert o["number_physically_missing_leaves"] is None
    assert x["invariants"]=={"matrix":[222,222],"sources":761,"graph":[252,238],"open_issues":11,"product":"CLOSED","algorithm_reopens":0,"candidate_collapses":0}
    assert all(v==0 for k,v in x["source_policy"].items() if k.endswith("_count") or k.endswith("_increment"))
    if state_check:
        s=read("docs/PROJECT-CURRENT-STATE-R1.json")
        l=read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
        assert s["schema_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]==l["binding"]["reviewed_state_version"]
        assert tuple(map(int,s["schema_version"].split("."))) >= (1,891,0)
        assert any(z.startswith("13IL ") for z in s["historical_audit"]["current_focus"])
        issue=next(i for i in l["issues"] if i["id"]==x["issue_id"])
        assert issue["status"]=="OPEN" and PATH in issue["source_refs"]
        assert any(z.get("new_action_prefix")=="13IL" for z in issue["history"])
    return True
if __name__=="__main__":
    assert check(read())
    print("TIANWEN_13IL_SNU_CURATORIAL_AND_FACSIMILE_FIREWALL_PASS")
