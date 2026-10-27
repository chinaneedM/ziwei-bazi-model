#!/usr/bin/env python3
"""12UR: inspect only source-published CText book/chapter public URLs.

No ID guessing, no login, no bypass, no images, no OCR. 403 is ACCESS_BLOCKED.
The output is a reproducible bounded probe, not a historical glyph vote.
"""
from __future__ import annotations
import argparse
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12UR-CTEXT-SCAN-PAGE-IDENTITY-PROBE-R1.json"
ALLOWED_HOST="ctext.org"
MAX_SIZE=1_200_000
class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag not in ("a","img"):return
        values=dict(attrs)
        href=values.get("href") if tag=="a" else values.get("src")
        if href:self.links.append((tag,href))
def public_image_link(url,base):
    full=urljoin(base,url)
    u=urlparse(full)
    if u.scheme!="https" or u.hostname!=ALLOWED_HOST:return None
    raw=(u.path+"?"+u.query).lower()
    if not any(t in raw for t in ("image","img","scan","file","pic","page","res=")):
        return None
    return full
def extract_links(data,base):
    p=Links()
    p.feed(data)
    return sorted({v for tag,url in p.links if (v:=public_image_link(url,base)) is not None})[:50]
def validate_ledger(d):
    if d.get("schema")!="TIANWEN-12UR-CTEXT-SCANNED-BOOK-IMAGE-IDENTITY-GATE-R1":
        raise ValueError("wrong CText evidence gate")
    assert d["known_book_url"]=="https://ctext.org/wiki.pl?if=en&res=1946940"
    assert d["known_received_chapter_url"]=="https://ctext.org/wiki.pl?chapter=418967&if=gb"
    if d["probe_policy"]["max_known_urls"]!=2 or d["probe_policy"]["maximum_html_bytes"]!=MAX_SIZE or d["probe_policy"]["scope"].find("NO_ENUMERATION")<0:
        raise ValueError("source only bounded public probe")
    if any(d[k] is not False for k in ("first_party_live_book_html_inspected_this_batch","first_party_item_image_url_bound","historical_glyph_vote","algorithm_reopen_authorized")):
        raise ValueError("unverified scan claimed as source")
    if any(d["outcome"][k]!=0 for k in ("new_external_sources","new_independent_original_witnesses","new_target_page_glyph_votes","available_source_image_count","algorithm_reopens")):
        raise ValueError("new historical vote without actual image")
    if d["prior_exhausted_german_example_source"]["total_public_sample_canvases"]!=38:
        raise ValueError("prior Berlin sample report altered")
    return {"validation":"PASS","known_urls":2,"historical_glyph_votes":0}
def probe_url(url):
    row={"requested_url":url,"outcome":"NOT_CHECKED","http_status":None,"found_source_emitted_links":[]}
    req=Request(url,headers={"User-Agent":"Tianwen-EvidenceResearch/1.0 (public metadata only; no image fetching)"})
    try:
        with urlopen(req,timeout=12) as response:
            row["http_status"]=response.status
            row["effective_url"]=response.url
            page=response.read(MAX_SIZE+1)
            if len(page)>MAX_SIZE:
                row["outcome"]="BODY_EXCEEDS_BOUNDED_LIMIT"
                return row
            row["body_sha256"]=hashlib.sha256(page).hexdigest()
            content_type=response.headers.get("Content-Type","")
            row["content_type"]=content_type.split(";")[0]
            if "text/html" not in content_type:
                row["outcome"]="NOT_PUBLIC_HTML"
                return row
            decoded=page.decode("utf-8","replace")
            if "captcha" in decoded.lower() or "verify that you" in decoded.lower():
                row["outcome"]="PUBLIC_ANTI_BOT_GATE_NO_BYPASS"
                return row
            row["found_source_emitted_links"]=extract_links(decoded,response.url)
            row["outcome"]="PUBLIC_HTML_HAS_SOURCE_LINKS" if row["found_source_emitted_links"] else "PUBLIC_HTML_NO_IMAGE_LINKS"
    except HTTPError as ex:
        row["http_status"]=ex.code
        row["outcome"]="HTTP_RESTRICTED_OR_UNAVAILABLE"
    except (URLError,TimeoutError,OSError) as ex:
        row["outcome"]="NETWORK_ERROR_OR_TIMEOUT"
        row["diagnostic"]=type(ex).__name__
    return row
def crosscheck_distinct_urls(probes):
    """Identical 200 HTML bytes for distinct CText URLs are not item verification."""
    if len(probes)!=2:return probes
    a,b=probes
    if (a.get("requested_url")!=b.get("requested_url")
            and a.get("http_status")==b.get("http_status")==200
            and a.get("body_sha256") and a["body_sha256"]==b.get("body_sha256")):
        for row in probes:
            row["outcome"]="AMBIGUOUS_IDENTICAL_HTML_SHELL"
            row["source_item_identity_proven"]=False
            row["warning"]="Distinct book and chapter URL returned byte-identical HTTP200 HTML; could be common shell, access prompt, or redirect. No historical image inference."
    else:
        for row in probes:
            row["source_item_identity_proven"]=False
    return probes
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--live",action="store_true")
    p.add_argument("--output",type=Path)
    x=p.parse_args()
    d=json.loads(LEDGER.read_text(encoding="utf-8"))
    res={"schema":"TIANWEN-12UR-CURRENT-PUBLIC-CTEXT-LINK-PROBE","baseline":validate_ledger(d),"historical_vote_authorized":False}
    if x.live:
        res["probes"]=crosscheck_distinct_urls([probe_url(url) for url in (d["known_book_url"],d["known_received_chapter_url"])])
    else:
        res["probes"]=[]
    body=json.dumps(res,ensure_ascii=False,indent=2)+"\n"
    if x.output:
        x.output.parent.mkdir(parents=True,exist_ok=True)
        x.output.write_text(body,encoding="utf-8")
    print(body)
if __name__=="__main__":main()
