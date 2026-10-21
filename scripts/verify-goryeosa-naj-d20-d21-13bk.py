#!/usr/bin/env python3
"""NAJ 13BK native source folio18 D19 long / D20,21 cumulative local arithmetic gate."""
import argparse,hashlib,json
from pathlib import Path
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13BK-GORYEOSA-NAJ-CANVAS18-D19-LONG-D20-D21-CUMULATIVE-R1.json"
PBG="docs/research/TIANWEN-13BG-GORYEOSA-NAJ-ADJACENT-FOLIOS-CUMULATIVE-D17-D19-R1.json"
PBJ="docs/research/TIANWEN-13BJ-GORYEOSA-WASEDA-P23-D18-D20-DIRECT-CUMULATIVE-AND-LONG-R1.json"
PYZ="docs/research/TIANWEN-12YZ-GORYEOSA-D14-D20-INTRATABLE-THREE-COLUMN-RECEIVED-ARITHMETIC-R1.json"
MD="docs/research/TIANWEN-13BK-GORYEOSA-NAJ-CANVAS18-D19-LONG-D20-D21-CUMULATIVE-R1.md"
IMAGE_SHA="88cecf62c8cd0dd623199eb06e3044efbe61771c1ffe058b8e7a87cc2f8f88cc"
EXPECTED=[
("D19_LONG",19,"LONG","四百一十三八四二九","413.8429",[2190,830,2260,1610],"24476b0b6f66287050f6e4ca3206f0fba0aa3f81b56afdddca516afd0cbe6155"),
("D20_CUM",20,"CUMULATIVE","八千八百四十三七五七一","8843.7571",[2125,826,2198,1740],"581d62cb12d5e2b878da5917796dd89ed1f87f634db7ccfaa085492f7236e40a"),
("D21_CUM",21,"CUMULATIVE","九千二百五十七六〇〇〇","9257.6000",[1952,826,2028,1740],"b8e48418e73508ceab24741ec9b5db47254aec49206d199453021e1b8e2d5e43"),
("D20_DAY",20,"DAY_HEADING","二十日",None,[2010,535,2135,795],"88fbbf326bd3bf944dbd5a2987e39134d0148972cb8b28309b4cdfa67a442f3b"),
("D21_DAY",21,"DAY_HEADING","二十一日",None,[1840,535,1965,795],"706514bf01352af25c44ae17a85d8f7d96a828046f830a47d023ad34d2c710e5")]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def replay_actual_image(e,image_path):
 from PIL import Image
 path=Path(image_path)
 assert hashlib.sha256(path.read_bytes()).hexdigest()==e["source"]["source_jpeg_sha256"]==IMAGE_SHA
 with Image.open(path) as original:
  image=original.convert("RGB")
  assert list(image.size)==e["source"]["image_dimensions"]==[3000,2215]
  for x in e["original_native_rois"]:
   assert hashlib.sha256(image.crop(x["bbox"]).tobytes()).hexdigest()==x["rgb_sha256"]
 return True
