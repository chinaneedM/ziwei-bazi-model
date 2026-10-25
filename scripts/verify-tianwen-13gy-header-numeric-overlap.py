#!/usr/bin/env python3
"""13GY: old numeric candidate encloses provisional heading; neither certifies a number."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "docs/research/TIANWEN-13GY-D14-HEADER-NUMERIC-ROI-OVERLAP-R1.json"

def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

def rect_intersection(a, b):
    x1, y1, x2, y2 = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    return [x1, y1, x2, y2] if x2 > x1 and y2 > y1 else None

def area(box):
    return (box[2] - box[0]) * (box[3] - box[1])

def check(e):
    assert e["schema"] == "TIANWEN-13GY-D14-HEADER-NUMERIC-ROI-OVERLAP-R1" and e["issue_id"] == "TW-OPEN-0005"
    assert e["kind"] == "FORWARD_ONLY_SOURCE_NATIVE_ROI_ROLE_OVERLAP_CORRECTION"
    ss = e["source_snapshots"]
    assert len(ss) == 4
    originals = {}
    for s in ss:
        assert s["file"].startswith("docs/research/")
        raw = (ROOT / s["file"]).read_bytes()
        assert git_blob(raw) == s["git_blob_sha"], s["file"]
        originals[s["file"].split("/")[-1][8:12]] = json.loads(raw)
    gr = next(v for k, v in originals.items() if k == "13GR")
    gs = next(v for k, v in originals.items() if k == "13GS")
    gw = next(v for k, v in originals.items() if k == "13GW")
    gx = next(v for k, v in originals.items() if k == "13GX")
    g = e["geometry"]
    c = next(x["source_xyxy"] for x in gr["d14_nested_existing_source_rois"]
             if x["role"] == "D14_UNADJUDICATED_NUMBER_LANE")
    h = next(x["source_xyxy"] for x in gw["scope"]
             if x["role"] == "PRINTED_FOURFEN_COLUMN_HEADING_PROVISIONAL")
    assert g["candidate_xyxy"] == c == next(x["box"] for x in gs["rects"] if x["tag"] == "D14_PREVIOUS_CANDIDATE")
    assert g["header_xyxy"] == h
    assert rect_intersection(c, h) == g["intersection_xyxy"] == h
    assert area(g["intersection_xyxy"]) == g["intersection_area_px2"] == 4212
    assert area(c) == g["candidate_area_px2"] == 9324
    assert [g["header_coverage_of_candidate_numerator"],g["header_coverage_of_candidate_denominator"]] == [117,259]
    assert g["unsegmented_remainder_xyxy"] == [c[0],h[3],c[2],c[3]]
    assert g["uninspected_lower_continuation_xyxy"] == next(x["box"] for x in gs["rects"] if x["tag"] == "D14_UNINSPECTED_LOWER_CONTINUATION")
    assert g["neighbor_chudu_xyxy"] == next(x["box"] for x in gs["rects"] if x["tag"] == "D14_NEIGHBOR_TECHNICAL_COLUMN")
    assert g["intercolumn_gutter_xyxy"] == next(x["box"] for x in gs["rects"] if x["tag"] == "D14_INTERCOLUMN_GUTTER")
    source = e["original_source"]
    assert source["permanent_image"] == gs["source"]["origin"] == gw["source"]["permanent_image"]
    assert source["original_image_rgb_sha256"] == gw["source"]["source_image_rgb_sha256"]
    assert source["original_pdf_sha256"] == gs["source"]["original_pdf_sha256"]
    assert [source["page"],source["xref"]] == [74,291]
    assert source["independent_witnesses_added"] == 0
    interpretation = e["interpretation"]
    assert interpretation["prior_region_is_pure_numeric_roi"] is False
    assert interpretation["prior_region_reclassified"] == "MIXED_PROVISIONAL_PRINTED_HEADER_AND_UNADJUDICATED_REMAINDER"
    assert interpretation["header_reading"] == "四分"
    assert interpretation["header_reading_grade"] == "VISUAL_PROVISIONAL_ONE_SURROGATE"
    for key in ("fourfen_chudu_mechanical_identity","ancient_unit_identity","fully_certified_D14_numeric",
                "original_D14_terminal_glyph","source_specific_numeric_field_identity"):
        assert interpretation[key] is None, key
    for key in ("lower_y680_822_numeric_certified","lower_y822_1060_numeric_certified","new_source_observation"):
        assert interpretation[key] is False, key
    assert interpretation["source_image_source_metadata_reused_only"] is True
    assert interpretation["mechanical_number_interpolation_forbidden"] is True
    assert gx["correction"]["effective_fourfen_chudu_mechanical_identity"] is None
    assert gx["correction"]["effective_fourfen_chudu_ancient_unit_identity"] is None
    u = e["unresolved"]
    assert all(u[k] is None for k in ("old_D9_numeric","old_D14_numeric","old_D30_numeric",
                 "source_physical_folio","printing_layer","original_ancient_unit"))
    assert u["old_D5"] == "〇/五_UNRESOLVED" and u["G893_six"] == "OPEN"
    assert u["prior_13EI"] == "RETRACTED"
    assert e["guards"] == {"matrix":[222,222],"registry":761,"genealogy":[252,238],
                "issues_open":11,"chart":"CLOSED","algorithm_reopens":0,"candidate_collapses":0,
                "new_physical_witnesses":0,"new_original_glyphs":0,"new_transmission_edges":0}
    t = e["transmission_impact"]
    assert all(t[k] == [] for k in ("edges_supported","edges_revised","edges_rejected","non_edges_added"))
    return True

if __name__ == "__main__":
    assert check(json.loads(E.read_text(encoding="utf-8")))
    print("13GY_PASS_ORIGINAL_HEADER_NUMERIC_OVERLAP_NO_PROMOTION")
