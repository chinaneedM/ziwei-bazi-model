#!/usr/bin/env python3
"""13JC: source-emitted SNU firstparty bookSearch.js fn_originalImg contract.

Read only the official script referenced literally by the 13JA saved
GK05554_00 vol0018 HTML. Never guess or call an image URI.
"""
import hashlib,json,os,re,time,urllib.error,urllib.parse,urllib.request
from pathlib import Path
URL="https://kyudb.snu.ac.kr/js/book/bookSearch.js"
MAX=1_000_000
MAX_ATTEMPTS=3
RETRY_HTTP={429,502,503,504}
MARKERS=("fn_originalImg","imgViewer","originalImg","vol_no","page_no","item_cd","book_cd")

def accepts_script_payload(media,data):
 """Do not promote an HTML error page or unknown binary to verified JS."""
 media=(media or "").split(";",1)[0].strip().lower()
 if media not in {"text/javascript","application/javascript","application/x-javascript","text/plain"}:return False
 prefix=data.lstrip()[:100].lower()
 return bool(data.strip()) and not prefix.startswith((b"<html",b"<!doctype",b"<?xml",b"<head"))
def transport_category(reason):
 text=str(reason).lower()
 if "timed out" in text or "timeout" in text:return "TIMEOUT"
 if "certificate" in text or "ssl" in text:return "TLS"
 if "name resolution" in text or "name or service" in text or "nodename" in text:return "DNS"
 if "proxy" in text:return "PROXY"
 if "connection refused" in text:return "CONNECTION_REFUSED"
 return "OTHER_TRANSPORT"

class StrictProvider(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,url):
  p=urllib.parse.urlsplit(url)
  if p.scheme!="https" or p.hostname!="kyudb.snu.ac.kr":
   raise urllib.error.HTTPError(url,code,"NOT_SOURCE_PROVIDER",headers,fp)
  return super().redirect_request(req,fp,code,msg,headers,url)
def inspect(data):
 t=data.decode("utf-8","replace")
 blocks=[]
 for name in MARKERS:
  match=re.search(re.escape(name),t,re.I)
  if match:
   off=match.start()
   blocks.append({"marker":name,"offset":off,"source_window":t[max(0,off-180):off+1050]})
 defined=re.search(r"function\s+fn_originalImg\s*\([^)]*\)",t)
 return {"raw_bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),
   "function_definition_observed":bool(defined),
   "function_signature":defined.group(0) if defined else None,
   "literal_bounded_windows":blocks,
   "printed_folio_content_acquired":False,"new_physical_witness_votes":0}
def main():
 out=Path(os.environ.get("TIANWEN_13JC_OUT","/tmp/tianwen-13jc"));out.mkdir(parents=True,exist_ok=True)
 result={"schema":"TIANWEN_13JC_SOURCE_EMITTED_SNU_BOOKSEARCH_JS_R1","url":URL,
         "status":"NOT_ACQUIRED","http":None,"detail":None,"original_image_downloaded":False}
 req=urllib.request.Request(URL,headers={"User-Agent":"Tianwen-13JC-SNU-Official-JS-Only/1.1","Accept":"text/javascript,application/javascript,*/*;q=0.7"})
 result["attempt_log"]=[]
 opener=urllib.request.build_opener(StrictProvider())
 for attempt in range(1,MAX_ATTEMPTS+1):
  try:
   with opener.open(req,timeout=18) as resp:
    p=urllib.parse.urlsplit(resp.geturl())
    if p.scheme!="https" or p.hostname!="kyudb.snu.ac.kr":
     result["status"]="UNTRUSTED_REDIRECT"
    else:
     data=resp.read(MAX+1)
     result["http"]=resp.status
     media=resp.headers.get("Content-Type","").split(";",1)[0].strip().lower()
     result["response_media_type"]=media
     if resp.status!=200:result["status"]="UNEXPECTED_HTTP_STATUS"
     elif len(data)>MAX:result["status"]="OVERSIZED"
     elif not data.strip():result["status"]="EMPTY"
     elif not accepts_script_payload(media,data):result["status"]="NOT_JAVASCRIPT_PAYLOAD"
     else:
      (out/"official-bookSearch.js").write_bytes(data)
      result["detail"]=inspect(data)
      result["status"]="OFFICIAL_JS_ACQUIRED"
    result["attempt_log"].append({"attempt":attempt,"status":result["status"],"http":result["http"]})
    break
  except urllib.error.HTTPError as ex:
   retry=ex.code in RETRY_HTTP and attempt<MAX_ATTEMPTS
   result["http"]=ex.code
   result["status"]="HTTP_ERROR"
   result["attempt_log"].append({"attempt":attempt,"status":"HTTP_ERROR","http":ex.code,"retry":retry})
   if not retry:break
  except urllib.error.URLError as ex:
   category=transport_category(getattr(ex,"reason",None))
   result["status"]="TRANSPORT_ERROR"
   result["exception_type"]="URLError"
   result["transport_category"]=category
   result["attempt_log"].append({"attempt":attempt,"status":"TRANSPORT_ERROR","category":category,"retry":attempt<MAX_ATTEMPTS})
   if attempt>=MAX_ATTEMPTS:break
  except Exception as ex:
   result["status"]="TRANSPORT_ERROR"
   result["exception_type"]=type(ex).__name__
   result["attempt_log"].append({"attempt":attempt,"status":"TRANSPORT_ERROR","exception_type":type(ex).__name__,"retry":False})
   break
  time.sleep(attempt)
 (out/"official-js-contract.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(result,ensure_ascii=False))
 print("NO_ANCIENT_ORIGINAL_IMAGE_OR_ALGORITHM_CHANGE")
if __name__=="__main__":main()
