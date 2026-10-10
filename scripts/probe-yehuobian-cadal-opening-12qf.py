#!/usr/bin/env python3
"""Bounded, no-OCR original-page capture for public CADAL first fascicle.

Only a source-local bibliographic/preface probe; do not infer impression
date or a v20 target copy relationship from matching title or a shared
publisher's name.
"""
from __future__ import annotations
import hashlib
import json
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "yehuobian-cadal-opening-12qf"
NAME = "CADAL02096900_野獲編（一）.djvu"
EXPECTED_BYTES = 2833699  # Commons duplicate-backup public file-list control
PREFACE_HEAD_MAX = 50
PREFACE_TAIL_MAX = 8

def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    md5 = hashlib.md5(NAME.encode("utf-8")).hexdigest()
    url = ("https://upload.wikimedia.org/wikipedia/commons/"
           + md5[0] + "/" + md5[:2] + "/" + urllib.parse.quote(NAME))
    receipt = {
        "schema": "MING-DATONG-YEHUOBIAN-CADAL-FIRST-OPENING-DIRECT-IMAGE-12QF",
        "source_filename": NAME,
        "source_url": url,
        "source_scope": "EXACT_PUBLIC_FASCICLE_ONE_SOURCE_IMAGE_ONLY",
        "expected_file_bytes_public_listing": EXPECTED_BYTES,
        "ocr_used": False,
        "direct_image_glyphs_manually_collated": False,
        "digital_series_same_copy_as_fascicle16": "UNPROVEN",
        "publisher/impression_1827_vs_1869": "UNRESOLVED",
        "status": "STARTED",
        "images": [],
        "contact_sheets": []
    }
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "TianwenHistoricalResearch/1.0 (public bibliography collation)"}
        )
        with urllib.request.urlopen(request, timeout=65) as response:
            raw = response.read(3500000)
        receipt["source_bytes"] = len(raw)
        receipt["source_sha1"] = hashlib.sha1(raw).hexdigest()
        receipt["source_sha256"] = digest(raw)
        if len(raw) != EXPECTED_BYTES:
            raise RuntimeError("SOURCE_PUBLIC_SIZE_IDENTITY_MISMATCH")
        target = OUT / "source.djvu"
        target.write_bytes(raw)
        count = int(subprocess.check_output(
            ["djvused", str(target), "-e", "n"], text=True, timeout=25
        ).strip())
        receipt["source_pages"] = count
        if not 15 <= count <= 350:
            raise RuntimeError("SOURCE_PAGE_COUNT_OUT_OF_BOUND")
        selection = list(range(1, min(PREFACE_HEAD_MAX, count) + 1))
        selection += [p for p in range(max(1, count - PREFACE_TAIL_MAX + 1), count + 1)
                      if p not in selection]
        receipt["sample_pdf_page_1based"] = selection
        directory = OUT / "pages"
        directory.mkdir(exist_ok=True)
        for p in selection:
            tmp = OUT / "tmp.ppm"
            subprocess.run(
                ["ddjvu", "-format=ppm", f"-page={p}", "-size=1300x1900", str(target), str(tmp)],
                timeout=40, check=True, stdout=subprocess.DEVNULL
            )
            with Image.open(tmp) as image:
                result = directory / f"p{p:03}.jpg"
                image.convert("RGB").save(result, "JPEG", quality=88, optimize=True)
            tmp.unlink(missing_ok=True)
            receipt["images"].append({
                "page": p, "sha256": digest(result.read_bytes()), "bytes": result.stat().st_size
            })
        contact = OUT / "contacts"
        contact.mkdir(exist_ok=True)
        for start in range(0, len(selection), 6):
            block = selection[start : start + 6]
            sheet = Image.new("RGB", (2280, 2300), "white")
            draw = ImageDraw.Draw(sheet)
            for i, p in enumerate(block):
                with Image.open(directory / f"p{p:03}.jpg") as picture:
                    thumb = picture.copy()
                thumb.thumbnail((710, 1070))
                x, y = (i % 3) * 760 + 20, (i // 3) * 1150 + 45
                sheet.paste(thumb, (x, y))
                draw.text((x, y - 22), f"source p{p}", fill="black")
            target_sheet = contact / f"sheet-{block[0]:03}.jpg"
            sheet.save(target_sheet, "JPEG", quality=84)
            receipt["contact_sheets"].append({
                "pages": block, "sha256": digest(target_sheet.read_bytes())
            })
        receipt["status"] = "BOUNDED_SOURCE_PAGES_CAPTURED_NOT_MANUALLY_READ"
    except Exception as exc:
        receipt["error"] = f"{type(exc).__name__}: {str(exc)[:400]}"
        receipt["status"] = (
            "SOURCE_IDENTITY_MISMATCH_FAIL_CLOSED" if "MISMATCH" in str(exc)
            else "SOURCE_ACCESS_OR_EXTRACT_BOUNDARY"
        )
    finally:
        (OUT / "status.json").write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8"
        )
    print(json.dumps({
        "status": receipt["status"],
        "page_count": receipt.get("source_pages"),
        "captured_pages": len(receipt["images"]),
        "error": receipt.get("error"),
    }))
    if receipt["status"] == "SOURCE_IDENTITY_MISMATCH_FAIL_CLOSED":
        raise SystemExit(1)

if __name__ == "__main__":
    main()
