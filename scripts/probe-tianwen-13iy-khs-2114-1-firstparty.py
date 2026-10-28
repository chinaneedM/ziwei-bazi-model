#!/usr/bin/env python3
"""13IY: fetch official KHS 2114-1 as an explicitly UNVERIFIED candidate locator.

Source-discovered official ctpt number 1121121140100 is not direct proof
that guessed cross-API ccbaAsno 0021140000100 resolves to the same object.
Only an exact-title + identity + detailed-description direct XML response
can upgrade the result. Never use modern heritage prose as ancient folio.
"""
import hashlib,json,os,urllib.error,urllib.parse,urllib.request,xml.etree.ElementTree as ET
from pathlib import Path

ROOT="https://www.khs.go.kr/cha/SearchKindOpenapiDt.do"
# Candidate API parameter is a cross-endpoint hypothesis, NOT a verified item.
CANDIDATE_CODE="0021140000100"
KNOWN_2114_2="0021140000200"
OFFICIAL_LINK="https://www.heritage.go.kr/heri/cul/culSelectDetail.do?ccbaCpno=1121121140100"
LIMIT=900000

class HttpsKhsOnly(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,url):
  p=urllib.parse.urlsplit(url)
  if (p.scheme,p.hostname,p.path)!=("https","www.khs.go.kr","/cha/SearchKindOpenapiDt.do"):
   raise urllib.error.HTTPError(url,code,"OFF_ORIGIN_REDIRECT",headers,fp)
  return super().redirect_request(req,fp,code,msg,headers,url)

def assess(body,expected="2114-1"):
 v={"body_sha256":hashlib.sha256(body).hexdigest(),"byte_count":len(body),
    "xml":False,"title_matched":False,"identity_matched":False,"long_description":False,
    "direct_official_2114_1":False,"description_length":0,"description_sha256":None,
    "description":None,"ancient_original_page":False,"physical_book29_juan_map":None,
    "numeric_or_chart_promotions":0}
 if len(body)<20 or len(body)>LIMIT or not body.lstrip().startswith(b"<"):return v
 try:root=ET.fromstring(body)
 except ET.ParseError:return v
 v["xml"]=True
 text=[(x.tag.split("}")[-1].lower(),(x.text or "").strip()) for x in root.iter() if (x.text or "").strip()]
 flat=" ".join(t for k,t in text)
 desc=max((t for k,t in text if k in ("content","contentkor","contenttxt","description","ccba_content","ccba_content1","ccba_content2")),key=len,default="")
 v["title_matched"]=("고려사" in flat or "高麗史" in flat)
 tokens=("2114-1","2021-1","0021140000100") if expected=="2114-1" else ("2114-2","2021-2","0021140000200")
 v["identity_matched"]=any(z in flat for z in tokens)
 v["description_length"]=len(desc)
 v["long_description"]=len(desc)>450
 if v["title_matched"] and v["identity_matched"] and v["long_description"]:
  v["description"]=desc
  v["description_sha256"]=hashlib.sha256(desc.encode("utf-8")).hexdigest()
  v["direct_official_2114_1"]=(expected=="2114-1")
 return v

def fetch(code,expected):
 url=ROOT+"?"+urllib.parse.urlencode({"ccbaKdcd":"12","ccbaAsno":code,"ccbaCtcd":"11"})
 info={"code":code,"expected":expected,"url":url,"http":None,"result":"SOURCE_ACCESS_NOT_PROVEN","body":None}
 req=urllib.request.Request(url,headers={"Accept":"application/xml,text/xml","User-Agent":"Tianwen-13IY-Official-2114-1-Comparison/1.0"})
 try:
  with urllib.request.build_opener(HttpsKhsOnly()).open(req,timeout=25) as response:
   url2=urllib.parse.urlsplit(response.geturl())
   if (url2.scheme,url2.hostname,url2.path)!=("https","www.khs.go.kr","/cha/SearchKindOpenapiDt.do"):
    info["result"]="UNTRUSTED_FINAL_URL";return info,None
   info["http"]=response.status
   body=response.read(LIMIT+1)
   info["body"]=assess(body,expected)
   info["result"]="SOURCE_IDENTITY_AND_LONG_DESCRIPTION_VERIFIED" if info["body"]["identity_matched"] and info["body"]["title_matched"] and info["body"]["long_description"] else "WRONG_OR_UNVERIFIED_DETAIL_RESPONSE"
   return info,body if info["result"]=="SOURCE_IDENTITY_AND_LONG_DESCRIPTION_VERIFIED" else None
 except urllib.error.HTTPError as e:info["http"]=e.code;info["result"]="HTTP_UNAVAILABLE"
 except Exception as e:info["result"]="NETWORK_OR_TLS_UNAVAILABLE";info["exception_type"]=type(e).__name__
 return info,None

def main():
 out=Path(os.environ.get("TIANWEN_13IY_OUT","/tmp/tianwen-13iy-khs"));out.mkdir(parents=True,exist_ok=True)
 a,raw=fetch(CANDIDATE_CODE,"2114-1")
 b,_=fetch(KNOWN_2114_2,"2114-2")
 good=a["result"]=="SOURCE_IDENTITY_AND_LONG_DESCRIPTION_VERIFIED"
 if good and raw is not None:(out/"official-2114-1-verified.xml").write_bytes(raw)
 record={"schema":"TIANWEN_13IY_KHS_2114_1_FIRSTPARTY_PROBE_R1","source_discovered_official_2114_1_page":OFFICIAL_LINK,
         "api_candidate_is_unverified_until_response_identity":True,
         "candidate":a,"known_separate_2114_2_control":{k:v for k,v in b.items() if k!="body"},
         "result":"MODERN_FIRSTPARTY_KOREAN_DESIGNATION_TEXT_ACQUIRED" if good else "NO_VERIFIED_2114_1_DESCRIPTION",
         "ancient_source_pages_acquired":0,"gk5553_book29_juan_original":None,"chart_algorithm_changes":0}
 (out/"firstparty-probe.json").write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"candidate":{k:v for k,v in a.items() if k!="body"},
   "candidate_description":a["body"],"control":{k:v for k,v in b.items() if k!="body"},
   "result":record["result"]},ensure_ascii=False))
 print("NO_ANCIENT_FOLIO_OR_ALGORITHM_UPGRADE")
if __name__=="__main__":main()
