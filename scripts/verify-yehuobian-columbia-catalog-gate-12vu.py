#!/usr/bin/env python3
"""12VU: Columbia secondary bibliography must not become an item or glyph vote."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD="docs/research/MING-DATONG-YEHUOBIAN-12VU-COLUMBIA-1827-CITATION-AND-FIRSTPARTY-CATALOG-GATE-R1.json"
SHARD="docs/research/MING-DATONG-YEHUOBIAN-12VU-COLUMBIA-1827-CITATION-AND-FIRSTPARTY-CATALOG-GATE-SOURCE-SHARD-R1.json"
MANIFEST="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
IDS=("EXT-UW-OBSERVING-UNSEEN-COLUMBIA1827-YEHUOBIAN-12VU","EXT-COLUMBIA-EASTASIAN-RARE-BOOKS-CLIO-ACCESS-12VU")
def require(v,msg):
    if not v:raise ValueError(msg)
def git_blob_sha(buf):
    return hashlib.sha1(b"blob "+str(len(buf)).encode()+bytes([0])+buf).hexdigest()
def validate(r,shard,manifest,state):
    require(r["schema"]=="TIANWEN-12VU-COLUMBIA-1827-SECONDARY-CITATION-FIRSTPARTY-CATALOG-ACCESS-GATE-R1","schema")
    c=r["source_claim"]
    require(c["source_url"]=="https://uw.manifoldapp.org/read/6aaf7354-623c-485a-b979-24b69d800c3e/section/942227a4-3c0a-4c0f-a54b-cebee051a28e" and c["cited_year"]==1827 and c["cited_holding_literal"]=="Columbia University Libraries","academic bibliography object")
    require(c["cited_author_literal"]=="Shen Defu 沈德府" and c["asserted_holding_status"]=="SECONDARY_PUBLICATION_CITATION_ONLY","quotation scope")
    require(c["source_issued_clio_id"] is None and c["call_number"] is None and c["physical_print_state_proven"] is False,"physical item not verified")
    o=r["institutional_controls"]
    require(o["rare_books_url"]=="https://library.columbia.edu/libraries/eastasian/chinese/rare_special.html" and o["rare_books_guide_url"]=="https://library.columbia.edu/libraries/eastasian/special_collections/RBR_Guidelines.html","first-party library policy route")
    require(all(o[k] is True for k in ("rare_books_portal_says_clio_and_worldcat","rare_books_portal_mentions_ia_digitized_title_list","generic_public_digitization_not_exact_1827_scan","general_reading_room_by_appointment","general_repro_request_not_item_eligibility","no_contact_sent","no_order_placed")),"institutional scope firewall")
    require(o["first_party_specific_yehuobian_item_found"] is False,"invented institutional copy")
    require(all(o[k] is None for k in ("clio_record_url","clio_barcode","shelfmark","image_manifest","target_folio")),"invented firstparty identity or image")
    q=r["acquisition_classification"]
    require(q["pending_secondary_holding_candidate_not_existing_eight_item_queue"] and q["eight_existing_source_issued_catalog_candidates_preserved"] and q["new_source_issued_physical_item_candidates"]==0,"nine-item queue promotion")
    for k in ("no_independent_1827_impression_proven","no_original_target_juan20_image","no_historical_glyph_votes","exact_1827_vs_1869_plate_check_open","print_date_vs_holding_vs_digitization_layers_separate"):
        require(q[k] is True,"historical evidence firewall: "+k)
    require(set(r["four_locus_gate"])=={"GONGJIN","CLOCK_NOUN","BEIJING_WINTER_SUNRISE","BEIJING_SUMMER_SUNSET"} and all(v is None for v in r["four_locus_gate"].values()),"unattested original glyphs")
    a=r["accounting"]
    require((a["root_sources"],a["extension_before"],a["extension_after"],a["union_before"],a["union_after"],a["new_bibliographic_or_service_sources"])==(647,51,53,698,700,2),"historical snapshot sources")
    require(all(a[k]==0 for k in ("ancient_original_target_image_pages","independent_original_glyph_votes","genealogy_nodes_added","genealogy_edges_added","algorithm_reopens")),"unearned independent witness")
    require((a["matrix_rows"],a["matrix_audited"],a["provenance_repairs"],a["formal_batches"])==(222,222,45,487),"Matrix baseline")
    require(len(shard["sources"])==2 and tuple(s["source_id"] for s in shard["sources"])==IDS,"two distinct source records")
    require(all(s["physical_glyph_authority"] is False and s["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY" and s["evidence"]==RECORD for s in shard["sources"]),"bibliography used as original leaf")
    row=[s for s in manifest["shards"] if s["path"]==SHARD]
    require(len(row)==1 and row[0]["source_count"]==2,"new source shard")
    require(manifest["combined_source_count"]>=700,"registry union cannot regress")
    require(manifest["combined_source_count"]==manifest["root_source_count"]+manifest["extension_source_count"],"registry arithmetic")
    require(state["historical_audit"]["external_source_registry_total_unique_count"]==manifest["combined_source_count"],"state union alignment")
    require(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","product unexpectedly reopened")
    require(r["transmission_impact"]["nodes_added_or_strengthened"]==[] and r["transmission_impact"]["edges_supported"]==[],"unproven genealogy")
    return {"status":"PASS","secondary_columbia_holding_leads":1,"source_register_additions":2,"verified_clio_items":0,"historical_glyph_votes":0}
def verify():
    def rd(f):return json.loads((ROOT/f).read_text())
    r,s,m,st=rd(RECORD),rd(SHARD),rd(MANIFEST),rd(STATE)
    output=validate(r,s,m,st)
    row=next(x for x in m["shards"] if x["path"]==SHARD)
    require(git_blob_sha((ROOT/SHARD).read_bytes())==row["blob_sha"],"source registry blob sha")
    return output
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False))
