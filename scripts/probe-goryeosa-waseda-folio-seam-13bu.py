#!/usr/bin/env python3
"""13BU source-pinned Waseda book33 preceding folio acquisition (no OCR)."""
import hashlib,io,json,os,urllib.parse,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13BU-GORYEOSA-WASEDA-D16-FOLIO-SEAM-AND-PRECEDING-SOURCE-R1.json"
PDF_URL="https://archive.wul.waseda.ac.jp/kosho/ri06/ri06_02809/ri06_02809_0033/ri06_02809_0033.pdf"
PDF_SHA="28ebfeb34191f45715bc449d27da61fe04fb05eb45e84dd00cf569699f46225f"
IMAGE23_SHA="388f3d5dd9e9861f8ce90c304b154edaeaee98614bb12cd3468f957dcde6fc66"
OUT=Path(os.environ.get("TIANWEN_13BU_OUT","goryeosa-13bu-waseda-original-neighbor"))
PAGES=(20,21,22)
def sha(b):return hashlib.sha256(b).hexdigest()
def fetch():
 parts=urllib.parse.urlsplit(PDF_URL)
 if parts.scheme!="https" or parts.netloc!="archive.wul.waseda.ac.jp" or parts.query or parts.fragment:raise ValueError("unapproved source URL")
 r=urllib.request.Request(PDF_URL,headers={"User-Agent":"Tianwen13BUSourceResearch","Accept":"application/pdf"})
 with urllib.request.urlopen(r,timeout=110) as q:
  if q.status!=200 or urllib.parse.urlsplit(q.geturl()).netloc!=parts.netloc:raise ValueError("source status or redirect drift")
  cl=q.headers.get("Content-Length")
  if cl and int(cl)>90_000_000:raise ValueError("oversize source")
  b=q.read(90_000_001)
 if len(b)>90_000_000 or not b.startswith(b"%PDF-") or sha(b)!=PDF_SHA:raise ValueError("PDF source type/sha/bounds mismatch")
 return b
def main():
 from PIL import Image
 import fitz
 OUT.mkdir(parents=True,exist_ok=True)
 receipt={"schema":"TIANWEN-13BU-WASEDA-PRIOR-ORIGINAL-PAGES-ACQUISITION-RECEIPT-R1","source_url":PDF_URL,
          "expected_pdf_sha256":PDF_SHA,"source_pdf_pages_1based":list(PAGES),"image_rows":[],
          "literal_text_readings":"NOT_REVIEWED","new_independent_historical_source_votes":0,"ocr_used":False}
 try:
  pdf=fetch()
  receipt["source_pdf_bytes"]=len(pdf)
  with fitz.open(stream=pdf,filetype="pdf") as doc:
   if doc.page_count<23:raise ValueError("PDF does not have page23")
   p23=doc.load_page(22)
   if 70 not in [z[0] for z in p23.get_images(full=True)]:raise ValueError("p23 known source image xref70 missing")
   original23=doc.extract_image(70)["image"]
   if sha(original23)!=IMAGE23_SHA:raise ValueError("p23 source-image integrity drift")
   receipt["page23_original_source_control"]={"xref":70,"jpeg_sha256":sha(original23)}
   for page in PAGES:
    imgrefs=list(dict.fromkeys(z[0] for z in doc.load_page(page-1).get_images(full=True)))
    if not 1<=len(imgrefs)<=4:raise ValueError("unexpected page image count")
    for ix,ref in enumerate(imgrefs):
     obj=doc.extract_image(ref)
     raw=obj["image"]
     if len(raw)>12_000_000:raise ValueError("one source image exceeds bound")
     ext=obj["ext"].lower()
     if ext not in ("jpeg","jpg","png","jpx"):raise ValueError("unexpected embedded image format")
     with Image.open(io.BytesIO(raw)) as im:
      dims=list(im.size)
      if min(dims)<900:raise ValueError("unexpected small original image")
      preview=im.convert("RGB")
      preview.thumbnail((1600,1600),Image.Resampling.LANCZOS)
      buf=io.BytesIO()
      preview.save(buf,format="JPEG",quality=82,optimize=True)
     key=f"p{page}-xref{ref}-{ix+1}"
     fname=key+"."+("jpg" if ext in ("jpeg","jpg") else ext)
     (OUT/fname).write_bytes(raw)
     pf=key+"-preview.jpg";(OUT/pf).write_bytes(buf.getvalue())
     info={"source_pdf_page_1based":page,"embedded_xref":ref,"extension":ext,"original_sha256":sha(raw),
           "original_file":fname,"preview_file":pf,"preview_sha256":sha(buf.getvalue()),"dimensions":dims}
     receipt["image_rows"].append(info)
     print("TW13BU_SOURCE_IMAGE "+json.dumps(info,ensure_ascii=False))
 except Exception as ex:
  receipt["error"]=type(ex).__name__+": "+str(ex)[:500]
 (OUT/"receipt.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("TW13BU_RECEIPT "+json.dumps({k:receipt.get(k) for k in ("error","page23_original_source_control","source_pdf_bytes")},ensure_ascii=False))
 if receipt.get("error") or len(receipt["image_rows"])<3:raise SystemExit(1)
if __name__=="__main__":main()
