#!/usr/bin/env python3
"""12XF audit: four institutional web surfaces cannot certify rare printed leaves."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12XF-UTOKYO-DIGITAL-ACCESS-DISAMBIGUATION-R1.json"
WZ="docs/research/MING-DATONG-YEHUOBIAN-12WZ-TOKYO-SEVEN-FIRSTPARTY-RECORDS-AND-IMABORI-LEAF-GATE-R1.json"
XA="docs/research/MING-DATONG-YEHUOBIAN-12XA-TOKYO-SEVEN-ITEM-IMAGE-LINK-BOUNDARY-R1.json"
XE="docs/research/MING-DATONG-YEHUOBIAN-12XE-TOKYO-PRINTED-COPY-CONSERVATION-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
MAN="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
def j(path):return json.loads((R/path).read_text(encoding="utf-8"))
def chk(ok,msg):
 if not ok:raise ValueError(msg)
def validate(d,wz,xa,xe,state,manifest):
 chk(d["schema"]=="TIANWEN-12XF-UTOKYO-DIGITAL-ACCESS-DISAMBIGUATION-R1","schema")
 chk((d["catalog_parent"],d["buttons_parent"],d["preservation_parent"])==(WZ,XA,XE),"parents")
 src={x["id"]:x for x in d["source_snapshots"]}
 chk(len(src)==len(d["source_snapshots"])==4,"four different institution surfaces")
 p=src["SHANBEN_FULLIMAGE"]
 chk(p["url"]=="https://shanben.ioc.u-tokyo.ac.jp/intro.html" and p["date"]=="2009-03","dated image intro")
 chk((p["titles"],p["A_full_global"],p["B_full_restricted"])==(4630,4019,611) and p["titles"]==p["A_full_global"]+p["B_full_restricted"] and p["object_matches"]==[],"historical A/B not per item")
 sl=src["SHANBEN_SELECTED_LIST"]
 chk(sl["url"]=="https://shanben.ioc.u-tokyo.ac.jp/list.php" and (sl["list_records"],sl["list_pages"],sl["verified_title_query"],sl["title_hits_in_selected_search"])==(3889,195,"野獲編",0),"bounded historical search")
 chk(sl["interpretation"]=="BOUNDED_SELECTED_INDEX_ONLY_DOES_NOT_PROVE_GENERAL_ABSENCE","no global negative")
 n=src["KURAISHI_LECTURE"]
 chk(n["url"]=="https://kuraishi.ioc.u-tokyo.ac.jp/about_system.html" and (n["notebooks"],n["digitized_notebooks"])==(40,35) and n["object_matches"]==[],"lecture notebooks not printed edition")
 chk(n["interpretation"]=="PERSONAL_LECTURE_NOTES_NOT_KURAISHI_LIBRARY_1869_PRINT","personal lectures false positive")
 chk(src["NIJL_PARTNER"]["object_matches"]==[] and src["NIJL_PARTNER"]["interpretation"]=="JAPANESE_CLASSICS_PROJECT_NO_EXACT_TARGET_COPY_MATCH","NIJL no item match")
 tgt=d["original_items"]
 chk([(x["id"],x["ncid"],x["barcode"],x["edition_year"]) for x in tgt]==[("9927","BC0492354X","6403767830",1827),("90972","BB23196128","6403148395",1869)],"original copy identifiers")
 wz_map={x["id"]:x for x in wz["items"]};xe_map={x["item"]:x for x in xe["copies"]}
 for x in tgt:
  y=wz_map[x["id"]]
  chk(x["ncid"]==y["ciNii"] and x["barcode"]==y["ciNiiItem"] and x["barcode"] in xe_map,"catalog-copy binding")
  chk(x["original_leaf_image_found"] is False and xa["physical_target_controls"][x["id"]]["source_original_juan20_folio_obtained"] is False,"no printed folio evidence")
 chk(len(d["blocked_promotions"])==5,"five non-edges")
 chk(d["sources_registered_delta"]==d["historical_glyph_votes"]==d["original_folios"]==d["original_print_plate_votes"]==d["requests_submitted"]==0,"no fabricated evidence")
 h=state["historical_audit"];c=d["invariants"]
 chk((c["root"],c["extensions"],c["union"])==(647,59,706) and (manifest["root_source_count"],manifest["extension_source_count"],manifest["combined_source_count"])==(h["external_source_registry_root_count"],h["external_source_registry_extension_count"],h["external_source_registry_total_unique_count"]) and manifest["extension_source_count"]>=c["extensions"],"registry counts")
 chk((c["matrix"],c["audited"],c["repaired"])==(222,222,45)==(h["row_count"],h["audited_row_count"],h["repaired_provenance_metadata_defect_count"]),"matrix")
 chk((c["graph_nodes"],c["graph_edges"],c["formal_batches"])==(252,238,len(h["completed_batches"]))==(252,238,487),"graph/formal batches")
 chk(c["algorithm_reopens"]==state["invariants"]["algorithm_reopen_count"]==0 and c["product"]==state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","product freeze")
 t=d["transmission_impact"]
 chk(t["nodes_added_or_strengthened"]==[] and t["edges_supported"]==[] and t["edges_revised"]==[],"no transmission promoted")
 return {"status":"PASS","separate_platforms":4,"target_original_folios":0,"new_historical_glyph_votes":0}
def verify():return validate(j(REC),j(WZ),j(XA),j(XE),j(STATE),j(MAN))
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False))
