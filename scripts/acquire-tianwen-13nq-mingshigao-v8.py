#!/usr/bin/env python3
"""13NQ: source-hash-bound Harvard MingShiGao v8 PDF intake and page atlas. No OCR."""
import base64
import hashlib
import io
import json
from pathlib import Path

import fitz
import requests
from PIL import Image, ImageDraw

NAME = "Harvard drs 428231729 明史稿 v.8.pdf"
URL = "https://upload.wikimedia.org/wikipedia/commons/1/1d/Harvard_drs_428231729_%E6%98%8E%E5%8F%B2%E7%A8%BF_v.8.pdf"
EXPECTED_BYTES = 102710779
EXPECTED_SHA1 = "08745948f3bca1658cd2f06003103138eb2e35ee"
OUT = Path("/tmp/tianwen-13nq")
OUT.mkdir(parents=True, exist_ok=True)


def main():
    s = requests.Session()
    s.headers.update({"User-Agent": "TianwenHistoricalResearch/13NQ (public-domain source verification)"})
    attempts = []
    source = OUT / "source-original.pdf"
    for attempt in range(2):
        try:
            h1, h256, n = hashlib.sha1(), hashlib.sha256(), 0
            with s.get(URL, stream=True, timeout=(25, 130)) as response:
                response.raise_for_status()
                assert response.url.startswith("https://upload.wikimedia.org/wikipedia/commons/")
                with source.open("wb") as f:
                    for chunk in response.iter_content(1024 * 1024):
                        if chunk:
                            n += len(chunk)
                            assert n <= EXPECTED_BYTES, "unexpected data length"
                            h1.update(chunk)
                            h256.update(chunk)
                            f.write(chunk)
            assert n == EXPECTED_BYTES and h1.hexdigest() == EXPECTED_SHA1, "source digest mismatch"
            break
        except Exception as exc:
            attempts.append(type(exc).__name__ + ": " + str(exc)[:180])
            source.unlink(missing_ok=True)
    else:
        # A rate limit is a bounded transport observation, never absence of the work.
        probes = []
        for probe_url in (
            "https://iiif.lib.harvard.edu/manifests/drs:428231729",
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1d/Harvard_drs_428231729_%E6%98%8E%E5%8F%B2%E7%A8%BF_v.8.pdf/page2-1920px-Harvard_drs_428231729_%E6%98%8E%E5%8F%B2%E7%A8%BF_v.8.pdf.jpg",
        ):
            try:
                response = s.get(probe_url, timeout=(15, 30))
                entry = {"url": probe_url, "http": response.status_code, "mime": response.headers.get("Content-Type")}
                if response.status_code == 200 and "iiif.lib.harvard.edu" in probe_url:
                    data = response.json()
                    sequences = data.get("sequences", [])
                    entry["manifest_sequence_count"] = len(sequences)
                    if sequences:
                        entry["manifest_canvas_count"] = len(sequences[0].get("canvases", []))
                        entry["manifest_first_canvas_id"] = sequences[0].get("canvases", [{}])[0].get("@id")
                if response.status_code == 200 and "thumb.wikimedia.org" in probe_url:
                    entry["bytes"] = len(response.content)
                    entry["sha256"] = hashlib.sha256(response.content).hexdigest()
                    (OUT / "provider-page2-preview.jpg").write_bytes(response.content)
                probes.append(entry)
            except Exception as exc:
                probes.append({"url": probe_url, "error": type(exc).__name__ + ": " + str(exc)[:170]})
        record = {"schema": "TIANWEN-13NQ-HARVARD-MINGSHIGAO-SOURCE-ACCESS-BOUNDARY-R1",
                  "source_pdf_acquired": False, "expected_pdf_bytes": EXPECTED_BYTES,
                  "expected_pdf_sha1_unverified": EXPECTED_SHA1,
                  "source_pdf_sha256": None, "attempt_errors": attempts,
                  "alternative_provider_probes": probes,
                  "original_j29_glyphs_collated": False,
                  "no_negative_historical_proof": True}
        # Restrict page discovery to a small known Commons preview family.
        # These are page-rendered public previews, NOT the source PDF or native-page pixels.
        available = {}
        first = OUT / "provider-page2-preview.jpg"
        if first.exists():
            available[2] = first.read_bytes()
        base_preview = "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1d/Harvard_drs_428231729_%E6%98%8E%E5%8F%B2%E7%A8%BF_v.8.pdf/"
        filename = "Harvard_drs_428231729_%E6%98%8E%E5%8F%B2%E7%A8%BF_v.8.pdf.jpg"
        for page in (15, 17, 19, 21, 23, 25, 27, 28):
            address = base_preview + "page%d-1920px-" % page + filename
            try:
                response = s.get(address, timeout=(15, 35))
                if response.status_code != 200:
                    record.setdefault("preview_access_errors", []).append({"page": page, "http": response.status_code})
                    if response.status_code in (429, 403):
                        break
                    continue
                body = response.content
                if not (body[:2] == bytes.fromhex("ffd8") and 10000 < len(body) < 3000000):
                    record.setdefault("preview_access_errors", []).append({
                        "page": page, "error": "invalid JPEG or unexpected size",
                        "mime": response.headers.get("Content-Type"),
                        "bytes": len(body),
                        "prefix_hex": body[:35].hex()
                    })
                    continue
                available[page] = body
                (OUT / ('sample-page-%03d.jpg' % page)).write_bytes(body)
            except Exception as exc:
                record.setdefault("preview_access_errors", []).append({"page": page, "error": type(exc).__name__+": "+str(exc)[:90]})
                break
        if available:
            canvas = Image.new("RGB", (4*400, 3*520), "white")
            draw = ImageDraw.Draw(canvas)
            recs = []
            for pos, (page, data) in enumerate(sorted(available.items())):
                im = Image.open(io.BytesIO(data)).convert("RGB")
                im.thumbnail((388, 484))
                left, top = pos%4*400, pos//4*520
                canvas.paste(im,(left+(400-im.width)//2,top+6))
                draw.text((left+8,top+493),"PREVIEW PDF p%d" % page,fill="black")
                recs.append({"page":page,"source":"COMMONS_PUBLIC_1920PX_RENDERED_PREVIEW_NOT_NATIVE_PDF",
                            "jpeg_sha256":hashlib.sha256(data).hexdigest(),"jpeg_bytes":len(data)})
            out=io.BytesIO()
            canvas.save(out,format="WEBP",quality=68,method=4)
            data=out.getvalue()
            (OUT/"preview-sample-contact.webp").write_bytes(data)
            record["verified_page_previews"]=recs
            record["preview_atlas_sha256"]=hashlib.sha256(data).hexdigest()
            record["preview_atlas_no_ocr"]=True
            print("TW13NQ_PREVIEW_ATLAS_B64:"+base64.b64encode(data).decode("ascii"),flush=True)
        (OUT / "source-access-error.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
        print("TW13NQ_SOURCE_ACCESS_BOUNDARY:" + json.dumps(record, ensure_ascii=False), flush=True)
        return
    results = []
    with fitz.open(source) as pdf:
        assert len(pdf) == 107, "unexpected PDF page count"
        for start in range(0, len(pdf), 16):
            canvas = Image.new("RGB", (4 * 400, 4 * 475), "white")
            draw = ImageDraw.Draw(canvas)
            for i in range(start, min(start + 16, len(pdf))):
                pg = pdf.load_page(i)
                pix = pg.get_pixmap(matrix=fitz.Matrix(0.20, 0.20), colorspace=fitz.csRGB, alpha=False)
                img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                img.thumbnail((385, 440))
                left = (i-start) % 4 * 400
                top = (i-start) // 4 * 475
                canvas.paste(img, (left + (400-img.width)//2, top+8))
                draw.text((left+12, top+450), "PDF p%d" % (i+1), fill="black")
            contents = io.BytesIO()
            canvas.save(contents, format="WEBP", quality=65, method=4)
            data = contents.getvalue()
            filename = "contact-%03d-%03d.webp" % (start+1, min(start+16, len(pdf)))
            (OUT / filename).write_bytes(data)
            results.append({"file": filename, "sha256": hashlib.sha256(data).hexdigest(), "pages": [start+1, min(start+16, len(pdf))]})
            # Log base64 for direct model review without relying on OCR or local network access.
            print("TW13NQ_ATLAS_B64_%02d:%s" % (start//16+1, base64.b64encode(data).decode("ascii")), flush=True)
    record = {"schema": "TIANWEN-13NQ-HARVARD-MINGSHIGAO-V8-SOURCE-ATLAS-INTAKE-R1",
              "commons_title": NAME, "commons_original_url": URL,
              "source_pdf_bytes": n, "provider_sha1_verified": h1.hexdigest(),
              "source_pdf_sha256": h256.hexdigest(), "pdf_pages": 107,
              "contact_atlases": results, "ocr_used": False,
              "original_target_glyph_collated": False,
              "original_target_juan29_page_found": False,
              "physical_impression_date_verified": False,
              "source_is_new_independent_physical_witness": False}
    (OUT / "source-meta.json").write_text(json.dumps(record, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("TW13NQ_RESULT_META:"+json.dumps(record, ensure_ascii=False), flush=True)
    source.unlink(missing_ok=True)  # artifact contains bounded atlas and source hashes, not 98 MB PDF.


if __name__ == "__main__":
    main()
