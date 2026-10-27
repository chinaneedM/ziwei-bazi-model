#!/usr/bin/env python3
"""12ZB recover existing Goryeosa D16 facsimile rather than invent fresh originals."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12ZB-GORYEOSA-CADAL-D16-EXISTING-FACSIMILE-AND-KYUDB-CATALOG-CROSSWALK-R1.json"
FAC="docs/research/GORYEOSA-V52-CADAL-FACSIMILE-CONTROL-READINGS-R1.json"
REG="docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
PRIOR="docs/research/TIANWEN-12ZA-GORYEOSA-OFFICIAL-HANJA-D18-EXTRA-THREE-FORWARD-ERRATUM-R1.json"
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC,FAC,REG,PRIOR,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def need(z,why):
 if not z: raise ValueError(why)
def verify(d,fac,reg,prior,state,ledger):
 need(d["schema"]=="TIANWEN-12ZB-EXISTING-GORYEOSA-FACSIMILE-D16-RECOVERY-AND-KYUDB-EDITION-ROUTE-R1","schema")
 p=d["previous_source"];need(p["existing_evidence"]==FAC and p["registry"]==REG and p["source_id"]==fac["source_id"],"exact old source")
 source=next(x for x in reg["sources"] if x["source_id"]==p["source_id"])
 need(p["source_url"]==source["url"] and p["scan_page"]==source["direct_image_control"]["exact_control_pages"]["solar_d16"]==39,"already registered page")
 original=next(x for x in fac["controls"] if x["control_id"]==p["control_id"])
 need(original["scan_page"]==p["scan_page"] and original["direct_surface"]==p["direct_glyph"]=="五分一三六二" and original["normalized_value"]==p["candidate_digit_number"]=="5.1362","old actual image glyph")
 need(fac["copy_level_date_status"]=="NOT_ADJUDICATED" and fac["ocr_used"] is False and p["reading_confidence"]=="HIGH","evidence grade")
 need(p["source_artifact_digest"]==fac["reproduction"]["artifact_digest"] and p["source_artifact_id"]==fac["reproduction"]["artifact_id"],"existing artifact digest not new image")
 need(p["source_workflow_run_id"]==fac["reproduction"]["workflow_run_id"] and p["new_image_acquired_this_batch"] is False and p["reopened_or_newly_registered_ancient_witness_count"]==0,"no fake new original")
 c=d["other_comparison"];need(c["NIKH_web_d16"]=="五分一三六二" and c["G893_original_d16_short_candidate"]=="五分二三六二","original variants distinct")
 need(c["NIKH_d18_five_place_erratum"]==PRIOR and prior["new_hanja_literal_candidate"]["decimal_lexical_five_place"]=="8424.64083","latest correction retained")
 need(c["G893_source_original_complete_control_for_d16"] is False and c["G893_same_column_unit_identity_to_received_goryeosa"]=="UNPROVEN" and c["NIKH_original_image_locus_for_d16"] is False,"original-vs-received bounds")
 im=d["official_image_route"]; need(im["exact_nikh_d16_link_bound_to_specific_book_code"] is False and im["direct_nikh_d16_paper_jpg_bytes_or_sha_acquired"] is False,"no viewer guess")
 catalog=im["catalog_candidates"];need([x["book_cd"] for x in catalog]==["GK03539_00","GK03579_00","GK05553_00"],"catalog candidate keys")
 need(catalog[0]["catalog_medium"]=="木版本" and catalog[0]["catalog_date"]=="[光海君5年(1613)]" and catalog[0]["volumes"]=="139卷85冊","1613 public catalog 3539")
 need(catalog[1]["same_edition_catalog_linked_to_GK03539"] is True and catalog[1]["exact_target_folio_not_read"] is True,"same edition not direct vote")
 need(catalog[2]["catalog_medium"]=="乙亥字" and catalog[2]["catalog_date"]=="[刊年未詳]" and catalog[2]["volume_52_exact_book_location_unbound"] is True,"type copy unknown volume")
 need(all(x["exact_target_folio_not_read"] is True and x["physical_edition_binding_to_NIKH_web"] is False for x in catalog),"catalog-only no target glyph")
 q=d["classification"];need(q["cadal_is_registered_received_physical_page_surrogate"] is True and q["independent_15th_century_print_or_original_from_cadal"] is False,"time scope")
 need(q["independent_stemmatic_original_voting_granted"]==q["new_source_registry_ids"]==q["new_graph_nodes"]==q["new_graph_edges"]==q["runtime_reopens"]==0,"no forged source or lineage")
 need(q["G893_principal_source_original_target_status"]=="5/6" and q["G893_cross_source_mechanical_final"]=="0/6" and q["TW_OPEN_0005"]=="OPEN" and q["total_issues_open"]==11 and q["product_R1"]=="CLOSED","unresolved baseline")
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 need(issue["status"]=="OPEN" and DOC in issue["source_refs"] and DOC.replace(".json",".md") in issue["source_refs"],"registry recovery issue")
 need(issue["g893_12zb_previously_registered_goryeosa_original_recovery"][-1]["old_cadal_scan_page"]==39,"append-only recovery record")
 need(ledger["binding"]["reviewed_state_version"]==state["schema_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"continuity versions")
 need(ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"]) and ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ")[0],"version linkage")
 need(any(x.startswith("12ZB ") for x in state["historical_audit"]["current_focus"]),"new recovery focus")
 need(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==len(ledger["issues"]),"P0 gate")
 return {"status":"PASS","original_cadal_D16":"5.1362","historical_witnesses_added":0,"new_images":0,"issue":"TW-OPEN-0005_OPEN"}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
