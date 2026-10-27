#!/usr/bin/env python3
"""12WG: first-party 1827 Berlin sample object coverage and national census landing.

This is a bounded METADATA-ONLY audit, not 1827/1869 physical-source adjudication.
All object identifiers and source endpoints were emitted by source institution.
"""
from __future__ import annotations
import argparse,hashlib,json,urllib.request,urllib.error,xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

PPN="PPN334378186X"
MANIFEST="https://content.staatsbibliothek-berlin.de/dc/"+PPN+"/manifest"
METS="https://content.staatsbibliothek-berlin.de/dc/"+PPN+".mets.xml"
NLC="https://gjpc.nlc.cn/xlsworkbench/publish"
EXPECTED={
  "manifest":(69638,"db26dd7d790c66faddc46ce542354396a30a1bb1bba70b9be011e6d57db27b82"),
  "mets":(73209,"c30688453d2c9540be407805b9c41d88ffc4e716d0bcb8dd0fdea9349c2cb9d8")
}
MAX_BYTES=12_000_000
MAX_NLC_BYTES=500_000
TARGETS=("卷二十","卷20","改造漏刻","juan 20","volume 20","20. band")
HEADERS={"User-Agent":"TIANWEN-12WG-source-provenance-verifier/1.0","Accept":"application/json,application/xml,text/xml,text/html,*/*"}
def checked_source(url,kind):
    p=urlparse(url)
    if kind=="nlc":
        if url!=NLC:raise ValueError("NLC host / route not first-party landing page")
    elif kind in ("manifest","mets"):
        if url!={"manifest":MANIFEST,"mets":METS}[kind]:raise ValueError("wrong exact provider-issued PPN")
    else:raise ValueError("unrecognized source category")
    if p.scheme!="https":raise ValueError("HTTPS required")
    return url
def read(url,kind,cap,timeout=35):
    checked_source(url,kind)
    with urllib.request.urlopen(urllib.request.Request(url,headers=HEADERS),timeout=timeout) as r:
        final=r.geturl()
        if final!=url:checked_source(final,kind)
        n=r.headers.get("Content-Length")
        if n and int(n)>cap:raise ValueError("declared response size exceeds budget")
        data=r.read(cap+1)
        if len(data)>cap:raise ValueError("response exceeds budget")
        return data,r.status,r.headers.get("Content-Type","")
def textlabel(x):
    if isinstance(x,str):return x
    if isinstance(x,list):return " ".join(textlabel(y) for y in x[:20])
    if isinstance(x,dict):return " ".join(textlabel(y) for y in list(x.values())[:10])
    return ""
def selected_label(s):
    return any(w.lower() in s.lower() for w in TARGETS)
def iiif_analysis(raw):
    obj=json.loads(raw.decode("utf-8-sig"))
    if not isinstance(obj,dict) or "Manifest" not in str(obj.get("type") or obj.get("@type") or ""):raise ValueError("not a IIIF manifest")
    sc=obj.get("sequences")
    canvases=sc[0].get("canvases",[]) if isinstance(sc,list) and sc else obj.get("items",[])
    if not isinstance(canvases,list) or len(canvases)>5000:raise ValueError("canvas out of bounds")
    rows=[]
    for k,canvas in enumerate(canvases):
        if not isinstance(canvas,dict):continue
        iid=canvas.get("id") or canvas.get("@id") or ""
        if not isinstance(iid,str):iid=""
        label=textlabel(canvas.get("label"))
        images=canvas.get("images",[])
        items=canvas.get("items",[])
        urls=[]
        for ann in images[:3] if isinstance(images,list) else []:
            resource=ann.get("resource",{}) if isinstance(ann,dict) else {}
            v=resource.get("@id") or resource.get("id")
            if isinstance(v,str):urls.append(v)
        for p in items[:2] if isinstance(items,list) else []:
            for ann in p.get("items",[])[:3] if isinstance(p,dict) else []:
                body=ann.get("body",{}) if isinstance(ann,dict) else {}
                v=body.get("id") or body.get("@id") if isinstance(body,dict) else None
                if isinstance(v,str):urls.append(v)
        rows.append({"ordinal":k+1,"canvas_id":iid[:600],"label":label[:200],
            "image_resource_urls_from_source":[u[:700] for u in urls[:3]],"keyword_label_hit":selected_label(label)})
    structures=obj.get("structures",[])
    ranges=[]
    for elem in structures[:3000] if isinstance(structures,list) else []:
        if not isinstance(elem,dict):continue
        label=textlabel(elem.get("label"))
        ranges.append({"id":str(elem.get("id") or elem.get("@id") or "")[:500],
            "label":label[:240],"keyword_hit":selected_label(label)})
    return {"manifest_label":textlabel(obj.get("label"))[:450],
      "iiif_type":str(obj.get("type") or obj.get("@type")),"canvas_count":len(rows),
      "canvas_labels":[x["label"] for x in rows],
      "canvas_summary":rows,
      "structures_count":len(ranges),"ranges":ranges,
      "target_keyword_canvas_label_hits":[{"ordinal":x["ordinal"],"label":x["label"]} for x in rows if x["keyword_label_hit"]],
      "target_keyword_range_hits":[x for x in ranges if x["keyword_hit"]],
      "declared_target_folio_image_human_verified":False}
