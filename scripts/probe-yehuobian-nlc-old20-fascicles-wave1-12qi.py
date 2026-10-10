#!/usr/bin/env python3
"""Hash and render exact public NLC old20 fascicles 1..3, without OCR.

A PDF page image is NOT an automatically collated manuscript glyph.  The ten
digital fascicles belong to one described NLC holding, not ten copy votes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import urllib.parse
from pathlib import Path
from PIL import Image, ImageDraw

SOURCES = {
    1: ("383065", 119, (1, 2, 3, 4)),
    2: ("383064", 72, (5,)),
    3: ("383068", 121, (6, 7)),
    4: ("383062", 56, (8, 9)),
    5: ("383066", 63, (10,)),
    6: ("383071", 116, (11,)),
    7: ("383070", 110, (12, 13, 14)),
    8: ("383069", 87, (15,)),
    9: ("383063", 141, (16, 17)),
}
EXPECTED_SOURCE_SHA256 = {
    1: "acd33a56d2c829fcafd8db1c15b4bb9cb3d3b21905cc8d1e9e9d5a5c45b11939",
    2: "8fa105b74efe109a08140286c96a8215f049a62d0b1cf587e7e3e5afdb559d57",
    3: "94ef8982e97b05427836639d45daeb88d46b8de3918d61bab4f444536388e739",
    4: "11c1cfacb913404be79e386a967324048b762a166b1c08c1853fcbdcc904d67a",
    5: "06692bd33c86c6c6cd8eb732fe89aa1d289e06da976663d33ca04352d9f45280",
    6: "9949f3c736d75f1772c306455f6bead7e744675b66283a415e7c50f4dc4f1c62",
    7: "540435e7f56bd33f54a5a7dd540b1e3312cb1beae1e18c384d45ab752aaf51b1",
    8: "8618b54338df71d07f4b8b70bb2d9b549613be0488529c9163a68ef25a7de366",
    9: "cbfea56ea3e447c6c241fee3dfb319b4886bc77eeddbc9de4bc5f81bf3d72d62",
}

ROOT = Path("artifacts/yehuobian-nlc-old20-wave1-12qi")

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fascicle", type=int, required=True, choices=sorted(SOURCES))
    args = parser.parse_args()
    idx = args.fascicle
    suffix, expected_pages, catalog_vols = SOURCES[idx]
    filename = f"NLC892-411999003250-{suffix} 萬曆野獲編 □□卷 第{idx}冊.pdf"
    source_url = "https://commons.wikimedia.org/wiki/Special:Redirect/file/" + urllib.parse.quote(filename)
    out = ROOT / f"fascicle-{idx}"
    out.mkdir(parents=True, exist_ok=True)
    status = {
        "schema": "MING-DATONG-YEHUOBIAN-12QI-NLC-OLD20-BOUNDED-FASCICLE-IMAGE-ATLAS-R1",
        "physical_holding_key": "NLC-411999003250-OLD20-ONE_HOLDING",
        "fascicle": idx,
        "catalogued_original_volume_labels": catalog_vols,
        "source_filename": filename, "source_url": source_url,
        "expected_pages": expected_pages,
        "ocr_performed": False, "automated_target_glyph_detection_performed": False,
        "exact_target_heading_manually_verified": False,
        "physical_copy_count_increment": 0, "historical_algorithm_reopened": False,
        "status": "STARTED", "image_pages": [], "contact_sheets": [],
    }
    try:
        pdf = out / "source.pdf"
        subprocess.run([
            "curl", "-fL", "--retry", "4", "--retry-all-errors",
            "--retry-delay", "3", "--connect-timeout", "25", "--max-time", "600",
            "-A", "TianwenHistoricalSourceOriginalImageProbe/1.0",
            source_url, "-o", str(pdf)
        ], timeout=630, check=True, capture_output=True)
        if pdf.read_bytes()[:4] != b"%PDF":
            raise ValueError("NOT_A_PDF")
        info = subprocess.check_output(["pdfinfo", str(pdf)], text=True, timeout=45)
        pages = int(next(line.split(":", 1)[1].strip() for line in info.splitlines() if line.startswith("Pages:")))
        status.update(source_pdf_sha256=sha256(pdf),
                      source_pdf_sha1=hashlib.sha1(pdf.read_bytes()).hexdigest(),
                      source_bytes=pdf.stat().st_size, observed_pages=pages)
        if status["source_pdf_sha256"] != EXPECTED_SOURCE_SHA256[idx]:
            raise ValueError("SOURCE_SHA256_IDENTITY_MISMATCH")
        if pages != expected_pages:
            raise ValueError("SOURCE_PAGE_COUNT_MISMATCH")
        images = out / "images"; images.mkdir(exist_ok=True)
        contact_dir = out / "contacts"; contact_dir.mkdir(exist_ok=True)
        group = []
        for page in range(1, pages + 1):
            dest = images / f"page-{page:03d}"
            subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", "100",
                            "-jpeg", "-jpegopt", "quality=78", "-singlefile",
                            str(pdf), str(dest)], timeout=55, check=True, capture_output=True)
            jpg = dest.with_suffix(".jpg")
            status["image_pages"].append({"page": page, "sha256": sha256(jpg), "size": jpg.stat().st_size})
            with Image.open(jpg) as img:
                reduced = img.convert("RGB")
                reduced.thumbnail((590, 625))
                group.append((page, reduced.copy()))
            if len(group) == 8 or page == pages:
                first = group[0][0]
                sheet = Image.new("RGB", (2480, 1460), "white")
                draw = ImageDraw.Draw(sheet)
                for i, (pn, img) in enumerate(group):
                    x = (i % 4) * 620 + 8
                    y = (i // 4) * 730 + 38
                    sheet.paste(img, (x, y))
                    draw.text((x, y - 24), f"NLC-411999003250 fascicle-{idx} PDF-page-{pn:03d}", fill="black")
                dest_sheet = contact_dir / f"sheet-{first:03d}.jpg"
                sheet.save(dest_sheet, "JPEG", quality=82)
                status["contact_sheets"].append({"pages": [x[0] for x in group],
                                                  "sha256": sha256(dest_sheet), "filename": dest_sheet.name})
                group = []
        status["status"] = "ALL_SOURCE_PAGES_CAPTURED_MANUAL_TARGET_SEARCH_PENDING"
    except Exception as exc:
        status["status"] = "SOURCE_IDENTITY_OR_ACCESS_BOUNDARY"
        status["error"] = f"{type(exc).__name__}: {str(exc)[:300]}"
    finally:
        (out / "status.json").write_text(json.dumps(status, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if "source.pdf" in [p.name for p in out.iterdir()]:
            (out / "source.pdf").unlink()
        print(json.dumps({"fascicle": idx, "status": status["status"],
                          "pages": len(status["image_pages"]), "error": status.get("error")}))
    return 0 if status["status"] == "ALL_SOURCE_PAGES_CAPTURED_MANUAL_TARGET_SEARCH_PENDING" else 1

if __name__ == "__main__":
    raise SystemExit(main())
