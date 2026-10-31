#!/usr/bin/env python3
"""13MQ D15 nonidentical original strings; optional SHA-bound archived pixel replay."""
from pathlib import Path
from io import BytesIO
import hashlib,json,zipfile,argparse,re
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13MQ-G893-ZHOU1569-D15-SECOND-LANE-ORIGINAL-PRINT-SCOPE-R1.json"
S=R/"docs/PROJECT-CURRENT-STATE-R1.json"
L=R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
Y=R/"docs/research/TIANWEN-12YG-G893-SEVEN-DAY-SOLAR-DECREASING-LANE-SECOND-ERRATUM-R1.json"
M=R/"docs/research/TIANWEN-13MO-G893-ZHOU1569-PAIRED-LANE-SOURCE-COMPARISON-R1.json"
def sha(raw):return hashlib.sha256(raw).hexdigest()
def check(e,s,l,y,m):
 assert e["schema"]=="TIANWEN-13MQ-G893-ZHOU1569-D15-SECOND-LANE-ORIGINAL-PRINT-SCOPE-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 p=e["provenance"];r=e["reading_adjudication"];rois=e["original_roi_controls"]
 assert p["archive_run_id"]==41144025711 and p["artifact_id"]==13019278183
 assert p["zip_sha256"]==m["archive"]["zip_sha256"]=="1d8f10da7c27411bf38ad635494a1b9f4e700fb76cb37b2a7541c075a0ca9835"
 assert p["g893_original_jpg_sha256"]==m["g893"]["jpeg_sha256"]=="f9812e8c6a357eb6cd1117bb2af58d816e01030d5b93f34e7094bddb766b2b55"
 assert p["zhou1569_pdf_sha256"]==m["zhou1569"]["pdf_sha256"]=="4c006b7ce131902fe33012d42f62cd2bbc2140affa3d5886e0da02966352cb7c"
 assert p["new_digital_source_objects"]==p["new_physical_copies"]==0 and p["ocr_used"] is False
 assert p["zhou1569_pdf_page_1based"]==15
 assert len(rois)==3
 assert [(x["source"],x["role"],x["box"],x["rgb_sha256"]) for x in rois]==[
 ("G893_GK00893_00","D15_PRINTED_LONG_LANE",[824,640,868,1435],"776e4a255da4787856b45298b2a3924d2d979e83b42e05b426f34151fd84c824"),
 ("ZHOU_XIANG_1569","D15_PRINTED_OTHER_NUMERIC_LANE",[1295,70,1353,1370],"188a2d98f567bf4c5c90cbd9dcb3bb4c0cbb86b097ec3f07196bf168413b0c94"),
 ("ZHOU_XIANG_1569","D15_DATE_AND_TWO_LANE_CONTEXT",[1240,50,1370,1390],"482656d6462165504d2b9c72b2b8d1b2e7057339bbd733300add22e4c4bca3c0")]
 assert r["compared_day"]==15 and r["g893_other_column_print"]=="四百三十四分八二四九"
 assert r["zhou_other_column_print"]=="七千一百三十五分八三七五"
 assert rois[1]["source_original_reading_prefix"]=="七千一百"
 assert rois[0]["source_original_reading"]==y["readings"][1]["long_glyph"]
 assert rois[0]["normalized_hypothesis"]==y["readings"][1]["long_decimal"]
 assert r["cross_source_D15_second_column_printed_strings_equal"] is False
 assert r["cross_source_D15_short_string_agreement"]==m["paired_column_transcriptions"][0]["short"]=="5.2176"
 assert r["cross_source_D16_D17_short_string_agreement"]==["5.2362","5.2548"]
 assert r["numerically_normalized_zhou_second_column_value"] is None
 assert r["source_header_label_and_column_unit_crosswalk"]=="OPEN"
 assert r["mechanical_same_field_or_equivalent_epoch"]=="NOT_PROVEN"
 assert r["direct_textual_copying"]=="NOT_PROVEN"
 assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
 assert s["schema_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]==l["binding"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,979,0)
 focus=s["historical_audit"]["current_focus"]
 assert any(x.startswith("13MQ ") for x in focus)
 assert l["binding"]["latest_research_focus_prefix"]==focus[-1].split(" ",1)[0]
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert str(E.relative_to(R)) in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13MQ-D15-SECOND-LANE-20261031" for x in issue["history"])
 assert any(x.get("id")=="OMISSIONS-13MQ-D15-SECOND-LANE-20261031" for x in l["checkpoint_log"])
 g=e["scope_guard"]
 assert g["G893_six_cross_original_historical_winners"]==g["algorithm_reopens"]==g["graph_edge_additions"]==0
 assert g["deterministic_product"]==s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 return {"status":"PASS","original_pixel_replay":"NOT_EXECUTED_WITHOUT_ARCHIVE","historical_six_winners":0}
def replay(e,filename):
 from PIL import Image
 import fitz
 assert fitz.VersionBind=="1.26.7","13MQ original crop SHA is a PyMuPDF 1.26.7 profile; fail-closed on renderer mismatch"
 raw=Path(filename).read_bytes()
 assert sha(raw)==e["provenance"]["zip_sha256"]
 with zipfile.ZipFile(BytesIO(raw)) as z:
  assert z.testzip() is None
  jpg=z.read("G893-002b.jpg");pdf=z.read("zhouxiang-1569-vol6-original.pdf")
 assert sha(jpg)==e["provenance"]["g893_original_jpg_sha256"]
 assert sha(pdf)==e["provenance"]["zhou1569_pdf_sha256"]
 im=Image.open(BytesIO(jpg)).convert("RGB")
 assert im.size==(1150,2000)
 d=fitz.open(stream=pdf,filetype="pdf")
 assert len(d)==45
 pix=d[14].get_pixmap(matrix=fitz.Matrix(2.5,2.5),colorspace=fitz.csRGB,alpha=False)
 zi=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
 assert zi.size==(2105,1489)
 for roi in e["original_roi_controls"]:
  source=im if roi["source"]=="G893_GK00893_00" else zi
  x0,y0,x1,y1=roi["box"]
  assert x0>=0 and y0>=0 and x1<=source.width and y1<=source.height
  assert sha(source.crop((x0,y0,x1,y1)).tobytes())==roi["rgb_sha256"]
 return {"status":"PASS","original_pixel_replay":"PASS","source_roi_hashes":3,"new_physical_witnesses":0}
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--source-archive",type=Path)
 args=ap.parse_args()
 e,s,l,y,m=(json.loads(p.read_text(encoding="utf-8")) for p in (E,S,L,Y,M))
 out=check(e,s,l,y,m)
 if args.source_archive:out=replay(e,args.source_archive)
 print(json.dumps(out,ensure_ascii=False))
