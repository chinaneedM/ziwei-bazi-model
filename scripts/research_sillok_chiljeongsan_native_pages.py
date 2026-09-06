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

def fetch(url: str, timeout: int = 35) -> tuple[int, str, bytes]:
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
    # Prefer the largest array because the viewer may contain both the active
    # article image and a full image-only tab array for the same bound unit.
    return max(arrays, key=len)

def image_proxy_url(token: str) -> str:
    file_path = "/s_img/SILLOK/" + token + ".jpg"
    return BASE + "/viewer/imageProxy.do?filePath=" + urllib.parse.quote(file_path, safe="/")

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
        thumb = im.resize((thumb_w, h))
        thumbs.append((token, thumb))
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

    result = {
        "schema": "SILLOK-CHILJEONGSAN-NATIVE-PAGES-R1",
        "base": BASE,
        "ocr_used": False,
        "target_values_authorized_by_fetch": False,
        "localization_basis": "OFFICIAL_ARTICLE_ID_TO_OFFICIAL_VIEWER_IMGARR_TO_OFFICIAL_IMAGEPROXY",
        "source_layer": "NATIONAL_INSTITUTE_OF_KOREAN_HISTORY_SILLOK_VIEWER",
        "articles": [],
    }
    any_error = False

    for article_id, meta in ARTICLES.items():
        viewer_url = f"{BASE}/popup/viewer.do?type=view&id={article_id}"
        vstatus, vctype, vbody = fetch(viewer_url)
        vtext = vbody.decode("utf-8", "replace")
        viewer_file = out / f"{article_id}-viewer.html"
        viewer_file.write_text(vtext, encoding="utf-8")

        article = {
            "article_id": article_id,
            "viewer_url": viewer_url,
            **meta,
            "viewer_status": vstatus,
            "viewer_content_type": vctype,
            "viewer_bytes": len(vbody),
            "ocr_used": False,
            "target_values_authorized_by_fetch": False,
            "pages": [],
        }
        try:
            tokens = parse_imgarr(vtext)
        except Exception as exc:
            article["parse_error"] = f"{type(exc).__name__}: {exc}"
            result["articles"].append(article)
            any_error = True
            continue
        article["imgarr_tokens"] = tokens
        native_for_sheet = []

        for index, token in enumerate(tokens):
            url = image_proxy_url(token)
            status, ctype, body = fetch(url)
            rec = {
                "index": index,
                "token": token,
                "proxy_url": url,
                "status": status,
                "content_type": ctype,
                "bytes": len(body),
                "sha256": hashlib.sha256(body).hexdigest(),
                "ocr_used": False,
                "target_values_authorized_by_fetch": False,
            }
            if status == 200:
                try:
                    im = Image.open(io.BytesIO(body)).convert("RGB")
                    rec["size"] = [im.width, im.height]
                    filename = f"{article_id}-{index:03d}-{token.split('/')[-1]}.jpg"
                    im.save(out / filename, quality=95)
                    rec["file"] = filename
                    native_for_sheet.append((token, im))
                except Exception as exc:
                    rec["image_error"] = f"{type(exc).__name__}: {exc}"
                    any_error = True
            else:
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
