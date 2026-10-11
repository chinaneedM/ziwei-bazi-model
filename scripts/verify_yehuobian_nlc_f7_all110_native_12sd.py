#!/usr/bin/env python3
"""12SD: F7 complete 110-page source-JPEG hash chain and bounded-grade firewall."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"docs/research"
RECORD=PRE/"MING-DATONG-YEHUOBIAN-12SD-NLC411999003250-F7-P61-110-ORIGINAL-SOURCE-CLOSE-R1.json"
SC=PRE/"MING-DATONG-YEHUOBIAN-12SC-NLC411999003250-F7-P21-60-ORIGINAL-NATIVE-BOUNDED-REVIEW-R1.json"
QR=PRE/"MING-DATONG-YEHUOBIAN-12QR-NLC411999003250-F7-OLD12-TWENTY-DIRECT-IMAGE-SCREENS-R1.json"
QS=PRE/"MING-DATONG-YEHUOBIAN-12QS-NLC411999003250-F7-REMAINING90-MONTAGE-TRIAGE-R1.json"
SHA50="46a91cac2f3bf6eb41cf84fb4f151015a3d37b1c3d91dd9650934828007bea3c"
SHA110="26a6c46170b03eb904bbd64619f8a920c840eab15a2a343570e9223214c7e92c"
SHA90="f2cb44f86dabe5047dfe6945defd88169acde9d7cc39e9e97ad76dc82292abce"
def read(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def chain(a):return hashlib.sha256("".join(a).encode("ascii")).hexdigest()
def fail(code):raise ValueError("12SD_"+code)
def verify(path=RECORD):
    d,sc,qr,qs=(read(p) for p in (path,SC,QR,QS))
    if (d["batch"],d["parent_open_batch"],d["stage"],d["status"])!=(
        "12SD","12QE","12QE_OPEN","F7_ALL110_ORIGINAL_JPEG_SOURCE_BOUNDED_FIRSTPASS_NOT_FULLTEXT_NOT_NEGATIVE_TARGET_ABSENCE_PROOF"):fail("STAGE")
    s,v,g=d["source"],d["review"],d["grade_union"]
    prior=qr["review"]["screened_pdf_pages"]
    a=[r["source_derived_page_jpeg_sha256"] for r in prior]+sc["review"]["page_sha256_in_order"]
    b=v["page_sha256_in_order"]
    if not(s["holding"]==sc["source"]["holding"]=="NLC411999003250_ONE_HOLDING"
      and s["digital_fascicle"]==sc["source"]["digital_fascicle"]==7
      and s["source_pdf_pages"]==110
      and s["source_pdf_sha256"]==sc["source"]["source_pdf_sha256"]==qs["source"]["source_pdf_sha256"]
      and s["source_pdf_binary_rehashed_this_batch"] is False
      and s["original_workflow_run_id"]==qs["source"]["original_workflow_run_id"]==38064436808
      and s["archived_artifact_id"]==sc["source"]["archived_artifact_id"]==11674890925
      and s["artifact_zip_sha256"]==sc["source"]["artifact_zip_sha256"]
      and s["artifact_status_sha256"]==sc["source"]["artifact_status_sha256"]
      and s["source_jpeg_sha_and_bytes_checked"]==110 and s["original_jpeg_mismatches"]==0):
        fail("SOURCE_ARCHIVE")
    if not(len(a)==60 and len(b)==50 and len(set(a+b))==110
      and all(isinstance(x,str) and re.fullmatch("[0-9a-f]{64}",x) for x in a+b)
      and chain(a)==v["parent_12sc_f7_p1_60_chain"]==sc["review"]["first20_plus_this40_sha256"]
      and chain(b)==v["sha256_of_joined_page_sha256"]==SHA50
      and chain(b[:20])==v["p61_80_chain"]=="62d07967e73fdd8d39953e0c4a82166b22214851fd6791f76fb6afd1204e30a0"
      and chain(b[20:])==v["p81_110_chain"]=="544e74b9168a1dc2a2187bfaceca339a735c7515ccd977aa1e0614ec806a39f5"
      and chain(a+b)==v["f7_p1_110_ordered_chain"]==s["all110_ordered_source_jpeg_sha256_chain"]==SHA110
      and chain(a[20:]+b)==v["qs_p21_110_ordered_chain"]==qs["review_scope"]["page_sequence_hash_sha256"]==SHA90):
        fail("SOURCE_JPEG_ORDERED_HASH_CHAIN")
    if not(v["page_range"]==[61,110] and v["pages_opened"]==50
      and v["mode"]=="ORIGINAL_SOURCE_JPEG_PIXEL_PRESERVING_2X2_MONTAGE_BOUNDED_MANUAL_HEADING_TOPIC_REVIEW"
      and v["montage_page_windows"]==[[i,i+3] for i in range(61,109,4)]+[[109,110]]
      and [x["pages"] for x in v["bounded_topic_notes"]]==[[61,68],[69,80],[81,92],[93,104],[105,110]]):
        fail("WINDOWS")
    for k in ("ocr_used","fulltext_line_by_line_collated",
       "original_old20_target_heading_or_glyph_attested","negative_absence_proven_on_any_page",
       "entire_f7_target_absence_proven","entire_old20_target_absence_proven",
       "independent_1827_print_target_collated"):
        if v.get(k) is not False:fail("UNSUPPORTED_TEXT_AUTHORITY")
    expected={"inherited_f7_native_source_pages":60,"new_f7_native_source_pages":50,
       "f7_native_source_pages_after":110,"f7_remaining_preview_only_pages":0,
       "whole_holding_pdf_source_pages":1030,"whole_holding_native_source_pages_before":614,
       "whole_holding_native_source_pages_after":664,"whole_holding_native_body_source_pages_after":663,
       "whole_holding_preview_only_body_pages_before":414,"whole_holding_preview_only_body_pages_after":364,
       "whole_holding_nontarget_preliminary_pages":2,"whole_holding_colophon_native_nonbody_pages":1,
       "whole_body_fulltext_collation_backlog":1027,"physical_holding_increment":0,
       "independent_witness_increment":0,"transmission_edge_increment":0,
       "source_pdf_rehashed":False,"source_jpeg_hash_integrity_only":True}
    if g!=expected or sc["grade_union"]["whole_holding_native_source_pages_after"]!=614:fail("DEDUP_GRADE")
    if d["transmission_impact"]["edges_supported"] or d["transmission_impact"]["edges_revised"]:fail("LINEAGE")
    if d["invariants"]!={"matrix_rows":222,"matrix_audited":222,"provenance_repairs":"45/45",
        "sources":"647+7=654","md_g03":"OPEN","hpa_dayun_cal_002":"MISSING_FROM_PRODUCT",
        "product_r1":"CLOSED","confirmed_algorithm_defects":0,"algorithm_reopens":0}:fail("PRODUCT_INVARIANTS")
    return {"batch":"12SD","f7_native_source_pages":110,"global_native_source_pages":664,
        "global_preview_only_pages":364,"fulltext_body_pending":1027,"algorithm_reopens":0}
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False,indent=2))
