#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import io
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

BASES = ["https://sillok.history.go.kr", "http://sillok.history.go.kr"]
TOKENS = ["da/ide_d156006a00", "da/ide_d156013a00"]
UA = "Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"

def fetch(url: str) -> tuple[int, str, bytes]:
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "image/jpeg,image/*,*/*;q=0.8",
        "Referer": "https://sillok.history.go.kr/",
    })
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return int(getattr(r, "status", 200)), r.headers.get("Content-Type", ""), r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type", ""), e.read()
    except Exception as e:
        return 0, type(e).__name__, str(e).encode("utf-8", "replace")

def candidates(token: str) -> list[str]:
    current = "/images/org_images/" + token + ".jpg"
    legacy = "/s_img/SILLOK/" + token + ".jpg"
    out = []
    for base in BASES:
        out.append(base + current)
    for base in BASES:
        out.append(base + "/viewer/imageProxy.do?filePath=" + urllib.parse.quote(current, safe="/"))
    for base in BASES:
        out.append(base + legacy)
    for base in BASES:
        out.append(base + "/viewer/imageProxy.do?filePath=" + urllib.parse.quote(legacy, safe="/"))
    return out

def main() -> int:
    out = Path("artifacts/sillok-native-transport-probe")
    out.mkdir(parents=True, exist_ok=True)
    result = {
        "schema": "SILLOK-NATIVE-TRANSPORT-PROBE-R1",
        "ocr_used": False,
        "target_values_authorized": False,
        "tokens": [],
    }
    success = False
    for token in TOKENS:
        rec = {"token": token, "attempts": []}
        for url in candidates(token):
            status, ctype, body = fetch(url)
            item = {
                "url": url,
                "status": status,
                "content_type": ctype,
                "bytes": len(body),
                "sha256": hashlib.sha256(body).hexdigest(),
            }
            try:
                im = Image.open(io.BytesIO(body))
                item["valid_image"] = True
                item["format"] = im.format
                item["size"] = [im.width, im.height]
                success = True
            except Exception as exc:
                item["valid_image"] = False
                item["image_error"] = type(exc).__name__
                if "text" in ctype.lower() or len(body) < 4096:
                    item["body_prefix"] = body[:600].decode("utf-8", "replace")
            rec["attempts"].append(item)
        result["tokens"].append(rec)
    (out / "transport-probe.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if success else 2

if __name__ == "__main__":
    raise SystemExit(main())
