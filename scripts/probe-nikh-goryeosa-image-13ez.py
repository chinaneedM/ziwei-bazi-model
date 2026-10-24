#!/usr/bin/env python3
"""13EZ bounded public NIKH image-link probe; no fabricated viewer API or glyph vote."""
from __future__ import annotations
import hashlib
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(os.environ.get("TIANWEN_13EZ_OUT", "nikh-goryeosa-13ez-evidence"))
ARTICLE = "https://db.history.go.kr/id/kr_052_0010_0010_0020_0020"
NOTICE_INDEX = "https://db.history.go.kr/goryeo/notice/noticeList.do"
HELP = "https://db.history.go.kr/main/help.do"
NOTICE_TITLE = "고려사 원문이미지 LINK 변경 안내"
LIMIT = 1_250_000
TIMEOUT = 18

class PageAnchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.anchors = []
        self.image_widgets = []
        self.script_sources = []
    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "script" and attrs.get("src"):
            self.script_sources.append(attrs["src"])
        if tag == "a":
            self.stack.append({"href": attrs.get("href", ""), "text": []})
        signal = " ".join(str(v or "") for k, v in attributes if k in ("title", "alt", "aria-label", "onclick", "data-original", "data-src"))
        if "원문이미지" in signal or "원문 이미지" in signal:
            keep = {k: str(v or "")[:400] for k, v in attributes if k in ("href", "src", "title", "alt", "aria-label", "onclick", "data-original", "data-src")}
            self.image_widgets.append({"tag": tag, "attributes": keep})
    def handle_data(self, data):
        for x in self.stack:
            x["text"].append(data)
    def handle_endtag(self, tag):
        if tag == "a" and self.stack:
            x = self.stack.pop()
            x["text"] = re.sub(r"\s+", " ", "".join(x["text"])).strip()
            self.anchors.append(x)

def official_notice_links(markup):
    parser = PageAnchors()
    parser.feed(markup)
    urls = []
    for entry in parser.anchors:
        if entry["text"] != NOTICE_TITLE:
            continue
        href = entry["href"].strip()
        if not href or href.startswith(("javascript:", "#")):
            continue
        url = urllib.parse.urljoin(NOTICE_INDEX, href)
        u = urllib.parse.urlsplit(url)
        if u.scheme == "https" and u.hostname == "db.history.go.kr" and u.path.endswith("/notice/noticeView.do") and not u.username and not u.password:
            urls.append(url)
    return sorted(set(urls))

def firstparty_script_urls(script_sources, root=ARTICLE):
    allowed = []
    for raw in script_sources:
        parsed = urllib.parse.urlsplit(urllib.parse.urljoin(root, raw))
        if (parsed.scheme == "https" and parsed.hostname == "db.history.go.kr"
                and parsed.username is None and parsed.password is None
                and parsed.path.endswith(".js")
                and parsed.path.startswith(("/resources/", "/goryeo/"))):
            allowed.append(urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, parsed.query, "")))
    seen = set()
    ordered = []
    for url in allowed:
        if url not in seen:
            ordered.append(url)
            seen.add(url)
    # Source-emitted assets only; this never probes guessed image endpoints.
    return ordered[:16]

def source_declared_viewer_url(script_records, target_options):
    script_proof = any("function fnImageViewerPopup" in z["markup"] and
                       '"/common/imageViewer.do"' in z["markup"]
                       for record in script_records for z in record.get("function_context", []))
    if not script_proof or len(target_options) != 1:
        return None
    call = target_options[0]["source_emitted_onclick"]
    m = re.fullmatch(r"fnImageViewerPopup\('(kr_052_0010_0010_0020_0020)', '(kr_052_[0-9]+)'\)", call)
    if not m:
        return None
    # Public URL is composed from the first-party publisher's actual JS
    # function body and the first-party target HTML onclick parameters.
    return urllib.parse.urljoin(ARTICLE, "/common/imageViewer.do") + "?" + urllib.parse.urlencode({"levelId": m.group(1), "begin": m.group(2)})

