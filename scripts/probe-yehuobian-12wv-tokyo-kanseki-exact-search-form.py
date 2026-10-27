#!/usr/bin/env python3
"""12WV first-party exact Chinese catalogue advanced search input/form schema, no search guesses."""
import argparse,hashlib,html.parser,json,urllib.error,urllib.parse,urllib.request
from pathlib import Path
URL="https://kanseki.ioc.u-tokyo.ac.jp/user/query_adv.php"
MAX=360_000
UA="Tianwen/12WV source-issued exact public university catalog HTML; no original-image request"
class FormReader(html.parser.HTMLParser):
 def __init__(self):
  super().__init__();self.forms=[];self.form=None;self.select=None;self.links=[];self.text=[];self.scripts=[];self.script=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=="form":
   self.form={"action":a.get("action"),"method":a.get("method","get").lower(),"inputs":[],"selects":[],"textareas":[],"submit_buttons":[]}
   self.forms.append(self.form)
  if tag=="select" and self.form is not None:
   self.select={"name":a.get("name"),"options":[]};self.form["selects"].append(self.select)
  if tag=="option" and self.select is not None:
   self.select["options"].append({k:a.get(k) for k in ("value","selected") if k in a})
  if tag=="input" and self.form is not None:
   control={k:a.get(k) for k in ("name","type","value","onclick","checked") if k in a}
   self.form["inputs"].append(control)
  if tag=="button" and self.form is not None:
   self.form["submit_buttons"].append({k:a.get(k) for k in ("name","type","value","onclick") if k in a})
  if tag=="textarea" and self.form is not None:
   self.form["textareas"].append({k:a.get(k) for k in ("name","rows","cols") if k in a})
  if tag=="a" and a.get("href"):self.links.append(a["href"])
  if tag=="script":self.script=True
 def handle_endtag(self,tag):
  if tag=="form":self.form=None;self.select=None
  if tag=="select":self.select=None
  if tag=="script":self.script=False
 def handle_data(self,x):
  if self.script:self.scripts.append(x)
  else:self.text.append(x)
def guard(url=URL):
 if url!=URL:raise ValueError("only source-issued exact University Tokyo advanced-search page is allowed")
 return True
def inspect(html):
 if len(html)>MAX:raise ValueError("catalog source HTML over 360KB")
 p=FormReader();p.feed(html.decode("utf-8",errors="replace"))
 text=" ".join(p.text)
 return {
  "schema":"TIANWEN-12WV-TOKYO-IOC-EXACT-ADVANCED-SEARCH-PROVIDER-FORM-R1",
  "source_url":URL,"original_sha256":hashlib.sha256(html).hexdigest(),"original_bytes":len(html),
  "source_emitted_forms":p.forms,"source_emitted_links":p.links[:100],
  "source_script_fragments":[q[:1500] for q in p.scripts[:10]],
  "visible_book_title_field":("書名" in text),"visible_call_number_field":("索書號" in text),
  "source_request_from_original_item_barcode_executed":False,
  "original_1827_juan20_page_obtained":False,"original_1869_juan20_page_obtained":False,
  "provider_copy_to_image_mapping_obtained":False,"original_print_votes":0,"ocr":False
 }
def run(outdir):
 guard()
 out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
 try:
  req=urllib.request.Request(URL,headers={"User-Agent":UA,"Accept":"text/html"})
  with urllib.request.urlopen(req,timeout=35) as resp:
   end=urllib.parse.urlparse(resp.geturl())
   if end.scheme!="https" or end.hostname!="kanseki.ioc.u-tokyo.ac.jp":raise ValueError("source form redirected off provider host")
   b=resp.read(MAX+1)
  r=inspect(b)
  (out/"advanced-search.html").write_bytes(b)
  (out/"form-receipt.json").write_text(json.dumps(r,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  print(json.dumps({"status":"PROVIDER_ADVANCED_SEARCH_FORM_ACQUIRED","bytes":len(b),"forms":len(r["source_emitted_forms"]),"source_print_votes":0},ensure_ascii=False))
 except Exception as e:
  (out/"access-error.json").write_text(json.dumps({"status":"ACCESS_BOUNDARY_NOT_NEGATIVE_HOLDING_EVIDENCE","error":type(e).__name__,"http_code":getattr(e,"code",None),"source_votes":0},ensure_ascii=False))
  raise
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--output-dir",default="12wv-tokyo-advanced-form-output");p=a.parse_args()
 run(p.output_dir)
