#!/usr/bin/env python3
"""12WT first-party University Tokyo separate Chinese classics holdings catalog, not source folios."""
import argparse,hashlib,html.parser,json,urllib.error,urllib.parse,urllib.request
from pathlib import Path
SOURCES={
 "kanseki_catalog_home":"https://kanseki.ioc.u-tokyo.ac.jp/user/index.php",
 "university_catalog_scope":"https://www.lib.u-tokyo.ac.jp/ja/library/contents/database/385",
}
MAX=600_000
UA="Tianwen historical provenance 12WT; bounded public metadata only; no OCR or source image"
class P(html.parser.HTMLParser):
 def __init__(self):
  super().__init__();self.links=[];self.forms=[];self.form=None;self.select=None;self.text=[];self.controls=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=="a" and a.get("href"):self.links.append({"href":a["href"],"title":a.get("title")})
  if tag=="form":
   self.form={"method":a.get("method","get").lower(),"action":a.get("action"),"inputs":[],"selects":[]};self.forms.append(self.form)
  if tag=="select" and self.form is not None:
   self.select={"name":a.get("name"),"values":[]};self.form["selects"].append(self.select)
  if tag=="option" and self.select is not None:self.select["values"].append(a.get("value"))
  if tag in ("input","button") and self.form is not None:self.form["inputs"].append({k:a[k] for k in ("name","value","type","onclick") if k in a})
  if tag=="input" and self.form is None:self.controls.append({k:a[k] for k in ("name","value","type","onclick") if k in a})
 def handle_endtag(self,tag):
  if tag=="form":self.form=None;self.select=None
  if tag=="select":self.select=None
 def handle_data(self,d):self.text.append(d)
def guard(name,url):
 if name not in SOURCES or url!=SOURCES[name]:raise ValueError("only two provider-issued catalogue pages permitted")
 return True
def parse(name,url,raw):
 guard(name,url)
 if len(raw)>MAX:raise ValueError("source metadata over 600KB")
 p=P();p.feed(raw.decode("utf-8",errors="replace"))
 text=" ".join(p.text)
 urls=[]
 for x in p.links:
  h=urllib.parse.urljoin(url,x["href"])
  u=urllib.parse.urlparse(h)
  if u.scheme=="https" and u.hostname in ("kanseki.ioc.u-tokyo.ac.jp","www.lib.u-tokyo.ac.jp") and not any(k in u.path.lower() for k in (".jpg",".pdf",".png",".zip",".tif",".jpeg")):
   urls.append({"url":h,"title":x["title"]})
 return {
 "source":name,"source_url":url,"original_bytes":len(raw),"original_sha256":hashlib.sha256(raw).hexdigest(),
 "html_forms":p.forms[:30],"unscoped_input_fields":p.controls[:40],
 "allowed_provider_links":urls[:100],"allowed_provider_link_count":len(urls),
 "visible_classics_catalog_description":("漢籍" in text or "古籍" in text),
 "visible_text_mentions_yekakuhen":"野獲編" in text or "野获编" in text,
 "visible_text_mentions_original_1827_item":"6403767830" in text,
 "visible_text_mentions_original_1869_item":"6403148395" in text,
 "original_page_pixels_retrieved":0,"printed_juan20_glyphs_retrieved":0,"original_paper_impression_votes":0,"ocr":False
 }
def capture_one(name,url,opener=urllib.request.urlopen):
 guard(name,url)
 req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html"})
 with opener(req,timeout=30) as f:
  u=urllib.parse.urlparse(f.geturl())
  if u.scheme!="https" or u.hostname!=urllib.parse.urlparse(url).hostname:raise ValueError("unexpected source-domain redirect")
  body=f.read(MAX+1)
 return body,parse(name,url,body)
def capture(outdir):
 out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
 summaries=[]
 for name,url in SOURCES.items():
  try:
   body,r=capture_one(name,url)
   (out/(name+".html")).write_bytes(body);summaries.append({"status":"PROVIDER_HTML_DIRECT",**r})
  except (ValueError,TimeoutError,urllib.error.HTTPError,urllib.error.URLError) as e:
   summaries.append({"source":name,"url":url,"status":"ACCESS_BOUNDARY_UNVERIFIED","error_class":type(e).__name__,"http_code":getattr(e,"code",None)})
 results={"schema":"TIANWEN-12WT-TOKYO-OFFICIAL-FULL-HANJI-CATALOG-FORM-INTAKE-R1",
 "status":"FIRST_PARTY_CATALOG_FORM_OR_ACCESS_BOUNDARY_NOT_ORIGINAL_LEAF",
 "source_results":summaries,"requests":len(summaries),"all_expected_requests":len(SOURCES),
 "matched_original_1827_juan20_leaf":False,"matched_1869_juan20_leaf":False,
 "authenticated_item_to_image_mapping":False,"source_absence_proven":False,
 "no_hypothetical_query_endpoint":True,"original_ancient_print_votes":0,"ocr":False}
 (out/"receipt.json").write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"status":results["status"],"acquired":[q["source"] for q in summaries if q["status"]=="PROVIDER_HTML_DIRECT"],"blocked":[q["source"] for q in summaries if q["status"]!="PROVIDER_HTML_DIRECT"],"prints":0},ensure_ascii=False))
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--output-dir",default="12wt-kanseki-source-form-output");args=a.parse_args()
 capture(args.output_dir)
