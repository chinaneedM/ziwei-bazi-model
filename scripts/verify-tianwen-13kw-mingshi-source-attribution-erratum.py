#!/usr/bin/env python3
"""13KW: forward-only correction for a mismatched 13KU received-source quotation."""
import json
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13KW-MINGSHI-V35-13KU-SOURCE-ATTRIBUTION-FORWARD-ERRATUM-R1.json"
OLD="docs/research/TIANWEN-13KU-MINGSHI-V35-FOUR-PHASE-RETURN-AND-RECEIVED-OPERATOR-R1.json"
V="docs/research/TIANWEN-13KV-MINGSHI-V35-THIRTEEN-SYNODIC-REM-RUBRIC-RECEIVED-VARIANTS-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def need(ok,msg):
 if not ok:raise ValueError(msg)
def read():
 return tuple(json.loads((ROOT/path).read_text(encoding="utf-8")) for path in (E,OLD,V,S,L))
def verify(e,old,v,state,ledger):
 need(e["schema"]=="TIANWEN-13KW-MINGSHI-V35-13KU-SOURCE-ATTRIBUTION-FORWARD-ERRATUM-R1" and e["issue_id"]=="TW-OPEN-0005","schema")
 need(e["transition"]=="FORWARD_ONLY_SOURCE_ATTRIBUTION_ERRATUM_NO_PREVIOUS_EVIDENCE_REWRITE","transition")
 need(e["prior_evidence_file"]==OLD and e["prior_field"]=="received_operator.operative_phrase","path")
 need(e["prior_source_id"]==old["received_operator"]["source_id"]=="EXT-WIKISOURCE-MINGSHI-V35-DATONG-TIME","registered source")
 need(e["prior_source_url"]==old["received_operator"]["source_url"]=="https://zh.wikisource.org/wiki/明史/卷35","old locator")
 need(e["prior_published_quote_preserved"]==old["received_operator"]["operative_phrase"],"immutable old phrase")
 need("各置遲疾歷" in e["prior_published_quote_preserved"],"old misquotation subject")
 correction=e["correction"]
 need(correction["ordinary_url"]==v["sources"]["common_received"]["url"]==e["prior_source_url"],"ordinary URL")
 need(correction["ordinary_received_exact_subject"]==v["sources"]["common_received"]["phrase_limit_subject"]=="推遲疾限　各置遲次歷","common actual received")
 need(correction["another_received_url"]==v["sources"]["siku_received"]["url"],"Siku URL")
 need(correction["siku_received_exact_subject"]==v["sources"]["siku_received"]["phrase_limit_subject"]=="推遲疾限　各置遲疾歴","Siku actual received")
 need(correction["first_forward_notice"]==V and correction["current_erratum_not_retroactive_edition_winner"] is True and correction["previous_13ku_json_and_md_kept_unmodified"] is True,"append only")
 need(correction["two_website_transcriptions_not_two_ancient_physical_copies"] is True,"witness count")
 for k in ("full_original_harvard_p7_to_p12_operator_native_glyph_verified","siku_edition_original_subject_glyph_verified"):
  need(correction[k] is False,"false original grade "+k)
 arithmetic=e["arithmetic_invariance"]
 need(F(arithmetic["prior_13ku_exact_four_quarters_minus_two_half_turns"])==4*F(old["rational_basis"]["quarter_turn_limit"])-2*F(old["rational_basis"]["middle_turn_limit"])==F(old["rational_basis"]["synodic_turn_limit"]),"old arithmetic")
 need(arithmetic["prior_13ku_math_unchanged"] is True and arithmetic["newly_proven_historical_index_or_rounding_rule"] is False and arithmetic["no_new_source_numeric_control_from_erratum"] is True,"math unchanged")
 b=e["bounded_consequence"]
 need(b["report_old_literal_as_misassigned_not_as_a_verified_quote"] is True and b["correct_source_ordinary_reading_to_chici"]=="遲次歷" and b["preserve_distinct_siku_received_reading"]=="遲疾歴","quotation correction")
 for k in ("historical_winner_selected","confirmed_chart_implementation_defect"):
  need(b[k] is False,"unearned winner")
 for k in ("source_registry_new_entries","historic_g893_six_winners","new_transmission_nodes","new_transmission_edges","algorithm_reopens"):
  need(b[k]==0,"unearned counts "+k)
 need(b["chart_product"]=="CLOSED" and b["risk_items_remaining_open"]==11,"scope")
 need(e["counts"]==dict(registry=765,matrix=222,graph_nodes=252,graph_edges=238,open_issues=11),"counts")
 need(not e["transmission_impact"]["edges_supported"] and not e["transmission_impact"]["edges_revised"],"genealogy")
 h=state["historical_audit"];i=state["invariants"];binding=ledger["binding"]
 need(state["schema_version"]==h["research_omission_guard"]["reviewed_state_version"]==binding["reviewed_state_version"],"sync")
 need(any(z.startswith("13KU ") for z in h["current_focus"]) and any(z.startswith("13KV ") for z in h["current_focus"]) and any(z.startswith("13KW ") for z in h["current_focus"]),"research forward")
 need(binding["source_focus_count"]==len(h["current_focus"]) and binding["latest_research_focus_prefix"]==h["current_focus"][-1].split(" ")[0],"latest focus")
 need(h["external_source_registry_total_unique_count"]==765 and h["row_count"]==h["audited_row_count"]==222 and i["algorithm_reopen_count"]==0 and i["deterministic_fusion_chart_product_r1"]=="CLOSED","counts chart")
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 need(issue["priority"]=="P0" and issue["status"]=="OPEN" and E in issue["source_refs"] and E.replace(".json",".md") in issue["source_refs"],"issue references")
 need(any(z.get("revision_id")=="TW-OPEN-0005-13KW-SOURCE-ATTRIBUTION-ERRATUM-20261030" and E in z.get("evidence_refs",[]) for z in issue["history"]),"erratum event")
 need(len(ledger["issues"])==11 and ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"],"checkpoint")
 return {"status":"PASS","corrected_source_subject":"遲次歷","preserved_siku_subject":"遲疾歴","prior_quote_immutable":True,"original_glyph_winners":0,"algorithm_reopens":0}
if __name__=="__main__":print(json.dumps(verify(*read()),ensure_ascii=False))
