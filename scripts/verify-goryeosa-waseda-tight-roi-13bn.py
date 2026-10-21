#!/usr/bin/env python3
"""13BN native Waseda source original isolated column and arithmetic gate."""
import argparse,hashlib,json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13BN-GORYEOSA-WASEDA-P23-P24-TIGHT-CUMULATIVE-AND-LONG-ROI-R1.json"
BJ="docs/research/TIANWEN-13BJ-GORYEOSA-WASEDA-P23-D18-D20-DIRECT-CUMULATIVE-AND-LONG-R1.json"
BM="docs/research/TIANWEN-13BM-GORYEOSA-WASEDA-P23-P24-DAY-HEADER-CUMULATIVE-FORWARD-ERRATUM-R1.json"
MD="docs/research/TIANWEN-13BN-GORYEOSA-WASEDA-P23-P24-TIGHT-CUMULATIVE-AND-LONG-ROI-R1.md"
EXPECTED=[["P23_D19_C",23,19,"CUMULATIVE","八千八百四十三七五七一","8843.7571",[638,685,688,1400],"ec5693f9712dbf5b270ec6034040b34459a141944f8ee7f28b20e9f17cd9c76f"],["P23_D19_LONG",23,19,"LONG","四百一十三八四二九","413.8429",[693,685,732,1400],"3f68459fc9d79b6860f29e0dd3f6860c2a517adc833374d94001a4f831c8e875"],["P23_D20_C",23,20,"CUMULATIVE","九千二百五十七六〇〇〇","9257.6000",[460,685,505,1400],"e380b2f287dcd536b96b72482683e8fbfe8700100cff68ea6a7d8401f2366768"],["P23_D20_LONG",23,20,"LONG","四百〇八五五〇九","408.5509",[514,685,551,1400],"8c4d45ed95801f3ae18c65a3a852196bd2ed3344d8af9bbbcecb2172a0de720f"],["P24_D21_C",24,21,"CUMULATIVE","九千六百六十六一五〇九","9666.1509",[2032,685,2071,1400],"9bcc7d6e5c42fd145756da116a0559600c5cefbba71f571ff4458091a4b5f231"]]
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def actual_replay(e,p23,p24):
 from PIL import Image
 for f,src in zip((p23,p24),e["source"]["images"]):
  raw=Path(f).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==src["jpeg_sha256"]
  with Image.open(f) as im:
   rgb=im.convert("RGB")
   assert list(rgb.size)==src["dimensions"]==[2592,1728]
   for row in e["original_single_numeric_lane_rois"]:
    if row["pdf_page_1based"]==src["pdf_page_1based"]:
     assert hashlib.sha256(rgb.crop(row["bbox"]).tobytes()).hexdigest()==row["rgb_sha256"]
 return True
