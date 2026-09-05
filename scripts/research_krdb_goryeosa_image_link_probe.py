#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import html
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

TARGET = "https://db.history.go.kr/goryeo/itemLevelKrList.do?parentId=kr_052_0010_0010_0020&types=o"
VIEWER = "https://db.history.go.kr/common/imageViewer.do?levelId=kr_052_0010_0010_0020&begin=kr_052_1034"
KNOWN_VIEWER_CAPTURE_HEAD = "8ef0565fc215a266ca3c7c1138ed592dad869a4c"
KNOWN_VIEWER_CAPTURE_ARTIFACT_ID = 9970511498
KNOWN_VIEWER_IMAGE_START = 1034
KNOWN_VIEWER_IMAGE_END = 1134
UA = "Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"
PAGE_KEYS = ("원문이미지", "ico_viewImage", "kyudb", "viewImage", "image", "kr_052", "규귀5553", "을해자")
VIEWER_KEYS = (
    "kr_052_1034", "kyudb", "snu.ac.kr", "image", "img", "viewer", "page", "begin",
    "levelId", "book_cd", "vol_no", "page_no", "GK05553", "5553", "규귀5553",
)


def fetch(url: str, attempts: int = 3, timeout: int = 30) -> tuple[str, dict[str, str]]:
    last: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,*/*;q=0.8"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = resp.read()
                ctype = resp.headers.get_content_charset() or "utf-8"
                return data.decode(ctype, errors="replace"), dict(resp.headers.items())
        except Exception as exc:
            last = exc
            if attempt < attempts:
                time.sleep(attempt * 2)
    assert last is not None
    raise last


def fetch_bytes(url: str, attempts: int = 3, timeout: int = 30) -> tuple[bytes, dict[str, str]]:
    last: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read(), dict(resp.headers.items())
        except Exception as exc:
            last = exc
            if attempt < attempts:
                time.sleep(attempt * 2)
    assert last is not None
    raise last


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
        if name.lower() in {
            "href", "onclick", "src", "data-url", "data-href", "data-link", "data-id",
            "data-page", "data-index", "id", "class", "title", "alt", "name", "value",
            "action", "method",
        }:
            found[name] = html.unescape(value)
    return found


def matching_tags(text: str, keys: tuple[str, ...]) -> list[dict[str, object]]:
    out = []
    for m in re.finditer(r"<[^>]+>", text, re.S):
        frag = m.group(0)
        if any(k.lower() in frag.lower() for k in keys):
            out.append({"fragment": frag[:6000], "attributes": attrs(frag)})
    return out


def script_probe(base_url: str, page: str, keys: tuple[str, ...], out: Path, prefix: str) -> list[dict[str, object]]:
    scripts = []
    seen = set()
    for src in re.findall(r"<script[^>]+src=['\"]([^'\"]+)['\"]", page, re.I):
        url = urllib.parse.urljoin(base_url, html.unescape(src))
        if url in seen:
            continue
        seen.add(url)
        rec: dict[str, object] = {"url": url, "status": "NOT_FETCHED", "hits": []}
        try:
            body, _ = fetch(url, attempts=2, timeout=20)
            rec["status"] = "FETCHED"
            rec["bytes"] = len(body.encode("utf-8"))
            hits = []
            for k in keys:
                for c in contexts(body, k, 800):
                    hits.append({"key": k, "context": c})
            rec["hits"] = hits
            if hits:
                safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", Path(urllib.parse.urlparse(url).path).name or "script")
                (out / f"{prefix}-script-hit-{len(scripts):02d}-{safe}.txt").write_text(body, encoding="utf-8")
        except Exception as exc:
            rec["status"] = "ERROR"
            rec["error"] = f"{type(exc).__name__}: {exc}"
        scripts.append(rec)
    return scripts


def endpoint_candidates(text: str, base_url: str) -> list[str]:
    raw = set()
    raw.update(html.unescape(x) for x in re.findall(r"https?://[^\s'\"<>]+", text))
    for x in re.findall(r"['\"]((?:/|\./|\.\./)[^'\"]*(?:image|img|viewer|page|list|json|ajax)[^'\"]*)['\"]", text, re.I):
        raw.add(urllib.parse.urljoin(base_url, html.unescape(x)))
    return sorted(raw)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/krdb-goryeosa-image-link-probe")
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    attempt = {
        "schema": "KRDB-GORYEOSA-IMAGE-LINK-PROBE-ATTEMPT-R1",
        "target": TARGET,
        "viewer": VIEWER,
        "known_holding_label": "규장각한국학연구원 소장본(규귀5553[을해자])",
        "known_level_id": "kr_052_0010_0010_0020",
        "known_begin": "kr_052_1034",
        "read_only": True,
        "ocr_used": False,
    }
    (out / "attempt.json").write_text(json.dumps(attempt, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

    # Viewer first. If the live viewer is transiently unavailable, fall back only to the
    # exact 101-image sequence archived by the successful 8ef0565f workflow artifact.
    # The fallback is provenance-labeled and is not represented as a fresh HTTP capture.
    viewer_status: dict[str, object]
    try:
        viewer, viewer_headers = fetch(VIEWER, attempts=2, timeout=20)
        (out / "image-viewer.html").write_text(viewer, encoding="utf-8")
        viewer_status = {
            "status": "FETCHED_LIVE",
            "bytes": len(viewer.encode("utf-8")),
        }
        img_paths = re.findall(r'"(kr/052/kr_052_\d+\.jpg)"', viewer)
        if not img_paths:
            raise ValueError("live viewer returned no kr_052 image array")
    except Exception as exc:
        viewer = ""
        viewer_headers = {}
        viewer_status = {
            "status": "FALLBACK_TO_PRIOR_EXACT_VIEWER_CAPTURE",
            "error": f"{type(exc).__name__}: {exc}",
            "source_head": KNOWN_VIEWER_CAPTURE_HEAD,
            "source_artifact_id": KNOWN_VIEWER_CAPTURE_ARTIFACT_ID,
            "source_image_start": KNOWN_VIEWER_IMAGE_START,
            "source_image_end": KNOWN_VIEWER_IMAGE_END,
        }
        img_paths = [
            f"kr/052/kr_052_{n}.jpg"
            for n in range(KNOWN_VIEWER_IMAGE_START, KNOWN_VIEWER_IMAGE_END + 1)
        ]

    viewer_tags = matching_tags(viewer, VIEWER_KEYS) if viewer else []
    viewer_contexts = []
    if viewer:
        for k in VIEWER_KEYS:
            for ctx in contexts(viewer, k):
                if ctx not in viewer_contexts:
                    viewer_contexts.append(ctx)
    viewer_scripts = script_probe(VIEWER, viewer, VIEWER_KEYS, out, "viewer") if viewer else []

    # Capture the exact page array as bounded, read-only thumbnail evidence.
    # These artifacts are intentionally not committed to the repository and are not OCRed.
    thumb_dir = out / "viewer-thumbs"
    thumb_dir.mkdir(parents=True, exist_ok=True)
    def capture_thumb(item: tuple[int, str]) -> dict[str, object]:
        page_no, rel_path = item
        url = "https://db.history.go.kr/common/imageProxy.do?" + urllib.parse.urlencode({
            "mode": "thumb",
            "filePath": "/" + rel_path,
        })
        rec: dict[str, object] = {"page_no": page_no, "rel_path": rel_path, "url": url, "status": "NOT_FETCHED"}
        try:
            body, img_headers = fetch_bytes(url, attempts=2, timeout=10)
            suffix = Path(rel_path).name
            (thumb_dir / suffix).write_bytes(body)
            rec.update({
                "status": "FETCHED",
                "bytes": len(body),
                "content_type": img_headers.get("Content-Type"),
            })
        except Exception as exc:
            rec.update({"status": "ERROR", "error": f"{type(exc).__name__}: {exc}"})
        return rec

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        thumb_capture = list(pool.map(capture_thumb, enumerate(img_paths, start=1)))
    (out / "viewer-page-map.json").write_text(json.dumps({
        "schema": "KRDB-GORYEOSA-VIEWER-PAGE-MAP-R1",
        "viewer": VIEWER,
        "ocr_used": False,
        "page_count": len(img_paths),
        "pages": thumb_capture,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    forms = []
    for m in re.finditer(r"<form\b.*?</form>", viewer, re.I | re.S):
        frag = m.group(0)
        fields = []
        for tag in re.findall(r"<(?:input|select|option|textarea)\b[^>]*>", frag, re.I | re.S):
            a = attrs(tag)
            if a:
                fields.append(a)
        forms.append({"form": attrs(frag.split(">", 1)[0] + ">"), "fields": fields})

    js_bodies = "\n".join(str(h.get("context", "")) for s in viewer_scripts for h in (s.get("hits") or []))
    endpoint_urls = endpoint_candidates(viewer + "\n" + js_bodies, VIEWER)
    relevant_endpoints = [u for u in endpoint_urls if any(k.lower() in u.lower() for k in ("image", "img", "viewer", "page", "kyudb", "goryeo"))]

    # Re-fetch the source article only as best-effort corroboration; its prior exact DOM is already archived.
    target_status: dict[str, object] = {"status": "SKIPPED_AFTER_PRIOR_R1_CAPTURE"}
    page_tags: list[dict[str, object]] = []
    page_contexts: list[str] = []
    page_scripts: list[dict[str, object]] = []
    try:
        page, headers = fetch(TARGET, attempts=1, timeout=15)
        (out / "target-page.html").write_text(page, encoding="utf-8")
        page_tags = matching_tags(page, PAGE_KEYS)
        for k in PAGE_KEYS:
            for c in contexts(page, k):
                if c not in page_contexts:
                    page_contexts.append(c)
        page_scripts = script_probe(TARGET, page, PAGE_KEYS, out, "target")
        target_status = {"status": "FETCHED", "bytes": len(page.encode("utf-8")), "headers": headers}
    except Exception as exc:
        target_status = {"status": "BEST_EFFORT_ERROR_PRIOR_R1_CAPTURE_REMAINS_VALID", "error": f"{type(exc).__name__}: {exc}"}

    manifest = {
        "schema": "KRDB-GORYEOSA-IMAGE-LINK-PROBE-R4",
        "target": TARGET,
        "viewer": VIEWER,
        "read_only": True,
        "ocr_used": False,
        "target_status": target_status,
        "viewer_status": viewer_status,
        "viewer_page_bytes": len(viewer.encode("utf-8")),
        "viewer_headers": viewer_headers,
        "target_matching_tags": page_tags,
        "target_inline_contexts": page_contexts,
        "target_scripts": page_scripts,
        "viewer_matching_tags": viewer_tags,
        "viewer_inline_contexts": viewer_contexts,
        "viewer_forms": forms,
        "viewer_scripts": viewer_scripts,
        "viewer_page_count": len(img_paths),
        "viewer_thumbnail_capture": thumb_capture,
        "viewer_endpoint_candidates": relevant_endpoints,
        "known_link_contract": {
            "holding_label": "규장각한국학연구원 소장본(규귀5553[을해자])",
            "level_id": "kr_052_0010_0010_0020",
            "begin": "kr_052_1034",
            "viewer_path": "/common/imageViewer.do",
            "kyujanggak_catalog_candidate": "GK05553_00",
            "catalog_candidate_status": "KYUJANGGAK_CATALOG_MATCHES_TITLE_CALL_NUMBER_EDITION; VIEWER_PAGE_MAPPING_STILL_TO_BE_EXTRACTED",
        },
        "evidence_scope": "FRONTEND_AND_VIEWER_LINK_CONTRACT_ONLY_NOT_GLYPH_EVIDENCE",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({
        "viewer": VIEWER,
        "viewer_status": viewer_status,
        "target_status": target_status,
        "viewer_page_count": len(img_paths),
        "viewer_thumbnail_fetch_success_count": sum(1 for x in thumb_capture if x["status"] == "FETCHED"),
        "viewer_matching_tag_count": len(viewer_tags),
        "viewer_form_count": len(forms),
        "viewer_scripts_with_hits": [x["url"] for x in viewer_scripts if x.get("hits")],
        "viewer_endpoint_candidates": relevant_endpoints[:100],
        "viewer_matching_tags": viewer_tags[:50],
        "viewer_forms": forms[:20],
    }, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
