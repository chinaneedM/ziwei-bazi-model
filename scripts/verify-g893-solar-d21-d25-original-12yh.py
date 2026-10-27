#!/usr/bin/env python3
"""12YH: same-original G893 exact D20-D25 separate source solar lanes; 12YE/F withdrawn."""
import argparse,hashlib,io,json,zipfile
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YH-G893-D21-D25-DIRECT-SOLAR-PRINT-CROSSLEAF-R1.json"
S=["5.3292","5.3478","5.3664","5.3850","5.4036"]
L=["403.2403","397.9111","392.5633","387.1969","381.8119"]
SG=["五分三二九二","五分三四七八","五分三六六四","五分三八五〇","五分四〇三六"]
LG=["四百〇三分二四〇三","三百九十七分九一一一","三百九十二分五六三三","三百八十七分一九六九","三百八十一分八一一九"]
SHA=["4be18fc49297ada3c853e4478c9408dc51dc3f4e2bdfeb4bf6e6d76feaf19cec","2d89b91c47a3420666188f5098d06b9dbce620ac04aca3cb8cf1f4efb7b48208","9357d463b0d5875d5a021b50eba90a7cbfe8e98992ea145c365fd7f9eecded2d","fd4e26d7e677d38da6b1bd57989c3e5db1595877accbf70877f5f1069e78174b","3c333d22dcd8ed6fdd2f97eb954b6fda57717aa740bc0155c6f64342963e2570","a0b9a9f33d5fbc4a39942a729bcb177ce38ea73ec393d2b396c6d39f1cf43a52","7a0ecf6fd16d23beec2b0513da9e146521e9de61ccd1184dacd484eb8eb12ed4","d1fa9a5aa8085fc1dec26544e2d7ea4955a9314a7bc338d50c0368ef91959607","095ca408a8ac4db385ecead5dc4145e3050b3bae2b04e1e1c8d734435e473508","45ad9c07aef600d4d5c1da3991b5c98e72273112bede60f9c66000975772c2dc"]
def need(value,reason):
 if not value:raise ValueError(reason)
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json"))
def verify(d,ledger,state):
 need(d["schema"]=="TIANWEN-12YH-G893-DIRECT-PRINT-SOLAR-D21-D25-R1" and d["source_id"]=="EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893","schema")
 o=d["archive"];need(o["size"]==33525981 and o["sha256"]=="ee9ecf1de3bb6abe5678e0f8ec8383ef985051e77d091ee40840756e57081107" and o["crc"]=="PASS" and o["report_verified_original_jpegs"]==204 and o["physical_original_copies"]==1 and o["new_independent_physical_copies"]==o["original_images_committed"]==0,"original archive")
 need([(x["id"],x["sha256"]) for x in d["pages"]]==[("003a","8f9df8af972a76ec5939d7fb6c2bbe4400a8e2505a6253fe4ba6bc9fcc3f6966"),("003b","b0d63e97ce934193120bf4bb1970b9a7a2764b65d7276762c01c315f00a7254b")],"original folio SHA")
 prior=json.loads((ROOT/d["prior_direct_source"]).read_text(encoding="utf-8"))
 base=d["baseline_D20"];a=prior["readings"][-1]
 need((base["day"],base["page"],base["short_decimal"],base["long_decimal"])==(a["day"],a["page"],a["short_decimal"],a["long_decimal"])==(20,"003a","5.3106","408.5509"),"prior D20 physical source seam")
 rows=d["direct_glyph_readings"];need(len(rows)==5,"five independent native rows")
 for i,row in enumerate(rows):
  expected=(i+21,"003a" if i<4 else "003b",SG[i],S[i],LG[i],L[i])
  need((row["day"],row["page"],row["short_glyph"],row["short_decimal"],row["long_glyph"],row["long_decimal"])==expected,"glyph or decimal transcription mismatch")
 rois=d["source_rois"];need(len(rois)==10 and [x["sha256"] for x in rois]==SHA,"native 10 ROI SHA")
 for i in range(5):
  a,b=rois[2*i:2*i+2];day=i+21;page="003a" if i<4 else "003b"
  need((a["day"],a["page"],a["lane"],b["day"],b["page"],b["lane"])==(day,page,"LONG",day,page,"SHORT"),"column/day identity")
  need(a["rect"][2]<b["rect"][0],"source column collision")
  for q in (a,b):
   left,top,right,bottom=q["rect"];need(0<=left<right<=1150 and 0<=top<bottom<=2000,"source crop bounds")
 a=d["exact_arithmetic"];ss=[Decimal("5.3106")]+list(map(Decimal,S));ls=[Decimal("408.5509")]+list(map(Decimal,L))
 diff=[ls[i+1]-ls[i] for i in range(5)];neg=[-ss[i] for i in range(5)]
 need(diff==neg and [str(z) for z in diff]==a["long_differences"]==a["negative_previous_short"]==["-5.3106","-5.3292","-5.3478","-5.3664","-5.3850"],"exact long subtraction")
 need([str(diff[i]+ss[i]) for i in range(5)]==a["residuals"]==["0.0000"]*5,"bad residual")
 need([str(ss[i+1]-ss[i]) for i in range(5)]==a["short_first_differences"]==["0.0186"]*5,"short stage")
 need([str(ls[i+2]-2*ls[i+1]+ls[i]) for i in range(4)]==a["long_second_differences"]==["-0.0186"]*4,"long second")
 need(a["precision"]=="EXACT_DECIMAL_4" and a["identity"]=="L(d+1)=L(d)-S(d), D20-D25 sampled original only","false universal formula")
 h=d["historical_error_precedence"]
 need(h["previous_12ye_eight_places"]=="RETRACTED" and h["previous_12yf_ascending_long"]=="RETRACTED_BY_12YG" and h["source_correct_12yg"]=="PRESERVED" and h["new_12yh"]=="APPENDED_ONLY" and h["second_reviewer"]=="NOT_INDEPENDENTLY_COMPLETED","previous errors reinstated")
 lim=d["unresolved"]
 need(all(lim[k]=="UNPROVEN" for k in ("original_header_001a_to_lanes","old_unit_second_shao","ming1569_same_numeric_field","whole_table_law","copying_lineage")),"field overclaim")
 need(lim["original_formal_target_fields"]=="5/6" and lim["cross_witness_mechanical_final"]=="0/6" and lim["open_research_issues"]==11 and all(lim[k]==0 for k in ("new_source_registry_entries","new_genealogy_edges","algorithm_reopens")),"false research award")
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 need(issue["status"]=="OPEN" and DOC in issue["source_refs"] and DOC.replace(".json",".md") in issue["source_refs"],"issue/source")
 review=issue["g893_12yh_extended_source_print_reviews"]
 need(len(review)==1 and review[0]["evidence_doc"]==DOC and review[0]["old_12yg_d20_baseline"]==["5.3106","408.5509"] and review[0]["correct_d21_d25_long"]==L and review[0]["correct_d21_d25_short"]==S and review[0]["no_new_external_votes"]==0,"missing crossleaf extension risk")
 need(any(x.get("event")=="G893_D21_D25_DIRECT_SOURCE_CONTINUATION_12YH_APPEND" and DOC in x.get("evidence_refs",[]) for x in issue["history"]),"forward-only history")
 need(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,state["schema_version"].split(".")))>=(1,621,0) and any(x.startswith("12YH ") for x in state["historical_audit"]["current_focus"]),"current version")
 need(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"product changed")
 return {"status":"PASS","source_direct_glyph_days":5,"distinct_original_rois":10,"crossleaf_source_edges":5,"independent_external_witnesses_added":0,"cross_witness_final":"0/6"}
