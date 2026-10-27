#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-12ZM-SNU-GORYEOSA-5553-81-83-3467-52-TRIANGULAR-SOURCE-SCOPE-R1.json"
PRIOR="docs/research/TIANWEN-12ZL-GORYEOSA-1972-MIXED-FACSIMILE-AND-5553-SUPPLEMENT-CONFLICT-R1.json"
def load():
 return tuple(json.loads((R/p).read_text(encoding="utf-8")) for p in (P,PRIOR,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def check(v,why):
 if not v:raise ValueError(why)
def verify(d,old,state,ledger):
 check(d["schema"]=="TIANWEN-12ZM-SNU-GORYEOSA-81-83-AND-WORK52-COPY-TRIANGLE-R1" and d["prior"]==PRIOR,"identity")
 s=d["source"];tri=d["three_way_replay"];b=d["boundaries"]
 f=s["first_party_snu_guide"];rows=f["rows"]
 check(f["kind"]=="FIRST_PARTY_INSTITUTIONAL_EXPOSITORY_HOLDINGS_TABLE_NOT_NATIVE_BOOK_GLYPH" and not f["no_image_object_acquired"]==False,"no physical source promotion")
 check([(r["copy"],r["book"],r["work_volumes"]) for r in rows[:4]]==[("奎 5553",8,[19,20,21]),("奎 5553",26,[73,74]),("奎 5553",29,[81,82,83]),("奎 3467",6,[52])],"official table copy-book-volume mapping")
 check(rows[4]["copy"]=="奎 5554" and rows[4]["surviving_books"]==32,"5554 source scope")
 check(s["first_party_snu_5553_catalog"]["manuscript_book_numbers"]==[8,26,29],"catalog matches institutional overview")
 check(s["secondary_heritage_description"]["source_class"]=="SECONDARY_REPUBLICATION" and s["secondary_heritage_description"]["manuscript_books"]==[8,12,26] and not s["secondary_heritage_description"]["native_first_party_heritage_full_paragraph_reaccessed"],"contrary secondary source not primary")
 check(s["modern_1972_scholarly_paper"]["woodblock_substituted"]==[19,20,21,31,73,74,77,78,79,81,82,83],"1972 specific substitution list")
 check(tri["snu_5553_ms_29"]==[81,82,83] and tri["secondary_5554_81_82"]==tri["modern_1972_woodblock_81_82"]==tri["overlap"]==[81,82],"81 82 paper-copy test coordinate")
 check(tri["interpretation"]=="DIFFERENT_COPY_AND_EDITION_LAYERS_OVERLAP_IN_WORK_VOLUME_IDENTIFIERS_NOT_IN_PHYSICAL_PAGE_PROVENANCE" and tri["same_book_count_not_equivalent_edition"],"physical-layer firewall")
 check(tri["snu_5553_books"]==[8,26,29] and tri["secondary_description_books"]==[8,12,26] and tri["disagreement"]==[12,29],"unresolved supplements")
 v=tri["eligible_vol52_separate_copy_route"]
 check(v["source_copy"]=="奎 3467" and v["work_volume"]==52 and v["physical_book"]==6 and v["copy_specific_catalog_level_only"] and v["printed_target_glyph_unseen"],"do not transfer v52 to 5554")
 check(tri["k5554_exact_work52_book_still_unknown"] and tri["original_g893_numeric_mechanics_not_extended"],"unbound original")
 for k in ("direct_5553_book29_native_scan_sha256","direct_5554_81_82_native_scan_sha256","direct_3467_book6_original_52_native_scan_sha256","direct_5554_work52_native_scan_sha256","direct_5554_d16_glyph","direct_5554_d18_glyph"):
  check(b[k] is None,"no original pixel "+k)
 check(not b["full_firstparty_heritage_designation_text_read"] and not b["manuscript_12_vs29_physical_correction_resolved"],"no false heritage closure")
 for k in ("independent_old_original_page_votes_added","new_source_registry_records","new_graph_nodes","new_graph_edges","algorithm_reopens"):
  check(b[k]==0,"no invented witness "+k)
 check((b["open_issues"],b["g893_source_local"],b["g893_cross_independent_original"],b["product_r1"])==(11,"5/6","0/6","CLOSED") and d["transmission_impact"]=="NONE","core scope")
 check(old["open_originals"]["gk5554_d16_image"] is None,"prior remains immutable")
 issue=next(z for z in ledger["issues"] if z["id"]=="TW-OPEN-0005")
 check(issue["status"]=="OPEN" and P in issue["source_refs"] and P.replace(".json",".md") in issue["source_refs"],"ledger source refs")
 foc=state["historical_audit"]["current_focus"]
 check(any(z.startswith("12ZM ") for z in foc) and ledger["binding"]["source_focus_count"]==len(foc) and ledger["binding"]["latest_research_focus_prefix"]==foc[-1].split(" ",1)[0],"focus sync")
 check(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"review version")
 check(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])=={z["id"] for z in ledger["issues"]},"issue sweep")
 return {"status":"PASS","new_original_votes":0,"open_issues":11,"work52_source_copy":"奎 3467"}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
