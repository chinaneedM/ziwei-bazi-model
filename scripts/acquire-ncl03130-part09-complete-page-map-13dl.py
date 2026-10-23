#!/usr/bin/env python3
"""13DL: SHA-pinned NCL03130 part09 complete visual page index for manual juan search.

Contact sheets are navigational only. A photographed physical book is not a
textual juan, and a Wikimedia mirror is not first-party NCL item authentication.
No OCR, inferred missing-volume exclusion, or editorial number correction.
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

SOURCE = "https://commons.wikimedia.org/wiki/Special:Redirect/file/NCL-03130_09_%E9%AB%98%E9%BA%97%E5%8F%B2.pdf"
SOURCE_SHA256 = "3c2a5621fb3f4eabc593020bcde12a38f6ecdae2842940dec12d5a3a56afd32e"
SOURCE_SIZE = 50_735_589
SOURCE_PAGES = 189
OUT = Path("ncl03130-13dl-part09-full-visual-map")
SHEET_COLUMNS = 6
SHEET_ROWS = 3
SHEET_CAPACITY = SHEET_COLUMNS * SHEET_ROWS
DETAIL_PAGES = (112, 116, 119, 120)


def sha256(payload):
    return hashlib.sha256(payload).hexdigest()


def acquire():
    chunks = []
    total = 0
    h = hashlib.sha256()
    with requests.get(SOURCE, stream=True, allow_redirects=True, timeout=(30, 180),
                      headers={"User-Agent": "TianwenHistoricalResearch/1.0"}) as response:
        response.raise_for_status()
        parsed = urlsplit(response.url)
        if parsed.scheme != "https" or parsed.hostname not in ("commons.wikimedia.org", "upload.wikimedia.org"):
            raise RuntimeError("unapproved mirror redirect")
        for chunk in response.iter_content(1024 * 1024):
            if not chunk:
                continue
            total += len(chunk)
            if total > 60_000_000:
                raise RuntimeError("source exceeded fixed input cap")
            h.update(chunk)
            chunks.append(chunk)
    raw = b"".join(chunks)
    if len(raw) != SOURCE_SIZE or h.hexdigest() != SOURCE_SHA256 or raw[:5] != b"%PDF-":
        raise RuntimeError("pinned source identity mismatch")
    return raw


def render(pdf, output, manifest, preview_logs=True):
    """Document can be synthetic for local tests; manifest remains explicit."""
    if pdf.is_encrypted or len(pdf) != SOURCE_PAGES:
        raise RuntimeError("expected exactly 189 unencrypted original-image pages")
    output.mkdir(parents=True, exist_ok=True)
    thumbs = []
    for i in range(1, len(pdf) + 1):
        pix = pdf[i - 1].get_pixmap(matrix=fitz.Matrix(0.75, 0.75), alpha=False)
        pic = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
        pic.thumbnail((294, 205))
        manifest["pages"].append({"pdf_page": i, "thumbnail_rgb_sha256": sha256(pic.tobytes()),
                                  "physical_book_id": "UNBOUND", "textual_juan": "UNREAD"})
        thumbs.append(pic)
    for j in range(0, len(thumbs), SHEET_CAPACITY):
        batch = thumbs[j:j + SHEET_CAPACITY]
        sheet = Image.new("RGB", (SHEET_COLUMNS * 312, SHEET_ROWS * 235), "white")
        draw = ImageDraw.Draw(sheet)
        for k, pic in enumerate(batch):
            x, y = (k % SHEET_COLUMNS) * 312, (k // SHEET_COLUMNS) * 235
            sheet.paste(pic, (x + 7, y + 24))
            draw.text((x + 8, y + 4), f"NCL03130 part09 PDF p{j + k + 1:03d}", fill="black")
        buff = io.BytesIO()
        sheet.save(buff, format="JPEG", quality=77, optimize=True)
        payload = buff.getvalue()
        name = f"atlas-{j+1:03}-{j+len(batch):03}.jpg"
        (output / name).write_bytes(payload)
        manifest["sheets"].append({"file": name, "first_page": j + 1,
                                   "last_page": j + len(batch), "sha256": sha256(payload)})
        if preview_logs:
            print("13DL_ATLAS_BEGIN", name, len(payload), flush=True)
            print(base64.b64encode(payload).decode("ascii"), flush=True)
            print("13DL_ATLAS_END", name, flush=True)
    for page_no in DETAIL_PAGES:
        pix = pdf[page_no-1].get_pixmap(matrix=fitz.Matrix(2.7, 2.7), alpha=False)
        data = pix.tobytes("png")
        name = f"native-p{page_no:03}.png"
        (output / name).write_bytes(data)
        manifest["details"].append({"pdf_page": page_no, "file": name,
                                    "sha256": sha256(data), "grade": "ORIGINAL_SOURCE_RENDER_UNREAD"})
    manifest["status"] = "SHA_PINNED_COMPLETE_NAVIGATION_IMAGES_REQUIRE_MANUAL_READ"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {"schema": "TIANWEN-13DL-NCL03130-PART09-VISUAL-JUAN-MAPPING-R1",
                "source": SOURCE, "source_sha256": SOURCE_SHA256,
                "expected_pdf_bytes": SOURCE_SIZE, "expected_pages": SOURCE_PAGES,
                "source_grade": "WIKIMEDIA_COMMONS_MIRROR_NOT_FIRSTPARTY_NCL_PHYSICAL_BINDING",
                "no_ocr": True, "juan52_proven": False, "source_physical_era": "UNBOUND",
                "pages": [], "sheets": [], "details": [], "status": "STARTED"}
    try:
        raw = acquire()
        pdf = fitz.open(stream=raw, filetype="pdf")
        render(pdf, OUT, manifest)
        print("13DL_COMPLETE", SOURCE_SHA256, len(raw), len(pdf), len(manifest["sheets"]), flush=True)
    except Exception as e:
        manifest.update(status="SOURCE_OR_RENDER_BOUNDARY", error_type=type(e).__name__, error=str(e)[:350])
        raise
    finally:
        (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
