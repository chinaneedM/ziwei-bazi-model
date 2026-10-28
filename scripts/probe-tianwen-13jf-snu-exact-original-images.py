#!/usr/bin/env python3
"""13JF: acquire ONLY two exact photo URLs emitted by the firstparty 13JE viewer.

Source origin: 13JE run40639358829 artifact12795210294: POST /pf01/rendererImg.do
from official 13JD JS. Exact provider-emitted ImageServlet src for digital
GK05554 volume0018 page048a and page085a. A JPEG is not automatically a
physical copy, historical edition, readable heading or glyph.
"""
import hashlib,http.cookiejar,json,os,time,urllib.error,urllib.parse,urllib.request
from pathlib import Path

BASE="https://kyudb.snu.ac.kr"
SOURCE_HTML={
 "048a":{"viewer_sha256":"d7422a70e9218471279826e7ad3360b46f3eeae9cd65a71908b9ef9e7eef0c4e",
         "source_emitted_src":"/ImageServlet.do?imgFileNm=GK05554_00_IL_0018_048a.jpg&path=/data01/stream/GJB/IMG/GK05554_00/GK05554_00_0018/GK05554_00_IL_0018_048a.jpg"},
 "085a":{"viewer_sha256":"44babd776b2e59cb6c1ce93f22b47c1d9e47c677967392f654a6e16669cd6c23",
         "source_emitted_src":"/ImageServlet.do?imgFileNm=GK05554_00_IL_0018_085a.jpg&path=/data01/stream/GJB/IMG/GK05554_00/GK05554_00_0018/GK05554_00_IL_0018_085a.jpg"}}
MAX_BYTES=24_000_000
ATTEMPTS=3
VIEWER_REFERER=BASE+"/pf01/rendererImg.do"

class FirstpartyOnly(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,url):
  p=urllib.parse.urlsplit(url)
  if (p.scheme,p.hostname)!=("https","kyudb.snu.ac.kr"):
   raise urllib.error.HTTPError(url,code,"OUTSIDE_PROVIDER",headers,fp)
  return super().redirect_request(req,fp,code,msg,headers,url)

def exact_image_url(page):
 if page not in SOURCE_HTML:raise ValueError("page was not observed in source-bound official viewer")
 return BASE+SOURCE_HTML[page]["source_emitted_src"]

def validate_jpeg(raw,media):
 media=(media or "").split(";",1)[0].strip().lower()
 if media not in ("image/jpeg","image/pjpeg","application/octet-stream"):
  return "NON_JPEG_CONTENT_TYPE"
 if len(raw)<100 or not raw.startswith(b"\xff\xd8\xff") or not raw.endswith(b"\xff\xd9"):
  return "INVALID_JPEG_BYTES"
 return "JPEG_BYTES_ACQUIRED_UNCOLLATED"

def read_original(page,opener,out):
 url=exact_image_url(page)
 d={"page_no":page,"digital_book":"GK05554_00","digital_vol":"0018",
    "source_viewer_html_sha256":SOURCE_HTML[page]["viewer_sha256"],
    "source_viewer_artifact":12795210294,"source_image_url":url,
    "status":"NOT_ACQUIRED","attempts":[],"historical_glyph_verified":False,
    "impression_year_verified":False,"physical_copy_identity_verified":False,
    "independent_physical_witness_votes":0,"algorithm_reopens":0}
 for n in range(1,ATTEMPTS+1):
  req=urllib.request.Request(url,headers={"User-Agent":"Tianwen-13JF-Source-Emitted-SNU-Images/1.0",
            "Accept":"image/jpeg,image/*;q=0.7","Referer":VIEWER_REFERER})
  try:
   with opener.open(req,timeout=30) as r:
    d["http"]=r.status
    actual=urllib.parse.urlsplit(r.geturl())
    if (actual.scheme,actual.hostname)!=("https","kyudb.snu.ac.kr"):
     d["status"]="UNTRUSTED_REDIRECT"
    else:
     raw=r.read(MAX_BYTES+1)
     if len(raw)>MAX_BYTES:d["status"]="OVERSIZED"
     elif r.status!=200:d["status"]="UNEXPECTED_HTTP_STATUS"
     else:
      d["content_type"]=r.headers.get("Content-Type","").split(";",1)[0].strip().lower()
      d["status"]=validate_jpeg(raw,d["content_type"])
      if d["status"]=="JPEG_BYTES_ACQUIRED_UNCOLLATED":
       d["raw_bytes"]=len(raw)
       d["sha256"]=hashlib.sha256(raw).hexdigest()
       (out/("gk5554-vol18-"+page+"-source-original.jpg")).write_bytes(raw)
    d["attempts"].append({"n":n,"status":d["status"],"http":d.get("http")})
    break
  except urllib.error.HTTPError as e:
   retry=e.code in (429,502,503,504) and n<ATTEMPTS
   d["status"]="HTTP_ERROR";d["http"]=e.code
   d["attempts"].append({"n":n,"status":"HTTP_ERROR","http":e.code,"retry":retry})
   if not retry:break
  except urllib.error.URLError as e:
   d["status"]="TRANSPORT_ERROR";d["error_type"]="URLError"
   d["attempts"].append({"n":n,"status":"TRANSPORT_ERROR","retry":n<ATTEMPTS})
   if n>=ATTEMPTS:break
  except Exception as e:
   d["status"]="TRANSPORT_ERROR";d["error_type"]=type(e).__name__
   d["attempts"].append({"n":n,"status":"TRANSPORT_ERROR","retry":False})
   break
  time.sleep(n)
 return d

def main():
 out=Path(os.environ.get("TIANWEN_13JF_OUT","/tmp/tianwen-13jf"));out.mkdir(parents=True,exist_ok=True)
 opener=urllib.request.build_opener(FirstpartyOnly(),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
 results=[read_original(p,opener,out) for p in ("048a","085a")]
 report={"schema":"TIANWEN_13JF_SNU_EXACT_VIEWER_IMAGE_BYTES_R1","source_run":40639358829,
    "source_artifact":12795210294,"pages":results,"original_page_glyphs_manually_collated":False,
    "physical_edition_verified":False,"historical_numerical_vote":0,"algorithm_reopens":0}
 (out/"source-image-intake.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(report,ensure_ascii=False))
 print("JPEG_ACQUISITION_IS_NOT_PRINTED_HEADING_GLYPH_COLLATION")
if __name__=="__main__":main()
