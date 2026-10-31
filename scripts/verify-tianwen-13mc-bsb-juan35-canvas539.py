#!/usr/bin/env python3
"""13MC witness-scoped BSB direct-content locus with no title or numeric promotion."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13MC-BSB-VOLUME1-JUAN35-CANVAS539-DIRECT-TEXTUAL-ANCHOR-R1.json"
S=ROOT/"docs/PROJECT-CURRENT-STATE-R1.json"
L=ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13MC-BSB-VOLUME1-JUAN35-CANVAS539-DIRECT-TEXTUAL-ANCHOR-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 a=e["source"];t=e["specific_target"];o=e["ordering_boundary"];ep=e["epistemic_limits"]
 assert a["digital_id"]=="bsb11166691" and a["manifest_canvas_count"]==1910
 assert a["manifest_sha256"]=="ed4ff6358db2c462edceb9ed5c2d667645cf000ed5f031eec8342fb3a241a369"
 assert a["artifact_id"]==12982700693 and a["library_file_id"]=="libfile_0dd09d6b40888191afaa8a5e9ffd4703"
 assert t["canvas_1based"]==539 and t["bytes"]==252919
 assert t["width_px"]==900 and t["height_px"]==1517
 assert t["jpeg_sha256"]=="7c26f50ce77c3265862e8d347047a568cf424c84f5c4df4dd60b72746fdf0ca0"
 assert t["decoded_rgb_sha256"]=="60122831911f4542d023fc3c3d55e94f1e8764e567205c7c4b0d6d0cb63b090a"
 assert t["attribution"]=="HIGH_CONFIDENCE_CANDIDATE_JUAN35_CONTENT_P539"
 assert all(not t[k] for k in ("is_chapter_title_leaf","is_native_original_optical_file","original_juan35_target_numeric_reading_verified"))
 assert o["proposed_local_juan35_title_leaf_search"]==[491,636]
 assert o["global_scan_direction_proven"] is False and o["chapter_title_leaf_number"] is None
 assert len(e["context_sample_crosswalk"])==5 and [x["canvas"] for x in e["context_sample_crosswalk"]]==[490,539,637,735,833]
 assert ep["product"]=="CLOSED" and ep["algorithm_reopens"]==ep["g893_six_numeric_winners_added"]==ep["independent_physical_copy_votes_added"]==0
 assert all(not ep[k] for k in ("source_page_full_line_collation_done","exact_1739_impression_proven","same_woodblock_between_holdings_proven","source_juan35_original_title_glyph_confirmed","numeric_variant_23897709_vs_28897709_adjudicated"))
 assert e["counters"]==dict(sources=765,root=647,extensions=118,matrix_rows=222,matrix_audited=222,genealogy_nodes=252,genealogy_edges=238,issues_open=11)
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,966,0)
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
 focus=s["historical_audit"]["current_focus"]
 assert any(x.startswith("13MC ") for x in focus)
 assert l["binding"]["latest_research_focus_prefix"]==focus[-1].split(" ",1)[0]
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0"
 assert issue["next_action"]  # rolling live action may advance beyond archived 13MC
 assert "docs/research/TIANWEN-13MC-BSB-VOLUME1-JUAN35-CANVAS539-DIRECT-TEXTUAL-ANCHOR-R1.json" in issue["source_refs"]
 archived=next(h for h in issue["history"] if h.get("revision_id")=="TW-OPEN-0005-13MC-BSB-V1-J35-P539-20261030")
 assert "docs/research/TIANWEN-13MC-BSB-VOLUME1-JUAN35-CANVAS539-DIRECT-TEXTUAL-ANCHOR-R1.json" in archived["evidence_refs"]
 assert any(c.get("state_version")=="1.966.0" and c.get("id")=="OMISSIONS-13MC-BSB-J35-C539-CROSSWALK-20261030" for c in l["checkpoint_log"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 return {"status":"PASS","BSB_canvas_539_content_crosswalk":True,"original_title_leaf_confirmed":False,"historical_numeric_winners_added":0}
if __name__=="__main__":print(json.dumps(check(*[json.loads(p.read_text(encoding="utf-8")) for p in (E,S,L)]),ensure_ascii=False))
