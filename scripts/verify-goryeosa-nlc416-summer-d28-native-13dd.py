#!/usr/bin/env python3
"""13DD: 1909 later print directly attests summer day28 0.994549, no inherited-error verdict."""
import argparse,hashlib,io,json,struct
from decimal import Decimal,ROUND_HALF_UP
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13DD-NLC416-1909-SUMMER-D28-NATIVE-ORIGINAL-GLYPH-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
PNG="docs/research/images/TIANWEN-13DD-NLC416-1909-SUMMER-D28-XINGDU-NATIVE.png"
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13DD-NLC416-1909-SUMMER-D28-DIRECT-ORIGINAL-GLYPH-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 a=e["acquisition"]
 assert (a["workflow_run"],a["artifact_id"],a["source_bytes"],a["pdf_page_count"])==(39871724324,12467041226,38410680,755)
 assert a["source_sha256"]=="b4bd5c557c7ba44bac1fc881e6c2e8784c9d56a8d2629f17b5255a1ec6bd9e97"
 assert a["ocr_used"] is False and a["publication_year"]==1909
 p=e["page_binding"]
 assert (p["table_heading_pdf_page"],p["day27_to_29_pdf_page"],p["embedded_image_count"])==(150,152,1)
 assert p["table_heading_literal"]=="大陽夏至前後二象縮初盈末限"
 assert p["image_dimensions"]==[1486,2162] and p["page152_upper_panel_days"]==list(range(23,29))
 assert p["source_page_152_native_rgb_sha256"]=="ca1bea6a3f334df93774b98726275f4e4bbe4911c4679fb6d1579dd722325b1c"
 assert p["table_heading_native_rgb_sha256"]=="2739bea6a9436cc97fd0c8f379eb79e869bd6217e814dd0729101768a96566c8"
 expected=[
 ("TABLE_HEADING",150,[1190,205,1390,520],"375407dfd9adc773f87cc28ade5451a26dfe5c6cf7d6e085ad1b7e408b7a7345","大陽夏至前後二象縮初盈末限"),
 ("D28_DAY",152,[341,211,391,378],"1428fcb78a76d84895045e82c1b0bb688e6a47ac4d22ffab6a3c9441147941f4","二十八日"),
 ("D28_SHORT",152,[350,424,396,660],"906063447a049edb3a070eaf9bb86c81eff62efca1b1975175cc1f22ddb0b4d7","四分八八九八"),
 ("D28_LONG",152,[306,424,353,690],"6a3e2211a47272b429658b81004cdb70b292c90dfa547a06aa08484ed12b7773","三百五十四五一〇一"),
 ("D28_CUMULATIVE",152,[253,424,307,790],"1592f56405287ac486b99a1197815e3793f43beee1749055a259b68937a2790d","一萬一千八百四五七六九六"),
 ("D28_XINGDU",152,[207,424,254,735],"cbcc4ee97586d772e1366b5b1b89037e6320e9117745cb357ae1a1398fa4687d","初度九十九四五四九"),
 ("D27_XINGDU",152,[386,424,438,735],"ef1b61274e9b3704b4ca57d110d94827e75d7f51030bd0dea10920956119a48f","初度九十六四〇六二"),
 ("D29_XINGDU",152,[1090,1320,1150,1710],"dec6f8fa30233e0ebb1381f71d1c41e8b0727ef26e5d0f492ca7f459066012f3","初度九十六五〇三八")]
 got=[(x["field"],x["pdf_page"],x["bbox"],x["rgb_sha256"],x["literal"]) for x in e["source_native_rois"]]
 assert got==expected
 for x in e["source_native_rois"]:
  x0,y0,x1,y1=x["bbox"]
  assert 0<=x0<x1<=1486 and 0<=y0<y1<=2162
 crop=e["binary_crop"];assert crop["file"]==PNG and crop["source_roi_field"]=="D28_XINGDU"
 assert crop["pixel_dimensions"]==[47,311] and crop["png_bytes"]==1514
 assert crop["sha256_png"]=="77122fc537e697e1fc95cae416723c2b809068865c5b3246af5733eecd30bd48"
 raw=(ROOT/PNG).read_bytes()
 assert len(raw)==1514 and hashlib.sha256(raw).hexdigest()==crop["sha256_png"]
 assert raw[:8]==b"\x89PNG\r\n\x1a\n"
 assert struct.unpack(">II",raw[16:24])==(47,311)
 assert crop["git_blob_sha"]=="24ae98ba091a40b2501c004fc7a08c3259d275e0"
 vals={x["field"]:Decimal(x["value"]) for x in e["source_native_rois"] if x.get("value")}
 z=e["independent_decimal_replay"]
 assert vals["D28_SHORT"]==Decimal("4.8898")
 assert vals["D28_LONG"]==Decimal(z["source_printed_day28_long"])==Decimal("354.5101")
 assert vals["D28_CUMULATIVE"]==Decimal("11845.7696")
 assert vals["D28_XINGDU"]==Decimal(z["source_printed_day28_xingdu"])==Decimal("0.994549")
 assert vals["D27_XINGDU"]==Decimal(z["source_printed_day27_xingdu"])==Decimal("0.964062")
 assert vals["D29_XINGDU"]==Decimal(z["source_printed_day29_xingdu"])==Decimal("0.965038")
 f=lambda v:(Decimal("1")-Decimal(v)/Decimal("10000")).quantize(Decimal("0.000001"),rounding=ROUND_HALF_UP)
 assert f(z["source_printed_day27_long"])==Decimal(z["day27_candidate"])==vals["D27_XINGDU"]
 assert f(z["source_printed_day28_long"])==Decimal(z["day28_candidate_only"])==Decimal("0.964549")
 assert f(z["source_printed_day29_long"])==Decimal(z["day29_candidate"])==vals["D29_XINGDU"]
 assert vals["D28_XINGDU"]-Decimal(z["day28_candidate_only"])==Decimal(z["day28_printed_minus_candidate"])==Decimal("0.030000")
 assert z["candidate_graphic_literal_unprinted"]=="初度九十六四五四九"
 assert z["printed_1909_glyph_is_source_positive"] and not z["source_1909_printing_error_uniquely_proven"]
 assert not z["ultimate_source_emendation_authorized"] and not z["global_historical_mechanical_rule_proven"]
 adj=e["adjudication"]
 assert adj["now"]=="1909_LATER_PRINT_DIRECT_XINGDU_D28_GLYPH_ATTESTED_ARITHMETIC_MISMATCH_OPEN"
 assert adj["original_1909_XINGDU_D28"]=="初度九十九四五四九"
 assert adj["earlier_edition_XINGDU_D28"]=="UNCOLLATED"
 assert adj["winter_D16_difference_5_1362_vs_5_2362"]=="SEPARATELY_OPEN"
 assert all(adj[k]==0 for k in ["new_independent_early_historical_witnesses","new_source_registry_entries","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","algorithm_reopens"])
 imp=e["impact"]
 assert (imp["matrix_rows"],imp["matrix_audited"],imp["registered_sources"],imp["genealogy_nodes"],imp["genealogy_edges"],imp["unresolved_risks"])==(222,222,754,252,238,11)
 assert imp["deterministic_chart"]=="CLOSED" and imp["algorithm_reopens"]==0
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]=="1.765.0"
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]=="13DD"
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"]
 assert any(h.get("revision_id")=="TW-OPEN-0005-13DD-SUMMER-D28-ORIGINAL-POSITIVE" for h in issue["history"])
 assert any(h.get("id")=="OMISSIONS-13DD-NLC416-SUMMER-D28-20261023" for h in l["checkpoint_log"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 assert sum(x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS") for x in l["issues"])==11
 return True
def replay_source_original(e,p):
 import fitz
 from PIL import Image
 raw=Path(p).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==e["acquisition"]["source_sha256"]
 d=fitz.open(stream=raw,filetype="pdf")
 assert len(d)==755
 sources={}
 for num in (150,152):
  images=d[num-1].get_images(full=True)
  assert len(images)==1
  im=Image.open(io.BytesIO(d.extract_image(images[0][0])["image"])).convert("RGB")
  assert im.size==(1486,2162)
  expect=e["page_binding"]["table_heading_native_rgb_sha256"] if num==150 else e["page_binding"]["source_page_152_native_rgb_sha256"]
  assert hashlib.sha256(im.tobytes()).hexdigest()==expect
  sources[num]=im
 for item in e["source_native_rois"]:
  cut=sources[item["pdf_page"]].crop(tuple(item["bbox"]))
  assert hashlib.sha256(cut.tobytes()).hexdigest()==item["rgb_sha256"]
 return True
if __name__=="__main__":
 parser=argparse.ArgumentParser()
 parser.add_argument("--original-pdf")
 args=parser.parse_args()
 e=load(E)
 assert check(e,load(S),load(L))
 if args.original_pdf:assert replay_source_original(e,args.original_pdf)
 print("TIANWEN_13DD_NLC416_1909_SUMMER_D28_NATIVE_GLYPH=PASS")
