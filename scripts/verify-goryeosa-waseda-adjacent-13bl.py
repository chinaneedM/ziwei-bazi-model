#!/usr/bin/env python3
"""13BL original-source acquisition identity and omission-forward-only scope verifier."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13BL-GORYEOSA-WASEDA-ADJACENT-P24-P25-ORIGINAL-FOLIO-ACQUISITION-R1.json"
MD="docs/research/TIANWEN-13BL-GORYEOSA-WASEDA-ADJACENT-P24-P25-ORIGINAL-FOLIO-ACQUISITION-R1.md"
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check(e,ledger,state):
 assert e["schema"]=="TIANWEN-13BL-WASEDA-ADJACENT-FOLIO-SOURCE-CAPTURE-AND-PREVIEW-SCREEN-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["date"]=="2026-10-21"
 assert e["grade"]=="SOURCE_SHA_VERIFIED_ORIGINAL_JPEG_ACQUIRED_PREVIEW_HEADING_SCREEN_NO_NATIVE_NUMERIC_ROI"
 src=e["source"]
 assert src["physical_holding"]=="WASEDA-RI06-02809-BOOK33"
 assert src["provider_pdf"].startswith("https://archive.wul.waseda.ac.jp/kosho/ri06/ri06_02809/")
 assert src["provider_pdf_sha256"]=="28ebfeb34191f45715bc449d27da61fe04fb05eb45e84dd00cf569699f46225f"
 assert src["provider_pdf_bytes"]==58769815 and src["provider_pdf_pages"]==85
 assert src["original_capture_run"]==39547966390 and src["original_capture_artifact"]==12322497620
 assert src["original_capture_url"]=="https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/39547966390"
 assert src["acquisition_commit"]=="9d8b162f3ee6fe9f934faa4201ba366960f37faf"
 assert src["script"]=="scripts/probe-goryeosa-waseda-adjacent-13bl.py" and src["workflow"]==".github/workflows/probe-goryeosa-waseda-adjacent-13bl.yml"
 expected=[
 (24,73,"913368872d9a7589abf88a4ae9b8d87ca4b836cc27c0d66d21b8ba82022e1574",690293,"7202517581d6a9ecd18fe134851d60c61166c11223e43b055f31c437aa4be1da",21,29),
 (25,76,"ac19365a36456f0a550dd85873c0a006cee37765a352aa2b23d37137b5478646",680130,"4b628cfd4cf69d1748772c6fbd770c64ae8cc76fb2f7391afc3e4fe423f7fb9b",30,38)]
 assert len(e["original_embedded_images"])==len(expected)
 for row,exp in zip(e["original_embedded_images"],expected):
  assert (row["pdf_page_1based"],row["embedded_xref"],row["original_jpeg_sha256"],
          row["image_bytes"],row["preview_sha256"])==exp[:5]
  assert row["image_dimensions"]==[2592,1728]
  assert row["visibility_grade"]=="SOURCE_DERIVED_DOWNSAMPLED_PREVIEW_HEADING_ONLY"
  assert len(row["visually_observed_headings_right_to_left"])==exp[6]-exp[5]+1
 assert e["original_embedded_images"][0]["visually_observed_headings_right_to_left"][0]=="二十一日"
 assert e["original_embedded_images"][1]["visually_observed_headings_right_to_left"][0]=="三十日"
 bound=e["bounded_interpretation"]
 assert bound["waseda_day21_original_source_page_locator"]=="PDF_PAGE_24_SOURCE_IMAGE_XREF73_POSITIVE"
 assert bound["source_images_acquired"] is True and bound["day21_heading_visually_located"] is True
 assert bound["day21_original_cumulative_numeric_direct_native_collation"]=="NOT_PERFORMED"
 assert bound["original_day21_cumulative_value"] is None
 assert bound["original_day20_to21_delta_direct_native_collation"]=="NOT_PERFORMED"
 assert bound["global_day_index_and_table_start_end"]=="UNADJUDICATED"
 assert bound["comparison_to_NAJ_D21_original"]=="NOT_YET_NATIVE_NUMERIC_COLLATION"
 assert bound["proof_of_stemmatic_independence"] is False
 assert bound["new_historical_numeric_vote"] is False
 assert bound["automatically_inferred_glyph_readings"] is False
 assert bound["text_absence_from_unreviewed_images_proven"] is False
 assert bound["acquisition_not_equal_target_adjudication"] is True
 counts=e["scope_counters"]
 assert counts["original_embedded_JPEG_objects_acquired"]==2
 for k in ("new_physical_historical_witnesses","independent_numerical_votes","external_registry_sources_added",
           "matrix_rows_added","transmission_nodes_added","transmission_edges_added","chart_algorithm_reopens"):
  assert counts[k]==0
 assert counts["research_omission_issues_open_or_blocked"]==11 and counts["deterministic_product"]=="CLOSED"
 tr=e["transmission_impact"]
 assert tr["nodes_added_or_strengthened"]==tr["edges_supported"]==tr["edges_revised"]==[]
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert issue["source_refs"].count(MD)==issue["source_refs"].count(P)==1
 assert issue["source_refs"].index(P)==issue["source_refs"].index(MD)+1
 h=next(x for x in issue["history"] if x.get("revision_id")=="TW-OPEN-0005-WASEDA-P24-P25-ORIGINAL-SOURCE-13BL")
 assert h["event"]=="ISSUE_REVISION" and set(h["changed_fields"])=={"evidence_boundary","missing_evidence","next_action"}
 assert h["previous_next_action"].startswith("13BK CURRENT ACTION")
 assert {MD,P,"scripts/probe-goryeosa-waseda-adjacent-13bl.py",".github/workflows/probe-goryeosa-waseda-adjacent-13bl.yml"}.issubset(set(h["evidence_refs"]))
 assert "[13BL 2026-10-21 WASEDA ADJACENT ORIGINAL IMAGE POSITIVE]" in issue["evidence_boundary"]
 assert "[13BL 2026-10-21 REMAINING NATIVE PIXEL NUMERIC REVIEW]" in issue["missing_evidence"]
 later_revs=[
    z for z in issue["history"][issue["history"].index(h)+1:]
    if z.get("event")=="ISSUE_REVISION" and "next_action" in z.get("changed_fields",[])]
 prefix=ledger["binding"]["latest_research_focus_prefix"]
 active=issue["next_action"]
 family=active.split(" CURRENT ACTION",1)[0]
 # Project focus may progress beyond the issue's latest evidenced action.
 # Prevent false resurrection of obsolete actions and fabricated families:
 # an actual later issue revision for the family (or synthetic append-only
 # future test at current focus) must exist.
 recorded=any(
    ("-"+family+"-") in z.get("revision_id","")
    or (not z.get("revision_id") and prefix==family)
    for z in later_revs)
 assert active.startswith("13BL CURRENT ACTION") or (
    bool(later_revs) and prefix!="13BL"
    and active.startswith(family+" CURRENT ACTION")
    and recorded
    and any(x.startswith(family+" ") for x in state["historical_audit"]["current_focus"]))
 assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert any(t.startswith("13BL ") for t in state["historical_audit"]["current_focus"])
 assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
 assert prefix==state["historical_audit"]["current_focus"][-1].split(" ")[0]
 assert ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"]
 assert set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])=={x["id"] for x in ledger["issues"]}
 assert (ROOT/MD).is_file()
 return True
if __name__=="__main__":
 assert check(load(P),load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"),load("docs/PROJECT-CURRENT-STATE-R1.json"))
 print("Goryeosa 13BL Waseda adjacent original source images and no-numeric-promotion gate PASS")
