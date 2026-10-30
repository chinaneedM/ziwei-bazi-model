#!/usr/bin/env python3
"""13LO p7/p8 three-source crosswalk; prevent false plate and historical vote upgrades."""
import json,re
from pathlib import Path
# Backward-looking assertions use append-only history, never overwrite live next_action.
try:
    from scripts._tianwen_historical_action_r1 import historical_action_view
except ModuleNotFoundError:
    from _tianwen_historical_action_r1 import historical_action_view
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13LO-NAJDA-HARVARD-J35-P7-P8-THREE-WAY-SOURCE-CROSSWALK-R1.json"
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in [E,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"])
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13LO-NAJDA-HARVARD-J35-P7-P8-THREE-WAY-SOURCE-CROSSWALK-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["no_ocr"] is True
 h=e["harvard"];page=h["same_text_page"]
 assert h["original_pdf_sha256"]=="36a2a99461d9d16a71e203d95ffa6cac189f1bbab94295de51ed6d3b60bd649b"
 assert h["original_pdf_bytes"]==70809419 and h["original_pdf_pages"]==74
 assert h["existing_artifact"]["artifact_zip_sha256"]=="687af64da3978927cdb096a7a43c0e79381dfb00bc6443f8b49b5b69d7eacec5"
 assert h["existing_artifact"]["artifact_zip_bytes"]==74203635
 assert h["durable_archive"]["zip_sha256"]==h["existing_artifact"]["artifact_zip_sha256"]
 assert h["durable_archive"]["library_file_id"]=="libfile_d77a1a76c0148191a85e5e0c9c4f351e"
 assert page["pdf_page_1_based"]==8 and page["pdf_zero_index"]==7 and page["pdf_image_pixels"]==[1800,1551]
 assert page["page_rgb_sha256"]=="fd419982a337823736296b0fe0fd1c86d20a6c2b8e48987c312b0346e0096a03"
 assert h["original_physical_copy_catalog_binding_complete"] is False and h["exact_1739_impression_proven"] is False
 n=e["naaj"];assert n["source_page_1_based"]==7 and n["physical_holdings"]==["281-0037","281-0038"]
 assert n["verified_six_native_color_roi_archive_sha256"]=="369e9b6c9bbb54f40210d589c515a20c0a0d2b41dc36ea25a11fff82d71bfd5b" and n["native_roi_count"]==6
 assert [x["target_id"] for x in e["same_passage_three_locus_controls"]]==["LEFT_NONCIRCLE_COLUMNS","GUTTER_NONCIRCLE_COLUMNS","RIGHT_NONCIRCLE_COLUMNS"]
 for x in e["same_passage_three_locus_controls"]:
  X,Y,X2,Y2=x["harvard_page_8_rgb_roi_xyxy"]
  assert 0<=X<X2<=1800 and 0<=Y<Y2<=1551
  assert x["harvard_roi_pixels"]==[X2-X,Y2-Y]
  assert re.fullmatch(r"[0-9a-f]{64}",x["harvard_roi_rgb_sha256"])
  assert x["matching_printed_writing"]=="CONTENT_LEVEL_CORRESPONDENCE" and x["unique_accidental_woodblock_damage_confirmed"] is False
 geo=e["exploratory_geometric_page_identification"]
 assert geo["same_plate_proven"] is False and geo["same_plate_refuted"] is False
 assert geo["font_or_frame_unique_damage_identified"] is False
 assert geo["naaj_2810037_vs_2810038_p7"]=={"pairs":564,"inliers":339}
 assert geo["naaj_2810037_vs_harvard_pdf_pages"]["8"]=={"pairs":163,"inliers":27}
 assert geo["naaj_2810038_vs_harvard_pdf_pages"]["8"]=={"pairs":212,"inliers":45}
 a=e["adjudication"]
 assert a["harvard_pdf_page8_corresponds_to_naaj_p7"] is True
 assert a["three_scanned_source_streams_not_three_historical_numeric_votes"] is True
 for k in ["shared_or_distinct_woodblock_proven","unique_accidental_engraving_break_proven","exact_1739_physical_impression_date_proven"]:
  assert a[k] is False,k
 for k in ["new_independently_authenticated_print_recensions","new_original_historical_source_registry_records","new_historical_g893_numeric_winners","algorithm_reopens"]:
  assert a[k]==0,k
 assert a["original_harvard_and_naaj_literal"]=="238977.09" and a["separate_cadal_siku_literal"]=="288977.09" and a["product"]=="CLOSED"
 assert e["transmission_impact"]["edges_supported"]==[] and e["transmission_impact"]["edges_revised"]==[]
 assert e["counts"]==dict(historical_sources=765,matrix_rows=222,matrix_audited=222,graph_nodes=252,graph_edges=238,open_issues=11,algorithm_reopens=0,product="CLOSED")
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,959,0)
 assert any(x.startswith("13LO ") for x in s["historical_audit"]["current_focus"])
 assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and "13LO CURRENT ACTION:" in historical_action_view(issue)
 assert "13LN CURRENT ACTION:" in historical_action_view(issue) and E in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13LO-HARVARD-NAJ-CROSSWALK-20261030" for x in issue["history"])
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 return {"status":"PASS","historical_numeric_winners":0,"same_plate_adjudication":"UNRESOLVED","harvard_page":8,"naaj_page":7}
if __name__=="__main__":print(json.dumps(check(*load()),ensure_ascii=False))
