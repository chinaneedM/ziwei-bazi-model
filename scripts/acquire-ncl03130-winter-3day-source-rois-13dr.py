#!/usr/bin/env python3
"""13DR: fixed original-pixel ROI for solar winter D15–D17 source columns.

Only a source-image visual-collation aid; never silently reads OCR, assumes a
stemmatically independent physical witness, or substitutes arithmetic glyphs.
"""
import base64, hashlib, io, json
from pathlib import Path
from urllib.parse import urlsplit
import fitz, requests
from PIL import Image, ImageDraw

URL = "https://commons.wikimedia.org/wiki/Special:Redirect/file/NCL-03130_09_%E9%AB%98%E9%BA%97%E5%8F%B2.pdf"
PDF_SHA = "3c2a5621fb3f4eabc593020bcde12a38f6ecdae2842940dec12d5a3a56afd32e"
PDF_BYTES = 50735589
OUT = Path("ncl03130-13dr-day15-17-native-rois")
COLUMNS = {"D17":(.078,.16,.145,.92), "D16":(.142,.16,.209,.92),
           "D15":(.206,.16,.274,.92)}
def sha(data):return hashlib.sha256(data).hexdigest()

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    m={"schema":"TIANWEN-13DR-NCL03130-WINTER-D15-D17-SOURCE-PIXELS-R1",
       "source_url":URL,"pdf_sha256":PDF_SHA,"source_status":"COMMONS_MIRROR_NCL_FIRSTPARTY_ITEM_UNVERIFIED",
       "pdf_page":66,"original_physical_stratum":"UNBOUND",
       "same_copy_repeat_not_independent_witness":True,"manual_glyph_adjudication":"NOT_YET_DONE",
       "no_ocr":True,"fields":[],"status":"INITIAL"}
    try:
        h=hashlib.sha256();size=0;chunks=[]
        with requests.get(URL,stream=True,timeout=(30,180),allow_redirects=True,
                          headers={"User-Agent":"TianwenHistoricalResearch/1.0"}) as response:
            response.raise_for_status()
            p=urlsplit(response.url)
            if p.scheme!="https" or p.hostname not in ("commons.wikimedia.org","upload.wikimedia.org"):
                raise RuntimeError("untrusted file redirect")
            for chunk in response.iter_content(1048576):
                if not chunk:continue
                size+=len(chunk)
                if size>60_000_000:raise RuntimeError("source cap exceeded")
                h.update(chunk);chunks.append(chunk)
        raw=b"".join(chunks)
        if size!=PDF_BYTES or h.hexdigest()!=PDF_SHA or raw[:5]!=b"%PDF-":
            raise RuntimeError("original PDF sha/byte identity changed")
        d=fitz.open(stream=raw,filetype="pdf")
        if d.is_encrypted or len(d)!=189:raise RuntimeError("189 page contract violated")
        pix=d[65].get_pixmap(matrix=fitz.Matrix(2.6,2.6),alpha=False)
        image=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
        m.update(source_rgb_sha256=sha(pix.samples),native_dimensions=[pix.width,pix.height])
        panels=[]
        for name,r in COLUMNS.items():
            x0,y0,x1,y1=r
            bb=(int(x0*image.width),int(y0*image.height),
                int(x1*image.width),int(y1*image.height))
            roi=image.crop(bb)
            raw_pixels=roi.tobytes()
            buff=io.BytesIO();roi.save(buff,format="PNG");png=buff.getvalue()
            fname=f"p066-{name}-source-column.png"
            (OUT/fname).write_bytes(png)
            m["fields"].append({"name":name,"source_page":66,"relative_roi":list(r),
               "native_bbox":list(bb),"native_dimensions":list(roi.size),
               "source_rgb_sha256":sha(raw_pixels),"png_sha256":sha(png),
               "file":fname,"glyph_status":"ORIGINAL_PIXELS_REQUIRE_MANUAL_READING"})
            # Interpolated enlargement is navigation only, not additional source pixels.
            view=roi.resize((roi.width*3,roi.height*2),Image.Resampling.NEAREST)
            panels.append((name,view))
        w=sum(x.width+20 for _,x in panels);height=max(x.height for _,x in panels)+65
        combined=Image.new("RGB",(w,height),"white");draw=ImageDraw.Draw(combined)
        at=0
        for name,part in panels:
            draw.text((at+10,10),f"PDF66 {name}: IMAGE-ONLY ORIGINAL GLYPHS",fill="black")
            combined.paste(part,(at+8,40));at+=part.width+20
        dest=io.BytesIO();combined.save(dest,format="JPEG",quality=92,optimize=True)
        data=dest.getvalue();(OUT/"navigation-D15-D17.jpg").write_bytes(data)
        m["visualization_jpeg_sha256"]=sha(data)
        m["status"]="SOURCE_SHA_VERIFIED_NATIVE_CROPS_CAPTURED_UNREAD"
        print("13DR_JPEG_BEGIN",len(data),flush=True)
        print(base64.b64encode(data).decode("ascii"),flush=True)
        print("13DR_JPEG_END",flush=True)
        print("13DR_SOURCE_PASS",PDF_SHA,size,len(d),flush=True)
    except Exception as e:
        m.update(status="SOURCE_ACCESS_OR_RENDER_BOUNDARY",error_type=type(e).__name__,error=str(e)[:240])
        raise
    finally:
        (OUT/"manifest.json").write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
