#!/usr/bin/env python3
"""12YN verify two true original scanned print witnesses, not two web transcription votes."""
from pathlib import Path
from decimal import Decimal
import json
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YN-NLC1892-MINGSHI-V33-PRINTED-TWO-LOCUS-R1.json"
def need(v,m):
 if not v: raise ValueError(m)
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json"))
def verify(d,ledger,state):
 a=d["source"];left,right=d["target_loci"];comparison=d["cross_source_collation"];s=d["safeguards"]
 need(d["schema"]=="TIANWEN-12YN-NLC1892-MINGSHI-V33-INDEPENDENT-CATALOG-PRINT-ORIGINAL-DUAL-LOCUS-R1" and d["grade"]=="DIRECT_HASH_BOUND_HISTORICAL_SCAN_OF_SEPARATELY_CATALOGUED_PRINT_ITEM","target evidence type")
 need(a["id"]=="NLC892-312002017339-363680" and a["holder"]=="中国国家图书馆" and a["image_pdf_bytes"]==78635564 and a["image_pdf_pages"]==108 and a["pdf_page_index_one_based"]==62,"NLC source identity")
 need(a["image_pdf_sha1"]=="58bc2ae04cf25c0065c301e8daf390fc274e38e3" and a["image_pdf_sha256"]=="938895cee288ce94ff02d17dc7feb3dfd88094f16ac27e6b1fe0404d47089be3","source original exact SHA")
 need(a["scan_page_render_sha256"]=="e1a2c0d19a734e458c20e2b40bf0155a3808b7fb7a2d809b700b168feb2d7360" and a["scan_page_native_render_width"]==2400 and a["scan_page_native_render_height"]==2235,"native original image hash")
 need(a["ocr_used"] is False and a["digitized_spread_not_original_leaf"] is True and a["copied_1739_label_does_not_fix_1892_physical_impression"] is True and a["physical_object_specific_colophon_directly_authenticated"] is False,"four dates firewall")
 need(left["direct_printed_result"]=="一秒八十六微" and right["direct_printed_result"]=="四分九十三秒八十六微","do not rewrite printed source")
 need(left["image_original_pdf_page"]==right["image_original_pdf_page"]==62 and left["ROI_png_page_bbox_xyxy"]==[1710,400,1875,1520] and right["ROI_png_page_bbox_xyxy"]==[1520,400,1700,1520],"direct PDF scope")
 need(left["ROI_rgb_sha256"]=="04be8d16ebd3f46bd06a723fb2cb79e9bd21d4f245ffff4175eb50765be9a3ac" and right["ROI_rgb_sha256"]=="3a9a5cbdfab51d7266c6412eac001072ed6b77bd12e1641ebe017cfbcf544a42","original RGB hash")
 need(right["ROI_png_page_bbox_xyxy"][2]<left["ROI_png_page_bbox_xyxy"][0],"two source crops must not overlap")
 need(comparison["cadal_12ym"]["first"]=="一秒三十六微" and comparison["cadal_12ym"]["final"]=="四分九十三秒八十六微","12YM primary source must be retained")
 need(comparison["nlc_12yn"]["first"]==left["direct_printed_result"] and comparison["nlc_12yn"]["final"]==right["direct_printed_result"],"12YN source-print cross comparison")
 need(comparison["first_result_disagrees_by_micro"]==50 and comparison["final_result_matches"] is True and comparison["independent_stemmatic_origin_or_direct_copy_proven"] is False and comparison["copying_cause"]=="UNVERIFIED","do not overstate stemmatic")
 need(Decimal("0.0031")*6==Decimal("0.0186") and Decimal("4.9200")+Decimal("0.0186")==Decimal("4.9386") and Decimal("0.0186")-Decimal("0.0136")==Decimal("0.0050"),"historical arithmetics")
 need(s["new_original_print_item_compared"]==1 and s["original_digital_item_cross_comparison"]==2 and s["new_independent_stemmatic_root_awarded"]==s["new_genealogy_edges"]==s["new_algorithm_reopens"]==0,"false branch or algorithm decision")
 need(s["remaining_g893_formal_original_fields"]=="5/6" and s["g893_cross_edition_mechanical_final"]=="0/6" and s["research_omission_open_count"]==11 and s["chart_product"]=="CLOSED","false G893 closure")
 issue=next(y for y in ledger["issues"] if y["id"]=="TW-OPEN-0005")
 need(issue["status"]=="OPEN" and DOC in issue["source_refs"] and DOC.replace(".json",".md") in issue["source_refs"],"missing evidence-bound omission")
 evidence=issue["mingshi_12yn_nlc1892_independent_original_reviews"]
 need(len(evidence)==1 and evidence[0]["source_sha256"]==a["image_pdf_sha256"] and evidence[0]["original_pdf_page"]==62 and evidence[0]["stemmatic_root_awarded"]==0,"issue evidence mismatch")
 need(ledger["binding"]["latest_research_focus_prefix"]=="12YN" and state["historical_audit"]["current_focus"][-1].startswith("12YN "),"latest scope")
 need(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,state["schema_version"].split(".")))>=(1,628,0),"research continuity state")
 need(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==len(ledger["issues"]),"11 item oversight not reviewed")
 need(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"chart reopen forbidden")
 return {"status":"PASS","two_print_objects":2,"first_locus_micro_gap":50,"printed_sum_matches":True,"independent_stemmatic_roots_proven":0}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
