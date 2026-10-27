#!/usr/bin/env python3
"""12RN: original JPEG-bounded mixed leaf of p83 directly anchors original juan7."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RN-NLC411999003250-F3-P81-84-ORIGINAL-JUAN7-MIXED-LEAF-R1.json"
PREVIOUS = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RM-NLC411999003250-F3-P41-60-NATIVE-SOURCE-REVIEW-R1.json"
NAVIGATION = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12QY-NLC411999003250-F1-F3-ALL-BODY-FIRSTPASS-R1.json"
PIN_HASHES = [
    "e099075b348b6f2af839856013ffa8baa53720c97633a9fc0e2395aa0a4c20c9",
    "33a10807e90f54cd9943cd77cfc51314bbb98e2c40b1dd5b36e9e75c6de5b35b",
    "a5fc4b32f0fa0e2425a313cf55504833af501435b3020809cb8578ad2b4720a6",
    "e4c657777f4178c5a64968e72d8cce1b250eca327cfab20bce11e6f3fc2f5876"
]
PIN_CHAIN = "fb01d6eeb00e53c5e6cbfeb654d1b0580a9fca16c94e197a74b0d48dccf6a3ee"

def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def verify(record_path=RECORD, previous_path=PREVIOUS, navigation_path=NAVIGATION):
    rec, before, atlas = read(record_path), read(previous_path), read(navigation_path)
    s, v, q = rec["source"], rec["review"], rec["queue"]
    prev = before["source"]
    n = atlas["sources"][2]
    if not (rec["batch"]=="12RN" and rec["stage"]=="12QE_OPEN" and rec["parent_open_batch"]=="12QE"
            and rec["status"]=="SOURCE_NATIVE_ORIGINAL_JUAN7_HEADING_DIRECTLY_ATTESTED_F3_P83_LEFT_LEAF_MIXED_BOUNDARY"
            and s["physical_holding"]==prev["holding"]=="NLC411999003250_ONE_HOLDING"
            and s["digital_fascicle"]==prev["digital_fascicle"]==n["fascicle"]==3
            and s["commons_file_id"]==prev["commons_file_id"]=="NLC892-411999003250-383068"
            and s["source_pdf_pages"]==prev["source_pdf_pages"]==n["source_pdf_pages"]==121
            and s["source_pdf_sha256"]==prev["source_pdf_sha256"]==n["source_pdf_sha256"]
            and s["source_pdf_binary_rehashed_in_batch"] is False
            and s["archive_artifact_id"]==prev["artifact_id"]==n["artifact_id"]==11673474713
            and s["archive_zip_sha256"]==prev["artifact_zip_sha256"]==n["zip_sha256"]
            and s["archive_status_json_sha256"]==prev["artifact_status_json_sha256"]==n["status_sha256"]
            and s["archive_all_jpeg_pages_rehashed"]==121
            and s["archive_original_jpeg_mismatches"]==0
            and s["archive_121_ordered_page_hash_chain"]==n["page_sha_chain"]
            and s["one_physical_holding_only"] is True):
        raise ValueError("12RN_ORIGINAL_SOURCE_IDENTITY_OR_ARCHIVE_SHA_DRIFT")
    h = v["source_page_sha256_in_order"]
    if not (v["mode"]=="INDIVIDUALLY_OPENED_ORIGINAL_RESOLUTION_P81_P82_P83_P84_FOR_CHRONICLE_VOLUME_BOUNDARY_AND_BOUNDED_TARGET_VISUAL_SCREEN"
            and (v["pdf_page_first"],v["pdf_page_last"],v["individual_original_jpegs_opened"])==(81,84,4)
            and h==PIN_HASHES
            and hashlib.sha256("".join(h).encode("ascii")).hexdigest()==v["sha256_concatenated_page_sha256"]==PIN_CHAIN
            and v["mixed_pdf_page"]==83
            and v["mixed_page_original_jpeg_sha256"]==h[2]==n["page_sha_pins"]["83"]
            and v["source_direct_juan7_heading_text"]=="萬曆三十二年甲辰卷七"
            and v["heading_directly_seen_on"]=="F3 PDF P83 LEFT ORIGINAL LEAF"
            and v["source_juan7_heading_visible"] is True
            and v["source_juan7_heading_evidence_level"]=="DIRECT_MANUAL_ORIGINAL_IMAGE_GLYPH_ATTESTATION_HASH_ANCHORED"
            and v["pdf_p83_right_leaf_previous_chronicle_content"] is True
            and v["pdf_p83_right_leaf_original_juan6_direct_heading_visible"] is False
            and v["pdf_p83_right_leaf_original_juan6_attribution"]=="CONTEXTUAL_PREVIOUS_JUAN_CANDIDATE_NOT_DIRECT_LEAF_HEADING"
            and v["pdf_p84_continues_juan7_text"] is True
            and v["source_juan6_7_mixed_original_leaf_boundary_verified"] is True
            and v["full_pdf_page83_assigned_exclusively_to_juan7"] is False):
        raise ValueError("12RN_DIRECT_JUAN7_HEADING_OR_MIXED_LEAF_BOUNDARY_DRIFT")
    forbidden=("original_juan6_opening_folio_located_in_this_batch",
               "old20_gaizao_louke_target_heading_or_folio_attested",
               "whole_work_target_absence_proven","page_target_absence_proven","ocr_used","full_text_transcribed")
    if any(v.get(k) is not False for k in forbidden) or v["not_equivalent_to_reedited_1827_juan7"] is not True:
        raise ValueError("12RN_FALSE_GLYPH_TEXT_ABSENCE_OR_EDITION_EQUIVALENCE")
    pq=before["queue"]
    if not (q["upstream_batch"]==before["batch"]=="12RM"
            and (q["prior_native_bounded_source_pages"],q["prior_preview_only_source_pages"],q["prior_native_target_backlog"])==
                (pq["new_whole_source_native_bounded_pages"],pq["new_preview_only_body_pages"],
                 pq["new_native_target_backlog"])==(278,750,750)
            and (q["new_native_bounded_source_pages"],q["new_preview_only_source_pages"],
                 q["new_native_target_backlog"])==(282,746,746)
            and (q["fascicle3_total_pdf_pages"],q["fascicle3_native_bounded_screened_pages"],
                 q["fascicle3_native_bounded_pending_pages"])==(121,64,57)
            and q["fascicle3_native_bounded_regions"]==[[1,60],[81,84]]
            and q["fascicle3_remaining_windows"]==[[61,80],[85,121]]
            and q["next_window_first"]==61 and q["next_window_last"]==80
            and (q["whole_holding_source_pages"],q["whole_holding_body_pages"],
                 q["unreviewed_prelim_nonbody_pages"],q["whole_body_fulltext_collation_pending"])==(1030,1027,2,1027)
            and 282+746+2==1030
            and q["physical_holding_increment"]==q["direct_copy_transmission_edge_increment"]==q["chart_algorithm_reopen_count"]==0
            and rec["transmission_impact"]["edges_supported"]==[]
            and rec["invariants"]=={"matrix":"222/222","provenance_repairs":"45/45",
                "external_sources":"647+7=654","md_g03":"OPEN","hpa_dayun_cal_002":"MISSING_FROM_PRODUCT",
                "product_r1":"CLOSED","algorithm_reopen_count":0}):
        raise ValueError("12RN_NONCONTIGUOUS_SCREEN_QUEUE_OR_LINEAGE_DRIFT")
    return {"batch":"12RN","original_juan7_heading":"萬曆三十二年甲辰卷七",
            "mixed_pdf_page":83,"left_original_leaf":"JUAN7",
            "right_original_leaf":"PREVIOUS_JUAN_CONTEXT_NOT_DIRECT_HEADING",
            "whole_native_bounded_pages":282,"preview_only_backlog":746,
            "fascicle3_native_remaining":57,"whole_body_fulltext_collation_pending":1027,
            "target_old20_gaizao_louke_attested":False}

if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
