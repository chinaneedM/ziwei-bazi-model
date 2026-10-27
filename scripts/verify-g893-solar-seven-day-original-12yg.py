#!/usr/bin/env python3
"""G893 12YG: second forward-only original-glyph erratum; source-bound seven day subtractive recurrence."""
import json,zipfile,hashlib,io,argparse
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH="docs/research/TIANWEN-12YG-G893-SEVEN-DAY-SOLAR-DECREASING-LANE-SECOND-ERRATUM-R1.json"
S=["5.1990","5.2176","5.2362","5.2548","5.2734","5.2920","5.3106"]
L=["440.0239","434.8249","429.6073","424.3711","419.1163","413.8429","408.5509"]
SG=["五分一九九〇","五分二一七六","五分二三六二","五分二五四八","五分二七三四","五分二九二〇","五分三一〇六"]
LG=["四百四十〇分〇二三九","四百三十四分八二四九","四百二十九分六〇七三","四百二十四分三七一一","四百一十九分一一六三","四百一十三分八四二九","四百〇八分五五〇九"]
ROIS=["a501af8303b7395b6e40e8e09ca5295e2c343ce7d45701aa1776999697b14ba1","cf529089ad87b4cc3c45b9431ace4b2ca13b2322f5090139d2fa4e8fd44ec119","776e4a255da4787856b45298b2a3924d2d979e83b42e05b426f34151fd84c824","b17c04be3f054f6648c6a6c87613e2ac9c3ca88a96ffa1c82d1832986fd8e14a","16a07d877e57b44447762b7ded340a755965941cac7c6dc02493374f7d465d84","d418e8c3394d02e2f5c515a5eb6eb037c0329c1cb0c2f057eeb8842d42c15ae8","fbd8db7d55680088317f4e7be84c34e8d6840048a32be65514697bcad525c935","cafcbe755599667e5dec66beac84c3eab2f4ac641748a0a5a0c4f5724fc759e9","a655439f038ff16a7aea8c6db255b3a89575f257024a7f15f358b9b3bfb2c36f","5046d008dd881484ece6e2b483a357f65c941b9ab56caa38135b8c64a1d481e5","59ba62b8307dd2825d16891d81e6a2f10834ae86a1bcfbe2e6eb85ee7b109003","1eef038a168caf1c4eb04ff33558f263d250fbf68f8f9a0d5cbc1bfcb09c0cc2","e7c70429c32d3f28b2ae4b7ca1e3c5081841857844958b7cc442f1051cdfe3b1","c4acd07d7ea237a8c66b31e6494ee101db813e2bf20a231a5ea7c15140ce648c"]
PAGES=["8b07513ca8aad42ae167a93f22c39f14850c8cd1c345db9ce98c1e0e769226a5","f9812e8c6a357eb6cd1117bb2af58d816e01030d5b93f34e7094bddb766b2b55","8f9df8af972a76ec5939d7fb6c2bbe4400a8e2505a6253fe4ba6bc9fcc3f6966"]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (PATH,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json"))
def verify(doc,ledger,state):
 need(doc["schema"]=="TIANWEN-12YG-G893-SEVEN-DAY-SECOND-ERRATUM-R1" and doc["source_id"]=="EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893","schema")
 a=doc["same_copy"];need(a["sha256"]=="ee9ecf1de3bb6abe5678e0f8ec8383ef985051e77d091ee40840756e57081107" and a["size"]==33525981 and a["crc"]=="PASS" and a["verified_original_jpegs"]==204 and a["new_physical_witnesses"]==a["committed_original_images"]==0,"original physical copy")
 pages=doc["pages"];need([p["id"] for p in pages]==["001a","002b","003a"] and [p["sha256"] for p in pages]==PAGES,"page image origins")
 h=doc["heading"];need(h["visible_original_terms"]==["盈縮積","盈縮加分","日差加一秒八十六少"] and h["unit_to_long_short_lane_mapping"]=="NOT_FORMALLY_PROVEN" and h["native_roi"]=={"page":"001a","rect":[480,580,720,1380],"sha256":"6416400c1805f41b5dc56e3ff6cc6f11b057ff6eb266bb3c8934ad8dcf7b853f"},"header source evidence and unsupported mapping")
 rois=doc["rois"];need(len(rois)==14 and [r["sha256"] for r in rois]==ROIS,"original split source image SHA")
 for i in range(7):
  a,b=rois[i*2:i*2+2];page="002b" if i<6 else "003a"; day=14+i
  need((a["page"],a["day"],a["lane"],b["page"],b["day"],b["lane"])==(page,day,"LONG",page,day,"SHORT") and a["rect"][2]<b["rect"][0],"native printed lane boundaries")
  for n in (a,b):
   left,top,right,bottom=n["rect"];need(0<=left<right<=1150 and 0<=top<bottom<=2000,"ROI bounds")
 rows=doc["readings"];need(len(rows)==7,"seven days")
 for i,row in enumerate(rows):
  need((row["day"],row["page"],row["short_glyph"],row["short_decimal"],row["long_glyph"],row["long_decimal"])==(i+14,"002b" if i<6 else "003a",SG[i],S[i],LG[i],L[i]),"wrong original printed glyph or lane")
 old=json.loads((ROOT/doc["forward_only_erratum"]["prior_12yf"]).read_text(encoding="utf-8"))
 retract=doc["forward_only_erratum"]
 need(retract["old_evidence_retained"] is True and retract["prior_original_image_hashes_valid_but_human_transcription_false"] is True and retract["prior_12ye_status"]=="CROSS_COLUMN_EIGHT_PLACE_FIELD_RETRACTED" and retract["prior_12yf_status"]=="LONG_LANE_DIGIT_DIRECTION_AND_10_MINUS_SHORT_LAW_RETRACTED","corrective precedence")
 need([x["long_decimal"] for x in old["direct_original_readings"]]==retract["prior_12yf_long_decimals"]==["424.8249","429.6073","434.3711","439.1163","443.8429"] and old["source_scoped_replay"]["long_next_minus_long_current"]==retract["prior_12yf_inferred_steps"],"12YF historical evidence changed")
 ar=doc["local_arithmetic"];xs=list(map(Decimal,S));ys=list(map(Decimal,L))
 steps=[ys[i+1]-ys[i] for i in range(6)]
 need(steps==[-xs[i] for i in range(6)] and [str(x) for x in steps]==ar["long_differences"]==ar["short_negations"]==["-5.1990","-5.2176","-5.2362","-5.2548","-5.2734","-5.2920"],"actual long decrement")
 need([str(steps[i]+xs[i]) for i in range(6)]==ar["zero_residuals"]==["0.0000"]*6,"nonzero residual")
 need([str(xs[i+1]-xs[i]) for i in range(6)]==ar["short_first_differences"]==["0.0186"]*6,"short increment")
 need([str(ys[i+2]-2*ys[i+1]+ys[i]) for i in range(5)]==ar["long_second_differences"]==["-0.0186"]*5,"long second difference")
 need(ar["precision"]=="EXACT_DECIMAL_4" and ar["identity"]=="L(d+1)-L(d)=-S(d); D14–D20 ONLY","false general mechanical claim")
 limits=doc["boundaries"]
 need(all(limits[x]=="UNPROVEN" for x in ("heading_old_unit_to_lanes","source_long_law_outside_seven_days","ming_1569_identical_operational_field","copying_or_lineage")),"source scope overclaim")
 need(limits["source_original_formal_main_target_fields"]=="5/6" and limits["cross_witness_final_mechanical_decisions"]=="0/6" and limits["open_research_issues"]==11 and all(limits[x]==0 for x in ("new_genealogy_edges","new_registry_sources","algorithm_reopens")),"false winner or fake original")
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 need(issue["status"]=="OPEN" and PATH in issue["source_refs"] and PATH.replace(".json",".md") in issue["source_refs"],"risk not registered")
 e=issue["g893_12yf_long_direction_errata"];need(len(e)==1 and e[0]["evidence_doc"]==PATH and e[0]["valid_relation"]=="LONG_NEXT_EQUALS_LONG_PREVIOUS_MINUS_SHORT_PREVIOUS" and e[0]["retracted_relation"]=="LONG_INCREASE_EQUALS_10_MINUS_SHORT" and e[0]["final_decisions_added"]==0,"retired historical error not recorded")
 need(any(x.get("event")=="G893_12YF_FALSE_LONG_DIRECTION_RETRACTION_12YG_APPEND" and PATH in x.get("evidence_refs",[]) for x in issue["history"]),"append-only history")
 need(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,state["schema_version"].split(".")))>=(1,620,0) and any(x.startswith("12YG ") for x in state["historical_audit"]["current_focus"]),"continuity version")
 need(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"product reopening")
 return {"status":"PASS","original_printed_days":7,"distinct_source_rois":14,"exact_subtraction_edges":6,"prior_12yf_original_mechanism":"RETRACTED","cross_witness_final":"0/6"}
