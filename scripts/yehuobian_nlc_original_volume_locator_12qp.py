#!/usr/bin/env python3
"""Conservative, leaf-aware locator for NLC-411999003250 manuscript juan.

No OCR and no page-level text inference. Page ranges between verified headings
are navigation candidates, not proof that an article exists or is absent.

Examples:
 python scripts/yehuobian_nlc_original_volume_locator_12qp.py --fascicle 7 --page 68
 python scripts/yehuobian_nlc_original_volume_locator_12qp.py --original-volume 14
 python scripts/yehuobian_nlc_original_volume_locator_12qp.py --coverage
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
QO_PATH = REPO / "docs/research/MING-DATONG-YEHUOBIAN-12QO-NLC411999003250-ALL20-CHRONICLE-VOLUME-OPENINGS-R1.json"
QL_PATH = REPO / "docs/research/MING-DATONG-YEHUOBIAN-12QL-NLC411999003250-TEN-FASCICLE-BINARY-CAPTURE-RECONCILIATION-R1.json"


def load_index(qo_path: Path = QO_PATH, ql_path: Path = QL_PATH):
    qo = json.loads(qo_path.read_text(encoding="utf-8"))
    ql = json.loads(ql_path.read_text(encoding="utf-8"))
    headings = qo["original_juan_openings"]
    sources = ql["sources"]
    assert qo["holding"] == "NLC411999003250_ONE_HOLDING"
    assert ql["holding_id"] == "NLC-411999003250"
    assert len(headings) == 20 and len(sources) == 10
    assert [r["volume"] for r in headings] == list(range(1, 21))
    assert [s["fascicle"] for s in sources] == list(range(1, 11))
    assert not qo["unresolved"]["absence_of_target_proved"]
    spans = []
    for src in sources:
        fascicle, total_pages = src["fascicle"], src["source_pdf_pages"]
        local = [r for r in headings if r["digital_fascicle"] == fascicle]
        assert local and local == sorted(local, key=lambda r: r["pdf_page"])
        assert len({r["pdf_page"] for r in local}) == len(local)
        for i, row in enumerate(local):
            following = local[i + 1] if i + 1 < len(local) else None
            last_page = (
                following["pdf_page"] - (0 if following["right_leaf_has_previous_volume"] else 1)
                if following else total_pages
            )
            assert 1 <= row["pdf_page"] <= last_page <= total_pages
            if row["right_leaf_has_previous_volume"]:
                assert i > 0, "Source fascicle cannot share prior volume outside its image"
            spans.append({
                "original_volume": row["volume"],
                "fascicle": fascicle,
                "start_pdf_page": row["pdf_page"],
                "end_pdf_page_inclusive": last_page,
                "starting_image_sha256": row["page_jpeg_sha256"],
                "opening_heading_directly_seen": True,
                "interior_pages_textually_collated": False,
                "first_page_right_leaf_has_previous_volume": row["right_leaf_has_previous_volume"],
                "navigation_only_not_article_attestation": True,
            })
    assert len(spans) == 20
    return sources, spans


def locate_page(sources, spans, fascicle: int, pdf_page: int):
    src = next((s for s in sources if s["fascicle"] == fascicle), None)
    if src is None:
        raise ValueError("UNKNOWN_DIGITAL_FASCICLE")
    if not 1 <= pdf_page <= src["source_pdf_pages"]:
        raise ValueError("PDF_PAGE_OUTSIDE_CAPTURED_SOURCE")
    candidate = [s for s in spans if s["fascicle"] == fascicle
                 and s["start_pdf_page"] <= pdf_page <= s["end_pdf_page_inclusive"]]
    if len(candidate) > 2:
        raise ValueError("MORE_THAN_TWO_ORIGINAL_VOLUME_CANDIDATES")
    result = {
        "physical_holding": "NLC411999003250_ONE_HOLDING",
        "digital_fascicle": fascicle,
        "pdf_page": pdf_page,
        "original_volume_candidates": [s["original_volume"] for s in candidate],
        "level": "NAVIGATION_ONLY_NOT_MANUSCRIPT_PASSAGE_COLLATION",
        "can_assert_target_absence": False,
    }
    if not candidate:
        result["page_scope"] = "PRELIM_OR_UNASSIGNED_OUTSIDE_INDEXED_VOLUME_OPENINGS"
    elif len(candidate) == 1:
        if fascicle == 10 and pdf_page == 145:
            result["page_scope"] = "END_COLOPHON_CONTEXT_NOT_CERTIFIED_VOLUME_TEXT"
        else:
            result["page_scope"] = (
                "OPENING_HEADING_IMAGE" if pdf_page == candidate[0]["start_pdf_page"]
                else "INFERRED_VOLUME_INTERVAL_NOT_LINE_BY_LINE_VERIFIED"
            )
    else:
        if candidate[1]["start_pdf_page"] != pdf_page or not candidate[1]["first_page_right_leaf_has_previous_volume"]:
            raise ValueError("OVERLAPPING_VOLUMES_WITHOUT_DIRECT_MIXED_LEAF_ATTESTATION")
        result["page_scope"] = "TWO_LEAF_CROSS_VOLUME_BOUNDARY"
        result["right_leaf_candidate_volume"] = candidate[0]["original_volume"]
        result["left_leaf_candidate_volume"] = candidate[1]["original_volume"]
    return result


def locate_volume(spans, volume: int):
    row = next((s for s in spans if s["original_volume"] == volume), None)
    if row is None:
        raise ValueError("UNKNOWN_ORIGINAL_VOLUME")
    return dict(row)


def coverage(sources, spans):
    counts = {"source_pages": 0, "unassigned_prelim": 0, "one_candidate": 0,
              "two_leaf_shared": 0, "volume_page_incidence": 0, "invalid_coverage": 0}
    for src in sources:
        for page in range(1, src["source_pdf_pages"] + 1):
            row = locate_page(sources, spans, src["fascicle"], page)
            n = len(row["original_volume_candidates"])
            counts["source_pages"] += 1
            counts["volume_page_incidence"] += n
            if n == 0:
                counts["unassigned_prelim"] += 1
                if src["fascicle"] != 1 or page not in (1, 2):
                    counts["invalid_coverage"] += 1
            elif n == 1:
                counts["one_candidate"] += 1
            elif n == 2 and row["page_scope"] == "TWO_LEAF_CROSS_VOLUME_BOUNDARY":
                counts["two_leaf_shared"] += 1
            else:
                counts["invalid_coverage"] += 1
    assert counts == {"source_pages": 1030, "unassigned_prelim": 2,
                      "one_candidate": 1020, "two_leaf_shared": 8,
                      "volume_page_incidence": 1036, "invalid_coverage": 0}
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--original-volume", type=int)
    group.add_argument("--coverage", action="store_true")
    group.add_argument("--fascicle", type=int)
    parser.add_argument("--page", type=int)
    args = parser.parse_args()
    if (args.fascicle is None) != (args.page is None):
        parser.error("--fascicle and --page must be provided together")
    sources, spans = load_index()
    try:
        if args.coverage:
            result = coverage(sources, spans)
        elif args.original_volume is not None:
            result = locate_volume(spans, args.original_volume)
        else:
            result = locate_page(sources, spans, args.fascicle, args.page)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
