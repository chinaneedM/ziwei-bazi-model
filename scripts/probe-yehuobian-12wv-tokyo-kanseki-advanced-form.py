#!/usr/bin/env python3
"""12WV bounded Tokyo general Kanseki catalogue advanced-search form source.

The exact URL occurs in SOURCE-GUIDE 12WU original HTML; no guessed result,
folio or image URLs, no request to search until method/field names verified.
"""
import argparse,hashlib,html.parser,json,urllib.request,urllib.error
from pathlib import Path
from urllib.parse import urljoin,urlparse
SOURCE="https://kanseki.ioc.u-tokyo.ac.jp/user/query_adv.php"
MAX_BYTES=450000
UA="Tianwen-12WV exact original IOC catalogue advanced form only no OCR"
class AdvancedForm(html.parser.HTMLParser):
 def __init__(self):
  super().__init__();self.forms=[];self.current=None;self.current_select=None;self.fields=[];self.links=[];self.scripts=[];self.text=[];self.in_option=False;self.last_option=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=="form":
   self.current={"method":a.get("method","get").upper(),"action":a.get("action"),
    "name":a.get("name"),"id":a.get("id"),"fields":[],"selects":[]}
   self.forms.append(self.current)
  elif tag in ("input","textarea","button"):
   z={k:a.get(k) for k in ("name","type","value","onclick","id") if k in a}
   if self.current is not None:self.current["fields"].append({"tag":tag,**z})
   else:self.fields.append({"tag":tag,**z})
  elif tag=="select":
   x={"name":a.get("name"),"id":a.get("id"),"options":[]}
   if self.current is not None:self.current["selects"].append(x)
   self.current_select=x
  elif tag=="option" and self.current_select is not None:
   z={"value":a.get("value"),"text":""}
   self.current_select["options"].append(z);self.last_option=z
  elif tag=="a" and a.get("href"):
   self.links.append({"url":urljoin(SOURCE,a["href"]),"title":a.get("title")})
  elif tag=="script" and a.get("src"):
   self.scripts.append(urljoin(SOURCE,a["src"]))
 def handle_data(self,data):
  self.text.append(data)
  if self.last_option is not None:self.last_option["text"]+=data
 def handle_endtag(self,tag):
  if tag=="form":self.current=None;self.current_select=None
  if tag=="option":self.last_option=None
  if tag=="select":self.current_select=None
def guard(url):
 u=urlparse(url)
 if url!=SOURCE or u.scheme!="https" or u.hostname!="kanseki.ioc.u-tokyo.ac.jp":
  raise ValueError("12WU did not source-issue this exact advanced form")
 return True
def parse(blob):
 if len(blob)>MAX_BYTES:raise ValueError("source too large")
 p=AdvancedForm();p.feed(blob.decode("utf-8",errors="replace"))
 text=" ".join(p.text)
 return {"schema":"TIANWEN-12WV-TOKYO-IOCGC-SOURCE-ISSUED-ADVANCED-SEARCH-FORM-R1",
    "provider_url":SOURCE,"original_html_size":len(blob),
    "original_html_sha256":hashlib.sha256(blob).hexdigest(),
    "html_forms":p.forms[:15],"unassociated_inputs":p.fields[:40],
    "external_script_urls":p.scripts[:25],"emitted_hyperlinks":p.links[:45],
    "visible_advanced_search_label":"進階檢索" in text,
    "source_catalog_historic_title_query_executed":False,
    "item_6403767830_page_image_proven":False,
    "item_6403148395_page_image_proven":False,
    "new_original_juan20_glyphs":0,
    "historic_independent_print_votes":0,
    "no_ocr":True}
def capture(d):
 out=Path(d);out.mkdir(parents=True,exist_ok=True)
 try:
  guard(SOURCE)
  req=urllib.request.Request(SOURCE,headers={"User-Agent":UA,"Accept":"text/html"})
  with urllib.request.urlopen(req,timeout=40) as f:
   if f.geturl()!=SOURCE:raise ValueError("source redirected away")
   blob=f.read(MAX_BYTES+1)
  record=parse(blob)
  (out/"original-advanced-search.html").write_bytes(blob)
  (out/"advanced-form-receipt.json").write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  print(json.dumps({"status":"SOURCE_ADVANCED_FORM_ACQUIRED","html_bytes":len(blob),
    "forms":len(record["html_forms"]),"original_print_votes":0},ensure_ascii=False))
 except Exception as e:
  (out/"access-boundary.json").write_text(json.dumps({"status":"NO_SOURCE_ADVANCED_FORM","error":type(e).__name__,"http_status":getattr(e,"code",None),"original_print_votes":0},ensure_ascii=False))
  raise
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--output-dir",default="12wv-kanseki-advanced-form")
 a=p.parse_args();capture(a.output_dir)
