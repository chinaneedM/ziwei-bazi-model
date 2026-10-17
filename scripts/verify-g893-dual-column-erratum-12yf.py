#!/usr/bin/env python3
"""12YF forward-only correction: separate two original source lanes, exact Decimal recurrence."""
from pathlib import Path
from decimal import Decimal
import json,argparse,hashlib,zipfile,io
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YF-G893-TWO-COLUMN-ERRATUM-AND-SOLAR-RECURRENCE-R1.json"
S=["5.2176","5.2362","5.2548","5.2734","5.2920"]
L=["424.8249","429.6073","434.3711","439.1163","443.8429"]
SHORT_GLYPH=["五分二一七六","五分二三六二","五分二五四八","五分二七三四","五分二九二〇"]
LONG_GLYPH=["四百二十四分八二四九","四百二十九分六〇七三","四百三十四分三七一一","四百三十九分一一六三","四百四十三分八四二九"]
HASHES=["7d065c072c313911c7ff62d7783714cd764413f064a5af28b9c4438517362b10","4fc2ffcf03239d0a2d0fa1ff6f21b8f92a9821cab1e11a14f011c763fd3720b6","139c9d66cf0cc142832448de85aabb4bfd319fbbc82abff20653daf7a0f32ea0","f34ff5ee28c2e5dd4cad5ab0596adece8f7efb054cea3df342850339821cd250","9ad82eef0c2e1fe7e1055a99978f50dedfb41483531ba130ecc8b231588cde5c","7ac1a2a264268868825042babba71812bb364f0a50e9b1b0dd2ab59b849d9629","2c1fc3bc3b7eb898ce35b9623c8d2bfb6589ce4c6cd5151f78e64641b9ba24e6","00c92cb82b0089b7a4e06c796cf11eb6e1bc3f0bbd987af0c830396a21fdfe84","2f584a9a438f1bde5d867e616db978767ca2b32ef1647eaf946d1f19295c3184","20552d924a42385f8f7bd92615a245ee94e5ad39a477c14b642cd1fb83737f34"]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json"))
def verify(d,ledger,state):
 need(d["schema"]=="TIANWEN-12YF-G893-TWO-COLUMN-READING-ERRATUM-R1" and d["correction_type"]=="FORWARD_ONLY_SOURCE_COLUMN_BOUNDARY_ERRATUM","schema")
 original=json.loads((ROOT/d["prior_evidence"]).read_text(encoding="utf-8"))
 need(d["prior_evidence_immutable"] is True and d["prior_evidence_status"]=="RETRACTED_AS_CROSS_COLUMN_CONCATENATION_NOT_EIGHT_PLACE_SOURCE_FIELD","erratum semantics")
 need([x["lexical_decimal"] for x in original["readings"]]==d["prior_false_claims"]["joined_decimal_numbers"]==["5.21768249","5.23626073","5.25483711"],"old 12YE record must remain auditable")
 need(d["prior_false_claims"]["false_derived_second_difference"]=="-0.00000186" and d["prior_false_claims"]["historical_numeric_evidence_validity"]=="REJECTED" and d["prior_false_claims"]["old_12ye_roi_semantics"]=="CROSSED_TWO_COLUMNS_CANNOT_SUPPORT_FULL_EIGHT_PLACE_FIELD","false precision still quoted as historical evidence")
 source=d["original_copy"]; need(source["zip_sha256"]==original["archive"]["sha256"]=="ee9ecf1de3bb6abe5678e0f8ec8383ef985051e77d091ee40840756e57081107" and source["zip_size"]==33525981 and source["original_source_jpegs_verified"]==204 and source["zip_crc"]=="PASS","same source")
 need(source["source_page_sha256"]=="f9812e8c6a357eb6cd1117bb2af58d816e01030d5b93f34e7094bddb766b2b55" and source["new_independent_physical_witnesses"]==source["original_images_committed"]==0,"source boundary")
 rois=d["native_rgb_rois"]["per_column"];need(len(rois)==10 and [x["sha256"] for x in rois]==HASHES,"source image digests")
 for i in range(5):
  a,b=rois[2*i:2*i+2];need((a["day"],a["lane"],b["day"],b["lane"])==(15+i,"LONG",15+i,"SHORT"),"lane identity")
  need(a["rect_px"][2]<b["rect_px"][0] and a["page"]==b["page"]=="002b","cross-column ROI reuse")
  for q in (a,b):
   l,t,r,bottom=q["rect_px"];need(0<=l<r<=1150 and 0<=t<bottom<=2000,"ROI bounds")
 rows=d["direct_original_readings"];need(len(rows)==5,"five original days")
 for i,row in enumerate(rows):
  need((row["day"],row["short_printed_glyphs"],row["short_decimal"],row["long_printed_glyphs"],row["long_decimal"])==(i+15,SHORT_GLYPH[i],S[i],LONG_GLYPH[i],L[i]) and row["same_copy_paired_columns_separate"] is True,"original source lane readings")
  need(row["short_printed_glyphs"]+row["long_printed_glyphs"].split("分")[-1] == d["prior_false_claims"]["joined_eight_digit_strings"][i] if i<3 else True,"incorrect join not captured")
 v=d["source_scoped_replay"]; x=list(map(Decimal,S));y=list(map(Decimal,L))
 step=[y[i+1]-y[i] for i in range(4)]
 complements=[Decimal(10)-x[i] for i in range(4)]
 need(step==complements and [str(q) for q in step]==v["long_next_minus_long_current"]==v["ten_minus_short_current"]==["4.7824","4.7638","4.7452","4.7266"],"two-lane arithmetic")
 need([str(x[i+1]-x[i]) for i in range(4)]==v["short_neighbor_increments"]==["0.0186"]*4,"source short lane increments")
 need([str(y[i+2]-2*y[i+1]+y[i]) for i in range(3)]==v["long_neighbor_second_differences"]==["-0.0186"]*3,"long second differences")
 need(v["precision"]=="EXACT_DECIMAL_4" and v["unit_and_epoch_bridge"]=="NOT_ESTABLISHED","mechanical unit promotion")
 guard=d["scope_guard"]
 need(all(guard[k]=="UNPROVEN" for k in ("header_to_column_unit_identity","independent_ming1569_equivalence","printing_or_copy_causation","comprehensive_all_days_table_law")),"unsupported historical award")
 need(guard["source_original_six_primary_target_fields"]=="5/6" and guard["cross_witness_mechanical_final_decisions"]=="0/6" and guard["open_omission_issues"]==11 and all(guard[k]==0 for k in ("new_genealogy_edges","new_source_records","algorithm_reopens")),"historical scope drift")
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 need(issue["status"]=="OPEN" and DOC in issue["source_refs"] and "docs/research/TIANWEN-12YF-G893-TWO-COLUMN-ERRATUM-AND-SOLAR-RECURRENCE-R1.md" in issue["source_refs"],"issue/source missing")
 corrections=issue["g893_12ye_dual_column_errata"]
 need(len(corrections)==1 and corrections[0]["evidence_doc"]==DOC and corrections[0]["retracted_false_second_difference"]=="-0.00000186" and corrections[0]["replacement_long_second_difference"]=="-0.0186" and corrections[0]["cross_witness_final_decisions_added"]==0,"issue 12YE not formally corrected")
 need(issue["history"][-1]["event"]=="G893_12YE_TWO_COLUMN_ERRATUM_AND_DUAL_LANE_REPLAY_APPEND" and DOC in issue["history"][-1]["evidence_refs"],"forward-only correction event")
 need(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]=="1.619.0" and state["historical_audit"]["current_focus"][-1].startswith("12YF "),"state handoff")
 need(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0 and sum(z["status"]!="RESOLVED_WITH_EVIDENCE" for z in ledger["issues"])==11,"chart/omission")
 return {"status":"PASS","erratum":"12YE_TWO_LANE_CONCATENATION_RETRACTED","valid_short_prints":5,"valid_long_prints":5,"paired_recurrence_checks":4,"cross_witness_final":"0/6"}
