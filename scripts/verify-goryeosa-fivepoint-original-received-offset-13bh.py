#!/usr/bin/env python3
"""13BH: replay five local received/original cumulative index alignments, not global historical law."""
import json
from decimal import Decimal
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
P = "docs/research/TIANWEN-13BH-GORYEOSA-NAJ-ORIGINAL-RECEIVED-CUMULATIVE-FIVEPOINT-OFFSET-R1.json"
PYZ = "docs/research/TIANWEN-12YZ-GORYEOSA-D14-D20-INTRATABLE-THREE-COLUMN-RECEIVED-ARITHMETIC-R1.json"
PBE = "docs/research/TIANWEN-13BE-GORYEOSA-D16-ORIGINAL-LONG-LANE-DUAL-COPY-COLLATION-R1.json"
PBF = "docs/research/TIANWEN-13BF-GORYEOSA-D14-D17-ORIGINAL-ACCUMULATIVE-LOCAL-INDEX-OFFSET-R1.json"
PBG = "docs/research/TIANWEN-13BG-GORYEOSA-NAJ-ADJACENT-FOLIOS-CUMULATIVE-D17-D19-R1.json"
MD = "docs/research/TIANWEN-13BH-GORYEOSA-NAJ-ORIGINAL-RECEIVED-CUMULATIVE-FIVEPOINT-OFFSET-R1.md"
def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(e, yz, be, bf, bg, ledger, state):
    assert e["schema"] == "TIANWEN-13BH-GORYEOSA-ORIGINAL-RECEIVED-FIVEPOINT-INDEX-OFFSET-REPLAY-R1"
    assert e["grade"] == "DERIVED_CROSS_LAYER_ALIGNMENT_OF_ALREADY_SHA_BOUND_ORIGINAL_GLYPHS_AND_INSTITUTIONAL_RECEIVED_TEXT"
    assert e["issue_id"] == "TW-OPEN-0005"
    assert e["input_evidence"] == {
       "original_day14_day15_long_and_day15_cum":PBF,
       "original_day16_day17_long_cum":PBE,
       "original_day18_day19_cum":PBG,
       "modern_institutional_received_rows":PYZ}
    assert e["source_holding"] == bg["source_holding"] == "NAJ-282-0006-PHYSICAL51"
    assert e["known_original_canvases"] == [17,18]
    assert e["same_physical_holding_not_independent_vote"] is True
    assert bg["source_canvases"][1]["source_jpeg_sha256"] == bf["manuscript_originals"][0]["source_JPEG_sha256"] == be["source_original_image_reviews"][0]["original_image_sha256"]
    originals = [
      bf["manuscript_originals"][0]["new_original_roi"][2]["decimal"],
      be["adjacent_cumulative_scope"]["printed_day16_decimal"],
      be["adjacent_cumulative_scope"]["printed_day17_decimal"],
      bg["source_canvases"][2]["new_day_slots"][0]["decimal"],
      bg["source_canvases"][2]["new_day_slots"][1]["decimal"]]
    longs = [
      bf["manuscript_originals"][0]["new_original_roi"][0]["decimal"],
      bf["manuscript_originals"][0]["new_original_roi"][1]["decimal"],
      be["roman_decimal_bridge"]["day16_long"],
      be["roman_decimal_bridge"]["day17_long"]]
    assert len(e["observed_original_vs_received"]) == 5
    for i, item in enumerate(e["observed_original_vs_received"]):
       assert item["original_layout_day"] == i + 15
       assert item["source_canvas"] == (17 if i < 3 else 18)
       assert item["direct_original_source"] == (PBF if i == 0 else PBE if i < 3 else PBG)
       assert item["received_digital_row_day"] == i + 14
       assert item["original_cumulative"] == originals[i]
       assert item["received_digital_cumulative"] == yz["modern_received_rows"][i]["cumulative"]
       assert Decimal(originals[i]) == Decimal(item["received_digital_cumulative"])
    assert len(e["original_four_local_edges"]) == 4
    for i, edge in enumerate(e["original_four_local_edges"]):
       assert edge["from_original_layout_day"] == 15 + i
       assert edge["to_original_layout_day"] == 16 + i
       assert edge["original_long_day"] == edge["received_digital_long_day"] == 14 + i
       assert Decimal(edge["cumulative_delta"]) == Decimal(originals[i+1]) - Decimal(originals[i])
       assert Decimal(edge["original_long"]) == Decimal(longs[i]) == Decimal(edge["cumulative_delta"])
       assert Decimal(edge["received_digital_long"]) == Decimal(yz["modern_received_rows"][i]["long"]) == Decimal(longs[i])
    assert e["local_offset_rule"] == "C_NAJ_LAYOUT(n) == C_RECEIVED_DIGITAL_ROW(n-1), limited to n=15..19 and these five already-read slots"
    assert e["same_numbered_day_equivalence"] is False
    assert e["historical_printed_header_index_convention"] == "UNADJUDICATED"
    assert e["section_start_and_end_and_transition_behavior"] == "NOT_DIRECTLY_COLLATED"
    assert e["Waseda_original_day18_day19_cumulative"] == "NOT_DIRECTLY_COLLATED"
    assert e["G893_other_work_column_unit_equivalence"] == "UNPROVEN"
    assert e["D16_original_short"] == be["roman_decimal_bridge"]["day16_short"] == "5.1362"
    assert e["D16_original_long_difference"] == be["roman_decimal_bridge"]["long_d16_minus_d17"] == "5.2362"
    assert e["D16_different_work_G893_short"] == "5.2362"
    assert e["D16_ancestral_original_choice"] == "UNRESOLVED" and e["historical_lineage_independence"] == "UNPROVEN"
    limits=e["scope_counters"]
    assert all(limits[key] == 0 for key in ("new_original_pixels_acquired","new_original_copies","new_registry_sources","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","algorithm_reopens"))
    assert limits["open_omission_issues"] == 11 and limits["deterministic_product"] == "CLOSED"
    issue=next(x for x in ledger["issues"] if x["id"] == "TW-OPEN-0005")
    assert issue["status"] == "OPEN" and issue["priority"] == "P0"
    assert issue["source_refs"].count(MD) == issue["source_refs"].count(P) == 1
    assert issue["source_refs"].index(P) == issue["source_refs"].index(MD) + 1
    assert any(x["event"] == "GORYEOSA_13BH_FIVEPOINT_ORIGINAL_RECEIVED_OFFSET_REPLAY" for x in issue["history"])
    assert state["schema_version"] == ledger["binding"]["reviewed_state_version"] == state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    assert any(x.startswith("13BH ") for x in state["historical_audit"]["current_focus"])
    assert ledger["binding"]["source_focus_count"] == len(state["historical_audit"]["current_focus"])
    assert ledger["binding"]["latest_research_focus_prefix"] == state["historical_audit"]["current_focus"][-1].split(" ")[0]
    assert ledger["checkpoint_log"][-1]["state_version"] == state["schema_version"]
    assert len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"]) == 11
    return True
if __name__ == "__main__":
    assert check(load(P),load(PYZ),load(PBE),load(PBF),load(PBG),load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"),load("docs/PROJECT-CURRENT-STATE-R1.json"))
    print("13BH 5-point local cross-layer cumulative offset gate PASS")
