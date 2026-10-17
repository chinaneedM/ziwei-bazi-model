#!/usr/bin/env python3
"""12YZ first-party received Goryeosa D14-D20 triple-column exact arithmetic, not ancient original."""
from decimal import Decimal
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YZ-GORYEOSA-D14-D20-INTRATABLE-THREE-COLUMN-RECEIVED-ARITHMETIC-R1.json"
PRIOR="docs/research/TIANWEN-12YY-GORYEOSA-FIRSTPARTY-ONLINE-SOLAR-D16-RECEIVED-VARIANT-VS-G893-ORIGINAL-R1.json"
G893="docs/research/TIANWEN-12YG-G893-SEVEN-DAY-SOLAR-DECREASING-LANE-SECOND-ERRATUM-R1.json"
def load():
    return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC,PRIOR,G893,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json"))
def need(cond,msg):
    if not cond: raise ValueError(msg)
def verify(d,prior,g893,ledger,state):
    need(d["schema"]=="TIANWEN-12YZ-GORYEOSA-OFFICIAL-RECEIVED-TRIPLE-COLUMN-LOCAL-ARITHMETIC-R1","schema")
    src=d["sources"]
    need(src["official_url"]=="https://db.history.go.kr/goryeo/level.do?levelId=kr_052_0010_0010_0020_0010&types=o","first party locator")
    need(src["earlier_comparison"]==PRIOR and src["g893_same_copy_original"]==G893,"prior evidence refs")
    need(src["new_original_page_acquired"] is False and src["g893_sha_bound_original_evidence_reused"] is True,"not new image")
    x=d["modern_received_rows"]
    need([z["day"] for z in x]==list(range(14,21)),"day window")
    need([z["short"] for z in x]==["5.1990","5.2176","5.1362","5.2548","5.2734","5.2920","5.3106"],"first party short transcription")
    need([z["long"] for z in x]==["440.0239","434.8249","429.6073","424.3711","419.1163","413.8429","408.5509"],"first party long transcription")
    need([z["cumulative"] for z in x]==["6695.8136","7135.8375","7570.6624","8000.2697","8424.6408","8843.7571","9257.6000"],"first party cumulative transcription")
    need([z["short_raw"] for z in x]==["五分一九九〇","五分二一七六","五分一三六二","五分二五四八","五分二七三四","五分二九二〇","五分三一〇六"],"literal short glyphs")
    need([z["long_raw"] for z in x]==["四百四十〇〇二三九","四百三十四八二四九","四百二十九六〇七三","四百二十四三七一一","四百一十九一一六三","四百一十三八四二九","四百〇八五五〇九"],"literal long glyphs")
    need([z["cumulative_raw"] for z in x]==["六千六百九十五八一三六","七千一百三十五八三七五","七千五百七十〇六六二四","八千〇〇〇二六九七","八千四百二十四六四〇八","八千八百四十三七五七一","九千二百五十七六〇〇〇"],"literal cumulative glyphs")
    need([z["day"] for z in g893["readings"]]==list(range(14,21)) and [z["long_decimal"] for z in g893["readings"]]==[z["long"] for z in x],"prior same-original G893 long control")
    need([z["short_decimal"] for z in g893["readings"]]==["5.1990","5.2176","5.2362","5.2548","5.2734","5.2920","5.3106"],"original one-glyph source difference")
    need([z["official_number"] for z in prior["direct_reading"]["days"]]==[z["short"] for z in x[1:4]],"12YY verified D15-D17")
    c=d["local_relations"]
    need(c["long_relation"]=="LONG(day) - LONG(day+1) = SHORT(day)" and c["cumulative_relation"]=="CUM(day+1) - CUM(day) = LONG(day)","local equations")
    fail=[]
    for i in range(6):
        z=x[i]; nxt=x[i+1]; item=c["edges"][i]
        dl=Decimal(z["long"])-Decimal(nxt["long"])
        dc=Decimal(nxt["cumulative"])-Decimal(z["cumulative"])
        ok=dl==Decimal(z["short"])
        need(item["day"]==z["day"] and str(dl)==item["long_drop_to_next"] and str(dc)==item["cumulative_rise_from_previous_to_next"] and item["short_equals_long_drop"] is ok,"per edge exact arithmetic")
        need(dc==Decimal(z["long"]),"cumulative recurrence")
        if not ok:fail.append(z["day"])
    need(fail==c["short_to_long_failure_days"]==[16] and c["short_to_long_success_count"]==5 and c["long_to_cumulative_success_count"]==6,"single failure only")
    need(str(Decimal(x[2]["short"])-Decimal(c["d16_own_long_implied"]))==c["d16_mismatch"]=="-0.1000","actual mismatch")
    need(c["d16_short_received"]=="5.1362" and c["d16_own_long_implied"]=="5.2362" and c["d16_own_cumulative_lane_confirms_long"]=="429.6073" and c["d16_same_copy_original_short"]=="5.2362","exact D16 binding")
    need(c["offending_literal"]=="五分一三六二" and c["original_literal"]=="五分二三六二","cannot silently repair textual glyph")
    fw=d["scope_firewall"]
    for k in ("institution_digital_locus_is_historic_original_folio","official_original_image_pixels_or_hash_acquired","same_goryeosa_paper_copy_as_G893_proven","digital_transcription_error_cause_proven","ancient_print_error_cause_proven","law_outside_14_to_20_proven","historical_少_vs_微_unit_identity_proven","Ming1569_target_column_mechanical_equivalence_proven"):
        need(fw[k] is False,"scope firewall "+k)
    for k in ("source_registry_entries_added","independently_attested_new_physical_originals","genealogy_nodes_added","genealogy_edges_added","algorithm_reopens"):need(fw[k]==0,"no invented sources or graph")
    need(fw["G893_six_controls_fully_adjudicated"]=="5/6" and fw["G893_cross_original_final_decisions"]=="0/6" and fw["product_R1"]=="CLOSED" and fw["unresolved_issue_count"]==11,"unresolved controls")
    issue=next(z for z in ledger["issues"] if z["id"]=="TW-OPEN-0005")
    need(issue["status"]=="OPEN" and DOC in issue["source_refs"] and DOC.replace(".json",".md") in issue["source_refs"],"issue remains open and crosslinked")
    need(issue["g893_12yz_goryeosa_triple_column_reviews"][-1]["received_unique_short_mismatch_day"]==16,"issue appended evidence")
    need(ledger["binding"]["reviewed_state_version"]==state["schema_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"semantic state gate")
    need(ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"]),"focus count")
    need(any(z.startswith("12YZ ") for z in state["historical_audit"]["current_focus"]),"new focus retained")
    need(ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ")[0],"last checkpoint")
    need(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==11,"all 11 reviewed")
    return {"status":"PASS","long_to_cumulative":6,"short_to_long":5,"mismatch_day":16,"mismatch":"-0.1000","new_original_votes":0,"open_issues":11}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
