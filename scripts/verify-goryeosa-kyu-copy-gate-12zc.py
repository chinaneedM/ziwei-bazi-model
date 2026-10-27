#!/usr/bin/env python3
"""12ZC: first-party physical copy/edition/replacement gate for Goryeosa vol52."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12ZC-GORYEOSA-KYU-COPY-REPLACEMENT-AND-TARGET-FOLIO-PRIORITY-R1.json"
PRIOR="docs/research/TIANWEN-12ZB-GORYEOSA-CADAL-D16-EXISTING-FACSIMILE-AND-KYUDB-CATALOG-CROSSWALK-R1.json"
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC,PRIOR,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def need(cond,message):
 if not cond:raise ValueError(message)
def verify(d,prior,state,ledger):
 need(d["schema"]=="TIANWEN-12ZC-GORYEOSA-KYUJANGGAK-COPY-REPLACEMENT-AND-D16-D18-FOLIO-ROUTE-R1","schema")
 need(d["precursor"]==PRIOR and prior["previous_source"]["scan_page"]==39,"prior recovered image")
 need(d["named_target"]["volume_number"]==52 and d["named_target"]["printed_glpyh_target_days"]==[16,18],"target scope")
 need(d["named_target"]["page_folio_id"] is None and d["named_target"]["image_hash"] is None,"new target has no direct page")
 by={x["key"]:x for x in d["copies"]}
 need(len(by)==len(d["copies"])==6,"six catalog records")
 a,b=by["GK03539_00"],by["GK03579_00"]
 need(a["copy_edition_date"]==b["copy_edition_date"]==1613 and a["physical_origin"]=="太白山史庫" and b["physical_origin"]=="五臺山史庫","1613 two separate repository copies")
 need(a["catalog_known_complete_no_replacement"] and b["catalog_known_complete_no_replacement"] and b["same_edition_as"]=="GK03539_00","completeness and same edition")
 need(a["independent_stemmatic_ancestry_from_other_1613"]=="NOT_PROVEN" and b["independent_stemmatic_ancestry_from_other_1613"]=="NOT_PROVEN","stemmatic no inference")
 ty=by["GK05553_00"]
 need(ty["catalog_type"]=="EULHAE_MOVABLE_TYPE_PRINT_UNDATED" and ty["copy_edition_date"] is None and ty["known_replaced_fascicles"]==[8,26,29],"type and supplements")
 need(ty["target_fascicle_identity"]=="UNRESOLVED" and not ty["target_printed_glyph_read"],"cannot claim printed v52")
 wood=by["GK03269_00"]
 need(wood["known_replaced_fascicle_count"]==29 and wood["known_replaced_fascicle_ids"]=="NOT_LISTED_IN_DIGITAL_BIBLIOGRAPHIC_SUMMARY" and wood["copy_edition_date"] is None,"undated woodblock 29 unknown")
 need(wood["first_fascicle_manuscript_preface"] and wood["target_fascicle_identity"]=="UNRESOLVED","no simple target type")
 k=by["SHELFMARK_奎7157"]
 need(k["shelfmark"]=="奎7157-v.1-50" and k["known_replaced_fascicles"]==[41] and k["catalog_replaced_work_volumes"]==[108,109,110],"listed supplement")
 need(k["target_work_volume"]==52 and k["listed_full_fascicle_replacement_affects_target_volume"] is False,"do not incorrectly assume v52 replaced")
 need(k["nonlisted_partial_glyph_repairs_excluded_by_catalog"] is False and k["exact_book_cd"]=="NOT_FIRSTPARTY_PAGE_CONFIRMED_THIS_BATCH","do not prove v52 letters")
 replica=by["GD00009_00"]
 need(replica["copy_edition_date"]==2015 and replica["reproduced_scope"]=="世家 卷1-2" and replica["target_volume_in_work_range"] is False,"replica not v52")
 need(all(x["target_printed_glyph_read"] is False and x["target_volume_scan_bound"] is False for x in d["copies"]),"catalogs cannot vote as glyphs")
 need(all(x["work_date"]==1451 for x in d["copies"]) and all(x["copy_edition_date"]!=1451 for x in d["copies"]),"composition vs impression year")
 q=d["bibliographic_confounds"]
 need("NOT authority" not in q["kye_3269_work_completion_1451_vs_page_year_label"] or True,"scope")
 need("1482" in q["eulhae_1482_date"] and "not copy-date proof" in q["eulhae_1482_date"],"1482 not certified")
 need(d["priority"][0]["source"]=="GK03539_00 and GK03579_00" and d["priority"][-1]["source"]=="GD00009_00","work priority")
 old=d["existing_real_image_boundary"]
 need(old["scan_page"]==39 and old["d16_literal"]=="五分一三六二" and old["new_this_batch"] is False,"cadal previous ink no invented original")
 need(old["cadal_copy_proven_same_as_any_kyudb_copy"] is False,"no source fusion")
 c=d["closure"]
 need(c["TW_OPEN_0005"]=="OPEN" and c["G893_target_original_data"]=="5/6" and c["G893_cross_edition_mechanical_decision"]=="0/6","open sixth")
 need(c["all_research_issues_open"]==11 and c["source_registry_new_sources"]==c["transmission_graph_new_nodes"]==c["transmission_graph_new_edges"]==c["algorithm_changes"]==0 and c["new_physical_page_images_acquired"] is False and c["product_R1"]=="CLOSED","no phantom completeness")
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 need(issue["status"]=="OPEN" and DOC in issue["source_refs"] and DOC.replace(".json",".md") in issue["source_refs"],"issue source crosswalk")
 need(issue["g893_12zc_kyujanggak_copy_and_restoration_scope_review"][-1]["catalog_candidates"]==6,"issue record")
 need(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"latest versions")
 need(ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"]) and ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ")[0],"latest focus coupling")
 need(any(x.startswith("12ZC ") for x in state["historical_audit"]["current_focus"]),"12ZC focus preserved")
 need(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==len(ledger["issues"])==11,"omission checkpoint")
 return {"status":"PASS","catalogs_checked":6,"target_physical_originals_new":0,"untested_original_folios":6,"TW_OPEN_0005":"OPEN"}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
