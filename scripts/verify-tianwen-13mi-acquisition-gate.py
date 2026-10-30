#!/usr/bin/env python3
"""13MI intake plan strict gate: images are NOT historical numeric proof."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
S=json.loads((R/"docs/PROJECT-CURRENT-STATE-R1.json").read_text())
L=json.loads((R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text())
E=json.loads((R/"docs/research/TIANWEN-13MI-G893-1569-ORIGINAL-IMAGE-FIELD-GATE-R1.json").read_text())
assert E["schema"]=="TIANWEN-13MI-G893-1569-ORIGINAL-IMAGE-FIELD-GATE-R1"
assert E["stage"]=="SOURCE_ACQUISITION_SCRIPT_AND_ACTION_STAGED_NOT_EXECUTED"
assert [x["page"] for x in E["source_a"]["known_original_pages"]]==["001a","002a","002b"]
assert E["source_b"]["target_pdf_pages_1based"]==[7,9,14,19]
assert E["source_b"]["expected_pdf_sha256"]=="4c006b7ce131902fe33012d42f62cd2bbc2140affa3d5886e0da02966352cb7c"
assert E["source_replay_plan"]["no_ocr"]
assert E["no_promotion"]["g893_six_cross_source_winners"]==0
assert E["no_promotion"]["algorithm_reopens"]==0
assert not E["no_promotion"]["same_field_assigned"]
assert S["schema_version"]==L["binding"]["reviewed_state_version"]==S["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
assert tuple(map(int,S["schema_version"].split(".")))>=(1,971,0)
assert len(S["historical_audit"]["current_focus"])==L["binding"]["source_focus_count"]
assert any(x.startswith("13MI ") for x in S["historical_audit"]["current_focus"])
assert L["binding"]["latest_research_focus_prefix"] in ("13MI","13MJ")
issue=next(x for x in L["issues"] if x["id"]=="TW-OPEN-0005")
assert issue["status"]=="OPEN" and issue["priority"]=="P0"
assert "docs/research/TIANWEN-13MI-G893-1569-ORIGINAL-IMAGE-FIELD-GATE-R1.json" in issue["source_refs"]
assert any(x.get("revision_id")=="TW-OPEN-0005-13MI-G893-1569-SOURCE-GATE-20261031" for x in issue["history"])
assert S["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
print("PASS: 13MI strict original source acquisition gated, no historical numerals promoted")
