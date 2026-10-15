#!/usr/bin/env python3
"""12WH: completed first-party SBB 38-canvas source receipt and print-vote firewall."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12WH-SBB1827-38-CANVAS-COVERAGE-VERDICT-AND-NLC-ACCESS-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
def req(x,msg):
 if not x:raise ValueError(msg)
def validate(r,st):
 req(r["schema"]=="TIANWEN-12WH-SBB1827-ACTUAL-IIIF38-METS-COVERAGE-VERDICT-R1","schema")
 c=r["receipt"]
 req((c["workflow_run_id"],c["workflow_job_id"],c["artifact_id"])==(38721590423,116377200692,11967090494),"real action receipt")
 req(c["head_sha"]=="edd29a80484fa6d89aebf5eac6a8ebc402326f65" and c["workflow_status"]=="completed_success","exact running HEAD")
 req(c["artifact_zip_sha256_reported_by_github"]=="0a8595c713fcccdf79330661b72334eaeff7aa689c71e5992cfe4e70c032519b" and c["artifact_zip_independently_redownloaded_and_rehashed"] is False,"zip scope")
 m,n=c["manifest"],c["mets"]
 req((m["http"],m["bytes"],m["canvas_count"],m["iiif_ranges_count"])==(200,69638,38,18),"manifest measurement")
 req(m["sha256"]=="db26dd7d790c66faddc46ce542354396a30a1bb1bba70b9be011e6d57db27b82","manifest SHA")
 req(n["sha256"]=="c30688453d2c9540be407805b9c41d88ffc4e716d0bcb8dd0fdea9349c2cb9d8" and n["bytes"]==73209,"METS digest")
 req(n["struct_map_types"]==["LOGICAL","PHYSICAL"],"two SBB source maps")
 req(len(m["iiif_range_labels_in_order"])==18,"all 18 IIIF ranges")
 expected=("野獲編　巻首　巻一","野獲編　補遺卷一","野獲編總目 (Beispielseiten)","萬厯野獲編序")
 req(all(x in m["iiif_range_labels_in_order"] for x in expected),"source named scope")
 req(m["canvas_label_juan20_keyword_hits"]==0 and m["range_label_juan20_keyword_hits"]==0 and n["juany20_keyword_div_label_hits"]==0,"no labelled vol20")
 w=c["nlc"]
 req(w["status"]=="ACCESS_OR_SOURCE_PARSE_BOUNDARY_NO_ABSENCE_INFERENCE" and w["item_query_sent"] is False,"national catalogue access boundary")
 req(w["absence_of_wenzhou_1827_1869_holdings_inferred"] is False,"NLC timeout is not a cataloguing result")
 a=r["adjudication"]
 req(a["vol20_declared_as_source_sample_section"] is False and a["all_38_source_images_manually_reviewed"] is False,"no all-page human review")
 req(a["catalogued_paper_book_has_no_juan20"] is False and a["original_juan20_article_target_leaf_attested"] is False,"sample != physical missing volume")
 req(a["physical_1827_first_print_proven"] is False and a["physical_1869_revised_print_proven"] is False,"no printing state")
 req(len(a["source_specific_guangjing_gonglou_reading_glyphs"])==4 and all(x is None for x in a["source_specific_guangjing_gonglou_reading_glyphs"].values()),"missing original glyphs")
 req(all(a[k]==0 for k in ("new_historical_glyph_votes","new_lineage_edges","new_sources_registered","algorithm_reopen")),"no unearned historical evidence")
 req(a["stop_repeat_sampling_same_38_labeled_preview_metadata"] is True,"data acquisition priority")
 h=st["historical_audit"]
 req(h["external_source_registry_total_unique_count"]>=r["handoff"]["union_sources"] and st["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","source and product invariants")
 req(r["transmission_impact"]["edges_supported"]==[],"no graph leap")
 return {"status":"PASS","independent_firstparty_metadata_originals":2,"source_declared_sampled_ranges":18,"juan20_original_target_images":0,"independent_1827_vs_1869_print_votes":0}
def verify():
 return validate(json.loads((ROOT/REC).read_text()),json.loads((ROOT/STATE).read_text()))
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False))
