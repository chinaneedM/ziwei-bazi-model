#!/usr/bin/env python3
"""13AN NAJDA catalog book order vs work volume and digital image plan boundary."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13AN-NAJDA-GORYEOSA-128BOOK-MANUSCRIPT-DIGITIZATION-TARGET-R1.json";SH="docs/research/TIANWEN-13AN-NAJDA-GORYEOSA-SOURCE-SHARD-R1.json";M="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def verify():
 d=load(E);sh=load(SH);m=load(M);s=load("docs/PROJECT-CURRENT-STATE-R1.json");l=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 assert d["issue_id"]=="TW-OPEN-0005"
 c=d["na_japan_holding"]
 assert c["shelf"]=="282-0006" and c["set_physical_books"]==128
 assert c["child_book_order"]=="0052" and c["work_volume_52_mapping"]=="UNKNOWN"
 assert c["target_work_volume_in_book_0052"] is None and c["target_work_volume_in_book_0052_proven"] is False and c["original_folio_obtained"] is False and c["image_byte_sha256"] is None
 assert d["independent_witness_status"]["digitization_completed_by_2022"]=="NOT_ESTABLISHED"
 assert d["independent_witness_status"]["image_published_online"]=="NOT_ESTABLISHED_BY_SEARCH_RESULT_OR_PLAN"
 assert d["independent_witness_status"]["cross_print_numeric_vote"]==0
 assert d["non_promotions"]["independent_numeric_votes"]==d["non_promotions"]["original_images"]==d["non_promotions"]["algo_reopens"]==0
 assert len(sh["sources"])==2 and all(x["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY" and x["physical_glyph_authority"] is False for x in sh["sources"])
 assert m["combined_source_count"]>=754 and s["historical_audit"]["external_source_registry_total_unique_count"]==m["combined_source_count"]
 assert any(x["path"]==SH and x["source_count"]==2 and x["schema"]==sh["schema"] for x in m["shards"])
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,699,0)
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13AN ") for x in s["historical_audit"]["current_focus"])
 o=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert o["status"]=="OPEN" and all(x in o["source_refs"] for x in [E,SH,"docs/research/TIANWEN-13AN-NAJDA-GORYEOSA-128BOOK-MANUSCRIPT-DIGITIZATION-TARGET-R1.md"])
 assert any(x["event"]=="NAJDA_GORYEOSA_128BOOK_QING_MANUSCRIPT_DIGITIZATION_PLAN_VS_WORK52_MAPPING_GATE" for x in o["history"])
 assert any(x["id"]=="OMISSIONS-13AN-NAJDA-QING-MS-BOOK52-AND-2022-DIGITIZATION-FIREWALL-20261020" for x in l["checkpoint_log"])
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0
 return True
if __name__=="__main__":
 assert verify();print("TIANWEN_13AN_NAJDA_GORYEOSA_WORK_VOLUME_FIREWALL_PASS")
