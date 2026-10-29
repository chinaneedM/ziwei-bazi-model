#!/usr/bin/env python3
"""13KE forward-only text-scope gate; no web OCR promoted into printed glyphs."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-13KE-G893-167-LIMIT-POLARITY-SOURCE-SCOPE-R1.json"
PRIOR="docs/research/TIANWEN-13KD-G893-MINGSHI-RECEIVED-RECURRENCE-UNIT-BRIDGE-R1.json"

def require(p,reason):
    if not p: raise ValueError(reason)

def verify(e):
    require(e["schema"]=="TIANWEN-13KE-G893-167-LIMIT-POLARITY-SOURCE-SCOPE-R1", "schema")
    require(e["issue_id"]=="TW-OPEN-0005", "issue")
    require(e["historical_inputs_unchanged"][1]==PRIOR, "prior review retained")
    old=json.loads((ROOT/PRIOR).read_text(encoding="utf-8"))
    require(old["indexing"]["loss_mirror_status"].startswith("EMPIRICAL_"), "historic old review should not be silently amended")
    require(old["results"]["same_copy_loss_gain_exact_rows"]==10, "prior 10-source-row evidence")
    received=e["received_loci"]
    require(set(received)=={"mingshi","huang"}, "two specified digital text routes")
    ms,hu=received["mingshi"],received["huang"]
    require(ms["gain_loss_direction"]=="GAIN_DECREASE_LOSS_INCREASE" and
            hu["gain_loss_direction"]=="GAIN_INCREASE_LOSS_DECREASE_AS_OCR_RENDERED","polarity directions kept distinct")
    require("益減損加" in ms["text"] and "益加損減" in hu["polarity_source_literal"],"original received-locus contrast lost")
    require("一百六十七限" in hu["reverse_index_source_literal"] and
            hu["reverse_index_grade"]=="ONLINE_OCR_TEXTUAL_POSITIVE_ONLY","167 source level")
    require(ms["source_type"].startswith("MODERN_") and hu["source_type"].startswith("MODERN_"),"received original-grade firewall")
    require("黄宗羡" in hu["ocr_internal_warning"] and "黄宗羲" in hu["ocr_internal_warning"],"OCR risk must be explicit")
    assert len(e["explicit_conflicts"])==3
    conflicts={x["id"]:x for x in e["explicit_conflicts"]}
    require(set(conflicts)=={"13KE-POLARITY-GAIN","13KE-INDEX-167","13KE-TAIL-50"},"missing conflict")
    require(conflicts["13KE-POLARITY-GAIN"]["historical_ocr_or_print_error_finalized"] is False,"unsupported historical scribal error adjudication")
    require(conflicts["13KE-INDEX-167"]["independently_attested_original_printed_leaf"] is False,"OCR is not source original")
    require(conflicts["13KE-INDEX-167"]["algorithm_index_proven_from_historic_original"] is False,"mirror original not located")
    require("五秒八十一微" in conflicts["13KE-TAIL-50"]["mingshi_received"] and
            "五十纤" in conflicts["13KE-TAIL-50"]["huang_ocr"],"microplace pair")
    require(len(e["source_acquisition_leads"])==3 and
            all(x["url"].startswith("https://") and x["role"].endswith("NOT_TARGET_FOLIO_VISUALLY_CHECKED") or x["role"].startswith(("SECONDARY_","MODERN_")) for x in e["source_acquisition_leads"]),"bibliographic lead not ancient original vote")
    require(e["comparator_identity"]["G893_digital_object"]=="GK00893_00" and
            e["comparator_identity"]["physical_independent_copy_delta"]==0 and
            e["comparator_identity"]["collated_same_copy_rows"]==15 and
            e["comparator_identity"]["exact_received_mingshi_recurrence_same_copy_rows"]==10,"source copy provenance")
    for key in ("original_witnesses_considered_new","full_historical_numeric_winners_awarded","received_text_transmission_edges_awarded","algorithm_reopens"):
        require(type(e[key]) is int and e[key]==0,"forbidden witness/winner promotion "+key)
    require(e["transmission_impact"].startswith("NONE"),"source grade prevents lineage award")
    return {"result":"PASS","received_text_pairs":2,"contested_loci":3,
            "source_original_pages_added":0,"historical_winners":0,"previous_ten_source_row_replay_preserved":True}

def handoff():
    state=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf-8"))
    ledger=json.loads((ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf-8"))
    h=state["historical_audit"]
    require(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==
            h["research_omission_guard"]["reviewed_state_version"],"state/research synchronization")
    require(len(h["current_focus"])==ledger["binding"]["source_focus_count"] and
            h["current_focus"][-1].startswith(ledger["binding"]["latest_research_focus_prefix"]+" "), "current focus")
    issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
    require(issue["next_action"].startswith(ledger["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:"),"current action follows live reviewed research batch")
    require({DOC,DOC.replace(".json",".md")}.issubset(set(issue["source_refs"])),"new source records bound")
    require(any(x.get("revision_id")=="TW-OPEN-0005-13KE-TEXT-SEGREGATION-20261029" for x in issue["history"]),"forward-only revision history")
    require(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and
            state["invariants"]["algorithm_reopen_count"]==0,"product closed")

if __name__=="__main__":
    handoff()
    print(json.dumps(verify(json.loads((ROOT/DOC).read_text(encoding="utf-8"))),ensure_ascii=False))
