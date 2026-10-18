#!/usr/bin/env python3
"""12ZR Goryeosa copies and plate-family source scope, fail-closed."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE="docs/research/TIANWEN-12ZR-GORYEOSA-DONGA-SNU-PLATE-FAMILY-R1.json"
SHARD="docs/research/TIANWEN-12ZR-GORYEOSA-SCHOLARSHIP-SOURCE-SHARD-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
MANIFEST="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"

def load():
    return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in
                 (EVIDENCE, SHARD, STATE, LEDGER, MANIFEST))
def check(ok, msg):
    if not ok:
        raise ValueError(msg)

def verify(d, shard, state, ledger, manifest):
    check(d["schema"]=="TIANWEN-12ZR-GORYEOSA-SAME-PLATE-FAMILY-COLLATION-SCOPE-R1"
          and d["issue_id"]=="TW-OPEN-0005", "evidence identity")
    kim=d["kci2012"]
    check(kim["kci_id"]=="ART001716355" and kim["doi"]=="10.17842/jsa.2012..54.1"
          and kim["year"]==2012 and kim["pages"]=="1-33", "KCI 2012 identity")
    check((kim["donga_books"],kim["kyujanggak_comparator_books"])==(75,85)
          and kim["author_claims_same_woodblock_edition"] is True, "source-scope set comparison")
    check("NO_TARGET_VOLUME52_IMAGES" in kim["proof_scope"], "abstract cannot replace folio")
    later=d["kci2014"]
    check(later["kci_id"]=="ART001898033" and later["author"]==kim["author"]
          and later["same_author_as_2012"] is True
          and later["independent_author_count_across_2012_and_2014"]==1,
          "same scholar two papers cannot be independent author votes")
    ed=d["modern2024"]
    check(ed["isbn"]=="9787214271327" and (ed["year"],ed["volumes"],ed["pages"])==(2024,6,3122)
          and ed["actual_vol52_apparatus_reviewed"] is False, "modern apparatus scope")
    scope=d["scope"]
    for k in ("author_claim_same_print_blocks_not_proven_by_this_project_original_images",
              "two_copies_distinct_physical_objects_can_still_share_one_plate_ancestry",
              "worn_later_impression_is_hypothesis_not_proven_date",
              "do_not_alias_85book_record_to_GK03539_GK03579",
              "two_kim_papers_not_independent_authors",
              "modern_editorial_text_not_direct_ancient_witness"):
        check(scope[k] is True, "plate lineage safeguard: "+k)
    check(scope["woodblock_85book_comparator_exact_SNU_ID"] is None,
          "unbound physical catalog ID")
    u=d["unresolved"]
    for k in ("donga_work52_native_image_sha256", "snu_woodblock_work52_native_image_sha256",
              "copy_identified_for_SNU_85_books", "modern2024_volume52_target_editorial_text",
              "gk3467_work52_ancient_glyphs", "gk5554_work52_ancient_glyphs"):
        check(u[k] is None, "no direct original allowed: "+k)
    for k in ("ancient_glyph_votes_added", "independent_ancestral_plate_votes_added",
              "transmission_graph_edges_added", "algorithm_reopens"):
        check(u[k]==0, "no fabricated glyph, genealogy or algorithm: "+k)
    check((u["open_issues"],u["g893_source_controls"],u["g893_cross_original"],u["chart_product"])
          ==(11,"5/6","0/6","CLOSED"), "historical candidate boundaries")
    check(d["transmission_impact"].startswith("NO_GRAPH_EDGE"), "transmission not prematurely closed")
    check(shard["schema"]=="TIANWEN-12ZR-GORYEOSA-SCHOLARSHIP-AND-CRITICAL-EDITION-SHARD-R1"
          and len(shard["sources"])==2, "source shard identity")
    check({x["source_id"] for x in shard["sources"]}
          =={"EXT-TIANWEN-12ZR-KCI-KIM2012-DONGA-SNU-WOODBLOCKS",
             "EXT-TIANWEN-12ZR-NANKAI-2024-GORYEOSA-JIAOZHU"}, "source ID dedup")
    check(all(x["physical_glyph_authority"] is False and x["evidence"]==EVIDENCE
              for x in shard["sources"]), "secondary sources not ancient physical pages")
    check({x["verification_status"] for x in shard["sources"]}
          =={"RECEIVED_TEXT_VERIFIED","BIBLIOGRAPHIC_METADATA_ONLY"}, "source status")
    specs=[x for x in manifest["shards"] if x["path"]==SHARD]
    check(len(specs)==1 and specs[0]["schema"]==shard["schema"]
          and specs[0]["source_count"]==2, "registered extension exact identity")
    check(manifest["root_source_count"]==647
          and manifest["extension_source_count"]>=65
          and manifest["combined_source_count"]==manifest["root_source_count"]+manifest["extension_source_count"],
          "source registry forward count")
    h=state["historical_audit"]
    check((h["external_source_registry_root_count"],h["external_source_registry_extension_count"],
           h["external_source_registry_total_unique_count"])
          ==(manifest["root_source_count"],manifest["extension_source_count"],manifest["combined_source_count"]),
          "state exact current registry count")
    issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
    check(issue["status"]=="OPEN" and all(p in issue["source_refs"]
          for p in (EVIDENCE,EVIDENCE.replace(".json",".md"),SHARD)), "P0 open lineage")
    focus=h["current_focus"]
    check(any(x.startswith("12ZR ") for x in focus)
          and ledger["binding"]["source_focus_count"]==len(focus)
          and ledger["binding"]["latest_research_focus_prefix"]==focus[-1].split(" ",1)[0],
          "active focus")
    check(state["schema_version"]==ledger["binding"]["reviewed_state_version"]
          ==h["research_omission_guard"]["reviewed_state_version"], "state continuity")
    check(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"]
          and len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==11, "all 11 reviewed")
    check(h["row_count"]==h["audited_row_count"]==222
          and state["invariants"]["algorithm_reopen_count"]==0
          and state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED",
          "do not reopen algorithm")
    return {"status":"PASS","registered_scholarship_sources":2,
            "independent_ancient_plate_votes":0,"open_issues":11}

if __name__=="__main__":
    print(json.dumps(verify(*load()),ensure_ascii=False))
