#!/usr/bin/env python3
"""13BJ Waseda source-original p23 D18-D20 visual original ROI and local arithmetic gate."""
import argparse,hashlib,json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13BJ-GORYEOSA-WASEDA-P23-D18-D20-DIRECT-CUMULATIVE-AND-LONG-R1.json"
PBE="docs/research/TIANWEN-13BE-GORYEOSA-D16-ORIGINAL-LONG-LANE-DUAL-COPY-COLLATION-R1.json"
PBG="docs/research/TIANWEN-13BG-GORYEOSA-NAJ-ADJACENT-FOLIOS-CUMULATIVE-D17-D19-R1.json"
PBH="docs/research/TIANWEN-13BH-GORYEOSA-NAJ-ORIGINAL-RECEIVED-CUMULATIVE-FIVEPOINT-OFFSET-R1.json"
PYZ="docs/research/TIANWEN-12YZ-GORYEOSA-D14-D20-INTRATABLE-THREE-COLUMN-RECEIVED-ARITHMETIC-R1.json"
MD="docs/research/TIANWEN-13BJ-GORYEOSA-WASEDA-P23-D18-D20-DIRECT-CUMULATIVE-AND-LONG-R1.md"
SOURCE_SHA="388f3d5dd9e9861f8ce90c304b154edaeaee98614bb12cd3468f957dcde6fc66"
ZIP_SHA="2b8fb5d5141d12b26949e1f4253806d31f3e548af9e04ac40e667093dc6c0f59"
EXPECTED=[
("D18_HEADING",18,"DAY_HEADING","十八日",None,[829,369,955,715],"b796a53437566e8cb2112644adb48449d4f009d093589fe05037b458280c3545"),
("D19_HEADING",19,"DAY_HEADING","十九日",None,[668,369,789,715],"1b369a17db7ca8438286ffc65e5eb88748fd8376b6329d950cea52fcd2942c5d"),
("D20_HEADING",20,"DAY_HEADING","二十日",None,[490,369,621,710],"a311225aac0de3e8da1118933962c7be04fa2be1be8b313c69999a175dbb088e"),
("D18_CUMULATIVE",18,"CUMULATIVE","八千〇〇〇二六九七","8000.2697",[917,690,996,1400],"b197a050b33eb1abce21ec6d64793409b54fcbab7a79025b5e20ea47ffbe79e3"),
("D19_CUMULATIVE",19,"CUMULATIVE","八千四百二十四六四〇八","8424.6408",[765,690,843,1400],"f14ba928fa4b9d3769bbcffad77fe98c2ddf82807acb3185a115a02114161bd2"),
("D20_CUMULATIVE",20,"CUMULATIVE","八千八百四十三七五七一","8843.7571",[601,690,686,1400],"c84bbc7355dbf1ea3d46aefa7302cfc7587549e5a39a0e126a5427485f39a93a"),
("D18_LONG",18,"LONG","四百一十九一一六三","419.1163",[840,686,907,1405],"7acbaf8a293c3293bbc1add2118cc2ac5e5c4f7561dfaadb840f3b1aad6d82f8")]
def load(path):
 return json.loads((ROOT/path).read_text(encoding="utf-8"))
def replay_actual_image(e,image_path):
 """Optional offline/archival replay, never merely trust metadata for physical source pixels."""
 from PIL import Image
 raw=Path(image_path).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==SOURCE_SHA==e["source"]["original_jpeg_sha256"]
 with Image.open(image_path) as src:
  im=src.convert("RGB")
  assert list(im.size)==e["source"]["image_dimensions"]==[2592,1728]
  for row in e["source_native_rgb_regions"]:
   bounds=row["original_rgb_roi_bbox"]
   crop=im.crop(bounds)
   assert hashlib.sha256(crop.tobytes()).hexdigest()==row["original_rgb_pixel_sha256"]
 return True
