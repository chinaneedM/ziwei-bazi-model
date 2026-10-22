#!/usr/bin/env python3
"""13CV: exact KRDB v52 D16 received text, math conjecture and forward-only link erratum."""
import json
from decimal import Decimal
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CV-GORYEOSA-KRDB-V52-D16-RECEIVED-ERRATUM-R1.json";S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
OLD="docs/research/TIANWEN-13CU-NCL03130-ZHI-MISSING-RANGE-GLYPH-ROI-R1.json"
def load(path):return json.loads((R/path).read_text(encoding="utf-8"))
def check(e,s,l,old):
 assert e["schema"]=="TIANWEN-13CV-GORYEOSA-KRDB-V52-D16-RECEIVED-SOURCE-ERRATUM-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["follows"]==OLD
 src=e["first_party_direct_target"]
 assert src["url"]=="https://db.history.go.kr/goryeo/level.do?levelId=kr_052_0010_0010_0020_0010&types=o"
 assert (src["whole_work_juan"],src["genre_juan"],src["section"],src["field"])==(52,6,"授時曆立成","日差加一秒八十六少")
 assert src["read_mode"]=="OFFICIAL_ONLINE_RECEIVED_TRANSCRIPTION_NOT_NATIVE_PHYSICAL_FOLIO"
 assert [(x["day"],x["received_literal"],x["numeric"]) for x in src["adjacent_day_readings"]]==[(15,"五分二一七六","5.2176"),(16,"五分一三六二","5.1362"),(17,"五分二五四八","5.2548")]
 er=e["forward_only_link_erratum"]
 assert er["wrong_url_as_preserved_in_13cu"]==old["text_structure"]["url"]
 assert "kr_051_" in er["wrong_url_as_preserved_in_13cu"]
 assert er["correct_url"]==src["url"] and er["prior_report_not_rewritten"] is True
 assert er["status"]=="URL_CORRECTED_IN_NEW_CHECKPOINT_ONLY"
 a=e["independent_arithmetic_lanes"]
 A,B,C=map(Decimal,(a["d15"],a["d16_printed_or_received"],a["d17"]))
 assert (A,B,C)==(Decimal("5.2176"),Decimal("5.1362"),Decimal("5.2548"))
 assert (B-A,C-B,(A+C)/2,(A+C)/2-B)==tuple(map(Decimal,(a["observed_d15_to_d16"],a["observed_d16_to_d17"],a["inferred_d16_by_both_neighbors"],a["neighbor_interpolation_delta"])))
 assert Decimal(a["recurrence_header_increment"])==Decimal("0.0186")
 sf=e["source_scope_firewalls"]
 assert sf["modern_official_received_krdb_text"]=="ONE_TRANSCRIPTION_CHANNEL_NOT_ADDITIONAL_PHYSICAL_COPY"
 assert sf["direct_third_historical_original_count_new"]==0
 assert sf["waseda_original_d16"]==sf["naj_original_d16"]==B.__str__()
 assert sf["modern_krdb_d16_variant_independently_original"] is False and sf["force_corrected_d16_as_printed"] is False
 assert sf["ncl_mirror_p7_zhi_range_connector"]=="UNRESOLVED"
 assert sf["taiwan_ncl_208_03130_firstparty_catalog_item"]==sf["qing_old_vs_1905_d16_folio_hand"]=="UNBOUND"
 assert sf["ncl_direct_detail_found"] is False
 assert not e["transmission_impact"]["nodes_added_or_strengthened"] and not e["transmission_impact"]["edges_supported"]
 z=e["snapshot"]
 assert (z["matrix"],z["audited"],z["sources"],z["graph_nodes"],z["graph_edges"],z["unresolved_risks"],z["chart"],z["algorithm_reopens"])==(222,222,754,252,238,11,"CLOSED",0)
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert any(x.startswith("13CV ") for x in s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"] in ("13CV","13CW")
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13CV-KRDB-V52-D16-ERRATUM" for x in issue["history"])
 assert any(x.get("event")=="ISSUE_REVISION" and x.get("revision_id")=="TW-OPEN-0005-13CV-KRDB-V52-D16-ERRATUM" for x in issue["history"])
 assert "CURRENT ACTION:" in issue["next_action"]
 assert any(x.get("id")=="OMISSIONS-13CV-KRDB-V52-D16-ERRATUM-20261022" for x in l["checkpoint_log"])
 assert sum(x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS") for x in l["issues"])==11
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 return True
if __name__=="__main__":
 assert check(load(E),load(S),load(L),load(OLD))
 print("TIANWEN_13CV_KRDB_V52_D16_RECEIVED_LINK_ERRATUM=PASS")
