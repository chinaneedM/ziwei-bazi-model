#!/usr/bin/env python3
"""Probe only EXACT official OPAC/Details relations in 13LU BSB manifest.
No guessing sibling identifiers, login, OCR, or automated catalog browsing.
"""
import hashlib,io,json,re,urllib.parse,urllib.request,argparse
from pathlib import Path
from html.parser import HTMLParser
TARGETS=[
 ("OPAC","https://opacplus.bsb-muenchen.de/title/BV039968895"),
 ("DETAILS","https://mdz-nbn-resolving.de/details:bsb11166692")
]
HOSTS={"opacplus.bsb-muenchen.de","mdz-nbn-resolving.de","www.digitale-sammlungen.de","digitale-sammlungen.de","opac.bsb-muenchen.de","www.bsb-muenchen.de"}
class SafeRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,newurl):
  p=urllib.parse.urlsplit(newurl)
  if p.scheme!="https" or p.hostname not in HOSTS:raise ValueError("redirect outside exact BSB host allowlist")
  return super().redirect_request(req,fp,code,msg,headers,newurl)
class LinkParser(HTMLParser):
 def __init__(self):super().__init__();self.hrefs=[]
 def handle_starttag(self,tag,attrs):
  if tag=="a":
   for k,v in attrs:
    if k=="href" and v:self.hrefs.append(v)
def scan(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 opener=urllib.request.build_opener(SafeRedirect)
 report={"schema":"TIANWEN-13LV-BSB-EXACT-OPAC-DETAILS-ROUTE-PROBE","targets":[],"opac_volume1_verified":False,"juan35_verified":False,"no_guess":True,"no_ocr":True}
 for name,url in TARGETS:
  record={"target":name,"original_url":url,"status":"NOT_ACCESSED"}
  try:
   req=urllib.request.Request(url,headers={"User-Agent":"TIANWEN/13LV edition catalog audit"})
   with opener.open(req,timeout=22) as resp:
    final=resp.geturl();p=urllib.parse.urlsplit(final)
    if p.scheme!="https" or p.hostname not in HOSTS:raise ValueError("unsafe final host")
    raw=resp.read(2500001)
    if len(raw)>2500000:raise ValueError("over bounded 2.5MB page")
    text=raw.decode(resp.headers.get_content_charset() or "utf8","replace")
    parser=LinkParser();parser.feed(text)
    links=[urllib.parse.urljoin(final,v) for v in parser.hrefs]
    links=[v for v in links if urllib.parse.urlsplit(v).hostname in HOSTS]
    volume_mentions=[x for x in links if "bsb" in x.lower() and x!=url]
    record.update(status="HTML_CAPTURED",final_url=final,http_status=resp.status,content_sha256=hashlib.sha256(raw).hexdigest(),content_bytes=len(raw),content_type=resp.headers.get("Content-Type"),firstparty_links_found=len(links),candidate_source_links=volume_mentions[:40],title_near_mingshi=bool(re.search("Ming shi|明史",text,re.I)))
  except Exception as exc:record.update(status="ACCESS_BOUNDARY",error=str(exc)[:350])
  report["targets"].append(record)
 (out/"opac-route-probe.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 print(json.dumps({"status":"RECORDED","routes":[[r["target"],r["status"]] for r in report["targets"]]},ensure_ascii=False))
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--out",required=True);scan(a.parse_args().out)
