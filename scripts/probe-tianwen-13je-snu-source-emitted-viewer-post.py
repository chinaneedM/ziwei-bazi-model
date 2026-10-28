#!/usr/bin/env python3
"""13JE: exact firstparty SNU viewer FORM POST from archived HTML and official JS.

13JA original SNU volume0018 HTML SHA256 31c9...74 emitted the eight frmPopViewer
hidden fields and literal page calls 048a/085a. 13JD original SNU common2.js SHA256
b2b4...87 explicitly POSTs them to /pf01/rendererImg.do. This probe requests
only that official viewer, does not discover by guessing or request an image.
"""
import hashlib,html.parser,http.cookiejar,json,os,time,urllib.error,urllib.parse,urllib.request
from pathlib import Path

BASE="https://kyudb.snu.ac.kr"
REFERER=BASE+"/book/text.do?item_cd=GJB&book_cd=GK05554_00&vol_no=0018"
ENDPOINT=BASE+"/pf01/rendererImg.do"
SOURCE_HTML_SHA256="31c9afa4e92d68b6ec728758c20ca4cd0787c91a5690cbcd222bf8febdd13374"
OFFICIAL_JS_SHA256="b2b4aaabf3da440b84b64f25768965a6c2c5500775b53e7634e98e4f59adf087"
PAGE_IDS=("048a","085a")
CAP=1_750_000
ATTEMPTS=2
FIELDS=("item_cd","book_cd","vol_no","page_no","imgFileNm","tbl_conts_seq","mokNm","add_page_no")

class ProviderOnly(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,url):
  p=urllib.parse.urlsplit(url)
  if (p.scheme,p.hostname)!=("https","kyudb.snu.ac.kr"):
   raise urllib.error.HTTPError(url,code,"OUTSIDE_PROVIDER",headers,fp)
  return super().redirect_request(req,fp,code,msg,headers,url)

def payload_for(page):
 if page not in PAGE_IDS:raise ValueError("not emitted by authenticated firstparty digital TOC")
 return {"item_cd":"GJB","book_cd":"GK05554_00","vol_no":"0018","page_no":page,
         "imgFileNm":"","tbl_conts_seq":"","mokNm":"","add_page_no":""}

