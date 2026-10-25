#!/usr/bin/env python3
"""13HA: source-scoped winter and summer D14 cannot be conflated or promoted to NCL original."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13HA-GORYEOSA-DOUBLE-D14-SEASONAL-ROW-KEY-FIREWALL-R1.json"

def blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+bytes([0])+raw).hexdigest()

def check(x):
    assert x["schema"]=="TIANWEN-13HA-GORYEOSA-DOUBLE-D14-SEASONAL-ROW-KEY-FIREWALL-R1" and x["issue_id"]=="TW-OPEN-0005"
    assert x["grade"]=="EXACT_FIRSTPARTY_MODERN_RECEIVED_SEASONAL_ROW_KEY_CONTROL_NOT_NEW_SOURCE_OR_ORIGINAL_PHOTO_GLYPH"
    src=x["first_party_received"]
    registry=(ROOT/src["existing_registry_file"]).read_bytes()
    assert blob(registry)==src["existing_registry_blob_sha"]
    found=[z for z in json.loads(registry)["sources"] if z["source_id"]==src["source_id_existing"]]
    assert len(found)==1 and "kr_052_0010_0010_0020" in found[0]["url"]
    assert src["source_hanja_text_not_original_photograph"] is True
    assert src["known_source_gallery_index4_JPEG_SHA256"]=="63a45c4dc223e360267659acd2a6900767aaf10d82db1bf43724463edb8ddc0a"
    assert src["gallery_index4_original_target_folio_bound"] is False
    assert src["gallery_index4_d14_original_glyph_review_done"] is False
    pri={}
    for j in x["source_snapshots"]:
        assert j["file"].startswith("docs/research/")
        raw=(ROOT/j["file"]).read_bytes()
        assert blob(raw)==j["git_blob_sha"]
        pri[Path(j["file"]).name[8:12]]=json.loads(raw)
    assert sorted(pri)==["12YZ","13FG","13GZ"]
    assert pri["12YZ"]["modern_received_rows"][0]["short_raw"]=="五分一九九〇"
    assert pri["13FG"]["source_image_recovery"]["captured_modern_index_to_exact_sha256"]["4"]==src["known_source_gallery_index4_JPEG_SHA256"]
    assert pri["13GZ"]["adjudication"]["historical_original_d14_complete_numeric"] is None
    assert pri["13GZ"]["adjudication"]["historical_original_d14_terminal_glyph"] is None
    tables=x["seasonal_tables"]
    assert len(tables)==2 and [q["id"] for q in tables]==["WINTER_EARLY_YING_LATE_SUO","SUMMER_EARLY_SUO_LATE_YING"]
    winter,summer=tables
    assert winter["declared_header"]=="大陽冬至前後二象盈初縮末限"
    assert summer["declared_header"]=="大陽夏至前後二象縮初盈末限"
    assert winter["first_numeric_column_label"]=="日差加一秒八十六少"
    assert summer["first_numeric_column_label"]=="日差加一秒六十二少"
    assert [q["day14"]["day_heading"] for q in tables]==["十四日","十四日"]
    for q in tables:
        assert [q["day12"]["day_heading"],q["day13"]["day_heading"]]==["十二日","十三日"]
    assert [winter[z]["first_field"] for z in ("day12","day13","day14")]==["五分一六一八","五分一八〇四","五分一九九〇"]
    assert [summer[z]["first_field"] for z in ("day12","day13","day14")]==["四分六三〇六","四分六四六八","四分六六三〇"]
    assert [winter["day14"][k] for k in ("second_field","third_field","fourth_field")]==["四百四十〇〇二三九","六千六百九十五八一三六","一度〇四四〇〇二"]
    assert [summer["day14"][k] for k in ("second_field","third_field","fourth_field")]==["四百二十一二六六三","六千三百七十八二七一二","初度九十五七八七四"]
    a=x["normalized_selector"]
    assert a["key_fields"]==["work","juan","section","seasonal_heading","day_heading","column_role"]
    assert [a[k] for k in ("work","juan","section","day_heading")]==["高麗史",52,"授時曆立成","十四日"]
    assert a["forbidden_selector"]==["work","juan","day_heading"] and a["distinct_seasonal_keys"]==2
    assert a["summer_received_first_field"]==summer["day14"]["first_field"]
    assert a["winter_received_first_field"]==winter["day14"]["first_field"]
    assert a["summer_received_first_field"]!=a["winter_received_first_field"]
    for k in ("same_first_party_page_two_distinct_rows",):assert a[k] is True
    for k in ("cannot_promote_summer_received_day14_to_NCL_original","cannot_promote_winter_received_day14_to_NCL_original","no_ancient_mechanical_equivalence_claim","no_ancient_unit_normalization_claim"):
        assert a[k] is True
    assert a["source_witness_multiplication"]==0
    e=x["original_evidence_firewall"]
    for k in ("NCL_p74_source_original_D14_complete_field","NCL_p74_D14_terminal_original_glyph","NCL_p74_D9_field","NCL_p76_D30_field","NIKH_source_photo_index4_exact_day14_glyphs"):
        assert e[k] is None,k
    assert e["same_physical_copy_or_impression_proven"] is False
    assert e["old_D5"]=="〇/五_UNRESOLVED" and e["G893_six"]=="OPEN" and e["old_13EI"]=="RETRACTED"
    assert e["chart"]=="CLOSED"
    assert all(e[k]==0 for k in ("algorithm_reopens","candidate_collapses","sources_added","matrix_rows_added","graph_edges_added","physical_copies_added"))
    assert x["counters"]=={"matrix":[222,222],"sources":761,"genealogy":[252,238],"open_issues":11}
    assert all(x["transmission_impact"][k]==[] for k in ("edges_supported","edges_revised","edges_rejected","non_edges_added"))
    return True
if __name__=="__main__":
    assert check(json.loads(E.read_text(encoding="utf8")))
    print("13HA_PASS_TWO_SEASONAL_DAY14_KEYS_NO_ORIGINAL_NUMERIC_PROMOTION")
