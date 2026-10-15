#!/usr/bin/env python3
"""12WZ seven source-index bibliographic details, not seven ancient printing votes."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12WZ-TOKYO-SEVEN-FIRSTPARTY-RECORDS-AND-IMABORI-LEAF-GATE-R1.json"
SHARD="docs/research/MING-DATONG-YEHUOBIAN-12WZ-TOKYO-SEVEN-DIRECT-FIRSTPARTY-DETAIL-SOURCE-SHARD-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
MAN="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
EXPECTED=["9927","9928","78464","90972","103841","104379","109371"]
def req(ok,msg):
 if not ok:raise ValueError(msg)
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def validate(r,s,st,m):
 req(r["schema"]=="TIANWEN-12WZ-TOKYO-KANSEKI-SEVEN-SOURCE-ISSUED-YEHUOBIAN-DETAILS-R1","schema")
 items=r["items"];req(len(items)==7 and [x["id"] for x in items]==EXPECTED,"seven exact source-emitted ids")
 req([x["rank"] for x in items]==list(range(1,8)) and all(len(x["sha"])==64 and x["bytes"]>4000 and x["original_glyphs"]==0 for x in items),"source page hash and no historical glyphs")
 z=r["source"]
 req(z["one_title12WX"]["query_html_sha256"]=="94d245a69438527a96af5a21e306bab9c76dbb66c2fe5b02be742eda49619d98" and z["one_title12WX"]["actual_results"]==7,"provider source query 7 rows")
 req(z["detail_pages12WY"]["artifact"]==11977836428 and z["detail_pages12WY"]["zip_sha256"]=="33f31f23f768e70edaa2b2a067aa4731f259898201201a86857281b3f6ca0c5f" and z["detail_pages12WY"]["all7_provider_html_retrieved"] is True,"all seven source detail originals")
 req(z["all_artifact_zips_locally_rehashed"] is True and z["all_seven_detail_html_sha256_locally_rehashed"] is True and z["no_ocr"] is True,"source digest receipts")
 req(items[0]["shelfmark"]=="大木-子部-雜家類-16" and items[0]["fascicles"]=="34" and items[0]["ciNiiItem"]=="6403767830","Oki catalog crosswalk")
 req(items[3]["shelfmark"]=="倉石文庫:20128" and items[3]["fascicles"]=="2帙20冊" and items[3]["ciNiiItem"]=="6403148395","Kuraishi catalog crosswalk")
 req(items[4]["shelfmark"]=="今堀文庫:J2006" and items[4]["notes"]=="闕卷第二十一第二十二" and r["imabori"]["reported_missing_juan"]==[21,22],"Imabori catalog scoped missing volume")
 req(items[5]["notes"]=="劣化（虫損）につき利用不可","damaged restricted candidate")
 req(all(r["imabori"][k] is False for k in ("juan20_physically_present_and_usable","original_juan20_folio_imaged","independently_dated_1827_plate_proven","independently_dated_1869_plate_proven")),"cannot promote Imabori physical target")
 req(all(t["source_issued_image_uri"] is None for t in r["target_physical_impressions"].values()),"no original folio image uri")
 for k in ("all_7_records_are_seven_independent_historical_print_witnesses","no_original_juan20_article_gaizao_louke_page_image","no_original_page_glyph_readings","no_new_algorithm_rule","no_confirmed_chart_bug","no_direct_cross_fascicle_paper_copy_identity"):
  # first is false; all other fields are explicit negative fact safeguards encoded true
  want=False if k.startswith("all_7") else True
  req(r["limits"][k] is want,"historical print inference gate "+k)
 req(r["limits"]["registered_metadata_sources"]==1 and r["limits"]["seven_rows_are_source_issued_metadata_not_physical_glyphs"] is True,"one source not seven")
 counts=r["counts"];h=st["historical_audit"]
 req((counts["source_root"],counts["source_extensions"],counts["source_union"])==(m["root_source_count"],m["extension_source_count"],m["combined_source_count"])==(647,59,706),"registered evidence growth")
 req(counts["source_union"]==h["external_source_registry_total_unique_count"],"state registry union")
 req(counts["matrix_rows"]==counts["matrix_audited"]==h["row_count"]==222 and counts["provenance_repairs"]==45,"matrix")
 req(counts["genealogy_nodes"]==252 and counts["genealogy_edges"]==238 and counts["formal_batches"]==len(h["completed_batches"])==487,"graph")
 req(counts["historical_print_votes"]==counts["source_glyph_votes"]==counts["algorithm_reopen_count"]==0 and counts["product"]==st["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","product")
 req(s["schema"]=="TIANWEN-12WZ-TOKYO-FIRSTPARTY-CATALOG-SOURCE-SHARD-R1" and len(s["sources"])==1,"one source shard")
 q=s["sources"][0]
 req(q["physical_glyph_authority"] is False and q["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY" and q["evidence"]==REC,"catalogue evidence only")
 req(q["independent_original_ancient_print_votes"]==0 and len(q["firstparty_detail_page_ids"])==7,"no paper votes")
 req(r["transmission_impact"]["edges_supported"]==[],"no genealogy promotion")
 return {"status":"PASS","official_catalogue_details":7,"new_external_bibliographic_sources":1,"historic_print_votes":0}
def verify():return validate(load(REC),load(SHARD),load(STATE),load(MAN))
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False))