def replay_archive(file,d):
 from PIL import Image
 b=Path(file).read_bytes();o=d["archive"]
 need(len(b)==o["size"] and hashlib.sha256(b).hexdigest()==o["sha256"],"zip identity")
 with zipfile.ZipFile(io.BytesIO(b)) as f:
  need(f.testzip() is None,"zip CRC")
  report=json.loads(f.read("report.json"));need(report["book_cd"]=="GK00893_00" and len(report["physical_pages"])==204,"physical report")
  imgs={}
  for x in report["physical_pages"]:
   b=f.read("physical/"+x["page"]+".jpg")
   need(len(b)==x["bytes"] and hashlib.sha256(b).hexdigest()==x["sha256"],"original 204 JPGs")
   if x["page"] in ("003a","003b"):imgs[x["page"]]=b
  for page in d["pages"]:
   need(hashlib.sha256(imgs[page["id"]]).hexdigest()==page["sha256"],"original page")
  rgb={x:Image.open(io.BytesIO(z)).convert("RGB") for x,z in imgs.items()}
  for roi in d["source_rois"]:
   need(hashlib.sha256(rgb[roi["page"]].crop(tuple(roi["rect"])).tobytes()).hexdigest()==roi["sha256"],"individual original pix SHA")
 return {"status":"PASS","sha_verified_original_jpegs":204,"sha_verified_native_rois":10}
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--archive");args=a.parse_args()
 d,*rest=load();print(json.dumps(verify(d,*rest),ensure_ascii=False))
 if args.archive:print(json.dumps(replay_archive(args.archive,d),ensure_ascii=False))
