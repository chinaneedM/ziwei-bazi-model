#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import json
import math
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

MANIFEST_URL = "https://catalog.lib.kyushu-u.ac.jp/image/manifest/1/820/6631038.json"
UA = "Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"


def fetch(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json,image/*,*/*;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def canvas_image_url(canvas: dict) -> str | None:
    images = canvas.get("images") or []
    if not images:
        return None
    resource = (images[0] or {}).get("resource") or {}
    service = resource.get("service") or {}
    service_id = service.get("@id") or service.get("id")
    if service_id:
        return service_id.rstrip("/") + "/full/600,/0/default.jpg"
    return resource.get("@id") or resource.get("id")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/kyushu-ogawa-contact-sheet")
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    raw = fetch(MANIFEST_URL)
    manifest = json.loads(raw.decode("utf-8"))
    (out / "manifest.json").write_bytes(raw)

    sequences = manifest.get("sequences") or []
    if not sequences:
        raise SystemExit("IIIF v2 sequence missing")
    canvases = sequences[0].get("canvases") or []

    records: list[dict] = []
    thumbs: list[tuple[int, Image.Image]] = []
    for index, canvas in enumerate(canvases):
        url = canvas_image_url(canvas)
        rec = {
            "canvas_index": index,
            "canvas_id": canvas.get("@id") or canvas.get("id"),
            "label": canvas.get("label"),
            "image_url": url,
            "ocr_used": False,
            "target_value_authorized": False,
        }
        if not url:
            rec["status"] = "NO_IMAGE"
            records.append(rec)
            continue
        try:
            body = fetch(url)
            im = Image.open(io.BytesIO(body)).convert("RGB")
            rec.update({"status": "OK", "size": [im.width, im.height], "bytes": len(body)})
            thumbs.append((index, im))
        except Exception as exc:
            rec.update({"status": "ERROR", "error": f"{type(exc).__name__}: {exc}"})
        records.append(rec)

    cell_w, cell_h = 620, 500
    cols = 4
    rows = max(1, math.ceil(len(thumbs) / cols))
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for pos, (index, im) in enumerate(thumbs):
        x = (pos % cols) * cell_w
        y = (pos // cols) * cell_h
        copy = im.copy()
        copy.thumbnail((cell_w - 20, cell_h - 35))
        sheet.paste(copy, (x + 10, y + 25))
        draw.text((x + 10, y + 5), f"canvas={index}", fill="black", font=font)
    sheet.save(out / "contact-sheet.jpg", quality=90)

    result = {
        "schema": "KYUSHU-OGAWA-1673-IIIF-CONTACT-SHEET-R1",
        "manifest_url": MANIFEST_URL,
        "manifest_label": manifest.get("label"),
        "canvas_count": len(canvases),
        "fetched_image_count": len(thumbs),
        "ocr_used": False,
        "page_offset_assumption": False,
        "target_value_authorized_by_contact_sheet": False,
        "localization_rule": "BIND_TARGETS_BY_PRINTED_TABLE_TITLE_LIMIT_HEADING_AND_FIELD_CONTEXT_NOT_BY_NDL_OR_CADAL_OFFSET",
        "pages": records,
    }
    (out / "page-map.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if thumbs else 2


if __name__ == "__main__":
    raise SystemExit(main())
