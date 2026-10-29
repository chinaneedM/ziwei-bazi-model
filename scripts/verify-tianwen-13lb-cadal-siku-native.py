#!/usr/bin/env python3
"""13LB native source hash and cross-witness arithmetic replay; no ancient winner."""
import json
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13LB-CADAL-SIKU-MINGSHI-V35-NATIVE-TARGET-COLLATION-R1.json"
H="docs/research/TIANWEN-13KY-HARVARD-MINGSHI-V11-P7-P9-DIRECT-ORIGINAL-DUAL-GLYPHS-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def check(x,m):
 if not x:raise ValueError(m)
def load():return tuple(json.loads((R/p).read_text(encoding="utf-8")) for p in (E,H,S,L))
def verify(e,harvard,state,ledger):
 check(e["schema"]=="TIANWEN-13LB-CADAL-SIKU-MINGSHI-V35-NATIVE-TARGET-COLLATION-R1" and e["issue_id"]=="TW-OPEN-0005","schema")
 s=e["source"]
 check(s["source_id"]=="CADAL06056956" and s["bytes"]==4528817 and s["pages"]==126,"source identity")
 check(s["sha1"]=="45fc977d134b07689391907d6671eac3c0b7eedb" and s["sha256"]=="98a65bbecf7f07fc8b7dbf3307ae2e2ee8888d0b7c7d841161c944e2ea3b9759","source hashes")
 check(s["original_acquisition_run_id"]==40972015901 and s["native_page_acquisition_run_id"]==40975329477 and s["native_page_artifact_id"]==12942167755,"Actions receipts")
 check(s["source_native_method"].startswith("ddjvu") and s["edition_impression_authenticated"] is False and s["physical_holding_accession_bound"] is False,"grade")
 rows=e["original_pages"]
 known=[
 (2,[770,1036],"6a463784c00de032774d0897e3ec9cd048a3c305c7d4a22bea70b7c6a19eec03",[470,88,700,500],"f11b8d11cc9a483e38ac2857eee72bdd6b18178b2618d4e330fa3e2a79136cfa","欽定四庫全書／明史卷三十五／志第十一／曆五"),
 (11,[806,1041],"e5fa19144c47b0024f566dea039f0a58bdecd9478801433c90830d832a10daaf",[106,116,240,932],"abc8187276d9a5fdf5c4605683e7f812480034704fa416afee4c88edbb353a58","有閏加二十八萬八九七七○九"),
 (16,[781,1056],"a96ec654d33b8f0fc1721cbeab0b1bcff56e13a30c512a108e9f303d56fb1caa",[370,108,468,947],"76ef540f88ea91512c0d45e18a7e75925d6506cfa9234df93d45294332d1f5c3","推遲疾限各置遲疾歷以日轉限乘之即得限數")]
 check(len(rows)==3,"source rows")
 for a,(p,dim,rgb,roi,hashroi,lit) in zip(rows,known):
  check((a["page"],a["size"],a["full_rgb_sha256"],a["roi_xyxy"],a["roi_rgb_sha256"],a["original_literal"])==(p,dim,rgb,roi,hashroi,lit),"original page/ROI/reading")
  check(len(a["full_png_sha256"])==64,"page PNG hash")
 h=harvard["source_native_page_collations"];c=e["cross_witness"]
 check(c["harvard_original_p7"]==h[0]["positive_glyph"]=="有閏加二十三萬八九七七○九","Harvard original 23")
 check(c["harvard_original_p9"]==h[1]["positive_glyph"]==c["siku_original_p16"]==rows[2]["original_literal"],"original operator")
 check(c["siku_original_p11"]==rows[1]["original_literal"] and c["same_operator_glyph_in_two_digital_origins"] is True,"siku direct original 28")
 check(c["independent_physical_editions_attested"] is False and c["historical_copying_lineage_proven"] is False,"physical historical scope")
 a=e["arithmetic"];m=F(a["synodic_month"]);mod=F(a["modulus"])
 check(m==F("295305.93") and mod==600000 and a["count"]==13,"base")
 remainder=13*m-(13*m//mod)*mod
 check(remainder==F(a["harvard_original_remainder"])==F("238977.09"),"exact source replay")
 check(F(a["siku_original_remainder"])==F("288977.09") and F(a["siku_original_remainder"])-remainder==F(a["source_discrepancy_units"])==50000,"difference")
 check(a["day_base"]==10000 and F(a["difference_day_base_equivalent"])==5 and a["historical_date_to_limit_worked_example_found"] is False,"historical date boundary")
 b=e["boundaries"]
 for key in ("source_original_1739_impression_proven","physical_holding_accession_authenticated","shared_harvard_siku_impression_proven","ancient_scribal_error_cause_proven","original_historic_83_84_index_proven","original_historic_167_168_mechanics_proven"):check(b[key] is False,"false edition/rule award "+key)
 for key in ("original_g893_six_numeric_winners","new_physical_witness_votes","new_external_registry_entries","graph_nodes_added","graph_edges_added","algorithm_reopens"):check(b[key]==0,"unearned count "+key)
 check(b["source_title_self_label_attested"] is True and b["siku_original_numeric_288977_attested"] is True and b["siku_original_chiji_attested"] is True and b["product"]=="CLOSED" and b["open_risks"]==11,"bounds")
 check(e["counts"]==dict(root=647,extensions=118,total=765,matrix=222,graph_nodes=252,graph_edges=238,open=11),"counts")
 check(not e["transmission_impact"]["edges_supported"] and not e["transmission_impact"]["edges_revised"],"transmission")
 hs=state["historical_audit"];li=ledger["binding"];inv=state["invariants"]
 check(state["schema_version"]==hs["research_omission_guard"]["reviewed_state_version"]==li["reviewed_state_version"],"handoff")
 check(hs["external_source_registry_total_unique_count"]==765 and hs["row_count"]==hs["audited_row_count"]==222 and inv["deterministic_fusion_chart_product_r1"]=="CLOSED" and inv["algorithm_reopen_count"]==0,"product")
 check(hs["current_focus"][-1].startswith("13LB ") and li["latest_research_focus_prefix"]=="13LB" and li["source_focus_count"]==len(hs["current_focus"]),"focus")
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 check(issue["priority"]=="P0" and issue["status"]=="OPEN" and E in issue["source_refs"] and E.replace(".json",".md") in issue["source_refs"],"issue")
 check(any(x.get("revision_id")=="TW-OPEN-0005-13LB-SIKU-NATIVE-20261030" and E in x.get("evidence_refs",[]) for x in issue["history"]),"forward revision")
 check(len(ledger["issues"])==11 and ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"],"risk review")
 return {"status":"PASS","native_original_pages":[2,11,16],"original_siku_remainder":"288977.09","original_harvard_remainder":"238977.09","delta_units":50000,"historical_winners":0,"chart_reopens":0}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
