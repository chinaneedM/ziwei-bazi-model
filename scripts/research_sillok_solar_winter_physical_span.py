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
# The endpoints are independently bound by official Sillok article locations:
# wda_50016011 starts at 60冊 156卷 6張 A面 and wda_50016012 starts at
# 60冊 156卷 9張 B面. The interior names below are transport candidates only
# until the official server returns valid image bytes and the page is inspected.
CANDIDATE_TOKENS = [
    "da/ide_d156006b00",
    "da/ide_d156007a00",
    "da/ide_d156007b00",
    "da/ide_d156008a00",
    "da/ide_d156008b00",
    "da/ide_d156009a00",
]


def fetch(url: str) -> tuple[int, str, bytes]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "image/jpeg,image/*,*/*;q=0.8",
            "Referer": BASE + "/id/wda_50016011",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return (
                int(getattr(response, "status", 200)),
                response.headers.get("Content-Type", ""),
                response.read(),
            )
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers.get("Content-Type", ""), exc.read()
    except Exception as exc:
        return 0, type(exc).__name__, str(exc).encode("utf-8", "replace")


def main() -> int:
    out = Path("artifacts/sillok-solar-winter-physical-span")
    out.mkdir(parents=True, exist_ok=True)
    result = {
        "schema": "SILLOK-SOLAR-WINTER-PHYSICAL-SPAN-PROBE-R1",
        "article_id": "wda_50016011",
        "article_title": "太陽冬至前後二象盈初縮末限",
        "official_start_location": "60冊 156卷 6張 A面",
        "next_article_id": "wda_50016012",
        "next_article_official_start_location": "60冊 156卷 9張 B面",
        "candidate_token_basis": (
            "INTERIOR_PHYSICAL_LEAVES_BETWEEN_TWO_OFFICIALLY_BOUND_ARTICLE_LOCATIONS; "
            "TOKEN_PATTERN_ALONE_HAS_NO_EVIDENTIARY_AUTHORITY"
        ),
        "ocr_used": False,
        "target_values_authorized_by_fetch": False,
        "candidate_as_direct_binding": "FORBIDDEN_UNTIL_VALID_OFFICIAL_IMAGE_BYTES_ARE_OBSERVED",
        "valid_image_as_target_reading": "FORBIDDEN_UNTIL_DIRECT_HUMAN_VISUAL_COLLATION",
        "probe_outcome": "NOT_RUN",
        "pages": [],
    }

    for token in CANDIDATE_TOKENS:
        url = f"{BASE}/images/org_images/{token}.jpg"
        status, content_type, body = fetch(url)
        item = {
            "candidate_token": token,
            "url": url,
            "status": status,
            "content_type": content_type,
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
            "valid_image": False,
        }
        try:
            image = Image.open(io.BytesIO(body)).convert("RGB")
            item["valid_image"] = True
            item["size"] = [image.width, image.height]
            filename = token.split("/")[-1] + ".jpg"
            image.save(out / filename, quality=95)
            item["file"] = filename
            item["binding_status"] = (
                "DIRECT_OFFICIAL_IMAGE_BYTES_OBSERVED_REQUIRES_VISUAL_PAGE_ADJUDICATION"
            )
        except Exception as exc:
            item["image_error"] = f"{type(exc).__name__}: {exc}"
            item["binding_status"] = "UNOBSERVED_CANDIDATE_ONLY"
            if "text" in content_type.lower() or len(body) < 4096:
                item["body_prefix"] = body[:600].decode("utf-8", "replace")
        result["pages"].append(item)

    valid = sum(1 for page in result["pages"] if page["valid_image"])
    if valid == len(result["pages"]):
        result["probe_outcome"] = "ALL_INTERIOR_CANDIDATES_RETURNED_VALID_OFFICIAL_IMAGE_BYTES"
    elif valid:
        result["probe_outcome"] = "PARTIAL_INTERIOR_CANDIDATES_RETURNED_VALID_OFFICIAL_IMAGE_BYTES"
    else:
        result["probe_outcome"] = "NO_INTERIOR_CANDIDATE_RETURNED_VALID_OFFICIAL_IMAGE_BYTES"

    (out / "physical-span-probe.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    # External transport availability is a research result, not a product CI gate.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
