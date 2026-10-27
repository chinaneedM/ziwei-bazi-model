#!/usr/bin/env python3
"""12VP: scoped Nagoya journal TOC evidence, not a global publication nonexistence claim."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
RECORD = "docs/research/MING-DATONG-YEHUOBIAN-12VP-NAGOYA-PUBLISHER-TOC-CONTINUATION-SCOPE-R1.json"
SHARD = "docs/research/MING-DATONG-YEHUOBIAN-12VP-NAGOYA-PUBLISHER-TOC-CONTINUATION-SCOPE-SOURCE-SHARD-R1.json"
MANIFEST = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
STATE = "docs/PROJECT-CURRENT-STATE-R1.json"
SOURCE_ID = "EXT-NAGOYA-TOYOSHI-JOURNAL-ISSUES43-50-TOC-12VP"
INDEX = "https://toyoshi.lit.nagoya-u.ac.jp/kenkyukai/backnumber.html"

def require(value, msg):
    if not value:
        raise ValueError(msg)

def git_blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + bytes([0]) + data).hexdigest()

def validate(r, shard, manifest, state):
    require(r["schema"] == "TIANWEN-12VP-NAGOYA-PUBLISHER-TOC-SCOPE-R1", "schema")
    pub = r["publisher_index"]
    require(pub["url"] == INDEX and pub["latest_listed_issue"] == 50, "publisher source")
    require(pub["issue_year_not_equated_to_repository_deposit_year"] is True, "publication/deposit date firewall")
    p = r["prior_issues"]
    require([(z["issue"], z["year"]) for z in p] == [(43,2019),(44,2020),(45,2021)], "initial publisher issue sequence")
    require(["版本問題" in p[0]["observed_title"], "校記（一）" in p[1]["observed_title"], "校記（二）" in p[2]["observed_title"]] == [True]*3, "earlier scholarship titles")
    require(all(z["target_juan20_apparatus"] is False for z in p), "modern criticism promoted to target apparatus")
    later = r["searched_continuation"]
    require([(z["issue"],z["year"]) for z in later] == [(i,i+1976) for i in range(46,51)], "issue-year scope")
    require(all(z["listed_inoue_yehuobian_koki_continuation"] is False and z["claim_scope"] == "TOC_LISTED_TITLES_ONLY" for z in later), "later TOC scope")
    neg = r["negative_claim"]
    require(neg["scope"] == "ONLY_OFFICIAL_LISTED_TITLES_OF_NAGOYA_JOURNAL_ISSUES_46_TO_50", "journal scope")
    for field in ("worldwide_no_further_publication","other_journals_checked","unlisted_material_excluded","fulltext_juan20_exhaustively_searched","author_stopped_work_claim"):
        require(neg[field] is False, "overbroad negative: " + field)
    require(all(v is True for k,v in r["cataloguing_controls"].items() if k != "existing_12vo_2020_2021_target_juan20_covered"), "catalogue firewall")
    require(r["cataloguing_controls"]["existing_12vo_2020_2021_target_juan20_covered"] is False, "target volume promotion")
    src = shard["sources"]
    require(len(src)==1 and src[0]["source_id"]==SOURCE_ID and src[0]["url"]==INDEX, "registry source binding")
    require(src[0]["physical_glyph_authority"] is False and src[0]["evidence"] == RECORD, "source glyph authority")
    require(src[0]["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY", "source class")
    a = r["accounting"]
    require((a["base_source_union"],a["new_bibliographic_source_rows"],a["source_union_after"])==(694,1,695), "batch snapshot")
    require(all(a[k]==0 for k in ("ancient_target_images","independent_glyph_votes","graph_nodes","graph_edges","formal_batch_increment","algorithm_reopens")), "glyph/graph/algorithm scope")
    require((a["matrix_rows"],a["matrix_audited"],a["provenance_repairs"])==(222,222,45), "Matrix snapshot")
    entry = [s for s in manifest["shards"] if s["path"] == SHARD]
    require(len(entry)==1 and entry[0]["source_count"]==1, "registry shard")
    require(manifest["combined_source_count"] >= 695, "registry must not regress after 12VP")
    require(manifest["combined_source_count"] == manifest["root_source_count"] + manifest["extension_source_count"], "registry arithmetic")
    require(state["historical_audit"]["external_source_registry_total_unique_count"] == manifest["combined_source_count"], "handoff registry")
    require(state["historical_audit"]["row_count"]==222 and state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED", "product invariant")
    require(r["transmission_impact"]["nodes_added_or_strengthened"] == [] and r["transmission_impact"]["edges_supported"] == [], "unproved lineage vote")
    return {"status":"PASS","publisher_issue_tail":[46,47,48,49,50],"new_bibliographic_sources":1,"new_ancient_glyph_votes":0}

def verify():
    r=json.loads((ROOT / RECORD).read_text())
    shard=json.loads((ROOT / SHARD).read_text())
    manifest=json.loads((ROOT / MANIFEST).read_text())
    state=json.loads((ROOT / STATE).read_text())
    result=validate(r,shard,manifest,state)
    entry=next(s for s in manifest["shards"] if s["path"]==SHARD)
    require(git_blob_sha((ROOT / SHARD).read_bytes()) == entry["blob_sha"], "source shard Git blob integrity")
    return result

if __name__ == "__main__":
    print(json.dumps(verify(),ensure_ascii=False))
