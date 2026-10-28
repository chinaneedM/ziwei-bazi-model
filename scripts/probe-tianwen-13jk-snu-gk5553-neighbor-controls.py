#!/usr/bin/env python3
"""13JK: SNU GK05553 own firstparty catalog -> official volList -> named viewer.

Do not equate DIGITAL VOL_NO=0012/0029 with physical ancient book ordinals.
Do not guess URLs or pages absent in firstparty response. No image GET, no
historical glyph adjudication, and no source-registry/algorithm changes.
"""
import hashlib,html.parser,json,os,re,time,urllib.error,urllib.parse,urllib.request
from pathlib import Path
BASE="https://kyudb.snu.ac.kr"
BOOK="GK05553_00"
CATALOG=BASE+"/book/view.do?book_cd="+BOOK
VOLS=BASE+"/ajax/book/mfPdfList.do"
VIEWER=BASE+"/book/text.do"
TARGET_VOL_TOKENS=("0008","0026","0011","0013","0025","0027")
MAX_BYTES=2_000_000
MAX_ATTEMPTS=3

class OfficialOnly(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,url):
  p=urllib.parse.urlsplit(url)
  if (p.scheme,p.hostname)!=("https","kyudb.snu.ac.kr"):
   raise urllib.error.HTTPError(url,code,"CROSS_PROVIDER",headers,fp)
  return super().redirect_request(req,fp,code,msg,headers,url)

