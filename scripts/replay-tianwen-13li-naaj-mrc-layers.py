#!/usr/bin/env python3
"""Read exact MRC/JPX/JBIG2 image layers of two hash-verified NAAJ originals.

Does not perform OCR or assert that JBIG2-reconstructed pixels certify physical
woodblock strokes, impression dates, or text/edition independence.
Usage:
 python scripts/replay-tianwen-13li-naaj-mrc-layers.py original-2810037-book010.pdf naaj-281-0038-shi11-13-original.pdf
Requires pymupdf.
"""
import hashlib,json,sys
from pathlib import Path
import fitz
EXPECTED={
 "281-0037":{"sha256":"8892b16c3b8e17f12211195cf7b58acfd5b7dc0d0aefca6623f653a04d4da93e","pages":51,"mask_roi":[3277,472,3566,3955]},
 "281-0038":{"sha256":"73322281149551c76f96008c1b9f3933e817543f7cb8710c92268ade9ca031eb","pages":73,"mask_roi":[3383,499,3738,4044]}
}
def source(path,holding):
    b=Path(path).read_bytes()
    assert hashlib.sha256(b).hexdigest()==EXPECTED[holding]["sha256"],"source original SHA256 does not match prior evidence"
    doc=fitz.open(stream=b,filetype="pdf")
    assert doc.page_count==EXPECTED[holding]["pages"]
    return doc
def snapshot(path,holding):
    doc=source(path,holding)
    p=doc[5]
    imglist=p.get_images(full=True)
    assert len(imglist)>=4
    layers=[]
    for role,info in zip(("BACKGROUND","TEXT_MASK","FOREGROUND"),imglist[1:4]):
        xref=info[0];descriptor=doc.xref_object(xref,compressed=False)
        filterName="JBIG2Decode" if "/JBIG2Decode" in descriptor else "JPXDecode" if "/JPXDecode" in descriptor else "OTHER"
        layers.append({"role":role,"xref":xref,"width":info[2],"height":info[3],"bits":info[4],"colorspace":info[5],"filter":filterName,"has_soft_mask":"/SMask" in descriptor})
    assert [x["xref"] for x in layers]==[32,33,34]
    assert [x["filter"] for x in layers]==["JPXDecode","JBIG2Decode","JPXDecode"]
    mask=fitz.Pixmap(doc,layers[1]["xref"])
    assert mask.n==1 and mask.alpha==0
    raw=mask.samples
    assert len(raw)==mask.width*mask.height
    roi=EXPECTED[holding]["mask_roi"]
    x1,y1,x2,y2=roi
    crop=b"".join(raw[y*mask.width+x1:y*mask.width+x2] for y in range(y1,y2))
    result={"holding":holding,"producer":doc.metadata["producer"],"creationDate":doc.metadata["creationDate"],"pdf_rect":[round(p.rect.width,2),round(p.rect.height,2)],"layers":layers,"mask_decoded_gray_sha256":hashlib.sha256(raw).hexdigest(),"target_crop_xyxy":roi,"target_crop_gray_sha256":hashlib.sha256(crop).hexdigest(),"historical_woodblock_identity_proven":False,"lossy_jbig2_substitution_proven":False,"no_ocr":True}
    doc.close()
    return result
if __name__=="__main__":
    if len(sys.argv)!=3:raise SystemExit("Pass two source-original PDF paths: 281-0037 then 281-0038")
    print(json.dumps([snapshot(sys.argv[1],"281-0037"),snapshot(sys.argv[2],"281-0038")],ensure_ascii=False,indent=2))
