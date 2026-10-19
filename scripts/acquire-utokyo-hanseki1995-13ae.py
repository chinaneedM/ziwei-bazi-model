#!/usr/bin/env python3
"""Bounded official UTokyo public-PDF acquisition for a 1995 bibliography, NOT historical image OCR."""
from __future__ import annotations
import hashlib,json,os,subprocess,urllib.error,urllib.request
from pathlib import Path
OUT=Path(os.environ.get("TIANWEN_13AE_OUT","utokyo-hanseki1995-13ae-evidence"))
OUT.mkdir(parents=True,exist_ok=True)
BASE="https://repository.dl.itc.u-tokyo.ac.jp/record/2010678/files/"
FILES=["kansekimokuroku_11_shibu.pdf","kansekimokuroku_12_shibu.pdf","kansekimokuroku_90_errata_1.pdf"]
MAX_BYTES=65*1024*1024
def acquire(filename):
    url=BASE+filename
    row={"file":filename,"url":url,"status":"UNKNOWN","http":None,"bytes":0,"sha256":None,"text_layer":"UNEXAMINED","candidate_lines":[],"source_item_bound":False,"original_glyph_authority":False}
    if not filename in FILES:raise ValueError("not allowlisted")
    request=urllib.request.Request(url,headers={"User-Agent":"Tianwen-Scholarly-Bibliographic-Audit/13AE (+public noncredentialed access; no retry)","Accept":"application/pdf"})
    try:
        with urllib.request.urlopen(request,timeout=45) as response:
            row["http"]=response.status
            if response.status!=200:row["status"]="HTTP_NON_200";return row
            length=response.headers.get("Content-Length")
            if length is not None and int(length)>MAX_BYTES:row["status"]="SOURCE_TOO_LARGE";return row
            path=OUT/filename; h=hashlib.sha256();count=0;start=b""
            with path.open("wb") as f:
                while True:
                    chunk=response.read(1024*1024)
                    if not chunk:break
                    count+=len(chunk)
                    if count>MAX_BYTES:row["status"]="STREAM_LIMIT";break
                    if not start:start=chunk[:8]
                    h.update(chunk);f.write(chunk)
            if row["status"]=="STREAM_LIMIT":path.unlink(missing_ok=True);return row
            row["bytes"]=count;row["sha256"]=h.hexdigest()
            if not start.startswith(b"%PDF-"):row["status"]="NOT_PDF_MAGIC";path.unlink(missing_ok=True);return row
            row["status"]="DOWNLOADED_PDF_BYTES"
            # Text layer can supply candidates only. Empty layer is not negative text proof.
            try:
                out=subprocess.run(["pdftotext","-layout",str(path),"-"],capture_output=True,text=True,timeout=90,check=False)
                if out.returncode==0:
                    text=out.stdout;row["text_layer"]="EXTRACTABLE" if text.strip() else "EMPTY_UNSEARCHABLE"
                    lines=text.splitlines()
                    row["candidate_lines"]=[{"line":i+1,"snippet":line[:190]} for i,line in enumerate(lines) if any(k in line for k in ("高麗史","高丽史","G23:12","G23:194"))][:100]
                    (OUT/(filename+".txt")).write_text(text,encoding="utf-8")
                else:row["text_layer"]="PDFTOTEXT_UNAVAILABLE_OR_UNREADABLE"
            except (OSError,subprocess.TimeoutExpired):
                row["text_layer"]="PDFTOTEXT_UNAVAILABLE_OR_UNREADABLE"
            return row
    except urllib.error.HTTPError as exc:row["http"]=exc.code;row["status"]="HTTP_RESTRICTED_OR_ERROR";return row
    except Exception as exc:row["status"]="TRANSPORT_EXCEPTION";row["error"]=f"{type(exc).__name__}: {str(exc)[:180]}";return row
def main():
    rows=[acquire(x) for x in FILES]
    evidence={"schema":"TIANWEN-13AE-UTOKYO-1995-CATALOG-ANONYMOUS-PDF-PROBE-R1","items":rows,"ocr_used":False,"historical_glyph_vote":0,"original_work52_target_folio":False}
    (OUT/"probe-result.json").write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({**evidence,"items":[{k:v for k,v in x.items() if k!="candidate_lines"} for x in rows]},ensure_ascii=False))
if __name__=="__main__":main()
