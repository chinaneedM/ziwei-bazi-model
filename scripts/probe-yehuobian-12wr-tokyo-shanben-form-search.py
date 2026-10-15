#!/usr/bin/env python3
"""12WR: one exact public source-issued POST form from archived 12WQ HTML, no image."""
import argparse,hashlib,html.parser,json,urllib.request,urllib.parse,urllib.error
from pathlib import Path

ENDPOINT="https://shanben.ioc.u-tokyo.ac.jp/list.php?order=rn_no"
TARGET="野獲編"
FORM={"str":TARGET,"col":"ti","submits":"檢索"}
MAX_BYTES=500_000
UA="Tianwen/12WR exact one public search form, no OCR, no folio enumeration"
class Reader(html.parser.HTMLParser):
 def __init__(self):
  super().__init__();self.pieces=[];self.links=[];self.current=None
 def handle_starttag(self,tag,attrs):
  if tag=="a":
   a=dict(attrs);self.current={"href":a.get("href"),"text":""}
 def handle_data(self,s):
  self.pieces.append(s)
  if self.current is not None:self.current["text"]+=s
 def handle_endtag(self,tag):
  if tag=="a" and self.current is not None:
   self.links.append(self.current);self.current=None
def guard(endpoint=ENDPOINT,form=FORM):
 if endpoint!="https://shanben.ioc.u-tokyo.ac.jp/list.php?order=rn_no":
  raise ValueError("not source-issued exact POST route")
 if form!={"str":"野獲編","col":"ti","submits":"檢索"}:
  raise ValueError("one source-issued title search only")
 return True
def summarize(raw):
 if len(raw)>MAX_BYTES:raise ValueError("oversized official search page")
 p=Reader();p.feed(raw.decode("utf-8",errors="replace"))
 text=" ".join(p.pieces)
 matches=[{"text":z["text"].strip()[:200],"href":z["href"]} for z in p.links if TARGET in z["text"]]
 return {
  "schema":"TIANWEN-12WR-TOKYO-IOC-SHANBEN-SOURCE-ISSUED-ONE-TITLE-QUERY-R1",
  "source_form_url":ENDPOINT,"source_form_fields":FORM,
  "response_html_sha256":hashlib.sha256(raw).hexdigest(),
  "response_bytes":len(raw),
  "visible_text_contains_exact_target_title":TARGET in text,
  "title_bearing_links":matches[:25],
  "title_bearing_links_count":len(matches),
  "list_form_search_exhausts_historical_catalog":False,
  "actual_titled_printed_leaf_inspected":False,
  "tokyo_1827_folio_glyph_attested":False,
  "tokyo_1869_folio_glyph_attested":False,
  "source_absence_proven":False,
  "inference_scope":"One source-issued public index form response; index search result cannot prove the item does not exist or that a source image is available.",
  "original_print_votes":0,"ocr_used":False
 }
def execute(directory,opener=urllib.request.urlopen):
 out=Path(directory);out.mkdir(parents=True,exist_ok=True)
 try:
  guard()
  data=urllib.parse.urlencode(FORM).encode("utf-8")
  req=urllib.request.Request(ENDPOINT,data=data,headers={"User-Agent":UA,"Accept":"text/html","Content-Type":"application/x-www-form-urlencoded"},method="POST")
  with opener(req,timeout=35) as r:
   final=urllib.parse.urlparse(r.geturl())
   if final.scheme!="https" or final.hostname!="shanben.ioc.u-tokyo.ac.jp" or final.path!="/list.php":
    raise ValueError("unexpected off-form redirect")
   raw=r.read(MAX_BYTES+1)
  result=summarize(raw)
  result["final_url"]=r.geturl()
  (out/"official-index-search-response.html").write_bytes(raw)
  (out/"search-receipt.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  print(json.dumps({"status":"EXACT_TITLE_FORM_RESPONSE_ACQUIRED","matches":result["title_bearing_links_count"],"contains":result["visible_text_contains_exact_target_title"],"ancient_print_votes":0},ensure_ascii=False))
 except Exception as e:
  (out/"query-access-error.json").write_text(json.dumps({"status":"ACCESS_BOUNDARY_NO_EVIDENCE","exception":type(e).__name__,"http":getattr(e,"code",None),"physical_copy_votes":0},ensure_ascii=False))
  raise
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--output-dir",default="12wr-source-form-output");args=a.parse_args()
 execute(args.output_dir)
