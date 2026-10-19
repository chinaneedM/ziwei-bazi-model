#!/usr/bin/env python3
"""13U original Waseda Goryeosa 80-volume archive: one public book fascicle acquisition.
Records document identity only. No OCR, no glyph adjudication, no cross-copy votes.
"""
import argparse
import hashlib
import json
import time
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13U-WASEDA-GORYEOSA-0030-ORIGINAL-FASCICLE-ATLAS-ROUTE-R1.json"
SOURCE="https://archive.wul.waseda.ac.jp/kosho/ri06/ri06_02809/ri06_02809_0030/ri06_02809_0030.pdf"
LIMIT=80_000_000
def evidence():
 return json.loads((ROOT/E).read_text(encoding="utf-8"))
def check_static(e):
 assert e["schema"]=="TIANWEN-13U-WASEDA-GORYEOSA-V52-NATIVE-FASCICLE-INDEX-ACQUISITION-R1"
 assert e["priority_issue"]=="TW-OPEN-0005" and e["target_work_volume"]==52
 assert e["firstparty_catalog"]["call_number"]=="リ06 02809" and e["firstparty_catalog"]["physical_books"]==80
 assert e["firstparty_catalog"]["imprint_year"] is None
 s=e["firstparty_archive_route"]
 assert s["sample_digital_group"]==30 and s["archive_file_url"]==SOURCE
 assert s["browser_pdf_request_rejected_due_size_bytes"]==48797544
 assert s["source_sha256"] is None and s["source_binary_downloaded_at_commit"] is False
 assert s["source_original_title_folio_verified"] is False and s["sample_digital_group_contains_juan52"] is None
 for k in ("independent_source_numerical_votes_added","physical_copies_cross_bound_from_images","transmission_graph_nodes_added","source_registry_entries_added","algorithm_reopens"):
  assert e["clearance"][k]==0
 assert e["clearance"]["research_omissions_open"]==11 and e["clearance"]["deterministic_product_r1"]=="CLOSED"
def download(path):
 last=None
 for attempt in range(3):
  try:
   request=urllib.request.Request(SOURCE,headers={"User-Agent":"TianwenHistoricalBiblioResearch/13U (public academic facsimile)"})
   size=0;h=hashlib.sha256()
   with urllib.request.urlopen(request,timeout=150) as stream,open(path,"wb") as f:
    if not stream.geturl().startswith("https://archive.wul.waseda.ac.jp/kosho/"):
     raise RuntimeError("unexpected redirect outside Waseda")
    while True:
     chunk=stream.read(1024*1024)
     if not chunk:break
     size+=len(chunk)
     if size>LIMIT:raise RuntimeError("source exceeded 80MB limit")
     f.write(chunk);h.update(chunk)
   with path.open("rb") as inp:
    if inp.read(5)!=b"%PDF-":raise RuntimeError("not a PDF")
   if size<1_000_000:raise RuntimeError("unexpected very small file")
   return {"sha256":h.hexdigest(),"bytes":size}
  except Exception as ex:
   last=ex
   if path.exists():path.unlink()
   if attempt<2:time.sleep(5)
 raise RuntimeError("Waseda first-party public PDF fetch failed: "+str(last))
def atlas(pdf,out,receipt):
 import fitz
 from PIL import Image,ImageDraw
 doc=fitz.open(str(pdf))
 try:
  count=doc.page_count
  if not (8<=count<=250):raise RuntimeError(f"unexpected Waseda page count {count}")
  selected=sorted(set([1,2,3,4,5,6,7,8, max(1,count//2-1),max(1,count//2),max(1,count//2+1),max(1,count//2+2),count-3,count-2,count-1,count]))
  thumb=out/"thumbnails";thumb.mkdir(exist_ok=True)
  records=[];images=[]
  for pg in selected:
   page=doc.load_page(pg-1)
   scale=min(.6,450/max(page.rect.width,1))
   b=page.get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=False).tobytes("png")
   (thumb/f"page-{pg:03}.png").write_bytes(b)
   img=Image.open(thumb/f"page-{pg:03}.png").convert("RGB")
   records.append({"pdf_page_1based":pg,"thumbnail_png_sha256":hashlib.sha256(b).hexdigest(),"target_internal_work_juan_read":False,"physical_leaf_number":None,"D16_glyph":None,"D18_glyph":None})
   images.append(img)
  for start in range(0,len(images),8):
   sheet=Image.new("RGB",(4*480,2*520),"white")
   pen=ImageDraw.Draw(sheet)
   for pos,img in enumerate(images[start:start+8]):
    x=(pos%4)*480;y=(pos//4)*520
    img.thumbnail((440,465))
    sheet.paste(img,(x+20,y+32))
    pen.text((x+16,y+7),f"PDF p.{selected[start+pos]}",fill="black")
   sheet.save(out/f"waseda-sample-sheet-{start//8+1:02}.jpg",quality=91)
  receipt.update({"actual_pdf_pages":count,"selected_first_mid_last":selected,"thumbnail_evidence":records,"digitized_book30_juan52_presence":None,"original_paper_date":None,"ancient_numerical_glyph_votes":0})
  (out/"acquisition-receipt.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  print("13U_WASEDA_ORIGINAL_ACQUISITION="+json.dumps({"sha256":receipt["sha256"],"bytes":receipt["bytes"],"pdf_pages":count,"thumbnail_pages":len(selected),"ancient_numeric_votes":0}))
 finally:doc.close()
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--output",default="waseda-goryeosa-0030-13u-evidence")
 a=ap.parse_args();e=evidence();check_static(e)
 out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 pdf=out/"waseda-ri06-02809-book0030-original.pdf"
 rec=download(pdf);rec.update({"exact_source":SOURCE,"firstparty_shelfmark":"リ06 02809","digital_group":30,"edition_imprint_year":None})
 atlas(pdf,out,rec)
if __name__=="__main__":main()
