#!/usr/bin/env python3
"""13R: hash-bound PDF page originals and scoped NLC D16/D18 direct glyph reading."""
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13R-NLC-GORYEOSA-V52-D16-D18-DIRECT-ORIGINAL-IMAGE-COLLATION-R1.json"
def get(path):return json.loads((R/path).read_text(encoding="utf-8"))
def sha(value):
 return isinstance(value,str) and bool(re.fullmatch(r"[0-9a-f]{64}",value))
def check(d):
 assert d["schema"]=="TIANWEN-13R-NLC-GORYEOSA-V52-D16-D18-HASH_BOUND-ORIGINAL-PIXEL-COLLATION-R1"
 assert d["issue_id"]=="TW-OPEN-0005" and d["prior_checkpoint"]=="docs/research/TIANWEN-13Q-NLC-GORYEOSA-WORK52-GROUP40-R1.json"
 c=d["capture"]
 assert c["workflow_run_id"]==39201734818 and c["artifact_id"]==12163174889 and c["artifact_name"]=="goryeosa-group40-original-pdf-13q"
 assert c["original_pdf_bytes"]==19799436 and c["actual_pdf_page_count"]==64
 assert c["original_pdf_sha256"]=="2b9e51cc5f44a4d92d3cb4a63318605f78cc8ffb118853036655b65ed279a689"
 assert c["artifact_zip_digest"]=="sha256:1a3ea6c6e287e3b8010d77cc01884210f89ba6b7226a46e5f861cafcbbdc015c"
 assert c["raw_pdf_sha256_local_reread_same_as_action"] is True and "no OCR" in c["reader_tool"]
 p=d["native_page_records"]
 assert len(p)==3 and [x["pdf_page_1_based"] for x in p]==[2,16,17]
 assert [x["embedded_raster_xref"] for x in p]==[13,111,118]
 assert [x["embedded_raster_sha256"] for x in p]==["d477a70c3543d328f79adb319163c63be1a5b83070f0be4c65f4940235ca7dcc","cfd7a3bb0741d49d9e0fe04147a88eefb3f32cffa404004f01f1748374ea637f","8807e0c2e3b6d88a508bfc450e3b9eec78c59948b9314586fc882338f3bf52af"]
 assert [x["source_crop_png_sha256"] for x in p]==["a765c220d7e14f61c19ac3c684eed64287fe23bc447cd9fbb6b7e9637000ea60","f3d52e8790db60958fce54b2b7459bdf6cfe3046d448120bc228b5751fac6066","640ce449af4967bacc2e684a44b9269208d3b3056cfcc9b5a2fa18e1cfccc5bd"]
 assert [x["direct_text"] for x in p]==["志卷第六","五分一三六二","八千四百二十四六四〇八"]
 for x in p:
  assert x["embedded_raster_format"]=="png" and x["pixel_dimensions"]==[4296,3607]
  assert x["pdf_page_zero_based"]==x["pdf_page_1_based"]-1
  assert x["direct_text_grade"]=="DIRECT_ORIGINAL_DIGITAL_SURROGATE_NATIVE_PIXEL_VISUAL"
  assert sha(x["embedded_raster_sha256"]) and sha(x["source_crop_png_sha256"])
  x0,y0,x1,y1=x["source_crop_xyxy"]
  assert 0<=x0<x1<=4296 and 0<=y0<y1<=3607
 comp=d["direct_comparison"]
 assert comp["d16"]["nlc_image_glyph"]=="五分一三六二" and comp["d16"]["preexisting_g893_original"]=="五分二三六二"
 assert comp["d16"]["candidate_difference"]=="-0.1000" and comp["d16"]["same_historical_unit_status"]=="UNADJUDICATED"
 assert comp["d18"]["nlc_image_glyph"]=="八千四百二十四六四〇八"
 assert comp["d18"]["preexisting_nikh_modern_hanja_received"]=="八千四百二十四六四〇八三"
 assert comp["d18"]["original_nlc_no_extra_three_visually_observed"] is True and comp["d18"]["recension_or_modern_transcription_error_cause"]=="UNADJUDICATED"
 e=d["evidence_grading"]
 assert all(e[x] is True for x in ("whole_source_original_digital_surrogate_acquired","internal_work52_title_original_paper_image_seen","target_d16_glyph_native_original_image_seen","target_d18_cumulative_glyph_native_original_image_seen","source_page_image_hash_bound"))
 assert all(e[x] is False for x in ("original_nlc_firstparty_item_identifier_bound","physical_copy_date_verified","edition_impression_verified"))
 assert all(e[x]==0 for x in ("independent_physical_original_numeric_votes_added","root_registry_new_sources","extension_registry_new_sources","transmission_edges_added","algorithm_reopen"))
 assert e["all_11_issue_status"]=="OPEN" and e["chart_r1"]=="CLOSED"
 assert e["cadal_same_original_copy_relation"]=="UNKNOWN" and e["institutional_hanja_error_cause"]=="UNKNOWN"
def verify():
 d=get(E);check(d)
 prev=get(d["prior_checkpoint"])
 assert prev["source_binary_downloaded_at_checkpoint"] is False and prev["source_pdf_sha256"] is None
 s=get("docs/PROJECT-CURRENT-STATE-R1.json")
 l=get("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,677,0)
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13R ") for x in s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"] and E[:-5]+".md" in issue["source_refs"]
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 assert set(l["checkpoint_log"][-1]["reviewed_issue_ids"])=={x["id"] for x in l["issues"]}
 assert any(c["id"]=="OMISSIONS-13R-NLC-WORK52-D16D18-DIRECT-PIXEL-20261019" for c in l["checkpoint_log"])
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0
 return {"status":"PASS","native_source_pages_directly_collated":3,"target_numeric_passage_scope_count":2,"independent_physical_votes":0}
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False))
