#!/usr/bin/env python3
"""13JO offline ZIP to original JPEG/RGB pixel ROI SHA replay; no historical numeric voting."""
import argparse, hashlib, io, json, re, zipfile
from pathlib import Path
from PIL import Image
ARTIFACT_SHA="74feace6f761f89ff8eaaf7528618d1a5368e5cbfb5cd5c0f5d961841cafdef5"
def sha(blob): return hashlib.sha256(blob).hexdigest()
def generated_box(kind,w,h):
    if kind=="heading_strip":return [round(w*.68),round(h*.12),w-20,round(h*.75)]
    if kind=="body_field":return [round(w*.07),round(h*.20),round(w*.60),round(h*.78)]
    raise ValueError(kind)
def verify_manifest(d):
    assert d["schema"]=="TIANWEN-13JO-SNU-GK5553-13JL-ORIGINAL-JPEG-PIXEL-ROI-REPLAY-R1"
    assert d["source"]["downloaded_artifact_zip_sha256"]==ARTIFACT_SHA
    assert len(d["original_images"])==6 and len({x["digital_volume"] for x in d["original_images"]})==6
    assert d["replay_result"]["new_independent_physical_witness_votes"]==d["replay_result"]["new_historical_numeric_target_winners"]==d["replay_result"]["algorithm_reopens"]==0
    assert d["adjudication"]["physical_ordinal_binding"]=="UNPROVEN"
    for item in d["original_images"]:
        assert re.fullmatch(r"\d{4}",item["digital_volume"]) and re.fullmatch(r"\d{3}[ab]",item["digital_page"])
        assert item["artifact_member"]=="gk5553-%s-%s-source-original.jpg"%(item["digital_volume"],item["digital_page"])
        w,h=item["native_pixel_size"]
        assert w>=1000 and h==2000
        assert len(item["original_rgb_rois"])==2
        assert {r["name"] for r in item["original_rgb_rois"]}=={"heading_strip","body_field"}
        assert re.fullmatch(r"[0-9a-f]{64}",item["jpeg_sha256"]) and re.fullmatch(r"[0-9a-f]{64}",item["native_rgb_sha256"])
        for roi in item["original_rgb_rois"]:
            xy=roi["xyxy"]
            assert len(xy)==4 and all(type(v) is int for v in xy)
            assert 0<=xy[0]<xy[2]<=w and 0<=xy[1]<xy[3]<=h
            assert xy==generated_box(roi["name"],w,h)
            assert roi["pixel_size"]==[xy[2]-xy[0],xy[3]-xy[1]]
            assert roi["pixel_size"][0]>=250 and roi["pixel_size"][1]>=500
            assert roi["pixel_format"]=="RGB" and roi["rgb_bytes"]==3*roi["pixel_size"][0]*roi["pixel_size"][1]
            assert re.fullmatch(r"[0-9a-f]{64}",roi["rgb_sha256"])
def verify_archive(archive,d):
    verify_manifest(d)
    assert sha(archive.read_bytes())==ARTIFACT_SHA,"GitHub archive digest mismatch"
    pages=d["original_images"]
    with zipfile.ZipFile(archive) as zipf:
        assert set(zipf.namelist())=={"source-jpeg-intake.json"}|{x["artifact_member"] for x in pages}
        for item in pages:
            raw=zipf.read(item["artifact_member"])
            assert len(raw)==item["jpeg_bytes"] and sha(raw)==item["jpeg_sha256"]
            assert raw.startswith(bytes.fromhex("ffd8ff")) and raw.endswith(bytes.fromhex("ffd9"))
            rgb=Image.open(io.BytesIO(raw)).convert("RGB")
            assert list(rgb.size)==item["native_pixel_size"] and sha(rgb.tobytes())==item["native_rgb_sha256"]
            for roi in item["original_rgb_rois"]:
                sub=rgb.crop(tuple(roi["xyxy"]))
                assert len(sub.tobytes())==roi["rgb_bytes"]
                assert sha(sub.tobytes())==roi["rgb_sha256"]
    return {"result":"PASS","source_jpegs":len(pages),"verified_rois":sum(len(x["original_rgb_rois"]) for x in pages),"independent_copies":0,"numeric_winners":0}
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--artifact-zip",type=Path,required=True)
    ap.add_argument("--evidence",type=Path,default=Path(__file__).resolve().parents[1]/"docs/research/TIANWEN-13JO-GK5553-13JL-ORIGINAL-JPEG-PIXEL-ROI-REPLAY-R1.json")
    args=ap.parse_args()
    print(json.dumps(verify_archive(args.artifact_zip,json.loads(args.evidence.read_text(encoding="utf-8")))))
