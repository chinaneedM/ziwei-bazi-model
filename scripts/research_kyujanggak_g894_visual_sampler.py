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
BOOK_CD = "GK00894_00"
ITEM_CD = "GJB"
VOLUMES = ("0001", "0002", "0003")
RENDERER = BASE + "/pf01/rendererImg.do"
UA = "Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"


def req(session, method, url, **kwargs):
    errors = []
    for attempt in range(1, 4):
        try:
            r = session.request(method, url, timeout=25, **kwargs)
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


def sample_pages(pages: list[str]) -> list[str]:
    if not pages:
        return []
    picks = set(pages[:4] + pages[-4:])
    for i in range(0, len(pages), 8):
        picks.add(pages[i])
    return [p for p in pages if p in picks]


def make_sheet(items: list[tuple[str, Image.Image]], path: Path) -> None:
    if not items:
        return
    thumb_w = 260
    label_h = 30
    cols = 4
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
        draw.text((x + 4, y + im.height + 4), label, fill="black")
    sheet.save(path, quality=88)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/g894-visual-sampler")
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    result = {
        "schema": "KYUJANGGAK-G894-VISUAL-SAMPLER-R1",
        "book_cd": BOOK_CD,
        "item_cd": ITEM_CD,
        "ocr_used": False,
        "sampling_role": "VISUAL_TABLE_FAMILY_LOCALIZATION_ONLY",
        "target_values_authorized": False,
        "page_identity_basis": "EACH_IMAGE_PATH_PARSED_FROM_DIRECT_RENDERER_RESPONSE_FOR_REQUESTED_PROVIDER_PAGE_ID",
        "filename_pattern_inference": "FORBIDDEN",
        "volumes": [],
    }
    s = requests.Session(impersonate="chrome")
    s.headers.update({"User-Agent": UA})
    for vol_no in VOLUMES:
        r0, m0 = req(s, "POST", RENDERER, data={"item_cd": ITEM_CD, "book_cd": BOOK_CD, "vol_no": vol_no, "page_no": "", "tool": "1"})
        rec = {"vol_no": vol_no, "renderer_index": m0, "samples": []}
        if r0 is None or r0.status_code != 200:
            result["volumes"].append(rec)
            continue
        pages = parse_page_ids(r0.text)
        rec["page_count"] = len(pages)
        rec["sample_page_ids"] = sample_pages(pages)
        sheet_items = []
        for page_no in rec["sample_page_ids"]:
            rr, rm = req(s, "POST", RENDERER, data={"item_cd": ITEM_CD, "book_cd": BOOK_CD, "vol_no": vol_no, "page_no": page_no, "tool": "1"})
            item = {"page_no": page_no, "renderer": rm}
            if rr is None or rr.status_code != 200:
                rec["samples"].append(item)
                continue
            path = parse_img_path(rr.text)
            item["direct_renderer_img_path"] = path
            if not path:
                rec["samples"].append(item)
                continue
            basename = path.rsplit("/", 1)[-1]
            image_url = BASE + "/ImageServlet.do?" + urlencode({"imgFileNm": basename, "path": path})
            ir, imeta = req(s, "GET", image_url, headers={"Referer": RENDERER, "Accept": "image/jpeg,image/*,*/*;q=0.8"})
            item["image_transport"] = imeta
            if ir is not None and ir.status_code == 200:
                try:
                    image = Image.open(io.BytesIO(ir.content)).convert("RGB")
                    item["valid_image"] = True
                    item["image_size"] = [image.width, image.height]
                    item["image_sha256"] = hashlib.sha256(ir.content).hexdigest()
                    fn = f"{vol_no}-{page_no}.jpg"
                    image.thumbnail((1000, 1400))
                    image.save(out / fn, quality=90)
                    item["sample_file"] = fn
                    sheet_items.append((f"{vol_no}:{page_no}", image.copy()))
                except Exception as exc:
                    item["valid_image"] = False
                    item["image_error"] = f"{type(exc).__name__}: {exc}"
            rec["samples"].append(item)
        sheet = out / f"contact-{vol_no}.jpg"
        make_sheet(sheet_items, sheet)
        if sheet.exists():
            rec["contact_sheet"] = sheet.name
        result["volumes"].append(rec)
    result["conclusion"] = {
        "valid_sample_images": sum(sum(1 for x in v.get("samples", ()) if x.get("valid_image")) for v in result["volumes"]),
        "algorithm_or_runtime_effect": "NONE",
    }
    (out / "g894-visual-sampler.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["conclusion"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
