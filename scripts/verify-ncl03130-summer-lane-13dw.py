#!/usr/bin/env python3
"""13DW: fail closed when page/day ROI headings are promoted to source XingDu values."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13DW-NCL03130-SUMMER-P82-P86-LANE-FIELD-FIREWALL-R1.json"
S=ROOT/"docs/PROJECT-CURRENT-STATE-R1.json"
L=ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def check(e,s,l):
    assert e["schema"]=="TIANWEN-13DW-NCL03130-SUMMER-HEADER-LANE-SCOPE-R1"
    assert e["issue_id"]=="TW-OPEN-0005"
    assert e["source_identity"]["pdf_sha256"]=="3c2a5621fb3f4eabc593020bcde12a38f6ecdae2842940dec12d5a3a56afd32e"
    assert e["source_identity"]["physical_copy_firstparty_item_binding"]=="UNBOUND"
    assert e["source_identity"]["qing_versus_1905_supplement_copy_layer"]=="UNBOUND"
    pages=e["reviewed_original_pages"]
    assert [(x["pdf_page"],x["original_png_sha256"]) for x in pages]==[
        (82,"4b8efc11d9ce84e9025f8115533cafb4a6a33e2653e33f548b1d85c9487c6ed7"),
        (83,"713d7dddf8f26030eaca40b3552f598acdc580cfbf291da059461a6d7bec83c0"),
        (86,"9107be92e0381fb596ffec33f2e7fbcffda2adc0f17bca4da303ffec6032693c")]
    a=e["p86_native_roi_provenance"]
    assert a["original_render_rgb_sha256"]=="550f80c6701408dcdab4e7728bec03a7480f0b762fda5837f514d4b9eb919cef"
    assert a["printed_day_roi_order_right_to_left"]==[27,28,29]
    assert [(x["day"],x["png_sha256"]) for x in a["rois"]]==[
        (27,"f54a1e57a61c0fa8fe9876d1f388fa37b6ea52bb006707fdd62b93db962284e0"),
        (28,"5428823bed7f7b25fce08fae873583cdd3ae01b4717ac5a396cb81da86f30167"),
        (29,"84bf5e203091a4cff47da390fce8ecd462842e6877da8947fbce124c71752c2d")]
    b=e["source_native_d28_unit_band"]
    assert b["heading_glyphs"]=="二十八" and b["header_glyphs_right_to_left"]==["日","分","度","度"]
    assert b["exact_xingdu_locus"]=="NOT_YET_INDEPENDENTLY_BOUND_TO_THE_UNIT_LANE"
    assert b["exact_xingdu_glyphs"] is None and b["exact_xingdu_decimal"] is None
    assert b["observation_grade"]=="SOURCE_ORIGINAL_MULTI_LANE_HEADER_POSITIVE_NUMERIC_FIELD_UNRESOLVED"
    c=e["cross_original_scope"]
    assert c["ncl03130_day28_printed_xingdu"]=="UNREAD"
    assert c["ncl03130_matches_any_previous_original"] is None
    assert c["day_label_mapping_proven"] is False and c["whole_table_day_offset_proven"] is False
    assert c["physical_copy_independence_proven"] is False
    assert all(v==0 for k,v in e["resolution"].items() if k not in ("chart_product",))
    assert e["resolution"]["chart_product"]=="CLOSED"
    assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
    assert any(x.startswith("13DW ") for x in s["historical_audit"]["current_focus"])
    assert any(x.startswith("13DV ") for x in s["historical_audit"]["current_focus"])
    assert next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")["status"]=="OPEN"
    return True
if __name__=="__main__":
    assert check(load(E),load(S),load(L))
    print("13DW_PASS")
