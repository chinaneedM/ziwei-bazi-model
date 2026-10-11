#!/usr/bin/env python3
"""12SG: fail-closed source JPEG sequence and bounded-original review scope gate."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RS=ROOT/"docs/research"
RECORD=RS/"MING-DATONG-YEHUOBIAN-12SG-NLC411999003250-F9-P81-141-ORIGINAL-SOURCE-CLOSE-R1.json"
SF=RS/"MING-DATONG-YEHUOBIAN-12SF-NLC411999003250-F9-P1-80-ORIGINAL-NATIVE-BOUNDED-REVIEW-R1.json"
QV=RS/"MING-DATONG-YEHUOBIAN-12QV-NLC411999003250-F9-141-PAGE-CONTACT-TRIAGE-R1.json"
SHA141="0b1f1df616301c576f937ffd336a513e6e87a0869d314f425890456e211828d5"
SHA61="c236919548219b0d92a89429f2fa09df8059db02bdca7d0feff1ce7c16bff26f"
def load(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def chain(xs):return hashlib.sha256("".join(xs).encode("ascii")).hexdigest()
def fail(s):raise ValueError("12SG_"+s)
def verify(path=RECORD):
 d,sf,qv=load(path),load(SF),load(QV)
 if [d.get("batch"),d.get("parent_open_batch"),d.get("stage"),d.get("status")]!=["12SG","12QE","12QE_OPEN","F9_ALL141_ORIGINAL_SOURCE_JPEG_NATIVE_BOUNDED_FIRSTPASS_NOT_FULLTEXT_NOT_NEGATIVE_ABSENCE_PROOF"]:fail("SCOPE")
 s,v,g=d["source"],d["review"],d["grade_union"]
 p=sf["source"];q=qv["source"]
 if not(s["physical_holding"]==p["physical_holding"]==q["holding"]=="NLC411999003250_ONE_HOLDING"
   and s["digital_fascicle"]==p["digital_fascicle"]==q["fascicle"]==9
   and s["source_pdf_pages"]==p["source_pdf_pages"]==q["pages"]==141
   and s["source_pdf_sha256"]==p["source_pdf_sha256"]==q["source_pdf_sha256"]
   and s["pdf_binary_rehashed_this_batch"] is False
   and s["original_artifact_id"]==p["archived_artifact_id"]==q["artifact_id"]==11674711170
   and s["original_workflow_run_id"]==p["original_workflow_run_id"]==q["workflow_run_id"]==38064436808
   and s["artifact_zip_sha256"]==p["artifact_zip_sha256"]==q["artifact_zip_sha256"]
   and s["artifact_status_sha256"]==p["artifact_status_json_sha256"]==q["status_json_sha256"]
   and s["source_jpeg_hash_and_byte_size_rechecked"]==141 and s["source_jpeg_mismatches"]==0
   and s["all141_original_source_jpeg_sha_chain"]==q["page_sha_chain"]==SHA141):fail("SOURCE")
 old=sf["review"]["individual_source_page_sha256_in_pdf_order"]
 new=v["source_jpeg_sha256_by_pdf_page_81_141"]
 if not(len(old)==80 and len(new)==61 and len(set(old+new))==141
   and all(isinstance(x,str) and re.fullmatch("[0-9a-f]{64}",x) for x in old+new)
   and chain(old)==v["parent_p1_80_sha_chain"]==sf["review"]["p1_80_ordered_source_page_sha256_chain"]
   and chain(new)==v["sha256_concat_81_141"]==SHA61
   and chain(new[:20])==v["sha256_concat_81_100"]=="258b2825cfe97f356d3e55ce2a400d1c16eb14a7d04b1aa4c2336a521bb511bf"
   and chain(new[20:40])==v["sha256_concat_101_120"]=="63cf13c1800140381c2c7ae5288d8532fb45050b360a8ad0eb12793609ca8d82"
   and chain(new[40:])==v["sha256_concat_121_141"]=="c58ec44040b07091a870baf66e5e5d5ff1734231002448a6ea579474eb2df82a"
   and chain(old+new)==v["full_f9_141_ordered_sha_chain"]==SHA141
   and new[3]==v["p84_source_jpeg_sha256"]==qv["navigation"]["p84_jpeg_sha256"]
   and new[-1]==v["p141_source_jpeg_sha256"]==qv["navigation"]["p141_jpeg_sha256"]):fail("SOURCE_PAGE_HASH_ORDER")
 if not(v["mode"]=="ORIGINAL_JPEG_PIXEL_PRESERVING_2X2_MONTAGE_BOUNDED_HEADING_TOPIC_VISUAL_SCREEN_ONLY"
   and [v["first_new_pdf_page"],v["last_new_pdf_page"],v["new_original_jpeg_pages_opened"]]==[81,141,61]
   and v["montage_windows"]==[[i,min(i+3,141)] for i in range(81,142,4)]
   and [x["pages"] for x in v["topic_windows"]]==[[81,84],[85,100],[101,120],[121,141]]
   and v["p84_right_leaf_original_volume"]==qv["navigation"]["p84_right_leaf_original_volume"]==16
   and v["p84_left_leaf_original_volume"]==qv["navigation"]["p84_left_leaf_original_volume"]==17
   and v["p84_original_heading"]==qv["navigation"]["f9_p84_original17_heading"]):fail("NATIVE_BOUNDED_NAVIGATION")
 for k in ("ocr_used","automated_text_or_glyph_search_used","fulltext_character_by_character_collated",
  "positive_old20_gaizao_louke_original_target_folio_attested","individual_page_target_absence_proven",
  "f9_volume_target_absence_proven","whole_old20_target_absence_proven",
  "old20_original_juan16_17_equated_to_1827_thematic_juan","independent_1827_target_leaf_collated"):
   if v.get(k) is not False:fail("FALSE_EVIDENCE_"+k)
 expected={"inherited_native_source_pages":831,"inherited_preview_only_body_pages":197,
   "new_native_source_body_pages":61,"after_native_source_pages":892,"after_native_body_pages":891,
   "after_preview_only_body_pages":136,"f9_original_native_pages_after":141,"f9_preview_only_pages_after":0,
   "whole_holding_source_pages":1030,"whole_body_fulltext_collation_backlog":1027,
   "non_target_f1_preliminary_pages":2,"nonbody_f10_colophon_native":1,
   "independent_physical_witness_increment":0,"transmission_edge_increment":0,"algorithm_reopen_count":0}
 if g!=expected or sf["grade_union"]["after_native_source_pages"]!=831 or sf["grade_union"]["after_preview_only_body_pages"]!=197:fail("DEDUP")
 if d["transmission_impact"]["edges_supported"] or d["transmission_impact"]["edges_revised"]:fail("GENEALOGY")
 if d["invariants"]!={"matrix_rows":222,"matrix_audited":222,"provenance_repairs":"45/45",
  "sources":"647+7=654","md_g03":"OPEN","hpa_dayun_cal_002":"MISSING_FROM_PRODUCT",
  "product_r1":"CLOSED","chart_algorithm_defects":0,"algorithm_reopens":0}:fail("PRODUCT")
 return {"batch":"12SG","f9_original_native_pages":141,"global_native_source_pages":892,
   "global_preview_only_body_pages":136,"f10_preview_only_to_review":136,
   "whole_body_fulltext_pending":1027,"algorithm_reopens":0}
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False,indent=2))
