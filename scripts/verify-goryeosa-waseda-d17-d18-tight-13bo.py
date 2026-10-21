#!/usr/bin/env python3
"""13BO original Waseda D17/D18 day headings and tight numeral lanes."""
import argparse,hashlib,json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13BO-GORYEOSA-WASEDA-P23-D17-D18-ORIGINAL-HEADER-CUMULATIVE-LONG-R1.json"
PREV="docs/research/TIANWEN-13BN-GORYEOSA-WASEDA-P23-P24-TIGHT-CUMULATIVE-AND-LONG-ROI-R1.json"
MD="docs/research/TIANWEN-13BO-GORYEOSA-WASEDA-P23-D17-D18-ORIGINAL-HEADER-CUMULATIVE-LONG-R1.md"
HEADERS=[["P23_D17_HEADING",17,"十七日",[1036,350,1110,655],"9828903b85991285876f365a4693a1ca1a75ef340554f349b2ecc184eb633a0d"],["P23_D18_HEADING",18,"十八日",[842,350,924,655],"8adcf623d7ccb9fffa568d621be6bea268fef4dd7b1f8630fd91b11484d4a5cb"]]
LANES=[["P23_D17_C",17,"CUMULATIVE","八千〇〇〇二六九七","8000.2697",[974,685,1008,1400],"f001d937390ad80026a05f26c0511b0a7e5507fd808e5b247a1268bc7fade866"],["P23_D17_LONG",17,"LONG","四百二十四三七一一","424.3711",[1011,685,1048,1400],"b4c061d08bf03b4d1909b529628427103ea16220a801b24a6d277c6854e90739"],["P23_D18_C",18,"CUMULATIVE","八千四百二十四六四〇八","8424.6408",[805,685,842,1400],"73cdfb29fcc0c3c5e5265f5fe29d3688dd7d8ea660c0ea671e5b560f9165760d"],["P23_D18_LONG",18,"LONG","四百一十九一一六三","419.1163",[854,685,889,1400],"d4c555e6445f5c7de9c5e15ad697bbdbf7accc1469b979af22ace692124c2772"]]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def replay_real_image(e,path):
 from PIL import Image
 b=Path(path).read_bytes()
 assert hashlib.sha256(b).hexdigest()==e["source"]["jpeg_sha256"]
 with Image.open(path) as im:
  rgb=im.convert("RGB")
  assert list(rgb.size)==e["source"]["dimensions"]==[2592,1728]
  for row in e["original_header_rois"]+e["original_numeric_rois"]:
   assert hashlib.sha256(rgb.crop(row["bbox"]).tobytes()).hexdigest()==row["pixel_sha256"]
 return True
