#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

TARGET = "https://db.history.go.kr/goryeo/itemLevelKrList.do?parentId=kr_052_0010_0010_0020&types=o"
UA = "Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"
KEYS = ("원문이미지", "ico_viewImage", "kyudb", "viewImage", "image", "kr_052")


def fetch(url: str) -> tuple[str, dict[str, str]]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as resp:
        data = resp.read()
        ctype = resp.headers.get_content_charset() or "utf-8"
        return data.decode(ctype, errors="replace"), dict(resp.headers.items())


def contexts(text: str, needle: str, radius: int = 900) -> list[str]:
    out = []
    lower = text.lower()
    start = 0
    n = needle.lower()
    while True:
        i = lower.find(n, start)
        if i < 0:
            break
        out.append(text[max(0, i-radius):i+len(needle)+radius])
        start = i + len(needle)
    return out


def attrs(fragment: str) -> dict[str, str]:
    found = {}
    for name, quote, value in re.findall(r"([:\w-]+)\s*=\s*(['\"])(.*?)\2", fragment, re.S):
        if name.lower() in {"href","onclick","src","data-url","data-href","data-link","data-id","id","class","title","alt"}:
            found[name] = html.unescape(value)
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/krdb-goryeosa-image-link-probe")
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    page, headers = fetch(TARGET)
    (out / "target-page.html").write_text(page, encoding="utf-8")

    tags = []
    for m in re.finditer(r"<[^>]+>", page, re.S):
        frag = m.group(0)
        if any(k.lower() in frag.lower() for k in KEYS):
            tags.append({"fragment": frag[:5000], "attributes": attrs(frag)})

    inline_contexts = []
    for k in KEYS:
        for c in contexts(page, k):
            if c not in inline_contexts:
                inline_contexts.append(c)

    scripts = []
    for src in re.findall(r"<script[^>]+src=['\"]([^'\"]+)['\"]", page, re.I):
        url = urllib.parse.urljoin(TARGET, html.unescape(src))
        rec = {"url": url, "status": "NOT_FETCHED", "hits": []}
        try:
            body, _ = fetch(url)
            rec["status"] = "FETCHED"
            rec["bytes"] = len(body.encode("utf-8"))
            for k in KEYS:
                for c in contexts(body, k, 700):
                    rec["hits"].append({"key": k, "context": c})
            if rec["hits"]:
                safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", Path(urllib.parse.urlparse(url).path).name or "script")
                (out / f"script-hit-{len(scripts):02d}-{safe}.txt").write_text(body, encoding="utf-8")
        except Exception as exc:
            rec["status"] = "ERROR"
            rec["error"] = f"{type(exc).__name__}: {exc}"
        scripts.append(rec)

    absolute_urls = sorted(set(html.unescape(x) for x in re.findall(r"https?://[^\s'\"<>]+", page)))
    candidate_urls = [u for u in absolute_urls if any(k.lower() in u.lower() for k in ("kyudb","image","goryeo","kr_052"))]

    manifest = {
        "schema": "KRDB-GORYEOSA-IMAGE-LINK-PROBE-R1",
        "target": TARGET,
        "read_only": True,
        "ocr_used": False,
        "page_bytes": len(page.encode("utf-8")),
        "response_headers": headers,
        "matching_tags": tags,
        "inline_contexts": inline_contexts,
        "candidate_absolute_urls": candidate_urls,
        "scripts": scripts,
        "evidence_scope": "FRONTEND_LINK_CONTRACT_ONLY_NOT_GLYPH_EVIDENCE",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({
        "target": TARGET,
        "matching_tag_count": len(tags),
        "candidate_url_count": len(candidate_urls),
        "scripts_with_hits": [x["url"] for x in scripts if x["hits"]],
        "matching_tags": tags[:20],
        "candidate_urls": candidate_urls[:50],
    }, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
