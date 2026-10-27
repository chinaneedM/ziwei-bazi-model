#!/usr/bin/env python3
"""12WM: immutable second-source binary receipt, no double historical print vote."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12WM-CADAL02096900-ACTUAL-OLD-NEW-PARATEXT-PAGE-DIGITAL-REPLAY-R1.json"
PENDING="docs/research/MING-DATONG-YEHUOBIAN-12WL-CADAL02096900-DUAL-ORIGINAL-IMAGE-REPLAY-R1.json"
WK="docs/research/MING-DATONG-YEHUOBIAN-12WK-FOUR-ERA-PARATEXT-ORIGINAL-IMAGE-COLLATION-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
MANIFEST="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
EXPECTED_SHA={"old":"30d111a7c47741dbca4feff9d065e09a7ea1d67c9343f55cb268968deb8918c6","new":"711dc16b17d139612fbe852dc99869bb709b85c161440dfc7618ee1dbd6f38fa"}
ZIP="04abe1a062bb001e125385e34d7ab74c7a1ab21962a505bd207e1f896bbe2f79"
PAGES={5:(0.03447,"30b97980cf969be75d2300026831816270d2185f08c95dea302dbaf5cbd047f1","19e977e8123bc1299d76eef384de97e7dbf80893c3b1a25500b3b0d7930c891f"),7:(0.07514,"d0751e812cad787070d13ba0ef5246dc892a7721ccab141e3796f1371edfafed","d64d32ad432cf1f184208e63b9fa78e54077a3f4a94832f544129f98b04d4e79"),10:(0.03550,"2b0613826cb9b4f5337147bddb0d459ffc2e403aaf65878a2f1678ca2f7b7ab5","7af56ca7276d8d6af0793716461b1be489528fbcc79bf9dba038541f02cecb23")}
def check(ok,msg):
 if not ok:raise ValueError(msg)
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def validate(r,pending,wk,state,manifest):
 check(r["schema"]=="TIANWEN-12WM-CADAL-FIRST-FASCICLE-ACTUAL-DUAL-ORIGINAL-DIGITAL-NEAR-DUPLICATE-R1","schema")
 a=r["acquisition"]
 check((a["github_run_id"],a["capture_job_id"],a["verify_job_id"],a["artifact_id"])==(38728723441,116401073670,116400901099,11969606929),"exact-head GitHub receipt")
 check(a["exact_capture_head"]=="25fdb16ffbdaac2899a137eca3651c2cb25be87e" and a["exact_run_status"]=="completed" and a["exact_run_conclusion"]=="success","completed source capture not pending")
 check(a["artifact_zip_bytes"]==5800015 and a["artifact_zip_sha256_github_reported"]==a["artifact_zip_sha256_independently_recomputed"]==ZIP,"actual archived bytes independently rehashed")
 check(all(a[k] is True for k in ("two_original_binary_sha256_independently_recomputed","six_page_png_sha256_independently_recomputed","three_preview_pixel_deltas_independently_recomputed","original_binary_sha1_consistent_with_commons_source_imageinfo","source_url_access_via_commons_api_and_source_emitted_url")) and a["ocr_used"] is False,"no fake image/ocr receipt")
 files=r["source_files"]
 check(len(files)==2 and [f["label"] for f in files]==["old","new"],"two source aliases")
 check([f["bytes"] for f in files]==[2791559,2833699] and all(f["pages"]==115 for f in files),"original binary bytes and pages")
 check([f["sha256"] for f in files]==[EXPECTED_SHA["old"],EXPECTED_SHA["new"]],"original binary SHA256")
 check([f["sha1"] for f in files]==["3aef0b8493c20f5e5c274269a274785be4a11edf","ea7e67a4eb47f6ca59bc54d4635f2f26eeef6f2a"],"Commons original SHA1")
 check(all(f["cadal_id"]=="02096900" and f["original_url"].startswith("https://upload.wikimedia.org/wikipedia/commons/") for f in files),"same numbered digital identifier")
 check(wk["source"]["original_djvu_sha256"]==files[1]["sha256"],"12WK image-bound source preserved")
 comp=r["page_comparisons"]
 check([p["page"] for p in comp]==[5,7,10],"direct page set")
 for p in comp:
  delta,oldpng,newpng=PAGES[p["page"]]
  check(p["delta"]==delta and p["old_png_sha256"]==oldpng and p["new_png_sha256"]==newpng,"actual preview pixel control")
  check(len(p["old_page_gray_sha256"])==len(p["new_page_gray_sha256"])==64 and p["old_page_gray_sha256"]!=p["new_page_gray_sha256"],"decoded old/new source pixels nonexact")
 cr=r["computed_relation"]
 check(cr["same_djvu_bytes"] is False and cr["same_file_page_count"] is True and cr["same_exact_decoded_grayscale_pixels_on_checked_pages"] is False and cr["selected_page_visual_near_identity"] is True,"digital near duplicate only")
 check(cr["comparison_preview_dimensions"]==[256,384] and cr["compared_original_page_dimensions"]==[2000,3000],"pixel geometry")
 check(all(cr[k]=="UNBOUND" for k in ("identity_of_underlying_scanned_physical_paper_copy","original_print_date_or_plate_revision","cross_fascicle_physical_copy_identity_to_CADAL02096915")),"no paper-copy or edition promotion")
 g=r["image_glyph_limit"]
 check(g["new_manual_full_resolution_old_fascicle_glyph_collation"] is False and g["new_paratext_glyph_votes"]==0 and g["new_juan20_gaizao_louke_glyph_votes"]==0,"no new manual ancient glyph")
 check(g["no_independent_original_1827_paper_first_impression_leaf"] is True and g["no_independent_original_1869_paper_revision_leaf"] is True,"no original dated leaves")
 c=r["accounting"]
 check(c["source_registry_additions"]==0 and c["ext_source_registry_total"]==705 and manifest["combined_source_count"]==state["historical_audit"]["external_source_registry_total_unique_count"]>=c["ext_source_registry_total"],"no source double count")
 check(c["matrix_rows"]==c["matrix_audited"]==state["historical_audit"]["row_count"]==222 and c["metadata_repairs"]==45,"matrix and provenance counts")
 check(c["formal_batches"]==len(state["historical_audit"]["completed_batches"])==487 and c["graph_nodes"]==252 and c["graph_edges"]==238,"batches graph fixed")
 check(c["algorithm_reopens"]==0 and c["true_chart_defects"]==0 and c["product"]==state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","product unaffected")
 check(pending["status"]=="PENDING_EXACT_HEAD_COMMONS_SOURCE_CAPTURE_NOT_YET_ATTESTED" and r["continuity"]["no_rewrite_of_12WL_pending_record"] is True,"forward-only pending historical snapshot")
 check(r["transmission_impact"]["edges_supported"]==[] and r["transmission_impact"]["nodes_added_or_strengthened"]==[],"no lineage edge")
 return {"status":"PASS","old_new_original_jvu_files_rechecked":2,"verified_comparison_pages":3,"actual_archived_bytes":a["artifact_zip_bytes"],"historic_independent_print_votes":0}
def verify():return validate(*(load(p) for p in (REC,PENDING,WK,STATE,MANIFEST)))
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False))
