#!/usr/bin/env python3
"""12WC: bounded, no-OCR original Commons duplicate-upload comparison. No print vote."""
import argparse,hashlib,json,subprocess,urllib.parse,urllib.request,tempfile
from pathlib import Path
from urllib.parse import urlparse

API="https://commons.wikimedia.org/w/api.php"
ITEMS=(
  {"title":"File:野獲編(十六).djvu","label":"old","expected_bytes":3400790},
  {"title":"File:CADAL02096915 野獲編（十六）.djvu","label":"new","expected_bytes":3495009,
   "expected_sha256":"262edac806b90c984d5f0c4fce1bc150a974ebd574d847738a08a00cad39640d"}
)
MAX_SOURCE_BYTES=8_000_000
PAGES=(121,122)
USER_AGENT="Tianwen-public-facsimile-audit/12WC (Wikimedia original-source verification; no OCR)"
def check_url(url,host,path_prefix):
    u=urlparse(url)
    if u.scheme!="https" or u.hostname!=host or not u.path.startswith(path_prefix):
        raise ValueError("unexpected source host or path")
def digest(path,kind):
    h=hashlib.new(kind)
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1_048_576),b""):h.update(b)
    return h.hexdigest()
def resolve(item):
    q=urllib.parse.urlencode({"action":"query","prop":"imageinfo","iiprop":"url|size|sha1","format":"json","formatversion":"2","titles":item["title"]})
    request=urllib.request.Request(API+"?"+q,headers={"User-Agent":USER_AGENT})
    with urllib.request.urlopen(request,timeout=45) as f:
        result=json.load(f)
    pages=result.get("query",{}).get("pages",[])
    if len(pages)!=1 or "imageinfo" not in pages[0] or len(pages[0]["imageinfo"])!=1:
        raise ValueError("source-emitted file identity is absent")
    info=pages[0]["imageinfo"][0]
    check_url(info["url"],"upload.wikimedia.org","/wikipedia/commons/")
    if info["size"]!=item["expected_bytes"]:
        raise ValueError("source API bytes disagree with file-inventory boundary")
    if len(info.get("sha1",""))!=40:
        raise ValueError("source API sha1 unavailable")
    return info
def download(item,info,path):
    request=urllib.request.Request(info["url"],headers={"User-Agent":USER_AGENT})
    n=0
    with urllib.request.urlopen(request,timeout=65) as f,Path(path).open("wb") as out:
        check_url(f.geturl(),"upload.wikimedia.org","/wikipedia/commons/")
        for block in iter(lambda:f.read(1_048_576),b""):
            n+=len(block)
            if n>MAX_SOURCE_BYTES:raise ValueError("source exceeds 8MB bound")
            out.write(block)
    if n!=info["size"] or digest(path,"sha1")!=info["sha1"]:
        raise ValueError("actual original SHA1/byte size mismatch")
    if item.get("expected_sha256") and digest(path,"sha256")!=item["expected_sha256"]:
        raise ValueError("known 12VZ original SHA256 mismatch")
    with Path(path).open("rb") as f:
        if f.read(8)!=b"AT&TFORM":raise ValueError("source not DJVU binary")
    return {"source_url":info["url"],"bytes":n,"sha1":digest(path,"sha1"),"sha256":digest(path,"sha256")}
def pagecount(path):
    r=subprocess.run(["djvused",str(path),"-e","n"],capture_output=True,text=True,check=True)
    n=int(r.stdout.strip())
    if not 2<n<500:raise ValueError("unexpected DjVu page count")
    return n
def render(path,n,output):
    from PIL import Image
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td)/"page.ppm"
        subprocess.run(["ddjvu","-format=ppm",f"-page={n}",str(path),str(tmp)],check=True,timeout=45)
        with Image.open(tmp) as im:
            gray=im.convert("L")
            dims=list(gray.size)
            pixels_sha256=hashlib.sha256(gray.tobytes()).hexdigest()
            preview=gray.resize((256,384),Image.Resampling.BILINEAR)
            preview.save(output,format="PNG")
            return {"page":n,"dimensions":dims,"raw_grayscale_pixel_sha256":pixels_sha256,
                    "preview_png_sha256":digest(output,"sha256"),"preview_png":Path(output).name,
                    "preview_256x384":list(preview.getdata())}
def compare_pages(a,b):
    if a is None or b is None:return {"comparison":"PAGE_OUT_OF_RANGE_NO_ABSENCE_CLAIM"}
    aa=a["preview_256x384"];bb=b["preview_256x384"]
    mean_abs_diff=round(sum(abs(x-y) for x,y in zip(aa,bb))/len(aa),5)
    return {"comparison":"COMPUTED_DIGITAL_PIXEL_RELATIONSHIP_ONLY",
            "same_exact_decoded_grayscale_pixels":a["raw_grayscale_pixel_sha256"]==b["raw_grayscale_pixel_sha256"] and a["dimensions"]==b["dimensions"],
            "mean_abs_grayscale_difference_256x384":mean_abs_diff,
            "historical_original_paper_or_impression_identity":"UNBOUND"}
def execute(outdir):
    output=Path(outdir);output.mkdir(parents=True,exist_ok=True)
    sources=[];pages={}
    for item in ITEMS:
        label=item["label"]
        original=output/(label+".djvu")
        info=resolve(item)
        src=download(item,info,original)
        src["label"]=label;src["source_title"]=item["title"]
        src["pages_count"]=pagecount(original)
        src["selected_page_images"]=[]
        for n in PAGES:
            if n>src["pages_count"]:continue
            image=render(original,n,output/f"{label}-p{n}.png")
            pages[(label,n)]=image
            src["selected_page_images"].append({k:v for k,v in image.items() if k!="preview_256x384"})
        sources.append(src)
    result={"schema":"TIANWEN-12WC-CADAL-SAME-ID-ORIGINAL-DIGITAL-ALIASES-ATLAS-R1",
       "status":"ORIGINAL_DIGITAL_FILE_AND_IMAGE_RELATIONSHIP_NO_HISTORICAL_COPY_ATTESTATION",
       "capture_method":"COMMONS_SOURCE_EMITTED_IMAGEINFO_URL_AND_DIGEST_NOT_OCR",
       "sources":sources,
       "selected_pages":{str(n):compare_pages(pages.get(("old",n)),pages.get(("new",n))) for n in PAGES},
       "ancient_1827_1869_print_votes":0,"edition_date_bound":False,
       "physical_copy_identity_bound":False,"target_glyph_recollation_human_approved":False,"ocr_used":False}
    (output/"atlas.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"sources":[{"label":x["label"],"bytes":x["bytes"],"sha256":x["sha256"],"pages":x["pages_count"]} for x in sources],"pixel_comparisons":result["selected_pages"],"ancient_print_votes":0},ensure_ascii=False))
    return result
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output-dir",default="cadal-alias-12wc-output")
    args=p.parse_args()
    try:execute(args.output_dir)
    except Exception as e:
        out=Path(args.output_dir);out.mkdir(parents=True,exist_ok=True)
        (out/"capture-error.json").write_text(json.dumps({"status":"CAPTURE_FAILED_NO_GLYPH_VOTE","error":type(e).__name__+":"+str(e),"ancient_print_votes":0},ensure_ascii=False))
        raise
if __name__=="__main__":main()
