#!/usr/bin/env python3
"""13W Waseda original group0033 collection: byte-constrained, scope-neutral, no OCR."""
import argparse,hashlib,json,urllib.request,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13W-WASEDA-GORYEOSA-BOOK34-WORK53-TO-BOOK33-R1.json"
SOURCE="https://archive.wul.waseda.ac.jp/kosho/ri06/ri06_02809/ri06_02809_0033/ri06_02809_0033.pdf"
MAX=90_000_000
def load():return json.loads((ROOT/E).read_text(encoding="utf-8"))
def validate(e):
 assert e["schema"]=="TIANWEN-13W-WASEDA-GORYEOSA-BOOK34-EXCLUDES-TARGET-BOOK33-PROBE-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["shelfmark"]=="リ06 02809"
 assert e["original_book_0034"]["original_pdf_sha256"]=="53644757776778236d28bd1ee21b41469814a69e794de3b780fb582c91b56ead"
 assert e["original_book_0034"]["volume53_proven"] is True and e["original_book_0034"]["volume52_target_present"] is False
 assert [r["pdf_page_1based"] for r in e["original_book_0034"]["native_page_recheck"]]==[1,2,71]
 assert [r["direct_read"] for r in e["original_book_0034"]["native_page_recheck"]]==["高麗史 志三十四","高麗史五十三／志卷第七","志卷第七"]
 assert e["candidate_book_0033"]["digital_group"]==33 and e["candidate_book_0033"]["archive_url"]==SOURCE
 assert e["candidate_book_0033"]["pdf_sha256"] is None and e["candidate_book_0033"]["internal_work52_verified"] is False
 assert all(e["safety"][k]==0 for k in ("independent_source_numeric_votes_added","original_source_registry_entries_added","transmission_graph_edges_added","algorithm_reopens"))
 assert e["safety"]["issues_open"]==11 and e["safety"]["chart_product_r1"]=="CLOSED"
def fetch(path):
 last=None
 for attempt in range(3):
  try:
   req=urllib.request.Request(SOURCE,headers={"User-Agent":"TianwenPhilologyResearch/13W (public source verification)"})
   sha=hashlib.sha256();n=0
   with urllib.request.urlopen(req,timeout=100) as resp,open(path,"wb") as f:
    if not resp.geturl().startswith("https://archive.wul.waseda.ac.jp/kosho/"):raise ValueError("unexpected download redirect")
    while True:
     b=resp.read(1024*1024)
     if not b:break
     n+=len(b)
     if n>MAX:raise ValueError("PDF above 90 MB bound")
     sha.update(b);f.write(b)
   with path.open("rb") as f:
    if f.read(5)!=b"%PDF-":raise ValueError("not PDF bytes")
   if n<1_000_000:raise ValueError("source too small for scanned manuscript")
   return {"source_pdf_bytes":n,"source_pdf_sha256":sha.hexdigest(),"source_url":SOURCE}
  except Exception as ex:
   last=ex
   if path.exists():path.unlink()
   if attempt<2:time.sleep(4)
 raise RuntimeError("first-party source unavailable: "+str(last))
def build(out,pdf,r):
 import fitz
 from PIL import Image,ImageDraw
 d=fitz.open(str(pdf))
 try:
  n=d.page_count
  if n<8 or n>250:raise ValueError("Waseda scanned book page count out of bound")
  selected=sorted(set(list(range(1,min(9,n+1)))+[max(1,n//2-1),max(1,n//2),max(1,n//2+1),max(1,n//2+2)]+list(range(max(1,n-3),n+1))))
  small=out/"thumbnails";small.mkdir(exist_ok=True)
  records=[];tiles=[]
  for page_no in selected:
   page=d.load_page(page_no-1)
   scale=min(.65,450/max(page.rect.width,1))
   bytes_=page.get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=False).tobytes("png")
   name=f"pdf-page-{page_no:03d}.png";(small/name).write_bytes(bytes_)
   img=Image.open(small/name).convert("RGB");img.thumbnail((440,460))
   tiles.append(img)
   records.append({"page_1based":page_no,"thumbnail_sha256":hashlib.sha256(bytes_).hexdigest(),"original_juan_read":None,"d16_glyph":None,"d18_glyph":None})
  for start in range(0,len(tiles),8):
   canvas=Image.new("RGB",(4*480,2*515),"white");brush=ImageDraw.Draw(canvas)
   for k,img in enumerate(tiles[start:start+8]):
    x=(k%4)*480;y=(k//4)*515
    canvas.paste(img,(x+20,y+30));brush.text((x+20,y+7),f"PDF page {selected[start+k]}",fill="black")
   canvas.save(out/f"contact-{start//8+1:02d}.jpg",quality=88)
  r.update({"pdf_page_count":n,"selected_pdf_page_numbers":selected,"thumb_manifest":records,"work52_original_title_verified":False,"numeric_source_votes":0,"paper_impression_year":None})
  (out/"source-receipt.json").write_text(json.dumps(r,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  print("TIANWEN_13W_WASEDA_BOOK0033_SOURCE="+json.dumps({k:r[k] for k in ("source_pdf_sha256","source_pdf_bytes","pdf_page_count","numeric_source_votes")}))
 finally:d.close()
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--output",default="waseda-goryeosa-0033-13w-artifact");args=ap.parse_args()
 e=load();validate(e);out=Path(args.output);out.mkdir(exist_ok=True,parents=True)
 pdf=out/"original-waseda-book0033.pdf";r=fetch(pdf);build(out,pdf,r)
if __name__=="__main__":main()
