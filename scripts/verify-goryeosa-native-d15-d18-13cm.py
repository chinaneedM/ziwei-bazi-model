#!/usr/bin/env python3
"""13CM source-native six new ROIs from verified archived original JPEGs, with optional binary replay."""
import argparse,hashlib,json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CM-GORYEOSA-TWO-HOLDING-D15-D18-NATIVE-SHORT-LONG-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def git_sha(p):
 raw=(ROOT/p).read_bytes()
 return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def D(v):return Decimal(v)
def check(e,s,l,prior,binary_paths=None):
 assert e["schema"]=="TIANWEN-13CM-ORIGINAL-TWO-HOLDING-D15-D18-LONG-SHORT-NATIVE-RGB-COLLATION-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 assert e["recovery_method"]["original_jpeg_count"]==3
 assert e["recovery_method"]["existing_historical_physical_copy_count"]==2
 assert e["recovery_method"]["source_archive_binaries_committed_to_repo"] is False
 for key,record in e["frozen_previous_git_blobs"].items():
  assert git_sha(record["path"])==record["sha"]
  assert prior[key] is not None
 a=prior["13CH"]["photos"]
 sources=e["original_sources"]
 assert set(sources)=={"W23","N17","N18"}
 assert sources["W23"]["jpeg_sha256"]==a["W23"]["original_jpeg_sha256"]
 assert sources["N17"]["jpeg_sha256"]==a["N17"]["original_jpeg_sha256"]
 assert sources["N18"]["jpeg_sha256"]==a["N18"]["original_jpeg_sha256"]
 assert sources["N17"]["holding"]==sources["N18"]["holding"]
 assert sources["N17"]["archived_zip_sha256"]==sources["N18"]["archived_zip_sha256"]
 assert sources["W23"]["holding"]!=sources["N17"]["holding"]
 assert sources["N17"]["github_actions_artifact_id"]==sources["N18"]["github_actions_artifact_id"]
 old=prior["13CI"]["rois"]
 assert len(e["native_original_rois"])==6
 expected={
  ("W23",15,"LONG"):("四百三十四八二四九","434.8249",(1576,680,1622,1410),"a3c7a4d375073cbed69ec3c00b4421fffdc0e72c2ddc6aab476ed0d9d5614a9d"),
  ("W23",15,"SHORT"):("五分二一七六","5.2176",(1622,680,1664,1410),"c230d004b4f5bd0b28359c10b2382bb22dc13603450172fdc9e7b1b5b1eb3d8b"),
  ("N17",15,"LONG"):("四百三十四八二四九","434.8249",(772,870,815,1775),"455bb6ddb8284977444a767408a80a35abfffa2b97bdb7c47aba9365c68d6cd4"),
  ("N17",15,"SHORT"):("五分二一七六","5.2176",(815,870,852,1775),"e29c504fcfd53a2a56c54481a3b069718466182fb089cb21de2d1d9dc7dddf55"),
  ("W23",18,"SHORT"):("五分二七三四","5.2734",(889,685,937,1400),"876e24eccf051b42cc9db1befb07b3b144b3ce6d8be9bbc5a6a5898b48b5cc44"),
  ("N18",18,"SHORT"):("五分二七三四","5.2734",(2385,835,2440,1775),"7d1481dd09794d79b577989454881fede694e19403b23a30e585e44bad6aeaa2")
 }
 assert set((r["source"],r["printed_day"],r["field"]) for r in e["native_original_rois"])==set(expected)
 for z in e["native_original_rois"]:
  k=(z["source"],z["printed_day"],z["field"])
  literal,num,box,sha=expected[k]
  assert (z["original_literal"],z["decimal"],tuple(z["bbox"]),z["rgb_sha256"])==(literal,num,box,sha)
  assert z["original_day_heading_from"]=="13CH"
  h=next(v for v in a[z["source"]]["day_header_rois"] if v["day"]==z["printed_day"])
  x1,y1,x2,y2=z["bbox"]
  hx1,hy1,hx2,hy2=h["bbox"]
  assert hx1<=x1<x2<=hx2 and hy2<y1
  assert (x2-x1)>10 and (y2-y1)>250
  assert z["source"] in sources
 for source,day,field,val in [
  ("W23",16,"SHORT","5.1362"),("N17",16,"SHORT","5.1362"),
  ("W23",17,"SHORT","5.2548"),("N17",17,"SHORT","5.2548"),
  ("W23",16,"LONG","429.6073"),("N17",16,"LONG","429.6073"),
  ("W23",17,"LONG","424.3711"),("N17",17,"LONG","424.3711")]:
  assert any(x["source"]==({"N17":"NAJ17","N18":"NAJ18","W23":"W23"}[source]) and x["printed_day"]==day and x["field"]==field and x["decimal"]==val for x in old)
 ar=e["original_local_arithmetic"]
 assert ar["d15_short"]==ar["d18_short"][:0]+"5.2176"
 assert (D(ar["d15_short"]),D(ar["d16_short_both_prior"]),D(ar["d17_short_both_prior"]),D(ar["d18_short"]))==(D("5.2176"),D("5.1362"),D("5.2548"),D("5.2734"))
 shorts=[D(ar[k]) for k in ["d15_short","d16_short_both_prior","d17_short_both_prior","d18_short"]]
 longs=[D(ar[k]) for k in ["d15_long","d16_long_both_prior","d17_long_both_prior","d18_long_both_prior"]]
 for i,key in enumerate(["local_delta_s15_to_s16","local_delta_s16_to_s17","local_delta_s17_to_s18"]):
  assert shorts[i+1]-shorts[i]==D(ar[key])
 for i,key in enumerate(["long_delta_d15_to_d16","long_delta_d16_to_d17","long_delta_d17_to_d18"]):
  assert longs[i]-longs[i+1]==D(ar[key])
 assert longs[0]-longs[1]==shorts[0]
 assert longs[1]-longs[2]==D(ar["isolated_d16_numeric_midpoint_conjecture"])==(shorts[0]+shorts[2])/2
 assert D(ar["original_d16_short_always_read"])==shorts[1]
 assert D(ar["delta_conjecture_minus_source"])==D("0.1000")
 assert ar["local_arithmetic_is_not_original_emendation"] is True
 assert ar["global_historical_recurrence"] is False
 assert prior["13CL"]["local_received_arithmetic"]["two_step_consistent_midpoint_candidate_D16"]=="5.2362"
 assert prior["13CL"]["local_received_arithmetic"]["printed_original_D16_two_physical_holdings"]=="5.1362"
 limits=e["limitations"]
 assert limits["new_source_native_rgb_crops"]==6
 assert limits["new_original_jpegs"]==limits["new_physical_copy_witnesses"]==0
 assert limits["no_independent_stemmatic_votes"] is True
 for k in ["waseda_D16_same_day_C","naj_D17_same_day_C"]:assert limits[k]=="UNBOUND"
 assert limits["original_d16_short_5_2362"]=="NOT_ATTESTED"
 assert limits["G893_shao_wei_Ming1569_units"]=="UNPROVEN"
 assert limits["OCR_used"] is False
 for k in ["new_external_source_registry_rows","new_historical_matrix_rows","new_transmission_nodes","new_transmission_edges","independent_stemmatic_votes","algorithm_reopens"]:assert e["scope"][k]==0
 assert e["scope"]["open_or_blocked_risks"]==11 and e["scope"]["product"]=="CLOSED"
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 assert s["invariants"]["algorithm_reopen_count"]==0
 assert s["historical_audit"]["row_count"]==s["historical_audit"]["audited_row_count"]==222
 assert s["historical_audit"]["external_source_registry_total_unique_count"]==754
 assert any(t.startswith("13CM ") for t in s["historical_audit"]["current_focus"])
 assert l["binding"]["reviewed_state_version"]==s["schema_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13CM-NATIVE-ROI" for x in issue["history"])
 assert any(x["id"]=="OMISSIONS-13CM-NATIVE-D15-D18-20261022" for x in l["checkpoint_log"])
 assert len([x for x in l["issues"] if x["status"] in ["OPEN","BLOCKED_SOURCE_ACCESS"]])==11
 if binary_paths:
  from PIL import Image
  for k in sources:
   assert k in binary_paths
   raw=Path(binary_paths[k]).read_bytes()
   assert hashlib.sha256(raw).hexdigest()==sources[k]["jpeg_sha256"]
   im=Image.open(binary_paths[k]).convert("RGB")
   assert list(im.size)==sources[k]["dimensions"]
   for z in e["native_original_rois"]:
    if z["source"]==k:
     crop=im.crop(tuple(z["bbox"]))
     assert hashlib.sha256(crop.tobytes()).hexdigest()==z["rgb_sha256"]
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument("--w23-jpeg",type=Path);p.add_argument("--n17-jpeg",type=Path);p.add_argument("--n18-jpeg",type=Path)
 args=p.parse_args()
 files=[args.w23_jpeg,args.n17_jpeg,args.n18_jpeg]
 assert all(x is None for x in files) or all(x is not None for x in files),"all three JPEG paths required or none"
 binary=dict(zip(["W23","N17","N18"],files)) if files[0] else None
 e=load(E)
 old={k:load(z["path"]) for k,z in e["frozen_previous_git_blobs"].items()}
 assert check(e,load(S),load(L),old,binary)
 print("TIANWEN_13CM_DIRECT_ORIGINAL_D15_D18=PASS; PIXEL_REPLAY="+("YES" if binary else "METADATA_ONLY"))
