#!/usr/bin/env python3
"""13FV same-page p76 native gutter geometry, no D30 source numeric inference."""
import argparse
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13FV-NLC-D30-GUTTER-DAY-HEADER-GEOMETRY-R1.json"
FT=ROOT/"docs/research/TIANWEN-13FT-NLC-GK3467-D16-D30-ORIGINAL-COUNTERPART-LOCATORS-R1.json"
FU=ROOT/"docs/research/TIANWEN-13FU-NLC-D16-DIRECT-FOURFEN-ORIGINAL-GLYPHS-R1.json"
FR=ROOT/"docs/research/TIANWEN-13FR-GK3467-BOOK6-D16-D30-DIRECT-FIELD-COLLATION-R1.json"
EXPECTED={
"DAY_30_RIGHT_OF_FOLD":([553,155,608,280],"e1852eb19d920b9be5d3b55330ca272a00cffbcdadfc8984d11f96535a6b3b88"),
"DAY_31_LEFT_OF_FOLD":([456,155,526,280],"83c55572704e96fb52ea9ae41026a05de2cfcf3a2e4e22fec0eb545161a87fbf"),
"DAY_29_RIGHT_NEIGHBOR":([638,155,700,280],"ab913b1962933932461d97dfc0446de6caf91c22a1ae20e0d276f240415bebd4"),
"FOLD_BOUNDARY":([527,150,550,803],"bfc8303641d1f7ad07c585201d8e9e79ad6592de8e5157cb7682b6bf4ff2db45"),
"SEAM_ADJACENT_CANDIDATE_STRIP":([551,405,592,790],"4e823fa944a65f6782b03be81412a976a30fe552ec93d5932485f613c674abf2"),
"NEXT_CANDIDATE_STRIP":([592,405,637,790],"141dc3a378a7ece0649ec22311be84026aa31cae41b92e7b052d082e167bbbed"),
"TABLE_TOP_CONTEXT":([550,403,637,606],"8bc0bc1c43fc0acc9ee9cb9768ec0b476e115b7da62c5396aaf666a25cbbefd7")
}
def digest(b):return hashlib.sha256(b).hexdigest()
def check(e,ft,fu,fr,archive_path=None):
    assert e["schema"]=="TIANWEN-13FV-NLC-D30-GUTTER-DAY-HEADER-GEOMETRY-R1"
    assert e["issue_id"]=="TW-OPEN-0005"
    s=e["source"]
    assert s["archived_original_action"]==39938606876 and s["artifact_id"]==12494518841
    assert s["original_png_filename"]=="original-p076.png" and s["original_scan_page"]==76
    assert s["png_sha256"]=="ce4eb8b044868fe48bb41fe5453b10fa7bbd949d8fdf2c8e31037f8b89f32fad"
    assert s["native_rgb_sha256"]=="cd8e71f9a048323d58475576548dc0c18d4cc8d0fe26cc0eb3af50feb26a5c07"
    assert s["native_wh"]==[1305,875]
    assert s["source_pdf_sha256"]=="3c2a5621fb3f4eabc593020bcde12a38f6ecdae2842940dec12d5a3a56afd32e"
    assert s["physical_copy_identity"] is None and s["old_leaf_number"] is None
    assert len(e["regions"])==len(EXPECTED)==7
    entries={r["label"]:r for r in e["regions"]}
    assert set(entries)==set(EXPECTED)
    for label,(xyxy,sha) in EXPECTED.items():
        r=entries[label]
        assert (r["rect"],r["sha256_rgb"])==(xyxy,sha)
        x0,y0,x1,y1=xyxy
        assert 0<=x0<x1<=1305 and 0<=y0<y1<=875
    for name,day,literal in [("DAY_30_RIGHT_OF_FOLD",30,"三十日"),("DAY_31_LEFT_OF_FOLD",31,"三十一日"),("DAY_29_RIGHT_NEIGHBOR",29,"二十九日")]:
        r=entries[name]
        assert (r["day"],r["literal"])==(day,literal)
        assert r["role"] in ("POSITIVE_DAY_HEADER_ONLY","NEIGHBOR_COUNTEREXAMPLE_HEADER_ONLY")
    assert entries["FOLD_BOUNDARY"]["role"]=="PAGE_SEAM_GEOMETRY_NOT_A_NUMERIC_FIELD"
    for name in ("SEAM_ADJACENT_CANDIDATE_STRIP","NEXT_CANDIDATE_STRIP"):
        assert entries[name]["role"]=="NUMERIC_NEIGHBOR_REGION_UNBOUND_FIELD"
    a,b=[entries[n]["rect"] for n in ("SEAM_ADJACENT_CANDIDATE_STRIP","NEXT_CANDIDATE_STRIP")]
    assert a[2]==b[0] and a[1]==b[1] and a[3]==b[3]
    g=e["geometry"]
    assert (g["day30_day_header_original"],g["day30_heading_certified"])==("三十日",True)
    assert g["day31_region"]=="LEFT_OF_FOLD" and g["day30_region"]=="RIGHT_OF_FOLD" and g["day29_region"]=="FURTHER_RIGHT"
    assert g["day30_fourfen_source_specific_field_locator"] is None and g["day30_complete_fourfen_original_digits"] is None
    assert g["close_candidate_spatial_proximity_is_not_column_identity"] and not g["original_full_line_by_line_page_collation"]
    match=next(x for x in ft["targets"] if x["day"]==30)
    assert (match["nlc_page"],match["png_sha256"],match["rgb_sha256"])==(76,s["png_sha256"],s["native_rgb_sha256"])
    assert match["nlc_fourfen_full_glyph_literal"] is None
    assert fu["limits"]["nlc_day30_full_fourfen_literal"] is None
    assert fr["readings"][1]["numeric_glyph_literal"]=="九二二一四三"
    c=e["comparison"]
    assert c["gk_day30_literal"]=="九二二一四三" and c["nlc_day30_literal"] is None and c["copy_relationship"] is None
    assert c["original_numeric_unit_bridge"]=="UNPROVEN" and c["g893_six_controls"]=="OPEN"
    assert c["nlc_day5_opposed"]=={"NLC":"〇一七二","NIKH":"五一七二","GK3467":"五一七二","winner":None}
    assert c["nlc_day9"] is None and c["no_historic_winner"] is True
    assert e["limits"]=={"new_original_ancient_witnesses":0,"new_source_registry_records":0,"new_graph_nodes":0,"new_graph_edges":0,"algorithms_reopened":0,"candidates_collapsed":0,"prior_13FT_13FU_records_immutable":True}
    assert not e["transmission_impact"]["edges_supported"]
    assert e["counts"]=={"matrix_total":222,"matrix_audited":222,"external_sources":761,"genealogy_nodes":252,"genealogy_edges":238,"issues_open_or_blocked":11,"product":"CLOSED"}
    if archive_path:
        import zipfile
        from io import BytesIO
        from PIL import Image
        with zipfile.ZipFile(archive_path) as z:
            manifest=json.loads(z.read("manifest.json"))
            assert manifest["source_sha256_expected"]==s["source_pdf_sha256"]
            p76=next(x for x in manifest["pages"] if x["page"]==76)
            data=z.read(s["original_png_filename"])
            assert digest(data)==s["png_sha256"]==p76["png_sha256"]
            im=Image.open(BytesIO(data)).convert("RGB")
            assert list(im.size)==s["native_wh"]
            assert digest(im.tobytes())==s["native_rgb_sha256"]==p76["rgb_sha256"]
            for name,(rect,sha) in EXPECTED.items():
                assert digest(im.crop(tuple(rect)).tobytes())==sha
    return True
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--nlc-archive");a=p.parse_args()
    assert check(json.loads(E.read_text("utf-8")),json.loads(FT.read_text("utf-8")),json.loads(FU.read_text("utf-8")),json.loads(FR.read_text("utf-8")),a.nlc_archive)
    print("13FV_PASS_SOURCE_NATIVE_D30_GUTTER_DAY_BOUNDARY_NO_FOURFEN_WINNER")
