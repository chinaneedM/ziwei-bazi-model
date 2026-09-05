#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import json
import urllib.request
from pathlib import Path

from PIL import Image

MANIFEST_URL = "https://catalog.lib.kyushu-u.ac.jp/image/manifest/1/820/6631038.json"
UA = "Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"
TARGETS = {
    68: {
        "controls": ["VAR-NUM-LUNAR-L8-LOSSGAIN"],
        "binding": "PRINTED_UPPER_BAND_LIMITS_INCLUDE_1_TO_13; L8_DIRECTLY_VISIBLE",
    },
    69: {
        "controls": ["NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING", "VAR-NUM-LUNAR-L114-DAYRATE"],
        "binding": "PRINTED_LOWER_BAND_LIMITS_INCLUDE_98_TO_117; L101_AND_L114_DIRECTLY_VISIBLE",
    },
    70: {
        "controls": ["VAR-NUM-LUNAR-L132-LOSSGAIN"],
        "binding": "PRINTED_LOWER_BAND_LIMITS_INCLUDE_118_TO_137; L132_DIRECTLY_VISIBLE",
    },
}


def fetch(url: str, timeout: int = 90) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json,image/*,*/*;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def body_for_canvas(canvas: dict) -> dict:
    pages = canvas.get("items") or []
    if not pages:
        raise ValueError("canvas annotation page missing")
    annotations = (pages[0] or {}).get("items") or []
    if not annotations:
        raise ValueError("canvas annotation missing")
    return (annotations[0] or {}).get("body") or {}


def native_url(body: dict) -> str:
    body_id = body.get("id") or body.get("@id")
    if body_id:
        return body_id
    service = body.get("service") or []
    if isinstance(service, dict):
        service = [service]
    if service:
        sid = (service[0] or {}).get("id") or (service[0] or {}).get("@id")
        if sid:
            return sid.rstrip("/") + "/full/max/0/default.jpg"
    raise ValueError("image body/service id missing")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/kyushu-ogawa-target-pages")
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    raw_manifest = fetch(MANIFEST_URL)
    manifest = json.loads(raw_manifest.decode("utf-8"))
    canvases = manifest.get("items") or []
    if manifest.get("type") != "Manifest" or not canvases:
        raise SystemExit("Kyushu IIIF Presentation 3 manifest expected")

    records = []
    for index, target in TARGETS.items():
        canvas = canvases[index]
        body = body_for_canvas(canvas)
        url = native_url(body)
        rec = {
            "canvas_index": index,
            "canvas_id": canvas.get("id"),
            "canvas_label": canvas.get("label"),
            "controls": target["controls"],
            "printed_binding": target["binding"],
            "url": url,
            "ocr_used": False,
            "target_values_authorized_by_fetch": False,
        }
        try:
            body_bytes = fetch(url)
            im = Image.open(io.BytesIO(body_bytes)).convert("RGB")
            path = out / f"canvas-{index:03d}.jpg"
            im.save(path, quality=95)
            rec.update({"status": "OK", "file": path.name, "size": [im.width, im.height], "bytes": len(body_bytes)})
        except Exception as exc:
            rec.update({"status": "ERROR", "error": f"{type(exc).__name__}: {exc}"})
        records.append(rec)

    result = {
        "schema": "KYUSHU-OGAWA-1673-TARGET-PAGES-R1",
        "manifest_url": MANIFEST_URL,
        "title": manifest.get("label"),
        "viewing_direction": manifest.get("viewingDirection"),
        "ocr_used": False,
        "cross_copy_page_offset_used": False,
        "localization_basis": "DIRECT_CONTACT_SHEET_INSPECTION_OF_PRINTED_LIMIT_HEADINGS_IN_THIS_KYUSHU_COPY",
        "target_values_authorized_by_fetch": False,
        "pages": records,
    }
    (out / "target-page-map.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if all(x.get("status") == "OK" for x in records) else 2


if __name__ == "__main__":
    raise SystemExit(main())
