#!/usr/bin/env python3
"""13ID: original-source layout re-read and immutable history errata."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];E="docs/research/TIANWEN-13ID-WASEDA-ORIGINAL-TABLE-START-LEFT-C-D17-D21-ERRATUM-R1.json"
def load(p):return json.loads((R/p).read_text(encoding="utf8"))
def check(e,with_state=True):
 assert e["schema"]=="TIANWEN-13ID-DIRECT-ARCHIVED-SOURCE-ORIGINAL-TABLE-START-DAY-C-FIREWALL-R1"
 assert e["issue"]=="TW-OPEN-0005" and len(e["roi"])==16
 src={}
 for d in e["dependencies"]:
  b=(R/d["path"]).read_bytes()
  assert hashlib.sha1(b"blob "+str(len(b)).encode()+bytes([0])+b).hexdigest()==d["sha"]
  src[d["k"]]=json.loads(b)
 assert len(src)==10
 assert e["images"]["W21"]["sha"]==src["CG"]["sources"]["WASEDA"]["original_jpeg_sha256"]
 assert e["images"]["W23"]["sha"]==src["BO"]["source"]["jpeg_sha256"]==src["BJ"]["source"]["original_jpeg_sha256"]
 assert e["images"]["W24"]["sha"]==src["BM"]["source"]["pages"][1]["jpeg_sha256"]
 assert e["images"]["N18"]["sha"]==src["BT"]["firstparty_source"]["jpeg_sha256"]
 r={(x[0],x[1]):x for x in e["roi"]}
 assert len(r)==16
 for day in [1,2,17,18,19,20,21]:
  k="W21" if day<=2 else ("W24" if day==21 else "W23")
  c=r[(k,f"D{day}_C")][2];h=r[(k,f"D{day}_HEAD")][2]
  assert c[0]+c[2]<h[0]+h[2],("C ink must be left of day heading",day)
 nhead=r[("N18","D18_HEAD")][2];nc=r[("N18","D18_C")][2]
 assert nc[0]>nhead[2]
 for i,(day,glyph,num) in enumerate(e["local_values"]):
  assert int(day)==17+i
  assert [num for _,_,num in e["local_values"]]==[80002697,84246408,88437571,92576000,96661509]
  if int(day)<=18:
   old=next(x for x in src["BO"]["original_numeric_rois"] if x["key"]=="P23_D"+day+"_C")
   assert old["literal"]==glyph and int(old["value"].replace(".",""))==num
   assert old["pixel_sha256"]==r[("W23","D"+day+"_C")][3]
  else:
   key=("P24_" if int(day)==21 else "P23_")+day+"_C"
   old=next(x for x in src["BN"]["original_single_numeric_lane_rois"] if x["key"]==key)
   assert old["original_literal"]==glyph and int(old["value"].replace(".",""))==num
   assert old["rgb_sha256"]==r[("W24" if int(day)==21 else "W23","D"+day+"_C")][3]
 assert [e["local_values"][i+1][2]-e["local_values"][i][2] for i in range(4)]==e["arithmetic"]["deltas"]==[4243711,4191163,4138429,4085509]
 assert src["BM"]["correction"]["legacy_labelled_printed_day"]==20 and src["BM"]["correction"]["source_original_corrected_printed_day"]==19
 assert src["BT"]["paired_original_field_columns"][0]["day"]==18 and src["BT"]["paired_original_field_columns"][0]["cumulative_value"]=="8000.2697"
 assert src["BT"]["paired_original_field_columns"][1]["day"]==19 and src["BT"]["paired_original_field_columns"][1]["cumulative_value"]=="8424.6408"
 assert src["CD"]["positive_literal_position_matches"][1]["observed_naj_minus_waseda_heading_offset"]==1
 assert src["IA"]["actual_original_printed_D18_C"]=="八千〇〇〇二六九七"
 assert src["IB"]["printed"]["D18"]["C"]==80002697 and src["IC"]["new_cross_holding_local_d18_c_offset"]==0
 x=e["holder_comparison"]
 assert (x["W_D17_B_NAJ_D17_B"],x["W_D17_C8000_NAJ_D18_C8000"],x["W_D18_C8424_NAJ_D19_C8424"])==(0,1,1)
 assert x["same_global_index_law"]=="UNPROVEN"
 assert e["table_start"]["day_1_C"]=="五百一十〇八五六九" and e["table_start"]["day_2_C"]=="一千〇一十六七七五二"
 assert e["table_start"]["initial_day_under_red_slip"]=="DO_NOT_INFER_HIDDEN_ROW"
 assert set(e["forward_errata"]["reaffirm"])=={"13BO","13BM","13BN","13CD_SCOPED_ORIGINAL_ORIGINAL","13CF_SPATIAL_ONLY"}
 assert all(e["forward_errata"].get(q) for q in ("BJ","IA","IB","IC"))
 f=e["firewalls"]
 assert f["NIKH_edited_D18_C_literal"]=="八千四百二十四六四〇八三"
 assert f["Wase_original_D18_C_literal"]=="八千四百二十四六四〇八"
 assert f["wase_d16_original"]=="五分一三六二" and f["wase_d16_computed_not_original"]=="五分二三六二"
 assert f["modern_raw_terminal_three_retained"]
 for q in ("new_historical_original_witnesses","new_registered_sources","new_graph_nodes","new_graph_edges","algorithm_reopened","candidates_collapsed"):assert f[q]==0
 assert f["unresolved_issues"]==11 and f["product"]=="CLOSED" and f["matrix"]==[222,222] and f["source_count"]==761 and f["graph"]==[252,238]
 if with_state:
  s=load("docs/PROJECT-CURRENT-STATE-R1.json");ld=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
  assert s["schema_version"]==ld["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
  assert tuple(map(int,s["schema_version"].split(".")))>=(1,883,0)
  assert any(t.startswith("13ID ") for t in s["historical_audit"]["current_focus"])
  assert ld["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split()[0]
  assert ld["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
  q=next(z for z in ld["issues"] if z["id"]=="TW-OPEN-0005")
  assert q["status"]=="OPEN" and (q["next_action"].startswith("13ID CURRENT ACTION:") or "ARCHIVED 13ID PRIOR ACTION:" in q["next_action"])
  assert "ARCHIVED 13IC PRIOR ACTION:" in q["next_action"] and E in q["source_refs"]
  assert any(z.get("revision_id","").startswith("TW-OPEN-0005-13ID-") for z in q["history"])
 return True
def check_source_pixels(e,directory):
 from PIL import Image
 pics={}
 for key,v in e["images"].items():
  p=directory/v["filename"];b=p.read_bytes()
  assert hashlib.sha256(b).hexdigest()==v["sha"],key
  pics[key]=Image.open(p).convert("RGB");assert list(pics[key].size)==v["size"]
 for key,name,bbox,h in e["roi"]:
  assert hashlib.sha256(pics[key].crop(tuple(bbox)).tobytes()).hexdigest()==h,(key,name)
 return True
if __name__=="__main__":
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument("--source-dir",type=Path);args=parser.parse_args()
 e=load(E);assert check(e)
 if args.source_dir:assert check_source_pixels(e,args.source_dir)
 print("TIANWEN_13ID_DIRECT_TABLE_START_AND_LEFT_C_DAY_RESTORATION_PASS")
