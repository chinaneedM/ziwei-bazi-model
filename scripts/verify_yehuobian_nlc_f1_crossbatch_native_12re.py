#!/usr/bin/env python3
"""12RE: replay five source-bound F1 image-review ledgers without upgrading textual evidence."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RE-NLC411999003250-F1-CROSSBATCH-NATIVE-RECONCILIATION-R1.json"
EXPECTED = (
    ("12QZ", 3, 22, "905741bf94a40320e807b31d1da04888c51b7f54bf6503b18be3a5dabc4c5aad"),
    ("12RA", 23, 42, "fef8ffcc685f2c3a83252e4d2eb54b99c26e28e15b5c5a70ee0ac5987224f569"),
    ("12RB", 43, 62, "bd3c8b8474eb1874243df0a53c3477a01f306c76db0c187432003cf47f322f01"),
    ("12RC", 63, 88, "4f20a1e8db05816b4a69a850f3cd7b0f5261a45ccde1fcd53655b0f4351f4cf8"),
    ("12RD", 89, 119, "a53d45e4f6c03bb7a160a46243fa973d001c271bbc6ae3dbc6ce4d628cc88a6e"),
)
SOURCE = {
    "holding": "NLC411999003250_ONE_HOLDING",
    "digital_fascicle": 1,
    "source_pdf_pages": 119,
    "source_pdf_sha256": "acd33a56d2c829fcafd8db1c15b4bb9cb3d3b21905cc8d1e9e9d5a5c45b11939",
    "artifact_id": 11674078668,
    "artifact_zip_sha256": "18908565bbcffda40cf2251e747ae37c3b487ce4b0c13a15e0d04cf01fc38429",
    "artifact_status_json_sha256": "7ba8967f430666612df09b8dfefd312d601b40ac60e35d7cc6f5d08e69b1c070",
}
GUARDS = {
    "total_source_pages": 1030,
    "total_body_pages": 1027,
    "first_fascicle_source_pages": 119,
    "first_fascicle_body_pages": 117,
    "first_fascicle_original_native_visual_target_screen_pages": 117,
    "first_fascicle_prelims_not_target_screened": 2,
    "inherited_other_fascicles_native_source_screens": 29,
    "other_native_screens_include_colophon": True,
    "whole_source_native_screens": 146,
    "whole_source_montage_only_screens": 882,
    "whole_source_nonbody_unscreened_prelims": 2,
    "whole_body_native_target_screen_backlog": 882,
    "whole_body_full_text_collation_backlog": 1027,
    "second_fascicle_native_target_review_pages_pending": 72,
    "second_fascicle_next_window": "f2 p1-72",
    "body_no_firstpass_screened_count": 0,
}
FALSE_CLAIMS = (
    "source_pdf_binary_rehashed_in_12re", "ocr_used_in_12re",
    "full_text_transcribed_in_12re", "any_page_target_absence_proven",
    "whole_work_target_absence_proven", "algorithm_reopened",
)
ZERO_CLAIMS = ("new_original_images_viewed_in_12re", "new_glyph_attestations",
               "new_physical_copies", "new_transmission_edges")


def _read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def verify(record_path=RECORD, replacement_sources=None):
    """Verify scoped metadata, ordered image digests, partition and false-negative guards.

    This does NOT download source ZIPs, visually inspect glyphs or authenticate the
    provenance of the archived JPEG bytes anew. Per-batch binary checks remain distinct.
    """
    record = _read(record_path)
    if not (record["batch"] == "12RE" and record["parent_open_batch"] == "12QE"
            and record["evidence_grade"] ==
            "DERIVED_CROSS_BATCH_METADATA_AND_HASH_LEDGER_REPLAY_NO_NEW_ORIGINAL_IMAGE_VIEWING"):
        raise ValueError("12RE_EVIDENCE_GRADE_DRIFT")
    ident = record["source_identity"]
    for key, value in SOURCE.items():
        if ident.get(key) != value:
            raise ValueError("12RE_PHYSICAL_HOLDING_OR_SOURCE_ARCHIVE_DRIFT")
    if ident.get("source_pages") != 119 or ident.get("body_first_page") != 3 or ident.get("body_last_page") != 119:
        raise ValueError("12RE_F1_SOURCE_RANGE_DRIFT")
    if record["review_accounting"] != GUARDS:
        raise ValueError("12RE_REVIEW_PARTITION_DRIFT")
    guards = record["boundary_guards"]
    if set(guards) != {
        "f1_page35_mixed_original_juan_1_2", "f1_page62_original_juan3_opens",
        "f1_page88_mixed_original_juan_3_4", "f1_page119_one_half_blank",
        "whole_page_must_not_be_assigned_exclusively_at_mixed_boundaries",
    } or not all(value is True for value in guards.values()):
        raise ValueError("12RE_ORIGINAL_JUAN_LEAF_BOUNDARY_DRIFT")
    claims = record["claims"]
    if (any(claims.get(key) is not False for key in FALSE_CLAIMS)
            or any(type(claims.get(key)) is not int or claims[key] != 0 for key in ZERO_CLAIMS)
            or claims.get("original_old20_gaizao_louke_folio") != "UNLOCATED"):
        raise ValueError("12RE_FALSE_TARGET_ABSENCE_OR_NEW_WITNESS_CLAIM")
    inv = record["invariants"]
    if not (inv["product_r1"] == "CLOSED" and inv["matrix_rows"] == inv["audited_rows"] == 222
            and inv["provenance_defects_repaired"] == inv["provenance_defects_confirmed"] == 45
            and inv["external_source_total"] == 654 and inv["md_g03"] == "OPEN"
            and inv["hpa_dayun_cal_002"] == "MISSING_FROM_PRODUCT"
            and inv["algorithm_reopen_count"] == 0):
        raise ValueError("12RE_PRODUCT_OR_SOURCE_COUNTER_DRIFT")
    if len(record["windows"]) != len(EXPECTED):
        raise ValueError("12RE_WINDOW_COUNT_DRIFT")
    replacement_sources = replacement_sources or {}
    covered = []
    read = {}
    for window, (batch, first, last, pinned_digest) in zip(record["windows"], EXPECTED):
        if not (window["batch"] == batch and window["first_page"] == first
                and window["last_page"] == last
                and window["ordered_hash_chain_sha256"] == pinned_digest
                and window["path"].startswith("docs/research/")
                and window["path"].endswith(".json")):
            raise ValueError("12RE_SCOPE_PIN_OR_WINDOW_DRIFT")
        upstream = _read(replacement_sources.get(batch, ROOT / window["path"]))
        source, page = upstream["source"], upstream["review"]
        if upstream["batch"] != batch or upstream["stage"] != "12QE_OPEN":
            raise ValueError("12RE_UPSTREAM_BATCH_IDENTITY_DRIFT")
        if any(source.get(key) != value for key, value in SOURCE.items()):
            raise ValueError("12RE_CROSS_BATCH_SOURCE_BINDING_MISMATCH")
        if source.get("source_pdf_binary_rehashed") is not False:
            raise ValueError("12RE_SOURCE_PDF_REHASH_CLAIM")
        hashes = page[window["page_hashes_field"]]
        if len(hashes) != last - first + 1:
            raise ValueError("12RE_PAGE_HASH_COUNT_MISMATCH")
        if any(not isinstance(h, str) or not re.fullmatch(r"[0-9a-f]{64}", h) for h in hashes):
            raise ValueError("12RE_PAGE_HASH_FORMAT_MISMATCH")
        digest = hashlib.sha256("".join(hashes).encode("ascii")).hexdigest()
        if digest != page[window["ordered_hash_chain_field"]] or digest != pinned_digest:
            raise ValueError("12RE_ORDERED_HASH_CHAIN_MISMATCH")
        if batch == "12RD":
            a, z = page["first_pdf_page"], page["last_pdf_page"]
        else:
            a, z = page["pdf_page_first"], page["pdf_page_last"] if batch != "12RC" else page["last_pdf_page"]
            if batch == "12RC":
                a = page["first_pdf_page"]
        if (a, z) != (first, last):
            raise ValueError("12RE_REVIEW_WINDOW_SOURCE_PAGE_DRIFT")
        if batch in {"12QZ", "12RA", "12RC"}:
            if page["proof_target_absent_in_manuscript"] is not False:
                raise ValueError("12RE_MANUSCRIPT_ABSENCE_PROMOTION")
        if batch == "12RB" and page["negative_manuscript_text_proven"] is not False:
            raise ValueError("12RE_MANUSCRIPT_ABSENCE_PROMOTION")
        if batch == "12RD" and page["whole_manuscript_target_absence_proven"] is not False:
            raise ValueError("12RE_MANUSCRIPT_ABSENCE_PROMOTION")
        covered.extend(range(first, last + 1))
        read[batch] = upstream
    if covered != list(range(3, 120)) or len(covered) != len(set(covered)):
        raise ValueError("12RE_NONCONTIGUOUS_OR_DUPLICATE_PAGE_COVERAGE")
    ra, rb, rc, rd = (read[k]["review"] for k in ("12RA", "12RB", "12RC", "12RD"))
    if not (ra["cross_volume_page"] == 35
            and ra["cross_volume_leaf_ownership"] == {"right_leaf_original_juan": 1, "left_leaf_original_juan": 2}
            and rb["year_1600_original_juan3_start"]["pdf_page"] == 62
            and rb["year_1600_original_juan3_start"]["left_half_volume"] == 3
            and rc["mixed_boundary_page_88"]["right_leaf_continues_original_juan"] == 3
            and rc["mixed_boundary_page_88"]["left_leaf_starts_original_juan"] == 4
            and rc["mixed_boundary_page_88"]["page_jpeg_sha256"] == rc["original_jpeg_sha256_by_pdf_page"][-1]
            and rd["page_119_one_side_blank"] is True
            and rd["page_119_terminal_source_image_sha256"] == rd["page_jpeg_sha256_in_pdf_order"][-1]):
        raise ValueError("12RE_MIXED_ORIGINAL_JUAN_BOUNDARY_OR_TERMINAL_DRIFT")
    last_queue = read["12RD"]["queue"]
    if not (last_queue["new_native_source_pages"] == GUARDS["whole_source_native_screens"]
            and last_queue["new_preview_only_source_pages"] == GUARDS["whole_source_montage_only_screens"]
            and last_queue["new_native_body_target_backlog"] == GUARDS["whole_body_native_target_screen_backlog"]
            and last_queue["whole_manuscript_full_text_body_collation_backlog"] == 1027
            and last_queue["first_fascicle_native_bounded_target_screened"] == 117
            and 117 + 29 == 146
            and 146 + 882 + 2 == 1030):
        raise ValueError("12RE_QUEUE_ARITHMETIC_OR_SOURCE_PAGE_ACCOUNTING_DRIFT")
    return {"batch": "12RE", "source": "NLC411999003250_ONE_HOLDING",
            "fascicle1_native_visual_pages": len(covered), "covered_first": covered[0],
            "covered_last": covered[-1], "crossbatch_gaps": 0, "crossbatch_overlaps": 0,
            "whole_source_native_screens": 146, "remaining_native_body_screen_queue": 882,
            "remaining_full_text_body_collation": 1027, "next_fascicle2_native_pages": 72,
            "new_glyphs_or_absence_proofs": 0}


if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