class LiteralLinks(html.parser.HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  if tag not in ("img","iframe","script","a","source","embed","form","link"):return
  d=dict(attrs)
  bits={k:v[:320] for k,v in d.items() if k in ("src","href","action","data-src","data-original") and isinstance(v,str)}
  if bits and len(self.links)<100:self.links.append({"tag":tag,"literal_attributes":bits})

def analyze(raw,content_type):
 media=(content_type or "").split(";",1)[0].strip().lower()
 result={"raw_bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"media_type":media,
         "original_ancient_folio_verified":False,"physical_copy_bound":False,
         "independent_historical_witness_votes":0,"algorithm_reopens":0}
 if "html" not in media and not raw.lstrip().lower().startswith((b"<html",b"<!doctype html")):
  result["status"]="NON_HTML_RESPONSE_NOT_INTERPRETED"
  return result
 text=raw.decode("utf-8","replace")
 parser=LiteralLinks();parser.feed(text)
 result["status"]="VIEWER_HTML_ONLY"
 result["literal_links"]=parser.links
 markers=("/pf01/","/imgviewer/","page_no","imgFileNm","image","renderer","jpg","png","iiif")
 result["bounded_source_windows"]=[]
 for m in markers:
  at=text.lower().find(m.lower())
  if at>=0:result["bounded_source_windows"].append({"marker":m,"offset":at,"window":text[max(0,at-140):at+460]})
 return result

def firstparty_url(url):
 p=urllib.parse.urlsplit(url)
 return (p.scheme,p.hostname)==("https","kyudb.snu.ac.kr")

def request(opener,page,out):
 data=urllib.parse.urlencode(payload_for(page)).encode("ascii")
 record={"page":page,"posted_form_fields":list(FIELDS),"request_method":"POST","endpoint":ENDPOINT,
         "status":"NOT_ACQUIRED","attempt_log":[],"original_image_get_requested":False,
         "official_js_sha256":OFFICIAL_JS_SHA256,"source_html_sha256":SOURCE_HTML_SHA256}
 for n in range(1,ATTEMPTS+1):
  req=urllib.request.Request(ENDPOINT,data=data,
   headers={"Referer":REFERER,"Origin":BASE,"Accept":"text/html,application/xhtml+xml,*/*;q=0.7",
            "User-Agent":"Tianwen-13JE-Exact-SNU-Viewer-POST/1.0"})
  try:
   with opener.open(req,timeout=20) as response:
    record["http"]=response.status
    record["final_url"]=response.geturl()
    if not firstparty_url(record["final_url"]):record["status"]="UNTRUSTED_REDIRECT"
    else:
     raw=response.read(CAP+1)
     if len(raw)>CAP:record["status"]="OVERSIZED"
     elif not raw:record["status"]="EMPTY"
     else:
      record["detail"]=analyze(raw,response.headers.get("Content-Type",""))
      if record["detail"]["status"]=="VIEWER_HTML_ONLY":
       (out/("viewer-"+page+".html")).write_bytes(raw)
      record["status"]=record["detail"]["status"]
    record["attempt_log"].append({"n":n,"status":record["status"],"http":record["http"]})
    break
  except urllib.error.HTTPError as exc:
   record["status"]="HTTP_ERROR";record["http"]=exc.code
   retry=exc.code in (429,502,503,504) and n<ATTEMPTS
   record["attempt_log"].append({"n":n,"status":"HTTP_ERROR","http":exc.code,"retry":retry})
   if not retry:break
  except urllib.error.URLError as exc:
   record["status"]="TRANSPORT_ERROR";record["error_type"]="URLError"
   record["attempt_log"].append({"n":n,"status":"TRANSPORT_ERROR","retry":n<ATTEMPTS})
   if n>=ATTEMPTS:break
  except Exception as exc:
   record["status"]="TRANSPORT_ERROR";record["error_type"]=type(exc).__name__
   record["attempt_log"].append({"n":n,"status":"TRANSPORT_ERROR","retry":False})
   break
  time.sleep(n)
 return record

def main():
 out=Path(os.environ.get("TIANWEN_13JE_OUT","/tmp/tianwen-13je"));out.mkdir(parents=True,exist_ok=True)
 cookiejar=http.cookiejar.CookieJar()
 opener=urllib.request.build_opener(ProviderOnly(),urllib.request.HTTPCookieProcessor(cookiejar))
 preflight={"url":REFERER,"status":"NOT_ACQUIRED"}
 try:
  with opener.open(urllib.request.Request(REFERER,headers={"User-Agent":"Tianwen-13JE-Exact-SNU-Viewer-POST/1.0"}),timeout=20) as r:
   preflight["http"]=r.status;preflight["final_url"]=r.geturl()
   preflight["status"]="FIRSTPARTY_COOKIE_PREFLIGHT" if firstparty_url(r.geturl()) else "UNTRUSTED_REDIRECT"
 except urllib.error.HTTPError as e:preflight.update({"status":"HTTP_ERROR","http":e.code})
 except Exception as e:preflight.update({"status":"TRANSPORT_ERROR","error_type":type(e).__name__})
 results=[request(opener,p,out) for p in PAGE_IDS]
 report={"schema":"TIANWEN_13JE_SNU_SOURCE_EMITTED_RENDERER_POST_R1",
         "firstparty_preflight":preflight,"pages":results,"original_folio_claim":False,
         "image_bytes_acquired":False,"historical_source_votes":0,"algorithm_reopens":0}
 (out/"viewer-post-evidence-boundary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(report,ensure_ascii=False))
 print("VIEWER_POST_IS_NOT_VERIFIED_ORIGINAL_FOLIO")
if __name__=="__main__":main()
