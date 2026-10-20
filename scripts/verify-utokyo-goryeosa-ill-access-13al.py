#!/usr/bin/env python3
"""Verify 13AL UTokyo exact-items vs conditional institutional ILL access."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13AL-UTOKYO-GORYEOSA-W52-ILL-REMOTE-COPY-ACCESS-ROUTE-R1.json";S="docs/research/TIANWEN-13AL-UTOKYO-GORYEOSA-ILL-ACCESS-SOURCE-SHARD-R1.json";M="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
def load(p):return json.loads((R/p).read_text(encoding="utf-8"))
def verify():
 e=load(E); sh=load(S);m=load(M);st=load("docs/PROJECT-CURRENT-STATE-R1.json"); l=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 assert e["issue_id"]=="TW-OPEN-0005"
 assert [(x["ncid"],x["call_number"],x["registration"]) for x in e["targets"]]==[("BC15973641","G23:194","0008542011"),("BC15670118","G23:12","0008535809")]
 assert all(x["direct_original_target_image"] is False and x["original_D16"] is None for x in e["targets"])
 a=e["access_routes"]
 assert a["remote_individual_direct_request"]=="NOT_ACCEPTED_BY_PROVIDER"
 assert a["japan_domestic_public_library"]=="LIBRARY_MEDIATED_COPIES_ONLY_CONDITIONAL"
 assert a["foreign_library"]=="LIBRARY_MEDIATED_ONLY_AND_SOLE_DOMESTIC_HOLDING_TEST_NOT_VERIFIED"
 assert a["request_sent"] is a["approval_received"] is a["original_scan_captured"] is False
 assert e["provenance_fences"]["direct_individual_ill_available"] is False
 assert e["non_promotions"]["independent_original_numeric_votes_added"]==0
 assert e["non_promotions"]["registry_total"]<=m["combined_source_count"]==st["historical_audit"]["external_source_registry_total_unique_count"]
 assert m["extension_source_count"]>=103 and len(sh["sources"])==2
 assert all(x["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY" and x["physical_glyph_authority"] is False for x in sh["sources"])
 assert any(x["path"]==S and x["source_count"]==2 and x["schema"]==sh["schema"] for x in m["shards"])
 assert st["schema_version"]==l["binding"]["reviewed_state_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,st["schema_version"].split(".")))>=(1,697,0)
 assert l["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]=="13AL"
 assert st["historical_audit"]["current_focus"][-1].startswith("13AL ")
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and all(x in issue["source_refs"] for x in [E,S,"docs/research/TIANWEN-13AL-UTOKYO-GORYEOSA-W52-ILL-REMOTE-COPY-ACCESS-ROUTE-R1.md"])
 assert any(x["event"]=="UTOKYO_FIRSTPARTY_ILL_NONMEMBER_REMOTE_COPY_GATE_AND_V52_CONDITIONAL_ACQUISITION" for x in issue["history"])
 assert any(x["id"]=="OMISSIONS-13AL-UTOKYO-ILL-AND-PERSONAL-REMOTE-COPY-GATE-20261020" for x in l["checkpoint_log"])
 assert st["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and st["invariants"]["algorithm_reopen_count"]==0
 return True
if __name__=="__main__":
 assert verify()
 print("TIANWEN_13AL_UTOKYO_GORYEOSA_ILL_ROUTE_PASS")
