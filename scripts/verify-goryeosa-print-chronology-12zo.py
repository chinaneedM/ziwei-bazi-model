#!/usr/bin/env python3
"""12ZO source-scope guard: edition chronology is not a physical D16/D18 witness."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-12ZO-GORYEOSA-PRINT-CHRONOLOGY-LAYER-FIREWALL-R1.json"
PRIOR="docs/research/TIANWEN-12ZN-GORYEOSA-GK3467-COMPOSITE-SUBRECORD-MICROFILM-IDENTITY-R1.json"
def load():
    return tuple(json.loads((R/p).read_text(encoding="utf-8")) for p in (P,PRIOR,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def check(flag,label):
    if not flag: raise ValueError(label)
def verify(d, prior, state, ledger):
    check(d["schema"]=="TIANWEN-12ZO-GORYEOSA-PRINT-CHRONOLOGY-SOURCE-SCOPE-R1" and d["prior"]==PRIOR, "identity")
    s=d["sources"]; c=d["contradiction"]; f=d["date_firewall"]; u=d["unresolved"]
    a=s["royal_annals_1452_order"]
    check(a["calendar_date"]=="1452-11-28" and "春秋館啓請印《高麗史》, 從之。"==a["text"],"annals wording")
    check(a["action"]=="REQUEST_AND_APPROVAL_TO_PRINT" and a["completed_print_attested"] is False and a["extant_copy_identified"] is False,"order not print")
    b=s["nikh_history_educational_essay"];k=s["kci_2014_abstract"]
    check(b["goryeosa_publication_claim"]=="1452-11" and b["goryeosa_jeolyo_publication_claim"]=="1453-04","institution history distinction")
    check(k["year"]==2014 and k["doi"]=="10.17842/jsa.2014..59.145" and k["first_print_claim"]=="1453-04_BOTH_GORYEOSA_AND_JEOLYO","scholarship provenance")
    check(k["first_print_gapinja"]=="HYPOTHESIS_NOT_SURVIVING_COPY_IDENTIFICATION" and k["original_full_text_reviewed"] is False,"first print conjecture")
    check(k["eulhae_print_date_claim"]=="1475_late_to_1476_early" and k["woodblock_recut_interval"]=="1610_late_to_1613_before_September","secondary era scoped")
    check(c["disagreement_is_real_at_interpretation_layer"] is True and c["resolution"].startswith("UNRESOLVED") and c["primary_1452_record_says_completed_publication"] is False,"retain contradiction")
    check(c["prevent_1452_order_from_becoming_completed_impression"] is True and c["prevent_1453_scholarly_date_from_overwriting_1452_institutional_history"] is True,"no silent winner")
    check(s["snu_gk05554_catalog"]["impression_date"]=="[刊年未詳]" and s["snu_gk05554_catalog"]["work52_original_folio_verified"] is False,"5554 physical date unbound")
    check(s["snu_gk03579_catalog"]["catalog_print_date"]=="[光海君5年(1613)]" and s["snu_gk03579_catalog"]["work52_d16_d18_original_folio_verified"] is False,"1613 target unbound")
    check("UNDETERMINED" in f["gk05554_individual_copy_impression"] and "UNBOUND" in f["gk3467_group_book6_edition_or_impression"],"copy chronology gate")
    check(len(d["forbidden_transfers"])==6 and "1453_or_1475_1476_to_GK05554_print_date" in d["forbidden_transfers"],"transfer firewall")
    check(all(u[x] is None for x in ("first_print_1452_vs_1453_event_reconciliation","gk05554_original_work52_d16_d18_image_sha256","gk3467_book6_exact_subrecord","gk3467_original_work52_d16_d18_image_sha256")),"unresolved targets")
    check(all(u[x]==0 for x in ("new_original_target_glyphs","new_independent_physical_witness_votes","new_genealogy_edges","new_registry_sources","algorithm_reopens")),"no invented originals")
    check((u["open_research_issues"],u["g893_direct_original_controls"],u["g893_cross_independent_original_controls"],u["product"])==(11,"5/6","0/6","CLOSED"),"research invariants")
    check(prior["unresolved"]["gk3467_book6_exact_subrecord"] is None and prior["unresolved"]["new_original_source_witness_votes"]==0,"previous evidence preserved")
    issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
    check(issue["priority"]=="P0" and issue["status"]=="OPEN" and P in issue["source_refs"] and P.replace(".json",".md") in issue["source_refs"],"P0 ledger binding")
    focus=state["historical_audit"]["current_focus"]
    check(any(x.startswith("12ZO ") for x in focus) and ledger["binding"]["source_focus_count"]==len(focus) and ledger["binding"]["latest_research_focus_prefix"]==focus[-1].split(" ",1)[0],"focus coverage")
    check(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"state ledger sync")
    check(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])=={x["id"] for x in ledger["issues"]},"all open reviewed")
    return {"status":"PASS","publication_interpretation_conflict":"OPEN","new_target_originals":0,"open_issues":11}
if __name__=="__main__":
    print(json.dumps(verify(*load()),ensure_ascii=False))
