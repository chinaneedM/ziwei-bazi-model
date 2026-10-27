#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-12ZN-GORYEOSA-GK3467-COMPOSITE-SUBRECORD-MICROFILM-IDENTITY-R1.json"
PRIOR="docs/research/TIANWEN-12ZM-SNU-GORYEOSA-5553-81-83-3467-52-TRIANGULAR-SOURCE-SCOPE-R1.json"
def load():
 return tuple(json.loads((R/p).read_text(encoding="utf-8")) for p in (P,PRIOR,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def check(x,msg):
 if not x:raise ValueError(msg)
def verify(d,prev,state,ledger):
 check(d["schema"]=="TIANWEN-12ZN-GORYEOSA-GK3467-MIXED-COPY-AND-SUBRECORD-SCOPE-R1" and d["prior"]==PRIOR,"new evidence identity")
 f=d["first_party"];a=d["arithmetic"];u=d["unresolved"]
 group=f["holdings_curated_table"];desc=f["separate_snu_catalog_expository_note"]
 check(group["entity"]=="奎3467 (combined group)" and group["total_physical_books"]==30 and group["book6"]=={"book":6,"work_volume":52,"reported_medium":"乙亥字"} and group["individual_suffix_identity_for_book6"] is None,"3467 work52 only group-level")
 check(desc["kind"]=="FIRST_PARTY_EXPOSITORY_CROSS_ITEM_DESCRIPTION_NOT_3467_NATIVE_IMAGE" and desc["page_is_about"].startswith("奎3269"),"cross-item explanation scope")
 check(desc["manuscript_book_numbers"]==[1] and desc["eulhae_type_book_numbers"]==[6,26,27,28,29,30] and desc["remaining_woodblock_book_count"]==23 and desc["stated_total_book_count"]==30,"30-book source descriptions")
 lst=f["separate_list"]
 check(lst["entry_3467_2"]["category"]==lst["entry_3467_4"]["category"]=="乙亥字" and lst["entry_3467_1"]["category"]=="木版本" and lst["entry_3467_3"]["category"]=="筆寫本" and lst["direct_book6_to_suffix_map"] is None,"do not invent subclass map")
 c2=f["item_3467_2"];c4=f["item_3467_4"]
 check(c2["call_number"]=="奎3467의2" and c2["listed_books"]==5 and c2["heading_medium"]=="乙亥字" and "第9冊(1冊)木板本" in c2["shared_copy_note"],"child2 source paradox retained")
 check(c4["call_number"]=="奎3467의4" and c4["listed_books"]==1 and c4["heading_medium"]=="乙亥字","child4 source")
 check(c2["microfilm_ids"]==c4["microfilm_ids"]==["M/F82-16-206-1","M/F82-166-206-2"] and c2["work_toc_generic_50_52"] and c4["work_toc_generic_50_52"],"reuse shared refs not two votes")
 for child in (c2,c4):
  check(child["book6_physical_image_identifier"] is None and child["per_book_work52_glyph"] is None,"no child original promotion")
 check((a["group_manuscript_book_count"],a["group_eulhae_book_count"],a["group_woodblock_book_count"],a["group_census_sum"])==(1,6,23,30) and a["group_census_sum"]==1+6+23,"census")
 check(a["child_2_book_count"]==5 and a["child_4_book_count"]==1 and a["children_simple_sum"]==6,"children sizes")
 for k in ("sum_of_child_catalog_books_is_not_proof_of_which_books_are_eulhae","child_2_heading_eulhae_does_not_override_book9_woodblock_exception","shared_microfilm_ids_not_independent_originals","official_group_book6_work52_catalog_target_supported","twelve_zi_isolation_no_runtime_change"):
  check(a[k] is True,"required caution "+k)
 check(a["subrecord_physical_book6_edition_mapping_supported"] is False,"false item binding")
 for k in ("gk3467_book6_exact_subrecord","gk3467_original_work52_image_sha256","gk3467_original_d16_glyph","gk3467_original_d18_glyph","gk5554_book_containing_work52","gk5554_original_work52_image_sha256","gk5554_original_d16_glyph","gk5554_original_d18_glyph"):
  check(u[k] is None,"missing original cannot be filled "+k)
 for k in ("duplicate_microfilm_independent_original_votes","new_original_source_witness_votes","new_registry_sources","new_genealogy_edges","algorithm_reopens"):
  check(u[k]==0,"no forged witness "+k)
 check((u["open_research_issues"],u["g893_direct_source_target"],u["g893_cross_independent_original"],u["chart_product"])==(11,"5/6","0/6","CLOSED") and d["transmission_impact"]=="NONE","study invariants")
 check(prev["boundaries"]["direct_3467_book6_original_52_native_scan_sha256"] is None,"prior no native glyph")
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 check(issue["status"]=="OPEN" and P in issue["source_refs"] and P.replace(".json",".md") in issue["source_refs"],"P0 continuity")
 fcs=state["historical_audit"]["current_focus"]
 check(any(x.startswith("12ZN ") for x in fcs) and ledger["binding"]["source_focus_count"]==len(fcs) and ledger["binding"]["latest_research_focus_prefix"]==fcs[-1].split(" ",1)[0],"focus count")
 check(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"state sync")
 check(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])=={x["id"] for x in ledger["issues"]},"all11 reviewed")
 return {"status":"PASS","copy_scope":"3467 group only","new_originals":0,"open_issues":11}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
