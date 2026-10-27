#!/usr/bin/env python3
"""12WP Tokyo IOC official shanben public catalogue navigation, NOT original folio/image."""
import argparse, hashlib, html.parser, json, urllib.error, urllib.request
from pathlib import Path
from urllib.parse import urljoin,urlparse

URLS={
 "ioc_directory":"https://www.ioc.u-tokyo.ac.jp/database/index.html",
 "shanben_home":"https://shanben.ioc.u-tokyo.ac.jp/",
 "shanben_help":"https://shanben.ioc.u-tokyo.ac.jp/help.html",
 "shanben_introduction":"https://shanben.ioc.u-tokyo.ac.jp/intro.html",
 "tokyo_1827_cinii":"https://ci.nii.ac.jp/ncid/BC0492354X",
 "tokyo_1869_cinii":"https://ci.nii.ac.jp/ncid/BB23196128",
}
TEXTLIMIT=400_000
MAX_REQUESTS=6
UA="Tianwen/12WP first-party bibliographic source-issued HTML (no OCR/images/scraping)"
class A(html.parser.HTMLParser):
 def __init__(self):
  super().__init__();self.links=[];self.text=[]
 def handle_starttag(self,tag,attrs):
  if tag!="a":return
  d=dict(attrs);self.links.append({"href":d.get("href"),"title":d.get("title"),"aria_label":d.get("aria-label")})
 def handle_data(self,data):
  self.text.append(data)
def permitted(name,url):
 if name not in URLS or URLS[name]!=url:raise ValueError("not one of six preapproved exact metadata pages")
 p=urlparse(url)
 if p.scheme!="https" or p.hostname not in ("www.ioc.u-tokyo.ac.jp","shanben.ioc.u-tokyo.ac.jp","ci.nii.ac.jp"):
  raise ValueError("non-official metadata host")
 if any(t in p.path for t in ("/image","/jpg","/pdf","/download","/scan","/thumbnail","/full")):
  raise ValueError("never probe source image data")
 return True
def digest(b):return hashlib.sha256(b).hexdigest()
def extract(name,url,body):
 permitted(name,url)
 if len(body)>TEXTLIMIT:raise ValueError("HTML oversized")
 p=A();p.feed(body.decode("utf-8",errors="replace"))
 txt=" ".join(p.text)
 links=[]
 for a in p.links:
  x=a.get("href")
  if not x:continue
  link=urljoin(url,x)
  if not link.startswith("https://"):continue
  d=urlparse(link)
  if d.hostname in ("shanben.ioc.u-tokyo.ac.jp","www3.ioc.u-tokyo.ac.jp","www.ioc.u-tokyo.ac.jp","ci.nii.ac.jp") and not any(w in d.path.lower() for w in (".jpg",".png",".gif",".jpeg",".pdf",".tif",".zip")):
   links.append({"url":link,"caption":a.get("title") or a.get("aria_label")})
 return {"source":name,"url":url,"html_sha256":digest(body),"html_bytes":len(body),"visible_html_contains_yekakuhen_kanji":"野獲編" in txt,"visible_html_contains_yekakuhen_simplified":"野获编" in txt,"visible_html_contains_1827_catalog_id":"6403767830" in txt,"visible_html_contains_1869_catalog_id":"6403148395" in txt,"document_links":links[:120],"link_count_in_html":len(links),"source_text_prefix":txt[:500]}
def request(name,url,opener=urllib.request.urlopen):
 permitted(name,url)
 req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html"})
 with opener(req,timeout=25) as r:
  final=r.geturl()
  if urlparse(final).scheme!="https" or urlparse(final).hostname!=urlparse(url).hostname:raise ValueError("source redirect out of institution")
  b=r.read(TEXTLIMIT+1)
 if len(b)>TEXTLIMIT:raise ValueError("source metadata exceeds bounded bytes")
 return b,extract(name,url,b)
def run(outdir):
 out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
 rows=[]
 for name,url in URLS.items():
  try:
   blob,summary=request(name,url)
   (out/(name+".html")).write_bytes(blob)
   rows.append({"status":"SOURCE_HTML_ACQUIRED",**summary})
  except (urllib.error.HTTPError,urllib.error.URLError,ValueError,TimeoutError) as e:
   rows.append({"source":name,"url":url,"status":"SOURCE_ACCESS_BOUNDARY","error_type":type(e).__name__,"http_status":getattr(e,"code",None)})
 result={"schema":"TIANWEN-12WP-TOKYO-IOC-SHANBEN-OFFICIAL-SOURCE-ISSUED-METADATA-ROUTES-R1",
    "status":"SIX_EXACT_OFFICIAL_HTML_METADATA_OBJECTS_SCOPED_WITH_PER_SOURCE_ACCESS_BOUNDARIES",
    "request_count":len(rows),"all_exact_routes":list(URLS),"source_results":rows,
    "human_read_original_target_1827_leaf":False,"human_read_original_target_1869_leaf":False,
    "physically_bound_catalog_item_to_digital_image":False,
    "source_absence_claim":False,
    "independent_ancient_impression_votes":0,"manual_fulltext_glyph_collation":False,"ocr_used":False}
 (out/"receipt.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"status":result["status"],"urls":len(rows),"acquired":sum(x["status"]=="SOURCE_HTML_ACQUIRED" for x in rows),"access_boundaries":[x["source"] for x in rows if x["status"]!="SOURCE_HTML_ACQUIRED"],"original_historical_print_votes":0},ensure_ascii=False))
 return result
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--output-dir",default="12wp-ioc-shanben-official-output");p=a.parse_args()
 run(p.output_dir)
