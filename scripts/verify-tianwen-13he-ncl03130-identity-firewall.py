#!/usr/bin/env python3
"""13HE: guard NCL03130 copy-layer and uploader comment claims, not glyph OCR."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "docs/research/TIANWEN-13HE-NCL03130-OLD-COPY-AND-COMMONS-UPLOAD-IDENTITY-FIREWALL-R1.json"
def gitblob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
def check(e, root=ROOT):
    assert e["schema"] == "TIANWEN-13HE-NCL03130-OLD-COPY-AND-COMMONS-UPLOAD-IDENTITY-FIREWALL-R1"
    assert e["issue_id"] == "TW-OPEN-0005"
    assert e["grade"].startswith("SECONDARY_PUBLIC_CATALOG_TRANSCRIPTION")
    assert not e["direct_primary_catalog_identity"] and not e["direct_primary_image_new"]
    for snap in e["immutable_prior_evidence"]:
        assert gitblob((root / snap["path"]).read_bytes()) == snap["blob_sha"], snap["path"]
    old = json.loads((root / e["immutable_prior_evidence"][0]["path"]).read_text(encoding="utf8"))
    photo = json.loads((root / e["immutable_prior_evidence"][1]["path"]).read_text(encoding="utf8"))
    tile = json.loads((root / e["immutable_prior_evidence"][2]["path"]).read_text(encoding="utf8"))
    assert not old["official_institutional_routes"]["provider_specific_item_url_obtained"]
    assert photo["direct_visual_glyph_reviews"][1]["visible_literal"] == "四分六六三〇"
    assert tile["adjudication"]["historical_original_d14_complete_numeric"] is None
    meta = e["commons_bibliographic_transcription"]
    assert meta["catalog_shelfmark"] == "208 03130" and meta["described_physical_booklets"] == 40
    assert meta["original_catalog_edition_claim"] == "清初葉舊鈔光緒間錢塘丁氏補鈔本"
    assert meta["accession_in_inscription"] == "光緒甲辰"
    assert meta["supplement_completion_in_inscription"] == "光緒乙巳夏"
    for key in ("which_juan_were_supplemented","juan52_copy_layer","which_pdf_page_was_original_or_supplemented"):
        assert meta[key] is None
    assert not meta["annotation_not_directly_read_from_physical_leaf"] is False
    assert not meta["first_party_item_specific_record_obtained"]
    sample=e["commons_upload_sample"]
    expected={"02":"2","08":"8","09":"9","21":"21"}
    actual={x["index"]:x for x in sample["observed_files"]}
    assert set(actual)==set(expected)
    for index,suffix in expected.items():
        x=actual[index]
        assert x["upload_comment"]=="03117_"+suffix+".pdf"
        assert x["display"]=="NCL-03130_"+index+" 高麗史.pdf"
        assert x["source_url"].startswith("https://commons.wikimedia.org/wiki/File:NCL-03130_"+index+"_")
        assert x["observed_pages"]>0
    assert sample["file_series_count_seen_in_commons_category"]==24
    assert sample["twenty_four_digital_files_not_same_as_forty_physical_booklets"]
    for key in ("exact_mislabel_cause",):
        assert sample[key] is None
    assert not sample["pdf_content_replacement_proven"]
    assert not sample["pdf_to_physical_book_fascicle_mapping_proven"]
    sc=e["day14_scope"]
    assert sc["current_ncl_source_pdf_sha256"]==old["existing_source_binding"]["old_original_pdf_sha256"]
    assert sc["permanent_native_d14_context_png_git_blob_sha"]==old["existing_source_binding"]["joint_context_git_blob_sha"]
    for key in ("NCL_03130_09_p74_D14_full_original_literal","NCL_03130_09_p74_D14_terminal_original","NCL_page74_earlyQing_or_Guangxu_supplement","D9","D30","ancient_unit","fourfen_chudu_mechanical_equivalence"):
        assert sc[key] is None, key
    assert sc["NIKH_photo4_D14_literal"] == "四分六六三〇" and sc["NIKH_is_a_separate_scoped_photo"]
    assert sc["D5"]=="〇/五_UNRESOLVED" and sc["G893_six"]=="OPEN"
    assert sc["prior_13EI"]=="RETRACTED" and sc["new_full_original_glyphs"]==0
    assert e["graph_scope"]["new_witnesses"]==e["graph_scope"]["new_transmission_edges"]==0
    assert e["invariants"]=={"matrix":[222,222],"sources":761,"graph":[252,238],"open_issues":11,"chart":"CLOSED","algorithm_reopens":0,"candidate_collapses":0}
    state=json.loads((root/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf8"))
    assert any(str(s).startswith("13HE ") for s in state["historical_audit"]["current_focus"])
    ledger=json.loads((root/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf8"))
    issue=next(i for i in ledger["issues"] if i["id"]=="TW-OPEN-0005")
    assert str(E.relative_to(root)) in issue["source_refs"]
    assert state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
    return True
if __name__ == "__main__":
    print("TIANWEN_13HE_NCL03130_IDENTITY_FIREWALL_PASS" if check(json.loads(E.read_text(encoding="utf8"))) else "FAIL")
