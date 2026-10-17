#!/usr/bin/env python3
"""12YM exact full-image source and original print dual-locus evidence admission gate."""
from __future__ import annotations
import json
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YM-MINGSHI-V33-CADAL-DIRECT-ORIGINAL-DUAL-LOCUS-R1.json"
def require(x,msg):
 if not x: raise ValueError(msg)
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json"))
def verify(doc,ledger,state):
 p=doc["provenance"]; a,b=doc["original_two_loci"]; u=doc["arithmetic_check"]; s=doc["safeguards"]
 require(doc["schema"]=="TIANWEN-12YM-MINGSHI-V33-DIRECT-ORIGINAL-DUAL-LOCUS-EVIDENCE-R1" and doc["research_grade"]=="DIRECT_SINGLE_DIGITIZED_IMPRINT_IMAGE_TWO_LOCUS_GLYPH_READING_NO_PHYSICAL_EDITION_CERTIFICATION","no false evidence grade")
 require(p["source_catalog_id"]=="CADAL06056955" and p["exact_djvu_byte_size"]==6001348 and p["sha1"]=="903ac33c6409ff95a5eff64c19b6eacd90f41a5e" and p["sha256"]=="0afffc8f8cf692d43e3da3b038dfe75324ce79053aff892b5687d50b70254362" and p["full_image_page_count_replayed"]==168,"original byte evidence mismatch")
 require(p["ocr_used"] is False and p["native_image_djvu_page_number_one_based"]==58 and p["native_rendered_image_dimensions_px"]==[2376,3117] and p["native_page_058_png_sha256"]=="d87819a7c9a0b6668a5b7f53db7ee6eb1d17c3913464648353dac6fc896e9428","original page pixel evidence mismatch")
 require(p["source_origin_physical_impression_date"]=="UNVERIFIED" and p["physical_copy_item_id"]=="UNVERIFIED" and p["catalog_published_year_1739_is_physical_imprint_date"] is False and p["folio_number_in_source"]=="NOT_INDEPENDENTLY_CERTIFIED_DIGITIZED_PAGE_ONLY","do not infer print date or original folio")
 require(a["target_glyph"]=="一秒三十六微" and b["target_glyph"]=="四分九十三秒八十六微" and a["printed_decimal_candidate"]=="0.0136" and b["printed_decimal_candidate"]=="4.9386","actual original printed glyphs must not be silently corrected")
 require(a["region"]["png_pixel_crop_xyxy"]==[1400,290,1905,2910] and b["region"]["png_pixel_crop_xyxy"]==[895,290,1395,2910] and a["region"]["rgb_pixel_sha256"]=="051a4e280b7177e9aa250cde1bc6aebf6bc82ae6e28a563853e06f08de762e1e" and b["region"]["rgb_pixel_sha256"]=="105420e6317defc6487ba311dc15fc3abd5c0152e356ddf14d4f337bbecd3ae9","ROI glyph provenance mismatched")
 require(a["region"]["png_pixel_crop_xyxy"][0]>b["region"]["png_pixel_crop_xyxy"][2],"ROI overlap disallowed")
 expected_mid=Decimal(31)*Decimal("0.0001")*Decimal(6)
 expected_sum=Decimal("4.9200")+expected_mid
 implied_sum=Decimal("4.9200")+Decimal(a["printed_decimal_candidate"])
 require(expected_mid==Decimal("0.0186") and expected_sum==Decimal(b["printed_decimal_candidate"]) and (expected_sum-implied_sum)==Decimal("0.0050"),"two-locus local numerical conflict proof")
 require(u["internal_gap_wei"]==50,"printed 50 micro-unit gap changed")
 require(doc["received_text_comparison"]["exact_scanned_imprint_supports_siku_labeled_two_locus_strings"] is True and doc["received_text_comparison"]["does_not_prove_siku_received_text_physical_base_identity"] is True,"received text source-fingerprint nonpromotion")
 require(all(s[x]==0 for x in ("new_independent_physical_impressions_awarded","new_genealogy_edges","new_source_registry_entries","algorithm_reopens")) and s["new_direct_original_target_loci"]==2,"unsupported original vote or algorithm reopen")
 require(s["g893_original_principal_field_count"]=="5/6" and s["g893_cross_witness_final"]=="0/6" and s["open_omission_issues"]==11 and s["deterministic_product"]=="CLOSED","false chart closure")
 issue=next(i for i in ledger["issues"] if i["id"]=="TW-OPEN-0005")
 require(issue["status"]=="OPEN" and DOC in issue["source_refs"] and DOC.replace(".json",".md") in issue["source_refs"],"TW-OPEN-0005 must persist")
 reviews=issue["mingshi_12ym_original_dual_locus_reviews"]
 require(len(reviews)==1 and reviews[0]["original_djvu_page_1based"]==58 and reviews[0]["locus_1_original_glyph"]==a["target_glyph"] and reviews[0]["locus_2_original_glyph"]==b["target_glyph"] and reviews[0]["independent_physical_witness_votes"]==0,"original review issue crossbind")
 require(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,state["schema_version"].split("."))) >= (1,627,0),"state forward-only sync")
 require(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and all(x["id"] in ledger["checkpoint_log"][-1]["reviewed_issue_ids"] for x in ledger["issues"]),"research omission oversight")
 require(any(f.startswith("12YM ") for f in state["historical_audit"]["current_focus"]) and state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"state focus/algorithm safeguards")
 return {"result":"PASS","source_pages_verified":p["full_image_page_count_replayed"],"original_direct_glyph_loci":2,"independent_physical_originals_added":0,"local_original_arithmetic_gap_wei":50,"unresolved_omission_issues":11}
if __name__=="__main__":
 print(json.dumps(verify(*load()),ensure_ascii=False))
