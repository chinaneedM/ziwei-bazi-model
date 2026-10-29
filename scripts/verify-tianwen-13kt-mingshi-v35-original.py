#!/usr/bin/env python3
"""13KT: replay exact original-image evidence receipt + three limit constants without historic index award."""
import json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13KT-HARVARD-MINGSHI-V11-J35-DIRECT-ORIGINAL-THREE-CONSTANTS-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def check(p,msg):
 if not p:raise ValueError(msg)
def read():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (E,S,L))
def verify(e,state,ledger):
 check(e["schema"]=="TIANWEN-13KT-HARVARD-MINGSHI-V11-J35-DIRECT-ORIGINAL-THREE-CONSTANTS-R1" and e["issue_id"]=="TW-OPEN-0005","schema")
 p=e["provenance"];w=e["witness"];x=e["adjudication"]
 check(p["source_sha256"]=="36a2a99461d9d16a71e203d95ffa6cac189f1bbab94295de51ed6d3b60bd649b" and p["source_bytes"]==70809419 and p["pdf_page_count"]==74,"source bytes")
 check(p["commons_sha1"]=="eb1c0fabec7e25893a0fd7d174528b41e9eadaf0" and p["source_sha1_and_bytecount_matched_commons_api"] is True,"source sha1")
 check(w["source_sha256"]==p["source_sha256"] and w["source_url"]==p["source_url"],"witness source")
 check(p["acquisition_run_id"]==40890865709 and p["manual_source_image_collation_run_id"]==40891158390,"runs")
 check(w["source_pages_checked"]==[4,5,6,7] and len(w["manually_collated_pages"])==4,"page controls")
 known={
 4:("d56640d9769b9b4577a036f1ad253b6dedf734051bcad17f7013a20cf918aa53","d47e121b242545e070a172cffb2d1811b12557fca32f27a025a2a51a47674ded"),
 5:("be46253a9e90c9504b2ad9dc2b6ef64fb8b97437c64b1e6547668738b4ce3ff2","3d3e4cb43ee40d9642079ba9d1caf36c9894a638ceb7e417a0c18a5b9dbca89e"),
 6:("822ea8564a0b3e8c900f37816f07f536a448282604b42d050667974cf3fdd929","0031d27106efbdc534f1b4043ebfdf5e9ea708cd07e590d99034c2fed7d2b283"),
 7:("20825351e8483b325d5e202b5bafa09037673864c3d2da17d80ef4682eef3133","b1e6e6065b9816ee8abbfb31ca36304a8af01c730a79275237116af0d9511e1f")}
 for z in w["manually_collated_pages"]:
  check((z["sha256"],z["rgb_sha256"])==known[z["page"]],"source original pixel hashes")
 check(w["manually_collated_pages"][2]["grade"]=="DIRECT_SOURCE_IMAGE_TARGET_POSITIVE","target page6")
 for q in ("日轉限一十二限二十","轉中限一百六十八限○八三○六○","朔轉限二十四限一○七一一四六","弦轉限九十○限○六八三○八六五"):
  check(q in w["original_phrases_p6"] and q in w["manually_collated_pages"][2]["literal"],"missing target original glyph:"+q)
 rates=[("轉中限",F(275546,2),F("168.083060")),("朔轉限",F(1975993,100),F("24.1071146")),("弦轉限",F(29530593,400),F("90.06830865"))]
 check(len(e["arithmetic_controls"])==3,"three")
 for c,(name,inp,output) in zip(e["arithmetic_controls"],rates):
  check(c["name"]==name and F(c["base_units"])==inp and F(c["exact_received_limit"])==output,"source-replay control")
  check(inp*F(61,5)/F(10000)==output,"printed source rate mismatch")
  check(inp/F(820)!=output,"exact820 not same source printed constant")
 for k in ("physical_copy_catalog_identity_bound","edition_impression_date_bound"):
  check(p[k] is False and w[k] is False,"false edition claim")
 check(p["new_independent_physical_witnesses"]==0 and p["new_source_registry_entry_in_this_batch"] is False,"duplicate source")
 check(x["hash_bound_source_original_three_constants"] is True and x["original_printed_12_20_daily_rate"] is True,"direct positive")
 check(x["received_13ks_three_constants_exactly_match_this_printed_source"] is True,"cross-source equality")
 for k in ("period_83_84_limit_index_equivalence_proven","source_dated_ancient_calendar_worked_example","ancient_0_1_index_base_selected","source_impression_1739_proven","huang_ming_copy_lineage_proven"):
  check(x[k] is False,"false historical promotion:"+k)
 check(x["original_g893_six_numeric_winners"]==x["new_independent_physical_witnesses"]==x["chart_algorithm_reopens"]==0 and x["chart_product"]=="CLOSED","algorithm gate")
 check(e["counts"]==dict(source_registry=765,matrix_rows=222,graph_nodes=252,graph_edges=238,open_risks=11),"frozen counts")
 check(not e["transmission_impact"]["edges_supported"] and not e["transmission_impact"]["edges_revised"],"no copied edge")
 h=state["historical_audit"];i=state["invariants"]
 check(state["schema_version"]==h["research_omission_guard"]["reviewed_state_version"]==ledger["binding"]["reviewed_state_version"],"state sync")
 check(ledger["binding"]["source_focus_count"]==len(h["current_focus"]) and ledger["binding"]["latest_research_focus_prefix"]=="13KT","focus reviewed")
 check(h["current_focus"][-1].startswith("13KT ") and h["external_source_registry_total_unique_count"]==765,"focus and source counts")
 check(i["deterministic_fusion_chart_product_r1"]=="CLOSED" and i["algorithm_reopen_count"]==0,"product")
 issue=next(j for j in ledger["issues"] if j["id"]=="TW-OPEN-0005")
 check(issue["status"]=="OPEN" and E in issue["source_refs"] and E.replace(".json",".md") in issue["source_refs"],"open issue refs")
 check(any(z.get("revision_id")=="TW-OPEN-0005-13KT-HARVARD-ORIGINAL-20261029" and E in z.get("evidence_refs",[]) for z in issue["history"]),"forward event")
 check(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and len(ledger["issues"])==11,"review")
 return {"status":"PASS","source_pdf_sha256":p["source_sha256"],"source_original_target_page":6,"original_limit_constants":3,"new_physical_votes":0,"historic_g893_winners":0,"chart_reopens":0}
if __name__=="__main__":print(json.dumps(verify(*read()),ensure_ascii=False))
