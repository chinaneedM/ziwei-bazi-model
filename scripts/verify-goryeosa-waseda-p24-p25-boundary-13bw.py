#!/usr/bin/env python3
"""13BW direct official original p24/p25 native-RGB day headings and forward-only ledger."""
import argparse,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13BW-GORYEOSA-WASEDA-P24-P25-ORIGINAL-D21-D38-AND-P26-P27-BOUNDARY-R1.json"
MD="docs/research/TIANWEN-13BW-GORYEOSA-WASEDA-P24-P25-ORIGINAL-D21-D38-AND-P26-P27-BOUNDARY-R1.md"
BV="docs/research/TIANWEN-13BV-GORYEOSA-WASEDA-P21-P23-ORIGINAL-SOLAR-TABLE-TITLE-AND-FIRST-DAY-INDEX-R1.json"
BN="docs/research/TIANWEN-13BN-GORYEOSA-WASEDA-P23-P24-TIGHT-CUMULATIVE-AND-LONG-ROI-R1.json"
BM="docs/research/TIANWEN-13BM-GORYEOSA-WASEDA-P23-P24-DAY-HEADER-CUMULATIVE-FORWARD-ERRATUM-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
HEADINGS=[["P24_D21_PRINTED_DAY",24,21,"二十一日",[2060,355,2200,660],"4e3e33bd0904986f10c20b6b2494cf12a1fd61454f5d6cefb79f8c240c1062b"],["P24_D29_PRINTED_DAY",24,29,"二十九日",[460,350,610,660],"341e616135d50ead66f257de1990e96efaf3b7dd3e16ca48505ec18bb7a11e8e"],["P25_D30_PRINTED_DAY",25,30,"三十日",[2040,345,2200,660],"ee24705cd642f32af8045b453e722f07cc687f48f3db847be59d14679f8c815d"],["P25_D38_PRINTED_DAY",25,38,"三十八日",[460,345,610,660],"b4aa290191661afeb20c22413c4e5dc1a36cbd09e6f7d1cd7121fbb973eb5f55"]]
def load(p):return json.loads((R/p).read_text(encoding="utf-8"))
def replay_original(e,original24,original25):
 from PIL import Image
 for source,path in zip(e["source"]["source_images"],[original24,original25]):
  raw=Path(path).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==source["jpeg_sha256"]
  with Image.open(path) as im:
   rgb=im.convert("RGB")
   assert list(rgb.size)==source["dimensions"]
   for z in e["original_native_day_header_rois"]:
    if z["pdf_page_1based"]==source["page"]:
     assert hashlib.sha256(rgb.crop(tuple(z["bbox"])).tobytes()).hexdigest()==z["original_native_rgb_sha256"]
 return True
