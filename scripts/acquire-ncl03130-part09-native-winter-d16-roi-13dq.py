#!/usr/bin/env python3
"""13DQ: original earlier-book numeric table and possible winter source-original glyph review; SHA-bound, no OCR.

A photographed cover ordinal != textual juan identifier. The source is a
Wikimedia mirror, not a verified Taiwan NCL first-party item binding.
"""
import base64,hashlib,io,json
from pathlib import Path
from urllib.parse import urlsplit
import fitz,requests
from PIL import Image
SOURCE="https://commons.wikimedia.org/wiki/Special:Redirect/file/NCL-03130_09_%E9%AB%98%E9%BA%97%E5%8F%B2.pdf"
PDF_SHA="3c2a5621fb3f4eabc593020bcde12a38f6ecdae2842940dec12d5a3a56afd32e"
PDF_SIZE=50735589
PAGES=(65,66)
OUT=Path("ncl03130-13dq-source-native-winter-d16-roi")
def hash_bytes(v):return hashlib.sha256(v).hexdigest()
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 m={"schema":"TIANWEN-13DQ-NCL03130-PART09-WINTER-D16-SOURCE-NATIVE-ROI-R1",
    "source":SOURCE,"source_sha256":PDF_SHA,"source_class":"COMMONS_MIRROR_NOT_FIRSTPARTY_NCL",
    "item_identity":"UNBOUND","textual_juan52":"UNRESOLVED","winter_d16_exact_source_page":"REQUIRES_GLYPH_REVIEW",
    "pages":[],"rois":[],"no_ocr":True,"status":"STARTED"}
 try:
  chunks=[];n=0;h=hashlib.sha256()
  with requests.get(SOURCE,stream=True,allow_redirects=True,timeout=(30,180),
       headers={"User-Agent":"TianwenHistoricalResearch/1.0"}) as resp:
   resp.raise_for_status()
   p=urlsplit(resp.url)
   if p.scheme!="https" or p.hostname not in ("commons.wikimedia.org","upload.wikimedia.org"):
    raise RuntimeError("unsafe download redirect")
   for chunk in resp.iter_content(1024*1024):
    if not chunk:continue
    n+=len(chunk)
    if n>60000000:raise RuntimeError("source cap")
    h.update(chunk);chunks.append(chunk)
  raw=b"".join(chunks)
  if n!=PDF_SIZE or h.hexdigest()!=PDF_SHA or not raw.startswith(b"%PDF-"):
   raise RuntimeError("source digest or size drift")
  d=fitz.open(stream=raw,filetype="pdf")
  if d.is_encrypted or len(d)!=189:raise RuntimeError("source page-count boundary")
  for i in PAGES:
   pix=d[i-1].get_pixmap(matrix=fitz.Matrix(2.6,2.6),alpha=False)
   png=pix.tobytes("png")
   (OUT/f"native-p{i:03d}.png").write_bytes(png)
   original=Image.open(io.BytesIO(png)).convert("RGB")
   ratio=(.53,.14,.98,.91) if i==65 else (.03,.13,.48,.92)
   bounds=tuple(int(v*(original.width if j%2==0 else original.height)) for j,v in enumerate(ratio))
   roi=original.crop(bounds)
   cropped_png=io.BytesIO()
   roi.save(cropped_png,format="PNG")
   cropped_png=cropped_png.getvalue()
   roi_name=f"original-p{i:03d}-context-ROI.png"
   (OUT/roi_name).write_bytes(cropped_png)
   crop_j=io.BytesIO()
   roi.save(crop_j,format="JPEG",quality=93,optimize=True)
   crop_j=crop_j.getvalue()
   (OUT/f"original-p{i:03d}-context-ROI.jpg").write_bytes(crop_j)
   m["rois"].append({"pdf_page":i,"source_original_rgb_sha256":hash_bytes(original.tobytes()),
      "bbox_native":list(bounds),"roi_rgb_sha256":hash_bytes(roi.tobytes()),
      "roi_png_sha256":hash_bytes(cropped_png),"roi_file":roi_name,
      "role":"SOLAR_WINTER_HEADER_CONTEXT" if i==65 else "D15_D16_D17_SOURCE_LANES_UNINTERPRETED"})
   print("13DQ_ROI_BEGIN",i,len(crop_j),flush=True)
   print(base64.b64encode(crop_j).decode(),flush=True)
   print("13DQ_ROI_END",i,flush=True)
   im=original.copy()
   im.thumbnail((2100,1600))
   j=io.BytesIO();im.save(j,format="JPEG",quality=88,optimize=True)
   jpg=j.getvalue()
   (OUT/f"preview-p{i:03d}.jpg").write_bytes(jpg)
   m["pages"].append({"pdf_page":i,"png_sha256":hash_bytes(png),"preview_sha256":hash_bytes(jpg),
                       "raw_rgb_sha256":hash_bytes(pix.samples),"native_dimensions":[pix.width,pix.height],
                       "glyph_read":"PENDING_MANUAL_READ"})
   print("13DQ_PAGE_BEGIN",i,len(jpg),flush=True)
   print(base64.b64encode(jpg).decode(),flush=True)
   print("13DQ_PAGE_END",i,flush=True)
  m["status"]="NATIVE_GLYPH_IMAGES_READY_UNINTERPRETED"
  print("13DQ_SOURCE_PASS",PDF_SHA,n,len(d),flush=True)
 except Exception as e:
  m.update(status="SOURCE_OR_RENDER_BOUNDARY",error_type=type(e).__name__,error=str(e)[:240])
  raise
 finally:
  (OUT/"manifest.json").write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
