#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw

BASE = "https://sillok.history.go.kr"
LEGACY_BASE = "http://sillok.history.go.kr"
ROOT = Path(__file__).resolve().parents[1]
DIRECT_BINDING_PATH = ROOT / "docs" / "research" / "SILLOK-CHILJEONGSAN-VIEWER-IMGARR-DIRECT-BINDING-R1.json"
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

def fetch(url: str, timeout: int = 15) -> tuple[int, str, bytes]:
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,image/jpeg,image/*,*/*;q=0.8",
        "Referer": BASE + "/",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return int(getattr(r, "status", 200)), r.headers.get("Content-Type", ""), r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type", ""), e.read()
    except Exception as e:
        return 0, type(e).__name__, str(e).encode("utf-8", "replace")

def parse_imgarr(viewer_html: str) -> list[str]:
    matches = re.findall(r"imgArr\s*=\s*\[(.*?)\];", viewer_html, flags=re.S)
    arrays = []
    for body in matches:
        vals = [x.replace("\\/", "/") for x in re.findall(r'"([^"]+)"', body)]
        if vals:
            arrays.append(vals)
    if not arrays:
        raise ValueError("imgArr not found")
    return max(arrays, key=len)

def image_candidate_urls(token: str) -> list[str]:
    current_path = "/images/org_images/" + token + ".jpg"
    current_q = urllib.parse.quote(current_path, safe="/")
    legacy_path = "/s_img/SILLOK/" + token + ".jpg"
    legacy_q = urllib.parse.quote(legacy_path, safe="/")
    return [
        BASE + current_path,
        LEGACY_BASE + current_path,
        BASE + "/viewer/imageProxy.do?filePath=" + current_q,
        LEGACY_BASE + "/viewer/imageProxy.do?filePath=" + current_q,
        BASE + legacy_path,
        LEGACY_BASE + legacy_path,
        BASE + "/viewer/imageProxy.do?filePath=" + legacy_q,
        LEGACY_BASE + "/viewer/imageProxy.do?filePath=" + legacy_q,
    ]

