#!/usr/bin/env python3
"""13MI: exact-source original G893 solar heading vs Zhou Xiang 1569 solar table.
Intake only: provider-issued images and separately fingerprinted public PDF.
NO OCR. SAME-FIELD, UNIT, EDITION AND HISTORICAL NUMERIC WINNERS UNADJUDICATED.
"""
from __future__ import annotations
import hashlib, io, json, os, re, urllib.parse, urllib.request, urllib.error
from pathlib import Path
from PIL import Image, ImageDraw

BASE = "https://kyudb.snu.ac.kr"
RENDER = BASE + "/pf01/rendererImg.do"
BOOK = "GK00893_00"
PREFIX = "/data01/stream/SIC/IMG/GK00893_00/GK00893_00_0001/"
TARGET = {"001a":"8b07513ca8aad42ae167a93f22c39f14850c8cd1c345db9ce98c1e0e769226a5",
          "002a":"31d0452e9350e32ff73549f49d894ab26f6e588654926d45b3a603ae4da9a914",
          "002b":"f9812e8c6a357eb6cd1117bb2af58d816e01030d5b93f34e7094bddb766b2b55"}
PDF = "https://www.kotenmon.com/cal/arabe/vol6.pdf"
PDF_SHA = "4c006b7ce131902fe33012d42f62cd2bbc2140affa3d5886e0da02966352cb7c"
PDF_PAGES = (7,9,14,19)
def sha(raw): return hashlib.sha256(raw).hexdigest()
class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, url):
        p=urllib.parse.urlsplit(url)
        if p.scheme!="https" or p.hostname not in {"www.kotenmon.com","kotenmon.com","kyudb.snu.ac.kr"}:
            raise ValueError("cross-origin redirect refused")
        return super().redirect_request(req,fp,code,msg,headers,url)
OPENER=urllib.request.build_opener(SafeRedirect)
def get(req,limit,timeout=45):
    with OPENER.open(req,timeout=timeout) as r:
        if r.status!=200: raise ValueError("non-200 status")
        raw=r.read(limit+1)
        if not raw or len(raw)>limit: raise ValueError("empty or oversized source payload")
        return raw
def source_page(page):
    form=urllib.parse.urlencode({"item_cd":"SIC","book_cd":BOOK,"vol_no":"0001",
                               "page_no":page,"tool":"1"}).encode()
    html=get(urllib.request.Request(RENDER,data=form,method="POST",
        headers={"User-Agent":"Mozilla/5.0 Tianwen13MI/1.0",
                 "Content-Type":"application/x-www-form-urlencoded",
                 "Referer":BASE+"/book/view.do?book_cd="+BOOK}),1000000)
    expected_path=PREFIX + f"GK00893_00IH_0001_{page}.jpg"
    values=re.findall(r'''(?:var\s+)?imgFileNm\s*=\s*["']([^"']+)["']''',
                      html.decode("utf-8","replace"))
    if expected_path not in values: raise ValueError("official renderer did not issue expected full path")
    url=BASE+"/ImageServlet.do?"+urllib.parse.urlencode({
        "imgFileNm": expected_path.rsplit("/",1)[-1], "path": expected_path})
    b=get(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 Tianwen13MI/1.0",
                                              "Accept":"image/jpeg","Referer":RENDER}),3000000)
    if sha(b)!=TARGET[page]:raise ValueError("original source hash drift")
    im=Image.open(io.BytesIO(b));im.load()
    if im.format!="JPEG" or im.size!=(1150,2000):raise ValueError("unexpected source image")
    rgb=im.convert("RGB")
    return b,{"page":page,"status":"EXACT_PROVIDER_JPEG_VERIFIED",
              "source_issued":True,"renderer_html_sha256":sha(html),"source_url":url,
              "filename":f"G893-{page}.jpg","sha256":sha(b),
              "rgb_sha256":sha(rgb.tobytes()),"pixels":[1150,2000],"bytes":len(b)}

