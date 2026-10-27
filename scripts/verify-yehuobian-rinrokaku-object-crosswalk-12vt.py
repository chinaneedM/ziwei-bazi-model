#!/usr/bin/env python3
"""12VT. Confirm dealer's first-party permalink without an independent historical glyph vote."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA="docs/research/MING-DATONG-YEHUOBIAN-12VT-RINROKAKU-UNIQUE-OBJECT-PERMALINK-CROSSWALK-R1.json"
PARENT="docs/research/MING-DATONG-YEHUOBIAN-12VS-RINROKAKU-24BOOK-COMMERCIAL-LOCATOR-R1.json"
SHARD="docs/research/MING-DATONG-YEHUOBIAN-12VS-RINROKAKU-24BOOK-COMMERCIAL-LOCATOR-SOURCE-SHARD-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
URL="https://rinrokaku.pro/en/product/%E9%87%8E%E7%8D%B2%E7%B7%A8-%E4%B8%89%E5%8D%81%E5%B7%BB-%E8%A3%9C%E9%81%BA%E5%9B%9B%E5%B7%BB/"
SOURCE_ID="EXT-RINROKAKU-ITEM69-YEHUOBIAN-24BOOK-1827-1869-12VS"

def require(v,message):
    if not v:raise ValueError(message)

def validate(rec,parent,shard,state):
    require(rec["schema"]=="TIANWEN-12VT-RINROKAKU-DIRECT-SELLER-OBJECT-CROSSWALK-R1","schema")
    item=rec["first_party_product"]
    require(item["url"]==URL and item["sku"]=="102667" and item["catalogue_numbers"]==["R18101492","R18000069","E24101101"],"first-party seller item identity")
    require(item["advertised_year"]==1827 and item["advertised_revised_year"]==1869 and item["advertised_books"]==24,"separate old print years and binding")
    require(item["available_to_purchase_or_in_stock"]=="NOT_INDEPENDENTLY_VERIFIED" and item["printed_year_attests_this_copy_first_impression"] is False,"invented current stock or physical impression")
    bridge=rec["identity_bridge"]
    require(bridge["seller_catalogue_item_69_matches"]=="R18000069" and parent["seller_catalogue_item_number"]==69,"seller item 69 crosswalk")
    require(bridge["seller_catalogue_pdf"]==parent["seller_catalogue"],"original seller catalogue source")
    require(bridge["one_commercial_exemplar_not_three_independent_witnesses"] is True and bridge["site_page_is_original_folio_scan"] is False and bridge["photos_of_the_four_loci_present_or_verified"] is False,"dealer object promoted to original folio")
    require(bridge["edition_date_1827_vs_revision_1869_still_requires_physical_plate_check"] is True,"unproved printing state")
    sr=rec["source_registration"]
    require(sr["original_source_id"]==SOURCE_ID==shard["sources"][0]["source_id"],"source double registration or changed binding")
    require(sr["do_not_duplicate_existing_12vs_source"] is True and sr["physical_glyph_authority"] is False,"duplicate source or false historical authority")
    require((sr["source_registry_root"],sr["extensions_before"],sr["extensions_after"],sr["source_union_before"],sr["source_union_after"])==(647,51,51,698,698),"source snapshot")
    require(all(rec["future_image_intake"][k] is None for k in ("original_source_pdf_or_image","folio","binary_sha256","printing_state_image")),"unacquired original image")
    require(set(rec["future_image_intake"]["loci"])=={"GONGJIN","CLOCK_NOUN","BEIJING_WINTER_SUNRISE","BEIJING_SUMMER_SUNSET"} and all(v is None for v in rec["future_image_intake"]["loci"].values()),"unsupported original glyph")
    require(all(v is False for v in rec["contact_or_purchase"].values()),"unauthorized external request")
    ac=rec["accounting"]
    require(all(ac[k]==0 for k in ("new_ancient_images","new_original_glyph_votes","new_source_entries","new_graph_edges","algorithm_reopens")),"spurious new evidence")
    require((ac["matrix_rows"],ac["audited"],ac["provenance_repairs"],ac["genealogy_nodes"],ac["genealogy_edges"],ac["formal_batches"])==(222,222,45,252,238,487),"historical audit snapshot")
    require(rec["transmission_impact"]["edges_supported"]==[] and rec["transmission_impact"]["nodes_added_or_strengthened"]==[],"unsupported physical genealogy")
    require(state["historical_audit"]["external_source_registry_total_unique_count"]>=698,"current registry regressed")
    require(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","product reopened")
    return {"status":"PASS","original_registered_sources_reused":1,"new_sources":0,"ancient_target_glyph_votes":0,"exact_dealer_sku":"102667"}

def verify():
    def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
    return validate(load(DATA),load(PARENT),load(SHARD),load(STATE))

if __name__=="__main__": print(json.dumps(verify(),ensure_ascii=False))
