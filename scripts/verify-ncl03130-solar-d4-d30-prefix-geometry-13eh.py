#!/usr/bin/env python3
"""13EH source-original p74 D4 / p76 D30 bounded prefix geometry; fail closed."""
import argparse, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13EH-NCL03130-SOLAR-D4-D30-PREFIX-LANE-GEOMETRY-R1.json";S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
EG="docs/research/TIANWEN-13EG-NCL03130-SOLAR-FOLIO-DAY-BOUNDARIES-R1.json"
EF="docs/research/TIANWEN-13EF-NCL03130-SOLAR-P73-TECHNICAL-HEADINGS-R1.json"
ED="docs/research/TIANWEN-13ED-NCL03130-SOLAR-D30-EXTENDED-ORIGINAL-STRIP-R1.json"
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def center_x(b):return (b[0]+b[2])/2
def check(e,s,l,eg,ef,ed):
 assert e["schema"]=="TIANWEN-13EH-NCL03130-SOLAR-D4-D30-PREFIX-LANE-GEOMETRY-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["kind"]=="SAME_SOURCE_PIXEL_SHA_BOUND_CHUDU_PREFIX_AND_RELATIVE_ROI_CENTER_GEOMETRY_ONLY"
 source=e["source"]
 assert source["pdf_sha256"]==eg["source"]["pdf_sha256"]==ef["source"]["pdf_sha256"]==ed["source"]["pdf_sha256"]
 assert source["archive_workflow_run"]==eg["source"]["archive_workflow_run"] and source["artifact_id"]==eg["source"]["archive_artifact_id"]
 assert source["ocr_used"] is False and source["physical_copy"]==source["qing_vs_1905_stratum"]=="UNBOUND"
 assert source["independent_physical_copy_count"]==0 and source["same_digitized_source"] is True
 pages=e["pages"]; assert [p["pdf_page"] for p in pages]==[73,74,76]
 for p in pages:
  anchor=next(a for a in eg["pages"] if a["pdf_page"]==p["pdf_page"])
  assert p["png_sha256"]==anchor["png_sha256"] and p["rgb_sha256"]==anchor["rgb_sha256"] and p["png_size"]==anchor["png_size"]
  for roi in p["rois"]:
   b=roi["bbox"];assert 0<=b[0]<b[2]<=p["png_size"][0] and 0<=b[1]<b[3]<=p["png_size"][1]
   assert len(roi["rgb_sha256"])==64 and not roi["positive_scope"].startswith("NUMERIC_ADJUDICATION")
 assert len(pages[0]["rois"])==2 and len(pages[1]["rois"])==4 and len(pages[2]["rois"])==4
 d4,d30=pages[1:]
 assert d4["day_heading"]["source_literal"]=="四日" and d4["day_heading"]["bbox"]==eg["pages"][1]["boundaries"][0]["bbox"]
 assert d30["day_heading"]["source_literal"]=="三十日" and d30["day_heading"]["bbox"]==next(z for z in ed["native_rois"] if z["name"]=="d30_heading")["bbox"]
 r4=next(z for z in d4["rois"] if z["name"]=="day4_visible_chudu_prefix_strip")
 r30=next(z for z in d30["rois"] if z["name"]=="day30_visible_chudu_prefix_strip")
 prior=next(z for z in ed["native_rois"] if z["name"]=="d30_extended_full_strip")
 assert r30["bbox"]==prior["bbox"] and r30["rgb_sha256"]==prior["rgb_sha256"]
 assert r4["visible_prefix"]==r30["visible_prefix"]=="初度" and r30["visible_literal"]==ed["finding"]["d30_visible_glyph_group"]=="初度九十六二〇三"
 obs=e["relative_column_observation"]
 assert obs["method"]=="NOMINAL_BBOX_X_CENTER_DIFFERENCE_NOT_OPTICAL_GLYPH_CENTROID"
 for page,roi,k,expected in ((d4,r4,"day4",22),(d30,r30,"day30",21)):
  d=obs[k]
  assert d["heading_center_x"]==center_x(page["day_heading"]["bbox"])
  assert d["visible_chudu_strip_center_x"]==center_x(roi["bbox"])
  assert d["offset_px"]==d["visible_chudu_strip_center_x"]-d["heading_center_x"]==expected
 assert obs["offset_delta_px"]==abs(obs["day4"]["offset_px"]-obs["day30"]["offset_px"])==1
 assert obs["direct_common_visible_prefix"]=="初度" and obs["conclusion"]=="CONSISTENT_RELATIVE_SOURCE_LOCAL_VISIBLE_PREFIX_STRIP_POSITIONS"
 q=e["open_questions"]
 assert q["day30_original_numeric_decimal"] is None and q["day30_literal"]=="初度九十六二〇三"
 assert q["full_day4_numeric_transcription"] is False and q["missing_digits_or_scribal_error_proven"] is False
 assert q["technical_name_to_full_numeric_lane_binding"]=="UNRESOLVED"
 for k in ("xingdu_yingsuoji_richa_mechanical_equivalence","cross_copy_row_equivalence","global_day_offset"):
  assert q[k]=="UNPROVEN"
 assert q["qing_vs_1905_leaf_identity"]==q["physical_witness_independence"]=="UNBOUND"
 impact=e["impact"]
 assert impact["source_original_pages_replayed"]==3 and impact["new_bounded_original_rois"]==10
 assert all(impact[k]==0 for k in ("new_independent_physical_witnesses","new_registry_sources","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","new_numeric_adjudications","algorithm_reopens","risks_closed"))
 assert impact["open_or_blocked_issues"]==11 and impact["product"]=="CLOSED"
 assert s["schema_version"]=="1.783.0"==l["binding"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]=="13EH"==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert s["historical_audit"]["current_focus"][-1].startswith("13EH SOURCE-ORIGINAL")
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN" and issue["next_action"].startswith("13EH CURRENT ACTION")
 assert all(z in issue["next_action"] for z in ("D4","D30","行度","盈縮積","日差","NULL"))
 assert {E,E.replace(".json",".md")}.issubset(set(issue["source_refs"]))
 h=issue["history"][-1]
 assert h["revision_id"]=="TW-OPEN-0005-13EH-SAME-SOURCE-PREFIX-GEOMETRY-20261023"
 assert h["previous_next_action"].startswith("13EG CURRENT ACTION") and set(h["changed_fields"])=={"source_refs","next_action"}
 assert {E,E.replace(".json",".md"),EG,EF,ED}.issubset(set(h["evidence_refs"]))
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 assert len(l["issues"])==11
 return True
def replay(e,folder):
 from PIL import Image
 for p in e["pages"]:
  f=Path(folder)/f'original-p{p["pdf_page"]:03d}.png'
  assert hashlib.sha256(f.read_bytes()).hexdigest()==p["png_sha256"]
  with Image.open(f) as original:rgb=original.convert("RGB")
  assert list(rgb.size)==p["png_size"] and hashlib.sha256(rgb.tobytes()).hexdigest()==p["rgb_sha256"]
  for roi in p["rois"]:
   assert hashlib.sha256(rgb.crop(tuple(roi["bbox"])).tobytes()).hexdigest()==roi["rgb_sha256"],(p["pdf_page"],roi["name"])
 return True
if __name__=="__main__":
 parser=argparse.ArgumentParser();parser.add_argument("--source-dir");args=parser.parse_args()
 e=read(E);assert check(e,read(S),read(L),read(EG),read(EF),read(ED))
 if args.source_dir: assert replay(e,args.source_dir)
 print("13EH_PASS D4_D30_CHUDU_PREFIX_RELATIVE_PIXEL_GEOMETRY D30_NUMERIC_NULL")
