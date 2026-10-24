#!/usr/bin/env python3
"""13ES: verify pre-existing source ROI geometry only; do not infer original ink or historical numbers."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13ES-NCL03130-D1-D6-ROI-OVERLAP-GEOMETRY-FIREWALL-R1.json"
ER="docs/research/TIANWEN-13ER-NCL03130-P73-D1-D3-FOURFEN-BOUNDED-ORIGINAL-R1.json"
EQ="docs/research/TIANWEN-13EQ-NCL03130-P73-D1-D3-ORIGINAL-CHUDU-STRIPS-R1.json"
EN="docs/research/TIANWEN-13EN-NCL03130-P74-FOURFEN-D4-D6-BOUNDED-PREFIX-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
EXPECTED=[(1,73,13,4420,14),(2,73,10,3050,18),(3,73,6,1824,21),(4,74,2,428,24),(5,74,6,1560,20),(6,74,6,1596,23)]
def read(p):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))
def geom(a,b):
    x=max(0,min(a[2],b[2])-max(a[0],b[0]))
    y=max(0,min(a[3],b[3])-max(a[1],b[1]))
    return x,x*y,b[0]-a[0]
def check(e,er,eq,en,s,l):
    assert e["schema"]=="TIANWEN-13ES-NCL03130-D1-D6-ROI-OVERLAP-GEOMETRY-FIREWALL-R1"
    assert e["issue_id"]=="TW-OPEN-0005" and e["evidence_grade"].startswith("DERIVED_COORDINATE_GEOMETRY")
    source=e["shared_source"]
    assert source["pdf_sha256"]==er["source"]["pdf_sha256"]==eq["source"]["pdf_sha256"]==en["source"]["pdf_sha256"]
    assert source["page73_png_sha256"]==er["source"]["png_sha256"]==eq["source"]["png_sha256"]
    assert source["page74_png_sha256"]==en["source"]["png_sha256"]
    assert source["archived_action_run"]==er["source"]["run"]==eq["source"]["run"]
    assert source["archived_artifact_id"]==er["source"]["artifact_id"]==eq["source"]["artifact_id"]
    assert source["physical_copy_binding"]=="UNBOUND" and source["independent_witnesses_added"]==0
    assert len(e["per_day_pairs"])==6 and len(e["upstream_records"])==3
    assert [v["path"] for v in e["upstream_records"]]==[ER,EQ,EN]
    for rec,(day,page,x,area,delta) in zip(e["per_day_pairs"],EXPECTED):
        f=next(z for z in (er["rois"] if page==73 else en["rois"]) if z["name"]==(f"P73_D{day}_FOURFEN" if page==73 else f"D{day}_FOURFEN_PREFIX"))
        c=next(z for z in (eq["rois"] if page==73 else en["rois"]) if z["name"]==(f"P73_D{day}_CHUDU" if page==73 else f"D{day}_CHUDU_CONTROL"))
        assert (rec["day"],rec["pdf_page"])==(day,page)
        assert rec["fourfen_roi_name"]==f["name"] and rec["chudu_roi_name"]==c["name"]
        assert rec["fourfen_bbox"]==f["bbox"] and rec["chudu_bbox"]==c["bbox"]
        assert rec["fourfen_rgb_sha256"]==f["rgb_sha256"] and rec["chudu_rgb_sha256"]==c["rgb_sha256"]
        assert geom(f["bbox"],c["bbox"])==(x,area,delta)
        assert (rec["bbox_x_overlap_px"],rec["bbox_xy_intersection_pixels"],rec["fourfen_left_of_chudu_start_px"])==(x,area,delta)
        assert rec["ink_intersection_proven"] is False and rec["mechanical_field_equivalence_proven"] is False
    a=e["adjudication"]
    assert a["bbox_pairs_with_nonzero_overlap"]==a["day_count"]==6
    assert a["all_fourfen_crop_left_edges_precede_chudu_crop_left_edges"] is True
    assert a["overlap_of_crop_rectangles_does_not_prove_glyph_ink_overlap"] is True
    assert a["overlap_of_crop_rectangles_does_not_prove_misattribution"] is True
    assert a["printed_heading_to_daily_value_lanes"]=="UNPROVEN" and a["day1_explicit_fen_semantics"]=="UNBOUND"
    assert a["complete_fourfen_historical_decimal_values"]==[None]*6
    assert a["original_full_fourfen_rows_proven"]==[False]*6
    assert a["p76_solar_d30_numeric"] is None and a["winter_d16_numeric"] is None
    assert a["g893_six_original_controls"]=="OPEN" and a["ncl_qing_vs_1905_copy_identity"]=="UNBOUND"
    assert a["prior_13ei_erratum"]=="STILL_RETRACTED"
    i=e["impact"]
    assert all(i[k]==0 for k in ("matrix_rows_changed","registry_sources_added","genealogy_nodes_added","genealogy_edges_added","risks_closed","algorithm_reopens"))
    assert i["chart_product"]=="CLOSED" and i["risks_open_or_blocked"]==11
    assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
    assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
    assert any(z.startswith("13ES ") for z in s["historical_audit"]["current_focus"])
    issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
    assert issue["priority"]=="P0" and issue["status"]=="OPEN"
    assert issue["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
    assert all(z in issue["next_action"] for z in ("D1","D2","D3","D4","D5","D6","D30","四分","初度","NULL"))
    assert {E,E.replace(".json",".md")}.issubset(set(issue["source_refs"]))
    rev=next(z for z in issue["history"] if z.get("revision_id")=="TW-OPEN-0005-13ES-ROI-GEOMETRY-20261024")
    assert rev["previous_next_action"].startswith("13ER CURRENT ACTION:")
    assert set(rev["changed_fields"])=={"source_refs","next_action"}
    assert len(l["issues"])==11 and l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
    return True
if __name__=="__main__":
    assert check(read(E),read(ER),read(EQ),read(EN),read(S),read(L))
    print("13ES_PASS BBOX_OVERLAP_D1_D6_SOURCE_GEOMETRY_ONLY_NUMERICS_UNBOUND")
