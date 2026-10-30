#!/usr/bin/env python3
"""13MF title-start evidence and 13MG prospective acquisition firewall."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=json.loads((ROOT/"docs/research/TIANWEN-13MF-BSB-JUAN35-DIRECT-TITLE-C560-AND-ADJACENT-FASCICLE-GATE-R1.json").read_text(encoding="utf8"))
S=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf8"))
L=json.loads((ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf8"))
assert E["schema"]=="TIANWEN-13MF-BSB-JUAN35-DIRECT-TITLE-C560-AND-ADJACENT-FASCICLE-GATE-R1"
assert E["issue_id"]=="TW-OPEN-0005"
a=E["acquisition"];assert a["workflow_run"]==41081537867 and a["conclusion"]=="success" and a["source_derived_900px_jpeg_count"]==29
assert a["reverified_jpeg_sha256_count"]==a["reverified_decoded_rgb_sha256_count"]==29
assert a["artifact_zip_sha256"]=="596b55bcda02a84b316f82ba7770c826417a62eaa4619d9a578ffa3fd0320c98"
p={x["canvas"]:x for x in E["direct_page_observations"]}
assert p[560]["glyphs"]==["明史卷三十五","志第十一","歷五","大統曆法三上"]
assert p[560]["jpeg_sha256"]=="3e28a2edb539561b952e46a01a75d4bfd003cdf46f0287f2140b0d20fc405ca8"
assert p[574]["glyphs"]==["明史卷三十四終"]
assert E["scoped_folio_relationship"]["original_title_leaf_juan35_positive"]
assert E["scoped_folio_relationship"]["original_juan35_title_leaf_canvas"]==560
assert E["next_acquisition_plan"]["status"]=="SCRIPT_AND_ACTION_STAGED_NOT_REPLAYED"
assert E["next_acquisition_plan"]["canvas_ids_1based"]==list(range(511,561))+[574]
assert E["limitations"]["original_g893_six_numeric_winners_added"]==E["limitations"]["algorithm_reopens"]==0
assert S["schema_version"]==L["binding"]["reviewed_state_version"]==S["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
assert tuple(map(int,S["schema_version"].split(".")))>=(1,969,0)
assert any(x.startswith("13MF ") for x in S["historical_audit"]["current_focus"])
assert len(S["historical_audit"]["current_focus"])==L["binding"]["source_focus_count"]
i=next(x for x in L["issues"] if x["id"]=="TW-OPEN-0005")
assert i["priority"]=="P0" and i["status"]=="OPEN" and "docs/research/TIANWEN-13MF-BSB-JUAN35-DIRECT-TITLE-C560-AND-ADJACENT-FASCICLE-GATE-R1.json" in i["source_refs"]
assert any(h.get("revision_id")=="TW-OPEN-0005-13MF-BSB-J35-TITLE-C560-20261031" for h in i["history"])
assert S["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
print(json.dumps({"status":"PASS","positive_original_juan35_title":560,"original_numeric_winners":0,"planned_source_images":51}))
