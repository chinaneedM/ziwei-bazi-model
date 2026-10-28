#!/usr/bin/env python3
"""13JL: source-issued GK5553 photos, not guessed image IDs or source votes.

13JH firstparty GK05553_00 volList listed 0012/0029 and exact viewer HTML
SHA 4a6f.../18d5... emitted the five target fn_originalImg calls. 13JD
firstparty common2.js defines POST /pf01/rendererImg.do. Follow only exact
returned ImageServlet img.src, then preserve raw JPEG, digest, dimensions
and no-OCR/physical-impression boundary. No new original printed glyph claim.
"""
import hashlib,html.parser,http.cookiejar,json,os,time,urllib.error,urllib.parse,urllib.request
from pathlib import Path
BASE="https://kyudb.snu.ac.kr"
VIEWER=BASE+"/pf01/rendererImg.do"
JS_SHA="b2b4aaabf3da440b84b64f25768965a6c2c5500775b53e7634e98e4f59adf087"
SOURCE_RUN=40674164409
SOURCE_ARTIFACT=12809168697
VOLUMES={"0008":{"html_sha256":"6f860dfe1bd8afc775f53620d0bc4c4a0604cb9623de9af0a06117bb4e0c0351","pages":["001a"]},
         "0026":{"html_sha256":"9013486d03c0e3379f61fb50b606bc2d267d1be7b24fa234d22f9699ae5ab5d3","pages":["001a"]},
         "0011":{"html_sha256":"b7e067654bd88e736cc37da01bb564d3adccd43fc446407cf6128e356e87ea79","pages":["002a"]},
         "0013":{"html_sha256":"7b047f111c51297a002d6878d58784c5830be56c13b1b55c8bd01715b4e9005b","pages":["002a"]},
         "0025":{"html_sha256":"68c2ace027df51cafd05b91dfafd52559c885981d9b50ccd8ac5645015413246","pages":["001a"]},
         "0027":{"html_sha256":"3c77961149257c085cc381d22c03c1f89bf642300f25be6b58c60c2280c9b40f","pages":["001a"]}}
CAP=12_000_000
ATTEMPTS=3
class SourceOnly(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,url):
  p=urllib.parse.urlsplit(url)
  if (p.scheme,p.hostname)!=("https","kyudb.snu.ac.kr"):
   raise urllib.error.HTTPError(url,code,"CROSS_PROVIDER",headers,fp)
  return super().redirect_request(req,fp,code,msg,headers,url)
class Images(html.parser.HTMLParser):
 def __init__(self):super().__init__();self.srcs=[]
 def handle_starttag(self,tag,attrs):
  if tag=="img":
   d=dict(attrs);s=d.get("src")
   if isinstance(s,str) and s.startswith("/ImageServlet.do?"):self.srcs.append(s)
def source_target(vol,page):
 return vol in VOLUMES and page in VOLUMES[vol]["pages"]
def body(vol,page):
 if not source_target(vol,page):raise ValueError("not provider-emitted page")
 fields={"item_cd":"GJB","book_cd":"GK05553_00","vol_no":vol,"page_no":page,
         "imgFileNm":"","tbl_conts_seq":"","mokNm":"","add_page_no":""}
 return urllib.parse.urlencode(fields).encode("ascii")
def authorize_src(src,vol,page):
 if not source_target(vol,page):return False
 parsed=urllib.parse.urlsplit(src)
 if parsed.scheme or parsed.netloc or parsed.path!="/ImageServlet.do":return False
 q=urllib.parse.parse_qs(parsed.query,keep_blank_values=True)
 fn="GK05553_00_IL_"+vol+"_"+page+".jpg"
 if set(q)!={"imgFileNm","path"} or q["imgFileNm"]!=[fn]:return False
 path=q["path"][0]
 prefix="/data01/stream/GJB/IMG/GK05553_00/GK05553_00_"+vol+"/"
 return path==prefix+fn
def valid_jpeg(raw,ctype):
 c=(ctype or "").split(";",1)[0].strip().lower()
 if c not in ("","image/jpeg","image/pjpeg","application/octet-stream"):return False
 return len(raw)>100 and raw.startswith(b"\xff\xd8\xff") and raw.endswith(b"\xff\xd9")
