#!/usr/bin/env python3
"""Recover four already registered G893 originals; never infer target glyphs."""
import hashlib
import io
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
XU = "docs/research/TIANWEN-12XU-G893-L8-L132-SOURCE-GLYPH-AND-SYMMETRIC-LOCATORS-R1.json"
XX = "docs/research/TIANWEN-12XX-G893-L124-DIRECT-ORIGINAL-JI-XINGDU-GLYPH-R1.json"
CAP = 3_000_000


def targets():
    xu = json.loads((ROOT / XU).read_text())
    xx = json.loads((ROOT / XX).read_text())
    pages = {x["page_id"]: {"url": x["original_source_url"],
             "sha256": x["source_jpeg_sha256"], "source_doc": XU}
             for x in xu["original_fields"]}
    for x in (xx["source_page"], xx["structural_header"]):
        pages[x["page_id"]] = {"url": x["source_issued_original_image_url"],
             "sha256": x["source_original_sha256"], "source_doc": XX}
    if set(pages) != {"018b", "019b", "035b", "036b"}:
        raise ValueError("only four pre-registered exact source pages permitted")
    for page, x in pages.items():
        p = urllib.parse.urlsplit(x["url"])
        q = urllib.parse.parse_qs(p.query)
        fn = f"GK00893_00IH_0001_{page}.jpg"
        if (p.scheme, p.netloc, p.path) != ("https", "kyudb.snu.ac.kr", "/ImageServlet.do"):
            raise ValueError("unexpected provider")
        if q != {"imgFileNm": [fn], "path": [f"/data01/stream/SIC/IMG/GK00893_00/GK00893_00_0001/{fn}"]}:
            raise ValueError("unregistered source path")
    return pages


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(newurl, code, "redirect not accepted", headers, fp)


def inspect(raw, expected):
    from PIL import Image
    if not raw.startswith(b"\xff\xd8\xff") or hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError("not exact previously registered JPEG bytes")
    with Image.open(io.BytesIO(raw)) as im:
        if im.format != "JPEG" or im.size != (1150, 2000):
            raise ValueError("unexpected source dimensions")
        rgb = im.convert("RGB")
        return {"size_px": list(rgb.size), "rgb_sha256": hashlib.sha256(rgb.tobytes()).hexdigest()}


def main():
    out = Path(os.environ.get("TIANWEN_13JZ_OUT", "/tmp/tianwen-13jz"))
    out.mkdir(parents=True, exist_ok=True)
    opener = urllib.request.build_opener(NoRedirect())
    records = []
    for page, target in sorted(targets().items()):
        record = {"page_id": page, **target, "attempts": [], "status": "NOT_ACQUIRED"}
        for attempt in range(1, 3):
            try:
                req = urllib.request.Request(target["url"], headers={
                    "User-Agent": "Mozilla/5.0 Tianwen-13JZ-Exact-Original/1.0",
                    "Accept": "image/jpeg", "Referer": "https://kyudb.snu.ac.kr/pf01/rendererImg.do"})
                with opener.open(req, timeout=22) as response:
                    raw = response.read(CAP + 1)
                    if response.status != 200 or not 0 < len(raw) <= CAP:
                        raise ValueError("non-200/empty/oversized response")
                    record["attempts"].append({"attempt": attempt, "http": response.status,
                        "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
                    record.update(inspect(raw, target["sha256"]))
                    (out / f"{page}.jpg").write_bytes(raw)
                    record.update(status="EXACT_ORIGINAL_REACQUIRED_UNCOLLATED", file=f"{page}.jpg")
                    break
            except urllib.error.HTTPError as e:
                record["attempts"].append({"attempt": attempt, "http": e.code, "error": "HTTPError"})
            except Exception as e:
                record["attempts"].append({"attempt": attempt, "error": type(e).__name__, "detail": str(e)[:200]})
        records.append(record)
    report = {"schema": "TIANWEN-13JZ-G893-EXACT-PAGE-RECOVERY-R1", "pages": records,
        "glyph_collation_performed": False, "cross_witness_winners": 0, "new_physical_witnesses": 0,
        "old_archive_recovered": False, "old_204_page_integrity_claim_replayed": False}
    (out / "receipt.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"exact_pages_recovered": sum(x["status"].startswith("EXACT_") for x in records),
                      "requested": len(records), "glyphs_collated": False}))


if __name__ == "__main__":
    main()
