#!/usr/bin/env python3
"""13BC: prior received arithmetic cannot be promoted to original glyph proof."""
import json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PC="docs/research/TIANWEN-13BC-GORYEOSA-D16-RECEIVED-ARITHMETIC-VS-ORIGINAL-GLYPH-CROSSLAYER-R1.json"
PA="docs/research/TIANWEN-12YZ-GORYEOSA-D14-D20-INTRATABLE-THREE-COLUMN-RECEIVED-ARITHMETIC-R1.json"
PB="docs/research/TIANWEN-13BA-NAJDA-GORYEOSA51-WINTER-SOLAR-D16-DIRECT-GLYPH-R1.json"
PD="docs/research/TIANWEN-13BB-GORYEOSA-SOLAR-D16-MULTIHOLDING-EVIDENCE-FIREWALL-R1.json"
MD=PC.replace(".json",".md")
def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(e,a,b,c,ledger,state):
    assert e["schema"]=="TIANWEN-13BC-D16-RECEIVED-ARITHMETIC-AND-HISTORICAL-ORIGINAL-GLYPH-CROSS-LAYER-GATE-R1"
    assert e["issue_id"]=="TW-OPEN-0005" and e["evidence_inputs"]=={
      "received_arithmetic":PA,"historical_original_NAJ":PB,"multiholding_original_scope":PD}
    assert e["prior_recurrence_discovered_in_batch"]=="12YZ" and e["new_historical_original_pages_acquired"]==0
    assert a["sources"]["official_grade"]=="INSTITUTIONAL_MODERN_DIGITAL_TRANSCRIPTION_NOT_ANCIENT_PHYSICAL_IMAGE"
    rows=a["modern_received_rows"]
    assert [r["day"] for r in rows]==list(range(14,21))
    r16,r17=rows[2],rows[3]
    x=e["received_triple_lane"]
    assert x["provider_url"]==a["sources"]["official_url"]
    assert x["grade"]=="MODERN_INSTITUTIONAL_TEXT_NOT_NEW_HISTORICAL_ORIGINAL"
    for key,seen in [("day16_short",r16["short"]),("day16_long",r16["long"]),
       ("day17_long",r17["long"]),("day16_cumulative",r16["cumulative"]),
       ("day17_cumulative",r17["cumulative"])]:
        assert x[key]==seen
    assert Decimal(x["day16_long"])-Decimal(x["day17_long"])==Decimal(x["long_difference_implies_day16_short"])==Decimal("5.2362")
    assert Decimal(x["day17_cumulative"])-Decimal(x["day16_cumulative"])==Decimal(x["cumulative_difference_confirms_day16_long"])==Decimal(x["day16_long"])
    assert x["day16_short"]=="5.1362" and Decimal(x["long_difference_implies_day16_short"])-Decimal(x["day16_short"])==Decimal("0.1000")
    assert x["literal_anomaly"]=="五分一三六二" and a["local_relations"]["short_to_long_failure_days"]==[16]
    assert x["tested_edges_days"]==list(range(14,20)) and x["only_short_to_long_failed_day"]==16
    assert b["source_glyph_loci"][1]["original_rgb_roi"][1]["reading"]=="五分一三六二"
    assert c["historical_earliest_one_or_two"]=="UNRESOLVED"
    originals=e["previously_attested_original_short_glyphs"]
    assert len(originals)==len(c["controls"])==4
    assert [r["id"] for r in originals]==[r["id"] for r in c["controls"]]
    for r,prior in zip(originals,c["controls"]):
        assert r["d16"]==prior["short_d16"] and r["jpeg_sha256"]==prior["source_file_sha256"]
    assert originals[0]["jpeg_sha256"]==b["source_glyph_loci"][1]["jpeg_sha256"]
    assert originals[3]["d16"]=="五分二三六二" and originals[3]["jpeg_sha256"] is None
    assert e["original_crosscolumn_image_collation_status"]=="NOT_PERFORMED_BY_13BC"
    for key in ("received_relation_may_be_computed_but_not_projected_onto_original_long_or_cumulative_glyphs",
        "original_digit_is_not_silently_normalized_by_arithmetic",
        "identical_received_long_lane_not_proof_of_cross_work_unit_or_stemmatic_independence"):
        assert e[key] is True
    for key in ("independent_numeric_votes_added","direct_transmission_edges_added","new_registry_sources_added","algorithm_reopens"):
        assert e[key]==0
    assert e["earliest_original_one_or_two"]=="UNRESOLVED" and e["product_status"]=="CLOSED"
    issue=next(i for i in ledger["issues"] if i["id"]=="TW-OPEN-0005")
    assert issue["priority"]=="P0" and issue["status"]=="OPEN"
    assert issue["source_refs"][-2:]==[MD,PC]
    assert ledger["binding"]["reviewed_state_version"]==state["schema_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
    assert ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ")[0]=="13BC"
    assert ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"]
    assert len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==11
    return True
if __name__=="__main__":
    assert check(load(PC),load(PA),load(PB),load(PD),load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"),load("docs/PROJECT-CURRENT-STATE-R1.json"))
    print("13BC received/original layer firewall PASS")
