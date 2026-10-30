#!/usr/bin/env python3
"""Recompute source-native SIFT/RANSAC layout compatibility from two verified NAAJ PDF byte streams.

This script compares photographed letterform geometry; it CANNOT authenticate a historical
woodblock, physical impression date, edition, stemmatic descent or numerical rule.
Usage:
 python scripts/replay-tianwen-13lh-naaj-geometry.py /path/2810037-book10.pdf /path/2810038-book11.pdf
Requirements: pymupdf, opencv-python-headless, numpy.
"""
import hashlib,json,sys
from pathlib import Path
import cv2,fitz,numpy as np

ORIGINALS={
 "281-0037":{"sha256":"8892b16c3b8e17f12211195cf7b58acfd5b7dc0d0aefca6623f653a04d4da93e","bytes":9931786,"pages":51},
 "281-0038":{"sha256":"73322281149551c76f96008c1b9f3933e817543f7cb8710c92268ade9ca031eb","bytes":15476093,"pages":73},
}
RECTS={"left":((105,86,501,675),(132,93,502,675)),"right":((500,80,897,672),(505,90,942,668))}
PAGES=(2,5,6,7)
def original(path,identity):
    b=Path(path).read_bytes()
    expected=ORIGINALS[identity]
    assert len(b)==expected["bytes"] and hashlib.sha256(b).hexdigest()==expected["sha256"],"source PDF integrity check failed"
    d=fitz.open(stream=b,filetype="pdf")
    assert d.page_count==expected["pages"],"PDF page count mismatch"
    return d
def render(doc,n):
    pix=doc[n-1].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False,colorspace=fitz.csRGB)
    assert pix.n==3 and pix.alpha==0
    rgb=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,3)
    return cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY),hashlib.sha256(pix.samples).hexdigest()
def crop(image,xyxy):
    x1,y1,x2,y2=xyxy
    assert 0<=x1<x2<=image.shape[1] and 0<=y1<y2<=image.shape[0]
    return image[y1:y2,x1:x2]
def measure(a,b):
    sift=cv2.SIFT_create(nfeatures=5500,contrastThreshold=0.013,edgeThreshold=20)
    k1,d1=sift.detectAndCompute(a,None);k2,d2=sift.detectAndCompute(b,None)
    assert d1 is not None and d2 is not None
    matching=cv2.BFMatcher().knnMatch(d1,d2,k=2)
    good=[m for m,n in matching if m.distance<0.78*n.distance]
    assert len(good)>5
    src=np.float32([k1[m.queryIdx].pt for m in good])
    dst=np.float32([k2[m.trainIdx].pt for m in good])
    h,mask=cv2.findHomography(dst,src,cv2.RANSAC,3.5)
    assert h is not None and mask is not None
    accepted=mask.ravel().astype(bool)
    p=cv2.perspectiveTransform(dst[accepted][None],h)[0]
    distances=np.linalg.norm(p-src[accepted],axis=1)
    return {"good_matches":len(good),"ransac_inliers":int(accepted.sum()),"median_residual_px":round(float(np.median(distances)),3)}
def replay(path0037,path0038):
    left=original(path0037,"281-0037");right=original(path0038,"281-0038")
    print("CV_VERSION",cv2.__version__,file=sys.stderr)
    result={"original_sha256":{k:v["sha256"] for k,v in ORIGINALS.items()},"page_native_rgb_sha256":{"281-0037":{},"281-0038":{}},"matches":[],"proven_same_plate":False,"independent_recension_votes":0,"no_ocr":True}
    for page in PAGES:
        la,ha=render(left,page);rb,hb=render(right,page)
        result["page_native_rgb_sha256"]["281-0037"][str(page)]=ha
        result["page_native_rgb_sha256"]["281-0038"][str(page)]=hb
        for side,(ar,br) in RECTS.items():
            cv2.setRNGSeed(0)
            metric=measure(crop(la,ar),crop(rb,br))
            result["matches"].append({"pdf_page":page,"leaf":side,**metric})
    left.close();right.close()
    return result
if __name__=="__main__":
    if len(sys.argv)!=3:raise SystemExit("Provide two exact source-original PDFs: NAAJ281-0037 book10 then 281-0038 book11")
    print(json.dumps(replay(*sys.argv[1:]),ensure_ascii=False,indent=2))
