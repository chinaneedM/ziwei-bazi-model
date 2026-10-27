#!/usr/bin/env python3
"""12YO Mei v3 original-image source route; enforce catalog-only negative controls."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YO-MEI-DATONG-LIZHI-V3-ORIGINAL-IMAGE-ACCESS-CROSSWALK-R1.json"
def require(ok,msg):
 if not ok:raise ValueError(msg)
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json"))
def verify(d,l,s):
 require(d["schema"]=="TIANWEN-12YO-MEI-DATONG-LIZHI-V3-IMAGE-ACCESS-PROVENANCE-CROSSWALK-R1" and d["status"]=="PUBLIC_DIGITAL_LOCATORS_IDENTIFIED_ORIGINAL_IMAGE_BYTES_AND_PRINTED_TARGET_UNVERIFIED","false original evidence grade")
 require(d["target"]["juan"]=="卷三" and d["target"]["source_glyphs_directly_verified"]==0,"no original Mei glyph")
 rs={e["id"]:e for e in d["catalog_routes"]}
 for key in ("CTEXT-RECEIVED-239751","CTEXT-SCAN-OCR-251951","CTEXT-AUTHOR-SCANS","FINNA-NELLI06-3790000000367099","SHIDIANGUJI-SK1539-V3","WIKISOURCE-MEI-V3"):
  require(key in rs,"source route missing")
 scan=rs["CTEXT-SCAN-OCR-251951"]
 require(scan["relevant_catalog_fascicle"]=="卷三至卷四" and scan["ocr_confidence"]=="UNRELIABLE_FOR_NUMERIC_GLYPH" and scan["retrieved_original_bytes"] is False and scan["direct_image_page_number"] is None and scan["original_sha256"] is None and scan["printed_target_gloss"] is None,"CText OCR illegally promoted to historical original")
 finn=rs["FINNA-NELLI06-3790000000367099"]
 require(finn["physical_identity_to_ctext"]=="UNPROVEN" and finn["bytes_downloaded"] is False and finn["role"].startswith("NATIONAL_LIBRARY_FINLAND_METADATA"),"two catalogues are not two original prints")
 witness=d["source_independence"]
 require(witness["physical_impression_votes_added"]==witness["source_registry_new_items"]==witness["genealogy_nodes"]==witness["genealogy_edges"]==0 and witness["ctext_reproductions_not_votes"] is True,"catalogue cannot vote in history")
 flags=d["safeguards"]
 require(flags["mei_original_verified_targets"]==0 and flags["g893_original_fields"]=="5/6" and flags["cross_witness_mechanical_final"]=="0/6" and flags["open_omission_issues"]==11 and flags["historical_matrix_rows"]==flags["historical_matrix_audited"]==222 and flags["product"]=="CLOSED" and flags["algorithm_reopens"]==0,"no mechanical or product reclassification")
 issue=next(a for a in l["issues"] if a["id"]=="TW-OPEN-0005")
 require(issue["status"]=="OPEN" and DOC in issue["source_refs"] and DOC.replace(".json",".md") in issue["source_refs"],"missing issue crossbinding")
 require(len(issue["mei_12yo_v3_scan_route_reviews"])==1 and issue["mei_12yo_v3_scan_route_reviews"][0]["original_target_glyphs_verified"]==0,"issue original glyph evidence incorrectly upgraded")
 require(s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,s["schema_version"].split(".")))>=(1,629,0),"review state stale")
 require(l["checkpoint_log"][-1]["state_version"]==s["schema_version"] and any(x.startswith("12YO ") for x in s["historical_audit"]["current_focus"]),"forward review gate missing")
 require(s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0,"chart algorithm reopen not licensed")
 return {"result":"PASS","ctext_fascicle_index":"卷三至卷四","source_pixels_verified":0,"physical_witness_votes":0,"unresolved_issues":len(l["issues"])}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
