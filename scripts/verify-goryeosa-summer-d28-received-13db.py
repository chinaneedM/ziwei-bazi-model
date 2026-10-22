#!/usr/bin/env python3
"""13DB: source-scoped modern received D28 summer outlier, not an ancient glyph or chart defect."""
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13DB-GORYEOSA-SUMMER-D28-RECEIVED-XINGDU-OUTLIER-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p): return json.loads((R/p).read_text(encoding="utf-8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13DB-GORYEOSA-SUMMER-D28-RECEIVED-XINGDU-ANOMALY-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["research_status"]=="NEW_SUBTARGET_REQUIRES_ORIGINAL_PAGE_COLLATION"
 w=e["witness_scope"]
 assert len(w["witnesses"])==2 and all(x["original_folio_examined"] is False for x in w["witnesses"])
 assert w["two_websites_not_two_independent_physical_or_early_witnesses"] and w["original_glyph_authority"] is False
 assert w["textual_independence"]=="UNPROVEN" and w["original_1909_summer_folio"]=="NOT_COLLATED"
 rows=e["received_summer_rows"]
 assert [x["day"] for x in rows]==[27,28,29]
 assert [x["short_literal"] for x in rows]==["四分八七三六","四分八八九八","四分九〇六〇"]
 assert [x["long_literal"] for x in rows]==["三百五十九三八三七","三百五十四五一〇一","三百四十九六二〇三"]
 assert [x["cumulative_literal"] for x in rows]==["一萬一千四百八六三八五九","一萬一千八百四五七六九六","一萬二千二百〇〇二七九七"]
 assert [x["xingdu_literal"] for x in rows]==["初度九十六四〇六二","初度九十九四五四九","初度九十六五〇三八"]
 short=[Decimal(x["short"]) for x in rows]
 long=[Decimal(x["long"]) for x in rows]
 cum=[Decimal(x["cumulative"]) for x in rows]
 received=[Decimal(x["xingdu"]) for x in rows]
 a=e["local_arithmetic"]
 assert long[0]-long[1]==short[0]==Decimal(a["summer_long27_minus_long28"])
 assert long[1]-long[2]==short[1]==Decimal(a["summer_long28_minus_long29"])
 assert cum[1]-cum[0]==long[0]==Decimal(a["cumulative28_minus_cumulative27"])
 assert cum[2]-cum[1]==long[1]==Decimal(a["cumulative29_minus_cumulative28"])
 derived=[(Decimal("1")-x/Decimal("10000")).quantize(Decimal("0.000001"),rounding=ROUND_HALF_UP) for x in long]
 assert [str(x) for x in derived]==[a["day27_derived_xingdu_6_places"],a["day28_derived_xingdu_6_places"],a["day29_derived_xingdu_6_places"]]
 assert received[0]==derived[0] and received[2]==derived[2] and received[1]!=derived[1]
 assert received[1]-derived[1]==Decimal(a["day28_received_minus_candidate"])==Decimal("0.030000")
 assert a["day28_candidate_literal_only"]=="初度九十六四五四九"
 assert a["day28_received_literal_preserved"]=="初度九十九四五四九"
 assert a["original_emendation_authorized"] is False and a["alleged_ancient_printing_defect_proven"] is False
 assert e["adjudication"]["status"]=="RECEIVED_DIGITAL_TEXT_INTERNAL_NUMERIC_OUTLIER_ORIGINAL_UNCOLLATED"
 assert e["adjudication"]["differentiated_from_13DA"]=="SUMMER_D28_XINGDU_FIELD_NOT_WINTER_D16_SHORT_COLUMN"
 for key in ("new_independent_original_witnesses","new_source_registry_entries","new_genealogy_edges","new_matrix_rows","algorithm_reopens"):
  assert e["adjudication"][key]==0
 imp=e["impact"]
 assert (imp["historical_matrix_rows"],imp["audited_rows"],imp["registry_sources"],imp["genealogy_nodes"],imp["genealogy_edges"],imp["open_or_blocked_issues"])==(222,222,754,252,238,11)
 assert imp["deterministic_chart"]=="CLOSED" and imp["algorithm_reopens"]==0
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13DB ") for x in s["historical_audit"]["current_focus"]), "13DB archival checkpoint must be retained"
 i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert i["status"]=="OPEN" and E in i["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13DB-SUMMER-D28-RECEIVED-OUTLIER" for x in i["history"])
 assert any(x.get("id")=="OMISSIONS-13DB-GORYEOSA-SUMMER-20261023" for x in l["checkpoint_log"])
 assert sum(x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS") for x in l["issues"])==11
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 return True
if __name__=="__main__":
 assert check(load(E),load(S),load(L))
 print("TIANWEN_13DB_GORYEOSA_SUMMER_D28_RECEIVED_OUTLIER_SCOPE=PASS")
