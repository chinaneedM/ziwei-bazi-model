#!/usr/bin/env python3
"""13MA immutable source-grade and state/omission continuity gate."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13MA-BSB-MINGSHI-V1-1910-CANVAS-40-DIRECT-PREVIEW-R1.json"
S=ROOT/"docs/PROJECT-CURRENT-STATE-R1.json"
L=ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13MA-BSB-MINGSHI-V1-1910-CANVAS-40-DIRECT-PREVIEW-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 src=e["source"];acq=e["acquisition"];vis=e["visual_review"];a=e["adjudication"]
 assert src["object_id"]=="bsb11166691" and src["manifest_bytes"]==1790512 and src["canvas_count"]==1910
 assert src["manifest_sha256"]=="ed4ff6358db2c462edceb9ed5c2d667645cf000ed5f031eec8342fb3a241a369"
 assert acq["run_id"]==41064404159 and acq["artifact_id"]==12982700693
 assert acq["head_sha"]=="7a761935f66baf3dd6405110d3261ab2005afe16"
 assert acq["artifact_zip_sha256"]=="60b97d2b848444182816b0620a8578286cfbbc349ba5a1a3b2e61a61a866f39e"
 assert acq["artifact_zip_bytes"]==11021794 and acq["library_file_id"]=="libfile_0dd09d6b40888191afaa8a5e9ffd4703"
 assert acq["sample_count"]==acq["successful_jpegs"]==acq["verified_jpeg_sha256_count"]==acq["verified_decoded_rgb_sha256_count"]==40
 assert acq["no_ocr"] and acq["readback_verified"]
 assert acq["atlas_sha256"]=="d0610e2110af0fde0ce79ae6a2aac1fbbe3bb7b0d80b47b1be272c35dfb2e660"
 assert not any(vis[k] for k in ("target_juan35_original_title_positive","source_full_folio_review_done","source_original_numeral_positive","source_copy_exact_1739_impression_positive","printing_block_identity_positive","global_target_absence_proven","negative_search_assertion"))
 assert a["new_historical_recension_votes"]==a["new_g893_historical_numeric_winners"]==a["algorithm_reopens"]==0 and a["product"]=="CLOSED"
 assert e["counts"]==dict(sources=765,root=647,extensions=118,matrix_rows=222,matrix_audited=222,genealogy_nodes=252,genealogy_edges=238,open_issues=11,original_g893_six_winners=0,algorithm_reopens=0)
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,965,0)
 assert any(x.startswith("13MA ") for x in s["historical_audit"]["current_focus"])
 assert s["historical_audit"]["current_focus"][-1].startswith("13MA ")
 assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
 assert l["binding"]["latest_research_focus_prefix"]=="13MA"
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and "13MA CURRENT ACTION:" in issue["next_action"]
 assert "docs/research/TIANWEN-13MA-BSB-MINGSHI-V1-1910-CANVAS-40-DIRECT-PREVIEW-R1.json" in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13MA-BSB-V1-DIRECT-PREVIEW-20261030" for x in issue["history"])
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 return {"status":"PASS","first_party_manifest_canvas":1910,"images_hash_verified":40,"original_juan35_numeric_winners":0}
if __name__=="__main__":
 e,s,l=(json.loads(p.read_text(encoding="utf-8")) for p in (E,S,L))
 print(json.dumps(check(e,s,l),ensure_ascii=False))
