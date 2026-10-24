#!/usr/bin/env python3
"""13FH: catalog-visible scope of SNU GK05553_00 / Goryeosa juan52.

Only source-named first-party page. Does NOT infer book number from work juan.
"""
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request

URL = "https://kyudb.snu.ac.kr/book/view.do?book_cd=GK05553_00"
OUT = Path(os.environ.get("TIANWEN_PROBE_OUT", "/tmp/tianwen-13fh-catalog"))
LIMIT = 1_400_000
MARKERS = [
    "GK05553_00", "奎貴5553", "奎貴 5553", "奎 5553", "乙亥字",
    "46冊", "46책", "139卷", "139권", "第8", "第26", "第29",
    "卷52", "卷五十二", "권52", "卷50-52", "卷50", "M/F74-102-17",
    "원문 이미지", "목차 정보", "마이크로필름"
]
class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.attrs = []
    def handle_data(self, d):
        if d.strip(): self.parts.append(d.strip())
    def handle_starttag(self, tag, attrs):
        if tag in ("a", "button", "input", "select"):
            d = dict(attrs)
            found = {k:v[:350] for k,v in d.items()
                     if k in ("href","onclick","data-book","data-src","data-target","id")
                     and isinstance(v,str)}
            if found: self.attrs.append({"element":tag, "attrs":found})
def bounded_context(s, needle, limit=4, flank=180):
    out = []
    at = 0
    while len(out)<limit:
        idx = s.find(needle, at)
        if idx<0: break
        out.append({"literal":needle,"offset":idx,
                    "context":s[max(0,idx-flank):min(len(s),idx+len(needle)+flank)]})
        at = idx + len(needle)
    return out
def microfilm_literals(s):
    return sorted(set(re.findall(r"M/F74-102-17-[1-7]", s)))
def read():
    result = {"url":URL, "http":None, "sha256":None,"bytes":0,"status":None}
    try:
        req = urllib.request.Request(URL, headers={
            "User-Agent":"Tianwen-13FH-SNU-Catalog-Scope-Audit/1.0",
            "Accept":"text/html,application/xhtml+xml;q=0.9"})
        with urllib.request.urlopen(req,timeout=24) as resp:
            result["http"] = resp.status
            u = urllib.parse.urlsplit(resp.geturl())
            if u.scheme!="https" or u.hostname!="kyudb.snu.ac.kr":
                result["status"]="REDIRECT_NOT_FIRST_PARTY"
                return result,None
            raw = resp.read(LIMIT+1)
            result["bytes"]=len(raw)
            if len(raw)>LIMIT:
                result["status"]="OVERSIZE"
                return result,None
            result["sha256"]=hashlib.sha256(raw).hexdigest()
            result["status"]="PUBLIC_HTML_CAPTURED"
            return result,raw
    except urllib.error.HTTPError as exc:
        result["http"]=exc.code
        result["status"]="HTTP_ERROR"
    except Exception as exc:
        result["status"]="TRANSPORT_ERROR"
        result["exception_type"]=type(exc).__name__
    return result,None

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    req,data = read()
    result = {
        "schema":"TIANWEN-13FH-SNU-GK05553-CATALOG-BOOK-VOLUME-MAPPING-BOUNDARY-R1",
        "date":"2026-10-24",
        "issue_id":"TW-OPEN-0005",
        "request":req,
        "literal_contexts":[],
        "literal_microfilm_group_ids":[],
        "source_emitted_buttons_and_links":[],
        "registered_catalog_identity":"GK05553_00",
        "work_juan_target":52,
        "physical_book_ordinal":None,
        "work_juan_to_physical_book_mapping_certified":False,
        "specific_image_to_mf_copy_certified":False,
        "ancient_glyph_votes_added":0,
        "independent_ancient_source_records_added":0
    }
    if data:
        (OUT/"official-catalog-page.html").write_bytes(data)
        markup = data.decode("utf-8","replace")
        parsed = Text()
        parsed.feed(markup)
        plain = " ".join(parsed.parts)
        result["parsed_text_length"]=len(plain)
        result["literal_contexts"]=[
            hit for marker in MARKERS for hit in bounded_context(plain,marker,limit=3)]
        result["literal_microfilm_group_ids"]=microfilm_literals(plain)
        result["source_emitted_buttons_and_links"]=[
            e for e in parsed.attrs
            if any(k in str(e) for k in ("5553","view","book","M/F","menu"))][:25]
        result["literal_juan52_contexts"]=bounded_context(plain,"卷52",limit=5)
    (OUT/"catalog-boundary.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":req["status"],"sha256":req["sha256"],
      "context_count":len(result["literal_contexts"]),
      "microfilm_groups":result["literal_microfilm_group_ids"],
      "ju52_contexts":result.get("literal_juan52_contexts",[]),
      "physical_book_number":result["physical_book_ordinal"]},ensure_ascii=False))
    assert result["ancient_glyph_votes_added"]==0 and result["physical_book_ordinal"] is None

if __name__=="__main__":
    main()
