#!/usr/bin/env python3
"""12WU: source-issued Tokyo IOC general Chinese catalog JS/manual retrieval.

Only two links literally present in institution source HTML (12WT).
No arbitrary search query, no server state mutations, no image download.
"""
import argparse,hashlib,html.parser,json,re,urllib.request,urllib.error
from pathlib import Path
from urllib.parse import urljoin,urlparse
SOURCES={
 "entry_script":"https://kanseki.ioc.u-tokyo.ac.jp/user/js/script.js",
 "source_guide":"https://kanseki.ioc.u-tokyo.ac.jp/kanseki/annai_jp.html",
}
MAX_BYTES=300_000
UA="Tianwen-12WU exact first-party Hanji catalogue source-linked navigation controls"
class Guide(html.parser.HTMLParser):
 def __init__(self):
  super().__init__();self.anchors=[];self.forms=[];self.images=[];self.current=None;self.currentlink=None;self.text=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=="a":
   self.currentlink={"href":a.get("href"),"text":"","title":a.get("title")};self.anchors.append(self.currentlink)
  if tag=="form":
   self.current={"action":a.get("action"),"method":a.get("method"),"inputs":[]};self.forms.append(self.current)
  if tag=="input" and self.current is not None:
   self.current["inputs"].append({"name":a.get("name"),"type":a.get("type")})
  if tag=="img":self.images.append({"src":a.get("src"),"alt":a.get("alt"),"title":a.get("title")})
 def handle_data(self,data):
  self.text.append(data)
  if self.currentlink is not None:self.currentlink["text"]+=data
 def handle_endtag(self,tag):
  if tag=="form":self.current=None
  if tag=="a":self.currentlink=None
def guard(name,url):
 if SOURCES.get(name)!=url:raise ValueError("not official source-emitted endpoint")
 q=urlparse(url)
 if q.scheme!="https" or q.hostname!="kanseki.ioc.u-tokyo.ac.jp" or q.query:
  raise ValueError("not exact first party")
 return True
def parse(name,raw):
 if len(raw)>MAX_BYTES:raise ValueError("source exceeds declared byte bound")
 src=SOURCES[name]
 result={"name":name,"url":src,"raw_sha256":hashlib.sha256(raw).hexdigest(),"raw_bytes":len(raw)}
 if name=="entry_script":
  js=raw.decode("utf-8",errors="replace")
  # Inspection-only: neither execute the JavaScript nor follow its links automatically.
  result.update({"script_function_names":re.findall(r"\bfunction\s+([A-Za-z_]\w*)\s*\(",js)[:60],
    "quoted_path_like_strings":re.findall(r"""["']([^"']{1,180}(?:\.php|\.html|\.htm|\.asp|\.cgi)(?:\?[^"']*)?)["']""",js)[:60],
    "relative_navigation_strings":re.findall(r"(?:window\.open|location\.href|window\.location|document\.location)\s*(?:=|\()\s*([^;\n]{1,170})",js)[:40],
    "contains_request_or_image_bulk_execution":False})
 else:
  x=Guide();x.feed(raw.decode("utf-8",errors="replace"))
  text=" ".join(x.text)
  result.update({"anchors":[{"url":urljoin(src,i["href"]),"label":i["text"].strip()[:200]} for i in x.anchors if i.get("href")][:75],
    "forms":x.forms[:20],
    "image_elements":len(x.images),
    "visible_text_mentions_database_title":"漢籍目錄" in text or "漢籍目録" in text,
    "manual_scope_notes":{"catalog_pre2001_originals":("2001年" in text),"new_since_2002_other_catalog":("2002年" in text),
      "separate_full_image_repository":("全文画像" in text),"physical_books_vs_traditional_bibliography":("物理的" in text)}})
 result["independent_original_1827_1869_print_votes"]=0
 result["original_juan20_target_glyphs"]=0
 result["keio_or_tokyo_book_copy_binding"]=False
 result["ocr_used"]=False
 return result
def capture(directory):
 out=Path(directory);out.mkdir(parents=True,exist_ok=True)
 rows=[]
 for name,url in SOURCES.items():
  try:
   guard(name,url)
   req=urllib.request.Request(url,headers={"User-Agent":UA})
   with urllib.request.urlopen(req,timeout=35) as f:
    if f.geturl()!=url:raise ValueError("redirect outside exact source")
    b=f.read(MAX_BYTES+1)
   x=parse(name,b)
   (out/(name+".source")).write_bytes(b)
   rows.append({"status":"OFFICIAL_ORIGINAL_SOURCE_ACQUIRED",**x})
  except (urllib.error.URLError,ValueError,TimeoutError) as e:
   rows.append({"status":"ACCESS_BOUNDARY_NO_ORIGINAL_SOURCE","source":name,"error_class":type(e).__name__,"http_status":getattr(e,"code",None)})
 doc={"schema":"TIANWEN-12WU-TOKYO-GENERAL-CATALOGUE-TWO-SOURCE-LINK-CONTROLS-R1",
       "sources":rows,"original_juan20_paper_image_attested":False,
       "independent_1827_1869_original_print_votes":0,
       "new_glyphs_attested":0,"no_ocr":True}
 (out/"source-link-receipt.json").write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"results":[(x["source"] if "source" in x else x.get("name"),x["status"]) for x in rows],"independent_print_votes":0},ensure_ascii=False))
 return doc
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--output-dir",default="12wu-kanseki-source-links")
 a=p.parse_args();capture(a.output_dir)
