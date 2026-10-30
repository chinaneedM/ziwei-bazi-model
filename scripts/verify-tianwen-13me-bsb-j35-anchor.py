#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=json.loads((R/"docs/research/TIANWEN-13ME-BSB-V1-J35-ORIGINAL-C511-END-AND-TITLE-RECHECK-R1.json").read_text(encoding="utf8"))
S=json.loads((R/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf8"))
L=json.loads((R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf8"))
assert E["schema"]=="TIANWEN-13ME-BSB-V1-J35-ORIGINAL-C511-END-AND-TITLE-RECHECK-R1"
assert E["acquisition_13md"]["conclusion"]=="success" and E["acquisition_13md"]["original_jpeg_count"]==33
assert E["original_juan35_end"]["manual_original_print"]=="明史卷三十五終"
assert E["original_juan35_end"]["jpeg_sha256"]=="d7c9ffb0ea1db796c30779f56b08388f960c099574181063dba3ea585ff70226"
assert E["original_juan35_end"]["rgb_sha256"]=="72764e4c0089c9c558e095cf6a2498a56552f7e829e04f3129053f2b1fcbbd92"
assert E["original_juan35_end"]["is_original_juan35_start_title"] is False
assert E["next_acquisition"]["status"]=="STAGED_NOT_ACQUIRED"
assert all(x in E["next_acquisition"]["indices_1based"] for x in (511,539,556,561,566,571,576,577))
assert E["no_promotion"]["original_juan35_title_leaf_verified"] is False
assert E["no_promotion"]["g893_six_numeric_winners"]==E["no_promotion"]["algorithm_reopens"]==0
assert S["schema_version"]==L["binding"]["reviewed_state_version"]==S["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
assert tuple(map(int,S["schema_version"].split(".")))>=(1,968,0)
assert any(x.startswith("13ME ") for x in S["historical_audit"]["current_focus"])
assert len(S["historical_audit"]["current_focus"])==L["binding"]["source_focus_count"]
issue=next(x for x in L["issues"] if x["id"]=="TW-OPEN-0005")
assert issue["priority"]=="P0" and issue["status"]=="OPEN" and "docs/research/TIANWEN-13ME-BSB-V1-J35-ORIGINAL-C511-END-AND-TITLE-RECHECK-R1.json" in issue["source_refs"]
assert any(x.get("revision_id")=="TW-OPEN-0005-13ME-J35-END-20261030" for x in issue["history"])
print(json.dumps({"status":"PASS","original_juan35_end_canvas":511,"original_title_leaf_verified":False,"planned_source_pages":len(E["next_acquisition"]["indices_1based"])}))
