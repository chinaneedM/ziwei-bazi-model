#!/usr/bin/env python3
"""13BP bounded two-source original-record field-specific alignment gate."""
import hashlib,json
from decimal import Decimal
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13BP-GORYEOSA-TWO-HOLDING-LOCAL-FIELD-DAY-ALIGNMENT-R1.json"
MD="docs/research/TIANWEN-13BP-GORYEOSA-TWO-HOLDING-LOCAL-FIELD-DAY-ALIGNMENT-R1.md"
W="docs/research/TIANWEN-13BN-GORYEOSA-WASEDA-P23-P24-TIGHT-CUMULATIVE-AND-LONG-ROI-R1.json"
N="docs/research/TIANWEN-13BK-GORYEOSA-NAJ-CANVAS18-D19-LONG-D20-D21-CUMULATIVE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
def load(path):return json.loads((R/path).read_text(encoding="utf-8"))
def blob(path):
    b=(R/path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def check(e,w,n,l,s,physical=True):
    assert e["schema"]=="TIANWEN-13BP-EXISTING-ORIGINAL-RECORDS-FIELD-SENSITIVE-PRINTED-DAY-ALIGNMENT-R1"
    assert e["issue_id"]=="TW-OPEN-0005"
    assert e["grade"]=="SHA_BOUND_CROSS_RECORD_NUMERIC_COMPARISON_NOT_NEW_ORIGINAL_IMAGE_REVIEW"
    ss=e["source_files"]
    assert [(z["path"],z["git_blob_sha"]) for z in ss]==[(W,"e5e7df6d6b1d8553b81561b9ee0e6798bedc1726"),(N,"3513e5957302e644ce4d064e0cf896e33549cfb0")]
    if physical:
        assert all(blob(z["path"])==z["git_blob_sha"] for z in ss)
        assert (R/MD).is_file()
    assert ss[0]["physical_copy"]==w["source"]["holding"]
    assert ss[1]["physical_copy"]==n["source"]["physical_holding"]
    wr={z["key"]:z for z in w["original_single_numeric_lane_rois"]}
    nr={z["key"]:z for z in n["original_native_rois"]}
    a=e["observed_local_matches"]
    assert [(z["field"],z["numeral"],z["waseda_day"],z["waseda_roi"],z["naj_day"],z["naj_roi"],z["day_delta"]) for z in a]==[
     ("CUMULATIVE","8843.7571",19,"P23_D19_C",20,"D20_CUM",1),
     ("CUMULATIVE","9257.6000",20,"P23_D20_C",21,"D21_CUM",1),
     ("LONG","413.8429",19,"P23_D19_LONG",19,"D19_LONG",0)]
    for z in a:
        x=wr[z["waseda_roi"]];y=nr[z["naj_roi"]]
        assert x["field"]==y["field"]==z["field"]
        assert x["printed_day"]==z["waseda_day"] and y["layout_day"]==z["naj_day"]
        assert Decimal(x["value"])==Decimal(y["decimal"])==Decimal(z["numeral"])
        assert z["naj_day"]-z["waseda_day"]==z["day_delta"]
    assert {z["day_delta"] for z in a}=={0,1}
    ar=e["local_arithmetic"]
    assert [(z["holding"],z["start_day"],z["end_day"],z["same_copy_long_day"]) for z in ar]==[("WASEDA",19,20,19),("NAJ",20,21,19)]
    for z in ar:
        assert (Decimal(z["to"])-Decimal(z["from"])==Decimal(z["same_copy_long"])==Decimal("413.8429"))
    assert {"UNIFORM_ALL_FIELD_DATE_OFFSET","FULL_TABLE_INDEX_LAW","CHART_ALGORITHM_REOPEN"}.issubset(set(e["unproven"]))
    assert e["transmission_impact"]["nodes_added"]==e["transmission_impact"]["edges_supported"]==e["transmission_impact"]["edges_revised"]==[]
    fw=e["scope_firewall"]
    for k in ("new_original_images","new_original_roi_reviews","new_physical_witnesses","independent_lineage_votes","source_registry_increase","matrix_rows_increase","genealogy_nodes_increase","genealogy_edges_increase","algorithm_reopens"):
        assert fw[k]==0
    assert fw["research_risks_open_or_blocked"]==len(l["issues"])==11
    assert fw["product"]==s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
    iss=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
    assert iss["status"]=="OPEN" and iss["priority"]=="P0"
    assert iss["source_refs"].count(P)==iss["source_refs"].count(MD)==1
    assert iss["source_refs"].index(P)==iss["source_refs"].index(MD)+1
    h=next(z for z in iss["history"] if z.get("revision_id")=="TW-OPEN-0005-CROSS-FIELD-13BP")
    assert h["previous_next_action"].startswith("13BO CURRENT ACTION")
    assert {MD,P,W,N}.issubset(set(h["evidence_refs"]))
    ix=iss["history"].index(h);later=any("next_action" in z.get("changed_fields",[]) for z in iss["history"][ix+1:])
    prefix=l["binding"]["latest_research_focus_prefix"]
    assert iss["next_action"].startswith("13BP CURRENT ACTION") or (later and prefix!="13BP" and iss["next_action"].startswith(prefix+" CURRENT ACTION"))
    assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
    assert any(z.startswith("13BP ") for z in s["historical_audit"]["current_focus"])
    assert prefix==s["historical_audit"]["current_focus"][-1].split(" ")[0]
    assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
    assert set(l["checkpoint_log"][-1]["reviewed_issue_ids"])=={z["id"] for z in l["issues"]}
    return True
if __name__=="__main__":
    assert check(load(P),load(W),load(N),load(L),load(S))
    print("13BP cross-source field/day original record comparison PASS")