def read_public_html(url, name):
    rec = {"url": url, "status": "NOT_FETCHED", "http": None, "bytes": 0, "sha256": None}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Tianwen-Research-13EZ/1.0 (read-only institutional bibliography)", "Accept": "text/html"})
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            rec["http"] = response.status
            if response.status != 200:
                rec["status"] = "HTTP_NON_200"
                return rec, None
            length = response.headers.get("Content-Length")
            if length and int(length) > LIMIT:
                rec["status"] = "DECLINED_TOO_LARGE"
                return rec, None
            raw = response.read(LIMIT + 1)
            if len(raw) > LIMIT:
                rec["status"] = "DECLINED_TOO_LARGE"
                return rec, None
            rec["bytes"] = len(raw)
            rec["sha256"] = hashlib.sha256(raw).hexdigest()
            rec["status"] = "PUBLIC_HTML_CAPTURED"
            ROOT.mkdir(parents=True, exist_ok=True)
            (ROOT / name).write_bytes(raw)
            return rec, raw.decode("utf-8", "replace")
    except urllib.error.HTTPError as err:
        rec["http"] = err.code
        rec["status"] = "HTTP_ERROR"
    except Exception as err:
        rec["status"] = "TRANSPORT_ERROR"
        rec["error_type"] = type(err).__name__
    return rec, None

def extract_target_viewer_menu(markup):
    # Extract only browser-source-emitted options under the specific first-party
    # multi-image menu. An onclick function call is NOT an authenticated image.
    if not markup:
        return []
    menu = re.search(r'<div class="popup-nd popup-multiImg">(?P<body>.*?)</ul>', markup, re.S)
    if not menu:
        return []
    result = []
    for match in re.finditer(r'<a\b[^>]*\bonclick="(?P<call>fnImageViewerPopup\([^"]+\))[^"]*"[^>]*>(?P<label>.*?)</a>', menu.group("body"), re.S):
        call = match.group("call")
        if not re.fullmatch(r"fnImageViewerPopup\('kr_052_0010_0010_0020_0020', 'kr_[0-9]+_[0-9]+'\)", call):
            continue
        label = re.sub(r"\s+", " ", re.sub(r"<[^>]*>", " ", match.group("label"))).strip()
        if label:
            result.append({"label": label, "source_emitted_onclick": call, "original_image_verified": False})
    return result[:8]

def bounded_literal_context(markup, literal, flank=520, limit=3):
    if not markup:
        return []
    results = []
    start = 0
    for _ in range(limit):
        offset = markup.find(literal, start)
        if offset < 0:
            break
        before = max(0, offset - flank)
        after = min(len(markup), offset + len(literal) + flank)
        results.append({"literal": literal, "offset": offset, "markup": markup[before:after]})
        start = offset + len(literal)
    return results

def source_emitted_thumb_urls(viewer_markup):
    # Read only actual HTML data-src bytes, never enumerate invented image IDs.
    if not viewer_markup:
        return []
    found = []
    for raw in re.findall(r'<img\b[^>]*\bdata-src="([^"]+)"', viewer_markup, re.I):
        u = urllib.parse.urlsplit(urllib.parse.urljoin(ARTICLE, raw))
        q = urllib.parse.parse_qs(u.query, keep_blank_values=True)
        if (u.scheme == "https" and u.hostname == "db.history.go.kr"
                and u.path == "/common/imageProxy.do"
                and q.get("mode") == ["thumb"]
                and len(q.get("filePath", [])) == 1
                and re.fullmatch(r"/kr/052/kr_052_[0-9]+\.jpg", q["filePath"][0])):
            found.append(urllib.parse.urlunsplit((u.scheme, u.netloc, u.path, u.query, "")))
    return list(dict.fromkeys(found))

