#!/usr/bin/env python3
"""12ZP: keep printing permission, fulfilled printing, distribution and old draft separate."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-12ZP-GORYEOSA-1452-1454-1482-ROYAL-ANNALS-PRINT-STATE-COLLATION-R1.json"
SHARD="docs/research/TIANWEN-12ZP-GORYEOSA-ROYAL-ANNALS-SOURCE-SHARD-R1.json"
def load():
    return tuple(json.loads((R/p).read_text(encoding="utf-8")) for p in (P,SHARD,"docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json","docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def ck(condition,name):
    if not condition:raise ValueError(name)
def verify(d,shard,manifest,state,ledger):
    ck(d["schema"]=="TIANWEN-12ZP-GORYEOSA-ROYAL-ANNALS-PRINT-STATE-COLLATION-R1" and d["issue_id"]=="TW-OPEN-0005","evidence scope")
    ck(d["transcription_grade"].startswith("FIRST_PARTY_NIKH_RECEIVED_DIGITAL_TRANSCRIPTION"),"digital not original")
    e={x["key"]:x for x in d["events"]}
    ck(len(e)==4 and len(shard["sources"])==4,"four historical record passages")
    ck(e["jeolyo_offer_1452_02_20"]["event_date"]=="1452-02-20" and "當印而頒之" in e["jeolyo_offer_1452_02_20"]["original_extract"],"Jeolyo proposed")
    ck(e["goryeosa_approval_1452_11_28"]["original_extract"]=="春秋館啓請印《高麗史》, 從之。","approval text")
    ck(e["limited_full_history_1454_10_13"]["event_date"]=="1454-10-13" and "《全史》則少印, 只藏內府" in e["limited_full_history_1454_10_13"]["original_extract"] and "《節要》頒賜" in e["limited_full_history_1454_10_13"]["original_extract"],"1454 limited-vs-distributed")
    ck(e["predecessor_draft_retrospective_1482_02_13"]["event_date"]=="1482-02-13" and "或稱權草、或稱紅衣草、或稱全文" in e["predecessor_draft_retrospective_1482_02_13"]["original_extract"],"draft identity")
    conclusions=d["conclusions"]
    ck(conclusions["chronology_dispute_1452_vs_1453"].startswith("STILL_UNRESOLVED"),"1452 vs1453 dispute open")
    ck("NOT_1451_FINAL" in conclusions["1482_memorial_predecessor_state"],"prior draft not final")
    ck("NOT_COMPLETION" in conclusions["1452_nov_goryeosa_state"],"approval != completed")
    ck("SEPARATE_NEW_APPROVAL" in conclusions["1454_oct_full_goryeosa_state"],"1454 newly approved not completed")
    ck(all(e1["url"].startswith("https://sillok.history.go.kr/id/") for e1 in d["events"]),"annals records")
    a=d["witness_delta"]
    for k in ("new_ancient_original_physical_copies","new_work52_native_image_pages","new_work52_d16_d18_glyph_votes","new_genealogy_nodes","new_genealogy_edges","algorithm_reopens"):
        ck(a[k]==0,"no physical original or algorithm promotion: "+k)
    ck((a["registered_official_digital_annals_passages"],a["remaining_open_research_issues"],a["g893_principal_direct_controls"],a["g893_cross_independent_original"],a["chart_product"])==(4,11,"5/6","0/6","CLOSED"),"scope invariants")
    ids={x["source_id"] for x in shard["sources"]}
    ck(ids=={x["source_id"] for x in e.values()} and all(x["physical_glyph_authority"] is False and x["verification_status"]=="RECEIVED_TEXT_VERIFIED" and x["evidence"]==P for x in shard["sources"]),"source shard failclosed")
    spec=[x for x in manifest["shards"] if x["path"]==SHARD]
    ck(len(spec)==1 and spec[0]["source_count"]==4 and (manifest["root_source_count"],manifest["extension_source_count"],manifest["combined_source_count"])==(647,63,710),"registered counts")
    focus=state["historical_audit"]["current_focus"]
    ck(any(x.startswith("12ZP ") for x in focus),"12ZP focus")
    ck((state["historical_audit"]["external_source_registry_extension_count"],state["historical_audit"]["external_source_registry_total_unique_count"])==(63,710),"state source count")
    ck(ledger["binding"]["source_focus_count"]==len(focus) and ledger["binding"]["latest_research_focus_prefix"]==focus[-1].split(" ",1)[0],"ledger focus")
    ck(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"state sync")
    issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
    ck(issue["status"]=="OPEN" and all(p in issue["source_refs"] for p in (P,P.replace(".json",".md"),SHARD)),"P0 scope")
    ck(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])=={x["id"] for x in ledger["issues"]},"all 11")
    return {"status":"PASS","new_annals_sources":4,"new_physical_originals":0,"open_issues":11}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
