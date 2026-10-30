#!/usr/bin/env python3
"""Source-scoped 13MH gate: 51 original source images, 4 original glyph loci, no cross-book promotion."""
import json
from decimal import Decimal
from pathlib import Path
R=Path(__file__).resolve().parents[1]
e=json.loads((R/"docs/research/TIANWEN-13MH-BSB-J35-51-IMAGE-REPLAY-C539-FOUR-FIELD-COLLATION-R1.json").read_text(encoding="utf-8"))
s=json.loads((R/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf-8"))
l=json.loads((R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf-8"))
assert e["schema"]=="TIANWEN-13MH-BSB-J35-51-IMAGE-REPLAY-C539-FOUR-FIELD-COLLATION-R1"
a=e["artifact"]
assert a["origin_run"]==41139192438 and a["run_conclusion"]=="success"
assert a["zip_bytes"]==18842912 and a["zip_sha256"]=="a23c600a5ee659e0e32372f4355640a25b6751fae4c8cec78161488653d3688b"
assert a["manifest_sha256_replayed"] and a["source_900px_jpegs_verified"]==a["decoded_rgb_verified"]==51
assert a["source_original_1based_pages"]==list(range(511,561))+[574]
assert a["full_51_page_literal_manual_collation_complete"] is False
hi=e["higher_resolution_provider_derivatives"]
assert sorted(x["canvas"] for x in hi)==[511,539,560,574]
assert all(x["status"]=="SOURCE_HIGHER_RESOLUTION_DERIVATIVE_CAPTURED" and x["decoded_rgb_sha256_recomputed_matches_report"] for x in hi)
v=e["c539_original_reading"]
assert v["original_1800px_sha256"]=="a9ac8e878b9823c89087b9a9be9147406c289c755f6b0dfd38dbd6e43d80d2f7"
assert [x["elapsed_days"] for x in v["observations"]]==[88,89,93,94]
assert [x["normalized_degree_string"] for x in v["observations"]]==["90.4009","91.4014","90.5990","91.5987"]
assert Decimal("91.4014")-Decimal("90.4009")==Decimal("1.0005")
assert Decimal("91.5987")-Decimal("90.5990")==Decimal("0.9997")
assert e["received_text_comparison"]["physical_copy_witness_added"]==0
f=e["safeguards"]
assert f["g893_six_cross_witness_mechanical_winners_added"]==0 and not f["chart_algorithm_reopened"]
assert not f["all_51_pages_literal_collated"] and f["chart_product"]=="CLOSED"
assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
assert tuple(map(int,s["schema_version"].split(".")))>=(1,970,0)
assert any(x.startswith("13MH ") for x in s["historical_audit"]["current_focus"])
assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
x=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
assert x["status"]=="OPEN" and x["priority"]=="P0" and "docs/research/TIANWEN-13MH-BSB-J35-51-IMAGE-REPLAY-C539-FOUR-FIELD-COLLATION-R1.json" in x["source_refs"]
assert any(h.get("revision_id")=="TW-OPEN-0005-13MH-C539-FOUR-ORIGINAL-FIELDS-20261031" for h in x["history"])
print(json.dumps({"status":"PASS","source_original_pages":51,"highres_source_pages":4,"original_c539_source_scope_numeric_fields":4,"g893_original_winners":0}))
