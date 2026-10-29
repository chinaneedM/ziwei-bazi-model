#!/usr/bin/env python3
"""13KS: strict Fraction replay for three received Ming Shi v35 numbers. No original-page claim."""
import json
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13KS-MINGSHI-V35-ROUNDED-LIMIT-THREE-CONSTANT-REPLAY-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
REGISTRY="docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"

def require(predicate,message):
    if not predicate:
        raise ValueError(message)

def read():
    return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (E,STATE,LEDGER,REGISTRY))

def verify(e,s,l,r):
    require(e["schema"]=="TIANWEN-13KS-MINGSHI-V35-ROUNDED-LIMIT-THREE-CONSTANT-REPLAY-R1" and e["issue_id"]=="TW-OPEN-0005","identity")
    src=e["source"]
    require(src["source_id"]=="EXT-WIKISOURCE-MINGSHI-V35-DATONG-TIME","source id")
    require(any(x["source_id"]==src["source_id"] for x in r["sources"]),"not registered")
    require(src["url"]=="https://zh.wikisource.org/wiki/明史/卷35","source URL")
    require(src["role"]=="ALREADY_REGISTERED_RECEIVED_TRANSCRIPTION_NOT_SOURCE_IMAGE","evidence grade")
    require(src["electronic_text_checked_this_batch"] is True,"text scope")
    for k in ("dated_original_folio_image_checked_this_batch","original_physical_impression_authenticated","publisher_or_copy_lineage_adjudicated"):
        require(src[k] is False,"fabricated original grade "+k)
    require(len(src["received_phrases"])==8 and all(isinstance(x,str) and x for x in src["received_phrases"]),"text phrases")
    a=e["arithmetic_basis"]
    require(a["day_base_units"]==10000 and a["original_820_units_per_limit"]==820,"base units")
    require(a["received_daily_limit_rate"]=="61/5" and a["exact_daily_limit_rate"]=="500/41","rate")
    require(a["comparison_is_model_scoped"] is True,"scope")
    require(a["half_turn_from_full_turn_units"]=="275546/2" and a["first_quarter_from_new_moon_units"]=="29530593/100/4" and a["new_moon_turn_difference_units"]=="1975993/100","received input provenance")
    assert_mid=F(275546,2)
    assert_delta=F(1975993,100)
    assert_quarter=F(29530593,100)/4
    inputs=(("TURN_MID_LIMIT","轉中限",assert_mid,"168.083060"),
            ("SYNODIC_TURN_DIFF_LIMIT","朔轉限",assert_delta,"24.1071146"),
            ("QUARTER_PHASE_TURN_LIMIT","弦轉限",assert_quarter,"90.06830865"))
    require(len(e["controls"])==3,"three controls")
    for c,(expected_id,expected_name,base,quoted) in zip(e["controls"],inputs):
        require((c["id"],c["source_label"],c["source_value"])==(expected_id,expected_name,quoted),"received displayed number")
        require(F(c["input_base_units"])==base,"input mismatch")
        rounded=base*F(61,5)/F(10000)
        exact=base/F(820)
        require(rounded==F(quoted),"received rate fails exact equality: "+c["id"])
        require(F(c["rounded_replay_fraction"])==rounded and c["rounded_replay_fraction"]==str(rounded),"rounded representation mismatch")
        require(F(c["exact_820_replay_fraction"])==exact and c["exact_820_replay_fraction"]==str(exact),"exact comparator mismatch")
        require(F(c["rounded_minus_exact_fraction"])==rounded-exact and c["rounded_minus_exact_fraction"]==str(rounded-exact),"surplus mismatch")
        require(rounded-exact==base/F(2050000)>0,"positive rate discrepancy")
    n=e["adjudication"]
    require(n["three_received_rounded_rate_matches"] is True and n["three_exact_820_replays_equal_received_values"] is False,"internal arithmetic verdict")
    require(n["received_text_rounded_rate_operational_consistency"]=="ATTESTED_WITHIN_THIS_RECEIVED_TEXT_AND_EXACT_REPLAY","claim grade")
    for k in ("is_a_calendar_dated_worked_example","source_specific_integer_limit_truncation_attested",
              "source_specific_index_base_selected","source_specific_83_84_threshold_reconciled",
              "ming_v35_turn_mid_limit_equals_ming_v33_integer_reverse_constant_as_full_mechanical_object",
              "huang_and_ming_same_epoch_and_coordinate_proven",
              "physical_original_page_direct_glyph_attested_this_batch"):
        require(n[k] is False,"false historical promotion: "+k)
    require(n["new_independent_source_count"]==n["original_g893_six_numeric_winners"]==n["deterministic_chart_algorithm_defect_confirmed"]==n["algorithm_reopens"]==0,"unapproved award")
    require(n["deterministic_chart_product"]=="CLOSED","product status")
    require(e["counts"]==dict(source_registry=765,matrix_rows=222,graph_nodes=252,graph_edges=238,open_research_issues=11),"counts")
    imp=e["transmission_impact"]
    require(not imp["edges_supported"] and not imp["edges_revised"] and not imp["nodes_added_or_strengthened"],"genealogy direct edge")
    require(s["schema_version"]=="1.938.0","state version")
    require(s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0,"chart invariants")
    h=s["historical_audit"]
    require(h["external_source_registry_total_unique_count"]==765 and h["row_count"]==h["audited_row_count"]==222,"source and matrix")
    require(h["research_omission_guard"]["reviewed_state_version"]==s["schema_version"]==l["binding"]["reviewed_state_version"],"ledger review version")
    require(l["binding"]["latest_research_focus_prefix"]=="13KS" and l["binding"]["source_focus_count"]==len(h["current_focus"]),"focus count")
    require(h["current_focus"][-1].startswith("13KS "),"focus event")
    issue=next(x for x in l["issues"] if x["id"]==e["issue_id"])
    require(issue["status"]=="OPEN" and issue["priority"]=="P0","open issue scope")
    require(E in issue["source_refs"] and E.replace(".json",".md") in issue["source_refs"],"evidence links")
    require(any(x.get("revision_id")=="TW-OPEN-0005-13KS-RECEIVED-CONSTANTS-20261029" and E in x.get("evidence_refs",[]) for x in issue["history"]),"append-only event")
    require(len(l["issues"])==11 and l["checkpoint_log"][-1]["state_version"]==s["schema_version"],"risk review")
    return {"status":"PASS","source_grade":"RECEIVED_TEXT_ONLY","verified_received_constants":3,"historical_winners":0,"algorithm_reopens":0}

if __name__=="__main__":
    print(json.dumps(verify(*read()),ensure_ascii=False))
