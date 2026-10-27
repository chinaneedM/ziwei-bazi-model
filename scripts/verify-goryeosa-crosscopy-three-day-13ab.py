#!/usr/bin/env python3
"""13AB direct multi-source original image adjacency collation, no OCR/no votes."""
import argparse,hashlib,json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13AB-WASEDA-NLC-GORYEOSA-WORK52-D15-D17-ORIGINAL-THREE-DAY-COVARIANT-R1.json"
WPDF="28ebfeb34191f45715bc449d27da61fe04fb05eb45e84dd00cf569699f46225f"
NPDF="2b9e51cc5f44a4d92d3cb4a63318605f78cc8ffb118853036655b65ed279a689"
WJPG="388f3d5dd9e9861f8ce90c304b154edaeaee98614bb12cd3468f957dcde6fc66"
NPIX="d99f7233a4203f634b58f25ae7f9d554aeaf363108e48c71a12f32e04d310832"
VALUES=["5.2176","5.1362","5.2548"]
GLYPHS=["五分二一七六","五分一三六二","五分二五四八"]
W_SHA=["065364783404881108618c8569384ea8a371440c712ef94ff6aee70624f87409","4cb2583525a40f59e69f7463853817dacc3bc988118969de0c6d18205d91c5aa","ebbafe25c190c2a97b2ebdd071545fa3bf05ed80e6288ee034be091013f7e963"]
N_SHA=["4c14516dd0fea4cfa54b5f6163263f3975d239ad5042eed8725a832a2f3c115a","90614d73b7112d5e3d41ddab40591a0fe89504fba0d1f47e027ef02252f10fd3","4af1d35f7dbae661381581702113001c9d8ec6554f48616b9c86c9efe375cc3f"]
W_BB=[[1500,300,1680,1540],[1400,300,1540,1540],[1070,300,1200,1540]]
N_BB=[[860,900,1210,3060],[550,900,900,3060],[240,900,590,3060]]
def read(p=E):return json.loads((ROOT/p).read_text(encoding="utf8"))
def check(e):
 assert e["schema"]=="TIANWEN-13AB-WASEDA-NLC-WORK52-THREE-DAY-SHORT-LANE-COATTESTATION-R1" and e["issue"]=="TW-OPEN-0005"
 w,n=e["source_waseda"],e["source_nlc"]
 assert (w["original_pdf_sha256"],w["pdf_page_1_based"],w["embedded_jpeg_xref"],w["jpeg_bytes_sha256"])==(WPDF,23,70,WJPG)
 assert (n["original_pdf_sha256"],n["pdf_page_1_based"],n["embedded_image_xref"],n["decoded_grayscale_pixel_sha256"])==(NPDF,16,111,NPIX)
 assert n["firstparty_nlc_item_crosswalk_verified"] is False and n["physical_impression_verified"] is False
 x=e["collation"]
 assert [r["day"] for r in x]==[15,16,17] and [r["glyph"] for r in x]==GLYPHS and [r["decimal"] for r in x]==VALUES
 assert [r["waseda_roi"] for r in x]==W_BB and [r["nlc_roi"] for r in x]==N_BB
 assert [r["waseda_rgb_sha256"] for r in x]==W_SHA and [r["nlc_rgb_sha256"] for r in x]==N_SHA
 a,b,c=map(Decimal,VALUES);h=e["local_finite_difference"]
 assert b-a==Decimal(h["day15_to16"])==Decimal("-0.0814")
 assert c-b==Decimal(h["day16_to17"])==Decimal("0.1186")
 assert (a+c)/2==Decimal(h["neighbor_midpoint"])==Decimal("5.2362")
 assert (a+c)/2-b==Decimal(h["difference"])==Decimal("0.1000")
 q=e["adjudication"]
 assert q["both_images_share_three_day_lexical_reading"] is True and q["three_day_pattern_alone_proves_shared_printing_plate"] is False
 assert q["copy_independence"]=="UNADJUDICATED" and q["not_a_g893_mechanical_equivalence"] is True and q["waseda_d18_cumulative_original"] is None
 assert all(q[k]==0 for k in ["physical_independent_numeric_votes_added","source_registry_sources_added","transmission_graph_nodes_added","transmission_graph_edges_added","algorithm_reopens"])
 assert q["open_research_issues"]==11 and q["chart_r1"]=="CLOSED"
 prior=read("docs/research/TIANWEN-13Y-WASEDA-GORYEOSA-WORK52-D12-D20-SOLAR-LOCAL-FINITE-DIFFERENCE-R1.json")
 assert [(t["day"],t["original_glyph"]) for t in prior["original_short_day_series"] if t["day"] in (15,16,17)]==list(zip([15,16,17],GLYPHS))
 state=read("docs/PROJECT-CURRENT-STATE-R1.json");ledger=read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 assert tuple(map(int,state["schema_version"].split(".")))>=(1,687,0)
 assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert any(z.startswith("13AB ") for z in state["historical_audit"]["current_focus"])
 assert any(z.get("id")=="OMISSIONS-13AB-NLC-WASEDA-D15-D17-TRIPLE-20261019" for z in ledger["checkpoint_log"])
 assert len(ledger["issues"])>=11
 t=next(y for y in ledger["issues"] if y["id"]=="TW-OPEN-0005")
 assert t["status"]=="OPEN" and E in t["source_refs"]
 return True
def replay_pdfs(e,waseda,nlc):
 import fitz
 from PIL import Image
 from io import BytesIO
 wd=Path(waseda).read_bytes();nd=Path(nlc).read_bytes()
 assert hashlib.sha256(wd).hexdigest()==WPDF and hashlib.sha256(nd).hexdigest()==NPDF
 wdoc=fitz.open(stream=wd,filetype="pdf");ndoc=fitz.open(stream=nd,filetype="pdf")
 try:
  assert len(wdoc)==85 and len(ndoc)==64
  assert 70 in [z[0] for z in wdoc[22].get_images(full=True)] and 111 in [z[0] for z in ndoc[15].get_images(full=True)]
  jpeg=wdoc.extract_image(70)["image"];assert hashlib.sha256(jpeg).hexdigest()==WJPG
  wi=Image.open(BytesIO(jpeg)).convert("RGB")
  pi=fitz.Pixmap(ndoc,111)
  assert (pi.width,pi.height,pi.n)==(4296,3607,1)
  assert hashlib.sha256(pi.samples).hexdigest()==NPIX
  ni=Image.frombytes("L",(pi.width,pi.height),pi.samples).convert("RGB")
  for r in e["collation"]:
   assert hashlib.sha256(wi.crop(tuple(r["waseda_roi"])).tobytes()).hexdigest()==r["waseda_rgb_sha256"]
   assert hashlib.sha256(ni.crop(tuple(r["nlc_roi"])).tobytes()).hexdigest()==r["nlc_rgb_sha256"]
 finally:wdoc.close();ndoc.close()
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--waseda-pdf");p.add_argument("--nlc-pdf");args=p.parse_args()
 e=read();check(e)
 if args.waseda_pdf or args.nlc_pdf:
  assert args.waseda_pdf and args.nlc_pdf
  replay_pdfs(e,args.waseda_pdf,args.nlc_pdf)
 print("TIANWEN_13AB_SOURCE_"+("PIXEL_REPLAY" if args.waseda_pdf else "STATIC")+"_PASS")
