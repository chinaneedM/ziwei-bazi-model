#!/usr/bin/env python3
"""12RA: fail-closed page-hash and mixed-leaf checks; visual screening is not negative proof."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RS = ROOT / "docs" / "research"
RECORD = RS / "MING-DATONG-YEHUOBIAN-12RA-NLC411999003250-F1-P23-42-NATIVE-SOURCE-REVIEW-R1.json"
QZ = RS / "MING-DATONG-YEHUOBIAN-12QZ-NLC411999003250-F1-P3-22-NATIVE-SOURCE-REVIEW-R1.json"
QO = RS / "MING-DATONG-YEHUOBIAN-12QO-NLC411999003250-ALL20-CHRONICLE-VOLUME-OPENINGS-R1.json"
PDF_SHA = "acd33a56d2c829fcafd8db1c15b4bb9cb3d3b21905cc8d1e9e9d5a5c45b11939"
ZIP_SHA = "18908565bbcffda40cf2251e747ae37c3b487ce4b0c13a15e0d04cf01fc38429"
STATUS_SHA = "7ba8967f430666612df09b8dfefd312d601b40ac60e35d7cc6f5d08e69b1c070"
CHAIN_SHA = "fef8ffcc685f2c3a83252e4d2eb54b99c26e28e15b5c5a70ee0ac5987224f569"
MIXED35_SHA = "92eaeeafefb06ddd60feb120082445a603a1ff153b3401cc5c87c4296f099732"

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def verify(record_path=RECORD, qz_path=QZ, qo_path=QO):
    data, previous, opening_data = load(record_path), load(qz_path), load(qo_path)
    s, r, q = data["source"], data["review"], data["queue_reconciliation"]
    pz, qz = previous["source"], previous["queue_reconciliation"]
    pins = r["page_image_sha256_in_pdf_order"]
    if not (data["batch"] == "12RA" and data["stage"] == "12QE_OPEN"
            and data["status"] == "TWENTY_ADDITIONAL_NATIVE_SOURCE_JPEG_TARGET_VISUAL_SCREENS_NONEXHAUSTIVE"
            and s["holding"] == pz["holding"] == "NLC411999003250_ONE_HOLDING"
            and s["digital_fascicle"] == 1
            and s["source_pdf_pages"] == pz["source_pdf_pages"] == 119
            and s["source_pdf_sha256"] == pz["source_pdf_sha256"] == PDF_SHA
            and s["artifact_id"] == pz["artifact_id"] == 11674078668
            and s["artifact_zip_sha256"] == pz["artifact_zip_sha256"] == ZIP_SHA
            and s["artifact_status_json_sha256"] == pz["artifact_status_json_sha256"] == STATUS_SHA
            and s["source_pdf_binary_rehashed"] is False
            and s["source_original_jpeg_members_rechecked"] == 20
            and s["image_hash_mismatches"] == 0):
        raise ValueError("12RA_SOURCE_OR_ARCHIVE_BINDING_DRIFT")
    if not (r["mode"] == "INDIVIDUAL_NATIVE_SOURCE_PAGE_VISUAL_HEADING_OR_TARGET_PHRASE_SCREEN"
            and (r["pdf_page_first"], r["pdf_page_last"], r["original_jpeg_pages_individually_opened"]) == (23, 42, 20)
            and len(pins) == 20 and all(len(x) == 64 and all(c in "0123456789abcdef" for c in x) for x in pins)
            and hashlib.sha256("".join(pins).encode("ascii")).hexdigest()
                  == r["page_image_sha256_concatenation_sha256"] == CHAIN_SHA
            and pins[12] == MIXED35_SHA
            and r["page_source_hashes_from"] == "EXACT_PREEXISTING_F1_ARTIFACT_STATUS_JSON_AND_BINARY_REHASH"
            and r["target_original_glyph_positive_attestations"] == 0
            and r["screen_is_bounded_not_complete_text_collation"] is True
            and r["full_text_transcribed"] is False
            and r["ocr_used"] is False
            and r["proof_target_absent_on_any_page"] is False
            and r["proof_target_absent_in_manuscript"] is False):
        raise ValueError("12RA_TARGET_REVIEW_GRADE_OR_PAGE_SHA_DRIFT")
    ownership = r["cross_volume_leaf_ownership"]
    opening = next((x for x in opening_data["original_juan_openings"]
                    if x["digital_fascicle"] == 1 and x["volume"] == 2), None)
    if not (r["cross_volume_page"] == 35
            and ownership == {"right_leaf_original_juan": 1, "left_leaf_original_juan": 2}
            and r["cross_volume_new_juan_heading"] == "萬曆二十七年己亥卷二"
            and r["cross_volume_year"] == 1599
            and r["source_page_cross_volume_not_exclusively_relabelled"] is True
            and opening is not None and opening["pdf_page"] == 35
            and opening["page_jpeg_sha256"] == pins[12]
            and opening["year_label"] == 1599
            and opening["right_leaf_has_previous_volume"] is True):
        raise ValueError("12RA_CROSS_VOLUME_RIGHT_LEFT_LEAF_COLLAPSE")
    expected_old = (49, 979, 979)
    expected_new = (69, 959, 959)
    if not (tuple(qz[k] for k in ("new_native_source_page_screens",
                               "new_preview_only_source_pages",
                               "new_native_body_target_review_backlog")) == expected_old
            and tuple(q[k] for k in ("old_native_source_page_screens",
                                    "old_preview_only_source_pages",
                                    "old_native_body_target_review_backlog")) == expected_old
            and tuple(q[k] for k in ("new_native_source_page_screens",
                                    "new_preview_only_source_pages",
                                    "new_native_body_target_review_backlog")) == expected_new
            and q["body_full_text_collation_backlog"] == qz["body_full_text_collation_backlog"] == 1027
            and q["body_not_even_firstpass_screened"] == 0
            and q["non_body_no_target_screen_pages"] == 2
            and (q["source_pages"], q["body_pages"]) == (1030, 1027)
            and q["fascicle1_new_native_source_screens"] == 40
            and q["fascicle1_preview_only_source_pages"] == 77
            and q["independent_physical_copy_increment"] == 0
            and q["whole_manuscript_negative_proven"] is False
            and data["invariants"]["deterministic_chart_product_r1"] == "CLOSED"
            and data["invariants"]["confirmed_algorithm_reopens"] == 0
            and data["transmission_impact"]["edges_supported"] == []):
        raise ValueError("12RA_QUEUE_FALSE_PROOF_OR_INVARIANT_DRIFT")
    return {"batch": "12RA", "native_screened_source_pages": 69,
            "native_body_review_backlog": 959, "preview_only_source_pages": 959,
            "full_text_collation_backlog": 1027, "mixed_original_juan_pdf_page": 35,
            "whole_manuscript_negative_proven": False}

if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
