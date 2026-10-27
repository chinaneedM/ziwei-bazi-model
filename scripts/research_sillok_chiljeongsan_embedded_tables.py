#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import io
import json
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

BASE = "https://sillok.history.go.kr"
UA = "Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"
TARGETS = {
    "wda_50016011": [
        "/images/slkimg/wda_50016011_01_v.jpg",
        "/images/slkimg/wda_50016011_01_h.jpg",
    ],
    "wda_50016016": [
        "/images/slkimg/wda_50016016_01_v.jpg",
        "/images/slkimg/wda_50016016_01_h.jpg",
        "/images/slkimg/wda_50016016_02_v.jpg",
        "/images/slkimg/wda_50016016_02_h.jpg",
    ],
}


def fetch(url: str) -> tuple[int, str, bytes]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Referer": BASE + "/",
            "Accept": "image/jpeg,image/*,*/*;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return (
                int(getattr(r, "status", 200)),
                r.headers.get("Content-Type", ""),
                r.read(),
            )
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers.get("Content-Type", ""), exc.read()
    except Exception as exc:
        return 0, type(exc).__name__, str(exc).encode("utf-8", "replace")


def main() -> int:
    out = Path("artifacts/sillok-chiljeongsan-embedded-tables")
    out.mkdir(parents=True, exist_ok=True)
    result = {
        "schema": "SILLOK-CHILJEONGSAN-EMBEDDED-TABLE-IMAGES-R1",
        "source_layer": "NIKH_OFFICIAL_ARTICLE_EMBEDDED_TABLE_IMAGE",
        "ocr_used": False,
        "target_values_authorized_by_fetch": False,
        "physical_scan_equivalence": "NOT_ASSUMED",
        "probe_exit_policy": (
            "TRANSPORT_UNAVAILABLE_OR_NON_IMAGE_BYTES_IS_A_RESEARCH_RESULT_NOT_A_CI_FAILURE"
        ),
        "probe_completed": False,
        "probe_outcome": "NOT_RUN",
        "attempt_count": 0,
        "valid_image_count": 0,
        "articles": [],
    }

    for article, paths in TARGETS.items():
        rec = {"article_id": article, "images": []}
        for path in paths:
            url = BASE + path
            status, content_type, body = fetch(url)
            result["attempt_count"] += 1
            item = {
                "path": path,
                "url": url,
                "status": status,
                "content_type": content_type,
                "bytes": len(body),
                "sha256": hashlib.sha256(body).hexdigest(),
            }
            try:
                image = Image.open(io.BytesIO(body))
                item["valid_image"] = True
                item["format"] = image.format
                item["size"] = [image.width, image.height]
                filename = Path(path).name
                (out / filename).write_bytes(body)
                item["file"] = filename
                result["valid_image_count"] += 1
            except Exception as exc:
                item["valid_image"] = False
                item["image_error"] = f"{type(exc).__name__}: {exc}"
                if "text" in content_type.lower() or len(body) < 4096:
                    item["body_prefix"] = body[:600].decode("utf-8", "replace")
            rec["images"].append(item)
        result["articles"].append(rec)

    result["probe_completed"] = True
    if result["valid_image_count"] == result["attempt_count"]:
        result["probe_outcome"] = "ALL_VALID_IMAGE_BYTES"
    elif result["valid_image_count"] > 0:
        result["probe_outcome"] = "PARTIAL_VALID_IMAGE_BYTES"
    else:
        result["probe_outcome"] = "NO_VALID_IMAGE_BYTES"

    (out / "embedded-table-map.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # This is a transport-research probe, not a product verification gate.
    # A remote host/network refusal is preserved in the artifact and must not
    # turn the repository's exact-HEAD CI red. Unhandled script/artifact errors
    # still fail naturally before reaching this return.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
