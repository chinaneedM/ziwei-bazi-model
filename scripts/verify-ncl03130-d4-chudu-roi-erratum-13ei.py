#!/usr/bin/env python3
"""13EI fail-closed visual glyph identity erratum, replay by archival RGB hashes."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13EI-NCL03130-D4-MISATTRIBUTED-CHUDU-ROI-ERRATUM-R1.json"; EH="docs/research/TIANWEN-13EH-NCL03130-SOLAR-D4-D30-PREFIX-LANE-GEOMETRY-R1.json";EG="docs/research/TIANWEN-13EG-NCL03130-SOLAR-FOLIO-DAY-BOUNDARIES-R1.json";ED="docs/research/TIANWEN-13ED-NCL03130-SOLAR-D30-EXTENDED-ORIGINAL-STRIP-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json";LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
EXPECTED={
 "p74_invalid_claimed_chudu_strip":(74,[929,396,951,785],"b86ee0c9fea7e8597ee2f05d2785fbfffe2aa3f68717e8643c6d8c1592fcc22c"),
 "p74_nearby_chudu_candidate_strip":(74,[958,396,982,785],"8bf39d5285c9a04980d0e9aba9ba425b9ff8d3ff0a711da5828b281b9753d5a7"),
 "p74_invalid_header_segment":(74,[929,403,951,520],"98bf429302771cace163f22a98afce705250237bf797a53ebd8fbe2e015f59bd"),
 "p74_nearby_chudu_header_segment":(74,[958,403,982,520],"2ff43928c468a342d18e98b3611b37383d62473e83efa0f0829da5aff9347ad1"),
 "p74_context_wide_panel":(74,[884,395,997,795],"a0b9f5fcab41c52756162da535da1cbc78701e6bedb9fdd0632c8fc9a346d2b4"),
 "p74_day4_source_heading":(74,[885,150,951,300],"dac2d4865d428da1a875428c6542a24b5192ac05b0bcb49799d6ed625b23bb38"),
 "p76_preserved_day30_literal":(76,[590,418,615,830],"bc91212e7b7a6a98f67913788e0051c3eabfd5af46982aa26f90a3339cf0efd4"),
 "p76_source_day30_multicolumn_panel":(76,[549,418,647,830],"b5b6769e552a7c05412b925add3490db8a11993f6a58baf650870f772ef6fab3"),
 "p73_original_technical_heading":(73,[325,392,459,622],"2cc22963cef125259bb01bd99eeb05e1848bec1f27c7a62cb34d1f801f3b7d19")
}
def read(path):return json.loads((ROOT/path).read_text(encoding="utf8"))
def check(e,s,l,eh,eg,ed):
 assert e["schema"]=="TIANWEN-13EI-NCL03130-D4-MISATTRIBUTED-CHUDU-ROI-ERRATUM-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["event"]=="FORWARD_ONLY_ORIGINAL_IMAGE_GLYPH_IDENTITY_ERRATUM"
 assert e["predecessor"]==EH
 src=e["source"]
 assert src["pdf_sha256"]==eh["source"]["pdf_sha256"]==eg["source"]["pdf_sha256"]==ed["source"]["pdf_sha256"]
 assert src["archive_run_id"]==eh["source"]["archive_workflow_run"]==eg["source"]["archive_workflow_run"]
 assert src["archive_artifact_id"]==eh["source"]["artifact_id"]==eg["source"]["archive_artifact_id"]
 assert src["ocr_used"] is False and src["physical_copy"]==src["qing_vs_1905_stratum"]=="UNBOUND"
 assert src["new_independent_physical_witnesses"]==0
 assert [p["pdf_page"] for p in src["pages"]]==[73,74,76]
 for page in src["pages"]:
  o=next(z for z in eg["pages"] if z["pdf_page"]==page["pdf_page"])
  assert page["png_sha256"]==o["png_sha256"] and page["rgb_sha256"]==o["rgb_sha256"] and page["size"]==o["png_size"]
 rois=e["rois"]
 assert len(rois)==len(EXPECTED)==9
 assert set(x["name"] for x in rois)==set(EXPECTED)
 for x in rois:
  assert (x["pdf_page"],x["bbox"],x["rgb_sha256"])==EXPECTED[x["name"]]
  assert x["source_grade"]=="BOUNDED_ORIGINAL_PIXEL_RGB_SHA_AND_VISUAL_ONLY"
 error=e["error"];fix=e["replacement"]
 prior=next(z for z in eh["pages"][1]["rois"] if z["name"]=="day4_visible_chudu_prefix_strip")
 assert prior["bbox"]==error["prior_bbox"]==EXPECTED["p74_invalid_claimed_chudu_strip"][1]
 assert prior["rgb_sha256"]==EXPECTED["p74_invalid_claimed_chudu_strip"][2]
 assert prior["visible_prefix"]==error["historical_recorded_prefix"]=="初度"
 assert error["actual_visible_opening"]=="四分" and error["adjudication"]=="REJECTED_SOURCE_GLYPH_MISATTRIBUTION"
 assert error["invalidate"]=="13EH_SOURCE_LOCAL_CHUDU_PREFIX_PAIR_AND_1PX_OFFSET_CONCORDANCE"
 assert error["preserve_original_13eh_record"] is True and error["correction_is_not_silent_rewrite"] is True
 assert fix["candidate_bbox"]==EXPECTED["p74_nearby_chudu_candidate_strip"][1]
 assert fix["candidate_opening"]=="初度"
 assert fix["candidate_scope"]=="P74_SAME_PAGE_NEIGHBOR_SOURCE_GLYPH_CANDIDATE_ONLY"
 assert fix["original_heading_四日_bbox"]==eg["pages"][1]["boundaries"][0]["bbox"]
 assert fix["revised_nominal_candidate_offset_px"]==52
 assert fix["original_13eh_invalid_offset_px"]==eh["relative_column_observation"]["day4"]["offset_px"]==22
 assert fix["previous_p76_offset_px"]==eh["relative_column_observation"]["day30"]["offset_px"]==21
 assert fix["normalized_pair_geometry"]=="RETRACTED_NOT_ADMISSIBLE"
 assert fix["day4_semantic_full_field_identity"]=="UNRESOLVED" and fix["alternate_column_blending"] is False
 assert fix["original_p76_day30_positive"]==ed["finding"]["d30_visible_glyph_group"]=="初度九十六二〇三"
 assert fix["original_p76_day30_numeric"] is None
 limits=e["limits"]
 assert limits["complete_day4_row_transcribed"] is False and limits["technical_label_to_day4_row_binding"]=="UNRESOLVED"
 assert limits["day30_exact_decimal"] is None and limits["source_independent_hands"]=="UNBOUND"
 assert limits["scribal_error_claim"]=="UNPROVEN" and limits["ocr_used"] is False and limits["new_numeric_interpretation"] is False
 impact=e["impact"];assert impact["risk_issues_open_or_blocked"]==11 and impact["chart"]=="CLOSED"
 assert all(impact[k]==0 for k in ("matrix_rows_changed","source_registry_entries_added","independent_physical_copy_votes","genealogy_nodes_added","genealogy_edges_added","algorithm_reopens","risk_issues_closed"))
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13EI FORWARD-ONLY ORIGINAL P74 GLYPH ERRATUM") for x in s["historical_audit"]["current_focus"])
 q=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
 assert q["priority"]=="P0" and q["status"]=="OPEN" and q["next_action"].startswith("13EI CURRENT ACTION")
 assert all(z in q["next_action"] for z in ("四分","初度","D30","NULL"))
 assert {E,E.replace(".json",".md")}.issubset(set(q["source_refs"]))
 h=next(x for x in q["history"] if x.get("revision_id")=="TW-OPEN-0005-13EI-GLYPH-LANE-FORWARD-ERRATUM-20261023")
 assert h["previous_next_action"].startswith("13EH CURRENT ACTION")
 assert set(h["changed_fields"])=={"source_refs","next_action"}
 assert {E,E.replace(".json",".md"),EH,EG,ED}.issubset(set(h["evidence_refs"]))
 assert len(l["issues"])==11 and l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
def replay(e,folder):
 from PIL import Image
 root=Path(folder)
 for p in e["source"]["pages"]:
  fn=root/f'original-p{p["pdf_page"]:03d}.png'
  assert hashlib.sha256(fn.read_bytes()).hexdigest()==p["png_sha256"]
  with Image.open(fn) as i: rgb=i.convert("RGB")
  assert list(rgb.size)==p["size"] and hashlib.sha256(rgb.tobytes()).hexdigest()==p["rgb_sha256"]
  for roi in e["rois"]:
   if roi["pdf_page"]==p["pdf_page"]:
    assert hashlib.sha256(rgb.crop(tuple(roi["bbox"])).tobytes()).hexdigest()==roi["rgb_sha256"],roi["name"]
 return True
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--source-dir");a=ap.parse_args()
 e=read(E);assert check(e,read(STATE),read(LEDGER),read(EH),read(EG),read(ED))
 if a.source_dir:assert replay(e,a.source_dir)
 print("13EI_PASS RETRACT_13EH_FALSE_P74_CHUDU_AND_OFFSET_D30_NUMERIC_NULL")
