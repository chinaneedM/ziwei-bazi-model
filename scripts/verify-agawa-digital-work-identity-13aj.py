#!/usr/bin/env python3
"""13AJ firstparty Agawa digital collection work-identity/edition-time fail-closed gate."""
import json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13AJ-AGAWA-DIGITAL-COLLECTION-YESHI-TIGANG-WORK-ID-R1.json";S="docs/research/TIANWEN-13AJ-AGAWA-DIGITAL-HIERARCHY-SOURCE-SHARD-R1.json";M="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
def load(p):return json.loads((P/p).read_text(encoding="utf-8"))
def verify():
 e=load(E);d=e["controlled_item"];c=e["collection"];q=e["comparison"];m=load(M);s=load(S)
 assert e["issue_id"]=="TW-OPEN-0005" and e["authority_grade"].endswith("NO_ORIGINAL_NUMERIC_GLYPH")
 assert c["visible_subcollection_title_cards_at_review"]==69 and c["cards_are_not_entire_physical_library_collection"]
 assert c["absent_title_claim"]=="NOT_DISPLAYED_IN_THIS_VISIBLE_SUBCOLLECTION_LIST_ONLY"
 assert c["physical_G2312_absence_proven"] is False and c["physical_G23194_absence_proven"] is False
 assert c["negative_catalog_inference_authorized"] is False
 assert d["title"]=="麗史提綱" and d["declared_juan_count"]==23 and d["creator"]=="兪棨"
 assert d["call_number"]=="A00:4671" and d["preface_dated"]=="顕宗8 [1667] 序"
 assert d["current_copy_label"]=="後印本" and d["edition_date_from_preface_proven"] is False
 assert d["source_item_identical_to_Goryeosa"] is False and d["source_item_original_Goryeosa_vol52"] is False
 assert d["source_item_numerical_field_D16"] is None and d["original_images_page_by_page_collated"] is False
 assert d["philological_identity"]=="麗史提綱_23JUAN_DISTINCT_FROM_高麗史_137JUAN"
 assert {x["call_number"] for x in e["physically_targeted_items"]}=={"G23:12","G23:194"}
 assert all(x["original_target_image"] is False and x["day16_value"] is None and x["provenance"]=="UNKNOWN" for x in e["physically_targeted_items"])
 assert q["preface_date_not_printing_date"] and q["near_homograph_not_identity"] and q["visible_titles_not_full_catalog"]
 assert q["metadata_hierarchy_supports_collection_membership_for_YeshiTigang_only"]
 assert q["metadata_hierarchy_supports_collection_membership_for_two_G23_targets"] is False
 assert q["D16_target_original_images_added"]==q["independent_numeric_votes_added"]==q["chart_algorithm_reopens"]==0
 assert q["source_registry_delta"]==1 and m["root_source_count"]==647
 assert m["extension_source_count"]==100 and m["combined_source_count"]==747
 assert len(s["sources"])==1 and s["sources"][0]["physical_glyph_authority"] is False
 assert s["sources"][0]["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY"
 assert any(x["path"]==S and x["schema"]==s["schema"] and x["source_count"]==1 for x in m["shards"])
 st=load("docs/PROJECT-CURRENT-STATE-R1.json");l=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 assert st["schema_version"]==l["binding"]["reviewed_state_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,st["schema_version"].split(".")))>=(1,695,0)
 assert st["historical_audit"]["external_source_registry_total_unique_count"]==747
 assert st["historical_audit"]["external_source_registry_extension_count"]==100
 assert st["historical_audit"]["current_focus"][-1].startswith("13AJ ")
 assert l["binding"]["latest_research_focus_prefix"]=="13AJ"
 assert l["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"])
 assert len(l["issues"])==11 and all(x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS") for x in l["issues"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0"
 assert all(x in issue["source_refs"] for x in (E,"docs/research/TIANWEN-13AJ-AGAWA-DIGITAL-COLLECTION-YESHI-TIGANG-WORK-ID-R1.md",S))
 assert any(x["event"]=="AGAWA_FIRSTPARTY_DIGITAL_YE_SHI_TIGANG_VS_GORYEOSA_WORK_ID_FENCE" for x in issue["history"])
 assert l["checkpoint_log"][-1]["state_version"]==st["schema_version"]
 assert st["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and st["invariants"]["algorithm_reopen_count"]==0
 return True
if __name__=="__main__":
 assert verify()
 print("TIANWEN_13AJ_AGAWA_DIGITAL_WORK_ID_FENCE_PASS")
