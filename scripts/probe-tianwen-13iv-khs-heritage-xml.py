#!/usr/bin/env python3
"""13IV: bounded firstparty KHS Korean heritage XML exact 2114-2 probe."""
import hashlib,json,os,urllib.parse,urllib.request,urllib.error,xml.etree.ElementTree as ET
from pathlib import Path
ROOT="https://www.khs.go.kr/cha/SearchKindOpenapiDt.do"
CODES=("21140200","0021140000200")
HOSTS={"www.khs.go.kr","khs.go.kr"}
LIMIT=900000
def request_url(code):
 assert code in CODES
 return ROOT+"?"+urllib.parse.urlencode({"ccbaKdcd":"12","ccbaAsno":code,"ccbaCtcd":"11"})
def parse_xml(data):
 if len(data)>LIMIT or len(data)<20 or not data.lstrip().startswith(b"<"):
  return {"parse":"REJECTED_NOT_XML_OR_SIZE","official_description_verified":False}
 try: root=ET.fromstring(data)
 except ET.ParseError:
  return {"parse":"INVALID_XML","official_description_verified":False}
 texts=[(el.tag.split("}")[-1].lower(),(el.text or "").strip()) for el in root.iter() if (el.text or "").strip()]
 flat=" ".join(v for k,v in texts)
 desc=[v for k,v in texts if k in ("content","contentkor","contenttxt","description","ccba_content","ccba_content1","ccba_content2")]
 matches_title=any(w in flat for w in ("고려사","高麗史","Goryeosa"))
 matches_identity=any(w in flat for w in ("21140200","0021140000200","2114-2","2021-2"))
 return {"parse":"XML","root":root.tag,"matched_title":matches_title,"matched_2114_2":matches_identity,
         "description_len":max((len(v) for v in desc),default=0),
         "description_excerpt":(desc[0][:180] if desc else ""),
         "official_description_verified":bool(matches_title and matches_identity and any(len(v)>450 for v in desc)),
         "original_ancient_folio_verified":False}
class SameOfficialHttps(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,newurl):
  u=urllib.parse.urlsplit(newurl)
  if (u.scheme,u.hostname,u.path)!=("https","www.khs.go.kr","/cha/SearchKindOpenapiDt.do"):
   raise urllib.error.HTTPError(newurl,code,"REDIRECT_REJECTED",headers,fp)
  return super().redirect_request(req,fp,code,msg,headers,newurl)
def fetch(code):
 out={"code":code,"url":request_url(code),"http":None,"result":"NOT_ACQUIRED","sha256":None,"byte_count":0,"parsed":None}
 req=urllib.request.Request(out["url"],headers={"User-Agent":"Tianwen-13IV-Heritage-Firstparty-Probe/1.0","Accept":"text/xml,application/xml"})
 try:
  with urllib.request.build_opener(SameOfficialHttps()).open(req,timeout=16) as response:
   u=urllib.parse.urlsplit(response.geturl())
   if (u.scheme,u.hostname,u.path)!=("https","www.khs.go.kr","/cha/SearchKindOpenapiDt.do"):
    out["result"]="UNTRUSTED_RESPONSE_URL";return out
   out["http"]=response.status
   data=response.read(LIMIT+1)
   out["byte_count"]=len(data)
   if len(data)>LIMIT:out["result"]="OVERSIZE";return out
   out["sha256"]=hashlib.sha256(data).hexdigest()
   out["parsed"]=parse_xml(data)
   out["result"]="OFFICIAL_XML_DESCRIPTION_IDENTITY_BOUND" if out["parsed"]["official_description_verified"] else "RESPONSE_NOT_DESCRIPTION_PROOF"
 except urllib.error.HTTPError as ex:out["http"]=ex.code;out["result"]="HTTP_UNAVAILABLE"
 except Exception as ex:out["result"]="TRANSPORT_OR_TLS_UNAVAILABLE";out["exception_type"]=type(ex).__name__
 return out
def main():
 path=Path(os.environ.get("TIANWEN_13IV_OUT","/tmp/tianwen-13iv-khs"))
 path.mkdir(parents=True,exist_ok=True)
 checks=[fetch(c) for c in CODES]
 results={"schema":"TIANWEN_13IV_KHS_PROBE_R1","official_xml_description_retrieved":any(x["result"]=="OFFICIAL_XML_DESCRIPTION_IDENTITY_BOUND" for x in checks),"checks":checks,"original_ancient_folios":0,"glyph_votes":0,"algorithm_reopens":0}
 (path/"probe-summary.json").write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 for x in checks:
  p=x["parsed"] or {}
  print(json.dumps({"code":x["code"],"http":x["http"],"result":x["result"],"sha256":x["sha256"],"bytes":x["byte_count"],"matched_title":p.get("matched_title"),"matched_2114_2":p.get("matched_2114_2"),"description_len":p.get("description_len"),"excerpt":p.get("description_excerpt")},ensure_ascii=False))
 print("NO_ANCIENT_FOLIO_OR_GLYPH_PROMOTION")
if __name__=="__main__":main()
