#!/usr/bin/env python3
"""13KN semantic-object firewall; received transcriptions are not original source glyphs."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13KN-MOON-LIMIT-OPERATOR-OBJECT-AND-INDEX-FIREWALL-R1.json"
def chk(v,message):
    if not v: raise ValueError(message)
def load():
    return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in [E,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"])
def apply(op,prior,delta,condition):
    chk(condition in ("益","損"),"condition")
    sign=op["effect_sign"] if condition=="益" else op["opposite_effect_sign"]
    return prior+sign*delta
def verify(e,state,ledger):
    chk(e["schema"]=="TIANWEN-13KN-MOON-LIMIT-OPERATOR-OBJECT-AND-INDEX-FIREWALL-R1","schema")
    ops={v["id"]:v for v in e["operator_layers"]}
    chk(set(ops)=={"HUANG_RECEIVED_NEXT_DAY","MING_HARVARD_NEXT_LIMIT","MEI_RECEIVED_FAST","MEI_RECEIVED_SLOW"},"four distinct operators")
    expect={"HUANG_RECEIVED_NEXT_DAY":("NEXT_DAY_GAIN_LOSS_AMOUNT",1,-1,"MODERN_TRANSCRIPTION_ONLY",False),"MING_HARVARD_NEXT_LIMIT":("NEXT_LIMIT_GAIN_LOSS_AMOUNT",-1,1,"DIRECT_PRINTED_ORIGINAL_P12",True),"MEI_RECEIVED_FAST":("FINAL_MOON_MOTION_DEGREE_FROM_BASELINE",1,-1,"RECEIVED_TEXT_TRANSCRIPTION",False),"MEI_RECEIVED_SLOW":("FINAL_MOON_MOTION_DEGREE_FROM_BASELINE",-1,1,"RECEIVED_TEXT_TRANSCRIPTION",False)}
    for name,(obj,pos,neg,grade,has_original) in expect.items():
        v=ops[name]
        chk((v["object"],v["effect_sign"],v["opposite_effect_sign"],v["evidence_level"],v["original_page_bound_to_this_full_clause"])==(obj,pos,neg,grade,has_original),"operator/evidence:"+name)
        chk(v["condition"]=="益" and v["opposite_condition"]=="損","condition:"+name)
    lim=e["limits"]
    chk(lim["primary_huang_p75"]=={"middle_limit":168,"initial_limit":84,"circumference_limit":336,"original_rgb_hash_recorded_in":"13KM"},"positive p75 numbers")
    chk(lim["received_huang_167_reverse_formula"]=="167 - obtained_limit" and lim["received_reverse_only_not_original"] is True and lim["original_index_base_adjudicated"] is False,"reverse-limit only received")
    for name,domain,reflection in [("zero_based_candidate",(0,167),167),("one_based_candidate",(1,168),169)]:
        c=lim[name]
        chk((c["domain_min"],c["domain_max"],c["reflection_sum"])==(*domain,reflection),"domain model")
        chk({reflection-i for i in range(domain[0],domain[1]+1)}==set(range(domain[0],domain[1]+1)),"bijective reflection")
    a=e["bounded_illustration"];chk(a["not_historical_source_numbers"] is True and a["inputs"]=={"prior_amount":100,"increment":10},"synthetic not historic")
    for name,key in [("HUANG_RECEIVED_NEXT_DAY","huang_received"),("MING_HARVARD_NEXT_LIMIT","ming_print"),("MEI_RECEIVED_FAST","mei_fast_degree"),("MEI_RECEIVED_SLOW","mei_slow_degree")]:
        for condition,suffix in [("益","gain"),("損","loss")]:
            chk(apply(ops[name],100,10,condition)==a["results"][key+"_"+suffix],"synthetic direction:"+name)
    bounds=e["adjudication"]
    for k in ["all_temporal_stage_semantics_identical_proven","mei_final_degree_operator_equals_ming_next_amount_operator","huang_p79_dayan_glyph_proves_received_next_day_clause","huang_original_full_167_glyph_verified","transcript_is_independent_manuscript_witness","ancient_copying_error_proven","zero_based_selection_proven","original_physical_edition_binding_proven"]:
        chk(bounds[k] is False,"no overpromotion:"+k)
    chk(bounds["huang_received_and_ming_primary_have_opposing_literal_next_amount_directions"] is True,"received textual difference retained")
    chk(len(e["primary_repo_evidence"])==2 and len(e["modern_reading_locators"])==2 and all(x["direct_original_target_glyph_verified"] is False for x in e["modern_reading_locators"]),"source class")
    inv=e["invariant_counts"];chk(inv=={"source_registry_total":765,"matrix_rows":222,"graph_nodes":252,"graph_edges":238,"open_risks":11,"g893_six_numeric_winners":0,"chart_algorithm_reopens":0,"chart_product":"CLOSED"},"source chart invariants")
    chk(not e["transmission_impact"]["edges_supported"] and not e["transmission_impact"]["edges_revised"],"lineage no award")
    h=state["historical_audit"];b=ledger["binding"]
    chk(state["schema_version"]==h["research_omission_guard"]["reviewed_state_version"]==b["reviewed_state_version"],"state/ledger version")
    chk(len(h["current_focus"])==b["source_focus_count"] and h["current_focus"][-1].startswith(b["latest_research_focus_prefix"]+" "),"focus")
    chk(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"closed")
    issue=next(x for x in ledger["issues"] if x["id"]==e["issue_id"])
    chk(issue["status"]=="OPEN" and issue["priority"]=="P0" and E in issue["source_refs"] and E.replace(".json",".md") in issue["source_refs"],"open issue evidence")
    chk(any(v.get("revision_id")=="TW-OPEN-0005-13KN-OPERATOR-OBJECT-FIREWALL-20261029" and E in v.get("evidence_refs",[]) for v in issue["history"]),"forward revision")
    chk(len(ledger["issues"])==11 and ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"],"risk review")
    return {"status":"PASS","operators":4,"historical_winners":0,"algorithm_reopens":0}
if __name__=="__main__":
    print(json.dumps(verify(*load()),ensure_ascii=False))
