#!/usr/bin/env python3
"""12SC: fail-closed F7 p21-60 SHA chain and bounded provenance-grade replay."""
import hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12SC-NLC411999003250-F7-P21-60-ORIGINAL-NATIVE-BOUNDED-REVIEW-R1.json"
QR=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QR-NLC411999003250-F7-OLD12-TWENTY-DIRECT-IMAGE-SCREENS-R1.json"
QS=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QS-NLC411999003250-F7-REMAINING90-MONTAGE-TRIAGE-R1.json"
def read(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def chain(xs): return hashlib.sha256("".join(xs).encode("ascii")).hexdigest()
def fail(code): raise ValueError("12SC_"+code)
def verify(path=RECORD):
    d, qr, qs = read(path), read(QR), read(QS)
    s, v, g=d["source"], d["review"], d["grade_union"]
    if [d["batch"],d["parent_open_batch"],d["stage"]] != ["12SC","12QE","12QE_OPEN"]: fail("STAGE")
    if not (s["holding"]=="NLC411999003250_ONE_HOLDING" and
        s["digital_fascicle"]==7 and s["source_pdf_pages"]==110 and
        s["source_pdf_sha256"]==qr["source"]["source_pdf_sha256"]==qs["source"]["source_pdf_sha256"] and
        s["archived_artifact_id"]==qr["source"]["artifact_id"]==qs["source"]["original_artifact_id"]==11674890925 and
        s["artifact_zip_sha256"]==qr["source"]["artifact_zip_sha256"]==qs["source"]["artifact_zip_sha256"] and
        s["artifact_status_sha256"]==qr["source"]["artifact_status_sha256"]==qs["source"]["artifact_status_json_sha256"] and
        s["source_pdf_binary_rehashed_this_batch"] is False and
        s["original_jpeg_sha_and_bytes_checked"]==40 and s["original_jpeg_mismatches"]==0):
        fail("SOURCE_IDENTITY")
    h=v["page_sha256_in_order"]
    old=[x["source_derived_page_jpeg_sha256"] for x in qr["review"]["screened_pdf_pages"]]
    if not (len(old)==20 and len(h)==40 and all(re.fullmatch("[0-9a-f]{64}",x) for x in old+h)
       and chain(h)==v["sha256_of_joined_page_sha256"]=="ee9fd9d1df5a0880785299dbf17bbbf5589925d125daf82c8e6d12955dd5f3f7"
       and chain(old+h)==v["first20_plus_this40_sha256"]=="51328acc984a907b6e0237d4299009691a951cd93a7945bdc9e44451a9e4c7cb"
       and v["f7_original_all110_sha256_from_archived_status"]=="26a6c46170b03eb904bbd64619f8a920c840eab15a2a343570e9223214c7e92c"):
        fail("ORIGINAL_PAGE_CHAIN")
    if not (v["page_range"]==[21,60] and v["pages_opened"]==40 and
        v["montage_page_windows"]==[[p,p+3] for p in range(21,61,4)] and
        v["mode"]=="ORIGINAL_SOURCE_JPEG_PIXEL_PRESERVING_2X2_MONTAGE_BOUNDED_MANUAL_HEADING_TOPIC_REVIEW"):
        fail("BOUNDED_WINDOWS")
    for key in ("ocr_used","fulltext_line_by_line_collated","original_old20_target_heading_or_glyph_attested",
                "negative_absence_proven_on_any_page","entire_f7_target_absence_proven",
                "entire_old20_target_absence_proven","independent_1827_print_target_collated"):
        if v.get(key) is not False: fail("OVERCLAIM_"+key)
    expected={"inherited_f7_native_source_pages":20,"new_f7_native_source_pages":40,
        "f7_native_source_pages_after":60,"f7_remaining_preview_only_pages":50,
        "whole_holding_pdf_source_pages":1030,"whole_holding_native_source_pages_before":574,
        "whole_holding_native_source_pages_after":614,"whole_holding_preview_only_body_pages_before":454,
        "whole_holding_preview_only_body_pages_after":414,
        "whole_holding_nontarget_preliminary_pages":2,"whole_body_fulltext_collation_backlog":1027,
        "physical_holding_increment":0,"independent_witness_increment":0,"transmission_edge_increment":0,
        "source_pdf_rehashed":False,"source_jpeg_hash_integrity_only":True}
    if g!=expected: fail("DEDUP_COUNTS")
    if d["transmission_impact"]["edges_supported"] or d["transmission_impact"]["edges_revised"]: fail("LINEAGE")
    if d["invariants"]!={"matrix_rows":222,"matrix_audited":222,"provenance_repairs":"45/45",
        "sources":"647+7=654","md_g03":"OPEN","hpa_dayun_cal_002":"MISSING_FROM_PRODUCT",
        "product_r1":"CLOSED","confirmed_algorithm_defects":0,"algorithm_reopens":0}: fail("R1_INVARIANTS")
    return {"batch":"12SC","native_graded_pages":614,"preview_only_pages":414,
            "f7_original_bounded_pages":60,"fulltext_body_pending":1027,"algorithm_reopens":0}
if __name__=="__main__": print(json.dumps(verify(),ensure_ascii=False,indent=2))
