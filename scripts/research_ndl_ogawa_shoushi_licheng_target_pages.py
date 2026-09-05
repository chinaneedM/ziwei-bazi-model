#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import json
import time
import urllib.request
from pathlib import Path

from PIL import Image

PID = "14488128"
BASE = "https://dl.ndl.go.jp/api/iiif"
UA = "Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"
TARGETS = {
    4: ["VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE"],
    14: ["VAR-NUM-LUNAR-L8-LOSSGAIN"],
    18: ["NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING"],
    19: ["VAR-NUM-LUNAR-L114-DAYRATE", "VAR-NUM-LUNAR-L124-JI-XINGDU"],
    20: ["VAR-NUM-LUNAR-L132-LOSSGAIN"],
}


def fetch(url: str, attempts: int = 3, timeout: int = 60) -> tuple[bytes, dict[str, str]]:
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "image/*,*/*;q=0.8"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read(), dict(r.headers.items())
        except Exception as exc:
            last = exc
            if attempt + 1 < attempts:
                time.sleep(1.0 * (attempt + 1))
    assert last is not None
    raise last


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/ndl-ogawa-target-pages")
    ap.add_argument("--width", type=int, default=3000)
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    records = []
    for page, controls in TARGETS.items():
        image_id = f"R{page:07d}"
        url = f"{BASE}/{PID}/{image_id}/full/{args.width},/0/default.jpg"
        rec = {
            "pid": PID,
            "canvas_index": page,
            "image_id": image_id,
            "controls": controls,
            "url": url,
            "ocr_used": False,
            "target_values_authorized_by_fetch": False,
        }
        try:
            body, headers = fetch(url)
            im = Image.open(io.BytesIO(body))
            im.load()
            im = im.convert("RGB")
            path = out / f"page-{page:04d}-{image_id}-w{args.width}.jpg"
            im.save(path, quality=94)
            rec.update({
                "status": "OK",
                "file": path.name,
                "size": [im.width, im.height],
                "bytes": len(body),
                "content_type": headers.get("Content-Type") or headers.get("content-type"),
            })
        except Exception as exc:
            rec.update({"status": "ERROR", "error": f"{type(exc).__name__}: {exc}"})
        records.append(rec)

    result = {
        "schema": "NDL-OGAWA-SHOUSHI-LICHENG-TARGET-PAGES-R1",
        "edition": "Ogawa Masaoki new collation, Kanbun 13 / 1673",
        "title": "大元授時暦經立成 6卷",
        "pid": PID,
        "ocr_used": False,
        "localization_basis": "DIRECT_PRINTED_VOLUME_TABLE_AND_LIMIT_HEADINGS_FROM_PRIOR_1000PX_CONTACT_SHEET_INSPECTION",
        "cross_copy_page_offset_used": False,
        "target_values_authorized_by_fetch": False,
        "pages": records,
    }
    (out / "target-page-map.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if all(x.get("status") == "OK" for x in records) else 2


if __name__ == "__main__":
    raise SystemExit(main())
