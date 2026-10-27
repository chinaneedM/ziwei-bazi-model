#!/usr/bin/env python3
"""Replay G893 12XY exact source originals and pixel geometry; no glyph OCR or numeric adjudication."""
import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs/research/TIANWEN-12XY-G893-L101-D16-ADJACENT-ORIGINAL-COLUMN-SCOPE-R1.json"

def require(v, why):
    if not v:
        raise ValueError(why)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def replay(archive, evidence_path=EVIDENCE):
    ev = json.loads(Path(evidence_path).read_text(encoding="utf-8"))
    require(ev["catalog_book_code"] == "GK00893_00" and ev["source_id"] == "EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893", "wrong original physical holding")
    require(ev["research_grade"]["final_cross_witness_numeric_or_mechanical_decisions"] == 0, "no source-to-numeric award")
    archive = Path(archive)
    require(archive.is_file() and archive.stat().st_size < 100_000_000, "missing original source zip")
    payload = archive.read_bytes()
    want = ev["source_archive"]
    require(len(payload) == want["bytes"] and digest(payload) == want["sha256"], "original source ZIP SHA-256 mismatch")
    with zipfile.ZipFile(io.BytesIO(payload)) as z:
        require(z.testzip() is None, "source original ZIP CRC mismatch")
        report = json.loads(z.read("report.json"))
        require(report["book_cd"] == "GK00893_00" and len(report["physical_pages"]) == 204, "wrong original image manifest")
        originals = {}
        for row in report["physical_pages"]:
            page = row["page"]
            require(page not in originals and row["download_ok"] is True, "duplicate/missing physical image")
            raw = z.read("physical/" + page + ".jpg")
            require(len(raw) == row["bytes"] and digest(raw) == row["sha256"], "original source JPEG mismatch " + page)
            originals[page] = raw
        require(len(originals) == want["total_original_jpg"] == want["original_jpg_sha256_rechecked"] == 204, "incomplete source archive")
        pages = {x["page_id"]: x for x in ev["source_pages"]}
        require(len(pages) == len(ev["source_pages"]) == 5, "five source pages not scoped")
        for pid, row in pages.items():
            require(pid in originals and digest(originals[pid]) == row["jpeg_sha256"], "original target page SHA mismatch " + pid)
            require(row["native_dimensions"] == [1150, 2000], "source dimensions not original")
            require(report["book_cd"] in row["source_issued_url"], "provider page locator identity mismatch")
        seen = set()
        for item in ev["replayed_original_rgb_regions"]:
            page = item["page_id"]
            require(page in pages, "ROI source outside reviewed pages")
            key = (page, item["role"])
            require(key not in seen, "duplicated source pixel region")
            seen.add(key)
            im = Image.open(io.BytesIO(originals[page]))
            im.verify()
            im = Image.open(io.BytesIO(originals[page])).convert("RGB")
            require(im.size == (1150, 2000), "native image pixel dimensions changed")
            l,t,r,b = item["rect_px"]
            require(all(type(n) is int for n in item["rect_px"]) and 0 <= l < r <= 1150 and 0 <= t < b <= 2000, "bad source geometry")
            require(digest(im.crop((l,t,r,b)).tobytes()) == item["rgb_pixel_sha256"], "native source ROI mismatch " + str(key))
    require(len(seen) == 8, "eight original pixel regions required")
    return {"result":"PASS","original_source_jpg_sha256_verified":204,"original_source_pages_reviewed":5,"native_rgb_roi_digests_verified":8,"machine_read_ancient_glyphs":0,"cross_witness_numerical_adjudications":0}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True, help="authorized locally held original G893 source ZIP; never include original images in Git repository")
    args = parser.parse_args()
    print(json.dumps(replay(args.archive), ensure_ascii=False))
