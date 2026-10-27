#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-12ZJ-GORYEOSA-5554-13941-NUMBERING-CENSUS-FIREWALL-R1.json"
OLD="docs/research/TIANWEN-12ZI-GORYEOSA-5554-FIRSTPARTY-PARATEXT-COUNT-AND-BOOK52-CLOSURE-GATE-R1.json"
def load():
 return tuple(json.loads((R/p).read_text(encoding="utf-8")) for p in (P,OLD,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def check(c,m):
 if not c:raise ValueError(m)
def verify(d,old,state,ledger):
 check(d["schema"]=="TIANWEN-12ZJ-GORYEOSA-5554-13941-CENSUS-FIREWALL-R1" and d["prior"]==OLD,"identity")
 s=d["source"];a=d["counts"];b=d["boundaries"]
 check(s["academic"]["parts"]==[46,39,2,50,2] and s["academic"]["standard_juan"]==139,"standard whole work")
 check(s["kyudb"]["item"]=="GK05554_00" and s["kyudb"]["books"]==32 and s["kyudb"]["impression"]=="[刊年未詳]" and s["kyudb"]["catalog_preface"].startswith("卷首:進高麗史箋"),"item original scope")
 check(s["heritage"]["claimed_juan"]==98 and not s["heritage"]["detailed_41_missing_original_text_obtained"],"heritage summary grade")
 check(s["reprint"]["kind"]=="SECONDARY_REPUBLICATION" and [s["reprint"][k] for k in ("claimed_full","claimed_missing","claimed_present","enumerated_body")]==[139,41,98,95],"reprint numbers")
 check(s["reprint"]["target52_books_range"]==[6,10] and s["kyudb_other_copy"]["book_count"]==46 and s["kyudb_other_copy"]["manuscript_book_numbers"]==[8,26,29],"copy difference")
 check(old["bounded_received_enumerations"]["third_party_heritage_republication"]["enumerated_numbered_work_volumes"]==95,"immutability")
 check(a["body_total"]==137 and a["catalog_total"]==2 and a["full_standard_total"]==139,"full totals")
 check(a["body_present_received"]==95 and a["body_missing_conditional"]==137-95==42,"body missing")
 check(a["two_catalogs_plus_body_conditional"]==95+2==97 and a["missing_standard_conditional"]==139-97==42,"numbered count")
 check(a["heritage_claimed"]==98 and a["one_numbered_unit_disagreement"]==98-97==1 and not a["claimed_missing_41_is_independent_folio_census"],"no fake 41 witness")
 check(a["one_unnumbered_preface_plus97_conditional"]==98 and not a["that_preface_in_standard_139"],"scope not shared")
 check(a["spine43_minus_surviving32"]==11 and not a["proven_lost_11_original_books"],"spine")
 check(a["possible_other_copy_43_printed_plus3_manuscripts"]==46 and not a["other_copy_43_printed_proven"],"different 5553")
 check(all(b[k] is None for k in ("exact_5554_work52_physical_book","glyph_5554_d16","glyph_5554_d18","original_page_sha256")) and not b["original_1482_impression_proved"],"no original")
 check(all(b[k]==0 for k in ("new_originals","new_source_registry","new_genealogy_edges","new_physical_votes","algorithm_reopens")),"no false witness")
 check((b["g893_original"],b["g893_crossoriginal"],b["open_issues"],b["product"])==("5/6","0/6",11,"CLOSED"),"invariants")
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 check(issue["status"]=="OPEN" and P in issue["source_refs"] and P.replace(".json",".md") in issue["source_refs"],"open issue")
 f=state["historical_audit"]["current_focus"]
 check(any(x.startswith("12ZJ ") for x in f) and ledger["binding"]["latest_research_focus_prefix"]==f[-1].split(" ",1)[0] and ledger["binding"]["source_focus_count"]==len(f),"forward sync")
 check(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"version")
 check(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])=={x["id"] for x in ledger["issues"]},"checkpoint")
 return {"status":"PASS","conditional_numbered":97,"one_unit_unresolved":1,"new_originals":0}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
