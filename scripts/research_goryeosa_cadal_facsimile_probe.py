#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
DEFAULT_FILE = "CADAL02050311 高麗史（四十九）.djvu"
UA = "ziwei-bazi-model-historical-research/1.0 (read-only Commons facsimile probe)"

NEEDLES = {
    "shoushi_licheng": ["授時曆立成", "授时历立成"],
    "solar_winter": ["太陽冬至", "大陽冬至", "太阳冬至", "大阳冬至"],
    "solar_yingsuo": ["盈初縮末限", "盈初缩末限", "盈縮", "盈缩"],
    "lunar_limits": ["太陰限數", "太阴限数", "太陰限", "太阴限"],
    "lunar_chiji": ["遲疾度", "迟疾度", "遲疾", "迟疾"],
    "volume_anchor": ["高麗史五十二", "高丽史五十二", "曆三", "历三"],
}

def commons_original_url(filename: str) -> str:
    q = urllib.parse.urlencode({
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url|size",
        "titles": f"File:{filename}",
    })
    req = urllib.request.Request(f"{COMMONS_API}?{q}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.load(resp)
    pages = data["query"]["pages"]
    page = next(iter(pages.values()))
    info = page["imageinfo"][0]
    return info["url"]

def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as resp, dest.open("wb") as out:
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)

def run_text(source: Path, page: int) -> str:
    proc = subprocess.run(
        ["djvutxt", f"--page={page}", str(source)],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        return ""
    return proc.stdout.decode("utf-8", errors="replace")

def norm(s: str) -> str:
    return re.sub(r"\s+", "", s)

def excerpt(text: str, needle: str, radius: int = 180) -> str:
    compact = re.sub(r"\s+", " ", text)
    i = compact.find(needle)
    if i < 0:
        return compact[: radius * 2]
    return compact[max(0, i-radius):i+len(needle)+radius]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/goryeosa-cadal-probe")
    ap.add_argument("--filename", default=DEFAULT_FILE)
    args = ap.parse_args()

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    source = out / "source.djvu"
    url = commons_original_url(args.filename)
    download(url, source)

    nproc = subprocess.run(
        ["djvused", str(source), "-e", "n"],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    page_count = int(nproc.stdout.strip())

    page_records = []
    hits = []
    text_pages = 0
    for page in range(1, page_count + 1):
        text = run_text(source, page)
        compact = norm(text)
        if compact:
            text_pages += 1
        matched = []
        score = 0
        for family, needles in NEEDLES.items():
            family_hits = [n for n in needles if n in compact or n in text]
            if family_hits:
                matched.append({"family": family, "needles": family_hits})
                score += 4 if family in {"shoushi_licheng", "solar_winter", "lunar_limits"} else 1
        rec = {
            "page": page,
            "text_chars": len(text),
            "score": score,
            "matched": matched,
        }
        page_records.append(rec)
        if matched:
            best = matched[0]["needles"][0]
            hits.append({
                **rec,
                "excerpt": excerpt(text, best),
            })

    hits.sort(key=lambda x: (-x["score"], x["page"]))
    manifest = {
        "schema": "GORYEOSA-CADAL-FACSIMILE-TEXT-LAYER-PROBE-R1",
        "source_filename": args.filename,
        "source_url": url,
        "page_count": page_count,
        "pages_with_extracted_text": text_pages,
        "ocr_used": False,
        "probe_scope": "EXISTING_DJVU_TEXT_LAYER_ONLY",
        "target_glyph_authority": False,
        "target_value_prepopulation_authorized": False,
        "note": "Text-layer hits localize candidate scan pages only. Exact target glyph conclusions require direct page-image inspection.",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    (out / "hits.json").write_text(json.dumps(hits, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    (out / "page-signatures.json").write_text(json.dumps(page_records, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    source.unlink(missing_ok=True)

    print(json.dumps({
        **manifest,
        "hit_count": len(hits),
        "top_hits": hits[:30],
    }, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
