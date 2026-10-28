#!/usr/bin/env python3
"""13JA: SNU original image viewer routes only from provider-listed GK05554 volumes.

Use the official image-viewer template seen in SNU's own public help/incident
page, but never guess a vol_no, printed juan, folio or image page. The selected
0017 and 0018 are provider-list child IDs from the exact verified 13IZ result,
not evidence those are physical ancient book ordinals.
"""
import hashlib,json,os,re,urllib.error,urllib.parse,urllib.request
from pathlib import Path
BASE="https://kyudb.snu.ac.kr"
BOOK="GK05554_00";ITEM="GJB"
PROVIDER_LISTED=("0017","0018")
PAGE="/book/text.do"
LIMIT=2_000_000
KEYS=("viewImgList","rendererImg","imgViewer","imageViewer","viewImg","book_cd","vol_no","page_no","GJB","GK05554_00")
class OnlyOfficial(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,url):
  p=urllib.parse.urlsplit(url)
  if p.scheme!="https" or p.hostname!="kyudb.snu.ac.kr":
   raise urllib.error.HTTPError(url,code,"CROSS_PROVIDER_REDIRECT",headers,fp)
  return super().redirect_request(req,fp,code,msg,headers,url)
def audit_html(body,vol):
 s=body.decode("utf-8","replace")
 phrases={k:len(list(re.finditer(re.escape(k),s,re.I))) for k in KEYS}
 return {"book_id_in_response":BOOK in s,"provider_volume_token_in_response":vol in s,
         "url_marker_counts":phrases,"original_ancient_folio_captured":False,
         "printed_juan81_or_82_bound":False,"physical_book17_or_18_identity_bound":False,
         "image_url_fingerprints":[]}
def get(vol):
 if vol not in PROVIDER_LISTED:raise ValueError("Not a source-listed child")
 url=BASE+PAGE+"?"+urllib.parse.urlencode({"item_cd":ITEM,"book_cd":BOOK,"vol_no":vol})
 r={"url":url,"book_cd":BOOK,"provider_vol_no":vol,"result":"NOT_REQUESTED","http":None}
 req=urllib.request.Request(url,headers={"Accept":"text/html,application/xhtml+xml","User-Agent":"Tianwen-13JA-SourceBound-Viewer-Discovery/1.0"})
 try:
  with urllib.request.build_opener(OnlyOfficial()).open(req,timeout=28) as res:
   dest=urllib.parse.urlsplit(res.geturl())
   if dest.scheme!="https" or dest.hostname!="kyudb.snu.ac.kr":r["result"]="UNTRUSTED_FINAL_URL";return r,None
   b=res.read(LIMIT+1);r["http"]=res.status;r["bytes"]=len(b)
   if len(b)>LIMIT:r["result"]="OVERSIZED";return r,None
   r["sha256"]=hashlib.sha256(b).hexdigest()
   if not b.lstrip().lower().startswith((b"<!doctype html",b"<html")):
    r["result"]="NON_HTML_RESPONSE";return r,b
   r["result"]="OFFICIAL_VIEWER_HTML_RECEIVED"
   r["markers"]=audit_html(b,vol)
   return r,b
 except urllib.error.HTTPError as e:r["http"]=e.code;r["result"]="HTTP_ERROR"
 except Exception as e:r["result"]="TRANSPORT_ERROR";r["exception_type"]=type(e).__name__
 return r,None
def main():
 out=Path(os.environ.get("TIANWEN_13JA_OUT","/tmp/tianwen-13ja-snu"));out.mkdir(parents=True,exist_ok=True)
 records=[]
 for vol in PROVIDER_LISTED:
  data,body=get(vol);records.append(data)
  if body is not None:(out/("gk5554-"+vol+"-viewer.response")).write_bytes(body)
 report={"schema":"TIANWEN_13JA_SOURCE_LISTED_GK5554_VIEWER_BOUNDARY_R1",
         "from_prior_firstparty_13iz_response_sha256":"af2c8082894765fa9752121b2ff29894f1c0d8848637f4d99817186226d97410",
         "official_public_template":"https://kyudb.snu.ac.kr/book/text.do?item_cd=GJB&book_cd=...&vol_no=...",
         "records":records,"ancient_original_glyph_votes":0,"new_ancient_physical_pages":0,
         "roman_book_numbers_as_ancient_folio_authority":False}
 (out/"viewer-boundary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"records":records,"ancient_folio":False},ensure_ascii=False))
if __name__=="__main__":main()
