#!/usr/bin/env python3
"""13LH historical boundary: SIFT scan geometry != edition/block/recension proof."""
import json
from pathlib import Path
# Verify historical action text through append-only revisions, not the current instruction.
try:
    from scripts._tianwen_historical_action_r1 import historical_action_view
except ModuleNotFoundError:
    from _tianwen_historical_action_r1 import historical_action_view
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13LH-NAJDA2810037-2810038-PRINT-GEOMETRY-REGISTRATION-R1.json"
def load():
    return tuple(json.loads((ROOT / p).read_text(encoding="utf-8")) for p in (E,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def check(e,s,l):
    assert e["schema"]=="TIANWEN-13LH-NAJDA2810037-2810038-PRINT-GEOMETRY-REGISTRATION-R1" and e["issue_id"]=="TW-OPEN-0005"
    a,b=e["input_originals"]
    assert a["archive_reference"]=="281-0037" and b["archive_reference"]=="281-0038"
    assert a["sha256"]=="8892b16c3b8e17f12211195cf7b58acfd5b7dc0d0aefca6623f653a04d4da93e"
    assert b["sha256"]=="73322281149551c76f96008c1b9f3933e817543f7cb8710c92268ade9ca031eb"
    assert a["original_numeral"]==b["original_numeral"]=="238977.09"
    d=e["replay"];c=e["adjudication"];scope=e["counts"]
    assert d["script"]=="scripts/replay-tianwen-13lh-naaj-geometry.py" and d["metric_status"]=="LOCAL_REPLAY_ON_FULL_ORIGINAL_SOURCE_BYTES"
    assert d["lowe_ratio"]==0.78 and d["sift_nfeatures"]==5500 and d["homography"].endswith("3.5)")
    assert d["page_native_rgb_sha256"]["281-0037"]["6"]=="a90105202278a2cd0a4c6fb06e7840a673a3d342882f1c6c6ed02e30d49a1913"
    assert d["page_native_rgb_sha256"]["281-0038"]["6"]=="f5963e5ce75039038ce4aee42655e1ecef6224b36ed9411cc6072c0fba793cb4"
    rows={(p["pdf_page"],p["leaf"]):p for p in d["paired_pages"]}
    for page,side,good,positive in [(6,"left",581,424),(6,"right",459,309),(7,"left",595,440),(7,"right",580,379)]:
        assert rows[page,side]["good_matches"]==good and rows[page,side]["ransac_inliers"]==positive
        assert 0<rows[page,side]["median_residual_px"]<0.7
    assert rows[2,"right"]["ransac_inliers"]==16 and d["registration_not_historical_source_proof"]
    assert not any(c[k] for k in ("same_woodblocks_historically_proven","same_historical_print_run_proven","same_physical_copy","original_1739_impression_proven","ancient_50000_error_causality_proven"))
    assert c["independent_textual_recension_votes_new"]==0 and c["historical_numeric_winners_added"]==0 and c["competing_cadal_siku_original"]=="288977.09"
    assert not e["transmission_impact"]["edges_supported"] and not e["transmission_impact"]["edges_revised"]
    assert scope==dict(source_root=647,extension=118,total=765,matrix_rows=222,audited=222,graph_nodes=252,graph_edges=238,unresolved_issues=11,algorithm_reopens=0,product="CLOSED")
    focus=s["historical_audit"]["current_focus"];binding=l["binding"]
    assert any(f.startswith("13LH ") for f in focus) and binding["source_focus_count"]==len(focus)
    assert binding["latest_research_focus_prefix"]==focus[-1].split(" ",1)[0]
    assert s["schema_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]==binding["reviewed_state_version"]==l["checkpoint_log"][-1]["state_version"]
    i=next(q for q in l["issues"] if q["id"]=="TW-OPEN-0005")
    assert i["status"]=="OPEN" and i["priority"]=="P0" and historical_action_view(i).startswith(binding["latest_research_focus_prefix"]+" CURRENT ACTION:")
    assert "13LG CURRENT ACTION:" in historical_action_view(i) and "13JM CURRENT ACTION:" in historical_action_view(i) and "RETRACTED" in historical_action_view(i)
    assert E in i["source_refs"] and E[:-5]+".md" in i["source_refs"]
    assert any(q.get("revision_id")=="TW-OPEN-0005-13LH-GEOMETRY-20261030" for q in i["history"])
    assert len(l["issues"])==11 and s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
    return {"status":"PASS","geometric_compatible":True,"plate_identity_proven":False,"historical_winners":0}
if __name__=="__main__":print(json.dumps(check(*load()),ensure_ascii=False))
