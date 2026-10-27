#!/usr/bin/env python3
"""13AI evidence-scoped bibliographic supplement bridge, fail closed."""
import json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13AI-AGAWA-CATALOG-EDITORIAL-BRIDGE-AND-OPAC-LOCATORS-R1.json"
def load(path): return json.loads((P/path).read_text(encoding="utf-8"))
def verify():
 e=load(E); s=load("docs/PROJECT-CURRENT-STATE-R1.json"); l=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 m=load("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
 ag=load("docs/research/TIANWEN-13AG-UTOKYO-AGAWA-KOREAN-COLLECTION-SOURCE-SHARD-R1.json")
 ah=load("docs/research/TIANWEN-13AH-AGAWA-OLD-CATALOG-G23-NANKI-SOURCE-SHARD-R1.json")
 assert e["issue_id"]=="TW-OPEN-0005" and e["evidence_grade"].endswith("ONLY")
 u=e["utokyo_firstparty_collection"]
 assert u["two_catalog_entries_both_listed"] is True
 assert {u["earlier_catalog_source_emitted_opac_bibid"],u["later_list_source_emitted_opac_bibid"]}=={"2003433569","2003433575"}
 assert u["complete_OPAC_item_detail_retrieved"] is False and u["earlier_catalog_original_page_retrieved"] is False
 assert u["later_catalog_original_page_retrieved"] is False
 a=e["utokyo_librarian_referral"]
 assert a["archive_case"]=="ASK0000025540" and a["operative_short_phrase"]=="書写目録を増補した"
 assert a["librarian_describes_supplement_to_prior_catalog"] is True
 assert a["precise_prior_manuscript_or_koseki_copy_identity_proven"] is False
 assert a["exact_entry_by_entry_derivation_proven"] is False and a["direct_copy_stemma_proven"] is False
 k=e["prior_related_bibliographic_work"]
 assert k["ncid"]=="BA63404722" and k["utokyo_separate_physical_copy_proven"] is False
 assert k["kyushu_and_utokyo_are_two_independent_catalog_physical_copies_proven"] is False
 assert {x["call_number"] for x in e["unrelated_target_holdings"]}=={"G23:12","G23:194"}
 assert all(x["agawa"]=="UNVERIFIED" and x["nanki"]=="UNVERIFIED" and x["D16_original"] is None for x in e["unrelated_target_holdings"])
 b=e["boundaries"]
 assert b["cross_original_numeric_votes"]==b["new_Goryeosa_folio_images"]==b["new_external_sources"]==b["algorithm_reopens"]==0
 assert b["catalog_inclusion_of_Goryeosa"]==b["catalog_exclusion_of_Goryeosa"]=="UNKNOWN"
 assert b["external_sources_remain"]==746 and m["combined_source_count"]>=b["external_sources_remain"]
 assert m["root_source_count"]>=647 and m["extension_source_count"]>=99
 assert b["graph_nodes_added"]==b["graph_edges_added"]==0 and b["product"]=="CLOSED"
 ids={x["source_id"] for x in ag["sources"]+ah["sources"]}
 assert all(x in ids for x in e["referenced_registry_source_ids"])
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,694,0)
 assert any(x.startswith("13AI ") for x in s["historical_audit"]["current_focus"])
 assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert len(l["issues"])>=11 and {"TW-OPEN-%04d"%k for k in range(1,12)}<={x["id"] for x in l["issues"]}
 i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert i["id"]=="TW-OPEN-0005"
 assert all(x in i["source_refs"] for x in (E,"docs/research/TIANWEN-13AI-AGAWA-CATALOG-EDITORIAL-BRIDGE-AND-OPAC-LOCATORS-R1.md"))
 assert any(x["event"]=="UTOKYO_AGAWA_1998_LIST_OFFICIAL_SUPPLEMENT_DESCRIPTION_AND_DUAL_OPAC_BIBLIOGRAPHIC_IDS" for x in i["history"])
 assert any(x["id"]=="OMISSIONS-13AI-AGAWA-LIBRARIAN-CATALOG-SUPPLEMENT-BIBIDS-20261020" for x in l["checkpoint_log"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0
 return True
if __name__=="__main__":
 assert verify()
 print("TIANWEN_13AI_AGAWA_CATALOG_EDITORIAL_BRIDGE_PASS")