def fetch(opener,req):
 errors=[]
 for n in range(1,ATTEMPTS+1):
  try:
   with opener.open(req,timeout=22) as resp:
    url=urllib.parse.urlsplit(resp.geturl())
    if (url.scheme,url.hostname)!=("https","kyudb.snu.ac.kr"):
     return {"status":"UNTRUSTED_FINAL_URL"},None
    raw=resp.read(CAP+1)
    meta={"status":"ACQUIRED" if 0<len(raw)<=CAP else "EMPTY_OR_OVERSIZED",
          "http":resp.status,"bytes":len(raw),"content_type":resp.headers.get("Content-Type",""),
          "sha256":hashlib.sha256(raw).hexdigest(),"attempt_log":errors}
    return meta,raw if meta["status"]=="ACQUIRED" else None
  except urllib.error.HTTPError as exc:
   retry=exc.code in (429,502,503,504) and n<ATTEMPTS
   errors.append({"attempt":n,"status":"HTTP_ERROR","http":exc.code,"retry":retry})
   if not retry:break
  except urllib.error.URLError:
   errors.append({"attempt":n,"status":"TRANSPORT_ERROR","retry":n<ATTEMPTS})
   if n>=ATTEMPTS:break
  except Exception as exc:
   errors.append({"attempt":n,"status":"TRANSPORT_ERROR","type":type(exc).__name__,"retry":False})
   break
  time.sleep(n)
 return {"status":"NOT_ACQUIRED","attempt_log":errors},None
def probe(opener,out,vol,page):
 data=body(vol,page)
 referer=BASE+"/book/text.do?item_cd=GJB&book_cd=GK05553_00&vol_no="+vol
 req=urllib.request.Request(VIEWER,data=data,headers={"User-Agent":"Tianwen-13JL-GK5553-Exact-Original/1.0","Accept":"text/html,application/xhtml+xml","Origin":BASE,"Referer":referer})
 x,html=fetch(opener,req)
 record={"vol_token":vol,"source_page_token":page,"source_html_sha256":VOLUMES[vol]["html_sha256"],
         "source_run":SOURCE_RUN,"source_artifact":SOURCE_ARTIFACT,
         "official_javascript_sha256":JS_SHA,"official_post":x,"image":None,
         "original_printed_glyph_reviewed":False,"physical_book_ordinal_proven":False,
         "edition_impression_year":None,"independent_physical_witness_votes":0}
 if html is None:return record
 if x.get("http")!=200 or "html" not in x.get("content_type","").lower():
  record["status"]="NON_HTML_VIEWER";return record
 f=Images();f.feed(html.decode("utf-8","replace"))
 links=[s for s in f.srcs if authorize_src(s,vol,page)]
 record["source_emitted_image_matches"]=links
 if len(links)!=1:record["status"]="NO_UNIQUE_SOURCE_IMAGE";return record
 record["status"]="SOURCE_IMAGE_LOCATED"
 image_url=BASE+links[0]
 img_req=urllib.request.Request(image_url,headers={"User-Agent":"Tianwen-13JL-GK5553-Exact-Original/1.0","Accept":"image/jpeg,image/*;q=0.7","Referer":VIEWER})
 meta,raw=fetch(opener,img_req)
 record["image"]={"source_emitted_url":image_url,"response":meta,
                  "valid_jpeg":raw is not None and valid_jpeg(raw,meta.get("content_type",""))}
 if record["image"]["valid_jpeg"]:
  name="gk5553-"+vol+"-"+page+"-source-original.jpg"
  (out/name).write_bytes(raw)
  record["image"]["saved_file"]=name
  record["status"]="SOURCE_JPEG_ACQUIRED_UNCOLLATED"
 return record
def main():
 out=Path(os.environ.get("TIANWEN_13JL_OUT","/tmp/tianwen-13jl"));out.mkdir(parents=True,exist_ok=True)
 opener=urllib.request.build_opener(SourceOnly(),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
 results=[probe(opener,out,vol,page) for vol,d in VOLUMES.items() for page in d["pages"]]
 report={"schema":"TIANWEN-13JL-SNU-GK5553-ORIGINAL-JPEG-INTEGRITY-R1","results":results,
         "original_headings_adjudicated":False,"historical_numeric_winners":0,
         "physical_books_8_or_26_identity_confirmed":False,"algorithm_reopens":0}
 (out/"source-jpeg-intake.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(report,ensure_ascii=False))
 print("RAW_ORIGINAL_JPEG_NOT_PHYSICAL_BOOK_OR_GLYPH_COLLATION")
if __name__=="__main__":main()
