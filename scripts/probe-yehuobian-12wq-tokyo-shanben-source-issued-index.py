#!/usr/bin/env python3
"""12WQ: one source-issued Tokyo official shanben list.php page; no mass crawl/images."""
import argparse,hashlib,html.parser,json,re,urllib.request,urllib.parse,urllib.error
from pathlib import Path
SOURCE_HOME="https://shanben.ioc.u-tokyo.ac.jp/"
SOURCE_LINK="https://shanben.ioc.u-tokyo.ac.jp/list.php"
MAX_BYTES=600_000
UA="Tianwen/12WQ public Tokyo IOC catalogue index entry, one metadata URL no images"
class IndexParser(html.parser.HTMLParser):
 def __init__(self):
  super().__init__();self.text=[];self.forms=[];self.links=[];self.form=None;self.select=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=="form":
   self.form={"method":a.get("method","get").lower(),"action":a.get("action"),"inputs":[],"selects":[]}
   self.forms.append(self.form)
  if tag=="input" and self.form is not None:
   self.form["inputs"].append({k:a.get(k) for k in ("name","type","value") if a.get(k) is not None})
  if tag=="select" and self.form is not None:
   self.select={"name":a.get("name"),"options":[]};self.form["selects"].append(self.select)
  if tag=="option" and self.select is not None:
   self.select["options"].append(a.get("value"))
  if tag=="a" and a.get("href"):
   self.links.append(a["href"])
 def handle_endtag(self,tag):
  if tag=="form":self.form=None;self.select=None
  if tag=="select":self.select=None
 def handle_data(self,txt):self.text.append(txt)
def validate_url(url):
 if url!=SOURCE_LINK:raise ValueError("not source-issued bounded exact Tokyo IOC HTML route")
 return True
def summarize(blob):
 if len(blob)>MAX_BYTES:raise ValueError("source HTML too large")
 p=IndexParser();p.feed(blob.decode("utf-8",errors="replace"))
 text=" ".join(p.text)
 import urllib.parse
 metadata={
  "schema":"TIANWEN-12WQ-TOKYO-IOC-OFFICIAL-SHANBEN-CATALOG-INDEX-FORMS-R1",
  "source":SOURCE_LINK,
  "source_html_bytes":len(blob),
  "source_html_sha256":hashlib.sha256(blob).hexdigest(),
  "visible_text_mentions_yekakuhen":"野獲編" in text or "野获编" in text,
  "visible_text_mentions_1827_copy_identifier":"6403767830" in text,
  "visible_text_mentions_1869_copy_identifier":"6403148395" in text,
  "index_page_labels":re.findall(r"(?:共\s*\d+\s*筆|[0-9]+\s*/\s*[0-9]+\s*頁|[0-9]+\s*/\s*[0-9]+\s*页)",text)[:12],
  "html_forms":p.forms[:12],
  "anchor_count":len(p.links),
  "linked_index_candidates":[urllib.parse.urljoin(SOURCE_LINK,x) for x in p.links if x.endswith(".php") and "list" in x.lower()][:15],
  "source_attests_entire_shanben_catalog_absence":False,
  "original_juan20_image_acquired":False,
  "original_paper_copy_bound":False,
  "1827_original_impression_proven":False,
  "1869_corrected_original_impression_proven":False,
  "ancient_print_votes":0,
  "ocr_used":False
 }
 return metadata
def capture(dir):
 out=Path(dir);out.mkdir(parents=True,exist_ok=True)
 try:
  validate_url(SOURCE_LINK)
  req=urllib.request.Request(SOURCE_LINK,headers={"User-Agent":UA,"Accept":"text/html"})
  with urllib.request.urlopen(req,timeout=45) as f:
   if f.geturl()!=SOURCE_LINK:raise ValueError("not permitted source-emitted destination")
   buf=f.read(MAX_BYTES+1)
  record=summarize(buf)
  (out/"source-list-index.html").write_bytes(buf)
  (out/"index-receipt.json").write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  print(json.dumps({"status":"EXACT_SOURCE_METADATA_INDEX_ACQUIRED","size":len(buf),"source":SOURCE_LINK,"forms":len(record["html_forms"]),"print_votes":0},ensure_ascii=False))
 except Exception as e:
  (out/"access-boundary.json").write_text(json.dumps({"status":"NO_SOURCE_INDEX_ATTESTATION","error":type(e).__name__,"http_code":getattr(e,"code",None),"ancient_print_votes":0},ensure_ascii=False))
  raise
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--output-dir",default="12wq-source-index-output");args=a.parse_args()
 capture(args.output_dir)
