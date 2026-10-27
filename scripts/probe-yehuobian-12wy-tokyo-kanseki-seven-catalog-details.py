#!/usr/bin/env python3
"""12WY: only seven directly returned Tokyo university title-row detail IDs (12WX)."""
import argparse,hashlib,html.parser,json,re,urllib.error,urllib.parse,urllib.request
from pathlib import Path

SOURCE_QUERY="https://kanseki.ioc.u-tokyo.ac.jp/user/query_adv.php"
SOURCE_HTML_SHA256="94d245a69438527a96af5a21e306bab9c76dbb66c2fe5b02be742eda49619d98"
# Exactly as emitted by img onclick="ftlink(dno,no,'qadv')" in provider's original 12WX result:
ACTUAL_PROVIDER_TUPLES=(("9927",1),("9928",2),("78464",3),("90972",4),("103841",5),("104379",6),("109371",7))
HOST="kanseki.ioc.u-tokyo.ac.jp"
PREFIX="https://"+HOST+"/user/query_detail.php"
UA="Tianwen 12WY only seven exact provider-emitted title row detail IDs, no image exploration"
MAX_PAGE=320_000
class Doc(html.parser.HTMLParser):
 def __init__(self):
  super().__init__();self.text=[];self.links=[];self.images=[];self.scripts=[];self.js=False;self.tags=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=="a" and a.get("href"):self.links.append({"href":a["href"],"onclick":a.get("onclick")})
  if t=="img":self.images.append({"src":a.get("src"),"onclick":a.get("onclick"),"alt":a.get("alt")})
  if t=="script":self.js=True
  if a.get("onclick"):self.tags.append({"tag":t,"onclick":a["onclick"]})
 def handle_endtag(self,t):
  if t=="script":self.js=False
 def handle_data(self,d):
  if self.js:self.scripts.append(d)
  else:self.text.append(d)
def url_for(id,index):
 if (str(id),int(index)) not in ACTUAL_PROVIDER_TUPLES:raise ValueError("detail request not one of seven source-emitted IDs")
 return PREFIX+"?"+urllib.parse.urlencode({"dno":str(id),"no":str(index),"tp":"qadv"})
def parse(id,index,raw):
 url_for(id,index)
 if len(raw)>MAX_PAGE:raise ValueError("source detail exceeded cap")
 p=Doc();p.feed(raw.decode("utf-8",errors="replace"))
 t=" ".join(p.text)
 return {"id":id,"rank":index,"url":url_for(id,index),"source_html_bytes":len(raw),"source_html_sha256":hashlib.sha256(raw).hexdigest(),
  "visible_title_yekakuhen":"野獲編" in t or "野获编" in t,
  "visible_1827_year":"道光七年" in t,"visible_1869_year":"同治八年" in t,
  "visible_oki_library":"大木" in t,"visible_kuraishi_library":"倉石" in t,
  "visible_1827_cinii_item":"6403767830" in t,"visible_1869_cinii_item":"6403148395" in t,
  "visible_text_prefix":t[:4000],"provider_emitted_href_controls":p.links[:100],
  "provider_emitted_image_controls":p.images[:50],"provider_emitted_onclick_controls":p.tags[:100],
  "original_page_pixels_downloaded":False,"independent_historical_print_voting":False,"ocr":False}
def run(out):
 d=Path(out);d.mkdir(parents=True,exist_ok=True)
 results=[]
 for id,no in ACTUAL_PROVIDER_TUPLES:
  url=url_for(id,no)
  try:
   req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html"})
   with urllib.request.urlopen(req,timeout=32) as r:
    u=urllib.parse.urlparse(r.geturl())
    if u.scheme!="https" or u.hostname!=HOST or u.path!="/user/query_detail.php":raise ValueError("provider detail redirect out of authorized route")
    body=r.read(MAX_PAGE+1)
   x=parse(id,no,body)
   (d/("detail-"+id+".html")).write_bytes(body)
   results.append({"status":"SOURCE_ISSUED_DETAIL_HTML",**x})
  except (ValueError,TimeoutError,urllib.error.HTTPError,urllib.error.URLError) as e:
   results.append({"status":"DETAIL_ACCESS_BOUNDARY","id":id,"rank":no,"url":url,"error":type(e).__name__,"http":getattr(e,"code",None)})
 obj={"schema":"TIANWEN-12WY-7-TOKYO-IOC-SOURCE-LINKED-YEHUOBIAN-DETAILS-R1",
  "source_original_title_query_sha256":SOURCE_HTML_SHA256,"source_script_provenance":"12WW ftlink('dno','no','qadv') => query_detail.php?dno=...&no=...&tp=qadv",
  "request_count":len(results),"provider_original_details":results,
  "source_status":"PROVIDER_ITEM_METADATA_OR_PER_OBJECT_ACCESS_BOUNDARY",
  "original_1827_juan20_image_verified":False,"original_1869_juan20_image_verified":False,
  "all_same_paper_copy_identity_proven":False,"ancient_independent_print_votes":0,
  "no_guessed_detail_numbers":True,"no_ocr":True}
 (d/"receipt.json").write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"source_details_acquired":[r["id"] for r in results if r["status"]=="SOURCE_ISSUED_DETAIL_HTML"],"access_boundaries":[r["id"] for r in results if r["status"]!="SOURCE_ISSUED_DETAIL_HTML"],"ancient_print_votes":0}))
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--output-dir",default="12wy-tokyo-seven-detail-output");p=a.parse_args()
 run(p.output_dir)
