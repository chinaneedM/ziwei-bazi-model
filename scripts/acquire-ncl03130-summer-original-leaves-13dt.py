#!/usr/bin/env python3
"""13DT: hash-bound NCL-03130 part09 solar-summer original-page collation intake.

Source-native photographic page images for a HUMAN reading of headings and D27-30.
Zero OCR. Do not assume the output row/day offset, original hand, copy independence,
NCL first-party exact item or a preferred emended numeric reading.
"""
import base64
import hashlib
import io
import json
from pathlib import Path
from urllib.parse import urlsplit

import fitz
import requests
from PIL import Image

URL = "https://commons.wikimedia.org/wiki/Special:Redirect/file/NCL-03130_09_%E9%AB%98%E9%BA%97%E5%8F%B2.pdf"
SHA = "3c2a5621fb3f4eabc593020bcde12a38f6ecdae2842940dec12d5a3a56afd32e"
BYTES = 50_735_589
PDF_PAGES = 189
TARGET = tuple(range(81, 91))
OUTPUT = Path("ncl03130-13dt-original-summer-source")
MAX_BYTES = 60_000_000


def digest(data):
    return hashlib.sha256(data).hexdigest()


def fetch_original():
    size = 0
    parts = []
    h = hashlib.sha256()
    with requests.get(URL, stream=True, timeout=(30, 180), allow_redirects=True,
                      headers={"User-Agent": "TianwenHistoricalResearch/1.0"}) as response:
        response.raise_for_status()
        loc = urlsplit(response.url)
        if loc.scheme != "https" or loc.hostname not in ("upload.wikimedia.org", "commons.wikimedia.org"):
            raise RuntimeError("untrusted source redirect")
        for buf in response.iter_content(1024 * 1024):
            if not buf:
                continue
            size += len(buf)
            if size > MAX_BYTES:
                raise RuntimeError("source exceeded size gate")
            h.update(buf)
            parts.append(buf)
    raw = b"".join(parts)
    if size != BYTES or h.hexdigest() != SHA or raw[:5] != b"%PDF-":
        raise RuntimeError("original source PDF identity or format drift")
    return raw


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    report = {
        "schema": "TIANWEN-13DT-NCL03130-PART09-SUMMER-PAGE-ORIGINAL-R1",
        "source_url": URL, "source_pdf_sha256": SHA, "source_pdf_expected_bytes": BYTES,
        "source_class": "WIKIMEDIA_MIRROR_NOT_NCL_FIRSTPARTY_ITEM_AUTHENTICATION",
        "scope": "SOURCE_PHOTOGRAPH_PAGES_81_TO_90_HEADING_AND_TABLE_SEARCH",
        "no_ocr": True, "target_summer_day28_value": "UNREAD",
        "day_label_mapping": "UNRESOLVED",
        "physical_copy_layer": "UNBOUND",
        "single_source_not_multiple_independent_witnesses": True,
        "pages": [], "status": "INITIAL"
    }
    try:
        raw = fetch_original()
        pdf = fitz.open(stream=raw, filetype="pdf")
        if pdf.is_encrypted or len(pdf) != PDF_PAGES:
            raise RuntimeError("original pages/encryption contract changed")
        report["observed_page_count"] = len(pdf)
        for page_no in TARGET:
            pg = pdf[page_no - 1]
            pix = pg.get_pixmap(matrix=fitz.Matrix(2.6, 2.6), alpha=False)
            source_rgb = pix.samples
            png = pix.tobytes("png")
            png_name = f"original-p{page_no:03d}.png"
            (OUTPUT / png_name).write_bytes(png)
            im = Image.open(io.BytesIO(png)).convert("RGB")
            im.thumbnail((2000, 1550))
            buf = io.BytesIO()
            im.save(buf, format="JPEG", quality=88, optimize=True)
            jpg = buf.getvalue()
            jpg_name = f"preview-p{page_no:03d}.jpg"
            (OUTPUT / jpg_name).write_bytes(jpg)
            report["pages"].append({
                "pdf_page": page_no, "native_dimensions": [pix.width, pix.height],
                "raw_rgb_sha256": digest(source_rgb), "native_png": png_name,
                "native_png_sha256": digest(png), "preview_file": jpg_name,
                "preview_sha256": digest(jpg),
                "heading": "UNREAD", "summer_xingdu_day28": "UNREAD",
                "grade": "SOURCE_IMAGE_CAPTURED_PENDING_MANUAL_GLYPH_READING"
            })
            print("13DT_PAGE_BEGIN", page_no, len(jpg), flush=True)
            print(base64.b64encode(jpg).decode("ascii"), flush=True)
            print("13DT_PAGE_END", page_no, flush=True)
        report["status"] = "SHA_VERIFIED_SOURCE_IMAGES_CAPTURED_GLYPHS_UNREAD"
        print("13DT_SOURCE_PASS", SHA, len(raw), len(pdf), len(TARGET), flush=True)
    except Exception as exc:
        report.update(status="SOURCE_OR_IMAGE_BOUNDARY", error_type=type(exc).__name__,
                      error=str(exc)[:300])
        raise
    finally:
        (OUTPUT / "manifest.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
