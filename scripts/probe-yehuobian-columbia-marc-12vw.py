#!/usr/bin/env python3
"""12VW: bounded first-party Columbia MARCXML shard title-candidate probe.

A positive title match is bibliographic only; a single shard nonhit is not an
institution-wide absence finding. Never promote MARC to an ancient glyph vote.
"""
import argparse
import gzip
import hashlib
import json
import re
import tempfile
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT_URL="https://lito.cul.columbia.edu/extracts/ColumbiaLibraryCatalog/full/"
TITLE_TAGS={"130","240","245","246","730","880"}
MAX_BYTES=80_000_000
MAX_RESULTS=100

def localname(tag):
    return tag.rsplit("}",1)[-1]

def title_candidate(strings):
    orig=" ".join(strings)
    if any(x in orig for x in ("野獲編","野获编","野獲","野获")):
        return True
    low=unicodedata.normalize("NFKC",orig).casefold()
    simplified=re.sub(r"[^a-z0-9]+"," ",low)
    compact=re.sub(r"[^a-z0-9]","",low)
    return any(x in compact for x in ("yehuobian","yehuopien","yehhuopian","wanliyehuo","wanliyehhuo")) or bool(re.search(r"\\b(?:ye|yeh)\\s+huo\\s+(?:bian|pien)\\b",simplified))

def parse_record(elem):
    titles=[]
    fields=[]
    id001=None
    publication=[]
    holdings=[]
    for child in elem:
        tag=localname(child.tag)
        if tag=="controlfield":
            if child.get("tag")=="001":id001=(child.text or "").strip()
            continue
        if tag!="datafield":continue
        code=child.get("tag","")
        subs=[{"code":s.get("code",""),"text":(s.text or "").strip()} for s in child if localname(s.tag)=="subfield"]
        if code in TITLE_TAGS:
            combined=" ".join(x["text"] for x in subs)
            titles.append(combined)
            fields.append({"tag":code,"subfields":subs})
        elif code in ("260","264","852","853","863","866","876"):
            small=" ".join(x["text"] for x in subs)[:500]
            (holdings if code in ("852","853","863","866","876") else publication).append({"tag":code,"text":small})
    if not title_candidate(titles):return None
    return {"marc_001":id001,"title_fields":fields,"publication_fields":publication,"holding_fields":holdings,
            "claim_status":"TITLE_CANDIDATE_ONLY_REQUIRES_FIRSTPARTY_ITEM_ID_COPY_AND_VOLUME_CHECK",
            "original_1827_1869_juan20_page":None,"historical_glyph_votes":0}

def scan_gz(path,max_results=MAX_RESULTS):
    count=0
    matched=0
    entries=[]
    with gzip.open(path,"rb") as fh:
        context=ET.iterparse(fh,events=("start","end"))
        _,root=next(context)
        for event,elem in context:
            if event=="end" and localname(elem.tag)=="record":
                count+=1
                result=parse_record(elem)
                if result is not None:
                    matched+=1
                    if len(entries)<max_results:entries.append(result)
                elem.clear()
                root.clear()
    return {"record_count":count,"matched_title_records":matched,"results_returned":len(entries),"results_truncated":matched>len(entries),"title_candidates":entries}

def sha256_file(path):
    result=hashlib.sha256()
    with Path(path).open("rb") as fh:
        for part in iter(lambda:fh.read(1024*1024),b""):result.update(part)
    return result.hexdigest()

def download_one(shard,output):
    if not isinstance(shard,int) or not 1<=shard<=111:raise ValueError("shard must be between 1 and 111")
    url=ROOT_URL+f"extract-{shard:03d}.xml.gz"
    req=urllib.request.Request(url,headers={"User-Agent":"TIANWEN-SOURCE-AUDIT/12VW (public MARCXML; research)"})
    transferred=0
    with urllib.request.urlopen(req,timeout=45) as resp,Path(output).open("wb") as file:
        for part in iter(lambda:resp.read(1024*1024),b""):
            transferred+=len(part)
            if transferred>MAX_BYTES:raise ValueError("compressed shard exceeds bounded 80 MB")
            file.write(part)
    return url,transferred

def report(path,source_url=None):
    path=Path(path)
    if path.stat().st_size>MAX_BYTES:raise ValueError("compressed shard exceeds bounded 80 MB")
    data=scan_gz(path)
    return {"schema":"TIANWEN-12VW-MARC-ONE-SHARD-PROBE-RESULT-R1",
            "status":"BOUNDED_SINGLE_SHARD_SCANNED",
            "source_url":source_url,"source_sha256":sha256_file(path),
            "compressed_bytes":path.stat().st_size,
            "shards_scanned":1,"publisher_index_shards":111,
            "whole_catalog_searched":False,"catalog_absence_inference_allowed":False,
            "physical_copy_identity_proven":False,"original_juan20_image_found":False,
            "ancient_glyph_votes":0,**data}

def main():
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input-gz",type=Path)
    group.add_argument("--download-shard",type=int)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    if args.input_gz is not None:
        out=report(args.input_gz)
    else:
        with tempfile.TemporaryDirectory() as dirname:
            source=Path(dirname)/"one.xml.gz"
            url,_=download_one(args.download_shard,source)
            out=report(source,url)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in out.items() if k!="title_candidates"},ensure_ascii=False))
if __name__=="__main__":main()
