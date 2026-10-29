#!/usr/bin/env python3
"""13KU: four quarter-turn limit residues; protect printed/received boundary."""
import json
from pathlib import Path
from fractions import Fraction as F

ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13KU-MINGSHI-V35-FOUR-PHASE-RETURN-AND-RECEIVED-OPERATOR-R1.json"
ORIGINAL="docs/research/TIANWEN-13KT-HARVARD-MINGSHI-V11-J35-DIRECT-ORIGINAL-THREE-CONSTANTS-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def require(test,message):
 if not test:raise ValueError(message)
def read():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (E,ORIGINAL,STATE,LEDGER))
def verify(e,prior,state,ledger):
 require(e["schema"]=="TIANWEN-13KU-MINGSHI-V35-FOUR-PHASE-RETURN-AND-RECEIVED-OPERATOR-R1" and e["issue_id"]=="TW-OPEN-0005","identity")
 o=e["original_source"]; r=e["received_operator"];a=e["rational_basis"]
 require(o["earlier_evidence"]==ORIGINAL and o["source_pdf_sha256"]==prior["provenance"]["source_sha256"]=="36a2a99461d9d16a71e203d95ffa6cac189f1bbab94295de51ed6d3b60bd649b","source bound")
 require(o["original_target_pdf_page"]==6 and o["original_target_literals"]==prior["witness"]["original_phrases_p6"][3:7],"original p6 literals")
 require(o["source_page_p7_to_p12_native_operator_collation_this_batch"] is False and o["exact_physical_impression_or_1739_date_proven"] is False and o["new_independent_physical_witnesses"]==0,"no fabricated original source")
 require(r["source_id"]=="EXT-WIKISOURCE-MINGSHI-V35-DATONG-TIME" and r["source_url"]=="https://zh.wikisource.org/wiki/明史/卷35","received source")
 require(r["arithmetic_text_graded_received_only"] is True and r["independent_source_native_page_confirmation_of_this_full_phrase"] is False,"received grade")
 require(all(s in r["operative_phrase"] for s in ("以日轉限乘","以弦轉限累加","滿轉中限去之","以朔轉限加之")),"operator atom")
 require(a["day_units"]==10000 and a["daily_limit_rate"]=="61/5" and a["exact_820_unit_rate"]=="500/41","daily basis")
 require(a["full_turn_units"]=="275546" and a["middle_turn_units"]=="137773" and a["synodic_period_units"]=="29530593/100" and a["synodic_turn_difference_units"]=="1975993/100","source units")
 rate=F(a["daily_limit_rate"]); h=F(a["middle_turn_limit"]);q=F(a["quarter_turn_limit"]);s=F(a["synodic_turn_limit"])
 require(h==F(a["middle_turn_units"])*rate/10000==F(prior["arithmetic_controls"][0]["exact_received_limit"]),"H replay")
 require(q==F(a["synodic_period_units"])/4*rate/10000==F(prior["arithmetic_controls"][2]["exact_received_limit"]),"quarter replay")
 require(s==F(a["synodic_turn_difference_units"])*rate/10000==F(prior["arithmetic_controls"][1]["exact_received_limit"]),"synodic replay")
 require(F(a["synodic_period_units"])-F(a["full_turn_units"])==F(a["synodic_turn_difference_units"]),"base-unit identity")
 require(4*q-2*h==s and s==F("24.1071146") and h!=168,"phase return proof")
 rows=e["conditional_four_phase_replay"]
 require(len(rows)==5,"five model rows")
 for k,row in enumerate(rows):
  value=k*q; n=value//h; residual=value-n*h
  require(row["phase_index"]==k and F(row["raw_cumulative_limit"])==value and row["half_turns_removed"]==n and F(row["residual_limit"])==residual,"phase row "+str(k))
  require(row["parity"]==("EVEN" if n%2==0 else "ODD"),"parity "+str(k))
 require(rows[4]["half_turns_removed"]==2 and F(rows[4]["residual_limit"])==s,"quarter return")
 m=e["mathematical_result"];require(F(m["four_times_quarter_minus_two_times_middle"])==s and F(m["direct_synodic_limit"])==s and m["exact_equality"] is True,"recorded result")
 require(m["threshold_168_integer_vs_middle_168_083060_distinct"] is True and m["phase_quotient_parity_a_conditional_model_only"] is True,"semantic scope")
 b=e["boundaries"]
 for key in ("dated_original_historic_calendar_example_found","source_specific_integer_floor_or_carry_attested","huang_vs_ming_83_84_or_167_168_mechanical_equivalence_proven","historic_zero_or_one_base_selected","historical_168_integer_is_identical_to_168_083060_middle_period"):
  require(b[key] is False,"unearned historical award "+key)
 for key in ("new_original_full_operator_glyphs_verified","historic_g893_six_numeric_winners","new_source_registry_entries","transmission_graph_nodes_added","transmission_graph_edges_supported","chart_algorithm_reopens"):
  require(b[key]==0,"unearned count "+key)
 require(b["deterministic_chart_product"]=="CLOSED" and b["remaining_open_risks"]==11,"scope")
 require(not e["transmission_impact"]["edges_supported"] and not e["transmission_impact"]["edges_revised"],"unsupported genealogy")
 ha=state["historical_audit"];i=state["invariants"];bind=ledger["binding"]
 require(state["schema_version"]==ha["research_omission_guard"]["reviewed_state_version"]==bind["reviewed_state_version"],"state review")
 require(bind["source_focus_count"]==len(ha["current_focus"]) and bind["latest_research_focus_prefix"]==ha["current_focus"][-1].split(" ")[0],"focus sync")
 require(any(x.startswith("13KT ") for x in ha["current_focus"]) and ha["current_focus"][-1].startswith("13KU "),"forward focus")
 require(ha["external_source_registry_total_unique_count"]==765 and ha["row_count"]==ha["audited_row_count"]==222,"source and matrix")
 require(i["deterministic_fusion_chart_product_r1"]=="CLOSED" and i["algorithm_reopen_count"]==0,"product frozen")
 issue=next(v for v in ledger["issues"] if v["id"]=="TW-OPEN-0005")
 require(issue["priority"]=="P0" and issue["status"]=="OPEN" and E in issue["source_refs"] and E.replace(".json",".md") in issue["source_refs"],"open source refs")
 require(any(x.get("revision_id")=="TW-OPEN-0005-13KU-FOUR-PHASE-20261030" and E in x.get("evidence_refs",[]) for x in issue["history"]),"forward revision")
 require(len(ledger["issues"])==11 and ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"],"checkpoint")
 return {"status":"PASS","four_quarters_minus_two_half_turns":str(s),"phase_cases":5,"new_original_operator_pages":0,"historic_winners":0,"chart_reopens":0}
if __name__=="__main__":print(json.dumps(verify(*read()),ensure_ascii=False))
