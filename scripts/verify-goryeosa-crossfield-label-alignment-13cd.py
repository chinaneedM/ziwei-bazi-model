#!/usr/bin/env python3
"""13CD: cross-physical-holder source printed two-field day-label negative control."""
import hashlib
import json
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CD-GORYEOSA-NAJ-WASEDA-CROSS-FIELD-DAY-HEADING-NONUNIFORMITY-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"

def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def evidence_files_and_sha(e):
    out={}
    for key,r in e["source_records"].items():
        b=(ROOT/r["path"]).read_bytes()
        blob=b"blob "+str(len(b)).encode()+bytes([0])+b
        assert hashlib.sha1(blob).hexdigest()==r["sha"], (key,"source blob changed")
        out[key]=json.loads(b)
    return out

def check(e, sources, s, ledger):
    assert e["schema"]=="TIANWEN-13CD-CROSS-HOLDING-TWO-FIELD-HEADING-ALIGNMENT-NEGATIVE-CONTROL-R1"
    assert e["issue_id"]=="TW-OPEN-0005"
    assert e["evidence_grade"]=="DERIVED_REPLAY_OF_ALREADY_DIRECT_ORIGINAL_SHA_BOUND_GLYPH_ROIS_ZERO_NEW_PIXELS"
    assert set(sources)=={"W","N_LONG","N_C","N_SEAM","HEADER"}
    w=sources["W"]
    wc=next(x for x in w["original_numeric_rois"] if x["key"]=="P23_D17_C")
    wl=next(x for x in w["original_numeric_rois"] if x["key"]=="P23_D17_LONG")
    wh=next(x for x in w["original_header_rois"] if x["key"]=="P23_D17_HEADING")
    n=sources["N_LONG"]
    nr=next(x for x in n["source_original_image_reviews"] if x["holding"]=="NAJ-282-0006-PHYSICAL51")
    nl=next(x for x in nr["day_rois"] if x["day"]==17)
    c=sources["N_C"]
    nc=next(x for x in c["paired_original_field_columns"] if x["day"]==18)
    seam=sources["N_SEAM"]
    sh=next(x for x in seam["original_rois"] if x["key"]=="NAJ_C17_D17_ORIGINAL_HEADER")
    sn=next(x for x in seam["original_rois"] if x["key"]=="NAJ_C17_NUMERAL_7570_TIGHT")
    assert wh["day"]==17 and wh["literal"]=="十七日"
    assert wc["day"]==wl["day"]==17
    assert wc["field"]=="CUMULATIVE" and wl["field"]=="LONG"
    assert Decimal(wc["value"])==Decimal(nc["cumulative_value"])==Decimal("8000.2697")
    assert Decimal(wl["value"])==Decimal("424.3711")
    assert nl["long_original"]=="四百二十四三七一一" and nr["original_image_sha256"]==seam["source"]["canvas17"]["original_jpeg_sha256"]
    assert nc["heading"]== "十八日" and nc["day"]==18
    assert sh["reading"]=="十七日" and sn["decimal"]=="7570.6624"
    assert seam["firstparty_comparison"]["original_D17_same_day_cumulative_field_fully_adjudicated"] is False
    assert sources["HEADER"]["direct_reading"]["original_D16_same_day_isolated_yingsuoji"]=="UNBOUND"
    obs=e["compared_observations"]
    assert obs=={
        "waseda_D17_header":"十七日","waseda_D17_long":"424.3711",
        "waseda_D17_yingsuoji":"8000.2697","naj_D17_long":"424.3711",
        "naj_D18_header":"十八日","naj_D18_yingsuoji":"8000.2697",
        "naj_D17_adjacent_numeral":"7570.6624",
        "naj_D17_adjacent_numeral_field_identity":"UNBOUND"}
    coords=e["positive_literal_position_matches"]
    assert len(coords)==2
    assert [(r["field"],r["waseda_printed_day"],r["naj_printed_day"],r["common_numeric"],r["observed_naj_minus_waseda_heading_offset"]) for r in coords]==[
        ("SOURCE_ORIGINAL_LONG_LANE",17,17,"424.3711",0),
        ("SOURCE_ORIGINAL_CUMULATIVE_TIGHT_LANE",17,18,"8000.2697",1)]
    for r in coords:
        assert r["naj_printed_day"]-r["waseda_printed_day"]==r["observed_naj_minus_waseda_heading_offset"]
    t=e["bounded_test"]
    assert t["same_offset_for_these_two_literal_match_coordinates"] is False
    assert t["difference_of_observed_heading_offsets"]==1
    assert t["global_column_shift_convention_proven"] is False
    assert t["all_rows_or_summer_table_proven"] is False
    assert t["does_not_uniquely_establish_historical_mechanical_row_identity"] is True
    assert t["can_equate_naj_D17_adjacency_to_printed_D17_yingsuoji"] is False
    assert t["original_waseda_D16_isolated_yingsuoji"]=="UNBOUND"
    assert t["identity_of_g893_shao_wei_and_ming1569_units"]=="UNPROVEN"
    assert t["naj_waseda_direct_copying"]=="UNPROVEN"
    assert t["historical_ancestral_D16_one_vs_two"]=="UNRESOLVED"
    assert e["source_independence"]["new_original_RGB_ROIs"]==0
    assert e["source_independence"]["new_original_jpeg_objects"]==0
    assert e["source_independence"]["new_independent_stemmatic_votes"]==0
    assert e["source_independence"]["new_registry_sources"]==0
    assert e["scope_firewall"]=={
        "new_matrix_rows":0,"new_source_entries":0,"new_genealogy_nodes":0,
        "new_genealogy_edges":0,"new_physical_witnesses":0,
        "new_independent_stemmatic_votes":0,"algorithm_reopens":0,
        "open_research_issues":11,"deterministic_product":"CLOSED"}
    a=s["historical_audit"]
    assert a["row_count"]==a["audited_row_count"]==222
    assert a["external_source_registry_total_unique_count"]==754
    assert any(x.startswith("13CD ") for x in a["current_focus"])
    assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
    assert s["invariants"]["algorithm_reopen_count"]==0
    assert ledger["binding"]["reviewed_state_version"]==s["schema_version"]
    assert ledger["binding"]["source_focus_count"]==len(a["current_focus"])
    assert ledger["binding"]["latest_research_focus_prefix"]==a["current_focus"][-1].split()[0]
    q=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
    assert q["status"]=="OPEN"
    assert E in q["source_refs"]
    assert any(x.get("revision_id")=="TW-OPEN-0005-CROSSFIELD-13CD" for x in q["history"])
    assert len([x for x in ledger["issues"] if x["status"] in {"OPEN","BLOCKED_SOURCE_ACCESS"}])==11
    return True

def main():
    e=load(E)
    assert check(e,evidence_files_and_sha(e),load(S),load(L))
    print("TIANWEN_13CD_CROSSFIELD_HEADING_BOUNDARY=PASS")

if __name__=="__main__":
    main()