def mets_analysis(raw):
    root=ET.fromstring(raw)
    if root.tag.rsplit("}",1)[-1].lower()!="mets":raise ValueError("not METS")
    maps=[];total_div=0;file_count=0
    for child in root:
        kind=child.tag.rsplit("}",1)[-1]
        if kind=="fileSec":
            for n in child.iter():
                if n.tag.rsplit("}",1)[-1]=="file":file_count+=1
        elif kind=="structMap":
            divisions=[]
            for n in child.iter():
                if n.tag.rsplit("}",1)[-1]=="div":
                    total_div+=1
                    label=n.attrib.get("LABEL","")
                    divisions.append({"type":n.attrib.get("TYPE","")[:120],
                        "id":n.attrib.get("ID","")[:160],
                        "label":label[:250],
                        "order_label":n.attrib.get("ORDERLABEL","")[:140],
                        "target_keyword_hit":selected_label(label)})
            maps.append({"type":child.attrib.get("TYPE",""),"label":child.attrib.get("LABEL",""),"divs":divisions[:1000]})
    return {"structmap_count":len(maps),"all_div_count":total_div,"files_count":file_count,
      "maps":maps[:15],"target_keyword_div_hits":[x for m in maps for x in m["divs"] if x["target_keyword_hit"]][:40],
      "target_article_original_page_human_verified":False}
def audit(output):
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    outcome={"schema":"TIANWEN-12WG-SBB-1827-PREVIEW-METADATA-COVERAGE-AND-NLC-LANDING-R1",
      "ppn":PPN,"source_issue_only":True,"ocr_used":False,"page_image_fetch_count":0,
      "manual_1827_1869_glyph_votes":0,"physical_impression_attestation":False,"sources":{}}
    for kind,url in (("manifest",MANIFEST),("mets",METS),("nlc",NLC)):
        cap=MAX_NLC_BYTES if kind=="nlc" else MAX_BYTES
        row={"url":url,"status":"NOT_FETCHED","http_status":None,"source_bytes":None,
          "sha256":None,"source_content_type":None,"analysis":None,"boundary":None}
        try:
            data,code,ctype=read(url,kind,cap,timeout=12 if kind=="nlc" else 35)
            row.update({"http_status":code,"source_bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),
                        "source_content_type":ctype})
            (out/(kind+".source")).write_bytes(data)
            if kind in EXPECTED:
                expected_len,expected_sha=EXPECTED[kind]
                if (len(data),row["sha256"])!=(expected_len,expected_sha):
                    row["status"]="SOURCE_MUTATED_SINCE_12WF_NO_AUTHORITY_UPGRADE"
                else:
                    row["analysis"]=iiif_analysis(data) if kind=="manifest" else mets_analysis(data)
                    row["status"]="VERIFIED_SAME_FIRSTPARTY_METADATA_BYTES_NO_ORIGINAL_LEAF"
            else:
                row["status"]="LANDING_FETCHED_NO_ITEM_QUERY_PERFORMED"
                row["analysis"]={"may_contain_simple_web_app_shell":True,
                  "target_title_query_performed":False,"target_catalog_item_found":False}
        except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError,ValueError,ET.ParseError,json.JSONDecodeError,UnicodeError) as e:
            row.update({"status":"ACCESS_OR_SOURCE_PARSE_BOUNDARY_NO_ABSENCE_INFERENCE",
                        "http_status":getattr(e,"code",None),"boundary":type(e).__name__+":"+str(e)[:250]})
        outcome["sources"][kind]=row
    (out/"coverage-atlas.json").write_text(json.dumps(outcome,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    short={}
    for kind,row in outcome["sources"].items():
        info=row.get("analysis") or {}
        short[kind]={"status":row["status"],"http":row["http_status"],
           "bytes":row["source_bytes"],"sha256":row["sha256"],
           "canvas_count":info.get("canvas_count"),"canvas_labels":info.get("canvas_labels"),
           "structures_count":info.get("structures_count"),"range_labels":[z["label"] for z in info.get("ranges",[])][:80],
           "structmap_types":[z["type"] for z in info.get("maps",[])],
           "top_div_labels":[z["label"] for m in info.get("maps",[]) for z in m.get("divs",[])][:90],
           "keyword_hits":info.get("target_keyword_canvas_label_hits") or info.get("target_keyword_div_hits") or []}
    print(json.dumps({"status":"FIRSTPARTY_SCOPE_INSTRUMENTED_NO_PRINT_VOTE","run_measures":short,
        "new_original_1827_1869_juan20_pages":0,"original_print_votes":0},ensure_ascii=False))
    return outcome
if __name__=="__main__":
    cli=argparse.ArgumentParser()
    cli.add_argument("--output-dir",default="sbb-12wg-coverage")
    audit(cli.parse_args().output_dir)