def check(e,s,l,p):
 assert e["schema"]=="TIANWEN-13BW-WASEDA-FIRSTPARTY-P24-P25-D21-D38-CONTINUITY-AND-P26-P27-ACQUISITION-R1"
 assert e["date"]=="2026-10-21" and e["issue_id"]=="TW-OPEN-0005"
 assert e["grade"]=="ORIGINAL_FIRSTPARTY_SHA256_SOURCE_JPEG_NATIVE_RGB_MANUAL_DAY_HEADERS_NO_OCR"
 src=e["source"]
 assert src["holding"]=="WASEDA-RI06-02809-BOOK33"
 assert src["pdf_sha256"]==p["BV"]["source"]["pdf_sha256"]=="28ebfeb34191f45715bc449d27da61fe04fb05eb45e84dd00cf569699f46225f"
 assert src["previous_original_capture_run"]==39547966390 and src["previous_original_capture_artifact_id"]==12322497620
 assert src["previous_zip_digest_sha256"]=="dbeaddd34f72d7f5501e13ebb8dc72c7b4f1bdaa842254bc98cc51c28f793f7a"
 assert [(x["page"],x["xref"],x["jpeg_sha256"],x["dimensions"]) for x in src["source_images"]]==[
  (24,73,"913368872d9a7589abf88a4ae9b8d87ca4b836cc27c0d66d21b8ba82022e1574",[2592,1728]),
  (25,76,"ac19365a36456f0a550dd85873c0a006cee37765a352aa2b23d37137b5478646",[2592,1728])]
 assert src["source_images"][0]["jpeg_sha256"]==p["BN"]["source"]["images"][1]["jpeg_sha256"]
 assert [(z["key"],z["pdf_page_1based"],z["printed_day"],z["literal"],z["bbox"],z["original_native_rgb_sha256"]) for z in e["original_native_day_header_rois"]]==[tuple(z) for z in HEADINGS]
 assert [z["printed_day"] for z in e["original_native_day_header_rois"]]==[21,29,30,38]
 assert [z["pdf_page_1based"] for z in e["original_native_day_header_rois"]]==[24,24,25,25]
 for z in e["original_native_day_header_rois"]:
  x1,y1,x2,y2=z["bbox"]
  assert 0<=x1<x2<=2592 and 0<=y1<y2<=1728
 sequence=e["source_local_page_continuity"]
 assert [x["pdf_page_1based"] for x in sequence]==[21,22,23,24,25]
 assert [(x["first_heading"],x["last_heading"]) for x in sequence]==[
  ("初日","二日"),("三日","十一日"),("十二日","二十日"),("二十一日","二十九日"),("三十日","三十八日")]
 assert [x["source"] for x in sequence]==["13BV"]*3+["13BW"]*2
 assert p["BV"]["finding"]["original_initial_day_heading"]=="初日"
 assert p["BV"]["finding"]["original_table_end"]=="UNCOLLATED_AFTER_DAY20"
 assert p["BM"]["source_native_rgb_rois"][-2]["printed_day"]==21
 acq=e["acquisition_next"]
 assert acq["source_pages_requested"]==[26,27] and acq["source_expected_pdf_sha256"]==src["pdf_sha256"]
 assert acq["status"]=="QUEUED_BY_REPO_WORKFLOW_NOT_YET_ORIGINAL_VISUAL_REVIEW"
 assert acq["source_images_sha256"]=="PENDING_SOURCE_ARTIFACT" and acq["ocr"] is False
 assert acq["script"]=="scripts/acquire-goryeosa-waseda-next-folios-13bw.py" and acq["workflow"]==".github/workflows/acquire-goryeosa-waseda-next-folios-13bw.yml"
 f=e["findings"]
 assert f["printed_day_index_contiguous_in_reviewed_page_endpoints"] is True
 assert f["all_intermediate_day_titles_individually_rgb_bound"] is False
 assert f["printed_table_end"]=="UNBOUND_AFTER_D38"
 assert f["Waseda_D16_isolated_cumulative"]=="UNBOUND"
 assert f["printed_積日_equals_cumulative_numeric_column"]=="NOT_ESTABLISHED"
 assert all(f[k]=="UNPROVEN" for k in ("full_original_table_index_formula","NAJ_WASEDA_printed_day_global_shift","G893_SHAO_WEI_MING1569_same_field_units"))
 assert e["prior_evidence"]=={"source_table_opening_and_day0_20":BV,"p24_original_D21_numeric":BN,"p24_original_D21_day_heading":BM}
 fw=e["scope_firewall"]
 assert all(fw[k]==0 for k in ("new_physical_witnesses","new_original_jpeg_objects_acquired_in_this_analysis","new_independent_stemmatic_votes","source_registry_entries_added","matrix_rows_added","genealogy_nodes_added","genealogy_edges_added","algorithm_reopens"))
 assert fw["research_issues_open_or_blocked"]==len(l["issues"])==11 and fw["deterministic_chart"]=="CLOSED"
 assert e["transmission_impact"]["nodes_added"]==e["transmission_impact"]["edges_supported"]==e["transmission_impact"]["edges_revised"]==[]
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0"
 assert issue["source_refs"].count(MD)==issue["source_refs"].count(P)==1
 assert issue["source_refs"].index(P)==issue["source_refs"].index(MD)+1
 rev=next(x for x in issue["history"] if x.get("revision_id")=="TW-OPEN-0005-WASEDA-P24-P25-AND-END-ACQ-13BW")
 assert rev["previous_next_action"].startswith("13BV CURRENT ACTION")
 assert {MD,P,BV,BN,BM}.issubset(set(rev["evidence_refs"]))
 later=any("next_action" in v.get("changed_fields",[]) for v in issue["history"][issue["history"].index(rev)+1:])
 prefix=l["binding"]["latest_research_focus_prefix"]
 assert issue["next_action"].startswith("13BW CURRENT ACTION") or (later and prefix!="13BW" and (issue["next_action"].startswith(prefix+" CURRENT ACTION") or issue["next_action"].startswith(next((z["revision_id"].split("-")[3]+" CURRENT ACTION" for z in reversed(issue["history"]) if "next_action" in z.get("changed_fields",[]) and len(z.get("revision_id","").split("-"))>3 and z["revision_id"].split("-")[3].startswith("13")),"__NO_RECORDED_ACTION__"))))
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert any(z.startswith("13BW ") for z in s["historical_audit"]["current_focus"])
 assert prefix==s["historical_audit"]["current_focus"][-1].split(" ")[0]
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 assert set(l["checkpoint_log"][-1]["reviewed_issue_ids"])=={x["id"] for x in l["issues"]}
 assert (R/MD).is_file()
 return True
if __name__=="__main__":
 a=argparse.ArgumentParser()
 a.add_argument("--source-p24");a.add_argument("--source-p25")
 args=a.parse_args()
 e=load(P);assert check(e,load(S),load(L),{"BV":load(BV),"BN":load(BN),"BM":load(BM)})
 if args.source_p24 or args.source_p25:
  assert args.source_p24 and args.source_p25
  assert replay_original(e,args.source_p24,args.source_p25)
 print("13BW Waseda original p24/p25 D21-D38 source day-header and next folio boundary gate PASS")
