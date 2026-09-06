#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import time
from pathlib import Path
from urllib.parse import urlencode

from curl_cffi import requests
from PIL import Image, ImageDraw

BASE = "https://kyudb.snu.ac.kr"
BOOK_CD = "GK26775_00"
ITEM_CD = "BBG"
VOLUMES = ("0001", "0002", "0003", "0004", "0005", "0006", "0007")
RENDERER = BASE + "/pf01/rendererImg.do"
UA = "Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"


def req(session, method, url, **kwargs):
    errors = []
    for attempt in range(1, 4):
        try:
            r = session.request(method, url, timeout=30, **kwargs)
            return r, {
                "url": r.url,
                "status": r.status_code,
                "content_type": r.headers.get("content-type", ""),
                "bytes": len(r.content),
                "sha256": hashlib.sha256(r.content).hexdigest(),
                "attempt": attempt,
            }
        except Exception as exc:
            errors.append({"attempt": attempt, "type": type(exc).__name__, "error": str(exc)})
            time.sleep(0.8 * attempt)
    return None, {"url": url, "status": 0, "attempts": errors}


def parse_page_ids(text: str) -> list[str]:
    out = []
    for m in re.finditer(r'''fn_goPageJumpWithMokIdxClear\(["']([A-Za-z0-9]+)["']\)''', text):
        p = m.group(1)
        if p not in out and not p.startswith("999"):
            out.append(p)
    return out


def parse_img_path(text: str) -> str | None:
    matches = re.findall(r'''var\s+imgFileNm\s*=\s*["']([^"']+)["']''', text)
    return matches[-1] if matches else None


def sample_pages(pages: list[str], stride: int) -> list[str]:
    if not pages:
        return []
    picks = set(pages[:4] + pages[-4:])
    for i in range(0, len(pages), max(1, stride)):
        picks.add(pages[i])
    return [p for p in pages if p in picks]


def make_sheet(items: list[tuple[str, Image.Image]], path: Path, cols: int = 2) -> None:
    if not items:
        return
    thumb_w = 520
    label_h = 34
    thumbs = []
    for label, im in items:
        ratio = thumb_w / im.width
        h = max(1, int(im.height * ratio))
        thumbs.append((label, im.resize((thumb_w, h))))
    cell_h = max(im.height for _, im in thumbs) + label_h
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w, rows * cell_h), "white")
    draw = ImageDraw.Draw(sheet)
    for i, (label, im) in enumerate(thumbs):
        x = (i % cols) * thumb_w
        y = (i // cols) * cell_h
        sheet.paste(im, (x, y))
        draw.text((x + 5, y + im.height + 5), label, fill="black")
    sheet.save(path, quality=90)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/kyujanggak-1930-catalog-visual-sampler")
    ap.add_argument("--stride", type=int, default=24)
    ap.add_argument("--sheet-size", type=int, default=12)
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    result = {
        "schema": "KYUJANGGAK-1930-NUMERIC-ORDER-CATALOG-VISUAL-SAMPLER-R1",
        "book_cd": BOOK_CD,
        "item_cd": ITEM_CD,
        "catalog_identifier": "奎26775-v.1-7",
        "catalog_title": "奎章閣圖書番號順目錄",
        "ocr_used": False,
        "sampling_role": "CATALOG_RANGE_AND_ENTRY_LOCALIZATION_ONLY",
        "g893_item_identity_authorized": False,
        "target_values_authorized": False,
        "filename_pattern_inference": "FORBIDDEN",
        "page_identity_basis": "EACH_IMAGE_PATH_PARSED_FROM_DIRECT_RENDERER_RESPONSE_FOR_REQUESTED_PROVIDER_PAGE_ID",
        "stride": args.stride,
        "volumes": [],
    }

    s = requests.Session(impersonate="chrome")
    s.headers.update({"User-Agent": UA})

    for vol_no in VOLUMES:
        r0, m0 = req(
            s, "POST", RENDERER,
            data={"item_cd": ITEM_CD, "book_cd": BOOK_CD, "vol_no": vol_no, "page_no": "", "tool": "1"},
        )
        rec = {"vol_no": vol_no, "renderer_index": m0, "samples": []}
        if r0 is None or r0.status_code != 200:
            result["volumes"].append(rec)
            continue
        pages = parse_page_ids(r0.text)
        rec["page_count"] = len(pages)
        rec["sample_page_ids"] = sample_pages(pages, args.stride)
        sheet_items: list[tuple[str, Image.Image]] = []

        for page_no in rec["sample_page_ids"]:
            rr, rm = req(
                s, "POST", RENDERER,
                data={"item_cd": ITEM_CD, "book_cd": BOOK_CD, "vol_no": vol_no, "page_no": page_no, "tool": "1"},
            )
            item = {"page_no": page_no, "renderer": rm}
            if rr is None or rr.status_code != 200:
                rec["samples"].append(item)
                continue
            img_path = parse_img_path(rr.text)
            item["direct_renderer_img_path"] = img_path
            if not img_path:
                rec["samples"].append(item)
                continue
            basename = img_path.rsplit("/", 1)[-1]
            image_url = BASE + "/ImageServlet.do?" + urlencode({"imgFileNm": basename, "path": img_path})
            ir, imeta = req(
                s, "GET", image_url,
                headers={"Referer": RENDERER, "Accept": "image/jpeg,image/*,*/*;q=0.8"},
            )
            item["image_transport"] = imeta
            if ir is not None and ir.status_code == 200:
                try:
                    image = Image.open(io.BytesIO(ir.content)).convert("RGB")
                    item["valid_image"] = True
                    item["image_size"] = [image.width, image.height]
                    item["image_sha256"] = hashlib.sha256(ir.content).hexdigest()
                    image.thumbnail((1400, 1900))
                    fn = f"{vol_no}-{page_no}.jpg"
                    image.save(out / fn, quality=92)
                    item["sample_file"] = fn
                    sheet_items.append((f"{vol_no}:{page_no}", image.copy()))
                except Exception as exc:
                    item["valid_image"] = False
                    item["image_error"] = f"{type(exc).__name__}: {exc}"
            rec["samples"].append(item)

        rec["contact_sheets"] = []
        for start in range(0, len(sheet_items), max(1, args.sheet_size)):
            chunk = sheet_items[start:start + args.sheet_size]
            fn = f"contact-{vol_no}-{start // max(1, args.sheet_size) + 1:02d}.jpg"
            make_sheet(chunk, out / fn)
            if (out / fn).exists():
                rec["contact_sheets"].append(fn)
        result["volumes"].append(rec)

    result["conclusion"] = {
        "valid_sample_images": sum(
            sum(1 for x in v.get("samples", ()) if x.get("valid_image"))
            for v in result["volumes"]
        ),
        "g893_catalog_entry": "NOT_READ_BY_SCRIPT_VISUAL_REVIEW_REQUIRED",
        "g893_identity_effect": "NONE_UNTIL_DIRECT_CATALOG_ENTRY_REVIEW",
        "target_effect": "NONE",
        "algorithm_or_runtime_effect": "NONE",
    }
    (out / "visual-sampler.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result["conclusion"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
