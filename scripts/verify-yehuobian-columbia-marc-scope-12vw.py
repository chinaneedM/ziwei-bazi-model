#!/usr/bin/env python3
"""12VW longitudinal record invariant: CLIO open MARC is no ancient witness."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD="docs/research/MING-DATONG-YEHUOBIAN-12VW-COLUMBIA-CLIO-OPEN-MARC-SHARD-GATE-R1.json"
SHARD="docs/research/MING-DATONG-YEHUOBIAN-12VW-COLUMBIA-CLIO-OPEN-MARC-SHARD-GATE-SOURCE-SHARD-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
MANIFEST="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
def require(v,msg):
    if not v:raise ValueError(msg)
def blob_sha(data):return hashlib.sha1(b"blob "+str(len(data)).encode()+bytes([0])+data).hexdigest()
def validate(rec,shard,manifest,state):
    require(rec["schema"]=="TIANWEN-12VW-COLUMBIA-OPEN-MARC-DATA-ACQUISITION-GATE-R1","schema")
    doc=rec["discovery"]
    require(doc["official_documentation"]=="https://library.columbia.edu/about/lib-ops/clio-data.html" and doc["official_dataset_index"]=="https://lito.cul.columbia.edu/extracts/ColumbiaLibraryCatalog/full/","first-party source")
    require(doc["index_numbered_shards"]==111 and doc["first_file"]=="extract-001.xml.gz" and doc["last_file"]=="extract-111.xml.gz","bounded directory count")
    require(doc["index_is_physical_holding_identification"] is False,"index mistaken for item")
    ctrl=rec["source_scope"]
    for name in ("bulk_shard_order_not_known_to_be_title_sorted","one_shard_nonhit_never_proves_book_absent","entire_archive_not_downloaded_this_batch","metadata_quality_not_guaranteed","marc_catalogue_is_not_original_page_scan"):
        if name=="marc_catalogue_is_not_original_page_scan":require(rec["repository_gates"][name] is True,name)
        else:require(ctrl[name] is True,name)
    require(ctrl["physical_1827_folio_proved"] is False and ctrl["ancient_glyphs_proved"] is False,"original image unverified")
    acq=rec["bounded_acquisition"]
    require(acq["default_one_shard"]==111 and acq["max_compressed_bytes"]==80000000,"bounded shard")
    require(acq["result_status_before_probe"]=="NOT_RUN_IN_RESEARCH_RECORD" and acq["negative_global_holding_claim_allowed"] is False,"unearned bulk result")
    require(all(acq[k] is None for k in ("exact_clio_id","record_sha256","physical_copy_call_number","digitized_juan20_leaf")),"unattested item identity")
    require(rec["repository_gates"]["do_not_add_ninth_verified_copy_on_hit_without_physical_item_and_volume"] is True,"premature ninth object")
    require(rec["repository_gates"]["do_not_cast_target_glyph_from_marc_metadata"] is True,"glyph promotion")
    a=rec["accounting"]
    require((a["root_sources"],a["extension_before"],a["extension_after"],a["source_union_before"],a["source_union_after"])==(647,53,54,700,701),"source as-of snapshot")
    require(a["new_first_party_metadata_source"]==1 and all(a[x]==0 for x in ("new_original_pages","original_glyph_votes","new_genealogy_edges","algorithm_reopens")),"new historical votes")
    require((a["matrix_rows"],a["audited_rows"],a["repaired_metadata"],a["genealogy_nodes"],a["genealogy_edges"],a["formal_batches"])==(222,222,45,252,238,487),"research invariants")
    require(len(shard["sources"])==1 and shard["sources"][0]["source_id"]=="EXT-COLUMBIA-CLIO-FIRSTPARTY-OPEN-MARC-111-SHARD-INDEX-12VW","source id")
    require(shard["sources"][0]["physical_glyph_authority"] is False and shard["sources"][0]["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY","glyph authority")
    entries=[x for x in manifest["shards"] if x["path"]==SHARD]
    require(len(entries)==1 and entries[0]["source_count"]==1,"new source shard")
    require(manifest["combined_source_count"]>=701 and manifest["combined_source_count"]==manifest["root_source_count"]+manifest["extension_source_count"],"source growth")
    require(state["historical_audit"]["external_source_registry_total_unique_count"]==manifest["combined_source_count"],"state source count")
    require(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","product re-open")
    return {"status":"PASS","new_open_metadata_source":1,"new_ancient_glyph_votes":0}
def verify():
    def load(p):return json.loads((ROOT/p).read_text())
    rec,shard,man,state=(load(p) for p in (RECORD,SHARD,MANIFEST,STATE))
    ans=validate(rec,shard,man,state)
    expected=next(x["blob_sha"] for x in man["shards"] if x["path"]==SHARD)
    require(blob_sha((ROOT/SHARD).read_bytes())==expected,"source bytes Git blob hash")
    return ans
if __name__=="__main__":print(json.dumps(verify()))
