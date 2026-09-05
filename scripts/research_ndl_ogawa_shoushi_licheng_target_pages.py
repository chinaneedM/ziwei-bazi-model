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
    3: ["VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE_LOCATOR_CANDIDATE"],
    4: ["SOLAR-D16-CONTEXT-ADD-ACCUMULATED-COLUMNS"],
    13: ["STRUCT-LUNAR-CHIJI-TABLE-HEADER"],
    14: ["VAR-NUM-LUNAR-L8-LOSSGAIN"],
    18: ["NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING"],
    19: ["VAR-NUM-LUNAR-L114-DAYRATE"],
    20: ["VAR-NUM-LUNAR-L132-LOSSGAIN"],
}
UNRESOLVED_CONTROLS = {
    "VAR-NUM-LUNAR-L124-JI-XINGDU": (
        "R0000019 is a Taiyin chiji table page and must not be promoted to evidence for the separate ji-xingdu field; "
        "locate the actual xingdu table or record this field as absent from this witness."
    )
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
    ap.add_argument("--width", type=int, default=7392)
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
        "localization_basis": "DIRECT_PRINTED_VOLUME_TABLE_AND_LIMIT_HEADINGS_FROM_PRIOR_CONTACT_SHEET_AND_NATIVE_PAGE_INSPECTION",
        "cross_copy_page_offset_used": False,
        "native_canvas_width_px": 7392,
        "solar_d16_locator_revision": {
            "previous_canvas_index": 4,
            "previous_image_id": "R0000004",
            "inspection_result": "CONTEXT_PAGE_PRINTS_D16_DERIVED_ADD_AND_ACCUMULATED_COLUMNS_BUT_NOT_THE_TARGET_DIFFERENCE_COLUMN",
            "new_locator_candidate_canvas_index": 3,
            "new_locator_candidate_image_id": "R0000003",
            "candidate_status": "FETCH_FOR_DIRECT_FIELD_BINDING_NOT_TARGET_VALUE_AUTHORIZATION",
        },
        "structural_header_binding": {
            "canvas_index": 13,
            "image_id": "R0000013",
            "printed_title": "太陰遲疾立成",
            "visible_fields": ["限數", "遲疾曆日率", "損益分", "遲疾積"],
            "purpose": "FIELD_CONTEXT_ONLY_NOT_A_TARGET_NUMERIC_READING",
        },
        "target_values_authorized_by_fetch": False,
        "unresolved_controls": UNRESOLVED_CONTROLS,
        "pages": records,
    }
    (out / "target-page-map.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if all(x.get("status") == "OK" for x in records) else 2


if __name__ == "__main__":
    raise SystemExit(main())