def check(e,prev,ledger,state):
 assert e["schema"]=="TIANWEN-13BO-WASEDA-D17-D18-SOURCE-ORIGINAL-TIGHT-LANE-AND-HEADER-COLLATION-R1"
 assert e["date"]=="2026-10-21" and e["issue_id"]=="TW-OPEN-0005"
 assert e["grade"]=="PROVIDER_JPEG_SHA_NATIVE_RGB_TIGHT_NUMERIC_AND_DAY_HEADER_ROI_NO_OCR"
 src=e["source"]
 assert src["holding"]=="WASEDA-RI06-02809-BOOK33"
 assert src["pdf_page_1based"]==23 and src["image_xref"]==70 and src["dimensions"]==[2592,1728]
 assert src["jpeg_sha256"]=="388f3d5dd9e9861f8ce90c304b154edaeaee98614bb12cd3468f957dcde6fc66"==prev["source"]["images"][0]["jpeg_sha256"]
 assert src["archived_artifact"]==12263559032 and src["another_physical_copy_added"] is False
 assert [(x["key"],x["day"],x["literal"],x["bbox"],x["pixel_sha256"]) for x in e["original_header_rois"]]==[tuple(x) for x in HEADERS]
 rows=e["original_numeric_rois"]
 assert [(x["key"],x["day"],x["field"],x["literal"],x["value"],x["bbox"],x["pixel_sha256"]) for x in rows]==[tuple(x) for x in LANES]
 for a,b in ((rows[0],rows[1]),(rows[2],rows[3])):
  assert a["bbox"][2]<b["bbox"][0]
  assert 30<=a["bbox"][2]-a["bbox"][0]<=42 and 30<=b["bbox"][2]-b["bbox"][0]<=42
 vals={x["key"]:Decimal(x["value"]) for x in rows}
 pvals={x["key"]:Decimal(x["value"]) for x in prev["original_single_numeric_lane_rois"]}
 assert len(e["same_copy_consecutive_arithmetic"])==2
 for i,(ca,cb,longkey) in enumerate((("P23_D17_C","P23_D18_C","P23_D17_LONG"),("P23_D18_C","P23_D19_C","P23_D18_LONG"))):
  edge=e["same_copy_consecutive_arithmetic"][i]
  beginning=vals[ca];ending=(vals if cb in vals else pvals)[cb];length=vals[longkey]
  assert Decimal(edge["c_start"])==beginning
  assert Decimal(edge["c_end"])==ending
  assert Decimal(edge["exact_delta"])==ending-beginning==length==Decimal(edge["native_long"])
 assert e["previous_tight_original_source"]==PREV
 all_c=[vals["P23_D17_C"],vals["P23_D18_C"],pvals["P23_D19_C"],pvals["P23_D20_C"],pvals["P24_D21_C"]]
 all_l=[vals["P23_D17_LONG"],vals["P23_D18_LONG"],pvals["P23_D19_LONG"],pvals["P23_D20_LONG"]]
 assert all(all_c[i+1]-all_c[i]==all_l[i] for i in range(4))
 chain=e["now_verified_source_local_chain"]
 assert chain["printed_days"]==[17,18,19,20,21]
 assert [Decimal(x) for x in chain["cumulative"]]==all_c
 assert [Decimal(x) for x in chain["preceding_native_long"]]==all_l
 assert chain["full_table_global_law_proven"] is False
 assert all(e["legacy_scope"].values())
 cross=e["cross_holding_scope"]
 assert cross["NAJ_source"]=="docs/research/TIANWEN-13BK-GORYEOSA-NAJ-CANVAS18-D19-LONG-D20-D21-CUMULATIVE-R1.json"
 assert all(cross[k] is False for k in ("Waseda_NAJ_same_impression_proven","whole_table_day_shift_proven","source_independent_lineage_vote_added"))
 assert e["transmission_impact"]["nodes_added"]==e["transmission_impact"]["edges_supported"]==e["transmission_impact"]["edges_revised"]==[]
 guard=e["source_firewall"]
 assert all(guard[k]==0 for k in ("new_JPEG_objects_downloaded","new_physical_witnesses","new_registry_sources","matrix_rows_added","genealogy_nodes_added","genealogy_edges_added","new_independent_voting_units","algorithm_reopens"))
 assert guard["open_or_blocked_research_issues"]==11 and guard["product"]=="CLOSED"
 issue=next(z for z in ledger["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert issue["source_refs"].count(MD)==issue["source_refs"].count(P)==1
 assert issue["source_refs"].index(P)==issue["source_refs"].index(MD)+1
 rev=next(z for z in issue["history"] if z.get("revision_id")=="TW-OPEN-0005-WASEDA-D17-D18-13BO")
 assert rev["event"]=="ISSUE_REVISION" and set(rev["changed_fields"])=={"evidence_boundary","missing_evidence","next_action"}
 assert rev["previous_next_action"].startswith("13BN CURRENT ACTION")
 assert {MD,P,PREV}.issubset(set(rev["evidence_refs"]))
 assert "[13BO 2026-10-21 WASEDA PRINTED D17/D18 TIGHT ORIGINAL LANES]" in issue["evidence_boundary"]
 later=any(z.get("event")=="ISSUE_REVISION" and "next_action" in z.get("changed_fields",[]) for z in issue["history"][issue["history"].index(rev)+1:])
 prefix=ledger["binding"]["latest_research_focus_prefix"]
 assert issue["next_action"].startswith("13BO CURRENT ACTION") or (later and prefix!="13BO" and issue["next_action"].startswith(prefix+" CURRENT ACTION"))
 assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert any(x.startswith("13BO ") for x in state["historical_audit"]["current_focus"])
 assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
 assert prefix==state["historical_audit"]["current_focus"][-1].split(" ")[0]
 assert ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"]
 assert set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])=={x["id"] for x in ledger["issues"]}
 assert (ROOT/MD).is_file()
 return True
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--source-p23")
 a=ap.parse_args();e=load(P)
 assert check(e,load(PREV),load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"),load("docs/PROJECT-CURRENT-STATE-R1.json"))
 if a.source_p23:assert replay_real_image(e,a.source_p23)
 print("13BO Waseda D17/D18 source-native headings long cumulative four-edge arithmetic PASS")
