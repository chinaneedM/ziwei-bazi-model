#!/usr/bin/env python3
"""13BD bounded NAJ/Waseda original image acquisition and visual preview, never OCR."""
import base64, hashlib, io, json, os, re, urllib.parse, urllib.request
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/"docs/research/TIANWEN-13BD-GORYEOSA-D16-D17-ORIGINAL-MULTICOLUMN-IMAGE-PROBE-R1.json"
OUT=Path(os.environ.get("TIANWEN_13BD_OUT","goryeosa-13bd-source-capture"))
MAX_MANIFEST=1_000_000
MAX_JPEG=12_000_000
MAX_PDF=90_000_000
def sha(b):return hashlib.sha256(b).hexdigest()
def fetch(url,cap,host):
    p=urllib.parse.urlsplit(url)
    if p.scheme!="https" or p.netloc!=host or p.query or p.fragment:
        raise ValueError("unapproved source URL")
    req=urllib.request.Request(url,headers={"User-Agent":"TianwenHistoricalCollation/13BD","Accept":"*/*"})
    with urllib.request.urlopen(req,timeout=95) as r:
        if r.status!=200 or urllib.parse.urlsplit(r.geturl()).netloc!=host:raise ValueError("HTTP or redirect boundary")
        cl=r.headers.get("Content-Length")
        if cl and int(cl)>cap:raise ValueError("source limit header")
        raw=r.read(cap+1)
    if len(raw)>cap:raise ValueError("source limit body")
    return raw
def preview(key,b):
    im=Image.open(io.BytesIO(b)).convert("RGB")
    orig=im.size
    im.thumbnail((1450,1450),Image.Resampling.LANCZOS)
    buf=io.BytesIO();im.save(buf,format="JPEG",quality=76,optimize=True)
    jpg=buf.getvalue()
    (OUT/(key+"-visual-overview.jpg")).write_bytes(jpg)
    encoded=base64.b64encode(jpg).decode("ascii")
    chunks=[encoded[i:i+2800] for i in range(0,len(encoded),2800)]
    # Public, provider-issued historical images only; chunks allow lossless source preview reconstruction.
    for i,part in enumerate(chunks):
        print(f"TW13BD_IMAGE {key} {i+1}/{len(chunks)} {part}")
    return {"original_dimensions":list(orig),"preview_sha256":sha(jpg),"preview_bytes":len(jpg),"preview_chunks":len(chunks)}
def main():
    d=json.loads(RECORD.read_text(encoding="utf8"))
    a,b=d["sources"];OUT.mkdir(exist_ok=True)
    report={"schema":"TIANWEN-13BD-FIRSTPARTY-ORIGINAL-IMAGE-ACQUISITION-RECEIPT-R1","source_file":str(RECORD.relative_to(ROOT)),"images":[],"reading": "NOT_MACHINE_INFERRED_NO_OCR","no_stemmatic_votes":True}
    try:
        raw=fetch(a["manifest"],MAX_MANIFEST,"www.digital.archives.go.jp")
        if sha(raw)!=a["manifest_sha256"]:raise ValueError("manifest SHA drift")
        j=json.loads(raw)
        canvases=j["sequences"][0]["canvases"]
        if len(canvases)!=36:raise ValueError("unexpected sequence")
        url=canvases[a["provider_canvas_1based"]-1]["images"][0]["resource"]["@id"]
        p=urllib.parse.urlsplit(url)
        if p.netloc!="www.digital.archives.go.jp" or not re.fullmatch(r"/api/content/item/da12/C[0-9]+/iiif/M[0-9]+_[0-9]+[.]jp2/full/max/0/native[.]jpg",p.path):
            raise ValueError("non-source-native URL")
        original=fetch(url,MAX_JPEG,"www.digital.archives.go.jp")
        if not original.startswith(b"\xff\xd8\xff") or sha(original)!=a["existing_JPEG_sha256"]:raise ValueError("original NAJ JPEG hash drift")
        (OUT/"NAJ-original-canvas17.jpg").write_bytes(original)
        shot=preview("NAJ",original)
        if shot["original_dimensions"]!=a["expected_dimensions"]:raise ValueError("NAJ image dimension drift")
        report["images"].append({"id":a["id"],"url":url,"file":"NAJ-original-canvas17.jpg","sha256":sha(original),"bytes":len(original),**shot})
        print("TW13BD_NAJ_SOURCE_PASS")
        pdf=fetch(b["pdf"],MAX_PDF,"archive.wul.waseda.ac.jp")
        if not pdf.startswith(b"%PDF-") or sha(pdf)!=b["pdf_sha256"]:raise ValueError("Waseda PDF checksum or filetype")
        import fitz
        doc=fitz.open(stream=pdf,filetype="pdf")
        try:
            page=doc.load_page(b["original_pdf_page_1based"]-1)
            if b["embedded_JPEG_xref"] not in [x[0] for x in page.get_images(full=True)]:raise ValueError("Waseda xref not on target page")
            obj=doc.extract_image(b["embedded_JPEG_xref"])
            original2=obj["image"]
        finally:doc.close()
        if sha(original2)!=b["embedded_JPEG_sha256"]:raise ValueError("Waseda embedded image SHA drift")
        (OUT/"Waseda-original-page23-xref70.jpg").write_bytes(original2)
        shot2=preview("WASEDA",original2)
        if shot2["original_dimensions"]!=b["expected_dimensions"]:raise ValueError("Waseda image dimension drift")
        report["images"].append({"id":b["id"],"url":b["pdf"],"pdf_sha256":sha(pdf),"file":"Waseda-original-page23-xref70.jpg","sha256":sha(original2),"bytes":len(original2),**shot2})
        print("TW13BD_WASEDA_SOURCE_PASS")
    except Exception as e:
        report["error"]=type(e).__name__+": "+str(e)[:300]
    (OUT/"receipt.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("TW13BD_RECEIPT "+json.dumps({k:report.get(k) for k in ("error","reading","no_stemmatic_votes")},ensure_ascii=False))
    if report.get("error") or len(report["images"])!=2:raise SystemExit(1)
if __name__=="__main__":main()
