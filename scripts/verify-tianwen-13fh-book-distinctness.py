#!/usr/bin/env python3
"""13FH: prevent transferring a 75-book woodblock object's ordinal into a 46-book type item."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13FH-GK5553-FORTYSIX-VS-DONGA-SEVENTYFIVE-BOOK-SCOPE-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def get(p):return json.loads((R/p).read_text(encoding="utf8"))
def check(x,s,l):
 assert x["schema"]=="TIANWEN-13FH-GK5553-FORTYSIX-VS-DONGA-SEVENTYFIVE-BOOK-SCOPE-R1"
 assert x["issue_id"]=="TW-OPEN-0005" and x["issue_status"]=="OPEN"
 a=x["first_party_target_catalog"];b=x["distinct_independent_comparator"];c=x["exact_actions_13fh_access_snapshot"];q=x["previous_13fg_snapshot_scope_reinterpretation"];m=x["no_reopen"]
 assert a["item_identifier"]=="GK05553_00" and a["work_juan_count"]==139 and a["physical_book_count"]==46
 assert a["writing_print_designation"]=="乙亥字" and a["edition_impression_year"] is None
 assert a["replacement_handwritten_books"]==a["treasure_excluded_books"]==[8,26,29]
 assert [(v["physical_book_start"],v["physical_book_end"]) for v in a["mifilms"]]==[(1,9),(10,16),(17,24),(25,31),(32,38),(39,43),(44,46)]
 assert a["exact_physical_book_containing_work_juan_52"] is a["folio_number_of_NIKH_kr_052_1056"] is None
 assert a["original_image_source_book_is_one_of_8_26_29"] is None and a["any_juan_book_number_equation_proven"] is False
 assert b["official_record"]=="Treasure 2115-4" and b["physical_book_count"]==75 and b["work_juan_count"]==139
 assert "Woodblock" in b["material"] and b["this_is_SNU_GK05553_00"] is False and b["same_book_ordinal_as_SNU_46_book_holding_proven"] is False
 assert b["photographic_D5_original_from_comparator_acquired"] is False and b["original_D5_glyph_value"] is None
 assert c["run_id"]==40060373115 and c["artifact_id"]==12546194844 and c["observed_status"]=="TRANSPORT_ERROR" and c["exception_type"]=="URLError"
 assert c["source_http"] is c["source_sha256"] is None and c["source_bytes"]==0
 assert c["no_source_raw_html_acquired_this_action"] and c["site_absent_in_all_environments_implied"] is False
 assert q["previous_value"]==1 and q["distinct_physically_authenticated_book_leaf_bindings_observed"]==0
 assert q["gallery_assumed_physical_witnesses_NOT_19"] and q["certified_distinct_original_edition_variants"]==0
 assert q["NIKH_saved_day5_reading"]=="四分五一七二" and q["NLC_p74_original_day5_reading"]=="四分〇一七二"
 assert q["day5_historical_numeric_value"] is None
 assert m["external_registry_root_sources"]==647 and m["external_registry_extension_sources"]==114 and m["external_registry_unique_sources"]==761
 assert m["matrix_rows"]==m["audited_rows"]==222 and m["genealogy_nodes"]==252 and m["genealogy_edges"]==238
 assert m["research_risks_open_or_blocked"]==11 and m["P0_issues_still_open"] and m["product"]=="CLOSED"
 assert all(m[k]==0 for k in ("algorithm_reopens","source_registry_delta","source_new_original_glyph_votes","physical_book_witnesses_authenticated_delta","genealogy_edges_added"))
 assert m["previous_13EI_false_claim"]=="RETRACTED" and m["missing_G893_original_six_controls"]=="OPEN"
 assert x["transmission_impact"]["new_supported_edges"]==[] and x["transmission_impact"]["distinct_editions_not_collapsed"]
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"].startswith("13") and any(z.startswith("13FH ") for z in s["historical_audit"]["current_focus"])
 issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0" and issue["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
 assert {P,P.replace(".json",".md")}.issubset(set(issue["source_refs"]))
 assert any(z.get("revision_id")=="TW-OPEN-0005-13FH-GK5553-46BOOK-VS-DONGA75-AND-PROBE-ACCESS-20261024" for z in issue["history"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"] and len(l["issues"])==11
 return True
if __name__=="__main__":
 assert check(get(P),get(S),get(L))
 print("13FH_PASS_PHYSICAL_BOOK_46_VS_75_NO_TARGET_FOLIO_OR_ALGORITHM_REOPEN")
