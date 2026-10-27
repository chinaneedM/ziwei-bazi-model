#!/usr/bin/env python3
"""13AA NII union holdings exact volume52 boundary: no target glyph or edition claim."""
import json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13AA-UTOKYO-GORYEOSA-WORK52-NII-UNION-HOLDING-R1.json"
S="docs/research/TIANWEN-13AA-UTOKYO-GORYEOSA-NII-UNION-SOURCE-SHARD-R1.json"
M="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
def load(path):return json.loads((P/path).read_text(encoding="utf8"))
def verify():
 e=load(E);s=load(S);m=load(M)
 assert e["schema"]=="TIANWEN-13AA-UTOKYO-NII-UNION-GORYEOSA-WORK52-HOLDING-LOCATOR-R1" and e["issue_id"]=="TW-OPEN-0005"
 b=e["bibliographic_source"]
 assert b["ncid"]=="BC15973641" and b["reported_institution"]=="東京大学 総合図書館"
 assert (b["call_number"],b["exact_work_volume"],b["item_holding_identifier"])==("G23:194",52,"0008542011")
 assert b["set_extent"]=="81冊" and b["edition_impression_date"] is None and b["original_target_folio"] is None
 assert e["independent_catalog_comparator"]["set_extent"]=="80冊" and e["independent_catalog_comparator"]["explicit_same_plate_identity_confirmed"] is False
 assert e["tested_access_boundary"]["does_not_prove_holding_absence"] is True
 assert e["safety"]["institutional_union_metadata_only"] and e["safety"]["not_utokyo_firstparty_catalog_confirmation"] and e["safety"]["not_original_folio"] and e["safety"]["not_proof_of_print_independence"]
 assert [e["safety"][q] for q in ("independent_original_numeric_votes_added","transmission_graph_nodes_added","transmission_graph_edges_added","algorithm_reopens")]==[0,0,0,0]
 assert e["safety"]["source_registry_new_entries"]==1 and e["safety"]["open_research_issues"]==11 and e["safety"]["chart_product_r1"]=="CLOSED"
 assert len(s["sources"])==1 and s["sources"][0]["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY" and s["sources"][0]["physical_glyph_authority"] is False
 assert s["sources"][0]["evidence"]==E and s["sources"][0]["url"]=="https://ci.nii.ac.jp/ncid/BC15973641"
 assert m["root_source_count"]==647 and m["extension_source_count"]>=88 and m["combined_source_count"]>=735
 assert any(z["path"]==S and z["source_count"]==1 and z["schema"]==s["schema"] for z in m["shards"])
 st=load("docs/PROJECT-CURRENT-STATE-R1.json");le=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 assert st["schema_version"]==le["binding"]["reviewed_state_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,st["schema_version"].split(".")))>=(1,686,0)
 assert any(x.startswith("13AA ") for x in st["historical_audit"]["current_focus"])
 assert any(z.get("id")=="OMISSIONS-13AA-NII-UTOKYO-WORK52-EXACT-CATALOG-20261019" for z in le["checkpoint_log"])
 assert le["binding"]["latest_research_focus_prefix"]==st["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert st["historical_audit"]["external_source_registry_extension_count"]==m["extension_source_count"]
 assert st["historical_audit"]["external_source_registry_total_unique_count"]==m["combined_source_count"]
 issue=next(x for x in le["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"] and len(le["issues"])>=11
 assert le["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"])
 assert le["checkpoint_log"][-1]["state_version"]==st["schema_version"]
 return True
if __name__=="__main__":
 assert verify()
 print("TIANWEN_13AA_NII_UNION_CATALOG_BOUNDARY_PASS")