def main():
    dest=Path(os.environ.get("TIANWEN_13MI_OUT","/tmp/tianwen-13mi"))
    dest.mkdir(parents=True,exist_ok=True)
    result={"schema":"TIANWEN-13MI-G893-SOLAR-HEADER-MING1569-ORIGINAL-BOUND-R1",
     "type":"SOURCE_ACQUISITION_NOT_TEXTUAL_ADJUDICATION","no_ocr":True,
     "g893_original":{"book":BOOK,"identity_exact_prior_hashes":TARGET,"pages":[]},
     "ming1569":{"source_url":PDF,"expected_pdf_sha256":PDF_SHA,
                 "status":"NOT_ACQUIRED","render_selected_pages":list(PDF_PAGES)},
     "comparison":{"same_field":False,"same_units":False,"same_day_index":False,
        "independent_original_numeric_decisions":0,"g893_six_historical_winners_added":0,
        "printed_original_少_vs_微":"NOT_ADJUDICATED_BY_INTAKE",
        "source_crosswalk":"NOT_ADJUDICATED","physical_editions_same_copy":False,
        "calendar_engine_change":False}}
    acquired={}
    for page in TARGET:
        failures=[]
        ok=False
        for attempt in (1,2,3):
            try:
                b,record=source_page(page);(dest/f"G893-{page}.jpg").write_bytes(b)
                record["attempt_count"]=attempt
                record["prior_access_boundaries"]=failures
                result["g893_original"]["pages"].append(record)
                acquired[page]=Image.open(io.BytesIO(b)).convert("RGB")
                ok=True
                break
            except Exception as e:
                failures.append({"attempt":attempt,"error":type(e).__name__+": "+str(e)[:220]})
        if not ok:
            result["g893_original"]["pages"].append({"page":page,"status":"ACCESS_OR_HASH_BOUNDARY",
                           "attempt_count":len(failures),"attempts":failures,"source_issued":False})
    if acquired:
        canvas=Image.new("RGB",(len(acquired)*430,760),"white");d=ImageDraw.Draw(canvas)
        for i,(page,img) in enumerate(acquired.items()):
            small=img.copy();small.thumbnail((390,675))
            canvas.paste(small,(i*430+15,45))
            d.text((i*430+15,12),"G893 "+page+" (source JPEG, no OCR)",fill="black")
        canvas.save(dest/"g893-contact.jpg",quality=92)
    try:
        pdf=get(urllib.request.Request(PDF,headers={"User-Agent":"Mozilla/5.0 Tianwen13MI/1.0"}),
                60000000,timeout=85)
        if sha(pdf)!=PDF_SHA:raise ValueError("public 1569 PDF SHA mismatch")
        import fitz
        doc=fitz.open(stream=pdf,filetype="pdf")
        if len(doc)!=45:raise ValueError("1569 PDF expected 45 pages")
        result["ming1569"].update(status="ORIGINAL_PRINT_PUBLIC_PDF_HASH_VERIFIED",
                                  pages=len(doc),sha256=sha(pdf),bytes=len(pdf))
        (dest/"zhouxiang-1569-vol6-original.pdf").write_bytes(pdf)
        rendered=[]
        for page in PDF_PAGES:
            pg=doc[page-1]
            pix=pg.get_pixmap(matrix=fitz.Matrix(2,2),colorspace=fitz.csRGB,alpha=False)
            im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
            name=f"zhouxiang-1569-vol6-p{page:02d}.png"
            im.save(dest/name,optimize=True)
            rendered.append({"page":page,"filename":name,"pixels":[im.width,im.height],
                             "image_png_sha256":sha((dest/name).read_bytes()),
                             "rgb_sha256":sha(im.tobytes())})
        result["ming1569"]["renders"]=rendered
    except Exception as e:
        result["ming1569"].update(status="SOURCE_PDF_ACCESS_OR_SHA_BOUNDARY",
                                  error=type(e).__name__+": "+str(e)[:250])
    a=sum(x["status"]=="EXACT_PROVIDER_JPEG_VERIFIED" for x in result["g893_original"]["pages"])
    b=result["ming1569"]["status"]=="ORIGINAL_PRINT_PUBLIC_PDF_HASH_VERIFIED"
    result["status"]="BOTH_OBJECTS_SOURCE_BOUND_UNCOLLATED" if a==3 and b else (
        "PARTIAL_ACCESS_BOUNDARY_UNCOLLATED" if a or b else "ALL_SOURCE_ACCESS_BOUNDARY")
    (dest/"source-report.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"g893_verified":a,
                      "ming1569_pdf_verified":b,"crosswitness_winners":0},ensure_ascii=False))
    if not (a or b):raise SystemExit(2)
if __name__=="__main__":main()
