#!/usr/bin/env python3
"""13FM official manuscript vs derivative woodblock repair-scope firewall."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13FM-GK05553-REPLACEMENT-MATERIAL-AND-ORDINAL-TRIPLE-SOURCE-R1.json"
FL="docs/research/TIANWEN-13FL-GK05553-REPLACEMENT-BOOK-ORDINAL-28-29-SOURCE-SCOPE-R1.json"
FK="docs/research/TIANWEN-13FK-NCL-P74-D7D8D10-CROSS-PHOTO-FOURFEN-BOUNDED-COLLATION-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def read(p):return json.loads((R/p).read_text(encoding="utf-8"))
def check(e,fl,fk,s,l):
 assert e["schema"]=="TIANWEN-13FM-GK05553-REPLACEMENT-MATERIAL-AND-ORDINAL-TRIPLE-SOURCE-R1" and e["issue_id"]=="TW-OPEN-0005"
 x=e["first_party_same_holding_two_descriptions"];a=x["source_1"];b=x["source_2"];c=e["secondary_article_republication"];d=e["third_republication_heritage_description_lead"];f=e["differentiation"];t=e["chart_and_original_witness_firewall"];im=e["impact"]
 assert a["reported_ordinals"]==b["reported_ordinals"]==fl["first_party_catalog"]["replacement_book_ordinals"]==[8,26,29]
 assert b["source_term"]=="필사본으로 보충하였다" and b["interpreted_media"]=="MANUSCRIPT_SUPPLEMENT"
 assert a["url"]=="https://kyudb.snu.ac.kr/book/view.do?book_cd=GK05553_00"
 assert b["url"]=="https://kyudb.snu.ac.kr/book/view.do?book_cd=GK03269_00&notes=basic"
 assert b["not_an_independent_ancient_original"] and not x["original_book_page_physical_review"]
 assert c["ordinals"]==fl["secondary_scholarship"]["replacement_book_ordinals_from_republished_text"]==[8,26,28]
 assert c["replacement_mechanism_term"]=="木板补写本" and c["direct_original_journal_pdf_target_page_image_verified"] is False
 assert c["original_article_target_page_hash"] is None and c["categorical_woodblock_evidence_independent_of_republication"] is False
 assert d["ordinals"]==[8,12,26] and d["volume_groups"]==["19-21","31-33","73-74"]
 assert d["source_role"]=="TERTIARY_DERIVATIVE_LOCATOR_ONLY_UNVERIFIED_AGAINST_GOVERNMENT_PAGE"
 assert d["heritage_official_original_exact_page_directly_checked"] is False and d["could_be_inventory_numbering_or_typographical_layer"] is None
 assert f["verified_same_ordinal_on_two_first_party_metadata_descriptions"] and f["same_holding_official_descriptions_not_independent_original_votes"]
 assert f["independent_physical_originals_authenticated_here"]==0 and f["no_certified_typo_assignment"] and f["no_certified_direct_printing_media_from_photo"]
 assert f["no_certified_mapping_volume_52_to_physical_book"] and f["no_certified_mapped_KRDB_original_to_specific_SNU_book_leaf"]
 assert t["NLC_13FK_D5"]==fk["comparison"]["NLC_day5_vs_NIKH_day5_opposed_source_photo_glyphs"][0]=="四分〇一七二"
 assert t["NIKH_13FI_D5"]==fk["comparison"]["NLC_day5_vs_NIKH_day5_opposed_source_photo_glyphs"][1]=="四分五一七二"
 assert t["original_D5_numeric_winner"] is t["NLC_13FK_D9_gutter"] is t["NIKH_official_image_1056_to_physical_leaf"] is None
 assert t["fourfen_to_chudu_relation"]=="UNPROVEN" and t["G893_six_original_controls"]=="OPEN" and t["earlier_13EI_discredited"]=="RETRACTED"
 assert im["root_source_count"]==647 and im["extension_source_count"]==114 and im["total_unique_sources"]==761
 assert im["matrix_rows"]==im["matrix_audited"]==222 and im["genealogy_nodes"]==252 and im["genealogy_edges"]==238
 assert im["open_or_blocked_risks"]==len(l["issues"])==11 and im["product"]=="CLOSED"
 assert all(im[key]==0 for key in ("new_source_registry_entries","independent_ancient_physical_witnesses","algorithm_reopens","chart_candidate_collapses"))
 assert not e["transmission_impact"]["edges_supported"] and not e["transmission_impact"]["edges_revised"]
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]=="1.813.0"
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]=="13FM" and s["historical_audit"]["current_focus"][-1].startswith("13FM ")
 issue=next(a for a in l["issues"] if a["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN" and issue["next_action"].startswith("13FM CURRENT ACTION:")
 assert all(p in issue["next_action"] for p in ("8/26/29","8/26/28","8/12/26","filsa","G893","D30","D1 D2 D3 D4 D5 D6","NULL","13EI","四分","初度","GK03539_00","GK03579_00","GK03269_00","GK05554_00"))
 assert {E,E.replace(".json",".md")}.issubset(issue["source_refs"])
 assert any(h.get("revision_id")=="TW-OPEN-0005-13FM-SNU-HANDCOPY-VS-WOODBLOCK-AND-8-12-26-DERIVATIVE-20261024" for h in issue["history"])
 assert l["checkpoint_log"][-1]["id"]=="OMISSIONS-13FM-SNU-HANDCOPY-VS-WOODBLOCK-THREE-ORDINAL-SCOPES-20261024"
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
if __name__=="__main__":
 assert check(read(E),read(FL),read(FK),read(S),read(L))
 print("13FM_PASS_OFFICIAL_HANDCOPY_SECONDARY_WOODBLOCK_THIRD_UNVERIFIED_NO_D5_OR_D9_ORIGINAL_CLAIM")
