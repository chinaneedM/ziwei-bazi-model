#!/usr/bin/env python3
"""12SH source-derived F10 JPEG 145-page identity and bounded-scope machine gate."""
import base64, hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RS=ROOT/"docs/research"
RECORD=RS/"MING-DATONG-YEHUOBIAN-12SH-NLC411999003250-F10-P1-136-ORIGINAL-BOUNDED-CLOSURE-R1.json"
PACK=RS/"MING-DATONG-YEHUOBIAN-12SH-NLC-F10-P1-136-JPEG-SHA256-PACKED-R1.txt"
QW=RS/"MING-DATONG-YEHUOBIAN-12QW-NLC411999003250-F6-F10-CONTACT-TRIAGE-R1.json"
QE=RS/"MING-DATONG-YEHUOBIAN-12QE-NLC-OLD20-V20-NINE-PAGE-BOUNDED-REVIEW-R1.json"
SG=RS/"MING-DATONG-YEHUOBIAN-12SG-NLC411999003250-F9-P81-141-ORIGINAL-SOURCE-CLOSE-R1.json"
FULL="73d9ee7c925b8a0fedaf02ead8236f1a5b0db78f5be6bb66ebdc518165995955"
WIN=["c43d12bf5e4da430e817e9abd76cfcf4c924a169e3f917f2d5526545f0ff2707","a3bde3e62d0254a01b8b0a8eddf791f00013a313d805f48171cddddeb4f986bc","57c96ea466cdf81e3a3037d6487aa0628a9541d2ff55e8341a40acb6a4d364e7","a63f064fb4351b91d17a484f4e95668180dea2ee156221b2dc23f47db593f629"]
def read(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def chain(xs):return hashlib.sha256("".join(xs).encode("ascii")).hexdigest()
def fail(c):raise ValueError("12SH_"+c)
def verify(record_path=RECORD,pack_path=PACK):
 d,qw,qe,sg=(read(p) for p in (record_path,QW,QE,SG))
 if (d.get("batch"),d.get("parent_open_batch"),d.get("stage"),d.get("status"))!=(
 "12SH","12QE","12QE_OPEN","ALL_1027_BODY_SOURCE_PAGES_NATIVE_JPEG_BOUNDED_FIRSTPASS_ONLY_NOT_FULLTEXT_NOT_ABSENCE_PROOF"):fail("SCOPE")
 s,v,g=d["source"],d["review"],d["grade_union"]
 q=next((x for x in qw["source_archives"] if x["fascicle"]==10),None)
 if q is None:fail("MISSING_ARCHIVE")
 if not(s["physical_holding"]=="NLC411999003250_ONE_HOLDING" and
  s["digital_fascicle"]==10 and s["source_pdf_pages"]==q["pdf_pages"]==145 and
  s["source_pdf_sha256"]==q["source_pdf_sha256"]==qe["source"]["source_pdf_sha256"] and
  s["source_pdf_rehashed_this_batch"] is False and s["source_jpeg_rasterized_pdf_dpi"]==85 and
  s["source_jpegs_are_archived_derived_images_not_physical_master"] is True and
  s["archived_artifact_id"]==q["artifact_id"]==qe["source"]["existing_capture_artifact_id"]==11666856770 and
  s["archived_workflow_run_id"]==q["workflow_run"]==38044584678 and
  s["archived_zip_sha256"]==q["artifact_zip_sha256"] and
  s["page_atlas_json_sha256"]==q["artifact_metadata_sha256"] and
  s["all_archived_page_jpeg_sha_and_bytes_verified"]==145 and s["archive_jpeg_mismatches"]==0 and
  s["all145_source_page_jpeg_ordered_sha256_chain"]==q["page_sha_chain"]==FULL):fail("SOURCE_IDENTITY")
 try:blob=base64.b64decode(Path(pack_path).read_text(encoding="ascii").strip(),validate=True)
 except Exception as e:raise ValueError("12SH_BAD_PACK") from e
 if len(blob)!=136*32:fail("PACKED_PAGE_COUNT")
 h=[blob[i:i+32].hex() for i in range(0,len(blob),32)]
 if not(len(set(h))==136 and all(re.fullmatch("[0-9a-f]{64}",x) for x in h) and
  v["hashes_packed_file"]=="docs/research/MING-DATONG-YEHUOBIAN-12SH-NLC-F10-P1-136-JPEG-SHA256-PACKED-R1.txt" and
  v["new_source_pdf_page_start"]==1 and v["new_source_pdf_page_end"]==136 and
  v["new_unique_original_size_archived_jpeg_page_screens"]==136 and
  v["montage_page_windows"]==[[i,min(i+3,136)] for i in range(1,137,4)] and
  v["mode"]=="ARCHIVED_SOURCE_DERIVED_JPEG_85DPI_ORIGINAL_PIXEL_SIZE_2X2_MONTAGES_BOUNDED_MANUAL_HEADING_TOPIC_SCREEN_ONLY"):fail("PACKED_HASHES_OR_WINDOWS")
 computed=[chain(h[:40]),chain(h[40:80]),chain(h[80:120]),chain(h[120:136])]
 stored=[v["page_sha256_chain_p1_40"],v["page_sha256_chain_p41_80"],v["page_sha256_chain_p81_120"],v["page_sha256_chain_p121_136"]]
 if computed!=stored or computed!=WIN or chain(h)!=v["page_sha256_chain_p1_136"]=="00e7e7e5bf85f64a15511ba522b00b6f9429727a353918049a02bd08f99d9924":fail("ORIGINAL_136_SOURCE_SHA_SEQUENCE")
 opens=q["original_juan_openings"]
 old=qe["direct_page_review"]["reviewed_pages"]
 nine=[x["derived_jpeg_sha256"] for x in old if 137<=x["pdf_page"]<=145]
 if not (len(nine)==9 and
  h[0]==opens[0]["sha256"] and h[80]==opens[1]["sha256"]==v["p81_original_page_sha256"] and
  h[135]==old[0]["derived_jpeg_sha256"]==v["p136_archived_context_page_sha256"] and
  nine[0]==opens[2]["sha256"] and
  nine[-1]==q["last_colophon_jpeg_sha"] and
  len(set(h+nine))==145 and chain(h+nine)==v["page_sha256_chain_p1_145"]==FULL):
  fail("FULL145_ORIGINAL_SHA_CROSS_BATCH")
 if not(v["p1_original_volume"]==18 and v["p81_right_leaf_previous_volume"]==18 and
  v["p81_left_leaf_new_volume"]==19 and v["p137_right_leaf_previous_volume"]==19 and
  v["p137_left_leaf_new_volume"]==20 and v["p137_145_inherited_native_bounded_from_12qe"] is True and
  [x["pages"] for x in v["page_topic_windows"]]==[[1,40],[41,80],[81,120],[121,136]]):fail("ORIGINAL_CHRONICLE_BOUNDARY")
 for k in ("ocr_used","automated_glyph_search_used","fulltext_line_by_line_collated",
 "any_original_old20_gaizao_louke_target_folio_positive_attestation","any_page_target_absence_proven",
 "fascicle10_target_absence_proven","whole_old20_work_target_absence_proven",
 "old20_juan_equivalent_to_1827_reorganized_thematic_juan","independent_1827_print_target_leaf_collated"):
  if v.get(k) is not False:fail("UNSUPPORTED_EVIDENCE_"+k)
 exp={"prior_global_native_source_pages":892,"prior_preview_only_body_pages":136,
 "new_f10_native_bounded_body_source_pages":136,"f10_native_bounded_source_pages_after":145,
 "f10_preview_only_after":0,"global_native_source_pages_after":1028,
 "global_native_body_source_pages_after":1027,"global_preview_only_body_pages_after":0,
 "non_target_first_fascicle_preliminary_pages":2,"f10_colophon_native_nonbody_pages":1,
 "whole_holding_source_pdf_pages":1030,"whole_body_pages":1027,
 "whole_body_fulltext_collation_pending":1027,"new_independent_physical_witnesses":0,
 "new_transmission_edges":0,"algorithm_reopens":0}
 if g!=exp or sg["grade_union"]["after_native_source_pages"]!=892 or sg["grade_union"]["after_preview_only_body_pages"]!=136:fail("GRADE_DEDUP")
 if d["transmission_impact"]["edges_supported"] or d["transmission_impact"]["edges_revised"]:fail("GENEALOGY")
 if d["invariants"]!={"matrix_rows":222,"matrix_audited":222,
 "provenance_metadata_repairs":"45/45","sources":"647+7=654","md_g03":"OPEN",
 "hpa_dayun_cal_002":"MISSING_FROM_PRODUCT","product_r1":"CLOSED",
 "confirmed_chart_algorithm_defects":0,"algorithm_reopens":0}:fail("PRODUCT")
 return {"batch":"12SH","whole_holding_total":1030,"native_source_pages":1028,
 "native_body_bounded":1027,"preview_only":0,"excluded_prelim_pages":2,
 "fulltext_body_pending":1027,"algorithms_reopened":0}
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False,indent=2))
