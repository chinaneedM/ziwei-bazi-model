#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin

from curl_cffi import requests

BASE = "https://kyudb.snu.ac.kr"
LIST_URL = f"{BASE}/book/list.do?book_cate=COB02&mid=GDS"
CALL_NUMBER = "奎26775-v.1-7"
TITLE = "奎章閣圖書番號順目錄"
COMPILER = "京城帝國大學附屬圖書館"
UA = "Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"


def response_meta(response):
    body = response.content
    return {
        "url": response.url,
        "status": response.status_code,
        "content_type": response.headers.get("content-type", ""),
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
    }


def request(session, method, url, **kwargs):
    errors = []
    for attempt in range(1, 4):
        try:
            response = session.request(method, url, timeout=30, **kwargs)
            meta = response_meta(response)
            meta["attempt"] = attempt
            return response, meta
        except Exception as exc:
            errors.append({
                "attempt": attempt,
                "error_type": type(exc).__name__,
                "error": str(exc),
            })
            time.sleep(1.2 * attempt)
    return None, {"url": url, "status": 0, "attempts": errors}


def context(text: str, needle: str, radius: int = 5000) -> str:
    index = text.find(needle)
    if index < 0:
        return ""
    return text[max(0, index-radius):min(len(text), index+len(needle)+radius)]


def extract_urls(text: str) -> list[str]:
    urls = []
    for raw in re.findall(r'''(?:src|href)\s*=\s*["']([^"']+)["']''', text, flags=re.I):
        value = raw.replace("&amp;", "&")
        if value.startswith("/"):
            value = urljoin(BASE, value)
        if value.startswith("http") and value not in urls:
            urls.append(value)
    return urls


def observed_identifiers(text: str) -> dict[str, object]:
    book_cds = []
    for pattern in (
        r"book_cd=([A-Za-z0-9_-]+)",
        r"/(?:thumb|ThumbServlet\.do[^\s\"']*)/[^/]*?(GK[0-9A-Za-z_-]+)",
        r"/thumb/[A-Za-z0-9_-]+/(GK[0-9A-Za-z_-]+)",
        r"(GK[0-9]{5,}_[0-9]{2})",
    ):
        for match in re.finditer(pattern, text, flags=re.I):
            value = match.group(1)
            if value not in book_cds:
                book_cds.append(value)

    item_cds = []
    for pattern in (
        r"item_cd=([A-Za-z0-9_-]+)",
        r"/thumb/([A-Za-z0-9_-]+)/GK[0-9A-Za-z_-]+",
    ):
        for match in re.finditer(pattern, text, flags=re.I):
            value = match.group(1)
            if value not in item_cds:
                item_cds.append(value)

    return {"book_cds": book_cds, "item_cds": item_cds}


