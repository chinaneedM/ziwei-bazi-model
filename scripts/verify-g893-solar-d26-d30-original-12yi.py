#!/usr/bin/env python3
"""12YI: bind D26-D30 source glyphs to G893 single original 003b, not predicted values."""
import argparse,hashlib,io,json,zipfile
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YI-G893-D26-D30-DIRECT-SOLAR-PRINT-R1.json"
S=["5.4222","5.4408","5.4594","5.4780","5.4966"]
L=["376.4083","370.9861","365.5453","360.0859","354.6079"]
SG=["五分四二二二","五分四四〇八","五分四五九四","五分四七八〇","五分四九六六"]
LG=["三百七十六分四〇八三","三百七十〇分九八六一","三百六十五分五四五三","三百六十〇分〇八五九","三百五十四分六〇七九"]
SHA=["0d8714530db50731b45d5a4d3b39df9aee4506d8051cec830e6b59b585ac7698","cb4a9ddcdbf86a9122cbba4254e68ba7c3461b1239f48ab62b3be84f48021e0f","0afe5ffeea904c812471279445da49fbb6aa2429210cbd40bf3571753afd70c2","33157d4170ba9e13942f29591eb76178c8d3ca4cc555f813d957aaabbfb6e2a9","4ff770dd5d62ccd68a9703aea95bd42ea736f38f81c66e8ec1f55f04b12271bc","827bbcb7de13bde350f4ae55e7c048dff1312466ef1db136e60636b3f9863eab","cc2eb6389aefe62d0fd174c82c05f68427f41e9402c96e92535c7b252b957396","7c5ec0162b7a3f14ab461013cf74e7f885db1d9f32753a0db57dd0b22fd36516","052acd175a9784fbae1b509552da42b2fae21d532d4a839a3f474d7911ecd883","ea17c701c96fc7f66c3f16036deb0e65faddc75eae3ef76467fe8cb7ff8b1af3"]
RECTS=[[815,600,866,1420],[870,600,918,1420],[620,600,672,1420],[675,600,723,1420],[426,600,478,1420],[482,600,533,1420],[224,600,279,1420],[283,600,333,1420],[29,600,80,1420],[84,600,133,1420]]
def need(value,reason):
 if not value:raise ValueError(reason)
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json"))
def verify(d,ledger,state):
 need(d["schema"]=="TIANWEN-12YI-G893-DIRECT-PRINT-SOLAR-D26-D30-R1" and d["source_id"]=="EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893","schema")
 o=d["archive"]
 need(o["size"]==33525981 and o["sha256"]=="ee9ecf1de3bb6abe5678e0f8ec8383ef985051e77d091ee40840756e57081107" and o["crc"]=="PASS" and o["report_verified_original_jpegs"]==204 and o["physical_original_copies"]==1 and o["new_independent_physical_copies"]==o["original_images_committed"]==0,"original ZIP/physical independence")
 need(d["pages"]==[{"id":"003b","sha256":"b0d63e97ce934193120bf4bb1970b9a7a2764b65d7276762c01c315f00a7254b"}],"source leaf")
 prior=json.loads((ROOT/d["prior_direct_source"]).read_text(encoding="utf-8"))
 b=d["baseline_D25"];p=prior["direct_glyph_readings"][-1]
 need((b["day"],b["page"],b["short_decimal"],b["long_decimal"])==(p["day"],p["page"],p["short_decimal"],p["long_decimal"])==(25,"003b","5.4036","381.8119"),"prior source D25 seam")
 rows=d["direct_glyph_readings"];need(len(rows)==5,"five days")
 for i,x in enumerate(rows):
  need((x["day"],x["page"],x["short_glyph"],x["short_decimal"],x["long_glyph"],x["long_decimal"])==(26+i,"003b",SG[i],S[i],LG[i],L[i]),"direct printed glyph/source-lane mismatch")
 roi=d["source_rois"];need(len(roi)==10,"ten independent ROIs on one original")
 for i,x in enumerate(roi):
  need((x["day"],x["page"],x["lane"],x["rect"],x["sha256"])==(26+i//2,"003b","LONG" if i%2==0 else "SHORT",RECTS[i],SHA[i]),"original image ROI checksum/coordinates")
  a,t,b,z=x["rect"];need(0<=a<b<=1150 and 0<=t<z<=2000,"bounds")
 for i in range(5):
  need(roi[2*i]["rect"][2]<roi[2*i+1]["rect"][0],"column collision")
 a=d["exact_arithmetic"];ss=[Decimal("5.4036")]+list(map(Decimal,S));ls=[Decimal("381.8119")]+list(map(Decimal,L))
 diff=[ls[i+1]-ls[i] for i in range(5)]
 need([str(x) for x in diff]==a["long_differences"]==a["negative_previous_short"]==["-5.4036","-5.4222","-5.4408","-5.4594","-5.4780"],"source arithmetic")
 need(diff==[-ss[i] for i in range(5)] and [str(diff[i]+ss[i]) for i in range(5)]==a["residuals"]==["0.0000"]*5,"residual")
 need([str(ss[i+1]-ss[i]) for i in range(5)]==a["short_first_differences"]==["0.0186"]*5,"short differences")
 need([str(ls[i+2]-2*ls[i+1]+ls[i]) for i in range(4)]==a["long_second_differences"]==["-0.0186"]*4,"long second differences")
 need(a["precision"]=="EXACT_DECIMAL_4" and a["identity"]=="L(d+1)=L(d)-S(d), D25-D30 source-original sampled only","false universal law")
 h=d["historical_error_precedence"]
 need(h["previous_12ye_eight_places"]=="RETRACTED" and h["previous_12yf_ascending_long"]=="RETRACTED_BY_12YG" and h["source_correct_12yg"]==h["source_correct_12yh"]=="PRESERVED" and h["new_12yi"]=="APPENDED_ONLY" and h["second_reviewer"]=="NOT_INDEPENDENTLY_COMPLETED","erratum or second reviewer falsely promoted")
 lim=d["unresolved"]
 need(all(lim[k]=="UNPROVEN" for k in ("original_header_001a_to_lanes","old_unit_second_shao","ming1569_same_numeric_field","whole_table_law","copying_lineage")),"historical overreach")
 need(lim["original_formal_target_fields"]=="5/6" and lim["cross_witness_mechanical_final"]=="0/6" and lim["open_research_issues"]==11 and all(lim[k]==0 for k in ("new_source_registry_entries","new_genealogy_edges","algorithm_reopens")),"false closure")
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 need(issue["status"]=="OPEN" and DOC in issue["source_refs"] and DOC.replace(".json",".md") in issue["source_refs"],"issue preservation")
 rec=issue["g893_12yi_extended_source_print_reviews"];need(len(rec)==1,"source snapshot cardinality")
 x=rec[0]
 need(x["evidence_doc"]==DOC and x["source_pages"]==["003b"] and x["old_12yh_d25_baseline"]==["5.4036","381.8119"] and x["correct_d26_d30_short"]==S and x["correct_d26_d30_long"]==L,"forward source binding")
 need(x["new_original_same_copy_days"]==5 and x["new_source_rois"]==10 and x["arithmetic_exact_new_edges"]==5 and x["original_jpegs_verified"]==204 and x["no_new_external_votes"]==x["no_new_physical_originals"]==x["algorithm_reopens"]==0,"false independent votes")
 need(any(z.get("event")=="G893_D26_D30_DIRECT_SOURCE_CONTINUATION_12YI_APPEND" and DOC in z.get("evidence_refs",[]) for z in issue["history"]),"append history")
 need(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,state["schema_version"].split(".")))>=(1,622,0),"state version")
 need(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0 and any(x.startswith("12YI ") for x in state["historical_audit"]["current_focus"]),"unapproved algorithm reopen")
 return {"status":"PASS","native_source_days":5,"original_ROIs":10,"local_new_exact_edges":5,"same_copy_day_span":"D14-D30","cross_witness_final":"0/6"}
