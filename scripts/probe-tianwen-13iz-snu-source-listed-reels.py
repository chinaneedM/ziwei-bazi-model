#!/usr/bin/env python3
"""13IZ: firstparty SNU GK05553/GK05554 source-listed microfilm route boundary.

Only fetch the exact official book pages and call the official source-listed
mfPdfList endpoint if the page names the book in its own control.
Do not guess a volume number, request a page image, or interpret an M/F reel
as a specific physical fascicle.
"""
import hashlib,json,os,re,urllib.error,urllib.parse,urllib.request
from pathlib import Path
BASE="https://kyudb.snu.ac.kr"
BOOKS=("GK05553_00","GK05554_00")
PDF_ENDPOINT="/ajax/book/mfPdfList.do"
LIMIT=1_700_000
class OfficialOnly(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,h,url):
  p=urllib.parse.urlsplit(url)
  if p.scheme!="https" or p.hostname!="kyudb.snu.ac.kr":
   raise urllib.error.HTTPError(url,code,"CROSS_PROVIDER_REDIRECT",h,fp)
  return super().redirect_request(req,fp,code,msg,h,url)
def read(url,post=None,timeout=22):
 data=urllib.parse.urlencode(post).encode() if post is not None else None
 req=urllib.request.Request(url,data=data,headers={"User-Agent":"Tianwen-13IZ-Public-Bibliography-Control/1.0","Accept":"text/html,application/json,application/xhtml+xml,*/*;q=0.8"})
 try:
  with urllib.request.build_opener(OfficialOnly()).open(req,timeout=timeout) as r:
   u=urllib.parse.urlsplit(r.geturl())
   if u.scheme!="https" or u.hostname!="kyudb.snu.ac.kr":return {"status":"FINAL_URL_UNTRUSTED"},None
   body=r.read(LIMIT+1)
   if len(body)>LIMIT:return {"status":"OVERSIZE","bytes":len(body),"http":r.status},None
   return {"status":"CAPTURED","http":r.status,"bytes":len(body),"sha256":hashlib.sha256(body).hexdigest(),"final_url":r.geturl()},body
 except urllib.error.HTTPError as e:return {"status":"HTTP_ERROR","http":e.code},None
 except Exception as e:return {"status":"TRANSPORT_ERROR","error_type":type(e).__name__},None
def summarize(book,html):
 t=html.decode("utf-8","replace")
 marker="fn_mfPdfPopShow('"+book+"')"
 return {"own_book_marker":book in t,"exact_provider_microfilm_button":marker in t,"provider_mfPdfList_literal":PDF_ENDPOINT in t,
         "reel_labels":sorted(set(re.findall(r'M/F74-102-17-[1-7](?:\s*\([^)]{0,90}\))?',t))),
         "source_named_volumes":sorted(set(re.findall(r'v\.?[0-9]{1,2}(?:[-–][0-9]{1,2})?',t)))[:40],
         "physical_book12_original_folio_proven":False,"physical_book29_original_folio_proven":False}
def parse_volumes(body,book):
 try:j=json.loads(body)
 except Exception:return {"status":"NON_JSON","volList_count":None,"volumes":[]}
 rows=j.get("volList") if isinstance(j,dict) else None
 if not isinstance(rows,list):return {"status":"NO_VOLLIST","result_literal":str(j.get("RESULT"))[:150] if isinstance(j,dict) else None,"volList_count":None,"volumes":[]}
 result=[]
 for row in rows[:100]:
  if isinstance(row,dict):
   result.append({k:row.get(k) for k in ("BOOK_CD","VOL_NO","ITEM_CD","IS_PDF","VOL_NM","VOL_TITLE","FILE_NM") if k in row})
 verified=all(isinstance(x,dict) and x.get("BOOK_CD")==book for x in rows)
 return {"status":"PROVIDER_LIST_BOUND" if verified else "UNTRUSTED_OR_MIXED_OBJECT","result_literal":str(j.get("RESULT"))[:150],"volList_count":len(rows),"volumes":result,"no_folio_to_reel_crosswalk":True}
def probe(book,folder):
 catalog_url=BASE+"/book/view.do?"+urllib.parse.urlencode({"book_cd":book})
 req,raw=read(catalog_url)
 result={"book":book,"catalog_url":catalog_url,"catalog":req,"source_emitted":None,"microfilm":None,"image_download_attempted":False,"original_folio_verified":False,"historical_number_awarded":False}
 if raw is None:return result
 (folder/(book+"-catalog.html")).write_bytes(raw)
 s=summarize(book,raw);result["source_emitted"]=s
 # Two source-identity gates and a documented prior firstparty endpoint are required.
 if not(s["own_book_marker"] and (s["exact_provider_microfilm_button"] or s["provider_mfPdfList_literal"])):
  result["microfilm"]={"status":"NO_EXACT_PROVIDER_CONTROL_NO_POST"};return result
 p,body=read(BASE+PDF_ENDPOINT,{"book_cd":book})
 result["microfilm"]={"request":p}
 if body is not None:
  (folder/(book+"-provider-volumes.json")).write_bytes(body)
  result["microfilm"]["parsed"]=parse_volumes(body,book)
 return result
def main():
 out=Path(os.environ.get("TIANWEN_13IZ_OUT","/tmp/tianwen-13iz-snu"));out.mkdir(parents=True,exist_ok=True)
 data={"schema":"TIANWEN_13IZ_SNU_GK5553_GK5554_SOURCE_LISTED_REEL_ROUTE_R1","books":[probe(b,out) for b in BOOKS],
       "claims":{"original_physical_books12_and29_acquired":False,"individual_gk5554_books17_18_juan81_82_bound":False,"reels_are_independent_witnesses":False,"algorithms_changed":False}}
 (out/"firstparty-reel-boundary.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"results":[{"book":b["book"],"catalog_status":b["catalog"]["status"],"controls":b["source_emitted"],"microfilm":b["microfilm"]} for b in data["books"]],"historical_original_folio_votes":0},ensure_ascii=False))
if __name__=="__main__":main()
