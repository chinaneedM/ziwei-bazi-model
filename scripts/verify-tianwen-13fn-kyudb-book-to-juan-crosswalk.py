#!/usr/bin/env python3
"""13FN: official Kyujanggak book-ordinal / work-juan crosswalk without glyph overreach."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13FN-KYUDB-GK5553-BOOK29-V81V83-AND-GK3467-BOOK6-V52-FIRSTPARTY-CROSSWALK-R1.json"
FM="docs/research/TIANWEN-13FM-GK05553-REPLACEMENT-MATERIAL-AND-ORDINAL-TRIPLE-SOURCE-R1.json"
FK="docs/research/TIANWEN-13FK-NCL-P74-D7D8D10-CROSS-PHOTO-FOURFEN-BOUNDED-COLLATION-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p):return json.loads((R/p).read_text(encoding="utf-8"))
def check(e,fm,fk,s,l):
 assert e["schema"]=="TIANWEN-13FN-KYUDB-GK5553-BOOK29-V81V83-AND-GK3467-BOOK6-V52-FIRSTPARTY-CROSSWALK-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["status"]=="FIRSTPARTY_INSTITUTIONAL_TABLE_BOOK_TO_WORK_JUAN_CROSSWALK_NO_ORIGINAL_FOLIO"
 src=e["first_party_source"];a=e["gk5553"];b=e["gk3467"];c=e["scholarly_disagreement"];t=e["historical_firewall"];m=e["impact"];corr=e["forward_only_revision"]
 assert src["institution"]=="Seoul National University Kyujanggak" and "postSeq=10775" in src["url"]
 assert src["source_role"]=="FIRSTPARTY_INSTITUTIONAL_HOLDING_BIBLIOGRAPHY_NOT_ORIGINAL_FOLIO" and src["same_institution_as_13FM_catalogs"]
 assert a["current_item"]=="GK05553_00" and a["repaired_book_to_work_juan"]==[{"book":8,"juan":[19,20,21],"medium":"필사본"},{"book":26,"juan":[73,74],"medium":"필사본"},{"book":29,"juan":[81,82,83],"medium":"필사본"}]
 assert a["catalog_supported_book29_work_juan"]==[81,82,83] and a["microfilm_group_for_book29"]=="M/F74-102-17-4"
 assert a["microfilm_group_book_ordinals"]==[25,26,27,28,29,30,31] and a["item_catalog_heritage_exclusion_books"]==[8,26,29]
 assert a["book29_original_photo_seen"] is False and a["work_juan52_to_physical_book"] is a["exact_juan52_physical_leaf"] is a["NIKH_viewer1056_to_this_physical_copy"] is None
 assert b["shelfmark"]=="奎3467" and b["direct_institutional_book_ordinal_for_work_juan52"]==6 and b["work_juan"]==52
 assert b["separate_physical_copy_from_GK5553"] and b["cannot_identify_NIKH_GK5553_image_as_GK3467_leaf"]
 assert b["physical_juan52_original_leaf"] is None and b["original_leaf_photo_seen"] is False
 assert c["secondary_book_ordinal"]==fm["secondary_article_republication"]["ordinals"][2]==28
 assert c["secondary_work_juan"]==c["secondary_statement_work_juan"] if "secondary_statement_work_juan" in c else c["secondary_work_juan"]==[81,82,83]
 assert c["new_official_same_volume_juan_book_ordinal"]==29 and c["new_official_medium"]=="필사본"
 assert c["journal_pdf_page_image_attested"] is False and c["cannot_assign_cause_to_author_vs_republication_vs_catalog"] is None
 assert corr["prior_batch"]=="13FL" and corr["preserve_prior_13FL_13FM_documents"] and corr["not_a_determination_of_modern_journal_typo"]
 assert t["NLC_D5"]==fk["comparison"]["NLC_day5_vs_NIKH_day5_opposed_source_photo_glyphs"][0]=="四分〇一七二"
 assert t["NIKH_D5"]==fk["comparison"]["NLC_day5_vs_NIKH_day5_opposed_source_photo_glyphs"][1]=="四分五一七二"
 assert t["numeric_D5_winner"] is t["NLC_D9_gutter"] is t["work_juan52_GK5553_physical_book"] is t["source_original_GK3467_juan52_page"] is None
 assert t["work_juan52_GK3467_physical_book"]==6 and t["fourfen_to_chudu_bridge"]=="UNPROVEN"
 assert t["G893_six_numerical_originals"]=="OPEN" and t["D1_D2_D3_D4_D5_D6_D30_numeric_units"] is None
 assert t["older_13EI_claim"]=="RETRACTED" and t["algorithm_reopen"]==0
 assert (m["source_registry_root"],m["source_registry_extensions"],m["source_registry_total"])==(647,114,761)
 assert (m["matrix_total"],m["matrix_audited"],m["genealogy_nodes"],m["genealogy_edges"],m["risk_count"])==(222,222,252,238,11)
 assert all(m[k]==0 for k in ("source_registry_delta","independent_physical_originals_added","original_page_glyphs_added","risk_closures","algorithm_reopens","chart_candidate_collapses"))
 assert m["product"]=="CLOSED" and not e["transmission_impact"]["edges_supported"]
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0] and any(q.startswith("13FN ") for q in s["historical_audit"]["current_focus"])
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 issue=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0" and issue["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
 assert all(any(h.get("revision_id", "").startswith("TW-OPEN-0005-" + t + "-") and "next_action" in h.get("changed_fields", []) for h in issue["history"]) for t in ['13FN'])
 assert {E,E.replace(".json",".md")}.issubset(set(issue["source_refs"]))
 assert any(x.get("revision_id")=="TW-OPEN-0005-13FN-FIRSTPARTY-GK5553-BOOK29-JUAN81-83-GK3467-BOOK6-JUAN52-20261024" for x in issue["history"])
 assert any(q.get("id")=="OMISSIONS-13FN-OFFICIAL-KYUDB-BOOK29-JUAN81-83-GK3467-BOOK6-JUAN52-20261024" for q in l["checkpoint_log"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"] and len(l["issues"])==11
 return True
if __name__=="__main__":
 assert check(load(E),load(FM),load(FK),load(S),load(L))
 print("13FN_PASS_SNU_BOOK29_VOL81_83_AND_DIFFERENT_BOOK6_VOL52_NO_ORIGINAL_GLYPH_OR_ALGO")
