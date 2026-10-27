#!/usr/bin/env python3
"""12WO: 429 is an audited access boundary, not a provider page or ancient print vote."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12WO-KEIO-GOOGLEBOOKS-1827-METADATA-ACCESS-GATE-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
WN=".github/workflows/probe-yehuobian-12wn-keio-googlebooks-record.yml"
WNSCRIPT="scripts/probe-yehuobian-12wn-keio-googlebooks-volume-metadata.py"
KNOWN_ARCHIVE="8f117a1565cf50b2d13497293008ed02ef65bc3ebcaa07169f999e2bf76879ec"
KNOWN_ERROR="3c779cc912e0eebcff2c61aeb7fc5f919795a9e76103d73585596be7359cb89e"
def check(ok,msg):
 if not ok:raise ValueError(msg)
def validate(r,state,workflow,script):
 check(r["schema"]=="TIANWEN-12WO-KEIO-GOOGLEBOOKS-1827-EXACT-ID-429-ACCESS-GATE-R1","schema")
 t=r["target"];c=r["capture"];s=r["scope"]
 check(t["id"]=="VAWHNTyDZC8C" and "野獲編" in t["work"] and t["discovery_is_not_authenticated_item_record"] is True,"precise discovery-only Keio candidate")
 check(t["independently_verified_keio_institutional_shelfmark"] is None and t["physical_paper_copy_proven"] is False and t["work_volume20_content_confirmed"] is False and t["source_page_of_gaizao_louke_found"] is False,"no exact Keio original volume20")
 check(c["workflow_run_id"]==38730460404 and c["capture_artifact_id"]==11969904093 and c["capture_artifact_archive_bytes"]==287,"actual bounded run receipt")
 check(c["capture_job_status"]=="completed_failure" and c["verify_job_status"]=="completed_success" and c["api_response"]=="HTTP_429_TOO_MANY_REQUESTS","actual HTTP rate limit status")
 check(c["capture_artifact_sha256_github_reported"]==c["capture_artifact_sha256_locally_recomputed"]==KNOWN_ARCHIVE and c["capture_error_member_sha256"]==KNOWN_ERROR and c["capture_error_member_bytes"]==166,"actual independent archive SHA")
 check(c["provider_response_original_json_acquired"] is False and c["unmodified_provider_volume_json_sha256"] is None and c["raw_book_page_images_acquired"]==0 and c["ocr_used"] is False,"not a fetched original page")
 check(r["alternative_firstparty"]["institution_exact_book_catalog_id"] is None and r["alternative_firstparty"]["direct_image_iiif_manifest_for_this_work"] is None,"institutional portal is not exact item")
 check(all(s[k]==0 for k in ("new_registry_sources","ancient_print_votes","original_juan20_glyph_votes","algorithm_reopens")),"no fabricated historical authority")
 check(s["union_sources"]==705 and state["historical_audit"]["external_source_registry_total_unique_count"]>=s["union_sources"],"source registry preserved")
 check(s["matrix_rows"]==s["matrix_audited"]==state["historical_audit"]["row_count"]==222 and s["metadata_repairs"]==45,"audit counts preserved")
 check(s["genealogy_nodes"]==252 and s["genealogy_edges"]==238 and s["formal_batches"]==len(state["historical_audit"]["completed_batches"])==487,"genealogy and formal batch invariants")
 check(s["product"]==state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","deterministic runtime not reopened")
 check(s["source_absence_proven"] is False and s["further_automatic_api_retries_disabled"] is True,"429 cannot prove absence or trigger auto retry")
 check(s["independent_provider_image_1827_first_impression_proven"] is False and s["independent_provider_image_1869_revised_impression_proven"] is False,"no paper date authority")
 check("if: github.event_name == 'workflow_dispatch'" in workflow and "    needs: verify" in workflow,"manual-only external capture")
 check('ID="VAWHNTyDZC8C"' in script and 'MAX_BYTES=550_000' in script,"exact documented API ID and byte cap")
 check(r["transmission_impact"]["edges_supported"]==[] and r["transmission_impact"]["nodes_added_or_strengthened"]==[],"no new transmission edges")
 return {"status":"PASS","google_books_access":"HTTP_429_RECORDED","registered_source_additions":0,"ancient_original_print_votes":0,"API_RETRY":"MANUAL_ONLY"}
def verify():
 r=json.loads((ROOT/REC).read_text(encoding="utf-8"))
 s=json.loads((ROOT/STATE).read_text(encoding="utf-8"))
 return validate(r,s,(ROOT/WN).read_text(encoding="utf-8"),(ROOT/WNSCRIPT).read_text(encoding="utf-8"))
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False))
