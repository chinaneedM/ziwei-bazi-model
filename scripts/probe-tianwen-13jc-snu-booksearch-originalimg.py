#!/usr/bin/env python3
"""13JC: source-emitted SNU firstparty bookSearch.js fn_originalImg contract.

Read only the official script referenced literally by the 13JA saved
GK05554_00 vol0018 HTML. Never guess or call an image URI.
"""
import hashlib,json,os,re,urllib.error,urllib.parse,urllib.request
from pathlib import Path
URL="https://kyudb.snu.ac.kr/js/book/bookSearch.js"
MAX=1_000_000
MARKERS=("fn_originalImg","imgViewer","originalImg","vol_no","page_no","item_cd","book_cd")
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
 req=urllib.request.Request(URL,headers={"User-Agent":"Tianwen-13JC-SNU-Official-JS-Only/1.0","Accept":"text/javascript,application/javascript,*/*;q=0.7"})
 try:
  with urllib.request.build_opener(StrictProvider()).open(req,timeout=26) as resp:
   p=urllib.parse.urlsplit(resp.geturl())
   if p.scheme!="https" or p.hostname!="kyudb.snu.ac.kr":result["status"]="UNTRUSTED_REDIRECT"
   else:
    data=resp.read(MAX+1);result["http"]=resp.status
    if len(data)>MAX:result["status"]="OVERSIZED"
    elif not data.strip():result["status"]="EMPTY"
    else:
     (out/"official-bookSearch.js").write_bytes(data)
     result["detail"]=inspect(data)
     result["status"]="OFFICIAL_JS_ACQUIRED"
 except urllib.error.HTTPError as ex:result["http"]=ex.code;result["status"]="HTTP_ERROR"
 except Exception as ex:result["status"]="TRANSPORT_ERROR";result["exception_type"]=type(ex).__name__
 (out/"official-js-contract.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(result,ensure_ascii=False))
 print("NO_ANCIENT_ORIGINAL_IMAGE_OR_ALGORITHM_CHANGE")
if __name__=="__main__":main()
