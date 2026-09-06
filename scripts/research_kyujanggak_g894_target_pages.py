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
BOOK_CD = "GK00894_00"
ITEM_CD = "GJB"
VOL_NO = "0001"
RENDERER = BASE + "/pf01/rendererImg.do"
# These pages are selected from direct visual bracketing in workflow 34022309182:
# 032a visibly contains limits 99-102 and 036a visibly contains 129-131.
# Earlier solar/lunar pages are included only as bounded search neighbors.
TARGET_PAGES = (
    "009a", "009b", "010a", "010b", "011a", "011b",
    "018a", "018b", "019a", "019b", "020a",
    "032a", "032b", "033a", "033b", "034a", "034b",
    "035a", "035b", "036a", "036b", "037a", "037b",
)
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


def parse_img_path(text: str) -> str | None:
    matches = re.findall(r'''var\s+imgFileNm\s*=\s*["']([^"']+)["']''', text)
    return matches[-1] if matches else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/g894-target-pages")
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    result = {
        "schema": "KYUJANGGAK-G894-DIRECT-TARGET-PAGES-R1",
        "book_cd": BOOK_CD,
        "item_cd": ITEM_CD,
        "vol_no": VOL_NO,
        "ocr_used": False,
        "target_values_authorized_by_fetch": False,
        "selection_basis": "DIRECT_VISUAL_BRACKETING_FROM_WORKFLOW_34022309182_PLUS_IMMEDIATE_NEIGHBORS",
        "filename_pattern_inference": "FORBIDDEN",
        "pages": [],
    }
    s = requests.Session(impersonate="chrome")
    s.headers.update({"User-Agent": UA})
    for page_no in TARGET_PAGES:
        rr, rm = req(s, "POST", RENDERER, data={"item_cd": ITEM_CD, "book_cd": BOOK_CD, "vol_no": VOL_NO, "page_no": page_no, "tool": "1"})
        item = {"page_no": page_no, "renderer": rm}
        if rr is None or rr.status_code != 200:
            result["pages"].append(item)
            continue
        path = parse_img_path(rr.text)
        item["direct_renderer_img_path"] = path
        if not path:
            result["pages"].append(item)
            continue
        basename = path.rsplit("/", 1)[-1]
        image_url = BASE + "/ImageServlet.do?" + urlencode({"imgFileNm": basename, "path": path})
        ir, imeta = req(s, "GET", image_url, headers={"Referer": RENDERER, "Accept": "image/jpeg,image/*,*/*;q=0.8"})
        item["image_transport"] = imeta
        if ir is not None and ir.status_code == 200:
            try:
                image = Image.open(io.BytesIO(ir.content))
                item["valid_image"] = True
                item["format"] = image.format
                item["size"] = [image.width, image.height]
                item["image_sha256"] = hashlib.sha256(ir.content).hexdigest()
                fn = f"{VOL_NO}-{page_no}.jpg"
                (out / fn).write_bytes(ir.content)
                item["file"] = fn
            except Exception as exc:
                item["valid_image"] = False
                item["image_error"] = f"{type(exc).__name__}: {exc}"
        result["pages"].append(item)
    result["conclusion"] = {
        "valid_image_count": sum(1 for x in result["pages"] if x.get("valid_image")),
        "requested_page_count": len(TARGET_PAGES),
        "algorithm_or_runtime_effect": "NONE",
    }
    (out / "g894-target-page-map.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["conclusion"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
