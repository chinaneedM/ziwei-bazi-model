#!/usr/bin/env python3
"""12YQ trace public Wikisource exact Mei Datong Lizhi vol3~4 archive item URLs.

Catalogue links are only target discovery, NOT original page glyph or imprint proof.
"""
from __future__ import annotations
import html,json,re,urllib.request,urllib.parse
from html.parser import HTMLParser
from pathlib import Path
OUT=Path("research-12yq-mei-ia")
OUT.mkdir(exist_ok=True)
URLS=[
 "https://zh.wikisource.org/zh-hans/Wikisource:%E5%8F%A4%E7%B1%8D%E8%B3%87%E6%BA%90/Internet_Archive_Scans/%E6%B8%85",
 "https://zh.wikisource.org/w/api.php?action=parse&page=Wikisource:%E5%8F%A4%E7%B1%8D%E8%B3%87%E6%BA%90/Internet_Archive_Scans/%E6%B8%85&prop=text&format=json",
]
class Anchors(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.current=None
 def handle_starttag(self,tag,attrs):
  if tag=="a": self.current={"href":dict(attrs).get("href",""),"text":""}
 def handle_data(self,data):
  if self.current is not None:self.current["text"]+=data
 def handle_endtag(self,tag):
  if tag=="a" and self.current is not None:self.links.append(self.current);self.current=None
data={"schema":"TIANWEN-12YQ-IA-SOURCE-CATALOG-LINK-RESOLUTION-ONLY","catalog":"Wikisource 古籍資源/Internet Archive Scans/清","subject":"梅文鼎 大統歷志","source_page":URLS[0],"grade":"CATALOGUE_DIRECT_LINK_DISCOVERY_NOT_ORIGINAL_GLYPHS","requests":[],"mei_ia_volume3_4_href":None,"mei_archive_item_id":None,"original_target_glyphs_read":0,"independent_physical_votes":0}
for url in URLS:
 try:
  rq=urllib.request.Request(url,headers={"User-Agent":"TianwenPhilologyResearch/1.0 (public public-domain source-citation)", "Accept":"text/html,application/json"})
  with urllib.request.urlopen(rq,timeout=50) as fp: b=fp.read(15_000_000);status=fp.status
  raw=b.decode("utf8","replace")
  if raw.lstrip().startswith("{"):
   j=json.loads(raw);raw=j.get("parse",{}).get("text",{}).get("*","")
  anchors=Anchors();anchors.feed(raw)
  matches=[]
  for i,a in enumerate(anchors.links):
   if "大统历志" in a["text"] or "大統歷志" in a["text"] or "大統厯志" in a["text"]:
    matches.append({"index":i,"anchor":a,"context":anchors.links[max(0,i-2):i+7]})
  data["requests"].append({"url":url,"http":status,"received_bytes":len(b),"link_count":len(anchors.links),"matches":matches[:8]})
  for mm in matches:
   for a in mm["context"]:
    label=a["text"].strip()
    if (("3" in label and "4" in label) or ("三" in label and "四" in label)) and "archive.org" in a["href"]:
     data["mei_ia_volume3_4_href"]=html.unescape(a["href"])
     mt=re.search(r"archive.org/(?:details|download)/([^/?#]+)",data["mei_ia_volume3_4_href"])
     if mt:data["mei_archive_item_id"]=mt.group(1)
     break
  if data["mei_archive_item_id"]:break
 except Exception as e:
  data["requests"].append({"url":url,"error":type(e).__name__+": "+str(e)[:350]})
(OUT/"catalog_route.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print(json.dumps({k:data[k] for k in ("mei_ia_volume3_4_href","mei_archive_item_id","original_target_glyphs_read","independent_physical_votes")},ensure_ascii=False))
print("REQUEST_OUTCOMES",json.dumps(data["requests"],ensure_ascii=False)[:7000])