def replay_archive(path,doc):
 from PIL import Image
 raw=Path(path).read_bytes()
 need(len(raw)==doc["same_copy"]["size"] and hashlib.sha256(raw).hexdigest()==doc["same_copy"]["sha256"],"zip hash")
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  need(z.testzip() is None,"zip CRC")
  report=json.loads(z.read("report.json"));need(report["book_cd"]=="GK00893_00" and len(report["physical_pages"])==204,"report")
  pages={}
  for entry in report["physical_pages"]:
   data=z.read("physical/"+entry["page"]+".jpg")
   need(len(data)==entry["bytes"] and hashlib.sha256(data).hexdigest()==entry["sha256"],"image SHA")
   if entry["page"] in ("001a","002b","003a"):pages[entry["page"]]=data
  need([hashlib.sha256(pages[x["id"]]).hexdigest() for x in doc["pages"]]==PAGES,"source page SHA")
  imgs={name:Image.open(io.BytesIO(data)).convert("RGB") for name,data in pages.items()}
  for rr in doc["rois"]+[doc["heading"]["native_roi"]]:
   need(hashlib.sha256(imgs[rr["page"]].crop(tuple(rr["rect"])).tobytes()).hexdigest()==rr["sha256"],"native pixels SHA")
 return {"status":"PASS","original_jpegs":204,"native_rois":15}
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--archive");args=ap.parse_args()
 d,*other=load();print(json.dumps(verify(d,*other),ensure_ascii=False))
 if args.archive:print(json.dumps(replay_archive(args.archive,d),ensure_ascii=False))
