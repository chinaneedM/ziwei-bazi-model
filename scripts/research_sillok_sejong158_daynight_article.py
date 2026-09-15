#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from pathlib import Path

from curl_cffi import requests

BASE = "https://sillok.history.go.kr"
PREFIX = "wda_50018"
TARGETS = (
    "日出入隨處各異",
    "內篇據漢陽日至之晷",
    "二至後日出入晝夜辰刻",
)
UA = "Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"


def fetch(session, url: str):
    errors = []
    for attempt in range(1, 4):
        try:
            r = session.get(url, timeout=25)
            return r, {
                "status": r.status_code,
                "url": r.url,
                "bytes": len(r.content),
                "content_type": r.headers.get("content-type", ""),
                "sha256": hashlib.sha256(r.content).hexdigest(),
                "attempt": attempt,
            }
        except Exception as exc:
            errors.append({"attempt": attempt, "type": type(exc).__name__, "error": str(exc)})
            time.sleep(0.7 * attempt)
    return None, {"status": 0, "url": url, "errors": errors}


def text_only(html: str) -> str:
    s = re.sub(r"<script\b.*?</script>", " ", html, flags=re.I | re.S)
    s = re.sub(r"<style\b.*?</style>", " ", s, flags=re.I | re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", "", s)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/sillok-sejong158-daynight-article")
    ap.add_argument("--max-article", type=int, default=80)
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    session = requests.Session(impersonate="chrome")
    session.headers.update({"User-Agent": UA, "Accept-Language": "ko-KR,ko;q=0.9,zh-CN;q=0.8"})

    result = {
        "schema": "SILLOK-SEJONG158-DAYNIGHT-ARTICLE-LOCATOR-R1",
        "discovery_only": True,
        "article_id_inference_as_evidence": "FORBIDDEN",
        "acceptance_rule": "ONLY_AN_OFFICIAL_RESPONSE_WHOSE_BODY_CONTAINS_TARGET_TEXT_MAY_BIND_THE_ARTICLE_ID",
        "targets": list(TARGETS),
        "probes": [],
        "matches": [],
    }
    for n in range(1, args.max_article + 1):
        article_id = f"{PREFIX}{n:03d}"
        url = f"{BASE}/id/{article_id}"
        r, meta = fetch(session, url)
        rec = {"article_id": article_id, "transport": meta}
        if r is None or r.status_code != 200:
            result["probes"].append(rec)
            continue
        html = r.text
        compact = text_only(html)
        hits = [t for t in TARGETS if t in compact]
        rec["target_hits"] = hits
        title = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.I | re.S)
        if title:
            rec["html_title"] = re.sub(r"\s+", " ", title.group(1)).strip()
        # Record viewer links only if emitted by the accepted article response.
        viewer_links = sorted(set(re.findall(r'''(?:href|onclick)=["'][^"']*(?:popup/viewer\.do|viewer\.do)[^"']*["']''', html, flags=re.I)))
        rec["viewer_link_fragments"] = viewer_links[:20]
        if hits:
            fn = f"{article_id}.html"
            (out / fn).write_text(html, encoding="utf-8")
            rec["saved_html"] = fn
            result["matches"].append(rec)
        result["probes"].append(rec)
    result["conclusion"] = {
        "match_count": len(result["matches"]),
        "matched_article_ids": [x["article_id"] for x in result["matches"]],
        "glyph_authority": "OFFICIAL_HTML_TRANSCRIPTION_ONLY; PHYSICAL_IMAGE_STILL_REQUIRED",
        "algorithm_or_runtime_effect": "NONE",
    }
    (out / "article-locator.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["conclusion"], ensure_ascii=False, indent=2))
    return 0 if result["matches"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
