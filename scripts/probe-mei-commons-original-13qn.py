#!/usr/bin/env python3
"""13QN acquire a catalog-listed public Commons Mei Datong Lizhi v5/v6 scan.

The catalog *listing* is not a scanned original: inspect exact MediaWiki
imageinfo, verify bytes, hashes and DjVu structure. No OCR, no physical
edition dating and no historical glyph award without independent page reading.
Reuse the source-acquisition pattern of 12YT; do not modify its evidence.
"""
from __future__ import annotations

import hashlib
import io
import json
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path("research-13qn-mei-commons")
OUT.mkdir(exist_ok=True)
NAME = "CADAL06054966 大統歷志·卷五~卷六.djvu"
CATALOG = "https://commons.wikimedia.org/wiki/Commons:Library_back_up_project/file_list/CADAL/13"
API = "https://commons.wikimedia.org/w/api.php"
METADATA_URL = API + "?" + urllib.parse.urlencode({
    "action": "query", "format": "json", "formatversion": 2,
    "titles": "File:" + NAME, "prop": "imageinfo",
    "iiprop": "url|size|sha1|mime|timestamp",
})
REPORT = {
    "schema": "TIANWEN-13QN-MEI-V5-V6-CADAL06054966-ORIGINAL-SCAN-ACQUISITION-R1",
    "source_title": NAME, "commons_catalog_index": CATALOG,
    "catalog_exact_file_label_verified": True,
    "download_source": None, "request_log": [],
    "source_file_bytes_acquired": False,
    "source_sha1": None, "source_sha256": None, "djvu_pages": None,
    "native_original_glyphs_reviewed": 0,
    "original_folio_locators_attested": 0,
    "physical_copy_and_print_year": "UNBOUND",
    "independent_ancient_physical_witnesses_added": 0,
    "G893_original_source_numeric_winners": 0,
    "chart_algorithm_reopens": 0,
}
def save():
    (OUT / "report.json").write_text(json.dumps(REPORT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
def get(url: str, limit: int) -> tuple[str, str, bytes]:
    req = urllib.request.Request(url, headers={
        "User-Agent": "TianwenPublicDomainTextWitness/1.0 (research-only; hashed-source-scans)",
        "Accept": "application/json, image/vnd.djvu, application/octet-stream, */*",
    })
    with urllib.request.urlopen(req, timeout=100) as response:
        content = response.read(limit + 1)
        if len(content) > limit:
            raise ValueError("SOURCE_EXCEEDS_LIMIT")
        return response.geturl(), response.headers.get("Content-Type", ""), content

try:
    actual, typ, metadata = get(METADATA_URL, 1_000_000)
    meta = json.loads(metadata)
    pages = meta.get("query", {}).get("pages", [])
    imageinfo = next((p["imageinfo"][0] for p in pages if p.get("imageinfo")), None)
    REPORT["request_log"].append({"route": "source_catalog_exact_imageinfo", "url": actual,
                                  "content_type": typ, "image_present": bool(imageinfo)})
except Exception as exc:
    imageinfo = None
    REPORT["request_log"].append({"route": "source_catalog_exact_imageinfo",
                                  "error": type(exc).__name__ + ": " + str(exc)[:300]})
if not imageinfo:
    REPORT["status"] = "INDEXED_CATALOG_LABEL_ONLY_IMAGEINFO_UNAVAILABLE_NO_SOURCE_BYTES"
    save()
    print("13QN CATALOG_ONLY_NO_ORIGINAL_IMAGEINFO", flush=True)
    raise SystemExit(0)
REPORT["commons_imageinfo"] = {key: imageinfo.get(key) for key in ("size", "sha1", "mime", "timestamp")}
url = imageinfo.get("url", "")
if not (url.startswith("https://upload.wikimedia.org/") or url.startswith("https://commons.wikimedia.org/")):
    REPORT["status"] = "SOURCE_IMAGEINFO_URL_NOT_TRUSTED"
    save()
    raise SystemExit(0)
try:
    actual, typ, raw = get(url, 80_000_000)
    REPORT["request_log"].append({"route": "exact_source_issued_url", "url": actual,
                                  "content_type": typ, "byte_length": len(raw)})
    if raw[:4] != b"AT&T":
        REPORT["status"] = "SOURCE_BYTES_NOT_A_DJVU"
        REPORT["first_bytes_hex"] = raw[:12].hex()
        save()
        raise SystemExit(0)
    sha1 = hashlib.sha1(raw).hexdigest()
    sha256 = hashlib.sha256(raw).hexdigest()
    if imageinfo.get("size") is not None and len(raw) != imageinfo["size"]:
        raise ValueError("IMAGEINFO_BYTE_COUNT_MISMATCH")
    if imageinfo.get("sha1") and sha1.lower() != imageinfo["sha1"].lower():
        raise ValueError("IMAGEINFO_SHA1_MISMATCH")
    source = OUT / NAME
    source.write_bytes(raw)
    p = subprocess.run(["djvused", str(source), "-e", "n"], check=True,
                       capture_output=True, text=True)
    count = int(p.stdout.strip())
    if not 10 <= count <= 800:
        raise ValueError("SOURCE_DJVU_PAGE_COUNT_OUT_OF_SCOPE")
    REPORT.update(status="EXACT_PUBLIC_DIGITAL_SOURCE_HASH_VERIFIED_PAGE_GLYPHS_PENDING",
                  source_file_bytes_acquired=True, download_source=actual,
                  source_sha1=sha1, source_sha256=sha256, djvu_pages=count)
    print("13QN SOURCE_VERIFIED", len(raw), count, sha256, flush=True)
    w, h = 180, 248
    atlas = []
    for first in range(1, count + 1, 24):
        sheet = Image.new("RGB", (w * 6, h * 4), "white")
        draw = ImageDraw.Draw(sheet)
        for i, page in enumerate(range(first, min(first + 24, count + 1))):
            p = subprocess.run(["ddjvu", "-format=pnm", f"-page={page}",
                                "-scale=18", str(source)], check=True,
                               capture_output=True)
            im = Image.open(io.BytesIO(p.stdout)).convert("RGB")
            im.thumbnail((w - 8, h - 25))
            x = (i % 6) * w + (w - im.width) // 2
            y = (i // 6) * h + 22
            sheet.paste(im, (x, y))
            draw.text(((i % 6) * w + 6, (i // 6) * h + 4),
                      f"PAGE {page:03d}", fill="black")
        dest = OUT / f"atlas_{first:03d}_{min(first + 23, count):03d}.jpg"
        sheet.save(dest, quality=84, optimize=True)
        atlas.append({"first_page": first, "last_page": min(first + 23, count),
                      "jpeg_sha256": hashlib.sha256(dest.read_bytes()).hexdigest(),
                      "filename": dest.name})
    REPORT["atlas"] = atlas
    REPORT["status"] = "EXACT_PUBLIC_DIGITAL_SOURCE_AND_CONTACT_ATLAS_HASH_VERIFIED_GLYPHS_PENDING"
    save()
    print("13QN ATLAS_READY", len(atlas), "original glyph decision zero", flush=True)
except Exception as exc:
    REPORT["status"] = "SOURCE_DOWNLOAD_OR_STRUCTURE_UNVERIFIED"
    REPORT["request_log"].append({"route": "original_byte_acquisition",
                                  "error": type(exc).__name__ + ": " + str(exc)[:320]})
    save()
    print("13QN ORIGINAL_BYTES_NOT_VERIFIED", type(exc).__name__, str(exc)[:180], flush=True)
