#!/usr/bin/env python3
"""12WD exact old/new Commons original source receipt: no physical impression vote."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12WD-CADAL02096915-ACTUAL-OLD-NEW-IMAGE-REPLAY-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
WF=".github/workflows/verify-yehuobian-12wc-official-catalog-and-cadal-digital-alias.yml"
def req(ok,msg):
    if not ok:raise ValueError(msg)
def validate(r,s,yaml):
    req(r["schema"]=="TIANWEN-12WD-CADAL-SAME-ID-ORIGINAL-FILES-ACTUAL-PIXEL-COMPARISON-R1","schema")
    x=r["receipt"]
    req((x["run"],x["job"],x["artifact_id"])==(38684377172,116255845608,11948889363),"actual workflow receipt")
    req(x["status"]=="success" and x["head"]=="c0dead2e1e70e01fbc5c8f00f8d809ff9619c3c4","exact workflow HEAD")
    req(x["github_reported_zip_sha256"]=="737efeb074c114eaf8c4df955080b037d531e349d10d1feb0e07103d63da2408" and x["zip_independently_rehashed"] is False,"zip SHA reporting scope")
    a,b=r["sources"]
    req((a["bytes"],a["pages"])==(3400790,135) and (b["bytes"],b["pages"])==(3495009,135),"original binaries")
    req(a["sha256"]=="c9cbad43811efa7ddd737bd0997bf663b5a84d825202dc4ca2e0dcaecb81448e","old source SHA")
    req(b["sha256"]=="262edac806b90c984d5f0c4fce1bc150a974ebd574d847738a08a00cad39640d","new source SHA")
    pages=r["image_pages"]
    req([(x["page"],x["preview_256x384_mean_abs_gray_0_255"]) for x in pages]==[(121,0.04801),(122,0.03985)],"reported pixel deltas")
    req(all(x["exact_grayscale_pixel_identity"] is False for x in pages),"no pixel identity")
    f=r["scope"]
    req(f["paper_copy_identity"]=="UNBOUND" and f["impression_1827_vs_1869"]=="UNBOUND","physical provenance")
    req(f["new_manual_target_glyphs"]==0 and f["new_independent_ancient_print_votes"]==0 and f["algorithm_reopen"]==0,"no historical votes")
    req(r["accounting"]["sources"]<=s["historical_audit"]["external_source_registry_total_unique_count"] and s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","status sync")
    req("if: github.event_name == 'workflow_dispatch'" in yaml,"manual only expensive capture")
    req(r["transmission_impact"]["edges_supported"]==[],"lineage scope")
    return {"status":"PASS","original_digital_files":2,"near_duplicate_digital_page_comparisons":2,"physical_historical_votes":0}
def verify():
    return validate(json.loads((ROOT/REC).read_text()),json.loads((ROOT/STATE).read_text()),(ROOT/WF).read_text())
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False))
