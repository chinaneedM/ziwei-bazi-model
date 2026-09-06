#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import io
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

BASE = "https://sillok.history.go.kr"
UA = "Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"
START_IMAGE_ID = "ide_d156006a00"
MAX_STEPS = 10


def fetch(url: str, accept: str, timeout: int = 15, attempts: int = 3) -> tuple[int, str, bytes, int]:
    last = (0, "NOT_RUN", b"", 0)
    for attempt in range(1, attempts + 1):
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": UA,
                "Accept": accept,
                "Referer": BASE + "/popup/viewer.do?id=wda_50016011&type=view",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return (
                    int(getattr(response, "status", 200)),
                    response.headers.get("Content-Type", ""),
                    response.read(),
                    attempt,
                )
        except urllib.error.HTTPError as exc:
            last = (exc.code, exc.headers.get("Content-Type", ""), exc.read(), attempt)
        except Exception as exc:
            last = (0, type(exc).__name__, str(exc).encode("utf-8", "replace"), attempt)
        if attempt < attempts:
            time.sleep(1.5 * attempt)
    return last


def api_record(*, image_id: str | None = None, seq: str | None = None) -> tuple[dict | None, dict]:
    if (image_id is None) == (seq is None):
        raise ValueError("exactly one of image_id or seq is required")
    query = urllib.parse.urlencode({"imageId": image_id} if image_id is not None else {"seq": seq})
    url = BASE + "/search/ajaxSelectImageInfo.do?" + query
    status, content_type, body, attempt = fetch(
        url,
        "application/json,text/plain,*/*;q=0.8",
    )
    meta = {
        "url": url,
        "status": status,
        "content_type": content_type,
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "attempt": attempt,
    }
    try:
        parsed = json.loads(body.decode("utf-8", "replace"))
    except Exception as exc:
        meta["parse_error"] = f"{type(exc).__name__}: {exc}"
        if "text" in content_type.lower() or len(body) < 4096:
            meta["body_prefix"] = body[:800].decode("utf-8", "replace")
        return None, meta
    if not isinstance(parsed, list):
        meta["parse_error"] = "JSON_RESPONSE_IS_NOT_LIST"
        return None, meta
    leaves = [item for item in parsed if str(item.get("level")) == "4"]
    meta["record_count"] = len(parsed)
    meta["leaf_record_count"] = len(leaves)
    if not leaves:
        meta["records"] = parsed[:20]
        return None, meta
    record = leaves[0]
    meta["selected_leaf"] = {
        key: record.get(key)
        for key in ("seq", "kingCode", "imageId", "title", "previous", "next", "firstchild", "endchild", "level")
    }
    return record, meta


def fetch_image(record: dict, out: Path, index: int) -> dict:
    king_code = str(record.get("kingCode") or "").strip("/")
    image_id = str(record.get("imageId") or "")
    url = f"{BASE}/images/org_images/{king_code}/{image_id}.jpg"
    status, content_type, body, attempt = fetch(
        url,
        "image/jpeg,image/*,*/*;q=0.8",
        timeout=20,
        attempts=4,
    )
    item = {
        "url": url,
        "status": status,
        "content_type": content_type,
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "attempt": attempt,
        "valid_image": False,
    }
    try:
        image = Image.open(io.BytesIO(body)).convert("RGB")
        item["valid_image"] = True
        item["size"] = [image.width, image.height]
        filename = f"{index:02d}-{king_code}-{image_id}.jpg".replace("/", "-")
        image.save(out / filename, quality=95)
        item["file"] = filename
    except Exception as exc:
        item["image_error"] = f"{type(exc).__name__}: {exc}"
        if "text" in content_type.lower() or len(body) < 4096:
            item["body_prefix"] = body[:800].decode("utf-8", "replace")
    return item


def main() -> int:
    out = Path("artifacts/sillok-image-tree-walk")
    out.mkdir(parents=True, exist_ok=True)
    result = {
        "schema": "SILLOK-OFFICIAL-IMAGE-TREE-WALK-R1",
        "source_id": "EXT-NIKH-SEJONG-SILLOK-V156-CHILJEONGSAN-TABLES",
        "article_id": "wda_50016011",
        "article_title": "太陽冬至前後二象盈初縮末限",
        "official_start_location": "60冊 156卷 6張 A面",
        "start_image_id": START_IMAGE_ID,
        "start_image_id_evidence": "PRIOR_DIRECT_OFFICIAL_VIEWER_IMGARR_BINDING",
        "navigation_evidence": "OFFICIAL_VIEWER_JAVASCRIPT_AJAXSELECTIMAGEINFO_NEXT_NODE_CHAIN",
        "ocr_used": False,
        "target_values_authorized_by_navigation": False,
        "sequential_filename_inference_used": False,
        "runtime_effect": "NONE",
        "walk": [],
        "outcome": "NOT_RUN",
    }

    current, start_meta = api_record(image_id=START_IMAGE_ID)
    result["start_api"] = start_meta
    if current is None:
        result["outcome"] = "START_API_UNAVAILABLE"
    else:
        seen: set[str] = set()
        for index in range(MAX_STEPS):
            seq = str(current.get("seq") or "")
            if not seq or seq in seen:
                result["outcome"] = "TREE_WALK_STOPPED_EMPTY_OR_REPEATED_SEQ"
                break
            seen.add(seq)
            node = {
                "index": index,
                "seq": seq,
                "kingCode": current.get("kingCode"),
                "imageId": current.get("imageId"),
                "title": current.get("title"),
                "previous": current.get("previous"),
                "next": current.get("next"),
                "firstchild": current.get("firstchild"),
                "endchild": current.get("endchild"),
                "level": current.get("level"),
                "image": fetch_image(current, out, index),
            }
            result["walk"].append(node)
            next_seq = str(current.get("next") or "")
            if not next_seq:
                result["outcome"] = "TREE_WALK_REACHED_END"
                break
            nxt, next_meta = api_record(seq=next_seq)
            node["next_api"] = next_meta
            if nxt is None:
                result["outcome"] = "NEXT_API_UNAVAILABLE"
                break
            current = nxt
        else:
            result["outcome"] = "MAX_STEPS_REACHED"

    result["valid_image_count"] = sum(
        1 for item in result["walk"] if item.get("image", {}).get("valid_image")
    )
    result["observed_tree_node_count"] = len(result["walk"])
    (out / "image-tree-walk.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    # External site availability is evidence state, not a product CI gate.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
