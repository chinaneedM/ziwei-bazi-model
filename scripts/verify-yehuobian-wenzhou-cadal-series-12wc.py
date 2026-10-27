#!/usr/bin/env python3
"""12WC: official catalogue publication is not a title-specific copy/glyph attestation."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12WC-WENZHOU-REGISTRATION-AND-CADAL-SERIES-DEDUP-R1.json"
MAN="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
SHARD="docs/research/MING-DATONG-YEHUOBIAN-12WC-WENZHOU-NLC2017-OFFICIAL-CATALOG-SOURCE-SHARD-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
def require(v,msg):
    if not v:raise ValueError(msg)
def blobsha(b):
    return hashlib.sha1(b"blob "+str(len(b)).encode()+bytes([0])+b).hexdigest()
def validate(r,s,m,state):
    require(r["schema"]=="TIANWEN-12WC-OFFICIAL-CENSUS-AND-CADAL-DUPLICATE-SERIES-R1","schema")
    o=r["official_catalogue"]
    require(o["isbn"]=="978-7-5013-6148-9" and o["publisher_claimed_records"]==13784 and o["publisher_date"]=="2017-09-29","official publication")
    require(o["numbers_are_ranges_not_row_identifiers"] is True and o["exact_yehuobian_entry_verified"] is False,"official item firewall")
    require(o["yehuobian_official_census_id"] is None and o["yehuobian_official_shelfmark"] is None,"false assigned census identifier")
    require(o["old_1827_target_page_obtained"] is False and o["new_1869_target_page_obtained"] is False,"historical original page")
    require(r["prior_wenzhou_secondary"]["thirdparty_claim_still_unverified_by_official_item"] is True,"thirdparty promotion")
    c=r["cadal_inventory"]
    require((c["main_book_pairs"],c["supplement_pairs"],c["total_id_paired_uploads"])==(23,4,27),"CADAL count")
    require((c["series_first"],c["series_last"],c["same_id_focus"])==("02096900","02096926","02096915"),"CADAL ID range")
    require(c["old_listed_bytes"]==3400790 and c["new_listed_bytes"]==3495009,"Commons inventory file sizes")
    require(c["old_file_original_bytes_obtained_at_research_commit"] is False and c["old_new_binary_comparison_pending_action"] is True,"premature source-byte assertion")
    require(c["same_category_is_not_same_physical_copy_proof"] is True and c["independent_historical_print_votes_from_uploads"]==0,"digital alias lineage")
    require(len(s["sources"])==2 and all(x["physical_glyph_authority"] is False for x in s["sources"]),"two bibliographic-only source records")
    require({x["source_id"] for x in s["sources"]}=={"EXT-NLCPRESS-WENZHOU-2017-CENSUS-CATALOG-PUBLICATION-12WC","EXT-NLC-WENZHOU-2018-CENSUS-SERIES-INTRO-12WC"},"source identities")
    require(m["root_source_count"]==647 and m["extension_source_count"]>=57 and m["combined_source_count"]==m["root_source_count"]+m["extension_source_count"],"registry arithmetic")
    require(state["historical_audit"]["external_source_registry_total_unique_count"]==m["combined_source_count"],"state registry sync")
    require(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","product scope")
    require(r["accounting"]["ancient_glyph_votes_added"]==0 and r["accounting"]["algorithm_reopens"]==0 and r["transmission_impact"]["edges_supported"]==[],"illicit historical winner")
    require(len([x for x in m["shards"] if x["path"]==SHARD and x["source_count"]==2])==1,"source shard manifest")
    return {"status":"PASS","new_catalogue_publication_sources":2,"ancient_1827_1869_target_glyph_votes":0}
def verify():
    def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
    r,s,m,st=[load(x) for x in (REC,SHARD,MAN,STATE)]
    d=next(x for x in m["shards"] if x["path"]==SHARD)
    require(blobsha((ROOT/SHARD).read_bytes())==d["blob_sha"],"Git blob shard digest")
    return validate(r,s,m,st)
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False))
