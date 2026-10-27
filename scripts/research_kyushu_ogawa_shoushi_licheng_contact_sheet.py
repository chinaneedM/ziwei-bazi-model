#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import json
import math
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

MANIFEST_URL = "https://catalog.lib.kyushu-u.ac.jp/image/manifest/1/820/6631038.json"
UA = "Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"
CONTACT_WIDTH = 320


def fetch(url: str, timeout: int = 45) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json,image/*,*/*;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def manifest_canvases(manifest: dict) -> tuple[str, list[dict]]:
    sequences = manifest.get("sequences") or []
    if sequences:
        return "IIIF_PRESENTATION_2", sequences[0].get("canvases") or []
    if manifest.get("type") == "Manifest" and isinstance(manifest.get("items"), list):
        return "IIIF_PRESENTATION_3", manifest["items"]
    raise SystemExit("unsupported IIIF manifest structure")


def canvas_image_url(canvas: dict) -> str | None:
    images = canvas.get("images") or []
    if images:
        resource = (images[0] or {}).get("resource") or {}
        service = resource.get("service") or {}
        if isinstance(service, list):
            service = service[0] if service else {}
        service_id = service.get("@id") or service.get("id")
        if service_id:
            return service_id.rstrip("/") + f"/full/{CONTACT_WIDTH},/0/default.jpg"
        return resource.get("@id") or resource.get("id")

    pages = canvas.get("items") or []
    if not pages:
        return None
    annotations = (pages[0] or {}).get("items") or []
    if not annotations:
        return None
    body = (annotations[0] or {}).get("body") or {}
    service = body.get("service") or []
    if isinstance(service, dict):
        service = [service]
    if service:
        service_id = (service[0] or {}).get("id") or (service[0] or {}).get("@id")
        if service_id:
            return service_id.rstrip("/") + f"/full/{CONTACT_WIDTH},/0/default.jpg"
    body_id = body.get("id") or body.get("@id")
    if body_id:
        if "/full/max/" in body_id:
            return body_id.replace("/full/max/", f"/full/{CONTACT_WIDTH},/")
        return body_id
    return None


def fetch_canvas(index: int, canvas: dict) -> tuple[int, dict, Image.Image | None]:
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
        return index, rec, None
    try:
        body = fetch(url)
        im = Image.open(io.BytesIO(body)).convert("RGB")
        rec.update({"status": "OK", "size": [im.width, im.height], "bytes": len(body)})
        return index, rec, im
    except Exception as exc:
        rec.update({"status": "ERROR", "error": f"{type(exc).__name__}: {exc}"})
        return index, rec, None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/kyushu-ogawa-contact-sheet")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    raw = fetch(MANIFEST_URL)
    manifest = json.loads(raw.decode("utf-8"))
    (out / "manifest.json").write_bytes(raw)
    presentation_version, canvases = manifest_canvases(manifest)

    records_by_index: dict[int, dict] = {}
    images_by_index: dict[int, Image.Image] = {}
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = [pool.submit(fetch_canvas, index, canvas) for index, canvas in enumerate(canvases)]
        for future in as_completed(futures):
            index, rec, im = future.result()
            records_by_index[index] = rec
            if im is not None:
                images_by_index[index] = im

    records = [records_by_index[i] for i in range(len(canvases))]
    thumbs = [(i, images_by_index[i]) for i in sorted(images_by_index)]

    cell_w, cell_h = 340, 280
    cols = 5
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
        "presentation_version": presentation_version,
        "viewing_direction": manifest.get("viewingDirection"),
        "canvas_count": len(canvases),
        "contact_width_px": CONTACT_WIDTH,
        "workers": max(1, args.workers),
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
