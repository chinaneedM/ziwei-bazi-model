#!/usr/bin/env python3
"""13FT: exact original NLC page counterparts to 13FR GK3467 D16/D30."""
import argparse
import copy
import hashlib
import json
import zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "docs/research/TIANWEN-13FT-NLC-GK3467-D16-D30-ORIGINAL-COUNTERPART-LOCATORS-R1.json"
FR = ROOT / "docs/research/TIANWEN-13FR-GK3467-BOOK6-D16-D30-DIRECT-FIELD-COLLATION-R1.json"
EXPECTED = {
    16: (75, "original-p075.png", "059821b008f41c1cdf11bf0daab89de01b44dc5ffee1263e569decb567f76458", "f90eb6e5be96ae16408833fb2722db9b90413347a8acd733efbd3836d7f5f534", [785,160,909,810], "5a4a6d0775e23d2da1395d5266264c0bf9fbc795a696078e12f3f2dba82821d0", 15, "十六日", "六九五四"),
    30: (76, "original-p076.png", "ce4eb8b044868fe48bb41fe5453b10fa7bbd949d8fdf2c8e31037f8b89f32fad", "cd8e71f9a048323d58475576548dc0c18d4cc8d0fe26cc0eb3af50feb26a5c07", [525,160,642,810], "bb1a267f001935e49dea9b9d6a42b95417e3d47fe72afe2fb3498b890a03724e", 17, "三十日", "九二二一四三")
}
def digest(b): return hashlib.sha256(b).hexdigest()
def check(e, fr, archive_path=None):
    assert e["schema"] == "TIANWEN-13FT-NLC-GK3467-D16-D30-ORIGINAL-COUNTERPART-LOCATORS-R1"
    assert e["issue_id"] == "TW-OPEN-0005"
    assert e["review"] == "DIRECT_ORIGINAL_PIXELS_BOUNDED_DAY_HEADER_ONLY"
    nlc = e["source_nlc"]
    assert (nlc["archived_action_run"],nlc["archived_artifact_id"]) == (39938606876,12494518841)
    assert nlc["archived_pages_are_one_digital_pdf_not_distinct_originals"] is True
    assert nlc["full_pdf_expected_sha256"] == "3c2a5621fb3f4eabc593020bcde12a38f6ecdae2842940dec12d5a3a56afd32e"
    assert e["source_gk3467"]["source_pdf_sha256"] == fr["original_pdf"]["pdf_sha256"]
    assert len(e["targets"]) == 2
    assert [x["day"] for x in e["targets"]] == [16,30]
    fr_by_day = {x["day"]:x for x in fr["readings"]}
    if archive_path:
        from PIL import Image
        from io import BytesIO
        zip_ref=zipfile.ZipFile(archive_path)
        manifest=json.loads(zip_ref.read("manifest.json"))
        assert manifest["schema"] == nlc["manifest_schema"]
        assert manifest["source_sha256_expected"] == nlc["full_pdf_expected_sha256"]
        source_pages={x["page"]:x for x in manifest["pages"]}
    for r in e["targets"]:
        day = r["day"]
        (page,name,png_sha,rgb_sha,rect,roi_sha,gk_page,title,literal) = EXPECTED[day]
        assert (r["nlc_page"],r["filename"],r["png_sha256"],r["rgb_sha256"]) == (page,name,png_sha,rgb_sha)
        assert r["roi_xyxy"] == rect and r["roi_rgb_sha256"] == roi_sha
        assert (r["gk_pdf_page"],r["heading"],r["gk_original_literal"]) == (gk_page,title,literal)
        assert (fr_by_day[day]["pdf_page_one_based"],fr_by_day[day]["heading_literal"],fr_by_day[day]["numeric_glyph_literal"]) == (gk_page,title,literal)
        assert r["nlc_fourfen_full_glyph_literal"] is None and r["nlc_ancient_folio"] is None
        assert r["field_identity_grade"] == "HEADER_AND_DAY_COUNTERPART_ONLY_NOT_FULL_FIELD_COLLATION"
        assert r["source_original_copy_identity"] is None
        if archive_path:
            png=zip_ref.read(name)
            assert digest(png) == png_sha == source_pages[page]["png_sha256"]
            im=Image.open(BytesIO(png)).convert("RGB")
            assert list(im.size) == r["wh"]
            assert digest(im.tobytes()) == rgb_sha == source_pages[page]["rgb_sha256"]
            assert digest(im.crop(tuple(rect)).tobytes()) == roi_sha
    d=e["decisions"]
    for key in ("nlc_d16_fourfen_complete","nlc_d30_fourfen_complete","day16_final_historical_winner","day30_final_historical_winner","source_impression_identity_equality","season_mapping","nlc_d9_fourfen"):
        assert d[key] is None
    assert d["technical_unit_fourfen_chudu_bridge"] == "UNPROVEN"
    assert d["g893_six_primary_controls"] == "OPEN"
    assert d["day5_disagreement_preserved"] == {"NLC":"〇一七二","NIKH":"五一七二","GK3467":"五一七二","winner":None}
    assert (d["counterpart_headers_confirmed"],d["new_ancient_copy_votes"],d["algorithms_reopened"],d["candidates_collapsed"]) == (2,0,0,0)
    assert not e["transmission_impact"]["edges_supported"]
    assert e["counts"] == {"matrix_audited":222,"matrix_total":222,"registry_root":647,"registry_extensions":114,"registry_total":761,"genealogy_nodes":252,"genealogy_edges":238,"risk_issues_open_or_blocked":11,"product":"CLOSED"}
    return True
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--nlc-archive")
    a=p.parse_args()
    assert check(json.loads(E.read_text(encoding="utf-8")),json.loads(FR.read_text(encoding="utf-8")),a.nlc_archive)
    print("13FT_PASS_NLC_D16_D30_BOUNDED_COUNTERPARTS_NO_NUMERIC_WINNER")
