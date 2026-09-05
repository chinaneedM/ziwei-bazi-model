#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
DEFAULT_FILE = "CADAL02050311 高麗史（四十九）.djvu"
UA = "ziwei-bazi-model-historical-research/1.0 (read-only Commons facsimile probe)"

NEEDLES = {
    "shoushi_licheng": ["授時曆立成", "授时历立成"],
    "solar_winter": ["太陽冬至", "大陽冬至", "太阳冬至", "大阳冬至"],
    "solar_yingsuo": ["盈初縮末限", "盈初缩末限", "盈縮", "盈缩"],
    "lunar_limits": ["太陰限數", "太阴限数", "太陰限", "太阴限"],
    "lunar_chiji": ["遲疾度", "迟疾度", "遲疾", "迟疾"],
    "volume_anchor": ["高麗史五十二", "高丽史五十二", "曆三", "历三"],
}

def commons_original_url(filename: str) -> str:
    q = urllib.parse.urlencode({
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url|size",
        "titles": f"File:{filename}",
    })
    req = urllib.request.Request(f"{COMMONS_API}?{q}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.load(resp)
    pages = data["query"]["pages"]
    page = next(iter(pages.values()))
    info = page["imageinfo"][0]
    return info["url"]

def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as resp, dest.open("wb") as out:
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)

def run_text(source: Path, page: int) -> str:
    proc = subprocess.run(
        ["djvutxt", f"--page={page}", str(source)],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        return ""
    return proc.stdout.decode("utf-8", errors="replace")

def norm(s: str) -> str:
    return re.sub(r"\s+", "", s)

def excerpt(text: str, needle: str, radius: int = 180) -> str:
    compact = re.sub(r"\s+", " ", text)
    i = compact.find(needle)
    if i < 0:
        return compact[: radius * 2]
    return compact[max(0, i-radius):i+len(needle)+radius]

def render_page(source: Path, page: int, dest: Path) -> Image.Image:
    subprocess.run(
        ["ddjvu", "-format=ppm", f"-page={page}", "-size=240x380", str(source), str(dest)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    with Image.open(dest) as im:
        image = im.convert("RGB")
    dest.unlink(missing_ok=True)
    return image

def make_contact_sheets(source: Path, page_count: int, out: Path) -> list[dict[str, object]]:
    contact_dir = out / "contact-sheets"
    contact_dir.mkdir(parents=True, exist_ok=True)
    cols, rows = 5, 6
    cell_w, image_h, label_h = 250, 395, 24
    font = ImageFont.load_default()
    sheets = []
    chunk = cols * rows
    for start in range(1, page_count + 1, chunk):
        end = min(page_count, start + chunk - 1)
        pages = []
        for page in range(start, end + 1):
            tmp = out / f"page-{page:04d}.ppm"
            pages.append((page, render_page(source, page, tmp)))
        canvas = Image.new("RGB", (cols * cell_w, rows * (image_h + label_h)), "white")
        draw = ImageDraw.Draw(canvas)
        for idx, (page, im) in enumerate(pages):
            x = (idx % cols) * cell_w
            y = (idx // cols) * (image_h + label_h)
            thumb = ImageOps.contain(im, (cell_w - 8, image_h - 8))
            canvas.paste(thumb, (x + (cell_w-thumb.width)//2, y + (image_h-thumb.height)//2))
            draw.text((x + 6, y + image_h + 4), f"scan page {page}", fill="black", font=font)
        name = f"contact-{start:03d}-{end:03d}.jpg"
        path = contact_dir / name
        canvas.save(path, quality=78, optimize=True)
        sheets.append({"file": f"contact-sheets/{name}", "start_page": start, "end_page": end})
    return sheets

def render_target_pages(source: Path, pages: list[int], out: Path) -> list[dict[str, object]]:
    target_dir = out / "target-pages"
    target_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for page in pages:
        ppm = out / f"target-{page:04d}.ppm"
        subprocess.run(
            ["ddjvu", "-format=ppm", f"-page={page}", "-scale=100", str(source), str(ppm)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        with Image.open(ppm) as im:
            rgb = im.convert("RGB")
            name = f"scan-{page:03d}-full.jpg"
            dest = target_dir / name
            rgb.save(dest, quality=96, optimize=True)
            records.append({
                "page": page,
                "file": f"target-pages/{name}",
                "size": [rgb.width, rgb.height],
                "ocr_used": False,
                "target_glyph_authority": "DIRECT_PAGE_IMAGE_REQUIRES_HUMAN_VISUAL_READING",
            })
        ppm.unlink(missing_ok=True)
    return records

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/goryeosa-cadal-probe")
    ap.add_argument("--filename", default=DEFAULT_FILE)
    ap.add_argument("--target-pages", default="")
    args = ap.parse_args()
    target_pages = [int(x) for x in args.target_pages.split(",") if x.strip()]

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    source = out / "source.djvu"
    url = commons_original_url(args.filename)
    download(url, source)

    nproc = subprocess.run(
        ["djvused", str(source), "-e", "n"],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    page_count = int(nproc.stdout.strip())

    page_records = []
    hits = []
    text_pages = 0
    for page in range(1, page_count + 1):
        text = run_text(source, page)
        compact = norm(text)
        if compact:
            text_pages += 1
        matched = []
        score = 0
        for family, needles in NEEDLES.items():
            family_hits = [n for n in needles if n in compact or n in text]
            if family_hits:
                matched.append({"family": family, "needles": family_hits})
                score += 4 if family in {"shoushi_licheng", "solar_winter", "lunar_limits"} else 1
        rec = {
            "page": page,
            "text_chars": len(text),
            "score": score,
            "matched": matched,
        }
        page_records.append(rec)
        if matched:
            best = matched[0]["needles"][0]
            hits.append({
                **rec,
                "excerpt": excerpt(text, best),
            })

    hits.sort(key=lambda x: (-x["score"], x["page"]))
    contact_sheets = []
    if text_pages == 0:
        contact_sheets = make_contact_sheets(source, page_count, out)

    target_page_records = render_target_pages(source, target_pages, out) if target_pages else []

    manifest = {
        "schema": "GORYEOSA-CADAL-FACSIMILE-PROBE-R2",
        "source_filename": args.filename,
        "source_url": url,
        "page_count": page_count,
        "pages_with_extracted_text": text_pages,
        "ocr_used": False,
        "probe_scope": "EXISTING_DJVU_TEXT_LAYER_THEN_LOW_RES_VISUAL_CONTACT_SHEETS_IF_TEXT_ABSENT",
        "visual_contact_sheets_generated": bool(contact_sheets),
        "contact_sheets": contact_sheets,
        "target_pages": target_page_records,
        "target_glyph_authority": False,
        "target_value_prepopulation_authorized": False,
        "note": "No OCR is run. Text-layer hits localize candidates when present; otherwise low-resolution contact sheets are visual navigation aids only. Exact target glyph conclusions require direct full-page image inspection.",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    (out / "hits.json").write_text(json.dumps(hits, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    (out / "page-signatures.json").write_text(json.dumps(page_records, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    source.unlink(missing_ok=True)

    print(json.dumps({
        **manifest,
        "hit_count": len(hits),
        "top_hits": hits[:30],
    }, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
