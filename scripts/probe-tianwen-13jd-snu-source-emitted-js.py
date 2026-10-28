#!/usr/bin/env python3
"""13JD: fetch only three JavaScripts literally emitted by archived SNU GK05554 vol0018 HTML.

The firstparty HTML source is SHA256 31c9...74; the 13JC bookSearch.js is SHA256
a156...032 but does not define fn_originalImg. This script discovers a function,
NOT an image, a printed folio, or an ancient edition. No image URL is constructed.
"""
import hashlib, json, os, re, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

BASE="https://kyudb.snu.ac.kr"
SOURCE_HTML_SHA256="31c9afa4e92d68b6ec728758c20ca4cd0787c91a5690cbcd222bf8febdd13374"
SOURCE_HTML_ARTIFACT=12792862189
SOURCE_EMITTED_SCRIPTS=("/js/common.js","/js/common2.js","/js/ux.js")
BYTE_CAP=750_000
MAX_ATTEMPTS=3

class FirstpartyOnly(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,url):
  parsed=urllib.parse.urlsplit(url)
  if (parsed.scheme,parsed.hostname)!=("https","kyudb.snu.ac.kr"):
   raise urllib.error.HTTPError(url,code,"OUTSIDE_FIRSTPARTY",headers,fp)
  return super().redirect_request(req,fp,code,msg,headers,url)

def script_url(path):
 if path not in SOURCE_EMITTED_SCRIPTS:
  raise ValueError("not source-emitted in the archived vol0018 HTML")
 return BASE+path

def classify_payload(content_type,data):
 media=(content_type or "").split(";",1)[0].strip().lower()
 if media not in ("application/javascript","application/x-javascript","text/javascript","text/plain"):
  return "UNEXPECTED_MEDIA_TYPE"
 if not data.strip():return "EMPTY"
 if data.lstrip()[:100].lower().startswith((b"<html",b"<!doctype",b"<?xml",b"<head")):
  return "HTML_NOT_SCRIPT"
 return "SCRIPT"

def analyze(data):
 txt=data.decode("utf-8","replace")
 without_blocks=re.sub(r"/\*.*?\*/","",txt,flags=re.S)
 clean="\n".join(line for line in without_blocks.splitlines() if not line.lstrip().startswith("//"))
 patterns=(
  r"\bfunction\s+fn_originalImg\s*\([^)]*\)",
  r"\b(?:window\.)?fn_originalImg\s*=\s*function\s*\([^)]*\)",
  r"\b(?:var|let|const)\s+fn_originalImg\s*=\s*(?:function\s*\([^)]*\)|\([^)]*\)\s*=>)"
 )
 hits=[m.group(0) for pattern in patterns for m in re.finditer(pattern,clean)]
 raw_hits=list(re.finditer(r"\bfn_originalImg\b",txt))
 return {"raw_bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),
         "function_definition_observed":bool(hits),"definition_signatures":hits[:8],
         "literal_source_windows":[txt[max(0,m.start()-220):m.start()+1500] for m in raw_hits[:5]],
         "printed_folio_acquired":False,"original_image_bytes":None,
         "independent_physical_witness_votes":0,"algorithm_reopens":0}

def failure_category(reason):
 s=str(reason).lower()
 if "timed out" in s or "timeout" in s:return "TIMEOUT"
 if "certificate" in s or "ssl" in s:return "TLS"
 if "name resolution" in s or "name or service" in s:return "DNS"
 if "proxy" in s:return "PROXY"
 return "OTHER_TRANSPORT"

def probe(path,out,opener=None):
 url=script_url(path)
 opener=opener or urllib.request.build_opener(FirstpartyOnly())
 record={"source_path":path,"url":url,"status":"NOT_ACQUIRED","attempts":[],
         "source_html_sha256":SOURCE_HTML_SHA256,"source_html_artifact":SOURCE_HTML_ARTIFACT,
         "image_requested":False,"historical_glyph_votes":0,"algorithm_reopens":0}
 req=urllib.request.Request(url,headers={"User-Agent":"Tianwen-13JD-Archived-SNU-Script-Only/1.0","Accept":"text/javascript,application/javascript,*/*;q=0.7"})
 for n in range(1,MAX_ATTEMPTS+1):
  try:
   with opener.open(req,timeout=15) as resp:
    final=urllib.parse.urlsplit(resp.geturl())
    if (final.scheme,final.hostname)!=("https","kyudb.snu.ac.kr"):
     record["status"]="UNTRUSTED_REDIRECT"
    else:
     raw=resp.read(BYTE_CAP+1)
     record["http"]=resp.status
     if len(raw)>BYTE_CAP:record["status"]="OVERSIZED"
     elif resp.status!=200:record["status"]="UNEXPECTED_HTTP_STATUS"
     else:
      media=resp.headers.get("Content-Type","")
      record["media_type"]=media.split(";",1)[0].strip().lower()
      check=classify_payload(media,raw)
      if check!="SCRIPT":record["status"]=check
      else:
       (out/("snu-"+path.rsplit("/",1)[-1])).write_bytes(raw)
       record["detail"]=analyze(raw)
       record["status"]="OFFICIAL_SCRIPT_CAPTURED"
    record["attempts"].append({"n":n,"status":record["status"],"http":record.get("http")})
    break
  except urllib.error.HTTPError as ex:
   retry=ex.code in (429,502,503,504) and n<MAX_ATTEMPTS
   record["status"]="HTTP_ERROR";record["http"]=ex.code
   record["attempts"].append({"n":n,"status":"HTTP_ERROR","http":ex.code,"retry":retry})
   if not retry:break
  except urllib.error.URLError as ex:
   category=failure_category(getattr(ex,"reason",None))
   record["status"]="TRANSPORT_ERROR"
   record["attempts"].append({"n":n,"status":"TRANSPORT_ERROR","category":category,"retry":n<MAX_ATTEMPTS})
   if n>=MAX_ATTEMPTS:break
  except Exception as ex:
   record["status"]="TRANSPORT_ERROR"
   record["attempts"].append({"n":n,"status":"TRANSPORT_ERROR","error_type":type(ex).__name__,"retry":False})
   break
  time.sleep(n)
 return record

def main():
 out=Path(os.environ.get("TIANWEN_13JD_OUT","/tmp/tianwen-13jd"));out.mkdir(parents=True,exist_ok=True)
 items=[]
 for p in SOURCE_EMITTED_SCRIPTS:
  record=probe(p,out);items.append(record)
  print(json.dumps(record,ensure_ascii=False))
 result={"schema":"TIANWEN_13JD_SNU_SOURCE_EMITTED_SCRIPT_FUNCTION_SEARCH_R1",
         "source_html_sha256":SOURCE_HTML_SHA256,"source_html_artifact":SOURCE_HTML_ARTIFACT,
         "scripts":items,"ancient_original_image_acquired":False,"historical_witness_votes":0}
 (out/"script-contracts.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("SOURCE_JS_NOT_ORIGINAL_FOLIO_NO_ALGORITHM_REOPEN")
if __name__=="__main__":main()
