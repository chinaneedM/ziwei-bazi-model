import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
R="docs/research/MING-DATONG-YEHUOBIAN-12WS-TOKYO-SHANBEN-EXACT-TITLE-INDEX-SCOPE-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
P="scripts/probe-yehuobian-12wr-tokyo-shanben-form-search.py"
def chk(c,msg):
 if not c: raise ValueError(msg)
def validate(r,s,code):
 chk(r["schema"]=="TIANWEN-12WS-TOKYO-IOC-SHANBEN-SOURCE-BOUND-TITLE-ZERO-RESULT-SCOPE-R1","schema")
 x=r["source_capture"]
 chk(len(x)==3 and [a["phase"] for a in x]==["12WP","12WQ","12WR"],"phase identity")
 for a,id,sha in zip(x,[11975441446,11976191702,11976172024],["2ce0473b68ad6fb822ff5752ea7e46b9193835b663ce9e03e48ff522f969feda","78d4cdc145e4888a1f136bde79322be5dece8be868dc8597ac353db7c9d5a0ef","ec9b262329343f1092d0b2ab627df63d0f0813ad8ad7826aca590c07fa599b08"]):
  chk(a["artifact"]==id and a["zip_sha256"]==sha,"original ZIP receipt")
 chk(sum(a["original_html_pages"] for a in x)==sum(a["original_html_sha256_rechecked"] for a in x)==8,"8 provider pages rehashed")
 chk(x[1]["index_page_record_total"]==3889 and x[1]["index_page_total"]==195 and x[1]["source_sha256"]=="4fdae7a8cdfae415615e9b3a942ce6d7c58ae0dd852989b1f0188d9e7138aa96","real index page")
 chk(x[2]["post_form"]=={"str":"野獲編","col":"ti","submits":"檢索"} and x[2]["visible_result_count"]==0 and x[2]["visible_no_row_phrase"]=="無任何資料" and x[2]["actual_target_title_links"]==0,"bounded 0-row actual response")
 chk(x[2]["search_term_echoed_in_inline_javascript"] is True and "actual_index_result_count_from_visible_count" in code and "actual_result_table_explicit_no_rows" in code,"query-echo correction")
 for z,barcode,yr in zip(r["catalog_items"],["6403767830","6403148395"],[1827,1869]):
  chk(z["copy_item"]==barcode and z["year_catalog"]==yr and z["physical_item_in_catalog"] is True and z["original_folio_image_obtained"] is False and z["online_image_crosswalk_bound"] is False,"distinct catalog holding/no original")
 i=r["inference"]
 for k in ("specialized_image_index_not_identical_to_general_holdings_catalog","index_no_hit_does_not_prove_physical_holding_absence","index_no_hit_does_not_prove_historical_original_print_absence","query_string_appearing_inside_js_does_not_mean_item_hit","no_speculative_iiif_or_folio_identifier","no_new_independent_1827_or_1869_original_paper_print_vote","no_original_juan20_gaizao_louke_glyph_vote"):
  chk(i[k] is True,"absence/paper date firewall:"+k)
 chk(i["source_registry_additions"]==0 and i["algorithm_reopens"]==0 and i["no_new_transmission_graph_edges"] is True,"scope frozen")
 m=r["metrics"];chk(m["matrix"]==m["audited"]==s["historical_audit"]["row_count"]==222 and m["registered_sources"]==s["historical_audit"]["external_source_registry_total_unique_count"]==705 and m["provenance_repairs"]==45,"state consistent")
 chk(m["genealogy_nodes"]==252 and m["genealogy_edges"]==238 and m["formal_batches"]==len(s["historical_audit"]["completed_batches"])==487 and m["product"]==s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","graph/closed")
 chk(r["transmission_impact"]["edges_supported"]==[],"no fictional genealogy vote")
 return {"status":"PASS","source_pages_checked":8,"tokyo_shanben_search_result_rows":0,"ancient_print_votes":0}
def verify():return validate(json.loads((ROOT/R).read_text()),json.loads((ROOT/S).read_text()),(ROOT/P).read_text())
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False))
