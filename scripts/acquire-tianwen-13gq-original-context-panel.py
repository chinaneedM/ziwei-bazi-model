#!/usr/bin/env python3
"""13GQ: wider contextual JPEG panels for joint day/field/gutter source inspection.

All crops come from the same exact 13GN PDF and remain candidate visual evidence
until separate human review binds full original headings and numeric rows.
"""
import base64, hashlib, io, json, os
from pathlib import Path
from urllib.parse import urlsplit
import fitz, requests
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=Path("ncl-13gq-original-context")
GN=json.loads((ROOT/"docs/research/TIANWEN-13GN-NCL03130-EMBEDDED-IMAGE-GRADE-ERRATUM-R1.json").read_text(encoding="utf8"))
CASES=[
 ("D9",74,[620,185,810,1080],"DAY9_HEADING_PLUS_PREVIOUSLY_UNADJUDICATED_GUTTER_CANDIDATE"),
 ("D14",74,[60,185,230,1080],"DAY14_HEADING_PLUS_TERMINAL_FOURFEN_CANDIDATE"),
 ("D30",76,[675,180,940,1130],"DAY29_30_31_HEADERS_PLUS_TWO_SEAM_NEIGHBOR_CANDIDATE_STRIPS")
]
def sha(x):return hashlib.sha256(x).hexdigest()
def download():
 b=bytearray()
 with requests.get(GN["source"]["url"],stream=True,allow_redirects=True,timeout=(30,180),headers={"User-Agent":"TianwenHistoricalResearch/1.0"}) as r:
  r.raise_for_status()
  u=urlsplit(r.url)
  assert u.scheme=="https" and u.hostname in ("commons.wikimedia.org","upload.wikimedia.org")
  for c in r.iter_content(1024*1024):
   if c:b.extend(c)
   assert len(b)<=GN["source"]["bytes"]
 assert len(b)==GN["source"]["bytes"] and sha(b)==GN["source"]["sha256"]
 return bytes(b)
def main():
 OUT.mkdir(exist_ok=True)
 src=download()
 result={"schema":"TIANWEN-13GQ-NCL03130-SOURCE-CONTEXT-PANEL-ACQUISITION-R1","pdf_sha256":sha(src),"pdf_bytes":len(src),"no_ocr_or_interpolation":True,"no_new_witness_or_original_glyph_adjudication":True,"panels":[]}
 with fitz.open(stream=src,filetype="pdf") as pdf:
  assert len(pdf)==189
  for target,page,bbox,label in CASES:
   row=next(x for x in GN["pages"] if x["page"]==page)
   obj=pdf.extract_image(row["embedded"]["xref"])["image"]
   assert sha(obj)==row["embedded"]["jpeg_sha256"] and len(obj)==row["embedded"]["jpeg_bytes"]
   im=Image.open(io.BytesIO(obj)).convert("RGB")
   assert list(im.size)==row["embedded"]["size"] and sha(im.tobytes())==row["embedded"]["rgb_sha256"]
   assert 0<=bbox[0]<bbox[2]<=im.width and 0<=bbox[1]<bbox[3]<=im.height
   crop=im.crop(bbox)
   bio=io.BytesIO();crop.save(bio,format="PNG",compress_level=9)
   png=bio.getvalue()
   fn=f"p{page:03d}-{target.lower()}-joint-heading-field-gutter.png"
   (OUT/fn).write_bytes(png)
   e={"target":target,"page":page,"source_xref":row["embedded"]["xref"],"xyxy":bbox,"role":label,"file":fn,"width":crop.width,"height":crop.height,"png_sha256":sha(png),"rgb_sha256":sha(crop.tobytes()),"png_bytes":len(png),"adjudicated_original_literal":None,"source_field_certified":False}
   result["panels"].append(e)
   print("13GQ_CONTEXT_META "+json.dumps(e,ensure_ascii=False),flush=True)
   if os.getenv("TIANWEN_LOG_CONTEXT_B64")=="1":print("13GQ_CONTEXT_B64_"+target+"="+base64.b64encode(png).decode("ascii"),flush=True)
 (OUT/"manifest.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 print("13GQ_PASS_SOURCE_CONTEXT_CROPS_NO_GLYPH_ADJUDICATION",sha(src),len(result["panels"]),flush=True)
if __name__=="__main__":main()
