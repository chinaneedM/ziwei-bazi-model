#!/usr/bin/env python3
"""Evidence firewall for first-party UTokyo source-specific oldbook inquiry and microform service."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13AM-UTOKYO-GORYEOSA-V52-EXACT-ITEM-INQUIRY-AND-MICRO-SPLIT-R1.json"; S="docs/research/TIANWEN-13AM-UTOKYO-OLD-BOOK-INQUIRY-MICRO-ACCESS-SOURCE-SHARD-R1.json"; M="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
def load(p):return json.loads((R/p).read_text(encoding="utf-8"))
def verify():
 e=load(E);sh=load(S);m=load(M);s=load("docs/PROJECT-CURRENT-STATE-R1.json");l=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 assert e["issue_id"]=="TW-OPEN-0005"
 assert [(x["ncid"],x["call_number"],x["registration"]) for x in e["exact_targets"]]==[("BC15973641","G23:194","0008542011"),("BC15670118","G23:12","0008535809")]
 assert all(x["original_folio_acquired"] is False and x["numeric_image"] is None for x in e["exact_targets"])
 a=e["provider_route"]
 assert a["official_inquiry_form"].endswith("/inquiry/inquiryform")
 assert a["actual_submission"] is a["automated_submission"] is a["library_reply"] is False
 assert "human_Captcha" in a["form_required_fields"]
 assert a["micro_can_export_USB"] is False and a["micro_original_copy_available"]=="NOT_VERIFIED_FOR_BOTH_EXACT_ITEMS"
 assert a["G23_prefix_alone_proves_rare"] is False
 assert e["boundaries"]["D16_in_print_and_manuscript_original"]=="UNREAD"
 assert e["boundaries"]["direct_historical_numeric_votes_added"]==e["boundaries"]["source_page_images_added"]==0
 assert e["counts"]["total"]==752 and m["combined_source_count"]>=752 and s["historical_audit"]["external_source_registry_total_unique_count"]==m["combined_source_count"]
 assert len(sh["sources"])==2 and all(x["physical_glyph_authority"] is False and x["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY" for x in sh["sources"])
 assert any(x["path"]==S and x["source_count"]==2 and x["schema"]==sh["schema"] for x in m["shards"])
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,698,0)
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert "13AM"==l["binding"]["latest_research_focus_prefix"]
 q=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert q["status"]=="OPEN" and all(x in q["source_refs"] for x in [E,S,"docs/research/TIANWEN-13AM-UTOKYO-GORYEOSA-V52-EXACT-ITEM-INQUIRY-AND-MICRO-SPLIT-R1.md"])
 assert any(x["event"]=="UTOKYO_V52_ORIGINAL_INQUIRY_FORM_AND_MICROFORM_SERVICE_SPLIT" for x in q["history"])
 assert any(x["id"]=="OMISSIONS-13AM-UTOKYO-SOURCE-ITEM-INQUIRY-AND-MICRO-SPLIT-20261020" for x in l["checkpoint_log"])
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0
 return True
if __name__=="__main__":assert verify();print("TIANWEN_13AM_SOURCE_SPECIFIC_INQUIRY_MICRO_SPLIT_PASS")
