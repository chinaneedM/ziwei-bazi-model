#!/usr/bin/env python3
"""13JB: original SNU GK05554_00 vol0018 viewer source-emitted image locator audit.

No page numbers, image paths, or selectors may be guessed. Exact volume came
from prior 13IZ provider volList; this extracts literal image anchors and
bounded script contexts from the existing official 13JA viewer page.
"""
import hashlib,html.parser,json,os,re,urllib.parse,urllib.request,urllib.error
from pathlib import Path
URL="https://kyudb.snu.ac.kr/book/text.do?item_cd=GJB&book_cd=GK05554_00&vol_no=0018"
EXPECTED_FROM_13JA="31c9afa4e92d68b6ec728758c20ca4cd0787c91a5690cbcd222bf8febdd13374"
CAP=2_000_000
NEEDLES=("imgViewer","page_no","/pf01/","rendererImg","viewImgList","images/","imgFile","data-src","book_cd","vol_no")
class Tags(html.parser.HTMLParser):
 def __init__(self):super().__init__();self.tag_links=[]
 def handle_starttag(self,tag,attrs):
  if tag not in ("img","a","iframe","source","script"):return
  d=dict(attrs)
  take={k:v[:240] for k,v in d.items() if k in ("src","href","data-src","data-original","onclick") and isinstance(v,str)}
  if take:self.tag_links.append({"tag":tag,"attrs":take})
def analyze(raw):
 t=raw.decode("utf-8","replace");parser=Tags();parser.feed(t)
 windows=[]
 for key in NEEDLES:
  at=t.find(key)
  if at>=0:
   windows.append({"key":key,"first_offset":at,"literal_snippet":t[max(0,at-140):at+240]})
 return {"html_sha256":hashlib.sha256(raw).hexdigest(),"html_bytes":len(raw),"sha_same_as_13JA":hashlib.sha256(raw).hexdigest()==EXPECTED_FROM_13JA,
         "exact_book_code_present":"GK05554_00" in t,
         "source_emitted_link_examples":parser.tag_links[:75],
         "bounded_source_literal_windows":windows,
         "page_number_literal_count":t.count("page_no"),"img_viewer_literal_count":t.count("imgViewer"),
         "original_page_image_retrieved":False,"printed_juan_or_folio_bound":False,
         "physical_edition_impression_date_bound":False}
def main():
 out=Path(os.environ.get("TIANWEN_13JB_OUT","/tmp/tianwen-13jb"));out.mkdir(parents=True,exist_ok=True)
 d={"schema":"TIANWEN_13JB_SOURCE_EMITTED_SNU_GK5554_VOL0018_VIEWER_DISCOVERY_R1","url":URL,"request_status":"UNAVAILABLE","result":None,
    "original_page_image_acquired":False,"historical_glyph_votes":0,"algorithm_reopens":0}
 req=urllib.request.Request(URL,headers={"Accept":"text/html,application/xhtml+xml","User-Agent":"Tianwen-13JB-SourceEmitted-HTML/1.0"})
 try:
  with urllib.request.urlopen(req,timeout=30) as r:
   u=urllib.parse.urlsplit(r.geturl())
   if (u.scheme,u.hostname)!=("https","kyudb.snu.ac.kr"):d["request_status"]="WRONG_PROVIDER"
   else:
    raw=r.read(CAP+1);d["http"]=r.status
    if len(raw)>CAP:d["request_status"]="OVERSIZED"
    elif not raw.lstrip().lower().startswith((b"<!doctype html",b"<html")):d["request_status"]="NOT_HTML"
    else:
     (out/"official-viewer-0018.html").write_bytes(raw)
     d["result"]=analyze(raw)
     d["request_status"]="FIRSTPARTY_VIEWER_HTML_CAPTURED"
 except urllib.error.HTTPError as e:d["request_status"]="HTTP_ERROR";d["http"]=e.code
 except Exception as e:d["request_status"]="TRANSPORT_ERROR";d["exception_type"]=type(e).__name__
 (out/"viewer-source-contexts.json").write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(d,ensure_ascii=False))
if __name__=="__main__":main()
