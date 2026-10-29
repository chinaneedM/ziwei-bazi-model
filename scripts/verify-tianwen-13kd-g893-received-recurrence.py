#!/usr/bin/env python3
"""13KD: exactly replay received-rule bridge against the immutable G893 originals."""
from __future__ import annotations
import argparse
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13KD-G893-MINGSHI-RECEIVED-RECURRENCE-UNIT-BRIDGE-R1.json"
UP="docs/research/TIANWEN-13KC-G893-SAME-COPY-FIVE-ROW-ORIGINAL-COLLATION-R1.json"
SCALE=10**6


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def microfen(s: str) -> int:
    value=Decimal(s)*SCALE
    require(value==value.to_integral_value(),"noninteger microfen")
    return int(value)


def q(g:int, init:int, first:int, increase:int) -> int:
    require(type(g)==int and 0<=g<=167,"invalid table-limit scope")
    require(increase % 2==0,"half-second-difference would be fractional")
    return init-first*g-(increase//2)*g*(g-1)


def verify(e):
    require(e["schema"]=="TIANWEN-13KD-G893-MINGSHI-RECEIVED-RECURRENCE-UNIT-BRIDGE-R1","schema")
    require(e["issue_id"]=="TW-OPEN-0005" and e["source_copy"]=="SNU Kyujanggak GK00893_00" and e["source_physical_copy_count"]==1,"source scope")
    require(e["upstream_same_copy_evidence"]==UP,"upstream G893 scope")
    c=e["historical_unit_position_candidate"]
    require(c["base_microfen"]==SCALE,"microfen unit base")
    p=c["derived"]
    require((p["initial_gain_microfen"],p["initial_step_microfen"],p["step_increase_microfen"],p["half_step_increase_microfen"])==(11081575,58150,1950,975),"received source rule constants")
    require(all("RECEIVED" in x["role"] or "SECONDARY" in x["role"] for x in e["received_rule_sources"]),"received source grading")
    require(all(x["url"].startswith("https://") for x in e["received_rule_sources"]),"source links")
    raw=json.loads((ROOT/UP).read_text(encoding="utf-8"))
    require(raw["book_code"]=="GK00893_00" and raw["physical_copy_count"]==1,"one original book")
    windows={x["target"]:x for x in raw["five_row_same_copy_windows"]}
    require(set(windows)=={8,124,132},"upstream three target cases")
    facts=e["exact_same_copy_replay"]
    require(len(facts)==2 and [x["target"] for x in facts]==[8,132],"two sign cases")
    for f in facts:
        w=windows[f["target"]]
        require(f["limits"]==w["limit_sequence"],"limits must match original source")
        require(len(f["limits"])==len(f["expected_microfen"])==len(f["expected_residual_microfen"])==5,"five rows")
        for n,real,micro,delta in zip(f["limits"],w["same_copy_display_magnitude"],f["expected_microfen"],f["expected_residual_microfen"]):
            require(microfen(real)==micro,"source display magnitude changed")
            g=n if f["target"]==8 else 167-n
            calc=q(g,p["initial_gain_microfen"],p["initial_step_microfen"],p["step_increase_microfen"])
            require(calc-micro==delta==0,"source-original or received-rule arithmetic mismatch")
    require(e["indexing"]["loss_mirror_status"].startswith("EMPIRICAL_"),"loss index is not primary text")
    ji=e["ji_limit_exploration"]
    require(ji["target"]==124 and ji["limits"]==windows[124]["limit_sequence"],"ji source limits")
    require(ji["displayed_ji_five_rows"]==windows[124]["same_copy_display_magnitude"],"ji source original changed")
    require(ji["degree_to_1e8_denominator"]==10**8,"unit scale")
    require(ji["candidate_mean_per_limit_degree"]=="1.0963","not fully proven mean degree")
    mean=Decimal(ji["candidate_mean_per_limit_degree"])
    errs=[]
    for n,raw_val,expected,delta in zip(ji["limits"],ji["displayed_ji_five_rows"],ji["candidate_prediction_degree"],ji["prediction_minus_display_1e8"]):
        g=167-n
        calc=mean-(Decimal(q(g,p["initial_gain_microfen"],p["initial_step_microfen"],p["step_increase_microfen"]))/Decimal(10**8))
        require(calc==Decimal(expected),"ji numerical bridge mismatch")
        residual=int((calc-Decimal(raw_val))*10**8)
        require(residual==delta,"ji residual changed")
        errs.append((n,calc,Decimal(raw_val)))
    bad=[n for n,pred,real in errs if pred.quantize(Decimal("0.0001"),rounding=ROUND_HALF_UP)!=real]
    require(bad==[122] and ji["four_decimal_half_up_violation_limit"]==122,"do not silently award ji rounding")
    require(ji["scope"].startswith("CANDIDATE_APPROXIMATION_ONLY"),"rounded ji algorithm not closed")
    res=e["results"]
    require(res["same_copy_loss_gain_exact_rows"]==res["same_copy_loss_gain_comparisons"]==10,"ten real rows")
    for field in ("new_physically_independent_historical_witnesses","source_registry_delta","genealogy_nodes_delta","genealogy_edges_delta","historical_cross_witness_numeric_winners","algorithm_reopens"):
        require(type(res[field])==int and res[field]==0, "historical scope promotion: "+field)
    require(res["remaining_omission_risks"]==11 and res["chart_product"]=="CLOSED" and res["ji_exact_literal_algorithm_closure"] is False,"risk/product scope")
    return {"result":"PASS","source_original_same_copy_rows":10,"received_rule_exact_matches":10,
            "ji_rounding_counterexample":122,"historical_winners":0,"physical_copy_count":1}


def handoff():
    s=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf-8"))
    l=json.loads((ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf-8"))
    h=s["historical_audit"]
    require(s["schema_version"]==l["binding"]["reviewed_state_version"]==h["research_omission_guard"]["reviewed_state_version"],"state/ledger sync")
    require(l["binding"]["source_focus_count"]==len(h["current_focus"]),"focus count")
    require(h["current_focus"][-1].startswith(l["binding"]["latest_research_focus_prefix"]+" "),"latest research focus")
    issue=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
    require(issue["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:"),"new batch action")
    require({E,E.replace(".json",".md")}.issubset(issue["source_refs"]),"evidence refs")
    require(any(x.get("revision_id")=="TW-OPEN-0005-13KD-RECEIVED-UNIT-20261029" for x in issue["history"]),"append-only issue history")
    require(s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0,"product close")


if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.parse_args()
    handoff()
    print(json.dumps(verify(json.loads((ROOT/E).read_text(encoding="utf-8"))),ensure_ascii=False))
