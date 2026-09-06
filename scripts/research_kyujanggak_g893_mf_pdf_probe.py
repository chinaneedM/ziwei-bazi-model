#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

from curl_cffi import requests

BASE = "https://kyudb.snu.ac.kr"
BOOK_CD = "GK00893_00"
DETAIL = f"{BASE}/book/view.do?book_cd={BOOK_CD}&mid=GDS&target=master"
PDF_LIST = f"{BASE}/ajax/book/mfPdfList.do"
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
            time.sleep(1.0 * attempt)
    return None, {"url": url, "status": 0, "attempts": errors}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/g893-mf-pdf-probe")
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    result = {
        "schema": "KYUJANGGAK-G893-MF-PDF-PROBE-R1",
        "book_cd": BOOK_CD,
        "catalog_identifier": "奎貴893",
        "microfilm_number": "M/F73-102-37-A",
        "read_only": True,
        "ocr_used": False,
        "route_type": "DISTINCT_MF_PDF_LIST_ROUTE_NOT_RENDERER_RETRY",
        "target_values_authorized": False,
        "attempts": {},
    }

    session = requests.Session(impersonate="chrome")
    session.headers.update({"User-Agent": UA})

    detail, detail_meta = request(session, "GET", DETAIL, headers={"Referer": BASE + "/"})
    result["attempts"]["detail"] = detail_meta
    if detail is not None and detail.status_code == 200:
        (out / "detail.html").write_text(detail.text, encoding="utf-8")
        result["detail_observation"] = {
            "book_cd_present": BOOK_CD in detail.text,
            "mf_pdf_ui_marker_present": "M/F PDF" in detail.text,
            "microfilm_number_present": "M/F73-102-37-A" in detail.text,
        }

    pdf_list, pdf_meta = request(
        session,
        "POST",
        PDF_LIST,
        data={"book_cd": BOOK_CD},
        headers={
            "Referer": DETAIL,
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    result["attempts"]["mf_pdf_list"] = pdf_meta
    if pdf_list is not None:
        (out / "mfPdfList.raw").write_bytes(pdf_list.content)
        try:
            result["mf_pdf_list_json"] = pdf_list.json()
        except Exception as exc:
            result["mf_pdf_list_parse_error"] = f"{type(exc).__name__}: {exc}"
            result["mf_pdf_list_body_prefix"] = pdf_list.text[:8000]

    payload = result.get("mf_pdf_list_json")
    result["conclusion"] = {
        "mf_pdf_list_transport_success": bool(pdf_list is not None and pdf_list.status_code == 200),
        "mf_pdf_list_nonempty_json": bool(payload),
        "renderer_boundary_effect": "NONE_DISTINCT_ROUTE",
        "direct_target_page_status": "PENDING_UNLESS_PDF_OBJECT_IS_RETURNED_AND_DIRECTLY_REVIEWED",
        "target_effect": "NONE",
    }
    (out / "probe.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result["conclusion"], ensure_ascii=False))
    if payload:
        print(json.dumps(payload, ensure_ascii=False)[:12000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
