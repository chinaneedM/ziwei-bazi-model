#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://sillok.history.go.kr"
UA = "Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"
ARTICLES = {
    "wda_50016011": {
        "table_identity": "SOLAR_YINGSUO",
        "title": "太陽冬至前後二象盈初縮末限",
        "taebaeksan_location": "60冊 156卷 6張 A面",
        "controls": ["VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE"],
    },
    "wda_50016016": {
        "table_identity": "LUNAR_CHIJI",
        "title": "太陰限數遲疾度",
        "taebaeksan_location": "60冊 156卷 13張 A面",
        "controls": [
            "VAR-NUM-LUNAR-L8-LOSSGAIN",
            "NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING",
            "VAR-NUM-LUNAR-L114-DAYRATE",
            "VAR-NUM-LUNAR-L124-JI-XINGDU",
            "VAR-NUM-LUNAR-L132-LOSSGAIN",
        ],
    },
}
PATTERNS = (
    re.compile(r"""(?i)(?:href|src)\s*=\s*["']([^"']*(?:viewer|imageproxy|image|original|popup)[^"']*)["']"""),
    re.compile(r"""(?i)(?:onclick|data-[\w-]+)\s*=\s*["']([^"']*(?:viewer|image|original|popup|wda_)[^"']*)["']"""),
    re.compile(r"""(?i)["']([^"']*(?:viewer\.do|imageProxy\.do|/s_img/SILLOK/|\.jpg|\.jpeg|\.png)[^"']*)["']"""),
)

def fetch(url: str, timeout: int = 12) -> tuple[int, str, bytes]:
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,image/avif,image/webp,image/*,*/*;q=0.8",
        "Referer": BASE + "/",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            return int(getattr(r, "status", 200)), r.headers.get("Content-Type", ""), body
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type", ""), e.read()
    except Exception as e:
        return 0, type(e).__name__, str(e).encode("utf-8", "replace")

def compact_context(text: str, needle: str, radius: int = 240) -> str:
    out = []
    lower = text.lower()
    start = 0
    nlow = needle.lower()
    while len(out) < 12:
        i = lower.find(nlow, start)
        if i < 0:
            break
        out.append(text[max(0, i-radius): min(len(text), i+len(needle)+radius)])
        start = i + len(needle)
    return "\n---\n".join(out)

def normalize_candidate(raw: str) -> str:
    value = html.unescape(raw).replace("\\/", "/").strip()
    if value.startswith("//"):
        return "https:" + value
    if value.startswith("/"):
        return BASE + value
    if value.startswith("http://") or value.startswith("https://"):
        return value
    return value

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/sillok-chiljeongsan-image-routes")
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    result = {
        "schema": "SILLOK-CHILJEONGSAN-IMAGE-ROUTE-PROBE-R1",
        "base": BASE,
        "ocr_used": False,
        "target_values_authorized": False,
        "article_html_as_target_value": "FORBIDDEN",
        "viewer_route_as_target_value": "FORBIDDEN",
        "articles": [],
    }

    for article_id, meta in ARTICLES.items():
        article_url = f"{BASE}/id/{article_id}"
        status, ctype, body = fetch(article_url)
        text = body.decode("utf-8", "replace")
        (out / f"{article_id}.html").write_text(text, encoding="utf-8")

        raw_candidates = []
        for pat in PATTERNS:
            for m in pat.finditer(text):
                raw_candidates.append(m.group(1))
        candidates = []
        seen = set()
        for raw in raw_candidates:
            value = normalize_candidate(raw)
            if value not in seen:
                seen.add(value)
                candidates.append(value)

        contexts = {}
        for needle in (
            "viewer", "imageProxy", "원본", "태백산", article_id,
            "imgArr", "popup", "s_img", "image",
        ):
            ctx = compact_context(text, needle)
            if ctx:
                contexts[needle] = ctx
        (out / f"{article_id}-contexts.json").write_text(
            json.dumps(contexts, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        viewer_candidates = [
            f"{BASE}/popup/viewer.do?type=view&id={urllib.parse.quote(article_id)}",
            f"{BASE}/popup/viewer.do?id={urllib.parse.quote(article_id)}",
        ]
        for value in candidates:
            if "viewer" in value.lower() and value.startswith("http"):
                viewer_candidates.append(value)

        viewer_candidates = list(dict.fromkeys(viewer_candidates))[:12]
        viewer_results = []
        for url in viewer_candidates:
            vstatus, vctype, vbody = fetch(url)
            vtext = vbody.decode("utf-8", "replace")
            rec = {
                "url": url,
                "status": vstatus,
                "content_type": vctype,
                "bytes": len(vbody),
                "contains_imgArr": "imgArr" in vtext,
                "contains_imageProxy": "imageProxy" in vtext,
                "contains_s_img": "/s_img/" in vtext,
            }
            if vstatus == 200 and ("text/html" in vctype or "<html" in vtext[:500].lower()):
                safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", url)[-140:]
                (out / f"{article_id}-viewer-{safe}.html").write_text(vtext, encoding="utf-8")
                image_strings = sorted(set(
                    normalize_candidate(x)
                    for x in re.findall(r"""["']([^"']*(?:/s_img/|imageProxy\.do|\.jpg|\.jpeg|\.png)[^"']*)["']""", vtext, flags=re.I)
                ))
                rec["image_strings"] = image_strings[:200]
                rec["imgarr_context"] = compact_context(vtext, "imgArr", 600)
                rec["imageproxy_context"] = compact_context(vtext, "imageProxy", 600)
            viewer_results.append(rec)

        article = {
            "article_id": article_id,
            "article_url": article_url,
            **meta,
            "article_status": status,
            "article_content_type": ctype,
            "article_bytes": len(body),
            "candidate_strings": candidates[:300],
            "viewer_results": viewer_results,
            "ocr_used": False,
            "target_values_authorized": False,
        }
        result["articles"].append(article)

    (out / "route-probe.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    ok = all(x["article_status"] == 200 for x in result["articles"])
    return 0 if ok else 2

if __name__ == "__main__":
    raise SystemExit(main())
