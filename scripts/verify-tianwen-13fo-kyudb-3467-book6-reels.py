#!/usr/bin/env python3
"""13FO: copy-scoped first-party GK3467 reel/physical book6 source gate."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13FO-KYUDB-GK3467-BOOK6-EULHAE-SUBCATALOG-MICROFILM-UNBOUND-R1.json"
FN="docs/research/TIANWEN-13FN-KYUDB-GK5553-BOOK29-V81V83-AND-GK3467-BOOK6-V52-FIRSTPARTY-CROSSWALK-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def read(path):return json.loads((ROOT/path).read_text(encoding="utf8"))
def check(e,fn,state,ledger):
 assert e["schema"]=="TIANWEN-13FO-KYUDB-GK3467-BOOK6-EULHAE-SUBCATALOG-MICROFILM-UNBOUND-R1" and e["issue_id"]=="TW-OPEN-0005"
 assert e["status"]=="FIRSTPARTY_CATALOG_BOUNDED_SUBITEM_LEAD_WITHOUT_UNIQUE_VOLUME_BINDING_OR_FOLIO"
 a,b=e["firstparty_holding_3467"]
 assert "postSeq=10775" in a["url"] and a["shelfmark"]=="奎3467" and a["physical_book"]==6 and a["work_juan"]==52
 assert a["book6_in_eulhae_segment"] is True and a["source_original_leaf"] is None
 assert b["url"]=="https://kyudb.snu.ac.kr/book/view.do?book_cd=GK03269_00&notes=basic"
 assert b["original_six_eulhae_books"]==[6,26,27,28,29,30]
 assert b["remaining_23_books"]=="WOODBLOCK" and b["another_first_book"]=="MANUSCRIPT"
 subs=e["candidate_sublibrary_records"]
 assert [x["catalog"] for x in subs]==["GK03467_02","GK03467_04"]
 assert [x["extent"] for x in subs]==["零本5冊","零本1冊"]
 assert all(x["classification"]=="乙亥字" and x["url"].endswith(x["catalog"]) for x in subs)
 reels=["M/F82-16-206-1","M/F82-166-206-2"]
 assert all(x["microfilm_identifiers_verbatim"]==reels and x["specific_book6_in_this_subrecord"] is None for x in subs)
 assert all(x["specific_juan52_in_this_subrecord"] is None and x["physical_page_image_seen"] is False for x in subs)
 v=e["important_microfilm_caveats"]
 assert v["same_two_reel_text_on_both_catalogs"] and v["reel_identifiers_do_not_uniquely_determine_physical_book6"]
 assert v["reel_one_inconsistent_literal_with_reel_two"]==reels and v["do_not_normalize_apparent_digit_variance_without_provider_confirmation"]
 assert v["reel_pdf_page_direct_access_success"] is False and v["reel_media_bytes_sha256"] is v["reel_target_page_sha256"] is None
 f=e["identity_firewall"]
 assert f["cannot_assume_GK03467_02_is_book6"] and f["cannot_assume_GK03467_04_is_book6"]
 assert f["GK3467_book6_vs_GK5553_juan52_physical_book_unknown"]
 assert f["KRDB_NIKH_viewer_kr_052_1056_physical_source"] is f["item_GK05553_00_juan52_book"] is None
 assert f["item_GK05553_00_book29_juan"]==fn["gk5553"]["catalog_supported_book29_work_juan"]==[81,82,83]
 assert f["original_2020_Wei_Chen_PDF_index_result_found"] and f["original_2020_Wei_Chen_PDF_direct_target_page_obtained"] is False
 t=e["historical_control_firewall"]
 assert t["NLC_13FK_D5"]=="四分〇一七二" and t["NIKH_13FI_D5"]=="四分五一七二"
 assert t["D5_winner"] is t["NLC_13FK_D9"] is t["physical_copy_source_for_either_photo"] is None
 assert t["g893_six_original_controls"]=="OPEN" and t["historical_D1_D2_D3_D4_D5_D6_D30_full_units"] is None
 assert t["fourfen_to_chudu_historical_bridge"]=="UNPROVEN" and t["thirteen_EI_claim"]=="RETRACTED"
 impact=e["impact"]
 assert (impact["matrix_total"],impact["matrix_audited"],impact["root_sources"],impact["extension_sources"],impact["total_sources"])==(222,222,647,114,761)
 assert (impact["genealogy_nodes"],impact["genealogy_edges"],impact["omission_issues"])==(252,238,11)
 assert all(impact[z]==0 for z in ("new_external_source_registry_records","new_authenticated_physical_originals","new_historical_source_glyphs","risk_closed","algorithm_reopens","candidate_collapses"))
 assert impact["product"]=="CLOSED" and not e["transmission_impact"]["edges_supported"]
 assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]=="1.815.0"
 assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
 assert ledger["binding"]["latest_research_focus_prefix"]=="13FO" and state["historical_audit"]["current_focus"][-1].startswith("13FO ")
 issue=next(i for i in ledger["issues"] if i["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN" and issue["next_action"].startswith("13FO CURRENT ACTION:")
 assert all(w in issue["next_action"] for w in ("8/26/29","8/26/28","8/12/26","filsa","G893","D30","D1 D2 D3 D4 D5 D6","NULL","13EI","四分","初度","GK03539_00","GK03579_00","GK03269_00","GK05554_00","GK3467","81-83","29","GK03467_02","GK03467_04"))
 assert {E,E.replace(".json",".md")}.issubset(set(issue["source_refs"]))
 assert any(x.get("revision_id")=="TW-OPEN-0005-13FO-GK3467-BOOK6-EULHAE-02-04-REELS-20261024" for x in issue["history"])
 assert ledger["checkpoint_log"][-1]["id"]=="OMISSIONS-13FO-GK3467-BOOK6-EULHAE-02-04-UNBOUND-REELS-20261024"
 assert ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and len(ledger["issues"])==11
 return True
if __name__=="__main__":
 assert check(read(E),read(FN),read(S),read(L))
 print("13FO_PASS_GK3467_BOOK6_EULHAE_UNBOUND_02_04_REELS_AND_ORIGINAL_FOURFEN_GLYPH_NULL")
