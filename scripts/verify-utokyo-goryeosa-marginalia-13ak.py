#!/usr/bin/env python3
"""Fail-closed validation of 13AK NII printed volume marginalia and institutional-name comparison."""
import json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13AK-GORYEOSA-UTOKYO-G23194-MARGINALIA-CHOGANG-CONTROL-R1.json"; S="docs/research/TIANWEN-13AK-CHOGANG-ACADEMY-SECONDARY-REFERENCE-SHARD-R1.json"; M="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
def load(p):return json.loads((P/p).read_text(encoding="utf-8"))
def verify():
 e=load(E); q=e["printed_copy"]; a=e["academy_reference"]; l=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json");st=load("docs/PROJECT-CURRENT-STATE-R1.json");m=load(M);sh=load(S)
 assert e["issue_id"]=="TW-OPEN-0005"
 assert q["ncid"]=="BC15973641" and q["call_number"]=="G23:194" and q["volume52_registration"]=="0008542011"
 assert q["published_place"]=="UNKNOWN" and q["published_date"]=="UNKNOWN"
 marks=q["explicit_copy_annotations"]
 assert len(marks)==7
 assert [(x["work_volume"],x["text"]) for x in marks]==[(114,"草江書院冊"),(124,"草江書院冊"),(2,"官上"),(10,"光州校上"),(30,"光州校上"),(110,"光州校上"),(127,"光卯校□□")]
 assert all(x["original_image_observed"] is False and x["medium"]=="墨書" for x in marks)
 assert all(x["work_volume"]!=52 for x in marks)
 assert q["mark_in_target_volume52"]=="NOT_ATTESTED_BY_THE_CATALOG_EXPLICIT_VOLUME_LOCATORS"
 assert not q["handwritten_marks_equivalent_to_printer_colophon"]
 assert not q["one_collection_level_mark_implies_volume52_ownership"]
 assert not q["mark_dates_current_print_run"]
 assert a["foundation_year"]==1611 and a["dismantling_year"]==1868
 assert a["semantic_referent_identity"]=="UNRESOLVED_SAME_STRING_NOT_DIRECT_PROVENANCE"
 assert not a["specific_UTokyo_copy_from_this_institution_proven"]
 assert not a["foundation_year_independent_earliest_date_of_this_printed_copy"]
 assert e["manuscript_copy"]["call_number"]=="G23:12"
 assert e["manuscript_copy"]["target_D16_original"] is None
 assert len(e["targets"])==2 and all(x["direct_folio_image"] is False and x["D16_original"] is None for x in e["targets"])
 n=e["non_promotions"]
 assert all(n[x] is False for x in ["coincidental_academy_title_is_direct_copy_provenance","ink_annotation_equates_to_printed_colophon","annotations_outside_volume52_are_glyph_evidence_for_volume52","date_1611_is_edition_date","prior_same_source_double_counted_as_new_original"])
 assert n["number_of_new_sources"]==1 and n["registry_total_after"]==748
 assert n["cross_print_independent_numeric_votes_added"]==n["target_original_folios_obtained"]==n["algorithm_reopens"]==0
 assert n["new_graph_nodes"]==n["new_graph_edges"]==0
 assert m["root_source_count"]>=647 and m["extension_source_count"]>=101 and m["combined_source_count"]>=748
 assert len(sh["sources"])==1 and sh["sources"][0]["physical_glyph_authority"] is False
 assert sh["sources"][0]["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY"
 assert any(x["path"]==S and x["schema"]==sh["schema"] and x["source_count"]==1 for x in m["shards"])
 assert st["schema_version"]==l["binding"]["reviewed_state_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,st["schema_version"].split(".")))>=(1,696,0)
 assert st["historical_audit"]["external_source_registry_total_unique_count"]==m["combined_source_count"]
 assert st["historical_audit"]["external_source_registry_extension_count"]==m["extension_source_count"]
 assert any(x.startswith("13AK ") for x in st["historical_audit"]["current_focus"])
 assert l["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==st["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert {"TW-OPEN-%04d"%i for i in range(1,12)}<={x["id"] for x in l["issues"]}
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert all(x in issue["source_refs"] for x in [E,"docs/research/TIANWEN-13AK-GORYEOSA-UTOKYO-G23194-MARGINALIA-CHOGANG-CONTROL-R1.md",S])
 assert any(x["event"]=="UTOKYO_G23194_VOLUME_SCOPED_INK_ANNOTATIONS_AND_CHOGANG_ACADEMY_HOMONYM_SCOPE" for x in issue["history"])
 assert any(x["id"]=="OMISSIONS-13AK-UTOKYO-CHOGANG-INK-MARK-NONPROMOTION-20261020" for x in l["checkpoint_log"])
 assert st["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and st["invariants"]["algorithm_reopen_count"]==0
 return True
if __name__=="__main__":
 assert verify()
 print("TIANWEN_13AK_UTOKYO_G23194_CHOGANG_VOLUME_INK_NONPROMOTION_PASS")
