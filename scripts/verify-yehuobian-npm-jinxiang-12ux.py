#!/usr/bin/env python3
"""NPM unified-number Qing pocket edition object; no unearned original juan20 glyphs."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD="docs/research/MING-DATONG-YEHUOBIAN-12UX-NPM-QING-JINXIANG-PHYSICAL-COPY-R1.json"
SHARD="docs/research/MING-DATONG-YEHUOBIAN-12UX-NPM-QING-JINXIANG-SOURCE-SHARD-R1.json"
MANIFEST="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
GRAPH="docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
IDS={"EXT-NPM-YEHUOBIAN-QING-JINXIANG-EXHIBIT-12UX","EXT-TELDAP-NPM-GUGUAN003512-003527-YEHUOBIAN-12UX"}
TRUE_GUARDS=(
"qin_printed_jinxiang_category_verified_catalogue_level",
"1827_fulishanfang_identity_unproven","1869_fulishanfang_identity_unproven",
"same_plate_as_tokyo_or_kyoto_unproven","same_wording_as_received_editions_unproven",
"individual_book003527_is_not_a_juan20_locator","16_book_count_is_not_16_juan_count",
"176x113cm_scale_not_stamp_or_colophon_date","2009_copy_restriction_is_not_current_access_denial",
"museum_cover_photo_not_four_target_page_glyphs","yuan_past_owner_narrative_not_physically_seal_proven",
"source_overlap_does_not_create_multiple_independent_physical_copy_votes","no_algorithm_reopen"
)
def validate(r,shard,manifest,graph,state):
    if r.get("schema")!="TIANWEN-12UX-NPM-QING-JINXIANG-OBJECT-SCOPED-BIBLIOGRAPHIC-BINDING-R1" or r.get("status")!="HOLDING_AND_QING_JINXIANG_FORM_CROSSCHECKED_NO_TARGET_PAGE":
        raise ValueError("identity/schema")
    o=r.get("object",{})
    if (o.get("institutional_unified_id"),o.get("shelfmark"),o.get("individual_book_count"),o.get("item_displayed_in_2023"),o.get("edition_description"))!=("故觀003512-003527","505",16,"故觀003527","清刊巾箱本"):
        raise ValueError("copy edition identity or quantity")
    if any(o.get(k) is not None for k in ("precise_impression_year","edition_printing_block_identity","physical_copy_date","digitization_date")):
        raise ValueError("unsupported impression or physical copy dating")
    if r.get("legacy_copy_note",{}).get("current_2026_permission")!="UNVERIFIED":
        raise ValueError("historical copy limit wrongly treated as current")
    if len(r.get("witnesses",[]))!=4:
        raise ValueError("source controls")
    if any(r.get("print_lineage_firewall",{}).get(k) is not True for k in TRUE_GUARDS):
        raise ValueError("lineage/permission firewall")
    outcome=r.get("scope_outcome",{})
    if tuple(outcome.get(k) for k in ("new_distinct_edition_catalog_class","new_identified_held_copy","new_source_registry_entries","new_graph_nodes","new_graph_edges","new_historical_target_glyph_votes","new_original_juan20_pages","physical_copy_inspection_for_plate","institutional_contact_sent","application_or_fee"))!=(1,1,2,2,1,0,0,0,0,0):
        raise ValueError("unsupported scope gain")
    if shard.get("schema")!="TIANWEN-12UX-NPM-YEHUOBIAN-JINXIANG-SOURCE-SHARD-R1" or {x.get("source_id") for x in shard.get("sources",[])}!=IDS:
        raise ValueError("shard identity")
    if any(x.get("physical_glyph_authority") is not False or x.get("verification_status")!="BIBLIOGRAPHIC_METADATA_ONLY" for x in shard["sources"]):
        raise ValueError("museum exhibition or catalog is not target page")
    if not any(x.get("path")==SHARD and x.get("source_count")==2 for x in manifest.get("shards",[])):
        raise ValueError("shard absent from manifest")
    if (manifest.get("root_source_count")!=647 or manifest.get("extension_source_count",0)<42 or
        manifest.get("combined_source_count")!=manifest.get("root_source_count")+manifest.get("extension_source_count")):
        raise ValueError("source count")
    n={x["node_id"]:x for x in graph["nodes"]}
    ids={"EDITION-YEHUOBIAN-NPM-QING-JINXIANG-PRINTYEAR-UNSPECIFIED","PHYSICAL-COPY-YEHUOBIAN-NPM-GUGUAN003512-003527"}
    if not ids<=set(n) or len(graph["nodes"])<252 or len(graph["edges"])<238:
        raise ValueError("graph size/identities")
    if any(n[x].get("target_original_leaf_collated",n[x].get("target_page_collated")) is not False for x in ids):
        raise ValueError("new target falsely collated")
    e=[x for x in graph["edges"] if x.get("edge_id")=="TG-E0238"]
    if len(e)!=1 or (e[0].get("from"),e[0].get("to"),e[0].get("relation"),e[0].get("status"))!=("PHYSICAL-COPY-YEHUOBIAN-NPM-GUGUAN003512-003527","EDITION-YEHUOBIAN-NPM-QING-JINXIANG-PRINTYEAR-UNSPECIFIED","PHYSICAL_COPY_OF_EDITION","CONFIRMED"):
        raise ValueError("incorrect lineage edge")
    if not set(IDS)<=set(e[0].get("evidence",[])):
        raise ValueError("graph evidence missing")
    if tuple(map(int,state.get("schema_version","0.0.0").split(".")))<(1,554,0):
        raise ValueError("state version")
    a=state["historical_audit"]
    if ((a["row_count"],a["audited_row_count"],a["external_source_registry_root_count"])!=(222,222,647) or
        a["external_source_registry_extension_count"]!=manifest["extension_source_count"] or
        a["external_source_registry_total_unique_count"]!=manifest["combined_source_count"]):
        raise ValueError("state counts unsynced")
    if not any(v.startswith("12UX ") for v in a["current_focus"]):
        raise ValueError("handoff not updated")
    return {"status":"PASS","physical_collection_unified_id":o["institutional_unified_id"],"new_catalog_control_sources":2,"new_nodes":2,"new_edges":1,"new_target_glyph_votes":0}
def verify(root=ROOT):
    def load(p):return json.loads((root/p).read_text(encoding="utf-8"))
    return validate(*(load(p) for p in (RECORD,SHARD,MANIFEST,GRAPH,STATE)))
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False,sort_keys=True))
