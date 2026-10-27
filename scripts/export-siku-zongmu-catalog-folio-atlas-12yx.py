#!/usr/bin/env python3
"""12YX non-OCR original-catalog scan retrieval for SSID卷106 and NLC第50冊.

Outputs replayable source hashes, all-page rendered image fingerprints, atlas sheets,
and selected full-scale page JPEGs. No automatically asserted historical glyph,
impression chronology, textual identity, or independent physical witness.
"""
from __future__ import annotations
import base64
import hashlib
import io
import json
import urllib.parse
import urllib.request
from pathlib import Path
import fitz
from PIL import Image, ImageDraw

OUT = Path("research-12yx-siku-catalog")
OUT.mkdir(exist_ok=True)
SOURCES = [
    {
        "id": "SSID-11564461",
        "filename": "SSID-11564461 欽定四庫全書總目 第106卷.pdf",
        "expected_pages": 101,
        "provider_reported_size": 8724887,
        "provider_reported_sha1": "1a355a64336198573a0bd9495997e30889be4fbe",
        "catalogue_provenance": "COMMONS_SINGLE_UNATTRIBUTED_SCAN_NO_VERIFIED_PHYSICAL_PRINT_DATE",
    },
    {
        "id": "NLC892-001945406-317607",
        "filename": "NLC892-001945406-317607 欽定四庫全書總目 二百卷，卷首四卷 第50冊.pdf",
        "expected_pages": 103,
        "provider_reported_size": None,
        "provider_reported_sha1": None,
        "catalogue_provenance": "NLC_CATALOGUED_QIANLONG_WUYINGDIAN_COPY_FASCICLE50_CONTAINS_JUAN105_106",
    },
]
source_records = []
for source in SOURCES:
    name = source["filename"]
    url = "https://commons.wikimedia.org/wiki/Special:Redirect/file/" + urllib.parse.quote(name, safe="")
    source_folder = OUT / source["id"]
    source_folder.mkdir(exist_ok=True)
    original = source_folder / "original.pdf"
    req = urllib.request.Request(url, headers={"User-Agent": "TianwenHistoricalSourceReplay/12YX (public-domain catalog scan; no OCR)"})
    h1, h256, count = hashlib.sha1(), hashlib.sha256(), 0
    with urllib.request.urlopen(req, timeout=180) as stream, original.open("wb") as writer:
        while True:
            b = stream.read(1 << 20)
            if not b:
                break
            writer.write(b)
            h1.update(b)
            h256.update(b)
            count += len(b)
    with original.open("rb") as rd:
        if rd.read(5) != b"%PDF-":
            raise ValueError(f"source is not PDF: {source['id']}")
    if source["provider_reported_size"] is not None and count != source["provider_reported_size"]:
        raise ValueError(f"provider declared bytes changed: {source['id']} {count}")
    if source["provider_reported_sha1"] is not None and h1.hexdigest() != source["provider_reported_sha1"]:
        raise ValueError(f"provider SHA1 differs: {source['id']}")
    source_row = {
        "source_id": source["id"],
        "source_title": name,
        "source_redirect_url": url,
        "source_file_bytes": count,
        "source_sha1_computed": h1.hexdigest(),
        "source_sha256_computed": h256.hexdigest(),
        "source_original_pdf_path_in_artifact": str(original),
        "catalogue_provenance": source["catalogue_provenance"],
        "catalogue_impression_year_from_scan": "UNVERIFIED",
        "page_printed_glyphs_authenticated_by_automation": 0,
        "ocr_used": False,
        "pdf_renderer": "PyMuPDF",
        "rendered_page_records": [],
        "contact_sheet_files": [],
    }
    pdf = fitz.open(original)
    if len(pdf) != source["expected_pages"]:
        raise ValueError(f"source page count changed {source['id']}: {len(pdf)}")
    source_row["pdf_page_count"] = len(pdf)
    thumb_entries = []
    for index, page in enumerate(pdf):
        render = page.get_pixmap(matrix=fitz.Matrix(1.0, 1.0), colorspace=fitz.csRGB, alpha=False)
        rgb = render.samples
        im = Image.frombytes("RGB", (render.width, render.height), rgb)
        th = im.copy()
        th.thumbnail((153, 265), resample=Image.Resampling.LANCZOS)
        page_rec = {
            "pdf_page_zero_based": index,
            "viewer_page_one_based": index + 1,
            "rendered_RGB_size": [render.width, render.height],
            "rendered_RGB_sha256": hashlib.sha256(rgb).hexdigest(),
            "source_pdf_sha256_binding": source_row["source_sha256_computed"],
            "render_engine_scoped_not_native_embedded_image_pixels": True,
        }
        if source["id"] == "NLC892-001945406-317607" and 40 <= index <= 102 and index % 2 == 0:
            export = source_folder / f"original_render_p{index+1:03d}.jpg"
            im.save(export, quality=85, subsampling=0)
            page_rec["raster_jpeg"] = str(export)
            page_rec["raster_jpeg_sha256"] = hashlib.sha256(export.read_bytes()).hexdigest()
        elif source["id"] == "SSID-11564461" and index in (86, 87, 88, 89):
            export = source_folder / f"original_render_p{index+1:03d}.jpg"
            im.save(export, quality=90, subsampling=0)
            page_rec["raster_jpeg"] = str(export)
            page_rec["raster_jpeg_sha256"] = hashlib.sha256(export.read_bytes()).hexdigest()
        source_row["rendered_page_records"].append(page_rec)
        thumb_entries.append(th)
        if (index + 1) % 10 == 0:
            print("12YX VERIFIED_PAGE_RENDER", source["id"], index + 1, "/", len(pdf), flush=True)
    pdf.close()
    for sheet_i, start in enumerate(range(0, len(thumb_entries), 20), 1):
        subset = thumb_entries[start:start + 20]
        atlas = Image.new("RGB", (5 * 180, 4 * 310), (255, 255, 255))
        draw = ImageDraw.Draw(atlas)
        for j, im in enumerate(subset):
            x, y = (j % 5) * 180, (j // 5) * 310
            atlas.paste(im, (x + (180 - im.width) // 2, y + 27))
            draw.text((x + 8, y + 8), f"{source['id']} p{start+j+1:03d}", fill=(0, 0, 0))
        output = source_folder / f"atlas_{sheet_i:02d}_p{start+1:03d}-{start+len(subset):03d}.jpg"
        atlas.save(output, quality=58, optimize=True)
        jpeg_bytes = output.read_bytes()
        source_row["contact_sheet_files"].append({
            "filename": str(output), "page_start": start + 1,
            "page_end": start + len(subset), "sha256": hashlib.sha256(jpeg_bytes).hexdigest(),
        })
        # JPEG previews are diagnostic only. Their image contents do not count as
        # native printed glyph adjudication or independent physical source copies.
        print("TIANWEN_12YX_ATLAS_B64", source["id"], sheet_i,
              base64.b64encode(jpeg_bytes).decode("ascii"), flush=True)
    source_records.append(source_row)
    print("12YX SOURCE_SHA", source["id"], count, h1.hexdigest(), h256.hexdigest(),
          "PAGES", len(thumb_entries), flush=True)
manifest = {
    "schema": "TIANWEN-12YX-SIKU-ZONGMU-SOURCE-ACQUISITION-AND-NON_OCR_ATLAS-R1",
    "evidence_grade": "DIGITAL_SOURCE_BYTE_HASH_AND_RENDERED_PAGE_PIXELS_NOT_YET_HUMAN_TARGET_GLYPH_ADJUDICATION",
    "date": "2026-10-17",
    "sources": source_records,
    "separate_historical_physical_prints_proven": False,
    "source_file_sha256_not_same_as_historical_impression_authentication": True,
    "target_glyph_count_certified": 0,
    "genetic_lineage_edges_added": 0,
    "algorithm_reopens": 0,
}
(OUT / "source-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("12YX SOURCE-IMAGE-ATLAS EXPORT COMPLETE NO OCR; no source-copy year, first-party leaf, or numeric rule adjudication", flush=True)
