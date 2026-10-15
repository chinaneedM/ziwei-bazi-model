#!/usr/bin/env python3
"""12WY exact four record-detail URLs emitted by 12WX Tokyo IOC title result.

Original 12WX HTML SHA256 94d245a6..., seven results; only four relevant
1827/1869 listed records checked. No other URLs, images or OCR allowed.
"""
import argparse,hashlib,html.parser,json,urllib.request,urllib.error
from pathlib import Path
from urllib.parse import urlencode,urlparse,urljoin
BASE="https://kanseki.ioc.u-tokyo.ac.jp/user/query_detail.php"
RESULT_PARENT_SHA="94d245a69438527a96af5a21e306bab9c76dbb66c2fe5b02be742eda49619d98"
RECORDS=(
 {"dno":"9927","no":"1","catalog_date_text":"道光七年刊本"},
 {"dno":"90972","no":"4","catalog_date_text":"(補遺)同治八年重校修補"},
 {"dno":"103841","no":"5","catalog_date_text":"道光七年刊；同治八年補刊本"},
 {"dno":"104379","no":"6","catalog_date_text":"道光七年刊本"},
)
MAX_BYTES=350000
UA="Tianwen-12WY four source-emitted IOC catalog detail views only; no image retrieval"
class Details(html.parser.HTMLParser):
 def __init__(self):
  super().__init__();self.text=[];self.links=[];self.current=None;self.forms=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=="a" and a.get("href"):
   self.current={"href":a["href"],"label":""}
  if tag=="form":
   self.forms.append({"action":a.get("action"),"method":a.get("method")})
 def handle_data(self,txt):
  self.text.append(txt)
  if self.current is not None:self.current["label"]+=txt
 def handle_endtag(self,tag):
  if tag=="a" and self.current is not None:
   self.links.append(self.current);self.current=None
def url_for(r):
 return BASE+"?"+urlencode([("dno",r["dno"]),("no",r["no"]),("tp","qadv")])
def guard(entry,url):
 if entry not in RECORDS:raise ValueError("not source-verified list record")
 if url!=url_for(entry) or urlparse(url).hostname!="kanseki.ioc.u-tokyo.ac.jp":
  raise ValueError("detail URL must be exactly source-emitted ftlink")
 return True
def inspect(raw,entry):
 if len(raw)>MAX_BYTES:raise ValueError("oversized detail HTML")
 p=Details();p.feed(raw.decode("utf-8",errors="replace"))
 txt=" ".join(p.text)
 return {
  "source_internal_dno":entry["dno"],
  "source_search_result_position":int(entry["no"]),
  "source_search_result_editional_text":entry["catalog_date_text"],
  "source_record_url":url_for(entry),
  "raw_provider_html_bytes":len(raw),"raw_provider_html_sha256":hashlib.sha256(raw).hexdigest(),
  "has_original_work_title_in_visible_text":"野獲" in txt or "野获" in txt,
  "visible_text_excerpt":txt[:4000],
  "links":[{"url":urljoin(url_for(entry),x["href"]),"label":x["label"].strip()[:110]} for x in p.links[:80]],
  "forms":p.forms[:6],
  "page_contains_Oki_barcode_literal":"6403767830" in txt,
  "page_contains_Kuraishi_barcode_literal":"6403148395" in txt,
  "original_juan20_leaf_image_acquired":False,
  "independently_printed_1827_paper_proven":False,
  "independently_revised_1869_paper_proven":False,
  "new_historical_glyph_votes":0
 }
def capture(directory):
 d=Path(directory);d.mkdir(parents=True,exist_ok=True)
 rows=[]
 for x in RECORDS:
  url=url_for(x)
  try:
   guard(x,url)
   q=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html"})
   with urllib.request.urlopen(q,timeout=35) as r:
    p=urlparse(r.geturl())
    if p.scheme!="https" or p.hostname!="kanseki.ioc.u-tokyo.ac.jp" or p.path!="/user/query_detail.php":
     raise ValueError("redirect away from original catalogue detail")
    raw=r.read(MAX_BYTES+1)
   rec=inspect(raw,x)
   (d/("provider-item-"+x["dno"]+".html")).write_bytes(raw)
   rows.append({"status":"FIRST_PARTY_DETAIL_HTML_ACQUIRED",**rec})
  except (urllib.error.HTTPError,urllib.error.URLError,ValueError,TimeoutError) as e:
   rows.append({"status":"ACCESS_BOUNDARY_NO_ORIGINAL_ITEM_DETAIL","source_internal_dno":x["dno"],"http_code":getattr(e,"code",None),"error_class":type(e).__name__,"new_historical_glyph_votes":0})
 summary={"schema":"TIANWEN-12WY-TOKYO-GENERAL-CATALOGUE-FOUR-SOURCE-EMITTED-DETAIL-RECEIPTS-R1",
  "original_title_query_parent_sha256":RESULT_PARENT_SHA,
  "provider_item_details":rows,
  "request_count":len(rows),
  "catalog_internal_identifiers_are_not_CiNii_item_barcodes":True,
  "no_original_1827_or_1869_paper_glyph_attestation":True,
  "new_independent_print_votes":0,
  "ocr_used":False}
 (d/"four-detail-receipt.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"status":"SOURCE_EMITTED_DETAIL_RETRIEVAL_COMPLETE","requested":len(rows),
   "acquired":sum(x["status"]=="FIRST_PARTY_DETAIL_HTML_ACQUIRED" for x in rows),
   "original_historical_print_votes":0},ensure_ascii=False))
 return summary
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--output-dir",default="12wy-tokyo-details");z=a.parse_args()
 capture(z.output_dir)
