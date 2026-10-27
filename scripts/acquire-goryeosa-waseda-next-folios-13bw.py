#!/usr/bin/env python3
"""13BW strict Waseda official PDF p26/27 embedded firstparty image acquisition; no OCR."""
import hashlib,io,json,os,urllib.parse,urllib.request
from pathlib import Path
PDF="https://archive.wul.waseda.ac.jp/kosho/ri06/ri06_02809/ri06_02809_0033/ri06_02809_0033.pdf"
SOURCE_SHA="28ebfeb34191f45715bc449d27da61fe04fb05eb45e84dd00cf569699f46225f"
P25_SHA="ac19365a36456f0a550dd85873c0a006cee37765a352aa2b23d37137b5478646"
PAGES=(26,27)
OUT=Path(os.environ.get("TIANWEN_13BW_OUTPUT","goryeosa-waseda-13bw-p26-p27"))
def sha(b):return hashlib.sha256(b).hexdigest()
def fetch():
 u=urllib.parse.urlsplit(PDF)
 if u.scheme!="https" or u.netloc!="archive.wul.waseda.ac.jp" or u.query or u.fragment:raise ValueError("untrusted source URL")
 req=urllib.request.Request(PDF,headers={"User-Agent":"Tianwen-13BW-OriginalPage-Research","Accept":"application/pdf"})
 with urllib.request.urlopen(req,timeout=110) as response:
  if response.status!=200 or urllib.parse.urlsplit(response.geturl()).netloc!=u.netloc:raise ValueError("source status or redirect mismatch")
  length=response.headers.get("Content-Length")
  if length and int(length)>90_000_000:raise ValueError("source size limit header")
  raw=response.read(90_000_001)
 if len(raw)>90_000_000 or not raw.startswith(b"%PDF-") or sha(raw)!=SOURCE_SHA:raise ValueError("source original PDF integrity mismatch")
 return raw
def main():
 import fitz
 from PIL import Image
 OUT.mkdir(exist_ok=True,parents=True)
 receipt={"schema":"TIANWEN-13BW-WASEDA-ORIGINAL-P26-P27-SOURCE-RECEIPT-R1",
          "source_url":PDF,"source_pdf_sha256_expected":SOURCE_SHA,"page_list_1based":list(PAGES),
          "image_rows":[],"original_text_reading":"NOT_REVIEWED","ocr":False,"independent_source_votes_added":0}
 try:
  raw=fetch()
  receipt["pdf_bytes"]=len(raw)
  with fitz.open(stream=raw,filetype="pdf") as doc:
   if doc.page_count<27:raise ValueError("PDF source too short")
   prior=doc.load_page(24)
   if 76 not in [x[0] for x in prior.get_images(full=True)]:raise ValueError("previous p25 xref76 missing")
   if sha(doc.extract_image(76)["image"])!=P25_SHA:raise ValueError("previous p25 original SHA drift")
   receipt["original_p25_cross_page_control"]={"xref":76,"jpeg_sha256":P25_SHA}
   for page in PAGES:
    refs=list(dict.fromkeys(row[0] for row in doc.load_page(page-1).get_images(full=True)))
    if not 1<=len(refs)<=4:raise ValueError("out of bound source embedded image count")
    for k,ref in enumerate(refs):
     obj=doc.extract_image(ref);data=obj["image"];fmt=obj["ext"].lower()
     if fmt not in ("jpeg","jpg","png","jpx") or len(data)>12_000_000:raise ValueError("out of bound original image")
     with Image.open(io.BytesIO(data)) as im:
      im.load();dims=list(im.size)
      if min(dims)<900:raise ValueError("original image unexpectedly small")
      img=im.convert("RGB")
      img.thumbnail((1500,1500),Image.Resampling.LANCZOS)
      buf=io.BytesIO();img.save(buf,format="JPEG",quality=80,optimize=True)
     key=f"p{page}-xref{ref}-{k+1}"
     filename=key+("."+"jpg" if fmt in ("jpeg","jpg") else "."+fmt)
     (OUT/filename).write_bytes(data)
     preview=key+"-preview.jpg";(OUT/preview).write_bytes(buf.getvalue())
     rec={"page":page,"xref":ref,"file":filename,"sha256":sha(data),"dimensions":dims,"bytes":len(data),
          "preview":preview,"preview_sha256":sha(buf.getvalue()),"literal_glyphs":"NOT_REVIEWED"}
     receipt["image_rows"].append(rec)
     print("TIANWEN_13BW_SOURCE_IMAGE "+json.dumps(rec,ensure_ascii=False))
 except Exception as ex:
  receipt["error"]=type(ex).__name__+": "+str(ex)[:450]
 (OUT/"receipt.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("TIANWEN_13BW_RECEIPT "+json.dumps({k:receipt.get(k) for k in ("error","pdf_bytes","original_p25_cross_page_control")},ensure_ascii=False))
 if receipt.get("error") or len(receipt["image_rows"])<2:raise SystemExit(1)
if __name__=="__main__":main()
