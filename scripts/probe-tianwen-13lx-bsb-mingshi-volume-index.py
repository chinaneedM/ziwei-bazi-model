#!/usr/bin/env python3
"""13LX: first-party BSB Ming shi 1..8 index route. Never guess digital IDs.
Fetch the exact provider title-discovery URL and preserve raw HTML + SHA.
A page label is not a verified physical copy, original leaf, or numeric reading.
"""
import argparse,hashlib,json,re,urllib.parse,urllib.request
from pathlib import Path
from bs4 import BeautifulSoup

URL="https://ostasien.digitale-sammlungen.de/discover/titles/M?q=Ming+shi+%28%E6%98%8E%E5%8F%B2%29"
HOSTS={"ostasien.digitale-sammlungen.de","www.digitale-sammlungen.de"}
class ScopedRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,url):
  p=urllib.parse.urlsplit(url)
  if p.scheme!="https" or p.hostname not in HOSTS:
   raise ValueError("redirect beyond provider hosts")
  return super().redirect_request(req,fp,code,msg,headers,url)
def safe_href(value,base):
 try:
  u=urllib.parse.urljoin(base,value)
  p=urllib.parse.urlsplit(u)
  if p.scheme=="https" and p.hostname in HOSTS and not p.username and not p.password:return u
 except (ValueError,TypeError):pass
 return None
def extract(html,base):
 soup=BeautifulSoup(html,"html.parser")
 card_titles=[]
 for label in soup.find_all(string=re.compile(r"(?i)ming\s+shi\s*\(明史\)\s*[;.]?\s*([1-8])\b")):
  m=re.search(r"(?i)ming\s+shi\s*\(明史\)\s*[;.]?\s*([1-8])\b",str(label))
  if not m:continue
  number=int(m.group(1))
  best=None
  parent=label.parent
  for depth in range(8):
   if parent is None:break
   text=" ".join(parent.get_text(" ",strip=True).split())
   links=[safe_href(a.get("href"),base) for a in parent.find_all("a",href=True)]
   links=[u for u in links if u]
   if len(text)<1400 and links:
    cand={"number":number,"provider_label":str(label).strip(),
          "container_text":text[:600],"provider_links":list(dict.fromkeys(links))[:30],
          "dom_ancestor_depth":depth}
    if best is None or ("Mehr Informationen" in text or "Download" in text) and not any("Mehr Informationen" in best["container_text"] for x in [0]):
     best=cand
     if "Mehr Informationen" in text:break
   parent=parent.parent
  card_titles.append(best or {"number":number,"provider_label":str(label).strip(),"provider_links":[],"container_text":"","dom_ancestor_depth":None})
 by_number={}
 for x in card_titles:
  n=x["number"]
  if n not in by_number or len(x["provider_links"])>len(by_number[n]["provider_links"]):by_number[n]=x
 return [by_number[n] for n in sorted(by_number)]
def fetch():
 opener=urllib.request.build_opener(ScopedRedirect)
 with opener.open(urllib.request.Request(URL,headers={"User-Agent":"TIANWEN/13LX open historical source bibliographic review"}),timeout=28) as r:
  u=r.geturl();p=urllib.parse.urlsplit(u)
  if p.hostname not in HOSTS or p.scheme!="https":raise ValueError("invalid final host")
  raw=r.read(2000001)
  if len(raw)>2000000:raise ValueError("provider page exceeds 2MB gate")
  return raw,u,r.status,r.headers.get("Content-Type")
def main(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 record={"schema":"TIANWEN-13LX-BSB-INDEX-1-8-FIRSTPARTY-SOURCE-PROBE-R1",
 "source_url":URL,"status":"SOURCE_UNVERIFIED","no_ocr":True,
 "sibling_volume1_original_id_confirmed":False,"juan35_original_leaf_verified":False,
 "exact_1739_physical_impression_proven":False,"original_numeric_winners":0,"cards":[]}
 try:
  raw,final,status,ctype=fetch()
  (out/"firstparty-ming-shi-volume-index.html").write_bytes(raw)
  cards=extract(raw.decode("utf-8","replace"),final)
  record.update(status="SOURCE_HTML_CAPTURED",final_url=final,http_status=status,
   content_type=ctype,source_html_bytes=len(raw),
   source_html_sha256=hashlib.sha256(raw).hexdigest(),cards=cards,
   volume_numbers_in_source=[c["number"] for c in cards],
   eight_distinct_volume_labels_found=[c["number"] for c in cards]==list(range(1,9)))
  record["volume1_explicit_digital_ids_extracted_not_yet_edition_verified"]=sorted(set(
   re.findall(r"bsb[0-9]{7,12}",json.dumps(next((c for c in cards if c["number"]==1),{})),re.I)))
 except Exception as e:record.update(status="SOURCE_ACCESS_BOUNDARY",error=str(e)[:450])
 (out/"firstparty-index-route.json").write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 print(json.dumps({k:record.get(k) for k in ["status","source_html_sha256","volume_numbers_in_source","eight_distinct_volume_labels_found","volume1_explicit_digital_ids_extracted_not_yet_edition_verified","error"]},ensure_ascii=False))
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--out",required=True);main(p.parse_args().out)
