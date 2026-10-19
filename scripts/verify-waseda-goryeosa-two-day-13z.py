#!/usr/bin/env python3
"""13Z two-day lexical Decimal replay of one hash-bound Waseda original PDF page."""
import argparse,hashlib,json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13Z-WASEDA-GORYEOSA-WORK52-TWODAY-ORIGINAL-SOLAR-REPLAY-R1.json"
PDF_SHA="28ebfeb34191f45715bc449d27da61fe04fb05eb45e84dd00cf569699f46225f"
JPEG_SHA="388f3d5dd9e9861f8ce90c304b154edaeaee98614bb12cd3468f957dcde6fc66"
LONG=["429.6073","419.1163","408.5509"]
SHORT=["5.1362","5.2548","5.2734","5.2920"]
ROI=["2e224a911046e4d7b6f5c2171ddba365a4f10e9fbc852339a8b45d743a712c53","02199532646f74b2e175f0f568ad905e5042ba57d4167543adee440aa14cfeb8","308aa07ea0f297e267c79ea950e57f2e1799ebd66a18d85e6e94f946a7fcc2bc"]
def read(p=E): return json.loads((ROOT/p).read_text(encoding="utf8"))
def check(e):
 assert e["schema"]=="TIANWEN-13Z-WASEDA-WORK52-TWO-DAY-SOLAR-SOURCE-LOCAL-REPLAY-R1"
 a=e["original"]
 assert (a["shelfmark"],a["digital_book_group"],a["pdf_sha256"],a["pdf_page_count"],a["pdf_page_1based"],a["embedded_jpeg_xref"],a["embedded_jpeg_sha256"])==("リ06 02809",33,PDF_SHA,85,23,70,JPEG_SHA)
 assert a["source_native_dimensions"]==[2592,1728] and a["physical_impression_date"] is None
 assert [x["day"] for x in e["long_original"]]==[16,18,20]
 assert [x["lexical_decimal"] for x in e["long_original"]]==LONG
 assert [x["original_glyph"] for x in e["long_original"]]==["四百二十九六〇七三","四百一十九一一六三","四百〇八五五〇九"]
 assert [x["roi_rgb_sha256"] for x in e["long_original"]]==ROI
 assert [x["roi_xyxy"] for x in e["long_original"]]==[[1400,320,1600,1500],[800,320,975,1500],[405,320,600,1500]]
 assert [x["day"] for x in e["short_original"]]==[16,17,18,19]
 assert [x["lexical_decimal"] for x in e["short_original"]]==SHORT
 assert [x["original_glyph"] for x in e["short_original"]]==["五分一三六二","五分二五四八","五分二七三四","五分二九二〇"]
 l=list(map(Decimal,LONG));s=list(map(Decimal,SHORT))
 exp=[(l[0]-l[1],s[0]+s[1],Decimal("0.1000")),(l[1]-l[2],s[2]+s[3],Decimal("0.0000"))]
 for ix,(replay,(drop,total,residual)) in enumerate(zip(e["two_day_replays"],exp)):
  assert replay["start_day"]==[16,18][ix] and replay["end_day"]==[18,20][ix]
  assert Decimal(replay["long_decrement"])==drop and Decimal(replay["two_short_sum"])==total
  assert Decimal(replay["decrement_minus_short_sum"])==drop-total==residual
 assert e["conclusions"]["waseda_d18_yingsuoji_cumulative_original_folio"] is None
 assert e["conclusions"]["d16_printed_short_glyph_preserved"] is True
 assert e["conclusions"]["source_original_numeric_glyph_transcription_error_assigned"] is False
 for field in ("final_independent_physical_numeric_votes_added","external_source_registry_entries_added","transmission_graph_edges_added","algorithm_reopens"):assert e["conclusions"][field]==0
 assert e["conclusions"]["remaining_open_omissions"]==11 and e["conclusions"]["chart_product_r1"]=="CLOSED"
 old=read(e["preceding_source"])
 assert old["original_short_day_series"][4]["original_glyph"]=="五分一三六二"
 st=read("docs/PROJECT-CURRENT-STATE-R1.json");le=read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 assert st["schema_version"]==le["binding"]["reviewed_state_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,st["schema_version"].split(".")))>=(1,685,0)
 assert any(x.startswith("13Z ") for x in st["historical_audit"]["current_focus"])
 assert any(x.get("id")=="OMISSIONS-13Z-WASEDA-TWO-DAY-ORIGINAL-LONG-SHORT-20261019" for x in le["checkpoint_log"])
 assert le["binding"]["latest_research_focus_prefix"]==st["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert le["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"])
 issue=next(x for x in le["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"]
 assert len(le["issues"])>=11 and le["checkpoint_log"][-1]["state_version"]==st["schema_version"]
 return True
def replay_pdf(source,e):
 import fitz
 from PIL import Image
 from io import BytesIO
 raw=Path(source).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==PDF_SHA
 d=fitz.open(stream=raw,filetype="pdf")
 try:
  assert len(d)==85 and any(z[0]==70 for z in d[22].get_images(full=True))
  rec=d.extract_image(70)
  assert rec["ext"]=="jpeg" and hashlib.sha256(rec["image"]).hexdigest()==JPEG_SHA
  rgb=Image.open(BytesIO(rec["image"])).convert("RGB")
  assert list(rgb.size)==[2592,1728]
  for r in e["long_original"]:
   assert hashlib.sha256(rgb.crop(tuple(r["roi_xyxy"])).tobytes()).hexdigest()==r["roi_rgb_sha256"]
 finally:d.close()
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--source-pdf");a=p.parse_args();e=read();check(e)
 if a.source_pdf:replay_pdf(a.source_pdf,e)
 print("TIANWEN_13Z_PASS_"+("ORIGINAL_SOURCE_PIXELS" if a.source_pdf else "STATIC_ARITHMETIC"))
