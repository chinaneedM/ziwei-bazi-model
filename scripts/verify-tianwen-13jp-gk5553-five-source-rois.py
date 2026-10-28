#!/usr/bin/env python3
"""13JP verify actual 13JI original JPEG archive bytes and ten native RGB pixel ROIs."""
import argparse
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs/research/TIANWEN-13JP-GK5553-13JI-FIVE-ORIGINAL-JPEG-PIXEL-ROI-REPLAY-R1.json"
PRIOR = ROOT / "docs/research/TIANWEN-13JJ-SNU-GK5553-ORIGINAL-12-29-PHOTO-COLLATION-R1.json"
ZIP_SHA = "3c6c870e6155edc2c994679ef6921334549696816f9443cc12b4dd6a97fb18fe"
PRIOR_GIT_BLOB = "77adb2bfac864c354f67890a0131dcfba1b6c2d2"

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def coords(name, width, height):
    if name == "heading_strip":
        return [round(width * .68), round(height * .12), width-20, round(height * .75)]
    if name == "body_field":
        return [round(width * .07), round(height * .20), round(width * .60), round(height * .78)]
    raise AssertionError("unexpected ROI name")

def verify_manifest(proof, prior):
    assert proof["source"]["artifact_zip_sha256"] == ZIP_SHA
    assert proof["source"]["prior_immutable_13jj_git_blob_sha1"] == PRIOR_GIT_BLOB
    assert proof["source"]["original_photos_artifact_id"] == 12809230903
    assert len(proof["original_images"]) == 5
    assert len(prior["original_pages"]) == 5
    assert proof["replay"]["verified_native_pixel_roi_sha256"] == 10
    assert proof["replay"]["new_independent_physical_witness_count"] == 0
    assert proof["replay"]["new_g893_numeric_controls_adjudicated"] == 0
    assert proof["replay"]["algorithm_reopens"] == 0
    assert proof["evidence_scope"]["actual_ancient_fascicle_ordinal"] == "UNBOUND"
    assert proof["evidence_scope"]["historical_13io_physical_book_29"].startswith("RETRACTED_")
    lookup = {(r["digital_volume"], r["page_no"]): r for r in prior["original_pages"]}
    assert set(lookup) == {(r["digital_volume"], r["digital_page"]) for r in proof["original_images"]}
    for page in proof["original_images"]:
        vol, leaf = page["digital_volume"], page["digital_page"]
        old = lookup[(vol, leaf)]
        assert page["artifact_member"] == old["artifact_member"]
        assert page["jpeg_bytes"] == old["source_jpeg_bytes"]
        assert page["jpeg_sha256"] == old["source_jpeg_sha256"]
        assert page["native_rgb_sha256"] == old["decoded_rgb_sha256"]
        assert page["work_juan"] == old["work_juan"]
        assert page["prior_13jj_visual_presentation"] == old["visual_presentation"]
        assert re.fullmatch("[a-f0-9]{64}", page["jpeg_sha256"])
        w, h = page["native_pixel_size"]
        assert 1000 <= w <= 1200 and h == 2000
        assert len(page["original_rgb_rois"]) == 2
        assert {x["name"] for x in page["original_rgb_rois"]} == {"heading_strip", "body_field"}
        for roi in page["original_rgb_rois"]:
            b = roi["xyxy"]
            assert len(b) == 4 and all(type(v) is int for v in b)
            assert b == coords(roi["name"], w, h)
            assert 0 <= b[0] < b[2] <= w and 0 <= b[1] < b[3] <= h
            assert roi["pixel_size"] == [b[2]-b[0], b[3]-b[1]]
            assert roi["pixel_size"][0] >= 250 and roi["pixel_size"][1] >= 500
            assert roi["pixel_format"] == "RGB"
            assert roi["rgb_bytes"] == 3 * roi["pixel_size"][0] * roi["pixel_size"][1]
            assert re.fullmatch("[a-f0-9]{64}", roi["rgb_sha256"])

def verify_zip(path, proof, prior):
    verify_manifest(proof, prior)
    assert sha(path.read_bytes()) == ZIP_SHA, "GitHub artifact ZIP digest mismatch"
    names = {x["artifact_member"] for x in proof["original_images"]}
    with zipfile.ZipFile(path) as z:
        assert set(z.namelist()) == names | {"source-jpeg-intake.json"}
        for page in proof["original_images"]:
            raw = z.read(page["artifact_member"])
            assert len(raw) == page["jpeg_bytes"] and sha(raw) == page["jpeg_sha256"]
            assert raw.startswith(bytes.fromhex("ffd8ff")) and raw.endswith(bytes.fromhex("ffd9"))
            rgb = Image.open(io.BytesIO(raw)).convert("RGB")
            assert list(rgb.size) == page["native_pixel_size"]
            assert sha(rgb.tobytes()) == page["native_rgb_sha256"]
            for roi in page["original_rgb_rois"]:
                im = rgb.crop(tuple(roi["xyxy"]))
                assert len(im.tobytes()) == roi["rgb_bytes"]
                assert sha(im.tobytes()) == roi["rgb_sha256"]
    return {"result": "PASS", "original_jpegs": 5, "rgb_rois": 10, "new_independent_physical_copies": 0}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact-zip", type=Path, required=True)
    ap.add_argument("--evidence", type=Path, default=EVIDENCE)
    ap.add_argument("--prior", type=Path, default=PRIOR)
    args = ap.parse_args()
    raw = args.prior.read_bytes()
    digest = hashlib.sha1(("blob %d" % len(raw)).encode() + bytes([0]) + raw).hexdigest()
    assert digest == PRIOR_GIT_BLOB, "immutable 13JJ source Git blob mismatch"
    proof = json.loads(args.evidence.read_text(encoding="utf-8"))
    prior = json.loads(raw)
    print(json.dumps(verify_zip(args.artifact_zip, proof, prior)))
