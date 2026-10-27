#!/usr/bin/env python3
"""13IW: only parse firstparty official Korean description when byte SHA matches 13IV."""
import hashlib,json,os,urllib.request,urllib.parse,urllib.error,xml.etree.ElementTree as ET
from pathlib import Path
SOURCE="https://www.khs.go.kr/cha/SearchKindOpenapiDt.do?ccbaKdcd=12&ccbaAsno=0021140000200&ccbaCtcd=11"
EXPECTED_SHA="c8a7de9c9f0ff5a64674153e7dd2048b3e6bb7e6193e0f9f9d18d7fc9106a5b9"
LIMIT=900000
MARKERS=("규귀","규기","5553","5554","권81","권82","81","82","8책","12책","26책","29책","43책","1482")
class SafeRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,url):
  p=urllib.parse.urlsplit(url)
  if (p.scheme,p.hostname,p.path)!=("https","www.khs.go.kr","/cha/SearchKindOpenapiDt.do"):
   raise urllib.error.HTTPError(url,code,"OFF_ORIGIN_REDIRECT",headers,fp)
  return super().redirect_request(req,fp,code,msg,headers,url)
def excerpts(content):
 found=[]
 for marker in MARKERS:
  pos=content.find(marker)
  if pos>=0:
   found.append({"marker":marker,"offset":pos,"context":content[max(0,pos-42):pos+len(marker)+45]})
 return found
def validate(body):
 sha=hashlib.sha256(body).hexdigest()
 v={"sha256":sha,"size":len(body),"sha_matched":sha==EXPECTED_SHA,"bound_firstparty_text":False,
    "description_length":0,"contexts":[],"ancient_original_leaf":False,"algorithms_changed":0}
 if sha!=EXPECTED_SHA:return v
 root=ET.fromstring(body)
 values=[(n.tag.split("}")[-1].lower(),(n.text or "").strip()) for n in root.iter()]
 alltext=" ".join(t for k,t in values)
 content=max((t for k,t in values if k in ("content","contentkor","contenttxt","description","ccba_content")),key=len,default="")
 if not any(w in alltext for w in ("고려사","高麗史","Goryeosa")) or not any(w in alltext for w in ("2114","2021-2","0021140000200")):return v
 if len(content)<1000:return v
 v["bound_firstparty_text"]=True
 v["description_length"]=len(content)
 v["contexts"]=excerpts(content)
 v["description_sha256_utf8"]=hashlib.sha256(content.encode("utf-8")).hexdigest()
 return v
def main():
 out=Path(os.environ.get("TIANWEN_13IW_OUT","/tmp/tianwen-13iw-khs"))
 out.mkdir(parents=True,exist_ok=True)
 d={"schema":"TIANWEN_13IW_FIRSTPARTY_OFFICIAL_SOURCE_CONTEXTS_R1","url":SOURCE,"result":"UNAVAILABLE","actual":None,"ancient_glyph_votes":0}
 req=urllib.request.Request(SOURCE,headers={"User-Agent":"Tianwen-13IW-Heritage-2114-2-Original-Description/1.0","Accept":"application/xml,text/xml"})
 try:
  with urllib.request.build_opener(SafeRedirect()).open(req,timeout=18) as resp:
   u=urllib.parse.urlsplit(resp.geturl())
   if (u.scheme,u.hostname,u.path)!=("https","www.khs.go.kr","/cha/SearchKindOpenapiDt.do"):
    d["result"]="WRONG_ENDPOINT"
   else:
    d["http"]=resp.status
    body=resp.read(LIMIT+1)
    if len(body)>LIMIT:d["result"]="OVERSIZED"
    else:
     d["actual"]=validate(body)
     d["result"]="BYTE_IDENTICAL_FIRSTPARTY_TARGET_CONTEXTS" if d["actual"]["bound_firstparty_text"] else "RESPONSE_NOT_SAME_HASH_BOUND_OFFICIAL_TEXT"
 except urllib.error.HTTPError as exc:d["http"]=exc.code;d["result"]="HTTP_ERROR"
 except Exception as exc:d["result"]="TRANSPORT_ERROR";d["exception_type"]=type(exc).__name__
 (out/"official-contexts.json").write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(d,ensure_ascii=False))
 print("HISTORICAL_ORIGINAL_LEAF_AND_SIX_NUMERIC_WINNERS_REMAIN_OPEN")
if __name__=="__main__":main()