def check(e,bj,bm,ledger,state):
 assert e["schema"]=="TIANWEN-13BN-WASEDA-SINGLE-NUMERIC-LANE-NATIVE-RGB-ROI-COLLATION-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 assert e["grade"]=="SHA256_VERIFIED_SOURCE_JPEG_WITH_NATIVE_RGB_SINGLE_LANE_MANUAL_NO_OCR"
 s=e["source"]
 assert s["holding"]=="WASEDA-RI06-02809-BOOK33"
 assert s["pdf_sha256"]==bj["source"]["pdf_sha256"]==bm["source"]["source_pdf_sha256"]
 assert [(x["pdf_page_1based"],x["embedded_xref"],x["jpeg_sha256"],x["dimensions"]) for x in s["images"]]==[(23,70,"388f3d5dd9e9861f8ce90c304b154edaeaee98614bb12cd3468f957dcde6fc66",[2592,1728]),(24,73,"913368872d9a7589abf88a4ae9b8d87ca4b836cc27c0d66d21b8ba82022e1574",[2592,1728])]
 assert s["origin"]=="REUSE_PREVIOUS_FIRSTPARTY_ARCHIVED_JPEG_BYTES_NO_NEW_IMAGE_ACQUISITION"
 actual=e["original_single_numeric_lane_rois"]
 assert [(x["key"],x["pdf_page_1based"],x["printed_day"],x["field"],x["original_literal"],x["value"],x["bbox"],x["rgb_sha256"]) for x in actual]==[tuple(row) for row in EXPECTED]
 assert all(25<=r["bbox"][2]-r["bbox"][0]<=50 for r in actual)
 # Exclude other numeral columns: not merely the image hash, but isolated x range.
 for a,b in ((actual[0],actual[1]),(actual[2],actual[3])):
  assert a["pdf_page_1based"]==b["pdf_page_1based"]==23
  assert a["bbox"][2]<b["bbox"][0]
 vals={r["key"]:Decimal(r["value"]) for r in actual}
 assert len(e["exact_local_arithmetic"])==2
 for i,(left,right,lane,longday) in enumerate((
  ("P23_D19_C","P23_D20_C","P23_D19_LONG",19),
  ("P23_D20_C","P24_D21_C","P23_D20_LONG",20))):
  edge=e["exact_local_arithmetic"][i]
  assert Decimal(edge["first_cumulative"])==vals[left]
  assert Decimal(edge["second_cumulative"])==vals[right]
  assert Decimal(edge["difference"])==vals[right]-vals[left]==vals[lane]
  assert Decimal(edge["original_long_value"])==vals[lane]
  assert edge["same_original_printed_day_long"]==longday
  assert edge["same_copy_native_two_column_check"] is True
 assert e["original_day_heading_binding_from"]==BM
 old=e["previous_record_restrictions"]
 assert [x["old_bbox"] for x in old]==[[601,690,686,1400],[601,690,686,1400],[455,690,527,1430],[2015,685,2080,1430]]
 assert old[0]["prior"]==BJ and all(x["prior"]==BM for x in old[1:])
 assert old[0]["old_bbox"]==next(x["original_rgb_roi_bbox"] for x in bj["source_native_rgb_regions"] if x["id"]=="D20_CUMULATIVE")
 for key,oldbox in (("P23_D19_CUM",old[1]["old_bbox"]),("P23_D20_CUM",old[2]["old_bbox"]),("P24_D21_CUM",old[3]["old_bbox"])):
  assert oldbox==next(z["bbox"] for z in bm["source_native_rgb_rois"] if z["key"]==key)
 assert e["audited_but_unrebound_legacy_records"][0]["old_ids"]==["D18_CUMULATIVE","D19_CUMULATIVE","D18_LONG"]
 assert e["cross_holding_scope"]["naj_book51_source"]=="docs/research/TIANWEN-13BK-GORYEOSA-NAJ-CANVAS18-D19-LONG-D20-D21-CUMULATIVE-R1.json"
 assert all(e["cross_holding_scope"][k] is False for k in ("whole_table_shift_proven","stemmatic_independence_proven","earliest_archetype_day16_proven"))
 assert e["cross_holding_scope"]["table_first_last_heading_scope_pending"] is True
 assert e["transmission_impact"]["nodes_added"]==e["transmission_impact"]["edges_supported"]==e["transmission_impact"]["edges_revised"]==[]
 fw=e["scope_firewall"]
 assert all(fw[k]==0 for k in ("new_physical_historical_copies","new_source_jpegs_acquired","new_independent_source_votes","new_registry_sources","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","algorithm_reopens"))
 assert fw["open_or_blocked_research_issues"]==11 and fw["deterministic_product"]=="CLOSED"
 issue=next(z for z in ledger["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0"
 assert issue["source_refs"].count(P)==issue["source_refs"].count(MD)==1 and issue["source_refs"].index(P)==issue["source_refs"].index(MD)+1
 h=next(z for z in issue["history"] if z.get("revision_id")=="TW-OPEN-0005-WASEDA-TIGHT-ROI-LONG-13BN")
 assert h["event"]=="ISSUE_REVISION" and set(h["changed_fields"])=={"evidence_boundary","missing_evidence","next_action"}
 assert h["previous_next_action"].startswith("13BM CURRENT ACTION")
 assert {P,MD,BJ,BM}.issubset(set(h["evidence_refs"]))
 assert "[13BN 2026-10-21 WASEDA SINGLE NUMERIC LANE AND LONG COLUMN POSITIVE]" in issue["evidence_boundary"]
 later=any(z.get("event")=="ISSUE_REVISION" and "next_action" in z.get("changed_fields",[]) for z in issue["history"][issue["history"].index(h)+1:])
 prefix=ledger["binding"]["latest_research_focus_prefix"]
 assert issue["next_action"].startswith("13BN CURRENT ACTION") or (later and prefix!="13BN" and issue["next_action"].startswith(prefix+" CURRENT ACTION"))
 assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert any(z.startswith("13BN ") for z in state["historical_audit"]["current_focus"])
 assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
 assert prefix==state["historical_audit"]["current_focus"][-1].split(" ")[0]
 assert ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"]
 assert set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])=={z["id"] for z in ledger["issues"]}
 assert (ROOT/MD).is_file()
 return True
if __name__=="__main__":
 ap=argparse.ArgumentParser()
 ap.add_argument("--waseda-p23")
 ap.add_argument("--waseda-p24")
 args=ap.parse_args()
 e=load(P)
 assert check(e,load(BJ),load(BM),load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"),load("docs/PROJECT-CURRENT-STATE-R1.json"))
 if args.waseda_p23 or args.waseda_p24:
  assert args.waseda_p23 and args.waseda_p24
  assert actual_replay(e,args.waseda_p23,args.waseda_p24)
 print("13BN single native Waseda cumulative+long source lane and arithmetic gate PASS")
