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
LIST_URL = f"{BASE}/book/list.do?book_cate=CUL05&mid=GDS"
BOOK_CD = "GK00894_00"
CALL_NUMBER = "奎貴894-v.1-3"
TITLE = "七政算內篇"
DETAIL_CANDIDATES = [
    f"{BASE}/book/view.do?book_cd={BOOK_CD}&mid=GDS&target=master",
    f"{BASE}/book/view.do?book_cd={BOOK_CD}",
]
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
            response = session.request(method, url, timeout=25, **kwargs)
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


def context(text, needle, radius=1600):
    index = text.find(needle)
    if index < 0:
        return ""
    return text[max(0, index-radius):min(len(text), index+len(needle)+radius)]


def extract_urls(text):
    urls = []
    for raw in re.findall(r'''(?:src|href)\s*=\s*["']([^"']+)["']''', text, flags=re.I):
        value = raw.replace("&amp;", "&")
        if value.startswith("/"):
            value = urljoin(BASE, value)
        if value.startswith("http") and value not in urls:
            urls.append(value)
    return urls


def parse_renderer(text):
    result = {}
    match = re.search(r'''first_page_no\s*=\s*["']([A-Za-z0-9]+)["']''', text)
    if match:
        result["first_page_no"] = match.group(1)
    match = re.search(r'''imgFileNm\s*=\s*["']([^"']+)["']''', text)
    if match:
        result["imgFileNm"] = match.group(1)
    pages = []
    for match in re.finditer(
        r'''fn_goPageJumpWithMokIdxClear\(["']([A-Za-z0-9]+)["']\)''',
        text,
    ):
        page = match.group(1)
        if page not in pages:
            pages.append(page)
    result["page_ids"] = pages
    volumes = []
    for match in re.finditer(
        r'''<option\s+value=["']([A-Za-z0-9]+)["']''',
        text,
        flags=re.I,
    ):
        volume = match.group(1)
        if volume not in volumes:
            volumes.append(volume)
    result["volume_ids"] = volumes
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="artifacts/g894-access")
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    result = {
        "schema": "KYUJANGGAK-G894-DIGITAL-OBJECT-ACCESS-PROBE-R1",
        "book_cd": BOOK_CD,
        "catalog_identifier": CALL_NUMBER,
        "title": TITLE,
        "provider_identity_expected_from_prior_direct_catalog": {
            "edition": "甲寅字",
            "publication_year": 1444,
            "authors": "李純之、金淡受命編",
        },
        "read_only": True,
        "ocr_used": False,
        "target_values_authorized": False,
        "filename_pattern_as_folio_binding": "FORBIDDEN",
        "network_failure_as_source_evidence": "FORBIDDEN",
        "attempts": {},
    }

    session = requests.Session(impersonate="chrome")
    session.headers.update({"User-Agent": UA})

    response, meta = request(
        session,
        "GET",
        LIST_URL,
        headers={"Referer": BASE + "/"},
    )
    result["attempts"]["official_list"] = meta
    observed_item_cd = None
    if response is not None and response.status_code == 200:
        text = response.text
        (out / "official-list.html").write_text(text, encoding="utf-8")
        item_context = context(text, CALL_NUMBER)
        (out / "g894-list-context.html").write_text(item_context, encoding="utf-8")
        observation = {
            "call_number_present": CALL_NUMBER in text,
            "title_present": TITLE in item_context,
            "book_cd_present": BOOK_CD in item_context,
            "context_urls": extract_urls(item_context),
        }
        patterns = [
            r"item_cd=([A-Za-z0-9_-]+)",
            r"/thumb/([A-Za-z0-9_-]+)/" + re.escape(BOOK_CD),
        ]
        for pattern in patterns:
            match = re.search(pattern, item_context)
            if match:
                observed_item_cd = match.group(1)
                break
        observation["observed_item_cd"] = observed_item_cd
        result["official_list_observation"] = observation

    detail_results = []
    for index, url in enumerate(DETAIL_CANDIDATES):
        response, meta = request(
            session,
            "GET",
            url,
            headers={"Referer": LIST_URL},
        )
        record = {
            "candidate_url": url,
            "transport": meta,
            "candidate_only_before_success": True,
        }
        if response is not None and response.status_code == 200:
            text = response.text
            (out / f"detail-{index}.html").write_text(text, encoding="utf-8")
            record["book_cd_present"] = BOOK_CD in text
            record["call_number_present"] = CALL_NUMBER in text
            record["title_present"] = TITLE in text
            record["urls"] = extract_urls(text)[:300]
            if record["book_cd_present"] or record["call_number_present"]:
                record["route_status"] = "DIRECT_OFFICIAL_DETAIL_RESPONSE_BOUND"
                for pattern in (
                    r"item_cd=([A-Za-z0-9_-]+)",
                    r'''name=["']item_cd["'][^>]*value=["']([A-Za-z0-9_-]+)["']''',
                ):
                    match = re.search(pattern, text, flags=re.I)
                    if match:
                        record["observed_item_cd"] = match.group(1)
                        observed_item_cd = observed_item_cd or match.group(1)
                        break
            else:
                record["route_status"] = "HTTP_200_BUT_OBJECT_IDENTITY_NOT_BOUND"
        detail_results.append(record)
    result["attempts"]["detail_routes"] = detail_results
    result["observed_item_cd"] = observed_item_cd

    response, meta = request(
        session,
        "POST",
        BASE + "/ajax/book/mfPdfList.do",
        data={"book_cd": BOOK_CD},
        headers={
            "Referer": DETAIL_CANDIDATES[0],
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    pdf_record = {"transport": meta}
    if response is not None and response.status_code == 200:
        try:
            pdf_record["json"] = response.json()
        except Exception as exc:
            pdf_record["parse_error"] = f"{type(exc).__name__}: {exc}"
            pdf_record["body_prefix"] = response.text[:1200]
    result["attempts"]["mf_pdf_list"] = pdf_record

    renderer = BASE + "/pf01/rendererImg.do"
    if observed_item_cd:
        response, meta = request(
            session,
            "POST",
            renderer,
            data={
                "item_cd": observed_item_cd,
                "book_cd": BOOK_CD,
                "vol_no": "",
                "page_no": "",
                "imgFileNm": "",
                "tbl_conts_seq": "",
                "mokNm": "",
                "add_page_no": "",
            },
            headers={
                "Referer": DETAIL_CANDIDATES[0],
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        renderer_record = {"transport": meta}
        if response is not None and response.status_code == 200:
            text = response.text
            (out / "renderer-index.html").write_text(text, encoding="utf-8")
            parsed = parse_renderer(text)
            renderer_record["parsed"] = parsed
            volumes = []
            for volume in parsed.get("volume_ids", [])[:3]:
                vol_response, vol_meta = request(
                    session,
                    "POST",
                    renderer,
                    data={
                        "item_cd": observed_item_cd,
                        "book_cd": BOOK_CD,
                        "vol_no": volume,
                        "page_no": "",
                        "tool": "1",
                    },
                    headers={
                        "Referer": renderer,
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                )
                vol_record = {"vol_no": volume, "transport": vol_meta}
                if vol_response is not None and vol_response.status_code == 200:
                    vol_text = vol_response.text
                    (out / f"renderer-{volume}.html").write_text(
                        vol_text,
                        encoding="utf-8",
                    )
                    vol_record["parsed"] = parse_renderer(vol_text)
                volumes.append(vol_record)
            renderer_record["volumes"] = volumes
        result["attempts"]["renderer"] = renderer_record
    else:
        result["attempts"]["renderer"] = {
            "status": "NOT_ATTEMPTED_ITEM_CD_NOT_DIRECTLY_OBSERVED"
        }

    result["conclusion"] = {
        "provider_object_identity": "PREVIOUSLY_DIRECTLY_CATALOG_BOUND",
        "digital_object_route_upgrade": "EVIDENCE_DEPENDS_ON_SUCCESSFUL_RESPONSES_RECORDED_ABOVE",
        "exact_target_folios": "PENDING",
        "target_glyphs": "PENDING",
        "algorithm_or_runtime_effect": "NONE",
    }
    (out / "g894-access-probe.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
