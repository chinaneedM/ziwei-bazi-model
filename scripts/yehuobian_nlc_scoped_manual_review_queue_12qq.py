#!/usr/bin/env python3
"""12QQ: hash-bound NLC old20 manual target review queue, NOT full-text collation."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
Q = ROOT / "scripts/yehuobian_nlc_original_volume_locator_12qp.py"
REVIEW = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12QE-NLC-OLD20-V20-NINE-PAGE-BOUNDED-REVIEW-R1.json"

def load_locator():
    spec = importlib.util.spec_from_file_location("nlc_locator_12qp_for_qq", Q)
    loc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loc)
    return loc

def bounded_review(sources, spans, path=REVIEW):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    src = data["source"]
    meta = data["direct_page_review"]
    tenth = sources[9]
    if not (
        src["copy_key"] == "CHINA-NLC-411999003250-FASCICLE10"
        and src["source_pdf_sha256"] == tenth["source_pdf_sha256"]
        and src["source_pdf_pages"] == tenth["source_pdf_pages"] == 145
        and meta["boundary_start_pdf_page"] == 137
        and meta["boundary_end_pdf_page"] == 145
        and meta["preceding_context_pdf_page"] == 136
        and meta["target_heading_seen_within_nine_pages"] is False
        and meta["actual_target_paragraph_separately_detected_within_nine_pages"] is False
        and meta["entire_original_20_volume_work_negatively_searched"] is False
        and meta["target_not_in_any_other_old20_volume"] == "UNRESOLVED"
        and data["comparison"]["do_not_mark_original_work_absent"] is True
    ):
        raise ValueError("PRIOR_BOUNDED_REVIEW_SCOPE_OR_SOURCE_CHANGED")
    page_list = meta["reviewed_pages"]
    if [r["pdf_page"] for r in page_list] != list(range(136, 146)):
        raise ValueError("CONTEXT_AND_TARGET_PAGE_LIST_CHANGED")
    known = {}
    for r in page_list:
        pg, digest = r["pdf_page"], r["derived_jpeg_sha256"]
        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise ValueError("INVALID_PREVIOUSLY_REVIEWED_IMAGE_SHA")
        if pg == 136:
            continue  # Context-only! Not among nine target scans.
        volume20 = [x for x in spans if x["original_volume"] == 20][0]
        if not volume20["start_pdf_page"] <= pg <= volume20["end_pdf_page_inclusive"]:
            raise ValueError("OLD20_TARGET_PAGE_SCOPE_MOVED")
        if pg == 137 and digest != volume20["starting_image_sha256"]:
            raise ValueError("OPENING_HASH_MISMATCH")
        known[pg] = digest
    if len(known) != 9:
        raise ValueError("TARGET_SCAN_COUNT_CHANGED")
    return known

def build_rows():
    loc = load_locator()
    sources, spans = loc.load_index()
    loc.coverage(sources, spans)
    known = bounded_review(sources, spans)
    opener = {(x["fascicle"], x["start_pdf_page"]): x["starting_image_sha256"]
              for x in spans}
    rows = []
    for s in sources:
        f = s["fascicle"]
        for p in range(1, s["source_pdf_pages"] + 1):
            pos = loc.locate_page(sources, spans, f, p)
            checked = f == 10 and p in known
            prelim = not pos["original_volume_candidates"]
            colophon = pos["page_scope"] == "END_COLOPHON_CONTEXT_NOT_CERTIFIED_VOLUME_TEXT"
            sides = {}
            if pos["page_scope"] == "TWO_LEAF_CROSS_VOLUME_BOUNDARY":
                sides = {"right": pos["right_leaf_candidate_volume"],
                         "left": pos["left_leaf_candidate_volume"]}
            rows.append({
                "holding": "NLC411999003250_ONE_HOLDING",
                "fascicle": f, "pdf_page": p,
                "source_pdf_sha256": s["source_pdf_sha256"],
                "page_jpeg_sha256_if_known": known.get(p) if f == 10 and checked
                                                else opener.get((f, p)),
                "original_volume_candidates": pos["original_volume_candidates"],
                "cross_volume_leaf_ownership": sides,
                "page_scope": pos["page_scope"],
                "target_review_status": "PRIOR_NINE_PAGE_BOUNDED_CHECK" if checked
                                        else "TARGET_NOT_MANUALLY_CHECKED",
                "prior_review_source": str(REVIEW.relative_to(ROOT)) if checked else None,
                "body_search_eligible": not prelim and not colophon,
                "needs_target_image_review": not prelim and not colophon and not checked,
                "entire_manuscript_target_absence_proven": False,
                "physical_witness_increment": 0,
            })
    return rows

def summary(rows):
    n = lambda predicate: sum(1 for r in rows if predicate(r))
    out = {
        "source_pages": len(rows),
        "unassigned_preliminary_pages": n(lambda r: not r["original_volume_candidates"]),
        "single_volume_candidate_pages": n(lambda r: len(r["original_volume_candidates"]) == 1),
        "two_leaf_shared_pages": n(lambda r: bool(r["cross_volume_leaf_ownership"])),
        "prior_nine_page_bounded_target_checks": n(lambda r: r["target_review_status"] == "PRIOR_NINE_PAGE_BOUNDED_CHECK"),
        "body_search_eligible_pages": n(lambda r: r["body_search_eligible"]),
        "eligible_prior_bounded_checked_pages": n(lambda r: r["body_search_eligible"] and r["target_review_status"] == "PRIOR_NINE_PAGE_BOUNDED_CHECK"),
        "remaining_target_body_review_queue": n(lambda r: r["needs_target_image_review"]),
        "entire_manuscript_target_absence_proven": False,
        "original_target_folio": "UNLOCATED",
        "new_physical_witnesses": 0,
    }
    expected = (1030, 2, 1020, 8, 9, 1027, 8, 1019)
    if tuple(list(out.values())[:8]) != expected:
        raise ValueError("SOURCE_BOUND_QUEUE_COUNT_DRIFT")
    return out

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--queue", action="store_true")
    ap.add_argument("--fascicle", type=int)
    ap.add_argument("--page", type=int)
    ap.add_argument("--original-volume", type=int)
    ap.add_argument("--limit", type=int, default=20)
    args = ap.parse_args()
    if args.page is not None and args.fascicle is None:
        ap.error("--page requires --fascicle")
    if args.original_volume is not None and not 1 <= args.original_volume <= 20:
        ap.error("UNKNOWN_ORIGINAL_VOLUME")
    if args.fascicle is not None and not 1 <= args.fascicle <= 10:
        ap.error("UNKNOWN_DIGITAL_FASCICLE")
    if args.limit < 1 or args.limit > 1030:
        ap.error("INVALID_PAGE_LIMIT")
    rows = build_rows()
    if args.summary or not (args.queue or args.fascicle is not None or args.original_volume is not None):
        result = summary(rows)
    else:
        rows = [r for r in rows if
                (args.fascicle is None or r["fascicle"] == args.fascicle)
                and (args.page is None or r["pdf_page"] == args.page)
                and (args.original_volume is None or args.original_volume in r["original_volume_candidates"])]
        if args.page is not None and not rows:
            ap.error("PDF_PAGE_OUTSIDE_CAPTURED_SOURCE")
        if args.queue:
            rows = [r for r in rows if r["needs_target_image_review"]]
        result = {"scope": "SOURCE_BOUND_NAVIGATION_NOT_TEXTUAL_NEGATIVE",
                  "pages": rows[:args.limit]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