def check(e,be,bg,bh,yz,ledger,state):
 assert e["schema"]=="TIANWEN-13BJ-WASEDA-P23-D18-D20-SOURCE-ORIGINAL-CUMULATIVE-ROI-REPLAY-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 src=e["source"]
 assert src["holding"]=="WASEDA-RI06-02809-BOOK33"
 assert src["original_jpeg_sha256"]==SOURCE_SHA==be["source_original_image_reviews"][1]["original_image_sha256"]
 assert src["pdf_sha256"]=="28ebfeb34191f45715bc449d27da61fe04fb05eb45e84dd00cf569699f46225f"
 assert src["physical_page_in_pdf_1based"]==23 and src["embedded_jpeg_xref"]==70
 assert src["image_dimensions"]==[2592,1728]
 assert src["prior_original_source_capture_action"]==be["source_capture"]["action_run_id"]==39421117170
 assert src["prior_original_source_capture_artifact"]==be["source_capture"]["artifact_id"]==12263559032
 assert src["artifact_zip_sha256"]==ZIP_SHA==be["source_capture"]["artifact_digest_sha256"]
 assert src["archive_reopened_and_source_bytes_verified"] is True and src["manual_image_review"]=="SOURCE_NATIVE_RGB_NO_OCR"
 assert len(e["source_native_rgb_regions"])==len(EXPECTED)==7
 assert [(r["id"],r["layout_day"],r["field"],r["original_literal"],r["decimal_value"],r["original_rgb_roi_bbox"],r["original_rgb_pixel_sha256"]) for r in e["source_native_rgb_regions"]]==EXPECTED
 assert len({x["original_rgb_pixel_sha256"] for x in e["source_native_rgb_regions"]})==7
 vals={r["id"]:Decimal(r["decimal_value"]) for r in e["source_native_rgb_regions"] if r["decimal_value"] is not None}
 assert len(e["arithmetic_relations"])==2
 for idx,(a,b,long_day,long_value) in enumerate((
  ("D18_CUMULATIVE","D19_CUMULATIVE",17,Decimal(be["roman_decimal_bridge"]["day17_long"])),
  ("D19_CUMULATIVE","D20_CUMULATIVE",18,vals["D18_LONG"]))):
  edge=e["arithmetic_relations"][idx]
  assert (edge["from_layout_day"],edge["to_layout_day"],edge["matches_source_original_long_layout_day"])==(int(a[1:3]),int(b[1:3]),long_day)
  assert Decimal(edge["original_cumulative_delta"])==vals[b]-vals[a]==long_value==Decimal(edge["original_long_value"])
 assert [(x["layout_day"],x["waseda_original_cumulative"],x["naj_original_cumulative"],x["naj_source"]) for x in e["cross_holding_existing_NAJ_comparison"]]==[
 (18,str(vals["D18_CUMULATIVE"]),bg["source_canvases"][2]["new_day_slots"][0]["decimal"],PBG),
 (19,str(vals["D19_CUMULATIVE"]),bg["source_canvases"][2]["new_day_slots"][1]["decimal"],PBG)]
 assert e["cross_holding_existing_NAJ_comparison"][0]["naj_original_cumulative"]==str(vals["D18_CUMULATIVE"])
 assert e["cross_holding_existing_NAJ_comparison"][1]["naj_original_cumulative"]==str(vals["D19_CUMULATIVE"])
 rec=e["modern_received_text_crosslayer"]
 assert rec["source"]==PYZ and rec["received_day"]==19 and rec["original_Waseda_layout_day"]==20
 assert rec["modern_received_cumulative"]==next(x["cumulative"] for x in yz["modern_received_rows"] if x["day"]==19)==str(vals["D20_CUMULATIVE"])
 assert rec["proof_of_whole_section_index"] is False
 scope=e["scope_firewall"]
 assert scope["existing_original_JPEG_reused_from_archived_artifact"] is True
 assert scope["new_original_pixel_ROI_direct_reviews"]==len(EXPECTED)
 assert all(scope[k]==0 for k in ("new_original_source_JPEG_objects_acquired","additional_physical_copies","independent_stemmatic_votes_added","source_registry_entries_added","matrix_rows_added","genealogy_nodes_added","genealogy_edges_added","algorithm_reopens"))
 assert scope["research_omissions_still_open_or_blocked"]==11 and scope["deterministic_product"]=="CLOSED"
 for k,v in (("impression_year","UNRESOLVED"),("early_archetype_D16_one_vs_two","UNRESOLVED"),("Waseda_vs_NAJ_stemmatic_independence","UNPROVEN"),("G893_other_work_field_and_unit_equivalence","UNPROVEN"),("whole_table_day_index_law","UNADJUDICATED"),("full_source_day21_and_section_boundaries","NOT_YET_COLLATED")):assert scope[k]==v
 assert e["transmission_impact"]["edges_supported"]==[] and e["transmission_impact"]["edges_revised"]==[]
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert issue["source_refs"].count(MD)==issue["source_refs"].count(P)==1 and issue["source_refs"].index(P)==issue["source_refs"].index(MD)+1
 ev=next(x for x in issue["history"] if x.get("revision_id")=="TW-OPEN-0005-ORIGINAL-WASEDA-D18-D20-13BJ")
 assert ev["event"]=="ISSUE_REVISION" and set(ev["changed_fields"])=={"evidence_boundary","missing_evidence","next_action"}
 assert ev["previous_next_action"].startswith("13BI CURRENT EVIDENCE-BOUND NEXT ACTION")
 assert {PBE,PBG,PBH,MD,P}.issubset(set(ev["evidence_refs"]))
 assert "[13BJ 2026-10-21 WASEDA NATIVE FOLIO POSITIVE REVIEW]" in issue["evidence_boundary"]
 assert "[13BJ 2026-10-21 REMAINING ORIGINAL TARGETS]" in issue["missing_evidence"]
 # 13BI is superseded, even when a newer legitimate ISSUE_REVISION exists.
 # Preserve original glyph/ROI checks and future-scoped append-only transitions.
 assert not issue["next_action"].startswith("13BI CURRENT EVIDENCE-BOUND NEXT ACTION")
 assert issue["next_action"].startswith("13BJ CURRENT ACTION") or any(
    z.get("event")=="ISSUE_REVISION" and "next_action" in z.get("changed_fields",[])
    for z in issue["history"][issue["history"].index(ev)+1:])
 assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert any(z.startswith("13BJ ") for z in state["historical_audit"]["current_focus"])
 assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
 assert ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ")[0]
 assert ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"]
 assert len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==11
 return True
if __name__=="__main__":
 ap=argparse.ArgumentParser()
 ap.add_argument("--source-image",help="Optional 13BD archived Waseda embedded JPEG; verifies every original RGB ROI against real source bytes")
 args=ap.parse_args()
 e=load(P)
 assert check(e,load(PBE),load(PBG),load(PBH),load(PYZ),load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"),load("docs/PROJECT-CURRENT-STATE-R1.json"))
 if args.source_image:
  assert replay_actual_image(e,args.source_image)
 print("13BJ Waseda p23 original D18-D20 native SHA-bound ROI + local cumulative gate PASS")
