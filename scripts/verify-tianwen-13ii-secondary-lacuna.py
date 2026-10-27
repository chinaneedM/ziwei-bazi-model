#!/usr/bin/env python3
"""Reject false physical completeness/loss claims from secondary lacuna index."""
import json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-13II-GK3467-SECONDARY-LACUNA-BOUNDARY-R1.json"
def load(path=DOC):
    return json.loads((BASE/path).read_text(encoding="utf8"))
def check(data,with_state=True):
    assert data["schema"]=="TIANWEN-13II-GK3467-SECONDARY-LACUNA-BOUNDARY-R1"
    assert data["issue_id"]=="TW-OPEN-0005"
    assert data["public_sources"][0]["actual_original_pdf_target_page_obtained"] is False
    assert set(x["juan"] for x in data["public_sources"][1]["recorded_lacunae"])=={9,10,44}
    assert data["public_sources"][1]["juan52_in_list"] is True
    assert data["public_sources"][1]["juan52_explicit_lacuna_annotation"] is False
    assert data["public_sources"][2]["independent_physical_witness"] is False
    assert [(p["pdf_page"],p["printed"]) for p in data["actual_source_original_same_side_folios"]]==[(4,2),(6,10),(7,11)]
    for k,v in data["adjudication"].items():
        if isinstance(v,bool): assert v is False,k
    assert data["adjudication"]["exact_edition_impression_year"] is None
    assert data["adjudication"]["physical_loss_count"] is None
    assert data["adjudication"]["second_independent_original_witness_added"]==0
    a=data["invariants"]
    assert a["matrix"]==[222,222] and a["sources"]==761 and a["graph"]==[252,238]
    assert a["issues"]==11 and a["product"]=="CLOSED"
    assert a["algorithm_reopen"]==a["candidate_collapse"]==0
    if with_state:
        s=load("docs/PROJECT-CURRENT-STATE-R1.json")
        l=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
        assert s["schema_version"]==l["binding"]["reviewed_state_version"]
        assert any(x.startswith("13II ") for x in s["historical_audit"]["current_focus"])
        i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
        assert i["status"]=="OPEN" and DOC in i["source_refs"]
        assert any(x.get("new_action_prefix")=="13II" for x in i["history"])
    return True
if __name__=="__main__":
    assert check(load())
    print("TIANWEN_13II_SECONDARY_LACUNA_SCOPE_PASS")
