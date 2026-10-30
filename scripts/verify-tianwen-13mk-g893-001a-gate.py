#!/usr/bin/env python3
"""13MK: G893 exact-HEAD source re-acquisition and bounded glyph/field firewall."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/"docs/research/TIANWEN-13MK-G893-001A-ORIGINAL-REACQUISITION-HEADER-D16-GEOMETRY-R1.json"
e=json.loads(p.read_text(encoding="utf-8"))
s=json.loads((R/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf-8"))
l=json.loads((R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf-8"))
assert e["schema"]=="TIANWEN-13MK-G893-001A-ORIGINAL-REACQUISITION-HEADER-D16-GEOMETRY-R1"
a=e["source_acquisition"]
assert a["run_id"]==41144025711 and a["run_head"]=="468f1d2576057404d279313c8b0a19e0597969f8"
assert a["conclusion"]=="success" and a["g893_requested"]==a["g893_source_issued_hash_verified"]==3
assert a["g893_001a_attempt_count"]==2
assert a["zip_sha256"]=="1d8f10da7c27411bf38ad635494a1b9f4e700fb76cb37b2a7541c075a0ca9835"
assert a["acquisition_status"]=="BOTH_OBJECTS_SOURCE_BOUND_UNCOLLATED"
assert {x["page"] for x in a["g893_verified_originals"]}=={"001a","002a","002b"}
v=e["direct_visual_reviews"]
assert len(v)==2 and all(x["no_ocr"] for x in v)
assert "加一秒八十六少" in v[0]["observed"] and "十六日" in v[1]["observed"]
assert v[0]["crop_rgb_sha256"]=="f1c2fd172cad71f37d546b4ae67181282aad76c22064e8113593a835d2103e88"
assert v[1]["crop_rgb_sha256"]=="0feb183b7f0c873ff01130e7c14b796dae03ee7539251dd38fbc1247a3156aaa"
c=e["comparison_controls"]
assert c["same_source_field_and_unit_crosswalk"]=="UNPROVEN"
assert c["numerical_g893_six_target_historical_winners"]==c["chart_algorithm_reopens"]==0
assert c["chart_product"]=="CLOSED"
assert c["external_source_entries_added"]==c["graph_edges_added"]==c["matrix_row_status_changes"]==0
assert s["schema_version"]==l["binding"]["reviewed_state_version"]
assert tuple(map(int,s["schema_version"].split("."))) >= (1,973,0)
assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
assert any(x.startswith("13MK ") for x in s["historical_audit"]["current_focus"])
assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ")[0]
issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
assert issue["status"]=="OPEN" and issue["priority"]=="P0"
assert str(p.relative_to(R)) in issue["source_refs"]
assert any(x.get("revision_id")=="TW-OPEN-0005-13MK-ORIGINAL-001A-REACQUIRED-20261031" for x in issue["history"])
assert any(x["state_version"]=="1.973.0" and x["id"]=="OMISSIONS-13MK-G893-001A-ORIGINAL-REACQUISITION-20261031" for x in l["checkpoint_log"])
assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
print(json.dumps({"result":"PASS","g893_original_pages_verified":3,"crosssource_winners":0,"product":"CLOSED"}))
