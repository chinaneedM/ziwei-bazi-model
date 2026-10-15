#!/usr/bin/env python3
"""12XC: independent item-specific Tokyo reproducibility / authorization firewall."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12XC-TOKYO-ITEM-SPECIFIC-REPRODUCTION-DOSSIER-R1.json"
WZ="docs/research/MING-DATONG-YEHUOBIAN-12WZ-TOKYO-SEVEN-FIRSTPARTY-RECORDS-AND-IMABORI-LEAF-GATE-R1.json"
XA="docs/research/MING-DATONG-YEHUOBIAN-12XA-TOKYO-SEVEN-ITEM-IMAGE-LINK-BOUNDARY-R1.json"
SN="docs/research/MING-DATONG-YEHUOBIAN-12SN-TOKYO-IOC-REPRODUCTION-SERVICE-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
MANIFEST="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
def read(path):
 return json.loads((ROOT/path).read_text(encoding="utf-8"))
def ck(cond,msg):
 if not cond:raise ValueError(msg)
def validate(r,wz,xa,sn,state,manifest):
 ck(r["schema"]=="TIANWEN-12XC-TOKYO-IOC-ITEM-SPECIFIC-REPRODUCTION-DOSSIER-R1","schema")
 ck(r["parent"]==WZ and r["prior_access_policy"]==SN and r["prior_image_button_check"]==XA,"parent records")
 urls={z["role"]:z["url"] for z in r["official_service_pages"]}
 ck(set(urls)=={"RARE_COPY_APPLICATION","ONSITE_COPY_BOUNDARY","OUTSIDE_READER_ACCESS","RESERVATION_METHOD_2024","FIRST_PARTY_LIBRARY_CONTACT"},"official source roles")
 ck(urls["RARE_COPY_APPLICATION"]==sn["first_party_pages"][0]["url"],"duplicate policy parent")
 ck(urls["ONSITE_COPY_BOUNDARY"]==sn["first_party_pages"][1]["url"],"self-copy policy parent")
 ck(urls["RESERVATION_METHOD_2024"]=="https://www.ioc.u-tokyo.ac.jp/~library/news/reserve/reserve.html","reservation route")
 ck(all(u.startswith("https://www.ioc.u-tokyo.ac.jp/~library/") for u in urls.values()),"official URLs")
 items=r["target_items"]
 ck([z["id"] for z in items]==["9927","90972","103841"],"target order")
 bz={z["id"]:z for z in wz["items"]}
 bx=xa["physical_target_controls"]
 for z in items:
  p=bz[z["id"]]
  ck(z["shelfmark"]==p["shelfmark"] and z["collection"] in ("大木文庫","倉石文庫","今堀文庫"),"source-scoped catalog binding")
  ck(z["physical"]=="UNVERIFIED_ORIGINAL_LEAF" and bx[z["id"]]["source_original_juan20_folio_obtained"] is False,"never promote paper leaf")
 ck(items[0]["item"]==bz["9927"]["ciNiiItem"]=="6403767830" and items[0]["year"]==1827 and items[0]["cinii"]=="BC0492354X","Oki exact identifier")
 ck(items[1]["item"]==bz["90972"]["ciNiiItem"]=="6403148395" and items[1]["year"]==1869 and items[1]["cinii"]=="BB23196128","Kuraishi exact identifier")
 ck(items[2]["year"] is None and items[2]["item"] is None and items[2]["cinii"] is None and bx["103841"]["recorded_missing_juan"]==[21,22],"Imabori unproven volume20")
 passage=r["target_passage"]
 ck(passage["chapter"]=="改造漏刻" and passage["glyph_votes"]==0 and len(passage["four_loci"])==4,"four-locus no-vote rule")
 packet=r["request_package"]
 ck(packet["recipient"]==sn["contact_public"]=="ioclibrary@ioc.u-tokyo.ac.jp","provider public contact")
 ck(len(packet["first_party_question_set"])==5,"specific acquisition questions")
 ck(packet["self_identifying_information_included"] is False,"no user-identifying information")
 for field in ("applicant_name","applicant_institution","applicant_phone","requested_visit_date"):
  ck(packet[field] is None,"personal information submission boundary")
 for field in ("requested_copy_fee_approval","inquiry_submitted","formal_copy_application_submitted","reservation_submitted","staff_reply_received","item_specific_copy_eligibility_confirmed"):
  ck(packet[field] is False,"external action must remain unsubmitted")
 gate=r["evidence_gates"]
 for field in ("no_duplicate_source_registry_entry","no_new_genealogy_node_or_edge","no_algorithm_reopen","personal_postal_copy_not_offered_does_not_prove_institutional_route_unavailable","reservation_or_application_preparation_not_equivalent_to_submission","public_service_policy_not_target_material_available","modern_1959_image_link_not_ancient_original"):
  ck(gate[field] is True,"evidence scope "+field)
 ck(gate["source_issued_original_juan20_page_image_count"]==gate["independently_proven_1827_1869_print_impression_votes"]==0 and gate["exact_page_sha256_recorded"] is False and gate["identified_original_edition_from_page"] is False,"original printed folio absent")
 h=state["historical_audit"];count=r["accounting"]
 ck((count["matrix_rows"],count["matrix_audited"],count["provenance_repairs"])==(h["row_count"],h["audited_row_count"],h["repaired_provenance_metadata_defect_count"])==(222,222,45),"matrix state")
 ck((count["registry_root"],count["registry_extension"],count["registry_union"])==(647,59,706),"frozen current source")
 ck(manifest["combined_source_count"]==h["external_source_registry_total_unique_count"]==706,"current union")
 ck(count["genealogy_nodes"]==252 and count["genealogy_edges"]==238 and count["formal_completed_batches"]==len(h["completed_batches"])==487,"genealogy and formal batches remain unchanged")
 ck(state["invariants"]["confirmed_chart_algorithm_defect_count"]==0 and state["invariants"]["algorithm_reopen_count"]==0 and gate["product"]==state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","chart implementation freeze")
 impact=r["transmission_impact"]
 ck(all(impact[z]==[] for z in ("nodes_added_or_strengthened","edges_supported","edges_revised","edges_rejected_or_unproved")),"not a lineage claim")
 return {"status":"PASS","item_specific_originals":2,"conditional_imabori":1,"source_issued_printed_folios":0,"communications_submitted":0}
def verify():
 return validate(read(REC),read(WZ),read(XA),read(SN),read(STATE),read(MANIFEST))
if __name__=="__main__":
 print(json.dumps(verify(),ensure_ascii=False))