def make_contact_sheet(images: list[tuple[str, Image.Image]], path: Path) -> None:
    if not images:
        return
    thumb_w = 240
    label_h = 28
    cols = 5
    thumbs = []
    for token, im in images:
        ratio = thumb_w / im.width
        h = max(1, int(im.height * ratio))
        thumbs.append((token, im.resize((thumb_w, h))))
    cell_h = max(t.height for _, t in thumbs) + label_h
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w, rows * cell_h), "white")
    draw = ImageDraw.Draw(sheet)
    for i, (token, thumb) in enumerate(thumbs):
        x = (i % cols) * thumb_w
        y = (i // cols) * cell_h
        sheet.paste(thumb, (x, y))
        draw.text((x + 4, y + thumb.height + 4), token.split("/")[-1], fill="black")
    sheet.save(path, quality=90)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/sillok-chiljeongsan-native-pages")
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    direct_binding = json.loads(DIRECT_BINDING_PATH.read_text(encoding="utf-8"))

    result = {
        "schema": "SILLOK-CHILJEONGSAN-NATIVE-PAGES-R1",
        "base": BASE,
        "ocr_used": False,
        "target_values_authorized_by_fetch": False,
        "localization_basis": "OFFICIAL_ARTICLE_ID_TO_OFFICIAL_VIEWER_IMGARR_TO_OFFICIAL_IMAGE_TRANSPORT",
        "source_layer": "NATIONAL_INSTITUTE_OF_KOREAN_HISTORY_SILLOK_VIEWER",
        "image_route_priority": [
            "HTTPS_DIRECT_CURRENT_ORG_IMAGES",
            "HTTP_DIRECT_CURRENT_ORG_IMAGES",
            "HTTPS_IMAGEPROXY_CURRENT_ORG_IMAGES",
            "HTTP_IMAGEPROXY_CURRENT_ORG_IMAGES",
            "HTTPS_DIRECT_LEGACY_S_IMG",
            "HTTP_DIRECT_LEGACY_S_IMG",
            "HTTPS_IMAGEPROXY_LEGACY_S_IMG",
            "HTTP_IMAGEPROXY_LEGACY_S_IMG",
        ],
        "official_viewer_config_evidence": {
            "head_sha": "1cb774234a4c91171e354d86058d779cd48a759f",
            "workflow_run_id": 34015242124,
            "artifact_id": 9983692998,
            "imgFileRootDir": "/images/org_images/",
            "imgFileExt": ".jpg",
            "main_image_loader": "DIRECT_ROOT_PLUS_IMGARR_TOKEN_PLUS_EXT",
        },
        "articles": [],
    }
    any_error = False

    for article_id, meta in ARTICLES.items():
        viewer_urls = [
            f"{BASE}/popup/viewer.do?type=view&id={article_id}",
            f"{LEGACY_BASE}/popup/viewer.do?type=view&id={article_id}",
            f"{BASE}/popup/viewer.do?id={article_id}&type=view",
            f"{LEGACY_BASE}/popup/viewer.do?id={article_id}&type=view",
        ]
        viewer_attempts = []
        tokens = None
        vtext = ""
        for viewer_url in viewer_urls:
            vstatus, vctype, vbody = fetch(viewer_url)
            current_text = vbody.decode("utf-8", "replace")
            attempt = {
                "url": viewer_url,
                "status": vstatus,
                "content_type": vctype,
                "bytes": len(vbody),
            }
            try:
                parsed = parse_imgarr(current_text)
                attempt["imgarr_token_count"] = len(parsed)
                tokens = parsed
                vtext = current_text
            except Exception as exc:
                attempt["parse_error"] = f"{type(exc).__name__}: {exc}"
            viewer_attempts.append(attempt)
            if tokens is not None:
                break

        token_source = "LIVE_OFFICIAL_VIEWER"
        if tokens is None:
            bound = direct_binding["articles"].get(article_id, {})
            tokens = list(bound.get("imgarr_tokens", ()))
            token_source = "FAIL_SOFT_PRIOR_DIRECT_VIEWER_BINDING"
            if not tokens:
                raise SystemExit(f"no live or directly bound imgArr tokens for {article_id}")

        (out / f"{article_id}-viewer.html").write_text(vtext, encoding="utf-8")
        article = {
            "article_id": article_id,
            "viewer_attempts": viewer_attempts,
            **meta,
            "token_source": token_source,
            "direct_binding_artifact": "docs/research/SILLOK-CHILJEONGSAN-VIEWER-IMGARR-DIRECT-BINDING-R1.json",
            "ocr_used": False,
            "target_values_authorized_by_fetch": False,
            "pages": [],
            "imgarr_tokens": tokens,
        }
        native_for_sheet = []

        for index, token in enumerate(tokens):
            rec = {
                "index": index,
                "token": token,
                "attempts": [],
                "ocr_used": False,
                "target_values_authorized_by_fetch": False,
            }
            selected_image = None
            selected_body = None
            selected_meta = None
            for url in image_candidate_urls(token):
                status, ctype, body = fetch(url)
                attempt = {
                    "url": url,
                    "status": status,
                    "content_type": ctype,
                    "bytes": len(body),
                    "sha256": hashlib.sha256(body).hexdigest(),
                }
                if status == 200:
                    try:
                        candidate = Image.open(io.BytesIO(body)).convert("RGB")
                        attempt["valid_image"] = True
                        attempt["size"] = [candidate.width, candidate.height]
                        selected_image = candidate
                        selected_body = body
                        selected_meta = (url, status, ctype)
                    except Exception as exc:
                        attempt["valid_image"] = False
                        attempt["image_error"] = f"{type(exc).__name__}: {exc}"
                        if "text" in ctype.lower():
                            attempt["body_prefix"] = body[:300].decode("utf-8", "replace")
                rec["attempts"].append(attempt)
                if selected_image is not None:
                    break

            if selected_image is not None and selected_meta is not None and selected_body is not None:
                url, status, ctype = selected_meta
                rec["selected_url"] = url
                rec["status"] = status
                rec["content_type"] = ctype
                rec["bytes"] = len(selected_body)
                rec["sha256"] = hashlib.sha256(selected_body).hexdigest()
                rec["size"] = [selected_image.width, selected_image.height]
                filename = f"{article_id}-{index:03d}-{token.split('/')[-1]}.jpg"
                selected_image.save(out / filename, quality=95)
                rec["file"] = filename
                native_for_sheet.append((token, selected_image))
            else:
                rec["status"] = "NO_VALID_IMAGE"
                any_error = True
            article["pages"].append(rec)

        sheet = out / f"{article_id}-contact-sheet.jpg"
        make_contact_sheet(native_for_sheet, sheet)
        if sheet.exists():
            article["contact_sheet"] = sheet.name
        result["articles"].append(article)

    (out / "native-page-map.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if any_error else 0

if __name__ == "__main__":
    raise SystemExit(main())
