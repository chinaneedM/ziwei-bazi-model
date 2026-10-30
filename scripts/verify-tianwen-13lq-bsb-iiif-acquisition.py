#!/usr/bin/env python3
"""13LQ exact first-party IIIF acquisition checkpoint; catalog/preview != target glyph."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13LQ-BSB1739-MINGSHI-1880-CANVAS-NATIVE-IIIF-20-PREVIEW-ACQUISITION-R1.json"
def load():return tuple(json.loads((ROOT/p).read_text(encoding="utf8")) for p in [E,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"])
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13LQ-BSB1739-MINGSHI-1880-CANVAS-NATIVE-IIIF-20-PREVIEW-ACQUISITION-R1" and e["issue_id"]=="TW-OPEN-0005"
 a=e["acquisition"];r=e["scope_review"];d=e["adjudication"]
 assert a["run_id"]==41054248271 and a["artifact_id"]==12975358673
 assert a["artifact_zip_sha256"]=="c13af97a923dd36adbb2c242858bd50f32780cacc3982a301e3ba263148d949e"
 assert a["artifact_zip_bytes"]==280457 and a["durable_archive"]["artifact_zip_sha256"]==a["artifact_zip_sha256"]
 assert a["durable_archive"]["library_file_id"]=="libfile_bd904974e1048191bcdc08a89e34db11"
 assert a["provider_manifest_sha256"]=="fb28be88c767636c6394926620c112e994f1b0b5d58cf896d4a5edc2919f047c"
 assert a["provider_manifest_bytes"]==1762391 and a["canvas_count"]==1880
 assert a["sampled_preview_count"]==len(a["sampled_canvas_numbers_1_based"])==20 and a["sampled_preview_all_success"] is True
 assert a["viewer_reported_count"]==1886 and a["viewer_vs_manifest_delta"]==6
 assert a["preview_contact_image"]["pixels"]==[1200,1300]
 assert a["preview_contact_image"]["sha256"]=="5be41d5fb0cfdf0ab9f528e8672c647859d2349a5a61ab7b8f2c2d88f51d6810"
 assert r["target_juan35_title_leaf"]=="UNIDENTIFIED" and r["target_13_lunation_numeric_glyph"]=="UNIDENTIFIED"
 assert r["low_resolution_only"] is True and r["no_ocr"] is True
 assert r["physical_1739_impression_proven"] is False
 assert r["independent_historical_recension_count_added"]==r["historical_g893_six_numeric_winners_added"]==0
 for f in ["physical_print_year_verified","juan35_target_present_verified","new_original_numeric_glyph_identified","woodblock_same_or_different_proven"]:
  assert d[f] is False,f
 assert d["new_numeric_winners"]==d["algorithm_reopens"]==0 and d["chart"]=="CLOSED"
 assert e["source_status"]==dict(root=647,extension_shards=68,extension_records=118,combined=765,added_registry_source_rows=0,matrix_rows=222,matrix_audited=222,graph_nodes=252,graph_edges=238,unresolved_issues=11)
 assert e["transmission_impact"]["edges_supported"]==e["transmission_impact"]["edges_revised"]==[]
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,961,0)
 assert any(x.startswith("13LQ ") for x in s["historical_audit"]["current_focus"])
 assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and "13LQ CURRENT ACTION:" in issue["next_action"]
 assert "13LP CURRENT ACTION:" in issue["next_action"] and E in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13LQ-BSB-MANIFEST-CANVAS-20261030" for x in issue["history"])
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 return {"status":"PASS","canvas_count":1880,"firstparty_previews":20,"original_juan35_glyph":"UNIDENTIFIED","numeric_winners":0}
if __name__=="__main__":print(json.dumps(check(*load()),ensure_ascii=False))
