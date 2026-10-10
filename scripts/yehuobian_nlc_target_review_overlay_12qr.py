#!/usr/bin/env python3
"""12QR forward-only overlay: add 20 bounded visual screens, never infer absence.

The 12QR source JPEG hashes were checked against the downloaded Actions artifact
status.json at acquisition time; this replay cannot redownload source binaries.
12QQ remains an immutable, independently replayable historical baseline.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QQ_SCRIPT = ROOT / "scripts/yehuobian_nlc_scoped_manual_review_queue_12qq.py"
QR_LEDGER = ROOT / (
    "docs/research/"
    "MING-DATONG-YEHUOBIAN-12QR-NLC411999003250-"
    "F7-OLD12-TWENTY-DIRECT-IMAGE-SCREENS-R1.json"
)


def load_previous_queue():
    spec = importlib.util.spec_from_file_location("yehuobian_12qq_scoped_queue", QQ_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def reconcile(ledger_path=QR_LEDGER):
    old = load_previous_queue()
    pages = old.build_rows()
    assert old.summary(pages)["remaining_target_body_review_queue"] == 1019
    data = json.loads(Path(ledger_path).read_text(encoding="utf-8"))
    src, review = data["source"], data["review"]
    if not (
        data["status"] == "TWENTY_PAGES_DIRECTLY_VISUALLY_SCREENED_TARGET_UNLOCATED_NOT_TRANSCRIBED"
        and src["holding_id"] == "NLC411999003250_ONE_HOLDING"
        and src["digital_fascicle"] == 7
        and src["original_volume_navigation_candidate"] == 12
        and src["source_page_count"] == 110
        and src["artifact_id"] == 11674890925
        and src["artifact_members_verified"] == {
            "page_jpegs": 110, "contact_sheets": 14, "hash_mismatches": 0
        }
        and src["source_pdf_rehashed_this_batch"] is False
        and review["first_pdf_page"] == 1
        and review["last_pdf_page"] == 20
        and review["target_heading"] == "改造漏刻"
        and review["screen_only_not_full_word_by_word_collation"] is True
        and review["any_page_proven_target_absent"] is False
        and review["whole_volume_absence_proven"] is False
        and review["whole_manuscript_absence_proven"] is False
        and review["new_target_positive_attestations"] == 0
    ):
        raise ValueError("SOURCE_REVIEW_SCOPE_DRIFT")
    by_key = {(p["fascicle"], p["pdf_page"]): p for p in pages}
    reviewed = review["screened_pdf_pages"]
    if len(reviewed) != 20:
        raise ValueError("TWENTY_PAGE_SCREEN_REQUIRED")
    expected_keys = [(7, i) for i in range(1, 21)]
    keys = [(x["fascicle"], x["pdf_page"]) for x in reviewed]
    if keys != expected_keys:
        raise ValueError("MISSING_DUPLICATED_OR_NONCONTIGUOUS_REVIEW_PAGE")
    digest_set = []
    for item in reviewed:
        key = (item["fascicle"], item["pdf_page"])
        original = by_key[key]
        digest = item["source_derived_page_jpeg_sha256"]
        if not (
            len(digest) == 64
            and all(k in "0123456789abcdef" for k in digest)
            and item["original_volume_candidates"] == [12]
            and original["original_volume_candidates"] == [12]
            and item["target_status"] == "NO_POSITIVE_TARGET_ATTESTATION_IN_THIS_SCREEN"
            and item["proof_target_absent_on_page"] is False
            and item["review_mode"] == "DIRECT_MANUAL_FULL_PAGE_SCREEN"
            and original["source_pdf_sha256"] == src["source_pdf_sha256"]
            and original["target_review_status"] == "TARGET_NOT_MANUALLY_CHECKED"
            and original["needs_target_image_review"] is True
        ):
            raise ValueError("PHOTO_SHA_OR_TARGET_REVIEW_SCOPE_DRIFT")
        # An already verified first-page opening hash provides an independent
        # local SHA anchor; other 19 hashes are archived direct-review evidence.
        if original["page_jpeg_sha256_if_known"] is not None:
            if original["page_jpeg_sha256_if_known"] != digest:
                raise ValueError("EARLIER_IMAGE_HASH_CONFLICT")
        digest_set.append(digest)
        original["target_review_status"] = "12QR_DIRECT_VISUAL_SCREEN_NO_POSITIVE_ATTESTATION"
        original["page_jpeg_sha256_if_known"] = digest
        original["review_source"] = str(Path(ledger_path).relative_to(ROOT))
        original["needs_target_image_review"] = False
        original["entire_manuscript_target_absence_proven"] = False
        original["physical_witness_increment"] = 0
    chain = hashlib.sha256("".join(digest_set).encode("ascii")).hexdigest()
    if chain != review["source_digest_sequence_sha256"]:
        raise ValueError("SOURCE_PAGE_SHA_CHAIN_DRIFT")
    remaining = sum(p["needs_target_image_review"] for p in pages)
    checked = sum(p["target_review_status"] == "PRIOR_NINE_PAGE_BOUNDED_CHECK"
                  for p in pages)
    screened = sum(p["target_review_status"] == "12QR_DIRECT_VISUAL_SCREEN_NO_POSITIVE_ATTESTATION"
                   for p in pages)
    summary = {
        "source_pages": len(pages),
        "prior_bounded_target_checked_source_pages": checked,
        "new_direct_screened_source_pages": screened,
        "cumulative_target_checked_or_screened_source_pages": checked + screened,
        "body_candidate_pages": sum(p["body_search_eligible"] for p in pages),
        "body_candidate_remaining_unreviewed": remaining,
        "old20_target_original_folio": "UNLOCATED",
        "all_manuscript_pages_line_by_line_collated": False,
        "whole_manuscript_absence_proven": False,
        "new_physical_witness_count": 0,
    }
    if summary != {
        "source_pages": 1030,
        "prior_bounded_target_checked_source_pages": 9,
        "new_direct_screened_source_pages": 20,
        "cumulative_target_checked_or_screened_source_pages": 29,
        "body_candidate_pages": 1027,
        "body_candidate_remaining_unreviewed": 999,
        "old20_target_original_folio": "UNLOCATED",
        "all_manuscript_pages_line_by_line_collated": False,
        "whole_manuscript_absence_proven": False,
        "new_physical_witness_count": 0,
    }:
        raise ValueError("RECONCILED_SOURCE_SCOPE_COUNTS_DRIFT")
    if data["queue_reconciliation"]["remaining_unscreened_body_candidate_pages"] != 999:
        raise ValueError("MACHINE_SNAPSHOT_DISAGREES_WITH_REPLAY")
    return summary, pages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", action="store_true")
    parser.add_argument("--fascicle", type=int)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    if args.fascicle is not None and args.fascicle not in range(1, 11):
        parser.error("UNKNOWN_DIGITAL_FASCICLE")
    if args.limit < 1 or args.limit > 1030:
        parser.error("INVALID_PAGE_LIMIT")
    summary, rows = reconcile()
    if args.queue:
        rows = [x for x in rows if x["needs_target_image_review"] and
                (args.fascicle is None or x["fascicle"] == args.fascicle)]
        result = {"scope": "NAVIGATION_AND_VISUAL_SCREEN_ONLY_NOT_NEGATIVE_PROOF",
                  "pages": rows[:args.limit]}
    else:
        result = summary
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
