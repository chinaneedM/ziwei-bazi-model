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
