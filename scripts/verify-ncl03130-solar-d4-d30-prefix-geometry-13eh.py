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
 EXPECTED={
  73:[([317,386,461,815],"66cf9dd345e16fcd399ed3ecf9c2a69b15cde76945f3bbe7fbd5e1e225937efe"),([328,388,371,800],"4341abf030c3008845ef6d1abf766ab8b6b24a7096978c6ae21da6543f6b44e3")],
  74:[([888,390,990,815],"bcc2dc933fbb7a23f995eeaaa42fcb499e1b71fb59e107d076c7f8f94d62244c"),([929,396,951,785],"b86ee0c9fea7e8597ee2f05d2785fbfffe2aa3f68717e8643c6d8c1592fcc22c"),([963,396,985,785],"f62529ffd6ce87613606a4440c7a1cb1c98f5f8204dfdcdc9aec6d289dede197"),([806,390,895,815],"3a9d70381ce4ac77292d58ab6dfb10bff7c2a976ddf667394afb566183d920df")],
  76:[([547,390,649,830],"9c63499771fb952f4ec6508a71a0ae183cdab7601cb5a6815bff4c7cb89ecccd"),([590,418,615,830],"bc91212e7b7a6a98f67913788e0051c3eabfd5af46982aa26f90a3339cf0efd4"),([625,418,647,830],"a8bb8540a5f4cbc2252eb6b1d7879cb5073fa653412605ec20313fdffd2f7752"),([553,418,580,830],"666db57c4380e9ff3d78c2af64edd909f4b5b63286bac3bc7eff87c4abd4e10e")]
 }
 for p in pages:
  assert [(x["bbox"],x["rgb_sha256"]) for x in p["rois"]]==EXPECTED[p["pdf_page"]],p["pdf_page"]
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
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 current=l["binding"]["latest_research_focus_prefix"]
 assert current==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13EH SOURCE-ORIGINAL") for x in s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN" and issue["next_action"].startswith(current+" CURRENT ACTION")
 assert "D30" in issue["next_action"]
 assert {E,E.replace(".json",".md")}.issubset(set(issue["source_refs"]))
 h=next(x for x in issue["history"] if x.get("revision_id")=="TW-OPEN-0005-13EH-SAME-SOURCE-PREFIX-GEOMETRY-20261023")
 assert h["previous_next_action"].startswith("13EG CURRENT ACTION") and set(h["changed_fields"])=={"source_refs","next_action"}
 assert {E,E.replace(".json",".md"),EG,EF,ED}.issubset(set(h["evidence_refs"]))
 if current!="13EH":
  assert any(x.startswith("13EI FORWARD-ONLY ORIGINAL P74 GLYPH ERRATUM") for x in s["historical_audit"]["current_focus"])
  assert any(z.get("revision_id")=="TW-OPEN-0005-13EI-GLYPH-LANE-FORWARD-ERRATUM-20261023" for z in issue["history"])
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
 print("13EH_ARCHIVAL_RECORD_REPLAYED_CORRECTION_IN_13EI D30_NUMERIC_NULL")
