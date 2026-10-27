#!/usr/bin/env python3
"""13Q source acquisition: bounded public digital scan bytes; no source-glyph interpretation."""
import argparse, hashlib, json, time, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13Q-NLC-GORYEOSA-WORK52-GROUP40-R1.json"
MAX_BYTES=30_000_000
def entry():
    return json.loads((ROOT/E).read_text(encoding="utf8"))
def check(e):
    assert e["schema"]=="TIANWEN-13Q-NLC-WORK52-GROUP40-LOCATOR-AND-ACQUISITION-R1"
    assert e["target_work_volume"]==52 and e["priority_scan_group"]==40
    assert [(x["digital_group"],x["uploader_description_zhi_volumes"],x["commons_pdf_pages"]) for x in e["adjacent_commons_upload_pages"]]==[(39,[5],53),(40,[6],64),(41,[7],47),(42,[8,9],54)]
    assert all(x["evidence_grade"]=="COMMONS_UPLOADER_DESCRIPTION_ONLY" and not x["original_leaf_inspected"] and not x["independent_numeric_vote"] for x in e["adjacent_commons_upload_pages"])
    assert e["priority_original_pdf_url"]=="https://upload.wikimedia.org/wikipedia/commons/c/c7/NLC892-411999022809-48456_%E9%AB%98%E9%BA%97%E5%8F%B2_%E7%AC%AC40%E5%86%8A.pdf"
    assert e["original_pdf_browser_rejection_bytes"]==19799436 and not e["source_binary_downloaded_at_checkpoint"]
    assert all(e[k] is None for k in ("source_pdf_sha256","source_original_target_page","d16_original_glyph","d18_original_glyph"))
    assert not e["nlc_first_party_physical_copy_bound"] and not e["independent_crosscopy_numeric_vote"]
    assert e["source_registry_entries_added"]==e["algorithm_reopens"]==0
def fetch(u,output):
    last=None
    for attempt in range(3):
        try:
            request=urllib.request.Request(u,headers={"User-Agent":"TianwenHistoricalSourceResearch-13Q/1.0 (GitHub open research repository)"})
            size=0;sh=hashlib.sha256()
            with urllib.request.urlopen(request,timeout=120) as resp,open(output,"wb") as dest:
                if not resp.geturl().startswith("https://upload.wikimedia.org/wikipedia/commons/"):
                    raise ValueError("unexpected source redirect")
                while True:
                    data=resp.read(1024*1024)
                    if not data:break
                    size+=len(data)
                    if size>MAX_BYTES:raise ValueError("over 30MB cap")
                    dest.write(data);sh.update(data)
            with open(output,"rb") as f:signature=f.read(5)
            if size<1000000 or signature!=b"%PDF-":raise ValueError("invalid PDF")
            return size,sh.hexdigest()
        except Exception as exc:
            last=exc
            if output.exists():output.unlink()
            if attempt<2:time.sleep(4)
    raise RuntimeError("Failed public original PDF access: "+str(last))
def acquire(out):
    import fitz
    from PIL import Image,ImageDraw
    from io import BytesIO
    e=entry();check(e);out.mkdir(exist_ok=True,parents=True)
    binary=out/"commons-digital-group40-original.pdf"
    byte_count,sha256=fetch(e["priority_original_pdf_url"],binary)
    scan=fitz.open(str(binary))
    if scan.page_count!=64:raise ValueError("expected 64 pages, got "+str(scan.page_count))
    thumbnails=out/"page-thumbnails";thumbnails.mkdir(exist_ok=True)
    records=[];images=[]
    for i in range(scan.page_count):
        page=scan.load_page(i)
        factor=350/max(page.rect.width,1)
        png=page.get_pixmap(matrix=fitz.Matrix(factor,factor),alpha=False).tobytes("png")
        (thumbnails/("page-%03d.png"%(i+1))).write_bytes(png)
        images.append(Image.open(BytesIO(png)).convert("RGB"))
        records.append({"pdf_page_one_based":i+1,"thumbnail_sha256":hashlib.sha256(png).hexdigest(),"original_native_glyph_collated":False,"physical_leaf":None,"D16":None,"D18":None})
    for start in range(0,len(images),12):
        sheet=Image.new("RGB",(1260,2200),"white");pen=ImageDraw.Draw(sheet)
        for j,img in enumerate(images[start:start+12]):
            x=(j%3)*420;y=(j//3)*550
            sheet.paste(img,(x+20,y+25));pen.text((x+20,y+5),"digital PDF p.%d"%(start+j+1),fill="black")
        sheet.save(out/("contact-%02d.jpg"%(start//12+1)),quality=88)
    result={"source_url":e["priority_original_pdf_url"],"source_pdf_sha256":sha256,"source_pdf_bytes":byte_count,"pdf_pages":scan.page_count,"page_thumbnail_manifest":records,"source_digital_surrogate_acquired":True,"firstparty_physical_copy_bound":False,"native_glpyhs_read":False,"ancient_numeric_votes":0}
    (out/"acquisition-receipt.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("GORYEOSA_13Q_ORIGINAL_PDF_CAPTURE="+json.dumps({k:result[k] for k in ("source_pdf_sha256","source_pdf_bytes","pdf_pages","source_digital_surrogate_acquired","ancient_numeric_votes")}))
    scan.close()
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--output",default="goryeosa-13q-evidence");args=ap.parse_args()
    acquire(Path(args.output))
