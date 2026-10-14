#!/usr/bin/env python3
"""Scoped 12VX outcome: one genuine runner-log MARC shard nonhit, no broad absence claim."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD="docs/research/MING-DATONG-YEHUOBIAN-12VX-COLUMBIA-MARC-SHARD111-ACTIONS-RESULT-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
MANIFEST="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
PARENT="docs/research/MING-DATONG-YEHUOBIAN-12VW-COLUMBIA-CLIO-OPEN-MARC-SHARD-GATE-R1.json"
URL="https://lito.cul.columbia.edu/extracts/ColumbiaLibraryCatalog/full/extract-111.xml.gz"
SHA="655b2dd9e02631b44e4c3c9319a11bd1f9d3d4492b3435575afd3e3102d8b9c5"
HEAD="c7f59899426144e64fbd779e79e9638491980714"
def require(x,msg):
    if not x:raise ValueError(msg)
def validate(rec,parent,state,manifest):
    require(rec.get("schema")=="TIANWEN-12VX-COLUMBIA-MARC-SHARD111-OBSERVED-RESULT-R1","schema")
    x=rec["exact_git_workflow"]
    require((x["head_sha"],x["github_run_id"],x["job_id"],x["artifact_id"])==(HEAD,38582081722,115914301391,11904401169),"exact head run artifact")
    require(x["conclusion"]=="success" and x["run_log_contains_structured_probe_output"] is True,"observed runner log")
    require(x["artifact_name"]=="columbia-clio-one-shard-12vw" and x["artifact_archive_size_bytes"]==597,"artifact metadata")
    require(all(x[k] is False for k in ("artifact_zip_binary_redownloaded_in_this_batch","artifact_member_json_directly_rehashed_in_this_batch","source_gzip_redownloaded_in_this_batch")),"false independent rehash")
    z=rec["observed_probe"]
    require(z["schema"]=="TIANWEN-12VW-MARC-ONE-SHARD-PROBE-RESULT-R1" and z["status"]=="BOUNDED_SINGLE_SHARD_SCANNED","probe schema")
    require(z["source_url"]==URL and z["source_sha256"]==SHA and re.fullmatch("[0-9a-f]{64}",SHA),"source binding")
    require(z["compressed_bytes"]==17907901 and z["record_count"]==21553,"runner log byte and parsed-record counts")
    require((z["shards_scanned"],z["publisher_index_shards"],z["matched_title_records"],z["results_returned"])==(1,111,0,0),"single shard scoped nonhit")
    require(all(z[k] is False for k in ("results_truncated","whole_catalog_searched","catalog_absence_inference_allowed","physical_copy_identity_proven","original_juan20_image_found")) and z["ancient_glyph_votes"]==0,"global catalog or ancient witness inference")
    require(z["source_hash_provenance"]=="ACTUAL_SHA256_REPORTED_BY_RUNNER_LOG_NOT_INDEPENDENTLY_REHASHED_THIS_BATCH","hash provenance")
    c=rec["claim_firewall"]
    require(all(c[k] is False for k in ("nonhit_extrapolation_to_all_111_shards","no_columbia_1827_copy_asserted","no_columbia_1827_copy_negated","false_equivalence_to_tokyo_or_kyoto","ancient_original_glyphs_attested_from_marc")),"unsafe negative or positive evidence promotion")
    require(c["synthetic_parser_tests_are_not_ancient_evidence"] is True and c["no_new_source_registration_same_12vw_dataset"] is True and c["columbia_physical_juan20_original_still_unbound"] is True,"material source authority firewall")
    d=parent["discovery"]
    require(d["index_numbered_shards"]==111 and parent["bounded_acquisition"]["default_one_shard"]==111,"parent source scope")
    a=rec["accounting"]
    require((a["root_sources"],a["extension_sources"],a["source_union"])==(647,54,701),"as-of source count")
    require(all(a[k]==0 for k in ("new_registered_external_sources","new_source_issued_original_folios","new_ancient_target_glyph_votes","new_graph_edges","algorithm_reopens")),"false source or graph promotion")
    require((a["matrix_rows"],a["audited"],a["repaired_provenance"],a["genealogy_nodes"],a["genealogy_edges"],a["formal_batches"])==(222,222,45,252,238,487),"historical audit invariant")
    require(a["product"]=="CLOSED" and rec["transmission_impact"]["edges_supported"]==[],"chart or genealogy reopen")
    require(state["historical_audit"]["external_source_registry_total_unique_count"]==manifest["combined_source_count"] and manifest["combined_source_count"]>=701,"current sources monotonic")
    require(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","product")
    return {"status":"PASS","parsed_records":21553,"title_hits_on_shard111":0,"global_absence_claim":False,"ancient_glyph_votes":0}
def verify():
    def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
    return validate(load(RECORD),load(PARENT),load(STATE),load(MANIFEST))
if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False))
