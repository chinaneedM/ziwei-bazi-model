#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import io
import json
import math
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

PIDS = ("14488128", "14488129", "14488130")
BASE = "https://dl.ndl.go.jp"
UA = "Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"


def get_bytes(url: str, timeout: int = 45, attempts: int = 3) -> tuple[bytes, dict[str, str]]:
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": UA, "Accept": "application/json,image/*,*/*;q=0.8"},
            )
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read(), dict(r.headers.items())
        except Exception as exc:
            last = exc
            if attempt + 1 < attempts:
                time.sleep(0.8 * (attempt + 1))
    assert last is not None
    raise last


def manifest_canvases(pid: str) -> tuple[dict, list[dict[str, str]]]:
    url = f"{BASE}/api/iiif/{pid}/manifest.json"
    body, _ = get_bytes(url)
    data = json.loads(body.decode("utf-8"))
    canvases = []
    seqs = data.get("sequences") or []
    for i, c in enumerate((seqs[0].get("canvases") if seqs else []) or [], start=1):
        images = c.get("images") or []
        if not images:
            continue
        resource = images[0].get("resource") or {}
        service = resource.get("service") or {}
        sid = service.get("@id") or service.get("id") or ""
        image_id = sid.rsplit("/", 1)[-1] if sid else f"R{i:07d}"
        canvases.append({
            "index": i,
            "label": str(c.get("label") or i),
            "canvas_id": str(c.get("@id") or c.get("id") or ""),
            "image_service_id": sid,
            "image_id": image_id,
            "thumb_url": f"{sid}/full/1000,/0/default.jpg" if sid else "",
        })
    return data, canvases


def fetch_thumb(rec: dict[str, str], out_dir: Path) -> dict:
    out = dict(rec)
    url = rec["thumb_url"]
    path = out_dir / f"page-{rec['index']:04d}-{rec['image_id']}.jpg"
    try:
        body, headers = get_bytes(url, timeout=45, attempts=2)
        im = Image.open(io.BytesIO(body))
        im.load()
        im = im.convert("RGB")
        im.save(path, quality=86)
        out.update({
            "status": "OK",
            "file": path.name,
            "size": [im.width, im.height],
            "content_type": headers.get("Content-Type") or headers.get("content-type"),
            "bytes": len(body),
        })
    except Exception as exc:
        out.update({"status": "ERROR", "error": f"{type(exc).__name__}: {exc}"})
    return out


def contact_sheet(records: list[dict], img_dir: Path, out: Path, cols: int = 4) -> None:
    ok = [r for r in records if r.get("status") == "OK"]
    if not ok:
        return
    cell_w, cell_h, label_h = 270, 360, 32
    rows = math.ceil(len(ok) / cols)
    canvas = Image.new("RGB", (cell_w * cols, (cell_h + label_h) * rows), "white")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    for i, rec in enumerate(ok):
        im = Image.open(img_dir / rec["file"]).convert("RGB")
        thumb = ImageOps.contain(im, (cell_w - 8, cell_h - 8))
        x = (i % cols) * cell_w
        y = (i // cols) * (cell_h + label_h)
        canvas.paste(thumb, (x + (cell_w-thumb.width)//2, y + (cell_h-thumb.height)//2))
        draw.text((x+5, y+cell_h+6), f"{rec['index']} {rec['label']} {rec['image_id']}", fill="black", font=font)
    canvas.save(out, quality=88)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/ndl-ogawa-shoushi-licheng")
    args = ap.parse_args()
    root = Path(args.output)
    root.mkdir(parents=True, exist_ok=True)

    summary = {
        "schema": "NDL-OGAWA-SHOUSHI-LICHENG-IIIF-PROBE-R1",
        "edition": "Ogawa Masaoki new collation, Kanbun 13 / 1673",
        "title": "大元授時暦經立成 6卷",
        "ocr_used": False,
        "target_values_authorized": False,
        "pids": [],
    }

    for pid in PIDS:
        pdir = root / pid
        idir = pdir / "pages"
        idir.mkdir(parents=True, exist_ok=True)
        manifest, canvases = manifest_canvases(pid)
        (pdir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            records = list(pool.map(lambda r: fetch_thumb(r, idir), canvases))

        for chunk_no, start in enumerate(range(0, len(records), 20), start=1):
            contact_sheet(
                records[start:start+20],
                idir,
                pdir / f"contact-{chunk_no:02d}.jpg",
            )

        (pdir / "page-map.json").write_text(
            json.dumps({
                "schema": "NDL-OGAWA-SHOUSHI-LICHENG-PAGE-MAP-R1",
                "pid": pid,
                "ocr_used": False,
                "pages": records,
            }, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        summary["pids"].append({
            "pid": pid,
            "manifest_url": f"{BASE}/api/iiif/{pid}/manifest.json",
            "canvas_count": len(canvases),
            "fetch_ok": sum(r.get("status") == "OK" for r in records),
            "fetch_error": sum(r.get("status") == "ERROR" for r in records),
        })

    (root / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