def replay(archive,d):
 from PIL import Image
 raw=Path(archive).read_bytes();src=d["original_copy"]
 need(len(raw)==src["zip_size"] and hashlib.sha256(raw).hexdigest()==src["zip_sha256"],"ZIP SHA")
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  need(z.testzip() is None,"ZIP CRC")
  report=json.loads(z.read("report.json"));need(report["book_cd"]=="GK00893_00" and len(report["physical_pages"])==204,"original source")
  img=None
  for p in report["physical_pages"]:
   b=z.read("physical/"+p["page"]+".jpg")
   need(hashlib.sha256(b).hexdigest()==p["sha256"] and len(b)==p["bytes"],"original JPEG mismatch")
   if p["page"]=="002b":img=b
  need(hashlib.sha256(img).hexdigest()==src["source_page_sha256"],"source day page")
  full=Image.open(io.BytesIO(img)).convert("RGB"); need(full.size==(1150,2000),"source dimensions")
  for roi in d["native_rgb_rois"]["per_column"]:
   need(hashlib.sha256(full.crop(tuple(roi["rect_px"])).tobytes()).hexdigest()==roi["sha256"],"original distinct lane ROI")
 return {"status":"PASS","verified_source_images":204,"verified_distinct_lane_rois":10}
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--archive");z=a.parse_args()
 d,*others=load();print(json.dumps(verify(d,*others),ensure_ascii=False))
 if z.archive:print(json.dumps(replay(z.archive,d),ensure_ascii=False))
