#!/usr/bin/env python3
"""13GZ: recombine original native pixel tiles; no source-specific numeric inference."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "docs/research/TIANWEN-13GZ-D14-ORIGINAL-SOURCE-TILE-REPLAY-R1.json"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + bytes([0]) + data).hexdigest()

def check(e, output_dir=None, log_panels=False):
    assert e["schema"] == "TIANWEN-13GZ-D14-ORIGINAL-SOURCE-TILE-REPLAY-R1" and e["issue_id"] == "TW-OPEN-0005"
    assert e["grade"] == "DIRECT_REPO_PERMANENT_SOURCE_NATIVE_PIXEL_TILING_NOT_COMPLETE_ANCIENT_TEXT_COLLATION"
    prior = {}
    for x in e["preserved_snapshots"]:
        p = ROOT / x["file"]
        assert x["file"].startswith("docs/research/")
        raw = p.read_bytes()
        assert git_blob(raw) == x["git_blob_sha"]
        key = p.name[8:12]
        assert key not in prior
        prior[key] = json.loads(raw)
    assert sorted(prior) == ["13GQ", "13GR", "13GS", "13GW", "13GY"]
    s = e["provenance"]
    assert [s["embedded_page"],s["embedded_xref"]] == [74,291]
    assert s["embedded_source_size"] == [1754,1173]
    assert s["new_independent_source_witnesses"] == 0
    raw = (ROOT / s["file"]).read_bytes()
    assert git_blob(raw) == s["png_git_blob_sha"]
    assert sha(raw) == s["png_sha256"]
    im = Image.open(ROOT / s["file"]).convert("RGB")
    assert sha(im.tobytes()) == s["rgb_sha256"]
    origin = s["parent_source_xyxy"]
    assert list(im.size) == [origin[2]-origin[0],origin[3]-origin[1]] == [170,895]
    assert origin == next(x for x in prior["13GQ"]["context_panels"] if x["tag"] == "D14")["box"]
    assert s["source_pdf_sha256"] == prior["13GS"]["source"]["original_pdf_sha256"]
    assert s["rgb_sha256"] == prior["13GW"]["source"]["source_image_rgb_sha256"]
    tile_list = e["tiles"]
    expected_tags = ["FOURFEN_PROVISIONAL_PRINTED_HEADING","FIRST_UNADJUDICATED_VERTICAL_REMAINDER",
                     "SECOND_UNADJUDICATED_VERTICAL_CONTINUATION","FULL_CANDIDATE_RECONSTRUCTION",
                     "SEPARATE_CHUDU_NEIGHBOR","SEPARATE_9PX_GUTTER","D14_DATE_HEADING_CONTEXT"]
    assert [t["tag"] for t in tile_list] == expected_tags
    boxes = [t["source_xyxy"] for t in tile_list]
    g = prior["13GY"]["geometry"]
    assert boxes[0] == g["header_xyxy"]
    assert boxes[1] == g["unsegmented_remainder_xyxy"]
    assert boxes[2] == g["uninspected_lower_continuation_xyxy"]
    assert boxes[3] == prior["13GS"]["rects"][2]["box"]
    assert boxes[4] == g["neighbor_chudu_xyxy"]
    assert boxes[5] == g["intercolumn_gutter_xyxy"]
    assert boxes[6] == next(x["source_xyxy"] for x in prior["13GR"]["d14_nested_existing_source_rois"] if x["role"] == "D14_PRINTED_DAY_HEADING")
    assert boxes[0][0] == boxes[1][0] == boxes[2][0] == boxes[3][0] == 135
    assert boxes[0][2] == boxes[1][2] == boxes[2][2] == boxes[3][2] == 171
    assert boxes[0][1] == boxes[3][1] and boxes[0][3] == boxes[1][1] and boxes[1][3] == boxes[2][1] and boxes[2][3] == boxes[3][3]
    assert boxes[4][0] == boxes[5][2] and boxes[5][0] == boxes[3][2]
    assert boxes[5][2]-boxes[5][0] == 9
    geo = e["geometry"]
    assert geo["column_vertical_coverage_px"] == 497
    assert geo["three_tiles_vertical_heights"] == [117,142,238]
    assert sum(geo["three_tiles_vertical_heights"]) == boxes[3][3]-boxes[3][1]
    assert all(geo[k] is True for k in ("partition_has_no_gap_or_overlap","pixel_reassembly_must_equal_source_crop","no_resizing_no_ocr"))
    assert geo["independent_gutter_width_px"] == 9

    report = []
    crops = []
    out = Path(output_dir) if output_dir else None
    if out: out.mkdir(parents=True,exist_ok=True)
    for tile, box in zip(tile_list,boxes):
        assert origin[0]<=box[0]<box[2]<=origin[2] and origin[1]<=box[1]<box[3]<=origin[3]
        crop = im.crop((box[0]-origin[0],box[1]-origin[1],box[2]-origin[0],box[3]-origin[1]))
        crops.append(crop)
        assert crop.size == (box[2]-box[0],box[3]-box[1])
        report.append({"tag":tile["tag"],"source_native_xyxy":box,"rgb_sha256":sha(crop.tobytes()),"interpretation":tile["grade"],"certified_numeric":False})
        if out: crop.save(out / (tile["tag"].lower()+".png"))
    recon = Image.new("RGB",crops[3].size)
    offset = 0
    for crop in crops[:3]:
        recon.paste(crop,(0,offset))
        offset+=crop.height
    assert offset == crops[3].height
    assert recon.tobytes() == crops[3].tobytes()
    a = e["adjudication"]
    for k in ("historical_original_d14_complete_numeric","historical_original_d14_terminal_glyph",
              "historical_original_d9_numeric","historical_original_d30_numeric",
              "lower_first_part_literal","lower_second_part_literal",
              "source_specific_fourfen_numeric_field_identity","fourfen_chudu_mechanical_identity",
              "ancient_unit","physical_leaf","copy_layer"): assert a[k] is None,k
    assert a["first_party_high_resolution_acquired"] is False and a["single_surrogate_only"] is True
    assert a["independent_original_glyphs_certified"] == 0 and a["field_numbers_can_be_interpolated"] is False
    assert a["printed_fourfen_heading"] == "四分_PROVISIONAL" and a["printed_chudu_heading"] == "初度_PROVISIONAL"
    assert a["original_d5"] == "〇/五_UNRESOLVED" and a["g893_six"] == "OPEN" and a["prior_13EI"] == "RETRACTED"
    assert e["guards"] == {"matrix":[222,222],"sources":761,"genealogy":[252,238],
              "open_research_issues":11,"product":"CLOSED","algorithm_reopens":0,
              "candidate_collapses":0,"physical_witnesses_added":0,"transmission_edges_added":0}
    t=e["transmission_impact"]
    for k in ("edges_supported","edges_revised","edges_rejected","non_edges_added"):assert t[k]==[]
    result={"result":"13GZ_PASS_SOURCE_NATIVE_TILING_NUMERIC_STILL_NULL","source_image_rgb_sha256":sha(im.tobytes()),
            "tiles":report,"reconstruction_exact":True,"original_numeric_certified":0,
            "new_independent_witnesses":0}
    if out: (out / "13gz-source-native-tiles.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if log_panels:
        from io import BytesIO
        for k in [1,2,4]:
            bio=BytesIO()
            crops[k].save(bio,format="PNG")
            print("13GZ_NATIVE_PANEL_B64_"+tile_list[k]["tag"]+"="+base64.b64encode(bio.getvalue()).decode("ascii"),flush=True)
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--output-dir")
    p.add_argument("--log-panels",action="store_true")
    a=p.parse_args()
    result=check(json.loads(E.read_text(encoding="utf8")),a.output_dir,a.log_panels)
    print(result["result"])
