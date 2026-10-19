#!/usr/bin/env python3
"""13AC Tokyo University firstparty public service: applies only after item shelf crossbind."""
import json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13AC-UTOKYO-GORYEOSA-WORK52-FIRSTPARTY-LIBRARY-ACCESS-POLICY-R1.json";SHARD="docs/research/TIANWEN-13AC-UTOKYO-GORYEOSA-ACCESS-SERVICE-SOURCE-SHARD-R1.json";M="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
RARE="https://www.lib.u-tokyo.ac.jp/ja/library/general/user-guide/materials/rare";STACK="https://www.lib.u-tokyo.ac.jp/ja/library/general/user-guide/materials/stack-classics"
def load(x):return json.loads((P/x).read_text(encoding="utf8"))
def check(e=None):
 if e is None:e=load(E)
 s=load(SHARD);m=load(M)
 assert e["schema"]=="TIANWEN-13AC-UTOKYO-WORK52-FIRSTPARTY-GENERAL-LIBRARY-ACCESS-POLICY-R1"
 t=e["target_item"]
 assert (t["call_number"],t["volume"],t["individual_registration"],t["nii_ncid"])==("G23:194",52,"0008542011","BC15973641")
 assert t["exact_storage_location"] is None and t["digital_original_object_id"] is None and t["d16_d18_original_folio"] is None
 assert t["utokyo_opac_item_firstparty_confirmed"] is False
 p=e["official_services"]
 assert [q["url"] for q in p]==[RARE,STACK]
 assert p[0]["explicit_special_prefixes"]==["A00","A05","A100","A150"]
 assert p[0]["g23_not_on_special_prefix_list"] and p[0]["does_not_prove_item_storage_or_availability"]
 assert p[1]["general_public_in_house_reading"] is True and p[1]["general_public_staff_retrieval"] is True
 assert p[1]["general_public_stack_entry"] is False and p[1]["general_public_home_loan"] is False
 assert p[1]["self_service_copier_allowed"] is False and p[1]["on_site_photography_normally_prohibited"] is True
 assert p[1]["limited_staff_approved_photos_per_day_upper_bound"]==10 and p[1]["exact_item_applies_only_if_storage_confirmed"] is True
 r=e["restrictions"]
 assert all(r[x] is True for x in ("no_request_submitted","no_record_specific_firstparty_opac_confirmed","no_public_scan_for_this_item_found","not_goryeosa_original_glyph","not_evidence_for_impression_year","not_a_new_independent_numeric_witness"))
 assert all(r[x]==0 for x in ("physical_numeric_votes_added","genealogy_nodes_added","genealogy_edges_added","algorithm_reopens"))
 assert r["new_metadata_source_records"]==2 and r["unresolved_research_issues"]==11 and r["product_r1"]=="CLOSED"
 assert len(s["sources"])==2
 assert all(x["url"] in (RARE,STACK) and x["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY" and x["physical_glyph_authority"] is False and x["evidence"]==E for x in s["sources"])
 assert m["root_source_count"]==647 and m["extension_source_count"]>=90 and m["combined_source_count"]>=737
 assert any(x["path"]==SHARD and x["schema"]==s["schema"] and x["source_count"]==2 for x in m["shards"])
 st=load("docs/PROJECT-CURRENT-STATE-R1.json");le=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 assert tuple(map(int,st["schema_version"].split(".")))>=(1,688,0)
 assert st["schema_version"]==le["binding"]["reviewed_state_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert any(q.startswith("13AC ") for q in st["historical_audit"]["current_focus"])
 assert any(q.get("id")=="OMISSIONS-13AC-UTOKYO-FIRSTPARTY-LIBRARY-ACCESS-20261019" for q in le["checkpoint_log"])
 assert st["historical_audit"]["external_source_registry_total_unique_count"]==m["combined_source_count"]
 issue=next(x for x in le["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"] and len(le["issues"])>=11
 return True
if __name__=="__main__":
 check();print("TIANWEN_13AC_FIRSTPARTY_POLICY_SCOPE_PASS")
