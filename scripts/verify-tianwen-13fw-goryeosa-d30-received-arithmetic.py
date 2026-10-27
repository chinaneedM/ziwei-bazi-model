#!/usr/bin/env python3
"""13FW received Goryeosa fourfen arithmetic. Not an ancient original-glyph validator."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "docs/research/TIANWEN-13FW-GORYEOSA-D30-RECEIVED-FOURFEN-ARITHMETIC-CONFLICT-R1.json"
FR = ROOT / "docs/research/TIANWEN-13FR-GK3467-BOOK6-D16-D30-DIRECT-FIELD-COLLATION-R1.json"
FV = ROOT / "docs/research/TIANWEN-13FV-NLC-D30-GUTTER-DAY-HEADER-GEOMETRY-R1.json"
DIGITS = {"〇":"0","一":"1","二":"2","三":"3","四":"4","五":"5","六":"6","七":"7","八":"8","九":"9"}
EXPECTED = [(28,"四分八八九八",8898),(29,"四分九〇六〇",9060),(30,"四分九二二二",9222),(31,"四分九三八四",9384),(32,"四分九五四六",9546)]

def check(e, fr, fv):
    assert e["schema"] == "TIANWEN-13FW-GORYEOSA-D30-RECEIVED-FOURFEN-ARITHMETIC-CONFLICT-R1"
    assert e["issue_id"] == "TW-OPEN-0005"
    source = e["source"]
    assert source["source_registry_id"] == "EXT-WIKISOURCE-GORYEOSA-V52-SHOUSHI-SOLAR-LICHENG"
    assert source["permalink_oldid"] == 2153170 and "oldid=2153170" in source["source_url"]
    assert source["original_image_acquired_this_batch"] is False
    assert source["original_image_glyph_review_this_batch"] is False
    assert source["independent_ancient_witness"] is False
    assert source["source_registry_already_contains_id"] is True
    assert e["received_table"]["columns"] == ["積日","日差加一秒六十二少","盈縮積","盈縮加分","行度"]
    rows = e["received_table"]["rows"]
    assert len(rows) == len(EXPECTED)
    nums = []
    for row,(day,glyphs,num) in zip(rows,EXPECTED):
        assert (row["day"],row["original_transcribed"],row["numeric"]) == (day,glyphs,num)
        assert glyphs.startswith("四分")
        assert int("".join(DIGITS[c] for c in glyphs[2:])) == num
        nums.append(num)
    diffs = [b-a for a,b in zip(nums,nums[1:])]
    assert diffs == e["received_table"]["neighbor_differences"] == [162]*4
    prior = e["original_prior_records"]
    assert prior["fr_original_field_literal_reported"] == fr["readings"][1]["numeric_glyph_literal"] == "九二二一四三"
    assert prior["fr_source_pdf_sha256"] == fr["original_pdf"]["pdf_sha256"]
    assert prior["fr_reading_archived_not_rewritten"] is True
    assert prior["fv_nlc_p76_original_fourfen_complete_digits"] is None
    assert prior["fr_vs_received_source_field_identity_same"] is False
    assert fv["geometry"]["day30_complete_fourfen_original_digits"] is None
    assert fv["comparison"]["nlc_day30_literal"] is None
    adj = e["adjudication"]
    assert adj["received_day30_fourfen"] == rows[2]["original_transcribed"]
    assert adj["source_original_fr_day30_prior_literal"] == "九二二一四三"
    assert adj["nlc_day30_original_complete_digits"] is None
    assert adj["historical_day30_fourfen_winner"] is None
    assert adj["source_original_erratum_authorized"] is False
    assert adj["implementation_defect_established"] is False
    assert adj["original_digit_unit_scaling"] is None
    assert adj["original_field_cross_identity"] == "UNRESOLVED"
    assert all(v==0 for k,v in e["limits"].items() if k.startswith(("new_","matrix_","algorithm_","candidate_","risk_")))
    assert e["limits"]["g893_original_six_controls"] == "OPEN"
    assert e["counts"] == {"matrix_total":222,"matrix_audited":222,"external_sources":761,"genealogy_nodes":252,"genealogy_edges":238,"issues_open_or_blocked":11,"product":"CLOSED"}
    assert not e["transmission_impact"]["edges_supported"]
    return True

if __name__ == "__main__":
    assert check(json.loads(EV.read_text(encoding="utf-8")),json.loads(FR.read_text(encoding="utf-8")),json.loads(FV.read_text(encoding="utf-8")))
    print("13FW_PASS_RECEIVED_ARITHMETIC_CONFLICT_SOURCE_GLYPH_UNADJUDICATED")
