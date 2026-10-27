#!/usr/bin/env python3
"""Validate the 12QS NLC f7 four-up montage triage without upgrading its authority.

The upstream Actions artifact retains individual source-JPEG hashes; this
repository snapshot pins its status.json and a concatenated 90-hash chain,
but DOES NOT re-download or rerun human visual interpretation in CI.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RS = ROOT / "docs/research"
QS = RS / "MING-DATONG-YEHUOBIAN-12QS-NLC411999003250-F7-REMAINING90-MONTAGE-TRIAGE-R1.json"
QR = RS / "MING-DATONG-YEHUOBIAN-12QR-NLC411999003250-F7-OLD12-TWENTY-DIRECT-IMAGE-SCREENS-R1.json"
QO = RS / "MING-DATONG-YEHUOBIAN-12QO-NLC411999003250-ALL20-CHRONICLE-VOLUME-OPENINGS-R1.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify_scope(qs_path=QS):
    qs = load(Path(qs_path))
    qr = load(QR)
    qo = load(QO)
    s, v, bounds, queue = (qs["source"], qs["review_scope"],
                           qs["leaf_aware_navigation"], qs["queue_reconciliation"])
    qrs = qr["source"]
    if not (
        qs["status"] == "SOURCE_SHA_BOUND_90_PAGE_DOWNSAMPLED_MONTAGE_VISUAL_TRIAGE_NOT_ORIGINAL_FULL_RES_COLLATION"
        and s["holding"] == "NLC411999003250_ONE_HOLDING"
        and s["fascicle"] == 7 and s["source_pdf_pages"] == 110
        and s["original_artifact_id"] == 11674890925
        and s["original_workflow_run_id"] == 38064436808
        and s["source_pdf_sha256"] == qrs["source_pdf_sha256"]
        and s["artifact_zip_sha256"] == qrs["artifact_zip_sha256"]
        and s["artifact_status_json_sha256"] == qrs["artifact_status_sha256"]
        and s["source_pdf_rehashed_this_round"] is False
        and s["image_integrity"] == {"source_page_jpegs_rehashed": 110,
                                     "contact_sheets_rehashed": 14,
                                     "hash_mismatches": 0}
    ):
        raise ValueError("SOURCE_OR_ARTIFACT_IDENTITY_DRIFT")
    if not (
        v["start_pdf_page"] == 21 and v["end_pdf_page"] == 110
        and v["new_visually_screened_pages"] == 90
        and v["visual_method"] == "4UP_DOWNSAMPLED_FULL_PAGE_MONTAGES_WITH_LEGIBLE_PAGE_HEADINGS_NOT_SINGLE_IMAGE_NATIVE_SIZE"
        and v["max_page_thumbnail_width"] == 1400
        and v["max_page_thumbnail_height"] == 1190
        and v["individually_reopened_full_resolution_source_pages"] == [48,68,110]
        and v["full_text_line_by_line_collated"] is False
        and v["ocr_used"] is False
        and v["original_target_heading"] == "改造漏刻"
        and v["positive_target_glyph_or_passage_attestation_count"] == 0
        and v["does_not_prove_absence_of_target_on_screened_pages"] is True
        and v["does_not_prove_absence_in_whole_work"] is True
        and v["page_sequence_hash_encoding"].startswith("sha256(lowercase ASCII concatenation")
    ):
        raise ValueError("VISUAL_REVIEW_SCOPE_OR_ABSENCE_FIREWALL_DRIFT")
    hexdigest = lambda h: isinstance(h, str) and re.fullmatch(r"[0-9a-f]{64}", h) is not None
    if not hexdigest(v["page_sequence_hash_sha256"]):
        raise ValueError("MISSING_SOURCE_PAGE_SHA_CHAIN")
    heads = {z["volume"]: z for z in qo["original_juan_openings"]}
    if not (
        heads[13]["digital_fascicle"] == heads[14]["digital_fascicle"] == 7
        and heads[13]["pdf_page"] == 48
        and heads[14]["pdf_page"] == 68
        and heads[14]["right_leaf_has_previous_volume"] is True
        and v["original_full_image_anchor_sha256"]["48"] == heads[13]["page_jpeg_sha256"]
        and v["original_full_image_anchor_sha256"]["68"] == heads[14]["page_jpeg_sha256"]
        and hexdigest(v["original_full_image_anchor_sha256"]["110"])
    ):
        raise ValueError("CROSS_LEAF_OR_MANUSCRIPT_OPENING_IMAGE_DRIFT")
    if not (
        (bounds["f7_pages_21_to_47_volume12"],
         bounds["f7_pages_48_to_67_volume13"],
         bounds["f7_page_68_mixed_original_volume13_right_volume14_left"],
         bounds["f7_pages_69_to_110_volume14"]) == (27,20,1,42)
        and bounds["source_page_48_heading"] == "萬曆三十八年庚戌卷十三"
        and bounds["source_page_68_left_heading"] == "萬曆三十九年辛亥卷十四"
    ):
        raise ValueError("CHRONOLOGICAL_VOLUME_CROSSWALK_DRIFT")
    if not (
        qr["queue_reconciliation"]["remaining_unscreened_body_candidate_pages"] == 999
        and qr["review"]["first_pdf_page"] == 1
        and qr["review"]["last_pdf_page"] == 20
        and queue == {
            "source_pages_total": 1030,
            "eligible_body_pages_total": 1027,
            "inherited_nine_page_bounded_target_check": 9,
            "inherited_12qr_native_individual_page_screen": 20,
            "new_12qs_fourup_preview_pages": 90,
            "source_pages_with_any_bounded_target_visual_screen": 119,
            "remaining_not_even_firstpass_screened_source_body_pages": 909,
            "still_requires_individual_native_source_page_target_review": 999,
            "old20_gaizao_louke_original_folio": "UNLOCATED",
        }
    ):
        raise ValueError("QUANTIFIED_VISUAL_TRIAGE_VS_NATIVE_REVIEW_DRIFT")
    if qs["invariants"]["algorithm_reopens"] != 0 or qs["invariants"]["product_r1"] != "CLOSED":
        raise ValueError("CLOSED_PRODUCT_GATE_DRIFT")
    return {"firstpass_source_pages_including_prior_scans": 119,
            "still_requires_individual_native_pages": 999,
            "f7_fourup_source_pages_this_batch": 90,
            "f7_cross_volume_page": 68,
            "absence_proven": False,
            "new_independent_physical_witnesses": 0}


if __name__ == "__main__":
    print(json.dumps(verify_scope(), ensure_ascii=False, indent=2))
