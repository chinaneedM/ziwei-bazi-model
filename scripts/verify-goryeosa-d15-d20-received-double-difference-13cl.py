#!/usr/bin/env python3
"""13CL: cross-replay local received short/long/cumulative differences, frozen historical original controls."""
from __future__ import annotations
import hashlib,json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CL-GORYEOSA-D15-D20-DOUBLE-DIFFERENCE-CHECK-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
REGISTRY="docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def git_blob(path):
 b=(ROOT/path).read_bytes()
 return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\x00"+b).hexdigest()
def D(v):return Decimal(v)
def check(e,s,l,reg,old):
 assert e["schema"]=="TIANWEN-13CL-SOLAR-D15-D20-RECEIVED-LOCAL-DIFFERENCE-AND-ORIGINAL-D16-ANOMALY-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 assert len(e["source_pages"])==2
 assert [z["name"] for z in e["source_pages"]]==["KRDB","WIKISOURCE"]
 for z in e["source_pages"]:
  assert z["html_sha256"]=="NOT_CAPTURED"
  assert any(x["source_id"]==z["reused_registry_source"] for x in reg["sources"])
 assert "NO_NEW_IMAGE" in e["grade"]
 b=e["exact_original_record_bindings"]
 assert set(b)=={"13CA","13CI","13CK"}
 for k,v in b.items():
  assert git_blob(v["path"])==v["sha"]
 assert old["13CA"]["direct_reading"]["rical_unit_literal"]==e["source_column_identity"]["original_Waseda_13CA_heading"]=="日差加一秒八十六少"
 assert old["13CA"]["direct_reading"]["original_D16_same_day_isolated_yingsuoji"]=="UNBOUND"
 assert old["13CI"]["local_exact_arithmetic"]["source_printed_D16_short"]=="5.1362"
 assert old["13CI"]["local_exact_arithmetic"]["long_D16_minus_D17"]=="5.2362"
 assert old["13CI"]["source_boundaries"]["W_D16_same_day_yingsuoji"]=="UNBOUND"
 assert old["13CK"]["scoped_comparison"]["institutional_d18_received_literal"]=="八千四百二十四六四〇八三"
 assert old["13CK"]["scoped_comparison"]["community_d18_received_literal"]=="八千四百二十四六四〇八"
 cols=e["source_column_identity"]
 assert cols["column_name_not_position_rule"] is True
 assert cols["short"]=="日差加一秒八十六少" and cols["long"]=="盈縮加分" and cols["c"]=="盈縮積"
 assert cols["krdb_order"]!=cols["wikisource_order"]
 assert cols["historical_shao_wei_to_decimal_unit_bridge"]=="UNPROVEN"
 assert cols["short_increment_observed_digit_decimal"]=="0.0186"
 row=e["received_rows"]
 assert [x["day"] for x in row]==[15,16,17,18,19,20]
 expect=[
 ("5.2176","434.8249","7135.8375","五分二一七六","四百三十四八二四九","七千一百三十五八三七五"),
 ("5.1362","429.6073","7570.6624","五分一三六二","四百二十九六〇七三","七千五百七十〇六六二四"),
 ("5.2548","424.3711","8000.2697","五分二五四八","四百二十四三七一一","八千〇〇〇二六九七"),
 ("5.2734","419.1163","8424.6408","五分二七三四","四百一十九一一六三","八千四百二十四六四〇八"),
 ("5.2920","413.8429","8843.7571","五分二九二〇","四百一十三八四二九","八千八百四十三七五七一"),
 ("5.3106","408.5509","9257.6000","五分三一〇六","四百〇八五五〇九","九千二百五十七六〇〇〇")]
 for x,y in zip(row,expect):
  assert tuple(x[k] for k in ("short","long","c","short_glyph","long_glyph","c_glyph"))==y
  if x["day"]==18:assert x["institutional_received_c_glyph"]==old["13CK"]["scoped_comparison"]["institutional_d18_received_literal"]
  else:assert "institutional_received_c_glyph" not in x
 a=e["local_received_arithmetic"]
 assert len(a["short_edges"])==len(a["long_edges"])==len(a["cumulative_edges"])==5
 for i in range(5):
  before,after=row[i:i+2]
  for key,expr,expected_match in [
   ("short_edges",D(after["short"])-D(before["short"]),i>=2),
   ("long_edges",D(before["long"])-D(after["long"]),i!=1),
   ("cumulative_edges",D(after["c"])-D(before["c"]),True)]:
   y=a[key][i]
   assert y["from"]==before["day"] and y["to"]==after["day"]
   assert D(y["difference"] if key=="short_edges" else y["delta"])==expr
   assert y["matches"]==expected_match if key=="short_edges" else y["match_previous_short" if key=="long_edges" else "match_previous_long"]==expected_match
   if key=="short_edges":assert D(y["expected_bounded_neighbor_increment"])==D("0.0186")
   if key=="long_edges":assert (expr==D(before["short"]))==expected_match
   if key=="cumulative_edges":assert expr==D(before["long"])
 assert D(a["spanning_two_day_diff_D15_D17"])==D(row[2]["short"])-D(row[0]["short"])==D("0.0372")
 assert D(a["two_step_consistent_midpoint_candidate_D16"])==(D(row[0]["short"])+D(row[2]["short"]))/2==D("5.2362")
 assert D(a["printed_original_D16_two_physical_holdings"])==D(row[1]["short"])==D("5.1362")
 assert D(a["candidate_minus_original_printed"])==D("0.1000")
 assert a["original_13CI_d16_d17_long_pair"]=="429.6073/424.3711"
 assert a["original_13CI_d16_d17_short_pair"]=="5.1362/5.2548"
 for key in ("source_13CK_KRDB_D18_trailing_three_is_quarantined_not_decimal_normalized","only_scoped_six_printed_days","no_universal_recurrence_law","D16_emendation_to_midpoint_NOT_authorized"):
  assert a[key] is True
 assert e["reasoned_conclusion"]["two_digit_candidate_scope"]=="NUMERIC_CONJECTURE_ONLY_NOT_HISTORICAL_EDITED_SOURCE"
 assert e["reasoned_conclusion"]["editorial_typographical_cause"]=="UNPROVEN"
 assert e["reasoned_conclusion"]["common_ancestor_error"]=="UNPROVEN"
 for k in ("W_D16_same_day_C","NAJ_D17_same_day_C"):assert e["reasoned_conclusion"][k]=="UNBOUND"
 assert e["reasoned_conclusion"]["historical_calendar_formula_or_generic_rule"]=="UNPROVEN"
 scope=e["research_impact"]
 for k in ("new_original_crops","new_original_jpegs","new_physical_witnesses","new_registry_sources","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","new_independent_stemmatic_votes","algorithm_reopens"):assert scope[k]==0
 assert scope["open_or_blocked_issues"]==11 and scope["product"]=="CLOSED"
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0
 assert s["historical_audit"]["row_count"]==s["historical_audit"]["audited_row_count"]==222
 assert s["historical_audit"]["external_source_registry_total_unique_count"]==754
 assert any(x.startswith("13CL ") for x in s["historical_audit"]["current_focus"])
 assert l["binding"]["reviewed_state_version"]==s["schema_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"]
 assert any(h["revision_id"]=="TW-OPEN-0005-LOCAL-DOUBLE-DIFFERENCE-13CL" for h in issue["history"])
 assert any(x["id"]=="OMISSIONS-13CL-TWO-CONTROLS-20261022" for x in l["checkpoint_log"])
 assert len([i for i in l["issues"] if i["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS")])==11
 return True
if __name__=="__main__":
 assert check(load(E),load(STATE),load(LEDGER),load(REGISTRY),{k:load(v["path"]) for k,v in load(E)["exact_original_record_bindings"].items()})
 print("TIANWEN_13CL_TWO_LOCAL_RECEIVED_DIFFERENCE_CONTROLS=PASS")
