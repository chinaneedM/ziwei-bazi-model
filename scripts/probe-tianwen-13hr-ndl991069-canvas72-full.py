#!/usr/bin/env python3
"""Acquire NDL1909 canvas72 source-issued full JPEG; do not infer ancient numbers."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import urllib.request
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PREVIOUS = ROOT / "scripts/probe-tianwen-13hn-ndl991069-v52-atlas.py"
SPEC = importlib.util.spec_from_file_location("tianwen_13hn", PREVIOUS)
HN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HN)
OUT = ROOT / "artifacts/13hr-ndl991069-canvas72-provider-full"
MANIFEST = "https://dl.ndl.go.jp/api/iiif/991069/manifest.json"
EXPECTED_MANIFEST_SHA = "5ef67e4f84917ffd1eafee2b2da1d22f1aeb68f8d7f2ac441b7d398be19bf674"
CANVAS = "https://dl.ndl.go.jp/api/iiif/991069/canvas/72"
PREVIEW_DIM = (1600, 1248)
HEADINGS = {"winter-heading-context": (115, 130, 780, 650), "initial-days-context": (105, 540, 775, 995)}

def source_canvas(manifest):
    cs, ids = HN.canvases(manifest)
    start, end = HN.toc_scope(manifest, ids)
    if (start, end) != (68, 91) or ids[71] != CANVAS:
        raise ValueError("different original volume/canvas")
    service = HN.image_service(cs[71])
    if service != "https://dl.ndl.go.jp/api/iiif/991069/R0000072":
        raise ValueError("unexpected source-issued service")
    return cs[71], service

def scaled_box(box, output_size, pad=0):
    w, h = output_size
    if w < 1600 or h < 1248 or max(w, h) > 5000:
        raise ValueError("unexpected image size")
    x1, y1, x2, y2 = box
    if not (0 <= x1 < x2 <= 1600 and 0 <= y1 < y2 <= 1248):
        raise ValueError("preview coordinates out of bounds")
    # Use source-preview fractions, NOT a guessed numerical/seasonal column.
    return (max(0, int((x1-pad)*w/1600)), max(0, int((y1-pad)*h/1248)),
            min(w, int((x2+pad)*w/1600 + 0.999999)),
            min(h, int((y2+pad)*h/1248 + 0.999999)))

def get(url, limit):
    data, code, mime = HN.fetch(url, limit)
    if code != 200:
        raise ValueError("non-200 response")
    return data, mime

def save_bytes(filename, data):
    dest = OUT / filename
    dest.write_bytes(data)
    return {"file": filename, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = {
        "schema": "TIANWEN-13HR-NDL991069-CANVAS73-ONE-PAGE-SOURCE-CAPTURE-R1",
        "provider": "National Diet Library of Japan", "pid": "991069",
        "juan": 52, "print_year": 1909, "canvas": 72,
        "evidence_grade": "1909_RECEIVED_PRINT_ACQUISITION_ONLY_UNREAD_NO_GLYPH_OR_NUMERIC_ADJUDICATION",
        "previous_preview_sha256": "295a3a839914f51a33c19f6e7cea6c113413d9bcb3c2423c60589bb51bdf5c86",
        "official_interface_spec": "https://dl.ndl.go.jp/static/files/IIIF_interface_En.pdf",
        "max_response_dimension_from_official_2018_spec": 5000,
        "no_ocr": True, "no_original_copy_identity_claim": True,
        "numeric_glyphs_decided": 0, "source_additions": 0,
        "Taiwan_NCL03130_D14": None, "G893_six": "OPEN",
        "assets": [],
    }
    try:
        data, mime = get(MANIFEST, 12000000)
        digest = hashlib.sha256(data).hexdigest()
        report["manifest_sha256"] = digest
        if digest != EXPECTED_MANIFEST_SHA:
            raise ValueError("manifest changed, rebind before interpreting")
        manifest = json.loads(data)
        canvas, service = source_canvas(manifest)
        declared_size = (canvas.get("width"), canvas.get("height"))
        if not all(isinstance(n, int) and n > 0 for n in declared_size):
            raise ValueError("canvas dimensions absent")
        report["declared_source_canvas_size"] = list(declared_size)
        image_url = service + "/full/full/0/default.jpg"
        body, mime = get(image_url, 30000000)
        if not mime.lower().startswith("image/jpeg") or not body.startswith(b"\xff\xd8"):
            raise ValueError("not original provider JPEG response")
        im = Image.open(io.BytesIO(body))
        im.load()
        if im.format != "JPEG" or max(im.size) > 5000 or min(im.size) < 1200:
            raise ValueError("unexpected full-size image response")
        if abs(im.width/im.height - declared_size[0]/declared_size[1]) > 0.015:
            raise ValueError("canvas width/height ratio mismatch")
        report["source_issued_full_request_url"] = image_url
        report["provider_response_dimensions"] = list(im.size)
        report["provider_response_limited_to_5000_pixels"] = max(im.size) == 5000
        report["assets"].append(save_bytes("canvas-072-full-provider.jpg", body))
        for tag, original in HEADINGS.items():
            box = scaled_box(original, im.size, pad=25)
            crop = im.crop(box)
            bio = io.BytesIO()
            crop.save(bio, format="PNG")
            asset = save_bytes(tag + ".png", bio.getvalue())
            asset.update(preview_approximate_context_bbox=list(original), image_bbox=list(box),
                         reading_status="UNREAD_NO_NUMERIC_DECISION", same_day_column_proven=False)
            report["assets"].append(asset)
        # Keep the left-leaf heading and day-range neighborhood, not a numeric finding.
        context = scaled_box((90, 140, 850, 1130), im.size)
        bio = io.BytesIO()
        im.crop(context).save(bio, format="PNG")
        a = save_bytes("left-leaf-table-context.png", bio.getvalue())
        a["image_bbox"] = list(context)
        report["assets"].append(a)
        report["status"] = "FULL_PROVIDER_IMAGE_CAPTURED_UNREAD"
    except Exception as exc:
        report["status"] = "SOURCE_ACCESS_OR_BINDING_BOUNDARY"
        report["error_type"] = type(exc).__name__
        report["error_message"] = str(exc)[:300]
    path = OUT / "report.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report.get(k) for k in (
        "status", "manifest_sha256", "provider_response_dimensions", "error_type", "assets"
    )}, ensure_ascii=False))

    return report["status"]

if __name__ == "__main__":
    if main() != "FULL_PROVIDER_IMAGE_CAPTURED_UNREAD":
        raise SystemExit(1)
