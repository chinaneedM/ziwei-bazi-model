#!/usr/bin/env python3
"""12WT bounded first-party Tokyo IOC General KANSEKI catalogue home receipt.

One source-verified HTTP GET. Extract HTML search forms, inputs, JS and links;
NO invented item URL, automatic search, image download or glyph/print vote.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

LANDING="https://kanseki.ioc.u-tokyo.ac.jp/user/index.php"
MAX_BYTES=500_000
ALLOWED_HOST="kanseki.ioc.u-tokyo.ac.jp"
UA="Tianwen/12WT source-bounded Chinese-books-general-catalogue navigation audit (no OCR)"
class Entry(HTMLParser):
    def __init__(self):
        super().__init__()
        self.forms=[];self.current_form=None;self.current_select=None
        self.links=[];self.scripts=[];self.frames=[];self.text=[];self.images=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="form":
            f={"method":a.get("method","get").upper(),"action":a.get("action"),
               "name":a.get("name"),"id":a.get("id"),"inputs":[],"selects":[]}
            self.forms.append(f);self.current_form=f
        elif tag=="input" and self.current_form is not None:
            self.current_form["inputs"].append({k:a.get(k) for k in ("name","id","type","value","onclick") if a.get(k) is not None})
        elif tag=="select" and self.current_form is not None:
            d={"name":a.get("name"),"id":a.get("id"),"options":[]}
            self.current_form["selects"].append(d);self.current_select=d
        elif tag=="option" and self.current_select is not None:
            self.current_select["options"].append(a.get("value"))
        elif tag=="a" and a.get("href"):
            self.links.append({"href":a.get("href"),"title":a.get("title")})
        elif tag=="script":
            if a.get("src"):self.scripts.append(a["src"])
        elif tag in ("frame","iframe"):
            if a.get("src"):self.frames.append({"tag":tag,"src":a["src"]})
        elif tag=="img":
            self.images.append({k:a.get(k) for k in ("src","alt","title") if a.get(k) is not None})
    def handle_endtag(self,tag):
        if tag=="form":self.current_form=None;self.current_select=None
        if tag=="select":self.current_select=None
    def handle_data(self,data):self.text.append(data)
def exact_url(url):
    p=urlparse(url)
    if p.scheme!="https" or p.hostname!=ALLOWED_HOST or p.path!="/user/index.php" or p.query:
        raise ValueError("only provider-issued general catalogue landing is in scope")
    return True
def parse(original):
    if len(original)>MAX_BYTES:raise ValueError("oversize source HTML")
    p=Entry();p.feed(original.decode("utf-8",errors="replace"))
    text=" ".join(p.text)
    relative=lambda u:urljoin(LANDING,u)
    return {
       "schema":"TIANWEN-12WT-TOKYO-IOC-GENERAL-CHINESE-CATALOGUE-FIRSTPARTY-ENTRY-R1",
       "source_url":LANDING,
       "raw_original_html_sha256":hashlib.sha256(original).hexdigest(),
       "raw_original_html_bytes":len(original),
       "forms":p.forms,
       "source_emitted_anchor_urls":[{"url":relative(x["href"]),"title":x["title"]} for x in p.links[:120]],
       "source_emitted_script_urls":[relative(u) for u in p.scripts[:40]],
       "source_emitted_frame_urls":[{"tag":x["tag"],"url":relative(x["src"])} for x in p.frames[:30]],
       "source_emitted_image_element_count":len(p.images),
       "visible_title_mentioned":"漢籍目錄" in text or "漢籍目録" in text,
       "item_6403767830_explicitly_bound":False,
       "item_6403148395_explicitly_bound":False,
       "juan20_original_paper_scan_acquired":False,
       "official_volume_item_search_executed":False,
       "source_image_glyphs_read":0,
       "historical_independent_print_votes":0,
       "no_ocr":True,
       "scope_note":"General library catalogue navigation only. HTML controls/links cannot prove an item-specific digitized leaf or edition print state."
    }
def capture(output):
    d=Path(output);d.mkdir(parents=True,exist_ok=True)
    try:
        exact_url(LANDING)
        req=Request(LANDING,headers={"User-Agent":UA,"Accept":"text/html"})
        with urlopen(req,timeout=35) as r:
            exact_url(r.geturl())
            raw=r.read(MAX_BYTES+1)
        record=parse(raw)
        (d/"kanseki-index-original.html").write_bytes(raw)
        (d/"entry-receipt.json").write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(json.dumps({"result":"ORIGINAL_PROVIDER_GENERAL_CATALOGUE_HTML","bytes":len(raw),
                          "forms":len(record["forms"]),"scripts":len(record["source_emitted_script_urls"]),
                          "source_images":0,"paper_votes":0},ensure_ascii=False))
        return record
    except Exception as e:
        (d/"access-boundary.json").write_text(json.dumps({"status":"NO_PROVIDER_SOURCE_ORIGINAL_CAPTURED",
        "error_class":type(e).__name__,"http_status":getattr(e,"code",None),"ancient_print_votes":0},
        ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        raise
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--output-dir",default="12wt-kanseki-original")
    a=ap.parse_args();capture(a.output_dir)
