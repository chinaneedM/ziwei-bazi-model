#!/usr/bin/env python3
"""13FU: NLC day16 source-original 四分六九五四 field; no D30 inference."""
import argparse
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13FU-NLC-D16-DIRECT-FOURFEN-ORIGINAL-GLYPHS-R1.json"
FR=ROOT/"docs/research/TIANWEN-13FR-GK3467-BOOK6-D16-D30-DIRECT-FIELD-COLLATION-R1.json"
FT=ROOT/"docs/research/TIANWEN-13FT-NLC-GK3467-D16-D30-ORIGINAL-COUNTERPART-LOCATORS-R1.json"
def digest(b):return hashlib.sha256(b).hexdigest()
def check(e,fr,ft,archive=None):
    assert e["schema"]=="TIANWEN-13FU-NLC-D16-DIRECT-FOURFEN-ORIGINAL-GLYPHS-R1"
    assert e["issue_id"]=="TW-OPEN-0005" and e["grade"]=="DIRECT_ORIGINAL_IMAGE_NATIVE_RGB_SINGLE_FIELD_GLYPHS_NO_OCR"
    s=e["source"];f=e["original_field"];cross=e["cross_original"];lim=e["limits"]
    assert s["digital_page_one_based"]==75 and s["original_image"]=="original-p075.png"
    assert (s["archived_run"],s["archived_artifact"])==(39938606876,12494518841)
    assert s["source_sha256"]=="3c2a5621fb3f4eabc593020bcde12a38f6ecdae2842940dec12d5a3a56afd32e"
    assert s["original_image_sha256"]=="059821b008f41c1cdf11bf0daab89de01b44dc5ffee1263e569decb567f76458"
    assert s["native_rgb_sha256"]=="f90eb6e5be96ae16408833fb2722db9b90413347a8acd733efbd3836d7f5f534"
    assert s["native_rgb_size"]==[1305,878]
    assert s["physical_copy_identity"] is None and s["physical_impression_date"] is None and s["ancient_folio_number"] is None
    assert f["day"]==16 and f["source_printed_day_heading"]=="十六日"
    assert (f["source_printed_field"],f["literal_digits"],f["complete_field_original_literal"])==("四分","六九五四","四分六九五四")
    assert f["roi_xyxy"]==[831,419,854,611] and (f["native_crop_width"],f["native_crop_height"])==(23,192)
    assert f["roi_rgb_sha256"]=="6251aba362676e55b4afdab8161727f465afbebacc829bead212cf6b79807546"
    assert f["roi_png_sha256"]=="3f6cc5c0de226255b75b6e5e32a4139735e7a401bfdafbe71496a7d309975264"
    assert f["machine_unit_value"] is None
    orig=next(x for x in fr["readings"] if x["day"]==16)
    assert orig["printed_field"]=="四分" and orig["numeric_glyph_literal"]=="六九五四" and orig["pdf_page_one_based"]==15
    assert cross["gk3467_original_pdf_sha256"]==fr["original_pdf"]["pdf_sha256"]
    assert (cross["gk3467_original"],cross["gk3467_literal_digits"])==(str(FR.relative_to(ROOT)),"六九五四")
    assert cross["comparison"]=="SAME_GLYPH_STRING_TWO_DIGITAL_SOURCE_GROUPS_NOT_CERTIFIED_INDEPENDENT_ORIGINAL_PHYSICAL_COPIES"
    assert cross["new_physically_authenticated_witnesses"]==0 and cross["historical_numeric_units"] is None and cross["transmission_edge_claim"] is None
    t16=next(x for x in ft["targets"] if x["day"]==16)
    assert (t16["nlc_page"],t16["png_sha256"],t16["rgb_sha256"])==(75,s["original_image_sha256"],s["native_rgb_sha256"])
    assert t16["nlc_fourfen_full_glyph_literal"] is None # Historical snapshot is immutable
    assert lim["nlc_day30_full_fourfen_literal"] is None and lim["nlc_day30_page_locator"]==76
    assert lim["nlc_day9_original_fourfen"] is None
    assert lim["day5_opposing_origins"]=={"NLC":"四分〇一七二","NIKH":"四分五一七二","GK3467":"四分五一七二","winner":None}
    for key in ("historical_winner_day16","historical_winner_day30","historical_scaling","season_day_mapping","impression_relation_to_gk3467"):
        assert lim[key] is None
    assert lim["chudu_fourfen_unit_bridge"]=="UNPROVEN" and lim["g893_six_original_controls"]=="OPEN"
    assert lim["no_modern_decimal_normalization"] is True
    assert (lim["algorithm_reopens"],lim["candidate_collapses"],lim["new_source_registry_entries"])==(0,0,0)
    assert not e["transmission_impact"]["edges_supported"]
    assert e["counts"]=={"matrix_total":222,"matrix_audited":222,"external_sources":761,"genealogy_nodes":252,"genealogy_edges":238,"issues_open_or_blocked":11,"product":"CLOSED"}
    if archive:
        from PIL import Image
        from io import BytesIO
        import zipfile
        with zipfile.ZipFile(archive) as z:
            manifest=json.loads(z.read("manifest.json"))
            assert manifest["source_sha256_expected"]==s["source_sha256"]
            page=next(x for x in manifest["pages"] if x["page"]==75)
            img=z.read(s["original_image"])
            assert digest(img)==s["original_image_sha256"]==page["png_sha256"]
            native=Image.open(BytesIO(img)).convert("RGB")
            assert list(native.size)==s["native_rgb_size"]
            assert digest(native.tobytes())==s["native_rgb_sha256"]==page["rgb_sha256"]
            crop=native.crop(tuple(f["roi_xyxy"]))
            assert crop.size==(f["native_crop_width"],f["native_crop_height"])
            assert digest(crop.tobytes())==f["roi_rgb_sha256"]
            b=BytesIO();crop.save(b,format="PNG")
            assert digest(b.getvalue())==f["roi_png_sha256"]
    return True
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--nlc-archive")
    a=p.parse_args()
    assert check(json.loads(E.read_text("utf-8")),json.loads(FR.read_text("utf-8")),json.loads(FT.read_text("utf-8")),a.nlc_archive)
    print("13FU_PASS_NLC_ORIGINAL_DAY16_FOURFEN_NO_DAY30_OR_HISTORY_COLLAPSE")
