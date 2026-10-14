#!/usr/bin/env python3
"""Fail closed on modern publication descriptor -> historical physical image promotion."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD="docs/research/MING-DATONG-YEHUOBIAN-12VQ-MODERN-EDITION-DESCRIPTOR-FIREWALL-R1.json"
SHARD="docs/research/MING-DATONG-YEHUOBIAN-12VQ-MODERN-EDITION-DESCRIPTOR-FIREWALL-SOURCE-SHARD-R1.json"
MANIFEST="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
SOURCES=("EXT-2026-MINGDAIYANJIU44-CHEN1997-YEHUOBIAN-BIBLIOGRAPHY-12VQ","EXT-CUHK-HIST3110-2011-OLDER-SYLLABUS-1959-YEHUOBIAN-12VQ")
def require(cond,msg):
    if not cond: raise ValueError(msg)
def git_blob_sha(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+bytes([0])+data).hexdigest()
def validate(r,s,m,state):
    require(r["schema"]=="TIANWEN-12VQ-MODERN-YEHUOBIAN-EDITION-DESCRIPTOR-FIREWALL-R1","schema")
    records=r["source_readings"]
    require(len(records)==2 and "1997" in records[0]["observation"] and "1959" in records[1]["observation"],"modern year separation")
    require(records[0]["pdf_page_zero_based"]==33 and records[0]["printed_page"]==146,"publication source page")
    require("影印" in records[0]["quoted_terminology"] and "排印" in records[1]["quoted_terminology"],"unresolved format terms")
    require(records[1]["visible_section"].startswith("以下是2011-12年度"),"old syllabus scope")
    require(records[0]["asserted_object"]!=records[1]["asserted_object"],"two books must remain separate")
    require(all(x["publication_format_directly_examined"] is False and x["original_1827_source_image_attested"] is False for x in records),"physical source promotion")
    c=r["critical_scope"]
    require(c["different_modern_items_not_logical_direct_contradiction"] is True,"false logical contradiction")
    require(c["modern_1997_facsimile_status"]=="NOT_VERIFIED_FROM_PUBLISHER_OR_PHYSICAL_COPY","1997 format shortcut")
    require(c["modern_1959_typeset_status"]=="CITED_BY_CUHK_NOT_INDEPENDENT_PHYSICAL_EXAMINATION","1959 format shortcut")
    require(all(c[z] is True for z in ("modern1997_not_1827_physical_print","cited_1827_title_not_direct_image","word_影印_does_not_create_target_glyph_vote","word_排印_does_not_prove_modern_1997_layout","positive_collation_requires_source_bound_original_physical_1827_or_1869_folio")),"ancient-image firewall")
    chron=r["chronology_layers"]
    require((chron["original_print_reference"],chron["first_modern_cited_version"],chron["later_modern_cited_version"])==(1827,1959,1997),"date sequence")
    require(chron["these_dates_are_not_identical_copy_or_print_dates"] is True,"date scope firewall")
    a=r["accounting"]
    require((a["root"],a["extension_before"],a["extension_after"],a["union_before"],a["union_after"])==(647,48,50,695,697),"source snapshot")
    require(a["new_bibliographic_source_rows"]==2 and all(a[z]==0 for z in ("new_ancient_original_page_images","new_glyph_votes","formal_batch_increment","new_genealogy_nodes","new_genealogy_edges","algorithm_reopens")),"no ancient source promotion")
    require((a["matrix_row_count"],a["audited_row_count"],a["provenance_repaired"],a["existing_formal_batches"])==(222,222,45,487),"matrix and formal invariant")
    require(len(s["sources"])==2 and tuple(x["source_id"] for x in s["sources"])==SOURCES,"registered source identities")
    require(all(x["physical_glyph_authority"] is False and x["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY" and x["evidence"]==RECORD for x in s["sources"]),"source register false authority")
    matching=[x for x in m["shards"] if x["path"]==SHARD]
    require(len(matching)==1 and matching[0]["source_count"]==2,"source shard")
    require(m["combined_source_count"]>=697,"registry count must not regress")
    require(m["combined_source_count"]==m["root_source_count"]+m["extension_source_count"],"registry total arithmetic")
    require(state["historical_audit"]["external_source_registry_total_unique_count"]==m["combined_source_count"],"continuity count")
    require(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["historical_audit"]["row_count"]==222,"product invariant")
    require(r["transmission_impact"]["nodes_added_or_strengthened"]==[] and r["transmission_impact"]["edges_supported"]==[],"lineage-promotion")
    return {"status":"PASS","bibliographic_rows":2,"ancient_target_votes":0}
def verify():
    r=json.loads((ROOT/RECORD).read_text())
    s=json.loads((ROOT/SHARD).read_text())
    m=json.loads((ROOT/MANIFEST).read_text())
    state=json.loads((ROOT/STATE).read_text())
    out=validate(r,s,m,state)
    entry=next(x for x in m["shards"] if x["path"]==SHARD)
    require(git_blob_sha((ROOT/SHARD).read_bytes())==entry["blob_sha"],"source hash")
    return out
if __name__=="__main__": print(json.dumps(verify()))
