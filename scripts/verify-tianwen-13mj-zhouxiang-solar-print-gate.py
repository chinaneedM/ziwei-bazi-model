#!/usr/bin/env python3
"""13MJ scope: 1569 source print D15-D17 original; don't promote cross-edition G893."""
import json
from decimal import Decimal
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=json.loads((R/"docs/research/TIANWEN-13MJ-ZHOUXIANG-1569-D15-D17-PRINTED-SOURCE-VS-G893-GATE-R1.json").read_text())
S=json.loads((R/"docs/PROJECT-CURRENT-STATE-R1.json").read_text())
L=json.loads((R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text())
assert E["schema"]=="TIANWEN-13MJ-ZHOUXIANG-1569-D15-D17-PRINTED-SOURCE-VS-G893-GATE-R1"
assert E["source_acquisition"]["conclusion"]=="success"
assert E["source_acquisition"]["g893_images_requested"]==3 and E["source_acquisition"]["g893_images_hash_verified"]==2
assert E["source_acquisition"]["report_status"]=="PARTIAL_ACCESS_BOUNDARY_UNCOLLATED"
assert E["source_acquisition"]["zip_sha256"]=="bc68ccf228848fedddc2cc75ce12d6dee6d669c684bc9e33558c2c85f0c8e9ab"
assert E["source_acquisition"]["ming1569_pdf"]["sha256"]=="4c006b7ce131902fe33012d42f62cd2bbc2140affa3d5886e0da02966352cb7c"
p=E["new_direct_source_locus"]
assert p["printed_three_days_page_1based"]==15
assert p["page15_replay"]["full_rgb_sha256"]=="7b35af0e1e802c9346c927a02c67d1681e01b5120c3cf891160126f2018478d5"
assert p["page15_replay"]["crop_rgb_sha256"]=="72f4069db6044ce0b77f85259303c830b4f1cd14407469f73ac37e6d00632e41"
d=p["source_printed_values"]
assert [(v["elapsed_day"],v["normalized"]) for v in d]==[(15,"5.2176"),(16,"5.2362"),(17,"5.2548")]
assert Decimal(d[1]["normalized"])-Decimal(d[0]["normalized"])==Decimal("0.0186")
assert Decimal(d[2]["normalized"])-Decimal(d[1]["normalized"])==Decimal("0.0186")
assert E["comparability_guard"]["g893_cross_witness_six_winners_awarded"]==0
assert E["comparability_guard"]["algorithm_reopens"]==0
assert not E["comparability_guard"]["original_field_name_radix_and_conversion_equal"]
assert E["followup_source_access"]["status"]=="13MI_SOURCE_SCRIPT_RETRY_ADDED_NOT_YET_REPLAYED"
assert S["schema_version"]==L["binding"]["reviewed_state_version"]==S["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
assert tuple(map(int,S["schema_version"].split(".")))>=(1,972,0)
assert any(x.startswith("13MJ ") for x in S["historical_audit"]["current_focus"])
assert len(S["historical_audit"]["current_focus"])==L["binding"]["source_focus_count"]
issue=next(x for x in L["issues"] if x["id"]=="TW-OPEN-0005")
assert issue["status"]=="OPEN" and issue["priority"]=="P0"
assert "docs/research/TIANWEN-13MJ-ZHOUXIANG-1569-D15-D17-PRINTED-SOURCE-VS-G893-GATE-R1.json" in issue["source_refs"]
assert any(x.get("revision_id")=="TW-OPEN-0005-13MJ-ZHOUXIANG-D15D17-PRINTED-20261031" for x in issue["history"])
assert S["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
print(json.dumps({"status":"PASS","printed_1569_D15_D16_D17":[x["normalized"] for x in d],"g893_original_six_winners":0}))
