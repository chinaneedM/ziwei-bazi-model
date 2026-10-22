#!/usr/bin/env python3
"""13CN original-image D19-D20 source-local two-copy comparison; optional pixel replay."""
import argparse,hashlib,json
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CN-GORYEOSA-TWO-HOLDING-D19-D20-SIX-DAY-NATIVE-R1.json"; S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def gitsha(p):
 b=(ROOT/p).read_bytes()
 return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\\0"+b).hexdigest()
def check(e,s,l,prior,images=None):
 assert e["schema"]=="TIANWEN-13CN-GORYEOSA-TWO-ORIGINAL-D19-D20-SIX-DAY-NATIVE-ROIS-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and set(prior)=={"13CH","13CM"}
 for k,z in e["frozen_previous_git_blobs"].items():
  assert gitsha(z["path"])==z["sha"]
 a=prior["13CH"]["photos"];c=prior["13CM"];src=e["original_sources"]
 assert set(src)=={"W23","N18"}
 assert src["W23"]["jpeg_sha256"]==a["W23"]["original_jpeg_sha256"]==c["original_sources"]["W23"]["jpeg_sha256"]
 assert src["N18"]["jpeg_sha256"]==a["N18"]["original_jpeg_sha256"]==c["original_sources"]["N18"]["jpeg_sha256"]
 assert src["W23"]["physical_holding"]!=src["N18"]["physical_holding"]
 assert src["W23"]["archive_zip_sha256"]==c["original_sources"]["W23"]["archived_zip_sha256"]
 assert src["N18"]["archive_zip_sha256"]==c["original_sources"]["N18"]["archived_zip_sha256"]
 assert len(e["direct_original_rois"])==8
 expected={
 ("W23",19,"SHORT"):("五分二九二〇","5.2920",(719,685,767,1400),"049ee7aa3091bf66357c9221c6ed631c6b2b38e3472424b905355602a1d9ea23"),
 ("W23",20,"SHORT"):("五分三一〇六","5.3106",(539,685,587,1400),"b02fef7761445b0333f22212fc70a1ed6afe4b6c3bc8d77e83575485677ab641"),
 ("N18",19,"SHORT"):("五分二九二〇","5.2920",(2215,835,2270,1775),"36fff605adb4f8b25eb49f3f022167fa1c587d6d669b64a038f3c8180d6229da"),
 ("N18",20,"SHORT"):("五分三一〇六","5.3106",(2045,835,2100,1775),"1fa8930d11d779f2cea67ee1bc856e5a9021ce016aa8dde70770ccc2f336bb7b"),
 ("W23",19,"LONG"):("四百一十三八四二九","413.8429",(684,685,719,1400),"54ac766821bea1f6b43d89dce4c47e54610f7251d3fb9ebb8a69920922c264d4"),
 ("W23",20,"LONG"):("四百〇八五五〇九","408.5509",(504,685,539,1400),"aafd66690ecdeaae7614b5dac4b3a66b27ef495b3ac09749820881436b711a9d"),
 ("N18",19,"LONG"):("四百一十三八四二九","413.8429",(2190,835,2240,1775),"5a1dec6df6919b25d907890cf86cff7fed18469ab9109ad847f6a6cc81a3b3d4"),
 ("N18",20,"LONG"):("四百〇八五五〇九","408.5509",(2020,835,2070,1775),"df3442a88c6a843badc62d7ad4068d37808ce0d9c433fc65893a9ec1aca7c345")}
 assert set((r["source"],r["printed_day"],r["field"]) for r in e["direct_original_rois"])==set(expected)
 for r in e["direct_original_rois"]:
  k=r["source"],r["printed_day"],r["field"]
  assert (r["original_literal"],r["decimal"],tuple(r["bbox"]),r["rgb_sha256"])==expected[k]
  assert r["original_day_heading_from"]=="13CH" and r["method"]=="PIL_RGB_CROP_TOBYTES_SHA256_MANUAL_VISUAL_NO_OCR"
  heading=next(h for h in a[r["source"]]["day_header_rois"] if h["day"]==r["printed_day"])
  x1,y1,x2,y2=r["bbox"];hx1,hy1,hx2,hy2=heading["bbox"]
  assert hx1<=x1<x2<=hx2 and hy2<y1<y2
 ar=e["same_field_local_arithmetic"]
 assert (ar["d18_short_source_native_prior"],ar["d18_long_source_native_prior"])==("5.2734","419.1163")
 assert any(r["source"]=="W23" and r["field"]=="SHORT" and r["printed_day"]==18 and r["decimal"]==ar["d18_short_source_native_prior"] for r in c["native_original_rois"])
 assert (ar["d19_short_original_both"],ar["d20_short_original_both"],ar["d19_long_original_both"],ar["d20_long_original_both"])==("5.2920","5.3106","413.8429","408.5509")
 assert D(ar["d19_short_original_both"])-D(ar["d18_short_source_native_prior"])==D(ar["delta_d18_d19"])==D("0.0186")
 assert D(ar["d20_short_original_both"])-D(ar["d19_short_original_both"])==D(ar["delta_d19_d20"])==D("0.0186")
 assert D(ar["d18_long_source_native_prior"])-D(ar["d19_long_original_both"])==D(ar["long_d18_minus_d19"])==D("5.2734")
 assert D(ar["d19_long_original_both"])-D(ar["d20_long_original_both"])==D(ar["long_d19_minus_d20"])==D("5.2920")
 assert ar["d16_short_source_native_prior"]==c["original_local_arithmetic"]["original_d16_short_always_read"]=="5.1362"
 assert ar["d16_short_derived_candidate_only"]=="5.2362" and ar["original_d16_emendation_authorized"] is False
 lim=e["limitations"];scope=e["scope"]
 assert lim["two_existing_physical_holding_count"]==2 and lim["new_original_source_images"]==0 and lim["new_source_native_rgb_rois"]==8
 assert lim["no_new_physical_copy_votes"] is True and lim["D16_printed_short"]=="5.1362" and lim["D16_conjectured_short"]=="NOT_ORIGINALLY_ATTESTED"
 assert lim["W_D16_same_day_cumulative"]==lim["NAJ_D17_same_day_cumulative"]=="UNBOUND"
 assert lim["G893_shao_wei_vs_Ming1569_units"]=="UNPROVEN" and lim["OCR_used"] is False
 assert all(scope[k]==0 for k in ["new_external_registry_rows","new_matrix_rows","new_lineage_nodes","new_lineage_edges","new_independent_votes","algorithm_reopens"])
 assert scope["open_issues"]==11 and scope["product"]=="CLOSED"
 assert s["historical_audit"]["row_count"]==s["historical_audit"]["audited_row_count"]==222
 assert s["historical_audit"]["external_source_registry_total_unique_count"]==754
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0
 assert s["historical_audit"]["latest_batch_doc"]=="docs/research/TIANWEN-13CN-GORYEOSA-TWO-HOLDING-D19-D20-SIX-DAY-NATIVE-R1.md"
 assert any(t.startswith("13CN ") for t in s["historical_audit"]["current_focus"])
 assert l["binding"]["reviewed_state_version"]==s["schema_version"] and l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13CN-NATIVE-ROI" for x in issue["history"])
 assert any(x["id"]=="OMISSIONS-13CN-NATIVE-D19-D20-20261022" for x in l["checkpoint_log"])
 assert len([x for x in l["issues"] if x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS")])==11
 if images is not None:
  from PIL import Image
  assert set(images)==set(src)
  for k,path in images.items():
   raw=Path(path).read_bytes();assert hashlib.sha256(raw).hexdigest()==src[k]["jpeg_sha256"]
   im=Image.open(path).convert("RGB");assert list(im.size)==src[k]["dimensions"]
   for roi in e["direct_original_rois"]:
    if roi["source"]==k:assert hashlib.sha256(im.crop(tuple(roi["bbox"])).tobytes()).hexdigest()==roi["rgb_sha256"]
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--w23-jpeg",type=Path);p.add_argument("--n18-jpeg",type=Path);args=p.parse_args()
 assert bool(args.w23_jpeg)==bool(args.n18_jpeg),"Both original JPEGs required for pixel replay"
 paths={"W23":args.w23_jpeg,"N18":args.n18_jpeg} if args.w23_jpeg else None
 e=load(E)
 assert check(e,load(S),load(L),{k:load(v["path"]) for k,v in e["frozen_previous_git_blobs"].items()},paths)
 print("TIANWEN_13CN_SOURCE_NATIVE_D19_D20=PASS; PIXEL_REPLAY="+("YES" if paths else "METADATA_ONLY"))
