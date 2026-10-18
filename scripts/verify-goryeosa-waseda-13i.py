#!/usr/bin/env python3
"""13I: Waseda independent item-level catalog without invented vol52 target glyph."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13I-WASEDA-RI06-02809-GORYEOSA-ORIGINAL-ACCESS-AND-NCL-PROXY-CROSSWALK-R1.json"
SH="docs/research/TIANWEN-13I-WASEDA-GORYEOSA-FIRSTPARTY-SOURCE-SHARD-R1.json"
def rd(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check_evidence(e):
 a=e["waseda_first_party"]; b=e["ncl_commons_proxy"]; c=e["adjudication"]
 assert e["schema"]=="TIANWEN-13I-WASEDA-GORYEOSA-ORIGINAL-ACCESS-AND-NCL-PROXY-FIREWALL-R1"
 assert a["catalog_shelfmark"]=="リ06 02809" and a["catalog_title"]=="高麗史. 目録,1-137"
 assert a["catalog_physical_books"]==80 and a["archive_listed_image_groups"]==80
 assert a["catalog_divisions"]["志"]=="47-85" and a["work_volume52_in_catalogued_range"] is True
 assert a["edition_impression_year"] is None and a["physical_copy_specific_year"] is None
 assert a["volume52_physical_book_index"] is None and a["volume52_exact_online_image"] is None and a["volume52_verified_figure"] is None
 assert a["d16_original_glyph"] is None and a["d18_original_glyph"] is None and a["original_page_sha256"] is None
 assert a["independent_physical_holding_catalogued"] is True and a["independent_numeric_glyph_witness_verified"] is False
 assert b["commons_upload_comment_original_file_goryeosa"]=="03117_8.pdf"
 assert b["commons_upload_comment_original_file_gukjobogam"]=="03799_2.pdf"
 assert b["catalog_call_number_goryeosa"]=="208 03130" and b["catalog_call_number_gukjobogam"]=="208 03136"
 assert b["uploader_original_filename_not_same_as_catalog_shelfmark"] is True
 assert b["first_party_filename_to_shelfmark_crosswalk_verified"] is False
 assert b["underlying_image_to_physical_copy_disproved"] is False and b["filename_difference_proves_misidentification"] is False
 assert c["waseda_firstparty_library_catalog_proves_item_description"] is True
 assert c["waseda80_image_groups_not80_independent_original_witnesses"] is True
 assert c["waseda_catalog_proves_1454_edition"] is False and c["waseda_catalog_binds_work52_to_specific_book_or_folio"] is False
 assert c["ncl_filename_difference_not_a_proven_catalog_defect"] is True
 assert c["gained_original_d16_d18_glyph_votes"]==c["gained_cross_copy_numeric_votes"]==c["new_proven_direct_transmission_edges"]==c["algorithms_reopened"]==0
 assert c["g893_existing_same_copy_target_source_readings"]==5 and c["g893_existing_six_control_target_count"]==6
 assert c["unresolved_issue_count"]==11 and c["deterministic_chart_r1"]=="CLOSED"
def verify():
 e=rd(E);check_evidence(e)
 sh=rd(SH); m=rd("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
 s=rd("docs/PROJECT-CURRENT-STATE-R1.json");l=rd("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 assert sh["schema"]=="TIANWEN-13I-WASEDA-GORYEOSA-FIRSTPARTY-SOURCE-SHARD-R1" and len(sh["sources"])==1
 z=sh["sources"][0]
 assert z["physical_glyph_authority"] is False and z["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY" and z["evidence"]==E
 assert z["url"]==e["waseda_first_party"]["catalog_url"]
 assert any(q["path"]==SH and q["schema"]==sh["schema"] and q["source_count"]==1 for q in m["shards"])
 assert m["combined_source_count"]==s["historical_audit"]["external_source_registry_total_unique_count"]>=731
 assert m["extension_source_count"]>=84 and m["root_source_count"]==647
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(q.startswith("13I ") for q in s["historical_audit"]["current_focus"])
 issue=next(q for q in l["issues"] if q["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and all(p in issue["source_refs"] for p in (E,"docs/research/TIANWEN-13I-WASEDA-RI06-02809-GORYEOSA-ORIGINAL-ACCESS-AND-NCL-PROXY-CROSSWALK-R1.md",SH))
 assert len(l["issues"])==11 and all(q["status"]!="RESOLVED_WITH_EVIDENCE" for q in l["issues"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 assert set(l["checkpoint_log"][-1]["reviewed_issue_ids"])=={q["id"] for q in l["issues"]}
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0
 return {"status":"PASS","registered_sources":m["combined_source_count"],"new_target_glyph_votes":0}
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False))
