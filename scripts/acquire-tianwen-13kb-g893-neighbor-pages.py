#!/usr/bin/env python3
"""Acquire source-issued G893 pages bordering three existing three-row windows.

This is only an intake instrument. No historic glyph, unit, table-row identity,
or stemmatic attribution is inferred from a generated locator or smooth series.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BOOK = "GK00893_00"
BASE = "https://kyudb.snu.ac.kr"
RENDERER = BASE + "/pf01/rendererImg.do"
DIR = "/data01/stream/SIC/IMG/GK00893_00/GK00893_00_0001/"
TARGETS = ("020a", "035a", "036a", "037a")
PREEXISTING = ("018b", "019b", "035b", "036b")
MAX_HTTP = 3_000_000
MAX_HTML = 1_000_000


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(newurl, code, "redirect refused", headers, fp)


def source_issued_image_url(page: str, html: str) -> str:
    """Only exact target path emitted by official page renderer is admissible."""
    if page not in TARGETS:
        raise ValueError("unregistered neighbor page")
    values = re.findall(r'''(?:var\s+)?imgFileNm\s*=\s*["']([^"']+)["']''', html)
    expected = DIR + f"{BOOK}IH_0001_{page}.jpg"
    if expected not in values:
        raise ValueError("renderer did not emit exact full image path")
    return BASE + "/ImageServlet.do?" + urllib.parse.urlencode({
        "imgFileNm": expected.rsplit("/", 1)[-1], "path": expected
    })


def validate_url(page: str, url: str) -> None:
    p = urllib.parse.urlsplit(url)
    q = urllib.parse.parse_qs(p.query, strict_parsing=True)
    fn = f"{BOOK}IH_0001_{page}.jpg"
    if (p.scheme, p.netloc, p.path, p.fragment) != ("https", "kyudb.snu.ac.kr", "/ImageServlet.do", ""):
        raise ValueError("unexpected source host/path")
    if q != {"imgFileNm": [fn], "path": [DIR + fn]}:
        raise ValueError("unexpected source-issued image locator")


def read_limited(opener, request, cap: int) -> tuple[bytes, str]:
    with opener.open(request, timeout=24) as resp:
        if resp.status != 200:
            raise ValueError("source did not return HTTP 200")
        raw = resp.read(cap + 1)
        if not raw or len(raw) > cap:
            raise ValueError("source payload is empty or oversized")
        return raw, resp.headers.get("Content-Type", "")


def inspect_image(raw: bytes) -> dict:
    from PIL import Image
    if not raw.startswith(b"\xff\xd8\xff"):
        raise ValueError("not a JPEG source image")
    with Image.open(io.BytesIO(raw)) as im:
        im.load()
        if im.format != "JPEG" or im.size != (1150, 2000):
            raise ValueError("source image is not expected native size")
        rgb = im.convert("RGB")
        return {"size_px": [1150, 2000], "rgb_sha256": hashlib.sha256(rgb.tobytes()).hexdigest()}


def request_renderer(page: str, opener) -> tuple[str, dict]:
    payload = urllib.parse.urlencode({
        "item_cd": "SIC", "book_cd": BOOK, "vol_no": "0001",
        "page_no": page, "tool": "1"
    }).encode()
    req = urllib.request.Request(RENDERER, data=payload, headers={
        "User-Agent": "Mozilla/5.0 Tianwen-13KB-Source-Issued/1.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": f"{BASE}/book/view.do?book_cd={BOOK}"
    }, method="POST")
    raw, ctype = read_limited(opener, req, MAX_HTML)
    html = raw.decode("utf-8", "replace")
    url = source_issued_image_url(page, html)
    validate_url(page, url)
    return url, {"renderer_html_sha256": hashlib.sha256(raw).hexdigest(),
                 "renderer_html_bytes": len(raw), "renderer_content_type": ctype,
                 "source_emitted_exact_image_path": True}


def main() -> None:
    output = Path(os.environ.get("TIANWEN_13KB_OUT", "/tmp/tianwen-13kb"))
    output.mkdir(parents=True, exist_ok=True)
    opener = urllib.request.build_opener(NoRedirect())
    report = {"schema": "TIANWEN-13KB-G893-NEIGHBOR-SOURCE-ISSUED-INTAKE-R1",
              "book_code": BOOK, "requested_pages": list(TARGETS),
              "source_historic_copy_count_delta": 0,
              "glyphs_visually_collated": False, "five_row_same_copy_completed": False,
              "cross_witness_winners": 0, "new_historical_units_adjudicated": 0,
              "claimed_numeric_rows": [], "pages": []}
    for page in TARGETS:
        rec = {"page": page, "status": "SOURCE_ISSUED_LOCATOR_NOT_CONFIRMED", "attempts": []}
        for attempt in range(1, 3):
            try:
                url, renderer = request_renderer(page, opener)
                rec.update(renderer)
                rec["source_issued_original_url"] = url
                req = urllib.request.Request(url, headers={
                    "User-Agent": "Mozilla/5.0 Tianwen-13KB-Source-Issued/1.0",
                    "Accept": "image/jpeg", "Referer": RENDERER})
                raw, ctype = read_limited(opener, req, MAX_HTTP)
                dig = hashlib.sha256(raw).hexdigest()
                rec.update(inspect_image(raw))
                rec.update({"status": "NEW_ADJACENT_JPEG_ACQUIRED_UNCOLLATED",
                            "bytes": len(raw), "sha256": dig, "content_type": ctype,
                            "file": f"{page}.jpg"})
                (output / f"{page}.jpg").write_bytes(raw)
                rec["attempts"].append({"attempt": attempt, "http": 200})
                break
            except Exception as exc:
                code = getattr(exc, "code", None)
                rec["attempts"].append({"attempt": attempt,
                                        "error": type(exc).__name__,
                                        "http": code, "detail": str(exc)[:180]})
        report["pages"].append(rec)
    (output / "intake.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"acquired": sum(x["status"] == "NEW_ADJACENT_JPEG_ACQUIRED_UNCOLLATED" for x in report["pages"]),
                      "requested": len(TARGETS), "glyphs_collated": False, "historical_winners": 0}))


if __name__ == "__main__":
    main()