def parse_renderer(text: str) -> dict[str, object]:
    result: dict[str, object] = {}
    m = re.search(r'''first_page_no\s*=\s*["']([A-Za-z0-9]+)["']''', text)
    if m:
        result["first_page_no"] = m.group(1)
    m = re.search(r'''imgFileNm\s*=\s*["']([^\"']+)["']''', text)
    if m:
        result["imgFileNm"] = m.group(1)

    volumes = []
    for m in re.finditer(r'''<option\s+value=["']([A-Za-z0-9]+)["']''', text, flags=re.I):
        value = m.group(1)
        if value not in volumes:
            volumes.append(value)
    result["volume_ids"] = volumes

    pages = []
    for m in re.finditer(r'''fn_goPageJumpWithMokIdxClear\(["']([A-Za-z0-9]+)["']\)''', text):
        value = m.group(1)
        if value not in pages:
            pages.append(value)
    result["page_ids"] = pages
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/kyujanggak-1930-catalog-locator")
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    result: dict[str, object] = {
        "schema": "KYUJANGGAK-1930-NUMERIC-ORDER-CATALOG-LOCATOR-PROBE-R1",
        "catalog_call_number": CALL_NUMBER,
        "catalog_title": TITLE,
        "catalog_compiler": COMPILER,
        "read_only": True,
        "ocr_used": False,
        "guessed_book_cd_authorized": False,
        "guessed_item_cd_authorized": False,
        "g893_item_identity_authorized": False,
        "target_values_authorized": False,
        "attempts": {},
    }

    s = requests.Session(impersonate="chrome")
    s.headers.update({"User-Agent": UA})

    response, meta = request(s, "GET", LIST_URL, headers={"Referer": BASE + "/"})
    result["attempts"]["official_catalog_list"] = meta
    if response is None or response.status_code != 200:
        result["conclusion"] = {
            "catalog_object_id_status": "UNRESOLVED_LIST_NOT_RETURNED",
            "g893_internal_entry_status": "NOT_ATTEMPTED",
            "target_effect": "NONE",
        }
        (out / "locator.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    text = response.text
    (out / "official-list.html").write_text(text, encoding="utf-8")
    ctx = context(text, CALL_NUMBER)
    (out / "catalog-list-context.html").write_text(ctx, encoding="utf-8")

    ids = observed_identifiers(ctx)
    result["list_observation"] = {
        "call_number_present": CALL_NUMBER in ctx,
        "title_present": TITLE in ctx,
        "compiler_present": COMPILER in ctx,
        "observed_identifiers": ids,
        "context_urls": extract_urls(ctx)[:300],
    }

    # Fail closed unless the official page itself returns exactly one book_cd in
    # the target context. No call-number -> book_cd naming inference is allowed.
    book_cds = ids["book_cds"]
    if len(book_cds) != 1:
        result["conclusion"] = {
            "catalog_object_id_status": "UNRESOLVED_OFFICIAL_CONTEXT_DID_NOT_RETURN_ONE_UNIQUE_BOOK_CD",
            "observed_book_cds": book_cds,
            "g893_internal_entry_status": "NOT_ATTEMPTED",
            "target_effect": "NONE",
        }
        (out / "locator.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    book_cd = book_cds[0]
    result["observed_book_cd"] = book_cd

    detail_url = f"{BASE}/book/view.do?book_cd={book_cd}&mid=GDS&target=master"
    response, meta = request(s, "GET", detail_url, headers={"Referer": LIST_URL})
    result["attempts"]["detail"] = meta
    observed_item_cd = None
    if response is not None and response.status_code == 200:
        detail = response.text
        (out / "detail.html").write_text(detail, encoding="utf-8")
        detail_ids = observed_identifiers(detail)
        result["detail_observation"] = {
            "call_number_present": CALL_NUMBER in detail,
            "title_present": TITLE in detail,
            "compiler_present": COMPILER in detail,
            "observed_identifiers": detail_ids,
            "urls": extract_urls(detail)[:400],
        }
        item_cds = detail_ids["item_cds"]
        if len(item_cds) == 1:
            observed_item_cd = item_cds[0]
            result["observed_item_cd"] = observed_item_cd

    if not observed_item_cd:
        item_cds = ids["item_cds"]
        if len(item_cds) == 1:
            observed_item_cd = item_cds[0]
            result["observed_item_cd"] = observed_item_cd

    if observed_item_cd:
        renderer = f"{BASE}/pf01/rendererImg.do"
        response, meta = request(
            s,
            "POST",
            renderer,
            data={
                "item_cd": observed_item_cd,
                "book_cd": book_cd,
                "vol_no": "",
                "page_no": "",
                "imgFileNm": "",
                "tbl_conts_seq": "",
                "mokNm": "",
                "add_page_no": "",
            },
            headers={
                "Referer": detail_url,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        result["attempts"]["renderer_index"] = meta
        if response is not None and response.status_code == 200:
            renderer_text = response.text
            (out / "renderer-index.html").write_text(renderer_text, encoding="utf-8")
            parsed = parse_renderer(renderer_text)
            result["renderer_observation"] = parsed
            volume_records = []
            for vol in parsed.get("volume_ids", [])[:10]:
                vr, vm = request(
                    s,
                    "POST",
                    renderer,
                    data={
                        "item_cd": observed_item_cd,
                        "book_cd": book_cd,
                        "vol_no": vol,
                        "page_no": "",
                        "tool": "1",
                    },
                    headers={
                        "Referer": renderer,
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                )
                rec = {"vol_no": vol, "transport": vm}
                if vr is not None and vr.status_code == 200:
                    vt = vr.text
                    (out / f"renderer-{vol}.html").write_text(vt, encoding="utf-8")
                    rec["parsed"] = parse_renderer(vt)
                volume_records.append(rec)
            result["volume_records"] = volume_records

    result["conclusion"] = {
        "catalog_object_id_status": "OFFICIAL_PAGE_RETURNED_UNIQUE_BOOK_CD",
        "observed_book_cd": book_cd,
        "item_cd_status": "OBSERVED" if observed_item_cd else "UNRESOLVED",
        "g893_internal_entry_status": "PENDING_DIRECT_CATALOG_PAGE_READING",
        "g893_identity_effect": "NONE_UNTIL_INTERNAL_ENTRY_OR_COPY_SPECIFIC_IDENTIFIER_IS_DIRECTLY_BOUND",
        "target_effect": "NONE",
    }
    (out / "locator.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2)+"\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
