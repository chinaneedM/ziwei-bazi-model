#!/usr/bin/env python3
"""12RQ F3 original source p105-121 hash-chain and first-pass boundary gate."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RQ-NLC411999003250-F3-P105-121-NATIVE-SOURCE-REVIEW-R1.json"
PRIOR = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RP-NLC411999003250-F3-P85-104-NATIVE-SOURCE-REVIEW-R1.json"
PINS = [
    "715773ab3786152eaf1235805161294211796674f26803b78d733a4f8a97ac35",
    "2383d1dc944205909de91b51e0e4a5c74770048273ba4799d9253cc2061c16ee",
    "0683c0c6f769f39150947d59773553ea0a48312716317e68bb90e6c0bd266e77",
    "bdc42be0727a49d196f46b40502d26b516d8e56d5c15f56e396241ce86206809",
    "8880fac7789e4bad5191a9ca7f8c6e464952e9850634fa46522f66f7df48af16",
    "93c8c58b4ae9da7bf3a3b35a01e986dc438ba62cdcda21dadbe8908ea86e755d",
    "e24d54af59a274fd7d745472a0208fcb8531a05457a3a80885c0bea9f08df8df",
    "8ba43be68085e5581dc7c81f251cf564c7e4520c76f27d2c4949742c392c2367",
    "20430ecdea33e211248222dfb24bea82f5f4583f85463ea2f64837e938cf71c4",
    "630ce60a932a0eb55a557b7bd692f29383a44c08f2166bd4a05a3a524c768291",
    "30820b55c7721e9a6afa6fdbd18dc60c28d3274225f7a9becdad22218709e3d3",
    "4d04b9c9ccfd443129aed676fae7082b4e3b540fce742eb697f35e288b942d8a",
    "b850565d6f5965ddfc21d0b3283677b64543fb350892338fcf77a772cb9d67ac",
    "5da531f8b665d3ad8c4d9456893273277345a4dfc032447a30f8f5344a673750",
    "b068ebe7f4aced68cd890e8eb2c70095cadb322c66082a1f972442ceece6d3cb",
    "3f2338393bd02c08556b239cf8c16d1e28ba06e5cc4443509be470d4e01b9a63",
    "06d18ec79259d48522da52e7c13f107870978846726dad16adbbb79f80bd2982"
]
WINDOW = "d118a4cd44c0967b75906d0f40c9569a0f8f10800ddb35da39a1db861717fb92"
FIRST104 = "4e6fd646637e2b41caba455015808133f443f0903336792d0fceb33bc348fb6d"
FULL121 = "9e15a3a0707adda7cd5b319b21d24f7e1df38b64dc35c48034cb92800e1eb769"

def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def chained(shas):
    return hashlib.sha256("".join(shas).encode("ascii")).hexdigest()

def verify(record_path=DATA, prior_path=PRIOR):
    d = read(record_path)
    prev = read(prior_path)
    s, v, q = d["source"], d["review"], d["queue"]
    ps, pv, pq = prev["source"], prev["review"], prev["queue"]
    if not (
        d["batch"] == "12RQ"
        and d["stage"] == "12QE_OPEN"
        and d["parent_open_batch"] == "12QE"
        and d["status"] == "F3_P105_121_BYTE_VERIFIED_BOUNDED_VISUAL_FIRST_PASS_F3_121_121_WITHOUT_FULLTEXT_OR_NEGATIVE_PROOF"
        and s["physical_holding"] == ps["physical_holding"] == "NLC411999003250_ONE_HOLDING"
        and s["commons_file_id"] == ps["commons_file_id"] == "NLC892-411999003250-383068"
        and s["source_pdf_pages"] == ps["source_pdf_pages"] == 121
        and s["source_pdf_sha256"] == ps["source_pdf_sha256"]
        and s["source_pdf_binary_rehashed_in_12rq"] is False
        and s["archive_artifact_id"] == ps["archive_artifact_id"] == 11673474713
        and s["archive_zip_sha256"] == ps["archive_zip_sha256"]
        and s["archive_status_sha256"] == ps["archive_status_sha256"]
        and s["full_fascicle_121_source_jpeg_hash_chain_sha256"] == ps["full_121_original_jpeg_ordered_sha256_chain"] == FULL121
        and s["archive_121_original_jpeg_byte_hash_and_size_status_mismatches"] == 0
    ):
        raise ValueError("12RQ_ARCHIVE_IDENTITY_DRIFT")
    source_pages = v["original_jpeg_sha256_in_pdf_page_order"]
    if not (
        source_pages == PINS and len(source_pages) == 17
        and (v["pdf_page_first"], v["pdf_page_last"]) == (105, 121)
        and v["page_level_original_jpeg_files_hash_verified"] == 17
        and v["page_level_images_seen_in_visual_review"] == 17
        and v["mode"] == "HASH_CHECKED_ORIGINAL_JPEG_SOURCE_WITH_PAGE_LEVEL_BOUNDED_VISUAL_SHEET_REVIEW_NOT_LINEWISE_COLLATION"
        and v["visual_review_display"] == "SOURCE_JPEGS_RENDERED_IN_TWO_BY_TWO_PAGE_SHEETS_WITH_ASPECT_RATIO_PRESERVED_AND_FINAL_SINGLE_PAGE_SHEET"
        and chained(source_pages) == v["window_ordered_sha256_hash_chain"] == WINDOW
        and v["first104_prior_batch_sha256_hash_chain"] == pv["fascicle3_first104_original_jpeg_ordered_hash_chain"] == FIRST104
        and v["whole_fascicle_121_ordered_sha256_hash_chain"] == FULL121
        and v["previous_juan7_heading_only_directly_seen_on_prior_p83_left_leaf"] == pv["direct_original_juan7_heading_in_source_pdf_p83_left_leaf"] == "萬曆三十二年甲辰卷七"
        and len(v["bounded_visual_findings"]) == 4
    ):
        raise ValueError("12RQ_PAGE_SHA_CHAIN_OR_SCOPE_DRIFT")
    blocked = (
        "new_original_juan8_heading_directly_attested",
        "current_p105_121_exclusively_assigned_to_original_juan7",
        "old20_gaizao_louke_original_title_or_glyph_attested",
        "ocr_performed", "complete_linewise_collation_performed",
        "any_target_absence_proven", "fascicle3_target_absence_proven",
        "whole_old20_work_target_absence_proven",
        "print1827_30juan_original_leaf_equivalence_proven")
    if any(v.get(k) is not False for k in blocked):
        raise ValueError("12RQ_UNSUPPORTED_GLYPH_ABSENCE_OR_LINEAGE_CLAIM")
    if not (
        q["previous_batch"] == prev["batch"] == "12RP"
        and q["prior_whole_native_bounded_source_pages"] == pq["new_whole_native_bounded_target_pages"] == 322
        and q["new_whole_native_bounded_source_pages"] == 339
        and q["prior_preview_only_source_pages"] == pq["new_preview_only_source_pages"] == 706
        and q["new_preview_only_source_pages"] == 689
        and q["total_source_pdf_pages"] == 1030
        and q["whole_holding_body_pages"] == 1027
        and q["nonbody_prelim_pages"] == 2
        and q["fascicle3_native_bounded_source_pages"] == 121
        and q["fascicle3_remaining_bounded_first_pass_pages"] == 0
        and q["whole_holding_fulltext_body_collation_pending"] == 1027
        and q["new_whole_native_bounded_source_pages"] + q["new_preview_only_source_pages"] + q["nonbody_prelim_pages"] == q["total_source_pdf_pages"]
        and all(q[k] == 0 for k in ("independent_physical_copy_increment", "new_direct_stemmatic_copy_edges", "algorithm_reopen_count"))
        and d["transmission_impact"]["edges_supported"] == []
        and d["transmission_impact"]["edges_revised"] == []
        and d["invariants"] == {"matrix_rows":222,"audited_rows":222,"provenance_repairs":45,"registered_sources":"647+7=654","md_g03":"OPEN","hpa_dayun_cal_002":"MISSING_FROM_PRODUCT","deterministic_product_r1":"CLOSED","algorithm_reopen_count":0}
    ):
        raise ValueError("12RQ_COMPLETION_COUNTER_OR_PRODUCT_DRIFT")
    return {
        "batch":"12RQ","fascicle3_source_page_bounded_firstpass":"121/121",
        "window_source_jpeg_sha256_pins":len(source_pages),
        "whole_holding_native_bounded":339,
        "whole_holding_preview_only":689,
        "fulltext_body_pages_still_pending":1027,
        "old20_target_presence_or_absence_proven":False
    }

if __name__ == "__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
