#!/usr/bin/env python3
"""12WE: bounded first-party Berlin 1827 digital-object METS/IIIF probe.

Uses one PPN emitted by an existing DDB->SBB original-view link; uses
official SBB-documented generic manifest/METS API formats. Does not guess
page numbers, harvest image files, OCR, or infer 1827/1869 paper impressions.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

PPN="PPN334378186X"
SOURCE_OBJECT="https://digital.staatsbibliothek-berlin.de/werkansicht/?PPN="+PPN
DOCUMENTATION="https://lab.sbb.berlin/dc/?lang=en"
URLS={
  "manifest":f"https://content.staatsbibliothek-berlin.de/dc/{PPN}/manifest",
  "mets":f"https://content.staatsbibliothek-berlin.de/dc/{PPN}.mets.xml",
}
MAX_RESPONSE_BYTES=12_000_000
MAX_CANVAS_COUNT=5000
USER_AGENT="Tianwen-Historical-Provenance/12WE (Berlin digital metadata scope; no OCR)"
KEYWORDS=("改造漏刻","卷二十","卷20","卷 20","juan 20","volume 20","bd. 20","band 20")

def sanctioned(url):
    u=urlparse(url)
    if u.scheme!="https" or u.hostname!="content.staatsbibliothek-berlin.de" or not u.path.startswith(f"/dc/{PPN}"):
        raise ValueError("unauthorized provider host or unsupported PPN")
    if u.path not in (f"/dc/{PPN}/manifest",f"/dc/{PPN}.mets.xml"):
        raise ValueError("not a provider-documented object metadata route")
    return url

def read_limited(url):
    sanctioned(url)
    req=urllib.request.Request(url,headers={"User-Agent":USER_AGENT,"Accept":"application/json, application/xml, text/xml, */*"})
    with urllib.request.urlopen(req,timeout=50) as response:
        if response.geturl()!=url:
            sanctioned(response.geturl())
        length=response.headers.get("Content-Length")
        if length and int(length)>MAX_RESPONSE_BYTES:
            raise ValueError("source byte limit exceeded by header")
        raw=response.read(MAX_RESPONSE_BYTES+1)
        if len(raw)>MAX_RESPONSE_BYTES:
            raise ValueError("source byte limit exceeded")
        return raw,response.headers.get("Content-Type","UNKNOWN"),response.status

def label_string(obj):
    if isinstance(obj,str):return obj
    if isinstance(obj,list):return " ".join(label_string(x) for x in obj[:8])
    if isinstance(obj,dict):return " ".join(label_string(x) for x in list(obj.values())[:8])
    return ""

def parse_manifest(raw):
    d=json.loads(raw.decode("utf-8-sig"))
    if not isinstance(d,dict):raise ValueError("non-object IIIF")
    presentation_type=d.get("type") or d.get("@type") or ""
    if "Manifest" not in str(presentation_type):raise ValueError("not an IIIF manifest")
    v2=d.get("sequences")
    if isinstance(v2,list):
        canvases=v2[0].get("canvases",[]) if v2 else []
    else:canvases=d.get("items",[])
    if not isinstance(canvases,list) or len(canvases)>MAX_CANVAS_COUNT:raise ValueError("implausible canvas count")
    matches=[]
    for i,canvas in enumerate(canvases):
        if not isinstance(canvas,dict):continue
        lab=label_string(canvas.get("label"))
        if any(k.lower() in lab.lower() for k in KEYWORDS):
            matches.append({"canvas_position_zero_based":i,"label":lab[:260],"source_canvas_id":str(canvas.get("id") or canvas.get("@id") or "")[:900]})
    structures=d.get("structures",[])
    ranges=[]
    if isinstance(structures,list):
        for x in structures[:1000]:
            lab=label_string(x.get("label")) if isinstance(x,dict) else ""
            if any(k.lower() in lab.lower() for k in KEYWORDS):
                ranges.append({"label":lab[:260],"range_id":str(x.get("id") or x.get("@id") or "")[:900]})
    return {"iiif_presentation_type":str(presentation_type),"manifest_label":label_string(d.get("label"))[:400],
      "canvas_count":len(canvases),"label_matched_canvases":matches[:30],
      "label_matched_ranges":ranges[:30],"has_source_issued_juan20_canvas_label":bool(matches),
      "target_article_original_folio_confirmed":False,
      "target_article_image_bytes_downloaded":False}

def parse_mets(raw):
    root=ET.fromstring(raw)
    if not root.tag.endswith("mets") and not root.tag.endswith("METS"):
        raise ValueError("not METS")
    counts={"file_links":0,"physical_struct_divs":0}
    labels=[]
    for node in root.iter():
        lname=node.tag.rsplit("}",1)[-1]
        if lname=="FLocat":counts["file_links"]+=1
        if lname=="div":
            counts["physical_struct_divs"]+=1
            label=node.attrib.get("LABEL","")
            if any(k.lower() in label.lower() for k in KEYWORDS):
                labels.append({"label":label[:300],"div_id":node.attrib.get("ID","")[:300]})
        if counts["file_links"]>50000 or counts["physical_struct_divs"]>50000:
            raise ValueError("METS too large")
    return {**counts,"label_matched_divs":labels[:30],
      "target_article_original_folio_confirmed":False,
      "physical_impression_date_confirmed":False}

def probe(outdir):
    out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
    rows=[]
    for kind,url in URLS.items():
        record={"kind":kind,"url":url,"status":"NOT_READ","http_status":None,
            "bytes":None,"sha256":None,"declared_content_type":None,
            "structured_metadata":None,"boundary_or_error":None}
        try:
            raw,content_type,status=read_limited(url)
            record.update({"http_status":status,"bytes":len(raw),
                "sha256":hashlib.sha256(raw).hexdigest(),"declared_content_type":content_type})
            (out/(kind+".source")).write_bytes(raw)
            record["structured_metadata"]=parse_manifest(raw) if kind=="manifest" else parse_mets(raw)
            record["status"]="SOURCE_METADATA_PARSED_TARGET_ORIGINAL_UNATTESTED"
        except urllib.error.HTTPError as e:
            record.update({"status":"PROVIDER_HTTP_BOUNDARY_NO_NEGATIVE_HOLDING_INFERENCE","http_status":e.code,"boundary_or_error":"HTTPError"})
        except (urllib.error.URLError,TimeoutError,ValueError,json.JSONDecodeError,ET.ParseError,UnicodeError) as e:
            record.update({"status":"ACCESS_OR_PARSING_BOUNDARY_NOT_NEGATIVE_HOLDING_PROOF",
                "boundary_or_error":type(e).__name__+":"+str(e)[:260]})
        rows.append(record)
    report={"schema":"TIANWEN-12WE-SBB1827-SOURCE-ISSUED-METADATA-PROBE-RESULT-R1",
      "ppn":PPN,"original_source_issued_view":SOURCE_OBJECT,"documented_public_api":DOCUMENTATION,
      "results":rows,"guessed_page_ids_or_urls":0,"original_image_files_downloaded":0,
      "ocr_used":False,"1827_original_print_impression_verified":False,
      "1869_original_print_impression_verified":False,"independent_historical_print_votes":0,
      "inspected_canvas_original_images_human_verified":0}
    (out/"probe-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":"PROBED_NO_ORIGINAL_GLYPH_VOTE","ppn":PPN,
       "results":[{"kind":x["kind"],"status":x["status"],"http":x["http_status"],
        "bytes":x["bytes"],"sha256":x["sha256"],
        "canvas_count":(x["structured_metadata"] or {}).get("canvas_count"),
        "match_ranges":(x["structured_metadata"] or {}).get("label_matched_ranges"),
        "matched_divs":(x["structured_metadata"] or {}).get("label_matched_divs")} for x in rows],
       "historical_votes":0},ensure_ascii=False))
    return report
if __name__=="__main__":
    cli=argparse.ArgumentParser()
    cli.add_argument("--output-dir",default="sbb-1827-12we")
    args=cli.parse_args()
    probe(args.output_dir)
