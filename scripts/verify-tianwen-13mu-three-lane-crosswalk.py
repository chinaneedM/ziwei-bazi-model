#!/usr/bin/env python3
"""13MU: fail-closed original Zhou printed D15-D16 three-lane correction."""
import argparse,hashlib,json
from pathlib import Path
from decimal import Decimal
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13MU-ZHOU1569-G893-D15-D16-THREE-LANE-CROSSWALK-R1.json"
S=R/"docs/PROJECT-CURRENT-STATE-R1.json"
L=R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
Q=R/"docs/research/TIANWEN-13MQ-G893-ZHOU1569-D15-SECOND-LANE-ORIGINAL-PRINT-SCOPE-R1.json"
def sha(x):return hashlib.sha256(x).hexdigest()
def check(e,s,l,q):
 assert e["schema"]=="TIANWEN-13MU-ZHOU1569-G893-D15-D16-THREE-LANE-CROSSWALK-R1"
 o=e["originals"];z=o["zhou"];g=o["g893"]
 assert z["sha256"]==q["provenance"]["zhou1569_pdf_sha256"]
 assert z["bytes"]==4936040 and z["pages"]==45 and z["pymupdf"]=="1.26.7"
 assert g["sha256"]==q["provenance"]["g893_original_jpg_sha256"]
 assert o["ocr_used"] is False and o["new_source_objects"]==o["new_physical_originals"]==0
 assert [(r["key"],r["page"],r["box"]) for r in e["native_rgb_rois"]]==[
 ("ZHOU_PAGE14_TABLE_FIELDS",14,[680,75,1085,1410]),
 ("ZHOU_PAGE14_HEADER_LABELS",14,[740,65,1065,1140]),
 ("ZHOU_PAGE15_D15_D16",15,[1215,90,1380,1420]),
 ("ZHOU_PAGE15_D15_MID_LOWER",15,[1290,500,1375,1410]),
 ("ZHOU_PAGE15_D16_MID_LOWER",15,[1210,500,1295,1410])]
 assert all(len(r["rgb_sha256"])==64 for r in e["native_rgb_rois"])
 assert e["visible_original_context"]["zhou_page14_table_title"]=="太陽冬至前後立成卷第二"
 assert e["visible_original_context"]["zhou_page15_day_headers"]==["十五日","十六日"]
 assert e["visible_original_context"]["normalized_from_context_not_all_glyphs_printed_each_day"] is True
 r=e["rows"];assert [x["day"] for x in r]==[15,16]
 assert [x["zhou_short"] for x in r]==["5.2176","5.2362"]
 assert [x["zhou_middle_normalized"] for x in r]==["434.8249","429.6073"]
 assert [x["zhou_lower_normalized"] for x in r]==["7135.8375","7570.6624"]
 assert [x["g893_decreasing"] for x in r]==["434.8249","429.6073"]
 a=e["arithmetical_source_local"]
 assert Decimal(r[1]["zhou_lower_normalized"])-Decimal(r[0]["zhou_lower_normalized"])==Decimal(a["zhou_c16_minus_c15"])==Decimal(r[0]["zhou_middle_normalized"])
 assert Decimal(r[0]["zhou_middle_normalized"])-Decimal(r[0]["zhou_short"])==Decimal(a["zhou_middle_d15_minus_short_d15"])==Decimal(r[1]["zhou_middle_normalized"])
 assert a["zhou_cumulative_delta_matches_zhou_middle_d15"] is True
 assert a["four_decimal_context_only_not_historical_unit_proof"] is True
 f=e["forward_only_adjudication"]
 assert f["previous_13mq_nonidentical_print_strings_still_true"] is True
 assert f["wrong_comparator_for_same_field_historical_disagreement"] is True
 assert f["corrected_zhou_to_g893_numeric_lane"]=="ZHOU_D15_MIDDLE_434.8249_EQUALS_G893_D15_DECREASING_434.8249_NUMBER_LEVEL_ONLY"
 assert f["full_original_field_unit_radix_epoch_bridge"]==f["independent_lineage"]=="UNPROVEN"
 assert f["G893_six_final_historical_winners"]==f["algorithm_reopen"]==0
 assert f["original_text_correction_asserted"] is False
 assert e["guard"]["registered_sources"]==s["historical_audit"]["external_source_registry_total_unique_count"]==765
 assert e["guard"]["product"]==s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,983,0)
 focus=s["historical_audit"]["current_focus"]
 assert len(focus)==l["binding"]["source_focus_count"] and any(x.startswith("13MU ") for x in focus)
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert "docs/research/TIANWEN-13MU-ZHOU1569-G893-D15-D16-THREE-LANE-CROSSWALK-R1.json" in issue["source_refs"] and "docs/research/TIANWEN-13MU-ZHOU1569-G893-D15-D16-THREE-LANE-CROSSWALK-R1.md" in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13MU-THREE-LANE-BRIDGE-20261031" for x in issue["history"])
 assert any(x["id"]=="OMISSIONS-13MU-THREE-LANE-BRIDGE-20261031" for x in l["checkpoint_log"])
 return {"status":"PASS","source_original_pixel_replay":"NOT_EXECUTED_WITHOUT_PDF","local_arithmetic_edges":2,"final_cross_original_winners":0}
def pixel_replay(e,source_pdf):
 from PIL import Image
 import fitz
 assert fitz.VersionBind=="1.26.7","version-pinned PyMuPDF required"
 assert Image.__version__=="11.3.0","version-pinned Pillow required"
 raw=Path(source_pdf).read_bytes()
 assert sha(raw)==e["originals"]["zhou"]["sha256"]
 d=fitz.open(stream=raw,filetype="pdf")
 assert len(d)==45
 pages={}
 for n in [14,15]:
  pix=d[n-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),colorspace=fitz.csRGB,alpha=False)
  pages[n]=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
  assert pages[n].size==(2105,1489)
 for r in e["native_rgb_rois"]:
  img=pages[r["page"]];assert sha(img.crop(tuple(r["box"])).tobytes())==r["rgb_sha256"],r["key"]
 return {"source_original_pixel_replay":"PASS","rgb_roi_hashes_verified":5}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--source-pdf",type=Path)
 arg=p.parse_args()
 e,s,l,q=(json.loads(x.read_text(encoding="utf8")) for x in (E,S,L,Q))
 out=check(e,s,l,q)
 if arg.source_pdf:out.update(pixel_replay(e,arg.source_pdf))
 print(json.dumps(out,ensure_ascii=False))
