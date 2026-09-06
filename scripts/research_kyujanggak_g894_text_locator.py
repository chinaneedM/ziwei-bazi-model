#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import time
from pathlib import Path

from curl_cffi import requests

BASE = "https://kyudb.snu.ac.kr"
BOOK_CD = "GK00894_00"
ITEM_CD = "GJB"
VOLUMES = ("0001", "0002", "0003")
RENDERER = BASE + "/pf01/rendererImg.do"
PAGE_TEXT = BASE + "/pf01/pageText.do"
UA = "Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"
TARGET_TERMS = (
    "太陽冬至前後二象盈初縮末限",
    "太陰限數遲疾度",
    "遲疾度",
    "遲疾日率",
    "損益分",
)


def req(session, method, url, **kwargs):
    errors = []
    for attempt in range(1, 4):
        try:
            r = session.request(method, url, timeout=20, **kwargs)
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
            time.sleep(0.6 * attempt)
    return None, {"url": url, "status": 0, "attempts": errors}


def clean_fragment(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.I)
    value = re.sub(r"<[^>]+>", "", value)
    return re.sub(r"\s+", "", value)


def parse_renderer(text: str) -> list[str]:
    pages = []
    for m in re.finditer(r'''fn_goPageJumpWithMokIdxClear\(["']([A-Za-z0-9]+)["']\)''', text):
        p = m.group(1)
        if p not in pages and not p.startswith("999"):
            pages.append(p)
    return pages


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/g894-text-locator")
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    result = {
        "schema": "KYUJANGGAK-G894-PROVIDER-TEXT-LOCATOR-R1",
        "book_cd": BOOK_CD,
        "item_cd": ITEM_CD,
        "provider_text_role": "NAVIGATION_AND_PAGE_LOCALIZATION_ONLY_NOT_DIRECT_GLYPH_AUTHORITY",
        "ocr_used_by_project": False,
        "provider_text_as_facsimile_glyph": "FORBIDDEN",
        "target_value_authorized_from_provider_text": False,
        "volumes": [],
        "hits": [],
    }

    session = requests.Session(impersonate="chrome")
    session.headers.update({"User-Agent": UA})

    for vol_no in VOLUMES:
        rr, rmeta = req(
            session,
            "POST",
            RENDERER,
            data={"item_cd": ITEM_CD, "book_cd": BOOK_CD, "vol_no": vol_no, "page_no": "", "tool": "1"},
            headers={"Referer": BASE + f"/book/view.do?book_cd={BOOK_CD}", "Content-Type": "application/x-www-form-urlencoded"},
        )
        vol = {"vol_no": vol_no, "renderer": rmeta, "pages": []}
        if rr is None or rr.status_code != 200:
            result["volumes"].append(vol)
            continue
        page_ids = parse_renderer(rr.text)
        vol["page_count"] = len(page_ids)
        for page_no in page_ids:
            tr, tmeta = req(
                session,
                "POST",
                PAGE_TEXT,
                data={"item_cd": ITEM_CD, "book_cd": BOOK_CD, "vol_no": vol_no, "page_no": page_no},
                headers={"Referer": RENDERER, "Content-Type": "application/x-www-form-urlencoded"},
            )
            rec = {"page_no": page_no, "transport": tmeta, "terms": []}
            if tr is not None and tr.status_code == 200:
                try:
                    payload = tr.json()
                    raw = ((payload.get("ORG") or {}).get("list") or "")
                    compact = clean_fragment(raw)
                    rec["provider_text_chars"] = len(compact)
                    rec["provider_text_sha256"] = hashlib.sha256(compact.encode("utf-8")).hexdigest()
                    terms = [term for term in TARGET_TERMS if term in compact]
                    rec["terms"] = terms
                    if terms:
                        snippet = compact[:1200]
                        hit = {"vol_no": vol_no, "page_no": page_no, "terms": terms, "provider_text_snippet": snippet}
                        result["hits"].append(hit)
                        (out / f"hit-{vol_no}-{page_no}.txt").write_text(compact + "\n", encoding="utf-8")
                except Exception as exc:
                    rec["parse_error"] = f"{type(exc).__name__}: {exc}"
                    rec["body_prefix"] = tr.text[:500]
            vol["pages"].append(rec)
        result["volumes"].append(vol)

    result["conclusion"] = {
        "pages_queried": sum(len(v.get("pages", ())) for v in result["volumes"]),
        "target_family_hit_count": len(result["hits"]),
        "exact_target_folios": "REQUIRE_DIRECT_IMAGE_CONFIRMATION_AFTER_TEXT_LOCALIZATION",
        "algorithm_or_runtime_effect": "NONE",
    }
    (out / "g894-text-locator.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["conclusion"], ensure_ascii=False, indent=2))
    print(json.dumps(result["hits"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
