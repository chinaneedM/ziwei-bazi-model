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
from PIL import Image

BASE = "https://kyudb.snu.ac.kr"
BOOK_CD = "GK26775_00"
ITEM_CD = "BBG"
VOL_NO = "0001"
PAGES = ("027a","027b","028a","028b","029a","029b","030a","030b")
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

def img_path(text: str) -> str | None:
    matches = re.findall(r'''var\s+imgFileNm\s*=\s*["']([^"']+)["']''', text)
    return matches[-1] if matches else None

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/kyujanggak-1930-g893-window")
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    s = requests.Session(impersonate="chrome")
    s.headers.update({"User-Agent": UA})
    result = {
        "schema": "KYUJANGGAK-1930-G893-TARGET-WINDOW-R1",
        "book_cd": BOOK_CD,
        "item_cd": ITEM_CD,
        "vol_no": VOL_NO,
        "page_ids": list(PAGES),
        "ocr_used": False,
        "role": "DIRECT_NUMERIC_ORDER_ENTRY_LOCALIZATION_ONLY",
        "g893_identity_authorized": False,
        "target_values_authorized": False,
        "pages": [],
    }

    for page_no in PAGES:
        rr, rm = req(
            s, "POST", RENDERER,
            data={"item_cd": ITEM_CD, "book_cd": BOOK_CD, "vol_no": VOL_NO, "page_no": page_no, "tool": "1"},
        )
        rec = {"page_no": page_no, "renderer": rm}
        if rr is None or rr.status_code != 200:
            result["pages"].append(rec)
            continue
        path = img_path(rr.text)
        rec["direct_renderer_img_path"] = path
        if not path:
            result["pages"].append(rec)
            continue
        base = path.rsplit("/", 1)[-1]
        image_url = BASE + "/ImageServlet.do?" + urlencode({"imgFileNm": base, "path": path})
        ir, imeta = req(
            s, "GET", image_url,
            headers={"Referer": RENDERER, "Accept": "image/jpeg,image/*,*/*;q=0.8"},
        )
        rec["image_transport"] = imeta
        if ir is not None and ir.status_code == 200:
            try:
                image = Image.open(io.BytesIO(ir.content)).convert("RGB")
                rec["valid_image"] = True
                rec["image_size"] = [image.width, image.height]
                rec["image_sha256"] = hashlib.sha256(ir.content).hexdigest()
                fn = f"{VOL_NO}-{page_no}.jpg"
                image.save(out / fn, quality=96)
                rec["file"] = fn
            except Exception as exc:
                rec["valid_image"] = False
                rec["image_error"] = f"{type(exc).__name__}: {exc}"
        result["pages"].append(rec)

    result["conclusion"] = {
        "valid_images": sum(1 for p in result["pages"] if p.get("valid_image")),
        "visual_review_required": True,
        "g893_entry_status": "PENDING_DIRECT_VISUAL_REVIEW",
        "identity_effect": "NONE_UNTIL_ENTRY_IS_READ",
        "target_effect": "NONE",
    }
    (out / "target-window.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result["conclusion"], ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
