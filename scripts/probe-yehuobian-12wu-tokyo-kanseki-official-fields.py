#!/usr/bin/env python3
"""12WU: provider-issued Tokyo IOC Chinese-book catalog documentation fields, not images."""
import argparse,hashlib,html.parser,json,urllib.error,urllib.parse,urllib.request
from pathlib import Path

SOURCES={
 "catalog_use_guide":"https://kanseki.ioc.u-tokyo.ac.jp/kanseki/annai_jp.html",
 "catalog_field_legend":"https://kanseki.ioc.u-tokyo.ac.jp/kanzi/user/menu/jintro.html",
 "catalog_search_guide":"https://kanseki.ioc.u-tokyo.ac.jp/kanzi/user/menu/help.html",
}
UA="Tianwen/12WU first party exact linked documentation metadata, no image or OCR"
MAX=300_000
class H(html.parser.HTMLParser):
 def __init__(self):
  super().__init__();self.text=[];self.links=[];self.forms=[];self.form=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=="a" and a.get("href"):self.links.append(a["href"])
  if tag=="form":
   self.form={"method":a.get("method","get"),"action":a.get("action"),"fields":[]};self.forms.append(self.form)
  if tag=="input" and self.form is not None:self.form["fields"].append({k:a[k] for k in ("name","type","value") if k in a})
 def handle_endtag(self,tag):
  if tag=="form":self.form=None
 def handle_data(self,x):self.text.append(x)
def allow(name,url):
 if name not in SOURCES or SOURCES[name]!=url:raise ValueError("only official source-linked exact documentation pages")
 return True
def parse(name,url,body):
 allow(name,url)
 if len(body)>MAX:raise ValueError("official metadata page too large")
 p=H();p.feed(body.decode("utf-8",errors="replace"))
 text=" ".join(p.text)
 links=[]
 for href in p.links:
  absolute=urllib.parse.urljoin(url,href)
  parsed=urllib.parse.urlparse(absolute)
  if parsed.scheme=="https" and parsed.hostname=="kanseki.ioc.u-tokyo.ac.jp" and not any(x in parsed.path.lower() for x in (".jpg",".gif",".png",".pdf",".zip",".tif")):
   links.append(absolute)
 return {"name":name,"url":url,"original_bytes":len(body),"original_sha256":hashlib.sha256(body).hexdigest(),
   "forms":p.forms[:20],"provider_metadata_links":links[:100],
   "explicit_frontmatter_or_cover_image_field":("卷首" in text or "巻首" in text or "書影" in text),
   "explicit_fulltext_link_field":("連結文本" in text or "全文影像資料庫" in text),
   "explicit_catalog_is_about_holdings":("所蔵" in text or "所藏" in text or "漢籍目錄" in text),
   "visible_year_2007":("2007" in text),"visible_title_target_yehuobian":("野獲編" in text),
   "observed_original_juan20_glyphs":0,"exact_1827_or_1869_item_image_authenticated":False,
   "historical_print_votes":0,"ocr":False}
def download(name,url):
 allow(name,url)
 req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html"})
 with urllib.request.urlopen(req,timeout=30) as r:
  end=urllib.parse.urlparse(r.geturl())
  if end.scheme!="https" or end.hostname!="kanseki.ioc.u-tokyo.ac.jp":raise ValueError("unexpected host redirect")
  body=r.read(MAX+1)
 return body,parse(name,url,body)
def run(outdir):
 out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
 pages=[]
 for name,url in SOURCES.items():
  try:
   data,p=download(name,url)
   (out/(name+".html")).write_bytes(data)
   pages.append({"status":"DIRECT_PROVIDER_ORIGINAL_HTML",**p})
  except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError,ValueError) as e:
   pages.append({"name":name,"url":url,"status":"ACCESS_BOUNDARY_METADATA_NOT_VERIFIED","error":type(e).__name__,"code":getattr(e,"code",None)})
 receipt={"schema":"TIANWEN-12WU-TOKYO-CATALOG-ORIGINAL-IMAGE-LINK-DESCRIPTORS-R1",
 "status":"EXACT_PROVIDER_DOCS_CONTROL_ONLY","source_results":pages,
 "source_page_count":len(pages),"original_juan20_image_count":0,
 "original_1827_or_1869_physical_item_bound":False,
 "online_image_availability_for_two_target_catalog_items":"UNVERIFIED",
 "full_catalog_no_original_page_absence_claim":True,
 "no_guessed_query_or_image_url":True,"ocr":False,"historical_print_votes":0}
 (out/"receipt.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"status":receipt["status"],"acquired":[x["name"] for x in pages if x["status"]=="DIRECT_PROVIDER_ORIGINAL_HTML"],"access_boundaries":[x["name"] for x in pages if x["status"]!="DIRECT_PROVIDER_ORIGINAL_HTML"],"historical_votes":0},ensure_ascii=False))
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--output-dir",default="12wu-tokyo-kanseki-fields-output");p=a.parse_args()
 run(p.output_dir)
