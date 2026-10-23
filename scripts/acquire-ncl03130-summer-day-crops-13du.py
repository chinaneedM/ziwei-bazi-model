#!/usr/bin/env python3
"""13DU — source-original p86 adjacent day-column crops, no OCR or auto-emendation.

Read the marked headings and numeric fields manually; column mapping is a
layout locator, not an accepted cross-edition correspondence or glyph judgment.
"""
import base64
import hashlib
import io
import json
from pathlib import Path
from urllib.parse import urlsplit

import fitz
import requests
from PIL import Image, ImageDraw

URL = "https://commons.wikimedia.org/wiki/Special:Redirect/file/NCL-03130_09_%E9%AB%98%E9%BA%97%E5%8F%B2.pdf"
SOURCE_SHA = "3c2a5621fb3f4eabc593020bcde12a38f6ecdae2842940dec12d5a3a56afd32e"
SOURCE_SIZE = 50_735_589
OUT = Path("ncl03130-13du-summer-source-original-rois")
PAGE = 86
COLS = {
    "D29": (.112, .16, .215, .94),
    "D28": (.216, .16, .317, .94),
    "D27": (.318, .16, .420, .94),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = {
        "schema": "TIANWEN-13DU-NCL03130-SUMMER-D27-D29-NATIVE-SOURCE-ROIS-R1",
        "source": URL, "source_sha256": SOURCE_SHA, "source_bytes": SOURCE_SIZE,
        "physical_copy_identity": "UNBOUND_FIRSTPARTY_NCL",
        "physical_stratum": "UNBOUND_OLD_OR_1905_SUPPLEMENT",
        "one_source_one_page": True, "source_pdf_page": PAGE,
        "summer_headings_and_xingdu": "PENDING_MANUAL_GLYPH_COLLATION",
        "no_ocr": True, "rois": [], "status": "INITIAL",
    }
    try:
        digest = hashlib.sha256()
        chunks = []
        n = 0
        with requests.get(URL, stream=True, allow_redirects=True, timeout=(30, 180),
                          headers={"User-Agent": "TianwenHistoricalResearch/1.0"}) as response:
            response.raise_for_status()
            p = urlsplit(response.url)
            if p.scheme != "https" or p.hostname not in ("commons.wikimedia.org", "upload.wikimedia.org"):
                raise RuntimeError("non-whitelisted source redirect")
            for chunk in response.iter_content(1024 * 1024):
                if not chunk:
                    continue
                n += len(chunk)
                if n > 60_000_000:
                    raise RuntimeError("input size exceeded")
                chunks.append(chunk)
                digest.update(chunk)
        raw = b"".join(chunks)
        if n != SOURCE_SIZE or digest.hexdigest() != SOURCE_SHA or not raw.startswith(b"%PDF-"):
            raise RuntimeError("source PDF identity mismatch")
        pdf = fitz.open(stream=raw, filetype="pdf")
        if pdf.is_encrypted or len(pdf) != 189:
            raise RuntimeError("PDF page/encryption mismatch")
        pix = pdf[PAGE-1].get_pixmap(matrix=fitz.Matrix(3.2, 3.2), alpha=False)
        original = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        report["source_native_render_rgb_sha256"] = sha(pix.samples)
        report["source_native_dimensions"] = [pix.width, pix.height]
        cards = []
        for name, rect in COLS.items():
            bbox = tuple(int(a * (original.width if i%2==0 else original.height))
                         for i, a in enumerate(rect))
            if not (0 <= bbox[0] < bbox[2] <= original.width and
                    0 <= bbox[1] < bbox[3] <= original.height):
                raise RuntimeError("invalid ROI bbox")
            native = original.crop(bbox)
            outname = f"page086-{name}-native-original-column.png"
            stream = io.BytesIO()
            native.save(stream, format="PNG")
            png = stream.getvalue()
            (OUT / outname).write_bytes(png)
            report["rois"].append({
                "nominal_source_day": name, "relative_box": list(rect), "native_bbox": list(bbox),
                "native_size": list(native.size), "original_rgb_sha256": sha(native.tobytes()),
                "native_png_sha256": sha(png), "image": outname,
                "status": "UNREAD_ORIGINAL_SOURCE_CROP"
            })
            cards.append((name, native))
        w = sum(im.width + 14 for _, im in cards) + 10
        h = max(im.height for _, im in cards) + 60
        composite = Image.new("RGB", (w, h), "white")
        draw = ImageDraw.Draw(composite)
        x = 12
        for name, im in cards:
            draw.text((x, 14), f"NCL03130-P09 PAGE86 {name} ORIGINAL", fill="black")
            composite.paste(im, (x, 48))
            x += im.width + 14
        composite.thumbnail((2400, 2600))
        buf = io.BytesIO()
        composite.save(buf, format="JPEG", quality=91, optimize=True)
        nav = buf.getvalue()
        (OUT / "source-3day-original-navigation.jpg").write_bytes(nav)
        report["navigation_sha256"] = sha(nav)
        report["status"] = "SOURCE_SHA_VERIFIED_NATIVE_ROIS_CAPTURED_UNREAD"
        print("13DU_NAV_BEGIN", len(nav), flush=True)
        print(base64.b64encode(nav).decode("ascii"), flush=True)
        print("13DU_NAV_END", flush=True)
        print("13DU_PASS", SOURCE_SHA, n, len(report["rois"]), flush=True)
    except Exception as exc:
        report.update(status="SOURCE_OR_CROP_BOUNDARY", error_type=type(exc).__name__, error=str(exc)[:250])
        raise
    finally:
        (OUT / "manifest.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
