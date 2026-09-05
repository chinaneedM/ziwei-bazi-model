#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import json
import math
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlencode, urljoin

import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE = "https://kyudb.snu.ac.kr"
BOOK_CD = "GK00893_00"
BOOK_URL = f"{BASE}/book/view.do?book_cd={BOOK_CD}"
RENDERER = f"{BASE}/pf01/rendererImg.do"
UA = "Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"


def post(session: requests.Session, url: str, data: dict[str, str]) -> requests.Response:
    r = session.post(
        url,
        data=data,
        headers={
            "User-Agent": UA,
            "Referer": BOOK_URL,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        timeout=45,
    )
    r.raise_for_status()
    return r


def extract_item_cd(text: str) -> str:
    patterns = [
        r"item_cd=([A-Za-z0-9_-]+)",
        r"name=[\"']item_cd[\"'][^>]*value=[\"']([A-Za-z0-9_-]+)[\"']",
        r"item_cd\s*=\s*[\"']([A-Za-z0-9_-]+)[\"']",
        r"value=[\"']([A-Za-z0-9_-]+)[\"'][^>]*name=[\"']item_cd[\"']",
    ]
    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            return m.group(1)
    return ""


def extract_volumes(text: str) -> list[str]:
    vals = re.findall(r"<option\s+value=[\"']([A-Za-z0-9]+)[\"']", text, re.I)
    out: list[str] = []
    for v in vals:
        if v not in out:
            out.append(v)
    return out


def extract_js_value(text: str, name: str) -> str:
    m = re.search(rf"{re.escape(name)}\s*=\s*[\"']([^\"']+)[\"']", text)
    return m.group(1) if m else ""


def extract_pages(text: str) -> list[dict[str, str]]:
    patterns = [
        r"fn_goPageJumpWithMokIdxClear\('([A-Za-z0-9]+)'\);\">([^<]+)</a>",
        r"fn_goPageJumpWithMokIdxClear\('([A-Za-z0-9]+)'\)",
    ]
    pages: list[dict[str, str]] = []
    seen: set[str] = set()
    for p in patterns:
        for m in re.finditer(p, text):
            page = m.group(1)
            if page in seen:
                continue
            seen.add(page)
            label = m.group(2).strip() if m.lastindex and m.lastindex >= 2 else page
            pages.append({"page_no": page, "label": label})
        if pages:
            break
    return pages


def textual_hits(text: str) -> list[dict[str, str]]:
    hits = []
    for needle in ("授時曆立成卷上", "授時曆立成卷下", "太陽", "太陰", "冬至", "夏至", "遲疾", "五星", "日出", "日入"):
        start = 0
        while True:
            i = text.find(needle, start)
            if i < 0:
                break
            excerpt = re.sub(r"\s+", " ", text[max(0, i-180):i+260])
            hits.append({"needle": needle, "offset": i, "excerpt": excerpt})
            start = i + len(needle)
    return hits


def build_image_url(page_id: str, img_file: str, vol: str, first_page: str, page_no: str) -> str:
    if not page_id or not img_file:
        return ""
    old = f"{vol}_{first_page}"
    new = f"{vol}_{page_no}"
    path = page_id.replace(old, new)
    file_name = Path(img_file).name.replace(old, new)
    return f"{BASE}/ImageServlet.do?{urlencode({'imgFileNm': file_name, 'path': path})}"


def fetch_image(session: requests.Session, url: str) -> Image.Image:
    r = session.get(url, headers={"User-Agent": UA, "Referer": RENDERER}, timeout=60)
    r.raise_for_status()
    ctype = r.headers.get("content-type", "")
    if "image" not in ctype.lower() and not r.content.startswith((b"\xff\xd8\xff", b"\x89PNG")):
        raise RuntimeError(f"not image content-type={ctype} bytes={r.content[:40]!r}")
    im = Image.open(io.BytesIO(r.content))
    im.load()
    return im.convert("RGB")


def sample_indices(n: int, stride: int) -> list[int]:
    if n <= 0:
        return []
    idx = set(range(min(6, n)))
    idx.update(range(max(0, n-6), n))
    idx.update(range(0, n, max(1, stride)))
    return sorted(i for i in idx if 0 <= i < n)


def make_contact_sheet(items: list[tuple[str, Image.Image]], out: Path, cols: int = 4) -> None:
    if not items:
        return
    thumb_w, thumb_h, label_h = 280, 390, 34
    rows = math.ceil(len(items) / cols)
    canvas = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), "white")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    for i, (label, im) in enumerate(items):
        x = (i % cols) * thumb_w
        y = (i // cols) * (thumb_h + label_h)
        thumb = ImageOps.contain(im, (thumb_w-8, thumb_h-8))
        ox = x + (thumb_w - thumb.width)//2
        oy = y + (thumb_h - thumb.height)//2
        canvas.paste(thumb, (ox, oy))
        draw.text((x+5, y+thumb_h+8), label, fill="black", font=font)
    canvas.save(out, quality=88)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/g893-probe")
    ap.add_argument("--stride", type=int, default=8)
    ap.add_argument("--max-volumes", type=int, default=4)
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    s = requests.Session()
    s.headers.update({"User-Agent": UA})

    entry = s.get(BOOK_URL, timeout=45)
    entry.raise_for_status()
    (out / "book-view.html").write_text(entry.text, encoding="utf-8")
    item_cd = extract_item_cd(entry.text)

    vol_resp = post(s, RENDERER, {
        "item_cd": item_cd,
        "book_cd": BOOK_CD,
        "vol_no": "",
        "page_no": "",
        "imgFileNm": "",
        "tbl_conts_seq": "",
        "mokNm": "",
        "add_page_no": "",
    })
    (out / "renderer-volume-index.html").write_text(vol_resp.text, encoding="utf-8")
    if not item_cd:
        item_cd = extract_item_cd(vol_resp.text)
    volumes = extract_volumes(vol_resp.text)
    if not volumes:
        volumes = ["0001"]

    manifest = {
        "schema": "KYUJANGGAK-G893-PROBE-R1",
        "book_cd": BOOK_CD,
        "book_url": BOOK_URL,
        "renderer_url": RENDERER,
        "item_cd": item_cd or None,
        "volumes": [],
        "probe_policy": {
            "read_only": True,
            "ocr_used": False,
            "full_resolution_images_committed_to_repo": False,
            "contact_sheets_only_in_actions_artifact": True,
            "target_values_authorized": False,
        },
    }

    for vol in volumes[:args.max_volumes]:
        r = post(s, RENDERER, {
            "item_cd": item_cd,
            "book_cd": BOOK_CD,
            "vol_no": vol,
            "page_no": "",
            "tool": "1",
        })
        html = r.text
        (out / f"renderer-{vol}.html").write_text(html, encoding="utf-8")
        first_page = extract_js_value(html, "first_page_no")
        page_id = extract_js_value(html, "imgFileNm")
        img_file = Path(page_id).name if page_id else ""
        pages = extract_pages(html)
        if not pages and first_page:
            pages = [{"page_no": first_page, "label": first_page}]

        records = []
        for p in pages:
            url = build_image_url(page_id, img_file, vol, first_page, p["page_no"])
            records.append({**p, "image_url": url})

        vol_rec = {
            "vol_no": vol,
            "first_page_no": first_page or None,
            "source_img_file": img_file or None,
            "source_img_path": page_id or None,
            "page_count": len(records),
            "textual_hits": textual_hits(html),
            "pages": records,
            "sampled_pages": [],
        }

        samples: list[tuple[str, Image.Image]] = []
        for i in sample_indices(len(records), args.stride):
            rec = records[i]
            if not rec["image_url"]:
                continue
            try:
                im = fetch_image(s, rec["image_url"])
            except Exception as e:
                vol_rec["sampled_pages"].append({
                    "index": i,
                    "page_no": rec["page_no"],
                    "label": rec["label"],
                    "status": "ERROR",
                    "error": f"{type(e).__name__}: {e}",
                })
                continue
            label = f"{i+1}/{len(records)} {rec['page_no']} {rec['label']}"
            samples.append((label, im))
            vol_rec["sampled_pages"].append({
                "index": i,
                "page_no": rec["page_no"],
                "label": rec["label"],
                "status": "OK",
                "size": [im.width, im.height],
            })
            time.sleep(0.08)

        for chunk_start in range(0, len(samples), 20):
            chunk = samples[chunk_start:chunk_start+20]
            make_contact_sheet(
                chunk,
                out / f"contact-{vol}-{chunk_start//20+1:02d}.jpg",
                cols=4,
            )
        manifest["volumes"].append(vol_rec)

    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    summary = {
        "book_cd": BOOK_CD,
        "item_cd": manifest["item_cd"],
        "volume_count": len(manifest["volumes"]),
        "volumes": [
            {
                "vol_no": v["vol_no"],
                "page_count": v["page_count"],
                "first_page_no": v["first_page_no"],
                "textual_hit_needles": sorted({x["needle"] for x in v["textual_hits"]}),
                "sample_ok": sum(x["status"]=="OK" for x in v["sampled_pages"]),
                "sample_error": sum(x["status"]=="ERROR" for x in v["sampled_pages"]),
            }
            for v in manifest["volumes"]
        ],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
