#!/usr/bin/env python3
"""13MD staging strict no-promotion and forward-only state guard."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=json.loads((R/"docs/research/TIANWEN-13MD-BSB-V1-JUAN35-TITLE-LEAF-BOUNDED-SWEEP-STAGING-R1.json").read_text(encoding="utf8"))
S=json.loads((R/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf8"))
L=json.loads((R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf8"))
assert E["schema"]=="TIANWEN-13MD-BSB-V1-J35-TITLE-LEAF-BOUNDED-SWEEP-STAGING-R1"
assert E["stage"]=="ACQUISITION_SCRIPT_STAGED_NOT_YET_RESULT"
assert E["issue_id"]=="TW-OPEN-0005"
assert E["source"]["provider_object_id"]=="bsb11166691" and E["source"]["canvas_count"]==1910
assert E["acquisition_plan"]["candidate_search_window_1based"]==[491,636]
assert E["acquisition_plan"]["no_ocr"] and E["acquisition_plan"]["uses_exact_manifest_declared_services"]
assert 490 in E["acquisition_plan"]["sampled_indexes"] and 539 in E["acquisition_plan"]["sampled_indexes"] and 637 in E["acquisition_plan"]["sampled_indexes"]
assert all(E["evidentiary_limits"][k] is False for k in ("title_leaf_original_glyph_verified","numeric_target_original_glyph_verified","independent_1739_impression_verified","global_negative_absence_proven"))
assert E["evidentiary_limits"]["g893_six_numerical_winners_added"]==E["evidentiary_limits"]["algorithm_reopens"]==0
assert S["schema_version"]==L["binding"]["reviewed_state_version"]==S["historical_audit"]["research_omission_guard"]["reviewed_state_version"]=="1.967.0"
assert len(S["historical_audit"]["current_focus"])==L["binding"]["source_focus_count"]
assert S["historical_audit"]["current_focus"][-1].startswith("13MD ")
assert L["binding"]["latest_research_focus_prefix"]=="13MD"
I=next(x for x in L["issues"] if x["id"]=="TW-OPEN-0005")
assert I["priority"]=="P0" and I["status"]=="OPEN"
assert I["next_action"].startswith("13MD CURRENT ACTION:")
assert "docs/research/TIANWEN-13MD-BSB-V1-JUAN35-TITLE-LEAF-BOUNDED-SWEEP-STAGING-R1.json" in I["source_refs"]
assert any(h.get("revision_id")=="TW-OPEN-0005-13MD-STAGED-SOURCE-TITLE-SWEEP-20261030" for h in I["history"])
assert S["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
print(json.dumps({"status":"PASS","source_sample_plan":len(E["acquisition_plan"]["sampled_indexes"]),"title_leaf_verified":False,"algorithm_reopen":0}))
