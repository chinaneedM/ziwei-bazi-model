#!/usr/bin/env python3
"""13KV: received variants, exact 12/13 lunation remainders, no original-glyph award."""
import json
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13KV-MINGSHI-V35-THIRTEEN-SYNODIC-REM-RUBRIC-RECEIVED-VARIANTS-R1.json"
PRIOR="docs/research/TIANWEN-13KT-HARVARD-MINGSHI-V11-J35-DIRECT-ORIGINAL-THREE-CONSTANTS-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def check(ok,msg):
 if not ok:raise ValueError(msg)
def read():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (E,PRIOR,STATE,LEDGER))
def verify(e,prior,state,ledger):
 check(e["schema"]=="TIANWEN-13KV-MINGSHI-V35-THIRTEEN-SYNODIC-REM-RUBRIC-RECEIVED-VARIANTS-R1" and e["issue_id"]=="TW-OPEN-0005","schema")
 s=e["sources"];common=s["common_received"];siku=s["siku_received"];orig=e["original_constant_control"]
 check(common["source_id"]=="EXT-WIKISOURCE-MINGSHI-V35-DATONG-TIME" and common["url"]=="https://zh.wikisource.org/wiki/明史/卷35","common received identity")
 check(siku["url"]=="https://zh.wikisource.org/wiki/明史_(四庫全書本)/卷035" and not siku["separate_physical_original_authenticated"] and not siku["independent_textual_stemma_proven"],"unproven Siku original")
 check(common["phrase_month_13"]=="有閏，加二十三萬八九七七零九" and siku["phrase_month_13"]=="有閏加二十八萬八九七七○九","exact received 13m variants")
 check(common["phrase_month_12"]==siku["phrase_month_12"]=="無閏加五十四萬三六七一一六","12m common control")
 check(common["phrase_divisor"]==siku["phrase_divisor"]=="紀法六十萬" and common["phrase_operator"]==siku["phrase_operator"]=="十三朔實去紀法","modular divisor source")
 check(common["phrase_limit_subject"]=="推遲疾限　各置遲次歷" and siku["phrase_limit_subject"]=="推遲疾限　各置遲疾歴","chici/chiji witness")
 check(orig["evidence_doc"]==PRIOR and orig["harvard_v11_page6_pdf_sha256"]==prior["provenance"]["source_sha256"],"prior hash")
 check(orig["source_original_p6_phrase"] in prior["witness"]["original_phrases_p6"] and orig["source_original_p6_phrase"]=="朔策二十九萬五千三百○五分九十三秒","original lunar period")
 check(orig["ancient_edition_or_impression_identity_bound"] is False and orig["original_harvard_v11_page_with_13_month_remainder_directly_verified_this_batch"] is False,"no new original")
 a=e["exact_arithmetic"];m=F(a["source_succeeding_moon_base_units"]);c=F(a["period_divisor_units"])
 check(m==F(29530593,100) and c==600000 and a["count_ordinary_months"]==12 and a["count_leap_months"]==13,"units")
 q12=(12*m)//c; r12=12*m-q12*c
 q13=(13*m)//c; r13=13*m-q13*c
 check(q12==5 and q13==6 and r12==F("543671.16") and r13==F("238977.09"),"strict fraction")
 check(F(a["ordinary_year_full_input"])==12*m and F(a["leap_year_full_input"])==13*m,"unreduced totals")
 check(a["ordinary_year_quotient"]==q12 and a["leap_year_quotient"]==q13 and F(a["ordinary_year_remainder"])==r12 and F(a["leap_year_remainder"])==r13,"recorded remainders")
 check(F(a["ordinary_received_leap_remainder"])==r13 and F(a["siku_received_leap_remainder"])==F("288977.09"),"both transcriptions")
 check(F(a["ordinary_received_leap_remainder"])!=F(a["siku_received_leap_remainder"]),"variant distinct")
 diff=F(a["siku_received_leap_remainder"])-r13
 check(diff==F(a["discrepancy_units"])==50000 and F(a["daily_base_units"])==10000 and diff/10000==F(a["discrepancy_daily_unit_equivalent"])==5,"bounded delta")
 check(a["strictly_internal_calculation_not_ancient_example"] is True,"no dated oracle")
 p=e["philological_controls"]
 check(p["ordinary_subject"]=="遲次歷" and p["siku_subject"]=="遲疾歴" and p["preceding_and_following_context_both_use_chiji"] is True,"subject contrast")
 check(p["interpretation"].startswith("VARIANT_OR_TRANSCRIPTION_NO_WINNER") and p["independent_source_native_image_original_glyph_p7_to_p12_verified"] is False and p["different_reading_may_not_be_silently_corrected"] is True,"textual winner gate")
 b=e["adjudication"]
 for k in ("arithmetic_13_month_remainder_matches_registered_common_received","arithmetic_13_month_remainder_does_not_match_siku_web_transcription","arithmetic_12_month_remainder_matches_both_web_transcriptions"):check(b[k] is True,"internal arithmetic result "+k)
 for k in ("modern_transcription_typo_proven","historical_siku_physical_edition_original_glyph_proven","historic_calendar_date_or_epoch_full_mechanical_example_collected","original_source_specific_rounding_convention_attested","two_web_pages_count_as_two_independent_physical_witnesses","historic_zero_one_index_for_83_84_proven"):check(b[k] is False,"false source winner "+k)
 for k in ("g893_six_historic_numeric_winners","new_independent_source_registry_entries","matrix_rows_changed","new_graph_nodes","new_graph_edges","algorithm_reopens"):check(b[k]==0,"false historical count "+k)
 check(b["product"]=="CLOSED" and b["open_risks"]==11 and e["counters"]==dict(registered_sources=765,matrix_rows=222,graph_nodes=252,graph_edges=238,unresolved_research_issues=11),"fixed research counts")
 check(not e["transmission_impact"]["edges_supported"] and not e["transmission_impact"]["edges_revised"],"no lineage")
 h=state["historical_audit"];i=state["invariants"];binding=ledger["binding"]
 check(state["schema_version"]==h["research_omission_guard"]["reviewed_state_version"]==binding["reviewed_state_version"],"state synchronization")
 check(h["external_source_registry_total_unique_count"]==765 and h["row_count"]==h["audited_row_count"]==222 and i["algorithm_reopen_count"]==0 and i["deterministic_fusion_chart_product_r1"]=="CLOSED","closure")
 check(any(x.startswith("13KU ") for x in h["current_focus"]) and any(x.startswith("13KV ") for x in h["current_focus"]),"research continuity")
 check(binding["source_focus_count"]==len(h["current_focus"]) and binding["latest_research_focus_prefix"]==h["current_focus"][-1].split(" ")[0],"current focus")
 issue=next(x for x in ledger["issues"] if x["id"]==e["issue_id"])
 check(issue["status"]=="OPEN" and issue["priority"]=="P0" and E in issue["source_refs"] and E.replace(".json",".md") in issue["source_refs"],"issue binding")
 check(any(z.get("revision_id")=="TW-OPEN-0005-13KV-RECEIVED-THIRTEEN-MOON-20261030" and E in z.get("evidence_refs",[]) for z in issue["history"]),"append only")
 check(len(ledger["issues"])==11 and ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"],"checkpoint")
 return {"status":"PASS","leap_13_remainder":str(r13),"difference":str(diff),"twelve_month_remainder":str(r12),"original_operator_glyphs_this_batch":0,"chart_reopens":0}
if __name__=="__main__":print(json.dumps(verify(*read()),ensure_ascii=False))
