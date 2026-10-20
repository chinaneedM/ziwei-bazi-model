#!/usr/bin/env python3
"""Bounded first-party NAJDA source-emitted link probe; not a manuscript glyph reader."""
import hashlib, json, os, re, unicodedata
import urllib.parse, urllib.request, urllib.error
from html.parser import HTMLParser
from pathlib import Path

SOURCE = "https://www.digital.archives.go.jp/search?fond=1073275&lang=en&page=1"
OUT = Path(os.environ.get("TIANWEN_13AP_OUT","najda-goryeosa-13ap-evidence"))
CAP = 1500000
class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.current=[]; self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=="a":
            href=dict(attrs).get("href","")
            self.current.append({"href":href,"text":[]})
    def handle_data(self,data):
        for link in self.current:link["text"].append(data)
    def handle_endtag(self,tag):
        if tag=="a" and self.current:
            x=self.current.pop()
            x["text"]="".join(x["text"])
            self.links.append(x)

def exact_item_links(html):
    parser=Links();parser.feed(html)
    hits=[]
    for entry in parser.links:
        title=unicodedata.normalize("NFKC",re.sub(r"\\s+","",entry["text"]))
        raw=entry["href"]
        url=urllib.parse.urljoin(SOURCE,raw)
        p=urllib.parse.urlparse(url)
        if title=="高麗史52" and p.scheme=="https" and p.netloc=="www.digital.archives.go.jp" and re.fullmatch(r"/item/[0-9]+",p.path):
            hits.append(url)
    return sorted(set(hits))

def capture(url,name):
    row={"url":url,"http":None,"outcome":"UNREAD","bytes":0,"sha256":None}
    request=urllib.request.Request(url,headers={"User-Agent":"Tianwen-Research-13AP/1.0 (bounded academic source check)","Accept":"text/html"})
    try:
        with urllib.request.urlopen(request,timeout=25) as response:
            row["http"]=response.status
            if response.status!=200:
                row["outcome"]="HTTP_NON_200";return row,None
            length=response.headers.get("Content-Length")
            if length and int(length)>CAP:
                row["outcome"]="TOO_LARGE";return row,None
            raw=response.read(CAP+1)
            if len(raw)>CAP:
                row["outcome"]="STREAM_LIMIT";return row,None
            row["bytes"]=len(raw);row["sha256"]=hashlib.sha256(raw).hexdigest()
            row["outcome"]="HTML_CAPTURED"
            OUT.mkdir(parents=True,exist_ok=True)
            (OUT/name).write_bytes(raw)
            return row,raw.decode("utf-8","replace")
    except urllib.error.HTTPError as exc:
        row["http"]=exc.code;row["outcome"]="HTTP_RESTRICTED_OR_ERROR"
    except Exception as exc:
        row["outcome"]="TRANSPORT_ERROR";row["error"]=type(exc).__name__+":"+str(exc)[:120]
    return row,None

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    primary,body=capture(SOURCE,"official-fond-index.html")
    links=exact_item_links(body) if body is not None else []
    rows=[]
    # Public source-emitted links only. Never enumerate numeric IDs or infer dates from link shapes.
    for url in links[:2]:
        row,_=capture(url,"exact-book52-item.html")
        rows.append(row)
    result={"schema":"TIANWEN-13AP-NAJDA-BOUND-ACCESS-REPLAY-R1",
            "source":primary,"source_emitted_book52_item_links":links,
            "item_details":rows,"original_work52_folio_read":False,
            "book52_equals_work_volume52":"UNKNOWN",
            "independent_numeric_votes_added":0,
            "no_endpoint_guessing":True,
            "no_ocr":True,
            "access_result_must_not_close_issue":True}
    (OUT/"probe-result.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
