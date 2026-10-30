#!/usr/bin/env python3
"""13LY: only catalog/sibling link is positive; no original glyph upgrade."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];E="docs/research/TIANWEN-13LY-BSB-MINGSHI-ALL-EIGHT-VOLUMES-FIRSTPARTY-TITLE-INDEX-R1.json"
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13LY-BSB-MINGSHI-ALL-EIGHT-VOLUMES-FIRSTPARTY-TITLE-INDEX-R1" and e["issue_id"]=="TW-OPEN-0005"
 a=e["firstparty_index"];c=e["capture"];q=e["adjudication"]
 assert a["source_html_sha256"]=="f4d775d5e4e4f0d7a9579f109bce0bfa8a26c99a5c0338077e3640bbf4dad53c"
 assert a["source_html_bytes"]==56460 and a["source_volume_labels"]==list(range(1,9))
 assert [x["volume"] for x in a["source_documents"]]==list(range(1,9))
 assert a["volume1_official_link"]=="https://ostasien.digitale-sammlungen.de/view/bsb11166691"
 assert a["not_inferred_from_numeric_increment"] is True and a["not_original_page_witness"] is True
 assert c["artifact_id"]==12981466158 and c["source_artifact_sha256"]=="a5b4d8f37aadbb79024eb990bd5b4bfd20e49b758d3bc59f076c867be4ac42fe"
 assert c["durable_library_file_id"]=="libfile_09c45f8cd2948191a080b6c8727ca824"
 assert e["next_probe"]["run_status_at_commit"]=="UNRUN" and e["next_probe"]["no_ocr"] is True
 for f in ["volume1_iiif_original_manifest_captured","juan35_source_title_leaf_positive","juan35_number_positive","known_1739_physical_impression","same_plate_or_lineage_proven"]:assert q[f] is False
 assert q["new_ancient_witness_vote"]==q["new_g893_numeric_winners"]==q["algorithm_reopens"]==0 and q["product"]=="CLOSED"
 assert e["transmission_impact"]["edges_supported"]==e["transmission_impact"]["edges_revised"]==[]
 assert e["counts"]==dict(sources=765,root=647,extensions=118,matrix_rows=222,matrix_audited=222,genealogy_nodes=252,genealogy_edges=238,open_issues=11,original_g893_six_winners=0,algorithm_reopens=0)
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,964,0)
 assert any(x.startswith("13LY ") for x in s["historical_audit"]["current_focus"])
 assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and "13LY CURRENT ACTION:" in issue["next_action"] and E in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13LY-BSB-EIGHT-FIRSTPARTY-VOLUMES-20261030" for x in issue["history"])
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 return {"status":"PASS","official_volume1":"bsb11166691","original_juan35_winners":0}
if __name__=="__main__":
 e,s,l=(json.loads((ROOT/p).read_text(encoding="utf8")) for p in [E,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"])
 print(json.dumps(check(e,s,l),ensure_ascii=False))
