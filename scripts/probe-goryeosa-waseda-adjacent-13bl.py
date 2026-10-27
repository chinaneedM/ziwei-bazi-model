#!/usr/bin/env python3
"""13BL bounded source-original Waseda adjacent-folio acquisition, no OCR or guessed glyphs."""
import base64, hashlib, io, json, os, urllib.parse, urllib.request
from pathlib import Path

PDF_URL="https://archive.wul.waseda.ac.jp/kosho/ri06/ri06_02809/ri06_02809_0033/ri06_02809_0033.pdf"
PDF_SHA="28ebfeb34191f45715bc449d27da61fe04fb05eb45e84dd00cf569699f46225f"
OUT=Path(os.environ.get("TIANWEN_13BL_OUT","goryeosa-13bl-original-capture"))
MAX_PDF=90_000_000
PAGES=(24,25) # Source PDF page numbers, not asserted historical table day labels.
def digest(raw):return hashlib.sha256(raw).hexdigest()
def main():
 from PIL import Image
 import fitz
 OUT.mkdir(parents=True,exist_ok=True)
 report={"schema":"TIANWEN-13BL-WASEDA-ADJACENT-ORIGINAL-FOLIO-ACQUISITION-R1",
         "provider_pdf":PDF_URL,"expected_pdf_sha256":PDF_SHA,
         "source_pdf_pages_1based":list(PAGES),"images":[],
         "glyph_readings":"NOT_REVIEWED","historical_D21_identification":"NOT_YET_VERIFIED",
         "OCR":False,"new_physical_witnesses":0,"historical_numeric_votes":0}
 try:
  p=urllib.parse.urlsplit(PDF_URL)
  if p.scheme!="https" or p.netloc!="archive.wul.waseda.ac.jp" or p.query or p.fragment:
   raise ValueError("unapproved source URL")
  req=urllib.request.Request(PDF_URL,headers={"User-Agent":"TianwenSourceResearch/13BL","Accept":"application/pdf"})
  with urllib.request.urlopen(req,timeout=120) as resp:
   if resp.status!=200 or urllib.parse.urlsplit(resp.geturl()).netloc!=p.netloc:
    raise ValueError("provider status or redirect boundary")
   length=resp.headers.get("Content-Length")
   if length and int(length)>MAX_PDF:raise ValueError("PDF length header exceeds bound")
   pdf=resp.read(MAX_PDF+1)
  if len(pdf)>MAX_PDF or not pdf.startswith(b"%PDF-") or digest(pdf)!=PDF_SHA:
   raise ValueError("source PDF bytes/type/SHA failed")
  report["downloaded_pdf_bytes"]=len(pdf)
  with fitz.open(stream=pdf,filetype="pdf") as doc:
   if doc.page_count<max(PAGES):raise ValueError("source PDF too short")
   report["provider_pdf_page_count"]=doc.page_count
   for page_number in PAGES:
    page=doc.load_page(page_number-1)
    xrefs=list(dict.fromkeys(row[0] for row in page.get_images(full=True)))
    report.setdefault("page_image_xrefs",{})[str(page_number)]=xrefs
    if not xrefs or len(xrefs)>4:raise ValueError("missing or overbroad page image list")
    for n,xref in enumerate(xrefs):
     obj=doc.extract_image(xref)
     raw=obj["image"]
     if len(raw)>12_000_000:raise ValueError("image exceeds 12 MB bound")
     with Image.open(io.BytesIO(raw)) as im:
      im.load()
      dims=list(im.size)
      if min(dims)<900:raise ValueError("unexpected small embedded image")
      overview=im.convert("RGB")
      overview.thumbnail((1350,1350),Image.Resampling.LANCZOS)
      buff=io.BytesIO()
      overview.save(buff,format="JPEG",quality=67,optimize=True)
      preview=buff.getvalue()
     key=f"waseda-p{page_number}-image{n+1}-xref{xref}"
     ext=obj["ext"].lower()
     if ext not in ("jpeg","jpg","png","jpx"):raise ValueError("unexpected image type")
     filename=key+"."+("jpg" if ext in ("jpeg","jpg") else ext)
     (OUT/filename).write_bytes(raw)
     (OUT/(key+"-preview.jpg")).write_bytes(preview)
     info={"source_pdf_page_1based":page_number,"image_xref":xref,"image_extension":ext,
           "original_image_file":filename,"original_image_sha256":digest(raw),
           "image_bytes":len(raw),"dimensions":dims,"preview_sha256":digest(preview)}
     report["images"].append(info)
     # Small source-bound previews are emitted as logs for human visual review.
     encoded=base64.b64encode(preview).decode("ascii")
     chunks=[encoded[i:i+2800] for i in range(0,len(encoded),2800)]
     for i,chunk in enumerate(chunks):
      print(f"TW13BL_PREVIEW {key} {i+1}/{len(chunks)} {chunk}")
     print("TW13BL_SOURCE_IMAGE "+json.dumps(info,ensure_ascii=False))
 except Exception as exc:
  report["error"]=type(exc).__name__+": "+str(exc)[:450]
 (OUT/"receipt.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("TW13BL_RECEIPT "+json.dumps({k:v for k,v in report.items() if k!="images"},ensure_ascii=False))
 if report.get("error") or len(report["images"])<2:
  raise SystemExit(1)
if __name__=="__main__":main()
