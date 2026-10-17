#!/usr/bin/env python3
"""12ZA: forward-only official modern Hanja D18 five-place received-text correction."""
from pathlib import Path
from decimal import Decimal
import json
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12ZA-GORYEOSA-OFFICIAL-HANJA-D18-EXTRA-THREE-FORWARD-ERRATUM-R1.json"
OLD="docs/research/TIANWEN-12YZ-GORYEOSA-D14-D20-INTRATABLE-THREE-COLUMN-RECEIVED-ARITHMETIC-R1.json"
def load():
    return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC, OLD, "docs/PROJECT-CURRENT-STATE-R1.json", "docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def require(x,reason):
    if not x:raise ValueError(reason)
def verify(d,old,state,ledger):
    require(d["schema"]=="TIANWEN-12ZA-GORYEOSA-RECEIVED-HANJA-D18-FORWARD-ERRATUM-R1","schema")
    require(d["supersedes_evidence_inferences_of"]==OLD and d["old_record_bytes_preserved"] is True,"append-only")
    require(old["modern_received_rows"][4]["cumulative_raw"]=="八千四百二十四六四〇八" and old["local_relations"]["long_to_cumulative_success_count"]==6,"old mistake visible")
    ss=d["source_surfaces"]
    require(ss["official_hanja"]["literal"]=="八千四百二十四六四〇八三" and ss["official_hanja"]["url"]=="https://db.history.go.kr/goryeo/level.do?levelId=kr_052_0010_0010_0020_0010&types=o","official Hanzi five-place")
    require(ss["official_korean"]["literal"]=="8424분 64초 08미" and ss["official_korean"]["same_institution_as_official_hanja"] is True,"official translated four-place")
    require(ss["wikisource"]["literal"]=="八千四百二十四六四〇八" and ss["wikisource"]["physical_independence_unverified"] is True,"received text is not ancient vote")
    require(d["prior_12yz_actual_record"]["cumulative"]==old["modern_received_rows"][4]["cumulative"]=="8424.6408","old normalized input retained")
    require(d["new_hanja_literal_candidate"]["decimal_lexical_five_place"]=="8424.64083" and d["new_hanja_literal_candidate"]["length_after_decimal"]==5,"five-place reading")
    rep=d["replay"];rows=rep["rows"];need=[14,15,16,17,18,19,20]
    require([x["day"] for x in rows]==need and len(rep["edges"])==6,"seven-day source window")
    require(rows[4]["cumulative_raw"]==ss["official_hanja"]["literal"] and rows[4]["cumulative"]=="8424.64083","no silent truncate D18")
    require(all(rows[i]["short"]==old["modern_received_rows"][i]["short"] and rows[i]["long"]==old["modern_received_rows"][i]["long"] for i in range(7)),"unrelated original numbers unchanged")
    require(all(rows[i]["cumulative"]==old["modern_received_rows"][i]["cumulative"] for i in (0,1,2,3,5,6)),"other cumulative rows unchanged")
    cum_ok=[]; short_ok=[]; residuals=[]
    for i in range(6):
        a,b=rows[i],rows[i+1]; z=rep["edges"][i]
        short_delta=Decimal(a["long"])-Decimal(b["long"])-Decimal(a["short"])
        cum_delta=Decimal(b["cumulative"])-Decimal(a["cumulative"])-Decimal(a["long"])
        require(z["from_day"]==a["day"] and z["to_day"]==b["day"],"day indexing")
        require(Decimal(z["long_short_residual"])==short_delta and Decimal(z["cumulative_minus_long_residual"])==cum_delta,"decimal exact edges")
        cum_ok.append(cum_delta==0);short_ok.append(short_delta==0);residuals.append(cum_delta)
    require(sum(cum_ok)==rep["cumulative_next_minus_current_equals_long_count"]==4,"D18 breaks two exact cumulative edges")
    require(sum(short_ok)==rep["short_equals_next_long_drop_count"]==5 and rep["short_equals_next_long_drop_failure_days"]==[16],"D16 independent status")
    require(rep["cumulative_vs_long_nonzero_edges"]==[{"from_day":17,"to_day":18,"residual":"0.00003"},{"from_day":18,"to_day":19,"residual":"-0.00003"}],"both residuals")
    require(residuals[3]==Decimal("0.00003") and residuals[4]==Decimal("-0.00003") and residuals[3]+residuals[4]==0,"residual sum")
    require(rep["claimed_12yz_cumulative_6_of_6_exact_retracted"] is True and rep["d16_short_discrepancy"]=="-0.1000","erratum accepted")
    q=d["qualifications"]
    require(q["physical_goryeosa_original_image_acquired"] is False and q["source_impression_or_leaf_identified"] is False,"no invented image")
    require(q["cause_of_extra_three"]=="UNADJUDICATED_MODERN_DIGITAL_VS_PRINT" and q["cause_of_d16_one_vs_two"]=="UNADJUDICATED_WITHOUT_HISTORICAL_ORIGINAL","no cause speculation")
    require(q["new_source_registry_entries"]==q["new_physical_witness_votes"]==q["new_transmission_graph_edges"]==q["algorithm_reopens"]==0,"no inflated votes")
    require(q["G893_full_original_fields"]=="5/6" and q["G893_final_cross_copy_decisions"]=="0/6" and q["open_research_issues"]==11 and q["product_R1"]=="CLOSED","invariants")
    issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
    require(issue["status"]=="OPEN" and DOC in issue["source_refs"] and DOC.replace(".json",".md") in issue["source_refs"],"issue crosswalk")
    require(issue["g893_12za_goryeosa_d18_digital_revision"][-1]["hanja_d18_raw"]==ss["official_hanja"]["literal"],"issue revision")
    require(ledger["binding"]["reviewed_state_version"]==state["schema_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"state versions")
    require(ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"]) and ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ")[0],"latest focus")
    require(any(x.startswith("12ZA ") for x in state["historical_audit"]["current_focus"]),"latest research recorded")
    require(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==len(ledger["issues"])==11,"omission check")
    return {"status":"PASS","received_hanja_cumulative_exact":"4/6","received_short_recurrence_exact":"5/6","d18_hanja_suffix":"三","new_physical_votes":0}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
