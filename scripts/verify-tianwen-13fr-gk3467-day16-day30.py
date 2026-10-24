#!/usr/bin/env python3
"""13FR: immutable source-bound collation gates, optional direct PDF pixel replay."""
import argparse
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "docs/research/TIANWEN-13FR-GK3467-BOOK6-D16-D30-DIRECT-FIELD-COLLATION-R1.json"
def sha(data):
    return hashlib.sha256(data).hexdigest()
def check(data, pdf_path=None):
    assert data["schema"] == "TIANWEN-13FR-GK3467-BOOK6-D16-D30-DIRECT-FIELD-COLLATION-R1"
    assert data["issue_id"] == "TW-OPEN-0005"
    src=data["original_pdf"]
    assert (src["subcatalog"],src["digital_volume"],src["physical_book"],src["work_juan"],src["pdf_pages"])==("GK03467_04","0001",6,52,53)
    assert src["pdf_sha256"] == "b75009805dae9ccc22797c005bd5f32c7870a192945b503f6b3af3fbf14e1386"
    readings=data["readings"]
    assert len(readings)==2
    expect={16:(15,"十六日","六九五四"),30:(17,"三十日","九二二一四三")}
    for r in readings:
        assert r["day"] in expect
        page,heading,literal=expect[r["day"]]
        assert (r["pdf_page_one_based"],r["heading_literal"],r["numeric_glyph_literal"])==(page,heading,literal)
        assert r["printed_field"]=="四分"
        assert r["reading_grade"]=="DIRECT_ORIGINAL_NATIVE_PIXEL_BOUNDED_HEADING_AND_FOURFEN_LANE"
        assert r["native_wh"]==[2432,2064]
        x0,y0,x1,y1=r["roi_xyxy"]
        assert 0<=x0<x1<=2432 and 0<=y0<y1<=2064
        for key in ("embedded_image_sha256","decoded_rgb_sha256","roi_rgb_sha256","roi_png_sha256"):
            assert len(r[key])==64 and all(c in "0123456789abcdef" for c in r[key])
        assert r["ancient_folio_number"] is None
    assert [r["day"] for r in readings]==[16,30]
    limits=data["adjudication"]
    for key in ("day16_historical_winner","day30_historical_winner","historical_numeric_scaling","physical_copy_independence_vs_NLC_NIKH","impression_date","season_labels_for_day16_day30","original_D9_NLC","source_book52_same_as_NIKH_GK5553"):
        assert limits[key] is None
    assert limits["original_column_labels_to_modern_unit_bridge"]=="UNPROVEN"
    assert limits["g893_six_controls"]=="OPEN" and not limits["full_work52_line_by_line_collation"]
    assert limits["day5_opposing_originals"]=={"NLC":"四分〇一七二","NIKH":"四分五一七二","GK3467":"四分五一七二","winner":None}
    assert not data["transmission_impact"]["edges_supported"]
    impact=data["impact"]
    assert (impact["matrix_total"],impact["matrix_audited"],impact["registry_total"],impact["open_issues"])==(222,222,761,11)
    assert impact["product"]=="CLOSED" and impact["algorithm_reopens"]==impact["candidate_collapses"]==0
    if pdf_path is not None:
        from PIL import Image
        import fitz
        from io import BytesIO
        raw=Path(pdf_path).read_bytes()
        assert sha(raw)==src["pdf_sha256"]
        doc=fitz.open(stream=raw,filetype="pdf")
        assert len(doc)==src["pdf_pages"]
        for r in readings:
            page=doc[r["pdf_page_one_based"]-1]
            imgs=page.get_images(full=True)
            assert len(imgs)==1
            assert imgs[0][0]==r["original_image_xref"]
            encoded=doc.extract_image(imgs[0][0])
            assert encoded["ext"]==r["embedded_image_format"]=="png"
            assert sha(encoded["image"])==r["embedded_image_sha256"]
            im=Image.open(BytesIO(encoded["image"])).convert("RGB")
            assert im.size==tuple(r["native_wh"])
            assert sha(im.tobytes())==r["decoded_rgb_sha256"]
            roi=im.crop(tuple(r["roi_xyxy"]))
            assert sha(roi.tobytes())==r["roi_rgb_sha256"]
        doc.close()
    return True
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--pdf",help="Optional complete, hash-pinned GK03467_04-0001.pdf")
    args=parser.parse_args()
    assert check(json.loads(E.read_text(encoding="utf-8")),args.pdf)
    print("13FR_PASS_DIRECT_D16_D30_SOURCE_BOUND_PIXELS_NO_UNIT_OR_WINNER_INFERENCE")