def check(e,bg,bj,yz,ledger,state):
 assert e["schema"]=="TIANWEN-13BK-NAJ-CANVAS18-D19-LONG-D20-D21-ORIGINAL-LOCAL-CUMULATIVE-R1"
 assert e["grade"]=="DIRECT_SHA_VERIFIED_ORIGINAL_JPEG_MANUAL_NATIVE_RGB_ROI_NO_OCR"
 assert e["issue_id"]=="TW-OPEN-0005"
 s=e["source"]
 assert s["physical_holding"]=="NAJ-282-0006-PHYSICAL51" and s["canvas_1based"]==18
 assert s["source_jpeg_sha256"]==IMAGE_SHA==bg["source_canvases"][2]["source_jpeg_sha256"]
 assert s["image_dimensions"]==[3000,2215]
 assert s["prior_13BA_capture_artifact"]==bg["previous_original_capture_artifact_id"]==12258234108
 assert s["prior_13BA_capture_run"]==bg["previous_original_capture_run"]
 assert s["prior_13BA_part2_zip_sha256"]==bg["previous_original_capture_part2_zip_sha256"]
 assert s["archive_native_image_reopened"] is True and s["original_native_RGB_bytes_sha_verified"] is True
 assert len(e["original_native_rois"])==len(EXPECTED)==5
 assert [(x["key"],x["layout_day"],x["field"],x["literal"],x["decimal"],x["bbox"],x["rgb_sha256"]) for x in e["original_native_rois"]]==EXPECTED
 assert len({x["rgb_sha256"] for x in e["original_native_rois"]})==5
 vals={x["key"]:Decimal(x["decimal"]) for x in e["original_native_rois"] if x["decimal"] is not None}
 edge=e["source_local_equations"]
 assert len(edge)==1
 edge=edge[0]
 assert (edge["source_from_layout_day"],edge["source_to_layout_day"],edge["equals_original_long_layout_day"])==(20,21,19)
 assert edge["source_same_canvas"] is True
 assert vals["D21_CUM"]-vals["D20_CUM"]==Decimal(edge["cumulative_difference"])==vals["D19_LONG"]==Decimal(edge["long_original"])
 assert Decimal(edge["cumulative_from"])==vals["D20_CUM"] and Decimal(edge["cumulative_to"])==vals["D21_CUM"]
 cross=e["cross_holding_existing"]
 assert cross["waseda_original_D20_source"]==PBJ
 assert cross["waseda_original_D20_cumulative"]==bj["source_native_rgb_regions"][5]["decimal_value"]==str(vals["D20_CUM"])==cross["naj_original_D20_cumulative"]
 assert cross["new_independent_vote"] is False
 received=e["crosslayer_existing_received"]
 assert received["source"]==PYZ and received["original_layout_day"]==21 and received["received_digital_day"]==20
 assert received["original_cumulative"]==received["received_digital_cumulative"]==next(x["cumulative"] for x in yz["modern_received_rows"] if x["day"]==20)==str(vals["D21_CUM"])
 assert received["scope"]=="LOCAL_MATCH_NOT_ORIGINAL_HEADING_INDEX_LAW"
 assert e["local_original_span_update"]["universal_day_header_law"]=="UNADJUDICATED"
 assert all(e["negative_controls"].values())
 counts=e["scope_counters"]
 assert counts["existing_original_JPEG_reused"] is True and counts["new_native_RGB_ROIs_reviewed"]==5
 assert all(counts[x]==0 for x in ("new_original_JPEG_objects","new_physical_copy_witnesses","independent_stemmatic_votes","registry_sources_added","matrix_rows_added","transmission_nodes_added","transmission_edges_added","algorithm_reopens"))
 assert counts["open_issues"]==11 and counts["product"]=="CLOSED"
 assert e["transmission_impact"]["edges_supported"]==[] and e["transmission_impact"]["edges_revised"]==[]
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0"
 assert issue["source_refs"].count(MD)==issue["source_refs"].count(P)==1
 assert issue["source_refs"].index(P)==issue["source_refs"].index(MD)+1
 h=next(x for x in issue["history"] if x.get("revision_id")=="TW-OPEN-0005-NAJ-CANVAS18-D20-D21-13BK")
 assert h["event"]=="ISSUE_REVISION" and set(h["changed_fields"])=={"evidence_boundary","missing_evidence","next_action"}
 assert h["previous_next_action"].startswith("13BJ CURRENT ACTION")
 assert set([PBG,PBJ,PYZ,MD,P]).issubset(set(h["evidence_refs"]))
 assert "[13BK 2026-10-21 DIRECT NAJ CANVAS18 ORIGINAL REVIEW]" in issue["evidence_boundary"]
 assert "[13BK 2026-10-21 CURRENT REMAINING GAPS]" in issue["missing_evidence"]
 assert issue["next_action"].startswith("13BK CURRENT ACTION") or any(z.get("event")=="ISSUE_REVISION" and "next_action" in z.get("changed_fields",[]) for z in issue["history"][issue["history"].index(h)+1:])
 assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert any(x.startswith("13BK ") for x in state["historical_audit"]["current_focus"])
 assert ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ")[0]
 assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
 assert ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==11
 return True
if __name__=="__main__":
 ap=argparse.ArgumentParser()
 ap.add_argument("--source-image",help="Optional local archived NAJ native JPEG (exact SHA verified)")
 args=ap.parse_args()
 e=load(P)
 assert check(e,load(PBG),load(PBJ),load(PYZ),load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"),load("docs/PROJECT-CURRENT-STATE-R1.json"))
 if args.source_image:assert replay_actual_image(e,args.source_image)
 print("NAJ 13BK original D19 LONG / D20-D21 CUM source native gate PASS")
