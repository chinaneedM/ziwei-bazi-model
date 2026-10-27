#!/usr/bin/env python3
"""13BX bounded 17-page original source image atlas; not text recognition."""
import hashlib,io,json,os,urllib.parse,urllib.request
from pathlib import Path
URL="https://archive.wul.waseda.ac.jp/kosho/ri06/ri06_02809/ri06_02809_0033/ri06_02809_0033.pdf"
PDF_SHA="28ebfeb34191f45715bc449d27da61fe04fb05eb45e84dd00cf569699f46225f"
P27_SHA="bfe72c70715b152295d526b8921a0ca1821a38340c73d275343a694d015201a0"
PAGES=list(range(28,45))
OUT=Path(os.environ.get("TIANWEN_13BX_OUT","goryeosa-waseda-13bx-original-atlas"))
MAX_PDF=90_000_000;MAX_IMAGE=12_000_000;MAX_TOTAL=28_000_000
def sha(b):return hashlib.sha256(b).hexdigest()
def original_pdf():
 p=urllib.parse.urlsplit(URL)
 if p.scheme!="https" or p.netloc!="archive.wul.waseda.ac.jp" or p.query or p.fragment:raise ValueError("source URL gate")
 req=urllib.request.Request(URL,headers={"User-Agent":"Tianwen-13BX-OriginalAtlas","Accept":"application/pdf"})
 with urllib.request.urlopen(req,timeout=120) as response:
  if response.status!=200 or urllib.parse.urlsplit(response.geturl()).netloc!=p.netloc:raise ValueError("source status/redirect gate")
  length=response.headers.get("Content-Length")
  if length and int(length)>MAX_PDF:raise ValueError("PDF declared size limit")
  b=response.read(MAX_PDF+1)
 if len(b)>MAX_PDF or not b.startswith(b"%PDF-") or sha(b)!=PDF_SHA:raise ValueError("PDF original bytes mismatch")
 return b
def main():
 import fitz
 from PIL import Image
 OUT.mkdir(exist_ok=True,parents=True)
 receipt={"schema":"TIANWEN-13BX-WASEDA-ORIGINAL-ATLAS-P28-P44-RECEIPT-R1",
          "source_url":URL,"pdf_sha256_expected":PDF_SHA,"original_source_pages":PAGES,
          "original_image_rows":[],"ocr":False,"glyphs_assigned":False,
          "historical_table_end":"NOT_YET_VISUALLY_REVIEWED","new_physical_source_votes":0}
 try:
  data=original_pdf();receipt["source_pdf_bytes"]=len(data)
  total=0
  with fitz.open(stream=data,filetype="pdf") as doc:
   if doc.page_count<44:raise ValueError("PDF page-count lacks proposed source range")
   p=doc.load_page(26)
   if 82 not in [x[0] for x in p.get_images(full=True)]:raise ValueError("p27 known source xref not present")
   if sha(doc.extract_image(82)["image"])!=P27_SHA:raise ValueError("p27 known source JPEG SHA drift")
   receipt["preceding_p27_jpeg_verified"]=P27_SHA
   for n in PAGES:
    refs=list(dict.fromkeys(z[0] for z in doc.load_page(n-1).get_images(full=True)))
    if not 1<=len(refs)<=3:raise ValueError("unexpected number of original embedded images on page "+str(n))
    for j,xref in enumerate(refs):
     obj=doc.extract_image(xref);raw=obj["image"];ext=obj["ext"].lower()
     if ext not in ("jpeg","jpg","png","jpx") or len(raw)>MAX_IMAGE:raise ValueError("image type/size bound")
     total+=len(raw)
     if total>MAX_TOTAL:raise ValueError("artifact original image cumulative cap")
     with Image.open(io.BytesIO(raw)) as im:
      im.load();wh=list(im.size)
      if min(wh)<900:raise ValueError("unexpected original source dimensions")
      thumb=im.convert("RGB")
      thumb.thumbnail((1400,1400),Image.Resampling.LANCZOS)
      out=io.BytesIO();thumb.save(out,format="JPEG",quality=77,optimize=True)
     key=f"p{n}-xref{xref}-{j+1}"
     original_name=key+"."+("jpg" if ext in ("jpg","jpeg") else ext)
     (OUT/original_name).write_bytes(raw)
     preview_name=key+"-preview.jpg";(OUT/preview_name).write_bytes(out.getvalue())
     row={"page_1based":n,"embedded_xref":xref,"original_file":original_name,
          "original_sha256":sha(raw),"width":wh[0],"height":wh[1],"bytes":len(raw),
          "preview_file":preview_name,"preview_sha256":sha(out.getvalue()),"original_glyph_reading":"NOT_REVIEWED"}
     receipt["original_image_rows"].append(row)
     print("TIANWEN13BX_ATLAS_ROW "+json.dumps(row,ensure_ascii=False))
  receipt["original_image_bytes_total"]=total
 except Exception as ex:receipt["error"]=type(ex).__name__+": "+str(ex)[:650]
 (OUT/"receipt.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("TIANWEN13BX_ATLAS_RECEIPT "+json.dumps({k:receipt.get(k) for k in ("error","source_pdf_bytes","original_image_bytes_total","historical_table_end")},ensure_ascii=False))
 if receipt.get("error") or len(receipt["original_image_rows"])<17:raise SystemExit(1)
if __name__=="__main__":main()
