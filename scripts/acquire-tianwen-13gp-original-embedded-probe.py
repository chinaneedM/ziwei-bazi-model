#!/usr/bin/env python3
"""13GP source acquisition probe: exact PDF bytes, PDF image affine, expanded native crops.

Outputs are candidate regions only. Their content never certifies a historical
number without separate date/field/gutter and edition-scoped adjudication.
"""
import base64
import hashlib
import io
import json
import math
import os
from pathlib import Path
from urllib.parse import urlsplit

import fitz
import requests
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GN = ROOT / "docs/research/TIANWEN-13GN-NCL03130-EMBEDDED-IMAGE-GRADE-ERRATUM-R1.json"
GO = ROOT / "docs/research/TIANWEN-13GO-NCL03130-EMBEDDED-ROI-COVERAGE-AUDIT-R1.json"
OUT = Path(os.environ.get("TIANWEN_PROBE_OUT", "ncl-13gp-source-probe"))

def sha(b):
    return hashlib.sha256(b).hexdigest()

def get_bytes(url, expected_size, expected_hash):
    h = hashlib.sha256()
    chunks, size = [], 0
    with requests.get(url, stream=True, allow_redirects=True, timeout=(30,180),
                      headers={"User-Agent": "TianwenHistoricalResearch/1.0"}) as r:
        r.raise_for_status()
        host = urlsplit(r.url).hostname
        if urlsplit(r.url).scheme != "https" or host not in ("commons.wikimedia.org", "upload.wikimedia.org"):
            raise AssertionError("untrusted PDF redirect: " + repr(host))
        for chunk in r.iter_content(1024*1024):
            if chunk:
                chunks.append(chunk)
                size += len(chunk)
                if size > expected_size:
                    raise AssertionError("unexpected PDF length")
                h.update(chunk)
    b = b"".join(chunks)
    assert len(b) == expected_size and h.hexdigest() == expected_hash and b.startswith(b"%PDF-")
    return b

def map_old_bbox_to_embedded(bbox, page, placement, size, zoom=3.1):
    # Page.get_image_rects(transform=True) returns a unit-image -> page-space
    # transform; invert it, then scale normalized coordinates to source pixels.
    unit_to_page = fitz.Matrix(placement)
    page_to_unit = ~unit_to_page
    corners = [(bbox[i]/zoom, bbox[j]/zoom) for i,j in ((0,1),(2,1),(0,3),(2,3))]
    xy = []
    for x,y in corners:
        u = fitz.Point(x + page.rect.x0, y + page.rect.y0) * page_to_unit
        xy.append((u.x*size[0],u.y*size[1]))
    xs=[p[0] for p in xy];ys=[p[1] for p in xy]
    return [math.floor(min(xs)),math.floor(min(ys)),math.ceil(max(xs)),math.ceil(max(ys))],xy

def run():
    gn=json.loads(GN.read_text(encoding="utf8"))
    go=json.loads(GO.read_text(encoding="utf8"))
    OUT.mkdir(parents=True,exist_ok=True)
    pdfbytes=get_bytes(gn["source"]["url"],gn["source"]["bytes"],gn["source"]["sha256"])
    result={"schema":"TIANWEN-13GP-ORIGINAL-JPEG-AFFINE-ROI-ACQUISITION-REPORT-R1",
            "source_pdf_sha256":sha(pdfbytes),"source_bytes":len(pdfbytes),
            "scope":"TWO_PAGES_SAME_DIGITAL_SURROGATE_NO_NEW_PHYSICAL_WITNESS",
            "geometry_grade":"SOURCE_PDF_XOBJECT_AFFINE_WITHOUT_INDEPENDENT_GLYPH_FIDUCIALS",
            "complete_original_literals":{"D9":None,"D14":None,"D30":None},
            "new_historical_glyph_assertions":0, "images":[]}
    with fitz.open(stream=pdfbytes,filetype="pdf") as pdf:
        assert len(pdf)==gn["source"]["pages"]==189
        for row in go["cases"]:
            target=row["target"]
            if target=="D9":
                continue
            page_number=row["page"]
            page=pdf[page_number-1]
            sealed=next(x for x in gn["pages"] if x["page"]==page_number)
            xref=sealed["embedded"]["xref"]
            image_obj=pdf.extract_image(xref)
            data=image_obj["image"]
            assert len(data)==sealed["embedded"]["jpeg_bytes"] and sha(data)==sealed["embedded"]["jpeg_sha256"]
            im=Image.open(io.BytesIO(data)).convert("RGB")
            assert list(im.size)==sealed["embedded"]["size"] and sha(im.tobytes())==sealed["embedded"]["rgb_sha256"]
            placements=page.get_image_rects(xref,transform=True)
            assert len(placements)==1, ("unexpected image placement count",len(placements))
            rect,m=placements[0]
            render=page.get_pixmap(matrix=fitz.Matrix(3.1,3.1),alpha=False)
            assert list((render.width,render.height))==sealed["previous_render"]["size"]
            assert sha(render.samples)==sealed["previous_render"]["rgb_sha256"]
            mapped,corners=map_old_bbox_to_embedded(row["prior_render_union_xyxy"],page,m,im.size)
            wanted=row["proposed_followup_embedded_probe_xyxy"]
            expanded=[min(mapped[0]-8,wanted[0]),min(mapped[1]-8,wanted[1]),
                      max(mapped[2]+8,wanted[2]),max(mapped[3]+8,wanted[3])]
            expanded=[max(0,expanded[0]),max(0,expanded[1]),
                      min(im.width,expanded[2]),min(im.height,expanded[3])]
            assert expanded[2]>expanded[0] and expanded[3]>expanded[1]
            # Keep bounded source pixels: no rescale, no sharpen, no OCR.
            crop=im.crop(expanded)
            bio=io.BytesIO()
            crop.save(bio,format="PNG",compress_level=9)
            png=bio.getvalue()
            fname=f"p{page_number:03d}-{target.lower()}-expanded-embedded.png"
            (OUT/fname).write_bytes(png)
            entry={"target":target,"pdf_page":page_number,"xref":xref,
                   "render_bbox_3_1":row["prior_render_union_xyxy"],
                   "prior_ratio_projection":row["ratio_projected_xyxy"],
                   "actual_pdf_affine_projection_candidate":mapped,
                   "source_box_xyxy":expanded,
                   "normalized_to_page_matrix":[m.a,m.b,m.c,m.d,m.e,m.f],
                   "image_placement_rect":[rect.x0,rect.y0,rect.x1,rect.y1],
                   "pixel_corner_coordinates":corners,
                   "image_filename":fname,"png_sha256":sha(png),"png_bytes":len(png),
                   "rgb_sha256":sha(crop.tobytes()),"pixel_grid":"PDF_EMBEDDED_JPEG_NATIVE_RGB",
                   "historical_field_certified":False,"complete_original_literal":None}
            result["images"].append(entry)
            print("13GP_BOUNDED_SOURCE "+json.dumps({k:v for k,v in entry.items() if k not in ("pixel_corner_coordinates",)},ensure_ascii=False),flush=True)
            if os.environ.get("TIANWEN_LOG_IMAGE_BASE64")=="1":
                print("13GP_PNG_BASE64_"+target+"="+base64.b64encode(png).decode("ascii"),flush=True)
    (OUT/"manifest.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("13GP_PASS_ACQUISITION_GEOMETRY_NOT_GLYPH_GRADE",sha(pdfbytes),len(result["images"]),flush=True)
if __name__=="__main__":
    run()
