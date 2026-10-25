#!/usr/bin/env python3
"""13GR same-source positive-control capture: days 12/13/14 on original PDF p74.

Capture source-native fields, headings and one adjacent alternative lane.
A print-field attribution requires independent direct visual review; arithmetic
recurrence and source-seam proximity are not sufficient.
"""
import base64,hashlib,io,json,os,importlib.util
from pathlib import Path
import fitz
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=Path("ncl13gr-original-d12-d14-lanes")
SOURCE=ROOT/"docs/research/TIANWEN-13GN-NCL03130-EMBEDDED-IMAGE-GRADE-ERRATUM-R1.json"
GD=ROOT/"docs/research/TIANWEN-13GD-NLC-P74-P75-D10-D15-BOUNDED-ORIGINAL-LANES-R1.json"
SPEC=importlib.util.spec_from_file_location("original_probe",ROOT/"scripts/acquire-tianwen-13gp-original-embedded-probe.py")
PROBE=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(PROBE)
def sha(b):return hashlib.sha256(b).hexdigest()
def capture(im,box,name,role,source,report):
 assert 0<=box[0]<box[2]<=im.width and 0<=box[1]<box[3]<=im.height
 crop=im.crop(box);o=io.BytesIO();crop.save(o,format="PNG",compress_level=9);png=o.getvalue()
 (OUT/name).write_bytes(png)
 v={"name":name,"role":role,"source_box_xyxy":box,"size":list(crop.size),"sha256_png":sha(png),"sha256_rgb":sha(crop.tobytes()),"bytes_png":len(png),"certified_historical_original_literal":None}
 report["panels"].append(v)
 print("13GR_PANEL "+json.dumps(v,ensure_ascii=False),flush=True)
 if os.environ.get("TIANWEN_LOG_LANES_BASE64")=="1":print("13GR_PNG_B64_"+name.replace(".png","").replace("-","_")+"="+base64.b64encode(png).decode("ascii"),flush=True)
def main():
 OUT.mkdir(exist_ok=True)
 e=json.loads(SOURCE.read_text(encoding="utf8"));d=json.loads(GD.read_text(encoding="utf8"))
 b=PROBE.get_bytes(e["source"]["url"],e["source"]["bytes"],e["source"]["sha256"])
 report={"schema":"TIANWEN-13GR-NLC-P74-D12-D14-ORIGINAL-LANES-PROBE-R1","pdf_sha256":sha(b),"grade":"SOURCE_NATIVE_SOURCE_FIELD_CONTROL_CAPTURE_UNADJUDICATED_D14","source_provenance":"SAME_NLC03130_09_P74_DIGITAL_SURROGATE","positive_controls":{"D12":d["positive_source_rows"][2]["remainder"],"D13":d["positive_source_rows"][3]["remainder"]},"target_D14_complete_original":None,"panels":[]}
 with fitz.open(stream=b,filetype="pdf") as pdf:
  assert len(pdf)==189;page=pdf[73];sealed=e["pages"][0]
  assert sealed["page"]==74
  xref=sealed["embedded"]["xref"];found=page.get_image_rects(xref,transform=True)
  assert len(found)==1
  orig=pdf.extract_image(xref)["image"]
  assert sha(orig)==sealed["embedded"]["jpeg_sha256"] and len(orig)==sealed["embedded"]["jpeg_bytes"]
  im=Image.open(io.BytesIO(orig)).convert("RGB")
  assert list(im.size)==sealed["embedded"]["size"] and sha(im.tobytes())==sealed["embedded"]["rgb_sha256"]
  rendered=page.get_pixmap(matrix=fitz.Matrix(3.1,3.1),alpha=False)
  assert sha(rendered.samples)==sealed["previous_render"]["rgb_sha256"]
  matrix=found[0][1]
  for day in (12,13,14):
   if day==14:
    v=next(x for x in d["non_adjudicated_original_scopes"] if x["day"]==day)
    raw=v["candidate_roi_xyxy"];h=v["source_heading_roi_xyxy"]
   else:
    v=next(x for x in d["positive_source_rows"] if x["day"]==day)
    raw=v["roi_xyxy"];h=v["heading_roi_xyxy"]
   nbox,_=PROBE.map_old_bbox_to_embedded(raw,page,matrix,im.size)
   hbox,_=PROBE.map_old_bbox_to_embedded(h,page,matrix,im.size)
   # Two independent source-native segments: actual day heading and numeric candidate;
   # their exact original pixels are preserved without image scaling/photographic enhancement.
   capture(im,nbox,f"p074-d{day}-numerical-source-lane.png",f"DAY_{day}_NUMERIC_LANE",e,report)
   capture(im,hbox,f"p074-d{day}-printed-heading.png",f"DAY_{day}_HEADING",e,report)
  # Larger frame includes the complete date12-date13-date14 heading and table contexts.
  capture(im,[70,185,420,1080],"p074-d12-d14-three-day-context.png","THREE_DAYS_ONE_PHYSICAL_SCAN",e,report)
  # Explicit alternative same-height print lane next to the day14 narrow-field candidate.
  capture(im,[180,545,230,1060],"p074-d14-adjacent-alternative-lane.png","ALTERNATIVE_PRINTED_LANE_NOT_CERTIFIED_FOURFEN",e,report)
 (OUT/"manifest.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 print("13GR_PASS_DIGIT_FREE_NATIVE_SOURCE_CONTROLS",len(report["panels"]),report["pdf_sha256"],flush=True)
if __name__=="__main__":main()