def get(opener,url,form=None):
 result={"url":url,"method":"POST" if form is not None else "GET","status":"UNAVAILABLE","attempts":[]}
 data=urllib.parse.urlencode(form).encode("ascii") if form is not None else None
 for n in range(1,MAX_ATTEMPTS+1):
  req=urllib.request.Request(url,data=data,headers={"User-Agent":"Tianwen-13JK-SNU-Official-CopyScope/1.0","Accept":"text/html,application/json,*/*;q=0.7",
   "Referer":CATALOG})
  try:
   with opener.open(req,timeout=20) as resp:
    p=urllib.parse.urlsplit(resp.geturl())
    if (p.scheme,p.hostname)!=("https","kyudb.snu.ac.kr"):
     result["status"]="UNTRUSTED_REDIRECT";return result,None
    raw=resp.read(MAX_BYTES+1)
    result["http"]=resp.status
    result["content_type"]=resp.headers.get("Content-Type","").split(";",1)[0].strip().lower()
    if len(raw)>MAX_BYTES:result["status"]="OVERSIZED";return result,None
    if not raw:result["status"]="EMPTY";return result,None
    result.update({"status":"FIRSTPARTY_BYTES","bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()})
    return result,raw
  except urllib.error.HTTPError as e:
   transient=e.code in (429,502,503,504) and n<MAX_ATTEMPTS
   result["status"]="HTTP_ERROR";result["http"]=e.code
   result["attempts"].append({"attempt":n,"http":e.code,"retry":transient})
   if not transient:break
  except urllib.error.URLError as e:
   result["status"]="TRANSPORT_ERROR";result["error_type"]="URLError"
   result["attempts"].append({"attempt":n,"status":"TRANSPORT_ERROR","retry":n<MAX_ATTEMPTS})
   if n>=MAX_ATTEMPTS:break
  except Exception as e:
   result["status"]="TRANSPORT_ERROR";result["error_type"]=type(e).__name__
   result["attempts"].append({"attempt":n,"status":"TRANSPORT_ERROR","retry":False})
   break
  time.sleep(n)
 return result,None

def summarize_catalog(raw):
 t=raw.decode("utf-8","replace")
 needed=("GK05553_00","奎貴5553","第8","第26","第29","刊年未詳","fn_mfPdfPopShow","mfPdfList")
 return {"self_identity":BOOK in t,"markers":{x:t.count(x) for x in needed},
         "exact_post_control":("fn_mfPdfPopShow('"+BOOK+"')" in t) or
                              ("/ajax/book/mfPdfList.do" in t and BOOK in t),
         "bounded_contexts":[{"marker":x,"context":t[max(0,t.find(x)-150):t.find(x)+450]}
           for x in needed if x in t],
         "original_printed_folio_held":False}

def parse_vols(raw):
 try:v=json.loads(raw)
 except (ValueError,UnicodeDecodeError):return {"status":"NON_JSON","listed":[]}
 rows=v.get("volList") if isinstance(v,dict) else None
 if not isinstance(rows,list):return {"status":"NO_VOLLIST","listed":[]}
 valid=all(isinstance(x,dict) and x.get("BOOK_CD")==BOOK and x.get("ITEM_CD")=="GJB" for x in rows)
 return {"status":"EXACT_BOOK_ROWS" if valid else "INVALID_OR_MIXED_BOOK_ROWS",
         "result":v.get("RESULT"),"count":len(rows),
         "listed":[{"VOL_NO":x.get("VOL_NO"),"VOL_NM":x.get("VOL_NM"),"ITEM_CD":x.get("ITEM_CD"),
                    "BOOK_CD":x.get("BOOK_CD"),"IS_PDF":x.get("IS_PDF")} for x in rows if isinstance(x,dict)][:100]}

class TextLinks(html.parser.HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  if tag not in ("img","script","a","form","div","input"):return
  d=dict(attrs)
  fields={k:v[:260] for k,v in d.items() if isinstance(v,str) and
          k in ("onclick","href","src","data-page_no","data-vol_no","data-ori_title","data-call_no","action")}
  if fields and len(self.links)<200:self.links.append({"tag":tag,"attrs":fields})

def analyze_viewer(raw,vol):
 t=raw.decode("utf-8","replace")
 parser=TextLinks();parser.feed(t)
 literal_calls=re.findall(r"fn_originalImg\s*\([^)]{0,180}\)",t)
 return {"status":"SOURCE_VIEWER_HTML","vol_token":vol,"book_token_present":BOOK in t,
         "literal_originalimg_calls":literal_calls[:60],
         "source_emitted_elements":[x for x in parser.links if
           "bookinfo" in str(x) or "page_no" in str(x) or "fn_originalImg" in str(x)][:45],
         "physical_book_ordinal_verified":False,
         "original_printed_juan_verified":False,
         "ancient_original_image_acquired":False}

def source_listed_targets(parsed):
 if parsed.get("status")!="EXACT_BOOK_ROWS":return []
 s={str(x["VOL_NO"]) for x in parsed["listed"] if x.get("VOL_NO") is not None}
 return [t for t in TARGET_VOL_TOKENS if t in s]

def main():
 import http.cookiejar
 out=Path(os.environ.get("TIANWEN_13JK_OUT","/tmp/tianwen-13jk"));out.mkdir(parents=True,exist_ok=True)
 opener=urllib.request.build_opener(OfficialOnly(),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
 report={"schema":"TIANWEN-13JK-GK5553-FIRSTPARTY-OWN-CATALOG-TO-VIEWER-R1","book":BOOK,
         "catalog":None,"volume_service":None,"target_viewers":[],
         "physical_book8_or26_original_verified":False,"manuscript_ordinal_winner":None,
         "ancient_numeric_winners":0,"independent_historical_witness_votes":0,"algorithm_reopens":0}
 c,raw=get(opener,CATALOG);report["catalog"]=c
 if raw is not None:
  (out/"snu-gk5553-catalog.html").write_bytes(raw)
  report["catalog_context"]=summarize_catalog(raw)
  if report["catalog_context"]["exact_post_control"]:
   v,body=get(opener,VOLS,{"book_cd":BOOK})
   report["volume_service"]=v
   if body is not None:
    (out/"snu-gk5553-volList.json").write_bytes(body)
    parsed=parse_vols(body);report["volume_service"]["parsed"]=parsed
    for vol in source_listed_targets(parsed):
     url=VIEWER+"?"+urllib.parse.urlencode({"item_cd":"GJB","book_cd":BOOK,"vol_no":vol})
     meta,html=get(opener,url);entry={"vol_token":vol,"retrieval":meta}
     if html is not None and b"GK05553_00" in html:
      (out/("snu-gk5553-"+vol+"-viewer.html")).write_bytes(html)
      entry["source_viewer"]=analyze_viewer(html,vol)
     report["target_viewers"].append(entry)
 (out/"catalog-to-viewer-boundary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(report,ensure_ascii=False))
 print("DIGITAL_VOL_NOT_PHYSICAL_COPY_NO_ORIGINAL_GLYPH_ADJUDICATION")
if __name__=="__main__":main()