def read_public_thumbnail(url, number):
    row = {"url": url, "status": "NOT_FETCHED", "http": None, "bytes": 0, "sha256": None, "jpeg_signature_verified": False}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Tianwen-Research-13EZ/1.0 (official-source-emitted-thumbnail-check)", "Accept": "image/jpeg,image/*;q=0.8"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            row["http"] = r.status
            if r.status != 200:
                row["status"] = "HTTP_NON_200"
                return row
            raw = r.read(3_000_001)
            if len(raw) > 3_000_000:
                row["status"] = "DECLINED_TOO_LARGE"
                return row
            row["bytes"] = len(raw)
            row["sha256"] = hashlib.sha256(raw).hexdigest()
            row["jpeg_signature_verified"] = raw.startswith(b"\xff\xd8\xff")
            row["status"] = "PUBLIC_THUMBNAIL_CAPTURED" if row["jpeg_signature_verified"] else "NOT_JPEG"
            if row["jpeg_signature_verified"]:
                (ROOT / f"official-juan52-thumb-{number:02d}.jpg").write_bytes(raw)
    except urllib.error.HTTPError as e:
        row["status"] = "HTTP_ERROR"
        row["http"] = e.code
    except Exception as e:
        row["status"] = "TRANSPORT_ERROR"
        row["error_type"] = type(e).__name__
    return row

def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    article, article_html = read_public_html(ARTICLE, "official-juan52-article.html")
    listing, list_html = read_public_html(NOTICE_INDEX, "official-notice-index.html")
    help_page, help_html = read_public_html(HELP, "official-image-viewer-help.html")
    parser = PageAnchors()
    if article_html:
        parser.feed(article_html)
    linked_notice = official_notice_links(list_html) if list_html else []
    js_files = []
    for idx, url in enumerate(firstparty_script_urls(parser.script_sources)):
        row, js_body = read_public_html(url, f"official-source-script-{idx:02d}.js")
        js_files.append({"fetch": row, "function_context": bounded_literal_context(js_body, "fnImageViewerPopup", flank=600, limit=2)})
    notice_body = []
    # Follow only an explicit first-party link emitted by the official index.
    for i, url in enumerate(linked_notice[:1]):
        row, html = read_public_html(url, f"official-notice-body-{i}.html")
        notice_body.append({"fetch": row, "declared_title_present": NOTICE_TITLE in html if html else None})
    viewer_url = source_declared_viewer_url(js_files, extract_target_viewer_menu(article_html))
    viewer_read = None
    viewer_html = None
    if viewer_url:
        viewer_read, viewer_html = read_public_html(viewer_url, "official-source-declared-juan52-viewer.html")
    thumbs = source_emitted_thumb_urls(viewer_html)
    thumb_reads = [read_public_thumbnail(url, i + 1) for i, url in enumerate(thumbs[:3])]
    result = {
        "schema": "TIANWEN-13EZ-NIKH-FIRSTPARTY-EMITTED-IMAGE-ENTRY-ACCESS-PROBE-R1",
        "source_article": article,
        "official_notice_list": listing,
        "official_help": help_page,
        "article_original_image_widget_attributes": parser.image_widgets[:20],
        "source_emitted_script_assets": js_files,
        "source_declared_public_viewer_url": viewer_url,
        "public_viewer_html": viewer_read,
        "public_viewer_source_emitted_thumbnail_urls": thumbs,
        "source_emitted_thumbnail_reads": thumb_reads,
        "thumbnail_image_is_not_a_full_original_source_folio": True,
        "public_viewer_target_context": bounded_literal_context(viewer_html, "kr_052_1055", flank=700),
        "public_viewer_image_references_context": bounded_literal_context(viewer_html, ".jpg", flank=300, limit=3),
        "inline_function_context": bounded_literal_context(article_html, "function fnImageViewerPopup", flank=600),
        "article_source_emitted_image_icon_context": bounded_literal_context(article_html, "고려사 원문이미지"),
        "target_source_emitted_viewer_options": extract_target_viewer_menu(article_html),
        "notice_list_title_event_context": bounded_literal_context(list_html, NOTICE_TITLE),
        "notice_2023_exact_source_emitted_detail_links": linked_notice,
        "notice_2023_detail_reads": notice_body,
        "help_original_image_label_present": ("원문이미지" in help_html) if help_html else None,
        "browser_popup_not_executed": True,
        "original_image_bytes_acquired": False,
        "specific_physical_book": None,
        "specific_juan52_folio": None,
        "source_original_png_sha256": None,
        "ncl_d5_original_photo_vs_krdb_editorial_glyph": "UNADJUDICATED",
        "historical_glyph_votes_added": 0,
        "source_id_inferred_from_published_label": False,
        "unverified_2023_link_destination_not_assumed": True,
        "no_hidden_endpoint_enumeration": True,
        "no_ocr_or_glyph_inference": True,
        "research_risk_closures": 0
    }
    (ROOT / "probe-result.json").write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))

if __name__ == "__main__":
    main()
