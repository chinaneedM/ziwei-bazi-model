#!/usr/bin/env python3
"""12VZ. A second image-scoped digital facsimile is not a second independent print."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12VZ-CADAL02112262-DIRECT-PRINTED-GLYPH-AND-DIGITAL-IDENTITY-R1.json"
SHARD="docs/research/MING-DATONG-YEHUOBIAN-12VZ-CADAL02112262-DIRECT-PRINTED-GLYPH-AND-DIGITAL-IDENTITY-SOURCE-SHARD-R1.json"
MAN="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
SRC="EXT-CADAL02112262-YEHUOBIAN-FASC16-PRINTED-V20-GAIZAO-LOUKE-12VZ"
def req(v,msg):
 if not v:raise ValueError(msg)
def blob_sha(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+bytes([0])+b).hexdigest()
def validate(r,s,m,state):
 req(r["schema"]=="TIANWEN-12VZ-CADAL02112262-DIRECT-PRINTED-GLYPH-IMAGE-SCOPE-R1","schema")
 f=r["exact_source_capture"]
 req((f["github_run_id"],f["github_job_id"],f["artifact_id"])==(38584869553,115924040077,11904279811),"captured run")
 req(f["artifact_zip_sha256_locally_recomputed"]=="53758ba2c556c45014a79134613445f3bdfbd063274380d6216a784c79e42118","ZIP identity")
 req(f["zip_members"]==20 and f["all_member_sha256_locally_verified"] is True and f["ocr_used"] is False,"binary verified scope")
 old,new=f["source_files"]
 req((old["id"],old["bytes"],old["pages"])==("CADAL02096915",3495009,135),"old original")
 req((new["id"],new["bytes"],new["pages"])==("CADAL02112262",3413348,133),"new original")
 req(new["sha256"]=="2481e717733c1ab1f31023222c934d0c1d83fc8a16c7166d84693a8ee57d4632","source digest")
 p=r["source_page_crosswalk"]
 req(p["old_volume20_target_pages"]==[121,122] and p["new_volume20_target_pages"]==[119,120] and p["new_volume20_heading_page"]==66,"page mapping")
 req(p["source_page_offset_for_selected_target"]==-2 and p["offset_is_not_global_page_by_page_proof"] is True,"page scope")
 loci=p["original_image_page_reading"]
 req({k:v["reading"] for k,v in loci.items()}=={"GONGJIN":"宮禁","CLOCK_NOUN":"官漏","BEIJING_WINTER_SUNRISE":"辰初二刻","BEIJING_SUMMER_SUNSET":"戌初三刻"},"exact target readings")
 req(all(x["source_page"]==119 for x in loci.values()),"target page")
 req(p["page_sha256"]["new_p119"]=="1ce6a56253dafb12b91455e17571a082394e95a963f5d4c0abd088f9ac1ffc6f","page binary")
 req(p["independent_historical_print_copy_votes_proven"]==0 and p["physical_item_shelfmark"] is None,"independent print vote")
 req(p["original_1827_print_first_impression_proven"] is False and p["revised_1869_impression_proven"] is False,"date protection")
 sc=r["source_scope"]
 req(sc["different_djvu_binary_sha256"] is True and sc["different_djvu_page_counts"] is True,"distinct digital file evidence")
 req(all(sc[k] is True for k in ("same_physical_copy_unproved","different_print_plates_unproved","direct_transmission_unproved","one_new_digitized_surface_not_a_second_verified_ancient_print")),"physical stemma protection")
 a=r["accounting"]
 req((a["root_sources"],a["ext_sources_before"],a["ext_sources_after"],a["source_union_before"],a["source_union_after"])==(647,54,55,701,702),"source growth snapshot")
 req(a["new_external_image_source_records"]==1 and all(a[k]==0 for k in ("ancient_print_lineages_verified","new_algorithm_reopens","new_genealogy_nodes","new_genealogy_edges")),"illicit ancient witness or algorithm")
 req((a["matrix_rows"],a["audited_rows"],a["provenance_repairs"],a["formal_batches"])==(222,222,45,487),"matrix invariant")
 src=s["sources"]
 req(len(src)==1 and src[0]["source_id"]==SRC and src[0]["physical_glyph_authority"] is True,"exact registered digital surface")
 req(src[0]["verification_status"]=="DIRECT_SOURCE_IMAGE_GLYPH_COLLATED_EDITION_UNBOUND","undated original source role")
 req(src[0]["direct_image_attestation"]["independent_physical_print_vote"] is False,"duplicate physical vote")
 entries=[x for x in m["shards"] if x["path"]==SHARD]
 req(len(entries)==1 and entries[0]["source_count"]==1,"registry shard")
 req(m["combined_source_count"]>=702 and m["combined_source_count"]==m["root_source_count"]+m["extension_source_count"],"future source union")
 req(state["historical_audit"]["external_source_registry_total_unique_count"]==m["combined_source_count"],"handoff")
 req(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","chart reopen")
 req(r["transmission_impact"]["edges_supported"]==[],"unsupported genealogy")
 return {"status":"PASS","direct_digital_image_sources_added":1,"independent_1827_1869_print_votes":0,"glyphs_scoped_to_print_image":4}
def verify():
 def load(path):return json.loads((ROOT/path).read_text())
 a,s,m,st=[load(x) for x in (REC,SHARD,MAN,STATE)]
 result=validate(a,s,m,st)
 entry=next(x for x in m["shards"] if x["path"]==SHARD)
 req(blob_sha((ROOT/SHARD).read_bytes())==entry["blob_sha"],"source shard Git blob")
 return result
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False))
