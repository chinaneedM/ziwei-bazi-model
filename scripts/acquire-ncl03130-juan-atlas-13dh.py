#!/usr/bin/env python3
"""13DH bounded NCL 03130 public Commons PDFs to manually build part -> juan boundaries.
No OCR, no inferred physical-copy identity, no source-original target glyph promotion.
"""
import base64,hashlib,io,json,os
from pathlib import Path
from urllib.parse import urlsplit
import fitz, requests
from PIL import Image,ImageDraw

PART=int(os.environ.get("NCL13DH_PART","8"))
if PART not in (8,9,10,11): raise SystemExit("part not in bounded probe set")
SOURCE=f"https://commons.wikimedia.org/wiki/Special:Redirect/file/NCL-03130_{PART:02d}_%E9%AB%98%E9%BA%97%E5%8F%B2.pdf"
EXPECTED_COUNTS={8:189,9:189,10:198,11:180}
OUTPUT=Path(f"ncl03130-13dh-part{PART:02d}")
SIZE_CAP=62_914_560
def digest(data):return hashlib.sha256(data).hexdigest()
def main():
 OUTPUT.mkdir(parents=True,exist_ok=True)
 manifest={"schema":"TIANWEN-13DH-NCL03130-MIRROR-JUAN-BOUNDARY-ATLAS-R1",
   "part":PART,"source":SOURCE,"source_class":"COMMONS_PUBLIC_MIRROR_NOT_NCL_FIRSTPARTY_PHYSICAL_COPY",
   "original_firstparty_NCL_item":"UNBOUND","juan52_found":"UNREVIEWED",
   "part_ordinal_does_not_equal_juan":True,"no_ocr":True,
   "status":"SOURCE_ACCESS_OR_FORMAT_BOUNDARY","original_pdf_sha256":"UNBOUND",
   "pages":[],"sheets":[],"hires":[]}
 try:
  with requests.get(SOURCE,stream=True,allow_redirects=True,timeout=(30,180),
                    headers={"User-Agent":"TianwenHistoricalSourceAudit/1.0 (public scan manuscript collation)"}) as resp:
   resp.raise_for_status()
   dest=urlsplit(resp.url)
   if dest.scheme!="https" or dest.hostname not in ("commons.wikimedia.org","upload.wikimedia.org"):
    raise RuntimeError("redirect not a Wikimedia public file host")
   chunks=[];total=0;sha=hashlib.sha256()
   for part in resp.iter_content(1024*1024):
    if not part:continue
    total+=len(part)
    if total>SIZE_CAP:raise RuntimeError("file exceeds 60MiB")
    sha.update(part);chunks.append(part)
  raw=b"".join(chunks)
  if raw[:5]!=b"%PDF-":raise RuntimeError("not PDF")
  pdf=fitz.open(stream=raw,filetype="pdf")
  if pdf.is_encrypted or len(pdf)!=EXPECTED_COUNTS[PART]:raise RuntimeError("source page count changed from public index")
  manifest.update(pdf_bytes=len(raw),original_pdf_sha256=sha.hexdigest(),
                  observed_pdf_pages=len(pdf),redirect_url=resp.url)
  shortlist=sorted(set([*range(1,min(11,len(pdf)+1)),
                         *range(max(1,len(pdf)//2-3),min(len(pdf)+1,len(pdf)//2+5)),
                         *range(max(1,len(pdf)-9),len(pdf)+1)]))
  renders=[]
  for page_no in range(1,len(pdf)+1):
   pg=pdf[page_no-1]
   pix=pg.get_pixmap(matrix=fitz.Matrix(0.55,0.55),alpha=False)
   im=Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
   im.thumbnail((240,168))
   renders.append(im)
   row={"pdf_page":page_no,"atlas_rgb_sha256":digest(im.tobytes()),
        "genre_juan_title":"UNREVIEWED","original_physical_volume":"UNBOUND"}
   if page_no in shortlist:
    big=pg.get_pixmap(matrix=fitz.Matrix(2.8,2.8),alpha=False)
    payload=big.tobytes("png")
    name=f"boundary-native-p{page_no:03}.png"
    (OUTPUT/name).write_bytes(payload)
    row["highres"]=name;row["highres_sha256"]=digest(payload)
    manifest["hires"].append(page_no)
   manifest["pages"].append(row)
  for start in range(0,len(renders),20):
   photos=renders[start:start+20]
   sheet=Image.new("RGB",(5*260,4*200),"white")
   draw=ImageDraw.Draw(sheet)
   for j,im in enumerate(photos):
    x=j%5*260;y=j//5*200
    sheet.paste(im,(x+6,y+21))
    draw.text((x+7,y+3),f"part {PART:02d} pdf {start+j+1:03}",fill="black")
   bio=io.BytesIO();sheet.save(bio,format="JPEG",quality=80,optimize=True)
   chunk=bio.getvalue();name=f"atlas-{start+1:03}-{start+len(photos):03}.jpg"
   (OUTPUT/name).write_bytes(chunk)
   manifest["sheets"].append({"name":name,"sha256":digest(chunk),"pages":[start+1,start+len(photos)]})
   # Only a small contact-sheet representative preview in runner logs;
   # the complete index is retained as GitHub artifact, not its base64 log.
   if start in (0,80,160):
    print("13DH_ATLAS_B64_BEGIN",name,len(chunk))
    print(base64.b64encode(chunk).decode())
    print("13DH_ATLAS_B64_END",name,flush=True)
  manifest["status"]="PDF_SHA_BOUND_ATLAS_UNREVIEWED"
  print("13DH_CAPTURE_OK",PART,sha.hexdigest(),len(raw),len(pdf),flush=True)
 except Exception as exc:
  manifest["status"]="SOURCE_ACCESS_OR_FORMAT_BOUNDARY"
  manifest["error_type"]=type(exc).__name__
  manifest["error"]=str(exc)[:350]
  print("13DH_SOURCE_BOUNDARY",PART,type(exc).__name__,str(exc)[:250],flush=True)
  raise
 finally:
  (OUTPUT/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
