#!/usr/bin/env python3
"""13MT fixed-Pillow dual PyMuPDF profiles and forward-only handoff state."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13MT-ZHOU1569-PINNED-RENDERER-DIGEST-ERRATUM-R1.json"
S=R/"docs/PROJECT-CURRENT-STATE-R1.json"
L=R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
P=R/"docs/research/TIANWEN-13MQ-G893-ZHOU1569-D15-SECOND-LANE-ORIGINAL-PRINT-SCOPE-R1.json"
A=R/"docs/research/TIANWEN-13MS-ZHOU1569-ORIGINAL-SOURCE-ATLAS-AND-NAAJ-HOLDING-R1.json"
def check(e,s,l,p,a):
 assert e["schema"]=="TIANWEN-13MT-ZHOU1569-PINNED-RENDERER-DIGEST-ERRATUM-R1"
 v=e["experiment"];pr=e["pinned_renderer_profiles"];a0=e["adjudication"]
 assert v["run_id"]==41197580583 and v["artifact_id"]==13041700130
 assert v["original_source_pdf_sha256"]==p["provenance"]["zhou1569_pdf_sha256"]==a["original_acquisition"]["source_sha256"]
 assert v["pdf_pages"]==45 and v["pdf_bytes"]==4936040
 assert v["pillow_fixed"]=="11.3.0" and v["roi_box"]==p["original_roi_controls"][1]["box"]
 assert len(pr)==2 and [x["pymupdf"] for x in pr]==["1.26.7","1.28.2"]
 assert pr[0]["roi_rgb_sha256"]==p["original_roi_controls"][1]["rgb_sha256"]
 assert pr[1]["roi_rgb_sha256"]==a["original_acquisition"]["original_roi_samples"][3]["rgb_sha256"]
 assert pr[0]["full_page_rgb_sha256"]=="7b35af0e1e802c9346c927a02c67d1681e01b5120c3cf891160126f2018478d5"
 assert pr[1]["full_page_rgb_sha256"]=="d617e4e0a553dd019ea89a5bc54307e4d08a50cb96e958e7b34897c203c7d75d"
 assert pr[0]["roi_rgb_sha256"]!=pr[1]["roi_rgb_sha256"] and all(x["verified_result"]=="PASS" for x in pr)
 assert a0["discrepancy_kind"]=="VERSION_SCOPED_PDF_RENDITION_RGB_PIXEL_BYTES"
 assert a0["source_pdf_byte_drift"] is False and a0["independent_printing_different"] is False
 assert a0["pymupdf_version_effect_isolated_by_constant_pillow"] is True
 assert a0["historical_field_identity_to_g893"]=="OPEN" and a0["unit_radix_epoch_crosswork"]=="OPEN"
 assert a0["new_physical_witness_count"]==0
 n=e["nonpromotion"]
 assert n["algorithm_reopens"]==n["g893_cross_original_historical_winners"]==n["lineage_edges_added"]==0
 assert n["product"]==s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 assert n["registered_sources_total"]==s["historical_audit"]["external_source_registry_total_unique_count"]==765
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,982,0)
 assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
 assert any(z.startswith("13MT ") for z in s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert "docs/research/TIANWEN-13MT-ZHOU1569-PINNED-RENDERER-DIGEST-ERRATUM-R1.json" in issue["source_refs"] and "docs/research/TIANWEN-13MT-ZHOU1569-PINNED-RENDERER-DIGEST-ERRATUM-R1.md" in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13MT-RENDERER-VERSION-BRIDGE-20261031" for x in issue["history"])
 assert any(x.get("id")=="OMISSIONS-13MT-RENDERER-VERSION-BRIDGE-20261031" for x in l["checkpoint_log"])
 return {"status":"PASS","source_render_profile_discrepancy":"RESOLVED_BY_PINNED_PYMUPDF_VERSION","historical_winners":0}
if __name__=="__main__":
 e,s,l,p,a=(json.loads(q.read_text(encoding="utf-8")) for q in (E,S,L,P,A))
 print(json.dumps(check(e,s,l,p,a),ensure_ascii=False))
