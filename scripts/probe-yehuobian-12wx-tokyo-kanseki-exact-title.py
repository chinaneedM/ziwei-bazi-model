#!/usr/bin/env python3
"""12WX exactly one provider-documented advanced book-title POST; no guess of records/images."""
import argparse,hashlib,html.parser,json,re,urllib.error,urllib.parse,urllib.request
from pathlib import Path

URL="https://kanseki.ioc.u-tokyo.ac.jp/user/query_adv.php"
TITLE="野獲編"
JS_SHA256="efc4dd5b6e3cd3237c2f26fce7e4e6e23cdd205b71d64b3aad0ddea247ba9183"
FORM_SHA256="363dedbd1e71d830870ee0497a52908970776906c98ac563e63dd9b1e2967684"
MAX=800_000
UA="Tianwen/12WX one public exact Chinese classics catalog title field query; no image"
def payload():
 sep=chr(30);rec=chr(31)
 # 12WW source-emitted qadv_ck JS combines booleans[i] + chr(30) + cols[i] + chr(30) + strs[i] + chr(31)
 token="and"+sep+"ti"+sep+TITLE+rec
 return [
 ("fun","qadv"),("q_str",token),("ref_w_flag","Y"),
 ("booleans","and"),("cols","ft"),("strs",""),
 ("booleans","and"),("strs",TITLE),("cols","ti"),
 ("booleans","and"),("strs",""),("cols","au"),
 ("qorder_by","nu"),("qorder_by2","asc"),("qpg_num","20")
 ]
def guard(url=URL,pairs=None):
 if url!=URL:raise ValueError("not the first-party source-issued POST endpoint")
 if pairs is not None and pairs!=payload():raise ValueError("not exact source JS reconstructed one title request")
 return True
class Indexed(html.parser.HTMLParser):
 def __init__(self):
  super().__init__();self.visible=[];self.links=[];self.a=None;self.script=False
 def handle_starttag(self,tag,attrs):
  if tag=="script":self.script=True
  if tag=="a":self.a={"href":dict(attrs).get("href"),"text":""}
 def handle_endtag(self,tag):
  if tag=="script":self.script=False
  if tag=="a" and self.a is not None:
   self.links.append(self.a);self.a=None
 def handle_data(self,d):
  if self.script:return
  self.visible.append(d)
  if self.a is not None:self.a["text"]+=d
def examine(raw):
 if len(raw)>MAX:raise ValueError("provider search response too large")
 p=Indexed();p.feed(raw.decode("utf-8",errors="replace"))
 content=" ".join(p.visible)
 titles=[{"href":a["href"],"text":a["text"].strip()[:180]} for a in p.links if TITLE in a["text"]]
 return {
 "schema":"TIANWEN-12WX-TOKYO-IOC-FULL-CLASSICS-ONE-EXACT-TITLE-POST-R1",
 "provider_endpoint":URL,"original_response_sha256":hashlib.sha256(raw).hexdigest(),"response_bytes":len(raw),
 "submitted_title":TITLE,"reconstructed_post_q_str_sha256":hashlib.sha256(payload()[1][1].encode()).hexdigest(),
 "result_visible_title_in_page":TITLE in content,"source_visible_target_anchor_count":len(titles),
 "source_visible_target_anchors":titles[:30],
 "visible_error_markers":[x for x in ("無任何資料","未查到","查無資料","Error","Fatal error") if x in content],
 "source_page_title_preview":content[:500],
 "source_emitted_original_volume20_paper_image":False,
 "item_1827_6403767830_physical_image_bound":False,
 "item_1869_6403148395_physical_image_bound":False,
 "a_positive_query_is_not_original_print_vote":True,
 "a_zero_hit_is_not_absence_of_tokyo_cinii_holdings":True,
 "new_independent_historical_paper_impression_votes":0,"ocr":False
 }
def run(outdir):
 out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
 q=payload();guard(URL,q)
 try:
  data=urllib.parse.urlencode(q).encode("utf-8")
  req=urllib.request.Request(URL,data=data,headers={"User-Agent":UA,"Content-Type":"application/x-www-form-urlencoded","Accept":"text/html"},method="POST")
  with urllib.request.urlopen(req,timeout=45) as resp:
   u=urllib.parse.urlparse(resp.geturl())
   if u.scheme!="https" or u.hostname!="kanseki.ioc.u-tokyo.ac.jp" or u.path!="/user/query_adv.php":
    raise ValueError("off-source search result redirect")
   raw=resp.read(MAX+1)
  result=examine(raw)
  result["expected_original_form_sha256"]=FORM_SHA256
  result["expected_original_script_sha256"]=JS_SHA256
  (out/"original-search-response.html").write_bytes(raw)
  (out/"receipt.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  print(json.dumps({"status":"SOURCE_ISSUED_TITLE_QUERY_RETURNED","bytes":len(raw),"title_anchors":result["source_visible_target_anchor_count"],"ancient_print_votes":0},ensure_ascii=False))
 except Exception as e:
  (out/"access-error.json").write_text(json.dumps({"status":"SOURCE_ACCESS_BOUNDARY_NOT_BOOK_ABSENCE","type":type(e).__name__,"http":getattr(e,"code",None),"original_glyph_votes":0},ensure_ascii=False))
  raise
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--output-dir",default="12wx-tokyo-one-title-output");p=a.parse_args()
 run(p.output_dir)