def replay_archive(path,d):
 from PIL import Image
 raw=Path(path).read_bytes();o=d["archive"]
 need(len(raw)==o["size"] and hashlib.sha256(raw).hexdigest()==o["sha256"],"source zip SHA")
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  need(z.testzip() is None,"ZIP CRC")
  report=json.loads(z.read("report.json"));need(report["book_cd"]=="GK00893_00" and len(report["physical_pages"])==204,"physical page manifest")
  for x in report["physical_pages"]:
   b=z.read("physical/"+x["page"]+".jpg")
   need(len(b)==x["bytes"] and hashlib.sha256(b).hexdigest()==x["sha256"],"original JPEG hash mismatch")
  jpg=z.read("physical/003b.jpg")
  need(hashlib.sha256(jpg).hexdigest()==d["pages"][0]["sha256"],"003b source SHA")
  rgb=Image.open(io.BytesIO(jpg)).convert("RGB")
  for x in d["source_rois"]:
   need(hashlib.sha256(rgb.crop(tuple(x["rect"])).tobytes()).hexdigest()==x["sha256"],"original native RGB ROI mismatch")
 return {"status":"PASS","source_JPEG_SHA_verified":204,"native_RGB_ROI_SHA_verified":10}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--archive");args=p.parse_args()
 d,*rest=load();print(json.dumps(verify(d,*rest),ensure_ascii=False))
 if args.archive:print(json.dumps(replay_archive(args.archive,d),ensure_ascii=False))
